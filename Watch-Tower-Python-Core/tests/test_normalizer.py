import json
import os
import sys
import unittest

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)

from core.normalizer import (  # noqa: E402
    normalize_local,
    normalize_many,
    normalize_program,
)

FIXTURES = os.path.join(BASE, "tests", "fixtures")


def load(source):
    with open(os.path.join(FIXTURES, f"{source}_data.json"), encoding="utf-8") as handle:
        return json.load(handle)


class NormalizerTests(unittest.TestCase):
    def test_every_source_produces_the_shared_shape(self):
        required = {
            "source",
            "slug",
            "program_name",
            "program_url",
            "scopes",
            "outScopes",
            "scope_details",
            "asset_types",
            "active",
            "meta",
        }
        for source in ("bugcrowd", "hackerone", "yeswehack", "intigriti"):
            with self.subTest(source=source):
                programs = normalize_many(source, load(source))
                self.assertTrue(programs)
                for program in programs:
                    self.assertTrue(required.issubset(program.keys()))
                    self.assertEqual(program["source"], source)
                    self.assertTrue(program["slug"])
                    self.assertIsInstance(program["scopes"], list)
                    self.assertIsInstance(program["outScopes"], list)

    def test_bugcrowd_slug_comes_from_engagement_url(self):
        program = normalize_many("bugcrowd", load("bugcrowd"))[0]
        self.assertEqual(program["slug"], "ccdata-mbb-og")
        self.assertTrue(any("data-api.coindesk.com" in scope for scope in program["scopes"]))
        self.assertIn("max_payout", program["meta"])

    def test_hackerone_uses_asset_identifier(self):
        program = normalize_many("hackerone", load("hackerone"))[0]
        self.assertEqual(program["slug"], "verisk-vdp")
        self.assertIn("*.verisk.com", program["scopes"])

    def test_intigriti_uses_endpoint_field(self):
        program = normalize_many("intigriti", load("intigriti"))[0]
        self.assertTrue(program["scopes"])
        self.assertEqual(program["scope_details"]["in"][0]["target"], "all")

    def test_out_of_scope_is_kept(self):
        programs = normalize_many("bugcrowd", load("bugcrowd"))
        self.assertTrue(any(p["outScopes"] for p in programs))

    def test_duplicate_slugs_are_dropped(self):
        raw = load("bugcrowd")[:1]
        self.assertEqual(len(normalize_many("bugcrowd", raw * 3)), 1)

    def test_program_without_name_is_skipped(self):
        self.assertEqual(normalize_many("bugcrowd", [{"targets": {}}]), [])

    def test_local_program_uses_out_scopes_key(self):
        program = normalize_local(
            "local",
            {
                "program_name": "Local Test",
                "scope": ["a.com", "b.com"],
                "outScopes": ["b.com"],
            },
        )
        self.assertEqual(program["slug"], "local-test")
        self.assertEqual(program["scopes"], ["a.com", "b.com"])
        self.assertEqual(program["outScopes"], ["b.com"])

    def test_unknown_source_raises(self):
        with self.assertRaises(Exception):
            normalize_program("unknown", {"name": "x"})


if __name__ == "__main__":
    unittest.main()
