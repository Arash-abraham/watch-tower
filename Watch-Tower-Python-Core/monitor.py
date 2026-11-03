#!/usr/bin/env python3
"""Watch Tower collector — the single entry point of the Python core.

Examples
--------
Run one sync of every configured source and send notifications::

    python monitor.py --once

Run in the background, every 30 minutes::

    python monitor.py --watch --interval 1800

Only Bugcrowd, from a local copy of the dataset (offline/CI)::

    python monitor.py --once --sources bugcrowd --input-dir ./tests/fixtures

Sync the hand-written JSON programs in ``programs/`` and never notify::

    python monitor.py --once --local --no-notify
"""

from __future__ import annotations

import argparse
import logging
import os
import signal
import sys
import time

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import config  # noqa: E402
from core import notifier  # noqa: E402
from core.diff import utcnow  # noqa: E402
from core.normalizer import SUPPORTED_SOURCES, normalize_local, normalize_many  # noqa: E402
from core.sources import SOURCE_FILES, fetch_source, load_source_file  # noqa: E402
from database import db  # noqa: E402

log = logging.getLogger("watchtower")

LOCAL_SOURCE = "local"
_running = True


def setup_logging(level: str | None = None) -> None:
    logging.basicConfig(
        level=getattr(logging, (level or config.LOG_LEVEL or "INFO").upper(), logging.INFO),
        format="%(asctime)s %(levelname)-7s %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def parse_sources(raw: list[str] | None) -> list[str]:
    if not raw:
        return list(config.SOURCES)
    sources: list[str] = []
    for item in raw:
        for part in item.split(","):
            part = part.strip().lower()
            if part and part not in sources:
                sources.append(part)
    unknown = [s for s in sources if s not in SOURCE_FILES and s != LOCAL_SOURCE]
    if unknown:
        raise SystemExit(f"unknown source(s): {', '.join(unknown)}. Known: {', '.join(SUPPORTED_SOURCES)}")
    return sources


def load_local_programs(directory: str | None = None) -> list[dict]:
    directory = directory or os.path.join(config.WATCH_DIR or config["WATCH_DIR"], "programs")
    if not os.path.isdir(directory):
        log.warning("local program directory not found: %s", directory)
        return []

    programs: list[dict] = []
    for filename in sorted(os.listdir(directory)):
        if not filename.endswith(".json"):
            continue
        path = os.path.join(directory, filename)
        try:
            import json

            with open(path, "r", encoding="utf-8") as handle:
                programs.append(normalize_local(LOCAL_SOURCE, json.load(handle)))
        except Exception as exc:  # noqa: BLE001 - one bad file must not stop the sync
            log.error("skipping %s: %s", path, exc)
    return programs


def _collect_programs(source: str, args) -> list[dict]:
    """Load and normalise one source (network or disk)."""
    if source == LOCAL_SOURCE:
        return load_local_programs(args.local_dir)

    if args.input_dir:
        path = os.path.join(args.input_dir, SOURCE_FILES[source])
        raw = load_source_file(source, path)
    else:
        raw = fetch_source(source, base_url=args.base_url)

    programs = normalize_many(source, raw)

    # Use the source-specific count when available; otherwise, fall back to max_programs.
    # Reject negative limits before slicing the program list.
    
    source_count = getattr(args, f"{source}_count", None)

    if source_count is None:
        source_count = args.max_programs

    if source_count is not None:
        if source_count < 0:
            raise ValueError("Program count cannot be negative")

        programs = programs[:source_count]
    return programs


def run_source(source: str, args) -> dict:
    """Sync one source. Never raises: failures are reported and recorded."""
    started = utcnow()

    try:
        programs = _collect_programs(source, args)
    except Exception as exc:  # noqa: BLE001 - network/parse problems must not kill the loop
        log.error("could not collect %s: %s", source, exc)
        if not args.dry_run:
            try:
                db.record_failed_run(source, started, str(exc))
            except Exception:  # noqa: BLE001 - database may be down too
                log.debug("could not record the failed run", exc_info=True)
        return {"source": source, "error": str(exc), "changes": []}

    if args.dry_run:
        conflicts = sum(1 for program in programs if set(program["scopes"]) & set(program["outScopes"]))
        log.info(
            "[dry-run] %s: %s programs, %s assets, %s with scope conflicts",
            source,
            len(programs),
            sum(len(program["scopes"]) for program in programs),
            conflicts,
        )
        return {"source": source, "dry_run": True, "programs": len(programs), "changes": []}

    try:
        summary = db.sync_programs(source, programs)
    except Exception as exc:  # noqa: BLE001 - one bad source must not stop the others
        log.exception("sync failed for %s", source)
        try:
            db.record_failed_run(source, started, str(exc))
        except Exception:  # noqa: BLE001
            log.debug("could not record the failed run", exc_info=True)
        return {"source": source, "error": str(exc), "changes": []}

    changes = summary.get("changes") or []
    if changes and not args.no_notify:
        results = notifier.notify(changes)
        log.info("notifications: %s", results)
        if "sent" in results.values():
            db.mark_notified([change["_id"] for change in changes if "_id" in change])

    return summary


def run_once(sources: list[str], args) -> int:
    failures = 0
    totals = {"inserted": 0, "updated": 0, "deactivated": 0, "changes": 0}

    for source in sources:
        summary = run_source(source, args)
        if summary.get("error"):
            failures += 1
            continue
        totals["inserted"] += summary.get("inserted", 0)
        totals["updated"] += summary.get("updated", 0)
        totals["deactivated"] += summary.get("deactivated", 0)
        totals["changes"] += len(summary.get("changes") or [])

    log.info(
        "run finished: +%s new, ~%s updated, %s deactivated, %s change(s), %s failure(s)",
        totals["inserted"],
        totals["updated"],
        totals["deactivated"],
        totals["changes"],
        failures,
    )
    return 1 if failures else 0


def _stop(signum, frame):  # noqa: ARG001
    global _running
    _running = False
    log.info("stop signal received, finishing current run...")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Watch Tower collector")
    parser.add_argument("--once", action="store_true", help="run a single sync (default)")
    parser.add_argument("--watch", action="store_true", help="run forever, syncing on an interval")
    parser.add_argument("--interval", type=int, default=None, help="seconds between runs in --watch mode")
    parser.add_argument("--sources", action="append", help="comma separated list (default: all configured)")
    parser.add_argument("--local", action="store_true", help="also sync the local programs/ directory")
    parser.add_argument("--local-dir", default=None, help="directory containing local program JSON files")
    parser.add_argument("--input-dir", default=os.getenv("INPUT_DIR"), help="read datasets from disk instead of the network")
    parser.add_argument("--base-url", default=None, help="override the dataset base URL")
    parser.add_argument("--max-programs", type=int, default=None, help="limit programs per source (debugging)")
    parser.add_argument("--no-notify", action="store_true", help="never send notifications")
    parser.add_argument("--dry-run", action="store_true", help="fetch + normalise only, no database writes")
    parser.add_argument("--log-level", default=None)
    
    # Define source-specific program count limits for each platform.
    parser.add_argument("--bugcrowd-count", type=int, default=None)
    parser.add_argument("--hackerone-count", type=int, default=None)
    parser.add_argument("--yeswehack-count", type=int, default=None)
    parser.add_argument("--intigriti-count", type=int, default=None)

    args = parser.parse_args(argv)

    setup_logging(args.log_level)

    sources = parse_sources(args.sources)
    if args.local and LOCAL_SOURCE not in sources:
        sources.append(LOCAL_SOURCE)

    if args.dry_run:
        log.info("dry-run mode: nothing will be written to MongoDB")

    signal.signal(signal.SIGINT, _stop)
    signal.signal(signal.SIGTERM, _stop)

    if not args.watch:
        return run_once(sources, args)

    interval = args.interval or config.SCAN_INTERVAL_SECONDS or 1800
    log.info("watch mode: %s, every %ss", ", ".join(sources), interval)
    while _running:
        run_once(sources, args)
        deadline = time.time() + interval
        while _running and time.time() < deadline:
            time.sleep(1)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
