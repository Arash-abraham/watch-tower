"""Backwards-compatible entry point.

Historically this script downloaded ``bugcrowd_data.json`` and wrote it to
MongoDB directly.  The logic now lives in ``monitor.py`` so that every source
goes through the same normalise → diff → notify pipeline.
"""

from __future__ import annotations

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from monitor import main  # noqa: E402


def RunCode(argv: list[str] | None = None) -> int:
    return main(["--sources", "bugcrowd", *(argv or [])])


if __name__ == "__main__":
    raise SystemExit(RunCode())
