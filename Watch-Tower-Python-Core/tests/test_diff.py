import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.diff import build_changes, diff_sets, find_conflicts  # noqa: E402

PROGRAM = {
    "source": "bugcrowd",
    "slug": "acme",
    "program_name": "Acme",
    "program_url": "https://bugcrowd.com/acme",
    "scopes": ["a.com", "b.com"],
    "outScopes": ["c.com"],
    "asset_types": {"a.com": "website", "b.com": "api", "c.com": "website"},
}


class DiffSetsTests(unittest.TestCase):
    def test_added_and_removed_are_sorted(self):
        added, removed = diff_sets(["b.com", "a.com"], ["c.com", "a.com"])
        self.assertEqual(added, ["c.com"])
        self.assertEqual(removed, ["b.com"])

    def test_none_values_are_treated_as_empty(self):
        self.assertEqual(diff_sets(None, ["x"]), (["x"], []))
        self.assertEqual(diff_sets(["x"], None), ([], ["x"]))

    def test_whitespace_is_ignored(self):
        added, removed = diff_sets([" a.com "], ["a.com"])
        self.assertEqual((added, removed), ([], []))

    def test_conflicts(self):
        self.assertEqual(find_conflicts(["a.com", "b.com"], ["b.com"]), ["b.com"])
        self.assertEqual(find_conflicts(None, None), [])


class BuildChangesTests(unittest.TestCase):
    def test_first_seen_produces_one_program_added_event(self):
        changes = build_changes(PROGRAM, None)
        self.assertEqual(len(changes), 1)
        self.assertEqual(changes[0]["type"], "program_added")
        self.assertEqual(changes[0]["notified"], False)

    def test_scope_changes_are_detected_in_both_directions(self):
        previous = {"scopes": ["a.com"], "outScopes": []}
        changes = build_changes(PROGRAM, previous)
        types = {(c["type"], c["target"]) for c in changes}
        self.assertIn(("scope_added", "b.com"), types)
        self.assertIn(("out_scope_added", "c.com"), types)

    def test_removed_scope(self):
        previous = {"scopes": ["a.com", "b.com", "old.com"], "outScopes": ["c.com"]}
        changes = build_changes(PROGRAM, previous)
        self.assertIn(("scope_removed", "old.com"), {(c["type"], c["target"]) for c in changes})

    def test_unchanged_program_produces_no_events(self):
        previous = {"scopes": ["a.com", "b.com"], "outScopes": ["c.com"]}
        self.assertEqual(build_changes(PROGRAM, previous), [])

    def test_conflict_is_reported(self):
        program = dict(PROGRAM, outScopes=["c.com", "a.com"])
        changes = build_changes(program, {"scopes": ["a.com", "b.com"], "outScopes": ["c.com"]})
        self.assertIn("conflict", {c["type"] for c in changes})

    def test_existing_conflicts_are_not_reported_twice(self):
        program = dict(PROGRAM, outScopes=["c.com", "a.com"])
        previous = {
            "scopes": ["a.com", "b.com"],
            "outScopes": ["c.com", "a.com"],
            "conflicts": ["a.com"],
        }
        self.assertEqual(build_changes(program, previous), [])


if __name__ == "__main__":
    unittest.main()
