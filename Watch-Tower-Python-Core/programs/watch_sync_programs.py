"""Sync the hand-written program files in this directory into MongoDB.

Kept for backwards compatibility; ``python monitor.py --local`` does the same.
"""

from __future__ import annotations

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from monitor import main  # noqa: E402


def RunCode(argv: list[str] | None = None) -> int:
    return main(["--sources", "local", "--no-notify", *(argv or [])])


if __name__ == "__main__":
    raise SystemExit(RunCode())
