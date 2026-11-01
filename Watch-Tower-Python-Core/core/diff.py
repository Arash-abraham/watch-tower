"""Pure diff helpers.

Kept free of database/network imports so they can be unit-tested in
isolation and reused by any collector.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Iterable

Change = dict


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def to_set(values: Iterable[str] | None) -> set[str]:
    if not values:
        return set()
    return {str(value).strip() for value in values if str(value).strip()}


def diff_sets(old: Iterable[str] | None, new: Iterable[str] | None) -> tuple[list[str], list[str]]:
    """Return ``(added, removed)`` as sorted lists."""
    old_set, new_set = to_set(old), to_set(new)
    return sorted(new_set - old_set), sorted(old_set - new_set)


def find_conflicts(scopes: Iterable[str] | None, out_scopes: Iterable[str] | None) -> list[str]:
    """Assets that are listed both in-scope and out-of-scope."""
    return sorted(to_set(scopes) & to_set(out_scopes))


def _change(
    program: dict,
    change_type: str,
    target: str | None = None,
    scope: str | None = None,
    asset_type: str | None = None,
    detected_at: datetime | None = None,
) -> Change:
    return {
        "source": program["source"],
        "slug": program["slug"],
        "program_name": program["program_name"],
        "type": change_type,
        "scope": scope,
        "target": target,
        "asset_type": asset_type,
        "detected_at": detected_at or utcnow(),
        "notified": False,
    }


def build_changes(
    program: dict,
    previous: dict | None,
    detected_at: datetime | None = None,
) -> list[Change]:
    """Compare a normalised program with its stored version.

    ``previous`` is ``None`` for programs seen for the first time; in that
    case a single ``program_added`` change is produced instead of one change
    per asset (a first sync should not flood the notification channel).
    """
    pending: list[Change] = []

    if previous is None:
        pending.append(
            _change(
                program,
                "program_added",
                target=program.get("program_url") or program["program_name"],
                detected_at=detected_at,
            )
        )
        return pending

    asset_types = program.get("asset_types") or {}

    added, removed = diff_sets(previous.get("scopes"), program.get("scopes"))
    for target in added:
        pending.append(
            _change(program, "scope_added", target, "in", asset_types.get(target), detected_at)
        )
    for target in removed:
        pending.append(
            _change(program, "scope_removed", target, "in", asset_types.get(target), detected_at)
        )

    added_out, removed_out = diff_sets(previous.get("outScopes"), program.get("outScopes"))
    for target in added_out:
        pending.append(
            _change(program, "out_scope_added", target, "out", asset_types.get(target), detected_at)
        )
    for target in removed_out:
        pending.append(
            _change(program, "out_scope_removed", target, "out", asset_types.get(target), detected_at)
        )

    # Only report conflicts that are new, otherwise every sync would re-alert.
    new_conflicts = set(find_conflicts(program.get("scopes"), program.get("outScopes")))
    previous_conflicts = set(
        previous.get("conflicts")
        or find_conflicts(previous.get("scopes"), previous.get("outScopes"))
    )
    for target in sorted(new_conflicts - previous_conflicts):
        pending.append(_change(program, "conflict", target, None, None, detected_at))

    return pending
