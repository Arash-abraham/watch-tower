"""Drop Watch Tower collections (destructive).

Usage::

    python database/reset_db.py            # asks for confirmation
    python database/reset_db.py --yes      # no prompt (automation)
    python database/reset_db.py --yes --keep-programs   # keep programs, clear alerts
"""

from __future__ import annotations

import argparse
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import config  # noqa: E402
from database import db  # noqa: E402

ALERT_ONLY = (db.CHANGES, db.SYNC_RUNS)
ALL_COLLECTIONS = (db.PROGRAMS, db.CHANGES, db.SYNC_RUNS, db.SUBDOMAINS)


def reset(collections=ALL_COLLECTIONS, confirm: bool = False) -> bool:
    database = db.get_db()
    existing = set(database.list_collection_names())
    targets = [name for name in collections if name in existing]

    if not targets:
        print(f"nothing to drop in '{config.DB_NAME}' (already empty)")
        return True

    print(f"database : {config.DB_NAME}")
    print(f"to drop  : {', '.join(targets)}")
    if not confirm:
        answer = input("This is destructive. Continue? (y/N): ").strip().lower()
        if answer not in {"y", "yes"}:
            print("aborted")
            return False

    for name in targets:
        database.drop_collection(name)
        print(f"dropped collection: {name}")

    db.ensure_indexes(database)
    print("collections recreated lazily, indexes ensured")
    return True


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Reset the Watch Tower database")
    parser.add_argument("--yes", action="store_true", help="skip the confirmation prompt")
    parser.add_argument("--keep-programs", action="store_true", help="only drop alerts/runs")
    args = parser.parse_args(argv)

    collections = ALL_COLLECTIONS if not args.keep_programs else ALERT_ONLY
    return 0 if reset(collections, confirm=args.yes) else 1


if __name__ == "__main__":
    raise SystemExit(main())
