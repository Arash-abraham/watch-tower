import argparse
import os
import sys
import unittest
from unittest.mock import call, patch

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

    def test_failed_channel_retries_on_next_sync_without_resending_successful_channel(self):
        args = make_args(input_dir=os.path.join(BASE, "tests", "fixtures"), no_notify=False)
        settings = {
            "NOTIFY_MAX_ITEMS": 2, "NOTIFY_ON_FIRST_SEEN": True,
            "TELEGRAM_BOT_TOKEN": "token", "TELEGRAM_CHAT_ID": "-123", "DISCORD_WEBHOOK_URL": "https://example.invalid",
        }
        with patch.dict(monitor.config, settings), patch.object(monitor.notifier, "send") as send:
            send.side_effect = lambda channel, _text: channel == "telegram"
            self.assertEqual(monitor.run_once(["bugcrowd"], args), 1)
            collection = self.db.get_db()["changes"]
            self.assertEqual(collection.count_documents({"notification_pending": ["discord"], "notified": False}), 5)
            self.assertEqual([c.args[0] for c in send.call_args_list], ["telegram"] * 3 + ["discord"])
            sent_text = "\n".join(c.args[1] for c in send.call_args_list if c.args[0] == "telegram")
            for event in collection.find():
                self.assertIn(event["program_name"], sent_text)

            send.reset_mock(side_effect=True)
            send.return_value = True
            self.assertEqual(monitor.run_once(["bugcrowd"], args), 0)
            self.assertEqual([c.args[0] for c in send.call_args_list], ["discord"] * 3)
            self.assertEqual(collection.count_documents({"notification_pending": [], "notified": True}), 5)

    def test_suppressed_first_seen_alerts_are_recorded_but_not_queued(self):
        args = make_args(input_dir=os.path.join(BASE, "tests", "fixtures"), no_notify=False)
        with patch.dict(monitor.config, {"NOTIFY_ON_FIRST_SEEN": False}), \
             patch.object(monitor.notifier, "configured_channels", return_value=("telegram",)), \
             patch.object(monitor.notifier, "send") as send:
            self.assertEqual(monitor.run_once(["hackerone"], args), 0)
        send.assert_not_called()
        changes = self.db.get_db()["changes"]
        self.assertGreater(changes.count_documents({"type": "program_added", "notified": False}), 0)
        self.assertEqual(changes.count_documents({"notification_pending": {"$exists": True}}), 0)

    @patch.object(monitor, "deliver_notifications")
    def test_dry_run_and_no_notify_do_not_drain_queue(self, deliver):
        for overrides in ({"dry_run": True, "no_notify": False}, {"no_notify": True}):
            self.assertEqual(monitor.run_once([], make_args(**overrides)), 0)
        deliver.assert_not_called()


class NotificationCommandTests(unittest.TestCase):
    @patch.object(monitor.db, "get_db", side_effect=AssertionError("unexpected database access"))
    @patch.object(monitor.notifier, "configured_channels", return_value=("telegram", "discord"))
    @patch.object(monitor.notifier, "send", side_effect=[False, True])
    def test_test_command_checks_both_channels_without_a_database(self, send, _channels, _get_db):
        self.assertEqual(monitor.main(["--test-notifications"]), 1)
        message = "WATCH TOWER — notification test"
        self.assertEqual(send.call_args_list, [call("telegram", message), call("discord", message)])

    @patch.object(monitor.notifier, "configured_channels", return_value=())
    def test_test_command_fails_without_credentials(self, _channels):
        with self.assertLogs("watchtower", level="ERROR"):
            self.assertEqual(monitor.main(["--test-notifications"]), 1)


if __name__ == "__main__":
    unittest.main()
