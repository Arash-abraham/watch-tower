import unittest
from unittest.mock import Mock, patch

import requests

from config import config
from core import notifier


def response(status, body=None, headers=None):
    reply = Mock(status_code=status, headers=headers or {})
    reply.json.return_value = body
    return reply


class NotifierTests(unittest.TestCase):
    def setUp(self):
        settings = patch.dict(config, {
            "TELEGRAM_BOT_TOKEN": "example-token",
            "TELEGRAM_CHAT_ID": "-123",
            "DISCORD_WEBHOOK_URL": "https://discord.com/api/webhooks/example/token",
        })
        settings.start()
        self.addCleanup(settings.stop)

    def test_long_unicode_lines_are_split_without_truncation(self):
        message = "لینک\n" + "🚀" * 2200 + "\nfinal asset"
        for limit in (notifier.DISCORD_LIMIT, notifier.TELEGRAM_LIMIT):
            with self.subTest(limit=limit):
                chunks = notifier._chunks(message, limit)
                self.assertGreater(len(chunks), 1)
                self.assertTrue(all(0 < len(chunk.encode("utf-16-le")) // 2 <= limit for chunk in chunks))
                self.assertEqual("".join(chunks), message)

    @patch("core.notifier.requests.post")
    def test_telegram_checks_provider_confirmation_and_uses_plain_text(self, post):
        post.side_effect = [response(200, {"ok": False}), response(200, {"ok": True})]
        with self.assertLogs("core.notifier", level="ERROR"):
            self.assertFalse(notifier.send_telegram("_scope_"))
        self.assertTrue(notifier.send_telegram("_scope_"))
        self.assertEqual(post.call_args.args[0], "https://api.telegram.org/botexample-token/sendMessage")
        self.assertEqual(post.call_args.kwargs["json"], {
            "chat_id": "-123", "text": "_scope_", "link_preview_options": {"is_disabled": True},
        })
        self.assertFalse(post.call_args.kwargs["allow_redirects"])

    @patch("core.notifier.time.sleep")
    @patch("core.notifier.requests.post")
    def test_discord_waits_for_delivery_disables_mentions_and_retries_rate_limit(self, post, sleep):
        post.side_effect = [response(429, {"retry_after": 0.25}), response(200, {"id": "123"})]
        self.assertTrue(notifier.send_discord("@everyone"))
        self.assertEqual(post.call_count, 2)
        sleep.assert_called_once_with(0.25)
        self.assertEqual(post.call_args.kwargs["params"], {"wait": "true"})
        self.assertEqual(post.call_args.kwargs["json"]["allowed_mentions"], {"parse": []})

    @patch("core.notifier.requests.post")
    def test_failed_chunk_stops_send_and_credentials_are_not_logged(self, post):
        post.side_effect = requests.ConnectionError(f"connection failed for {config.DISCORD_WEBHOOK_URL}")
        with self.assertLogs("core.notifier", level="ERROR") as logs:
            self.assertFalse(notifier.send_discord("x" * 5000))
        self.assertNotIn(config.DISCORD_WEBHOOK_URL, " ".join(logs.output))
        self.assertEqual(post.call_count, 1)
