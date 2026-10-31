import json
import os
import sys
import unittest

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)

try:
    import mongomock
except ImportError:  # pragma: no cover - mongomock is a dev dependency
    mongomock = None

from core.normalizer import normalize_many  # noqa: E402

FIXTURES = os.path.join(BASE, "tests", "fixtures")


def load(source):
    with open(os.path.join(FIXTURES, f"{source}_data.json"), encoding="utf-8") as handle:
        return json.load(handle)


@unittest.skipIf(mongomock is None, "mongomock is not installed (pip install -r requirements-dev.txt)")
class SyncTests(unittest.TestCase):
    def setUp(self):
        from database import db

        self.db = db
        db.set_client(mongomock.MongoClient(tz_aware=True))
        self.database = db.get_db()
        self.programs = normalize_many("bugcrowd", load("bugcrowd"))

    def tearDown(self):
        self.database.client.close()
        self.db.set_client(None)

    def test_first_sync_inserts_and_creates_program_added_alerts(self):
        summary = self.db.sync_programs("bugcrowd", self.programs)
        self.assertEqual(summary["inserted"], len(self.programs))
        self.assertEqual(summary["updated"], 0)
        self.assertEqual(len(summary["changes"]), len(self.programs))
        self.assertEqual({c["type"] for c in summary["changes"]}, {"program_added"})
        self.assertEqual(self.database["programs"].count_documents({}), len(self.programs))

    def test_second_sync_is_idempotent(self):
        self.db.sync_programs("bugcrowd", self.programs)
        summary = self.db.sync_programs("bugcrowd", self.programs)
        self.assertEqual(summary["inserted"], 0)
        self.assertEqual(summary["updated"], 0)
        self.assertEqual(summary["changes"], [])
        self.assertEqual(summary["unchanged"], len(self.programs))

    def test_new_scope_is_detected_on_next_sync(self):
        self.db.sync_programs("bugcrowd", self.programs)

        changed = json.loads(json.dumps(self.programs))
        changed[0]["scopes"].append("new-target.example.com")
        summary = self.db.sync_programs("bugcrowd", changed)

        self.assertEqual(summary["updated"], 1)
        types = {(c["type"], c["target"]) for c in summary["changes"]}
        self.assertIn(("scope_added", "new-target.example.com"), types)

        stored = self.database["programs"].find_one({"source": "bugcrowd", "slug": changed[0]["slug"]})
        self.assertIn("new-target.example.com", stored["scopes"])

    def test_program_missing_from_snapshot_is_deactivated(self):
        self.db.sync_programs("bugcrowd", self.programs)
        summary = self.db.sync_programs("bugcrowd", self.programs[:-1])

        self.assertEqual(summary["deactivated"], 1)
        removed = [c for c in summary["changes"] if c["type"] == "program_removed"]
        self.assertEqual(len(removed), 1)

        stored = self.database["programs"].find_one(
            {"source": "bugcrowd", "slug": self.programs[-1]["slug"]}
        )
        self.assertFalse(stored["active"])

    def test_changes_are_persisted_and_can_be_marked_notified(self):
        summary = self.db.sync_programs("bugcrowd", self.programs)
        ids = [change["_id"] for change in summary["changes"]]
        self.assertTrue(ids)

        stored = self.database["changes"].count_documents({})
        self.assertEqual(stored, len(ids))

        modified = self.db.mark_notified(ids)
        self.assertEqual(modified, len(ids))
        self.assertEqual(self.database["changes"].count_documents({"notified": True}), len(ids))

    def test_sync_run_is_recorded(self):
        summary = self.db.sync_programs("bugcrowd", self.programs)
        self.assertIn("run_id", summary)
        run = self.database["sync_runs"].find_one({"_id": summary["run_id"]})
        self.assertEqual(run["status"], "success")
        self.assertEqual(run["stats"]["inserted"], len(self.programs))


if __name__ == "__main__":
    unittest.main()
