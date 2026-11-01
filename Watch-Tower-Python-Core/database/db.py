"""MongoDB persistence layer.

Python owns writes (collector + notifier state), Laravel owns reads (public
API).  The document shape written here is the contract consumed by
``Watch-Tower-Laravel-Core``.

Collections
-----------
``programs``     one document per program/source, with ``scopes`` and ``outScopes``
``changes``      one document per detected scope change (the alert feed)
``sync_runs``    one document per collector execution (observability)
``subdomains``   reserved for the upcoming asset-discovery monitors
"""

from __future__ import annotations

import logging
from datetime import datetime, timedelta
from typing import Iterable

from pymongo import ASCENDING, DESCENDING, MongoClient
from pymongo.errors import PyMongoError

from config import config
from core.diff import build_changes, find_conflicts, utcnow
from core.normalizer import normalize_many, slugify

log = logging.getLogger(__name__)

PROGRAMS = "programs"
CHANGES = "changes"
SYNC_RUNS = "sync_runs"
SUBDOMAINS = "subdomains"

_client: MongoClient | None = None


def get_client() -> MongoClient:
    global _client
    if _client is None:
        _client = MongoClient(
            config.MONGO_URI,
            serverSelectionTimeoutMS=config.MONGO_TIMEOUT_MS or 8000,
            tz_aware=True,
        )
    return _client


def set_client(client) -> None:
    """Used by tests to inject ``mongomock``."""
    global _client
    _client = client


def get_db():
    return get_client()[config.DB_NAME]


def ping(timeout_ms: int = 2000) -> bool:
    try:
        get_client().admin.command("ping")
        return True
    except Exception as exc:  # noqa: BLE001 - health endpoint must never raise
        log.warning("mongo ping failed: %s", exc)
        return False


def ensure_indexes(db=None) -> None:
    if db is None:
        db = get_db()
    try:
        # Index names are left to MongoDB so that the Laravel migrations
        # (which use the same key patterns) stay idempotent.
        db[PROGRAMS].create_index([("source", ASCENDING), ("slug", ASCENDING)], unique=True)
        db[PROGRAMS].create_index([("scopes", ASCENDING)])
        db[PROGRAMS].create_index([("last_synced_at", DESCENDING)])
        db[CHANGES].create_index([("detected_at", DESCENDING)])
        db[CHANGES].create_index([("source", ASCENDING), ("detected_at", DESCENDING)])
        db[SYNC_RUNS].create_index([("started_at", DESCENDING)])
        db[SUBDOMAINS].create_index([("host", ASCENDING)], unique=True)
    except PyMongoError as exc:  # index creation is best effort
        log.warning("could not create indexes: %s", exc)


def _program_document(program: dict, now: datetime) -> dict:
    return {
        "source": program["source"],
        "slug": program["slug"],
        "program_name": program["program_name"],
        "program_url": program.get("program_url"),
        "scopes": program.get("scopes") or [],
        "outScopes": program.get("outScopes") or [],
        "scope_details": program.get("scope_details") or {"in": [], "out": []},
        "meta": program.get("meta") or {},
        "conflicts": find_conflicts(program.get("scopes"), program.get("outScopes")),
        "active": bool(program.get("active", True)),
        "last_update": now,
        "last_synced_at": now,
    }


