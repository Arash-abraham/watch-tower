import argparse
import os
import sys
import unittest

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)

try:
    import mongomock
except ImportError:  # pragma: no cover
    mongomock = None

import monitor  # noqa: E402
from core.sources import SourceError  # noqa: E402


def make_args(**overrides):
    defaults = dict(
        local_dir=None,
        input_dir=None,
        base_url=None,
        max_programs=None,
        dry_run=False,
        no_notify=True,
    )
    defaults.update(overrides)
    return argparse.Namespace(**defaults)


class MonitorTests(unittest.TestCase):
    def setUp(self):
        if mongomock is None:
            self.skipTest("mongomock is required for the failure-recording path")
        from database import db

        db.set_client(mongomock.MongoClient(tz_aware=True))

    def tearDown(self):
        from database import db

        db.get_db().client.close()
        db.set_client(None)

    def test_fixture_directory_is_used_instead_of_the_network(self):
        args = make_args(input_dir=os.path.join(BASE, "tests", "fixtures"), dry_run=True)
        result = monitor.run_source("bugcrowd", args)
        self.assertTrue(result.get("dry_run"))
        self.assertEqual(result["programs"], 5)

    def test_network_failure_is_reported_not_raised(self):
        original = monitor.fetch_source
        monitor.fetch_source = lambda *a, **kw: (_ for _ in ()).throw(SourceError("boom"))
        try:
            result = monitor.run_source("bugcrowd", make_args())
        finally:
            monitor.fetch_source = original

        self.assertEqual(result["error"], "boom")
        self.assertEqual(result["changes"], [])

    def test_run_once_returns_non_zero_when_a_source_fails(self):
        original = monitor.fetch_source
        monitor.fetch_source = lambda *a, **kw: (_ for _ in ()).throw(SourceError("offline"))
        try:
            code = monitor.run_once(["bugcrowd"], make_args(dry_run=True))
        finally:
            monitor.fetch_source = original
        self.assertEqual(code, 1)


@unittest.skipIf(mongomock is None, "mongomock is not installed")
class MonitorDatabaseTests(unittest.TestCase):
    def setUp(self):
        from database import db

        db.set_client(mongomock.MongoClient(tz_aware=True))
        self.db = db

    def tearDown(self):
        self.db.get_db().client.close()
        self.db.set_client(None)

    def test_successful_fixture_sync_persists_programs(self):
        args = make_args(input_dir=os.path.join(BASE, "tests", "fixtures"))
        summary = monitor.run_source("yeswehack", args)
        self.assertNotIn("error", summary)
        self.assertEqual(summary["inserted"], 5)
        self.assertEqual(self.db.get_db()["programs"].count_documents({"source": "yeswehack"}), 5)

    def test_failed_run_is_recorded(self):
        original = monitor.fetch_source
        monitor.fetch_source = lambda *a, **kw: (_ for _ in ()).throw(SourceError("offline"))
        try:
            monitor.run_source("hackerone", make_args())
        finally:
            monitor.fetch_source = original

        run = self.db.get_db()["sync_runs"].find_one({"source": "hackerone"})
        self.assertEqual(run["status"], "failed")
        self.assertIn("offline", run["error"])


if __name__ == "__main__":
    unittest.main()