def sync_programs(
    source: str,
    programs: Iterable[dict],
    *,
    deactivate_missing: bool | None = None,
    record_run: bool = True,
    now: datetime | None = None,
) -> dict:
    """Upsert a full snapshot for ``source`` and record every change.

    Returns a summary dict::

        {"source": ..., "inserted": 0, "updated": 0, "unchanged": 0,
         "deactivated": 0, "programs_total": 0, "changes": [...], "run_id": ...}
    """
    db = get_db()
    ensure_indexes(db)

    started_at = now or utcnow()
    programs_coll = db[PROGRAMS]
    changes_coll = db[CHANGES]

    if deactivate_missing is None:
        deactivate_missing = config.DEACTIVATE_MISSING

    inserted = updated = unchanged = 0
    pending_changes: list[dict] = []
    seen_slugs: list[str] = []

    for program in programs:
        slug = program["slug"]
        seen_slugs.append(slug)

        previous = programs_coll.find_one({"source": source, "slug": slug})
        document = _program_document(program, started_at)

        if previous is None:
            document["first_seen_at"] = started_at
            programs_coll.insert_one(document)
            inserted += 1
        else:
            document["first_seen_at"] = previous.get("first_seen_at") or started_at
            programs_coll.update_one({"_id": previous["_id"]}, {"$set": document})
            if (
                previous.get("scopes") != document["scopes"]
                or previous.get("outScopes") != document["outScopes"]
            ):
                updated += 1
            else:
                unchanged += 1

        pending_changes.extend(build_changes(program, previous, detected_at=started_at))

    deactivated = 0
    if deactivate_missing:
        stale_filter = {"source": source, "slug": {"$nin": seen_slugs}, "active": True}
        stale_programs = list(programs_coll.find(stale_filter))
        if stale_programs:
            programs_coll.update_many(
                stale_filter, {"$set": {"active": False, "last_update": started_at}}
            )
            deactivated = len(stale_programs)
            for stale in stale_programs:
                pending_changes.append(
                    {
                        "source": source,
                        "slug": stale["slug"],
                        "program_name": stale["program_name"],
                        "type": "program_removed",
                        "scope": None,
                        "target": stale.get("program_url"),
                        "asset_type": None,
                        "detected_at": started_at,
                        "notified": False,
                    }
                )

    if pending_changes:
        changes_coll.insert_many(pending_changes)

    summary = {
        "source": source,
        "inserted": inserted,
        "updated": updated,
        "unchanged": unchanged,
        "deactivated": deactivated,
        "programs_total": inserted + updated + unchanged,
        "changes": pending_changes,
        "started_at": started_at,
        "finished_at": utcnow(),
    }

    if record_run:
        summary["run_id"] = record_run_document(
            source=source,
            started_at=started_at,
            finished_at=summary["finished_at"],
            status="success",
            stats={
                "inserted": inserted,
                "updated": updated,
                "unchanged": unchanged,
                "deactivated": deactivated,
                "changes": len(pending_changes),
            },
        )

    log.info(
        "sync %s: +%s new, ~%s updated, %s unchanged, %s deactivated, %s change(s)",
        source,
        inserted,
        updated,
        unchanged,
        deactivated,
        len(pending_changes),
    )
    return summary


def record_run_document(
    source: str,
    started_at: datetime,
    finished_at: datetime,
    status: str = "success",
    stats: dict | None = None,
    error: str | None = None,
):
    db = get_db()
    document = {
        "source": source,
        "started_at": started_at,
        "finished_at": finished_at,
        "duration_ms": int((finished_at - started_at).total_seconds() * 1000),
        "status": status,
        "error": error,
        "stats": stats or {},
    }
    result = db[SYNC_RUNS].insert_one(document)
    return result.inserted_id


def record_failed_run(source: str, started_at: datetime, error: str):
    return record_run_document(
        source=source,
        started_at=started_at,
        finished_at=utcnow(),
        status="failed",
        error=error[:500],
    )


def mark_notified(change_ids: Iterable) -> int:
    ids = list(change_ids or [])
    if not ids:
        return 0
    result = get_db()[CHANGES].update_many(
        {"_id": {"$in": ids}}, {"$set": {"notified": True, "notified_at": utcnow()}}
    )
    return result.modified_count


def recent_changes(limit: int = 20) -> list[dict]:
    return list(get_db()[CHANGES].find().sort("detected_at", DESCENDING).limit(limit))


def stats() -> dict:
    """Small aggregate used by the Python health service."""
    db = get_db()
    day_ago = utcnow() - timedelta(days=1)
    return {
        "programs": db[PROGRAMS].count_documents({}),
        "active_programs": db[PROGRAMS].count_documents({"active": True}),
        "changes_24h": db[CHANGES].count_documents({"detected_at": {"$gte": day_ago}}),
        "changes": db[CHANGES].count_documents({}),
        "last_run": db[SYNC_RUNS].find_one(sort=[("started_at", DESCENDING)]),
    }


# ---------------------------------------------------------------------------
# Backwards-compatible helpers (old scripts imported these names)
# ---------------------------------------------------------------------------

def check_and_create_database() -> str:
    """Kept for compatibility. Mongo creates databases lazily, no prompt."""
    ensure_indexes()
    return "Exist"


def upsert_program(
    program_name: str,
    scopes: list[str] | None,
    outScopes: list[str] | None,
    config_data: dict | None = None,
    source: str = "local",
) -> dict:
    program = {
        "source": source,
        "slug": slugify(program_name),
        "program_name": program_name,
        "program_url": None,
        "scopes": scopes or [],
        "outScopes": outScopes or [],
        "scope_details": {"in": [], "out": []},
        "meta": config_data or {},
        "active": True,
    }
    return sync_programs(source, [program], deactivate_missing=False)


def insert_all_bugcrowd_programs(all_data: list[dict]) -> dict:
    """Deprecated: normalise + sync instead. Kept so old entry-points work."""
    programs = normalize_many("bugcrowd", all_data)
    return sync_programs("bugcrowd", programs)
