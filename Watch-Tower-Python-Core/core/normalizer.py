"""Normalise the four supported bounty datasets into one shape.

Supported sources (all served by ``arkadiyt/bounty-targets-data``):

===================================  ==============================
source                               asset identifier field
===================================  ==============================
bugcrowd                             ``target``
hackerone                            ``asset_identifier``
yeswehack                            ``target``
intigriti                            ``endpoint``
===================================  ==============================

The normalised document is the contract shared with the Laravel API:
``source``, ``slug``, ``program_name``, ``program_url``, ``scopes``,
``outScopes``, ``scope_details``, ``asset_types`` and ``meta``.
"""

from __future__ import annotations

import re
from typing import Any, Iterable

SUPPORTED_SOURCES = ("bugcrowd", "hackerone", "yeswehack", "intigriti")

_IDENTIFIER_KEYS = ("target", "asset_identifier", "endpoint", "uri", "host")
_TYPE_KEYS = ("type", "asset_type")


class NormalizationError(ValueError):
    pass


def slugify(value: str) -> str:
    value = re.sub(r"[^a-zA-Z0-9]+", "-", (value or "").strip().lower())
    return value.strip("-") or "unknown"


def _first(item: dict, keys: Iterable[str]) -> str | None:
    for key in keys:
        value = item.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return None


def _number(value: Any) -> float | None:
    if isinstance(value, bool) or value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, dict):  # intigriti: {"value": 500, "currency": "EUR"}
        return _number(value.get("value"))
    return None


def _collect(targets: dict, key: str) -> tuple[list[str], list[dict], dict[str, str]]:
    seen: list[str] = []
    details: list[dict] = []
    asset_types: dict[str, str] = {}

    for item in targets.get(key) or []:
        if not isinstance(item, dict):
            if isinstance(item, str) and item.strip():
                target, asset_type = item.strip(), "unknown"
            else:
                continue
        else:
            target = _first(item, _IDENTIFIER_KEYS)
            if not target:
                continue
            asset_type = _first(item, _TYPE_KEYS) or "unknown"

        if target in asset_types:
            continue
        asset_types[target] = asset_type
        seen.append(target)
        details.append({"target": target, "type": asset_type})

    return seen, details, asset_types


def normalize_program(source: str, item: dict) -> dict:
    """Convert one raw program entry into the shared document shape."""
    if not isinstance(item, dict):
        raise NormalizationError(f"{source}: program entry is not an object")

    name = (item.get("name") or "").strip()
    if not name:
        raise NormalizationError(f"{source}: program without a name")

    targets = item.get("targets") or {}
    scopes, in_details, asset_types = _collect(targets, "in_scope")
    out_scopes, out_details, out_types = _collect(targets, "out_of_scope")
    asset_types.update(out_types)

    meta: dict[str, Any] = {}
    active = True

    if source == "bugcrowd":
        slug = (item.get("url") or "").rstrip("/").split("/")[-1] or slugify(name)
        url = item.get("url")
        meta = {
            "allows_disclosure": bool(item.get("allows_disclosure")),
            "managed": bool(item.get("managed_by_bugcrowd")),
            "safe_harbor": item.get("safe_harbor"),
            "max_payout": _number(item.get("max_payout")),
        }
    elif source == "hackerone":
        slug = item.get("handle") or slugify(name)
        url = item.get("url") or f"https://hackerone.com/{slug}"
        severities = [
            target.get("max_severity")
            for target in (targets.get("in_scope") or [])
            if isinstance(target, dict) and target.get("max_severity")
        ]
        meta = {
            "offers_bounties": bool(item.get("offers_bounties")),
            "managed": bool(item.get("managed_program")),
            "allows_bounty_splitting": bool(item.get("allows_bounty_splitting")),
            "submission_state": item.get("submission_state"),
            "max_severity": (severities[0] if severities else None),
            "website": item.get("website"),
        }
        active = item.get("submission_state") in (None, "open")
    elif source == "yeswehack":
        slug = item.get("id") or slugify(name)
        url = item.get("url") or f"https://yeswehack.com/programs/{slug}"
        meta = {
            "min_bounty": _number(item.get("min_bounty")),
            "max_bounty": _number(item.get("max_bounty")),
            "managed": bool(item.get("managed")),
            "public": bool(item.get("public", True)),
        }
        active = not bool(item.get("disabled"))
    elif source == "intigriti":
        slug = item.get("handle") or slugify(name)
        company = item.get("company_handle") or "programs"
        url = item.get("url") or (
            f"https://app.intigriti.com/programs/{company}/{slug}/detail"
        )
        meta = {
            "min_bounty": _number(item.get("min_bounty")),
            "max_bounty": _number(item.get("max_bounty")),
            "currency": (item.get("max_bounty") or {}).get("currency")
            if isinstance(item.get("max_bounty"), dict)
            else None,
            "confidentiality": item.get("confidentiality_level"),
            "status": item.get("status"),
        }
        active = item.get("status") in (None, "open")
    else:
        raise NormalizationError(f"unsupported source: {source}")

    return {
        "source": source,
        "slug": slugify(slug),
        "program_name": name,
        "program_url": url,
        "scopes": scopes,
        "outScopes": out_scopes,
        "scope_details": {"in": in_details, "out": out_details},
        "asset_types": asset_types,
        "active": bool(active),
        "meta": meta,
    }


def normalize_many(source: str, raw: Iterable[dict]) -> list[dict]:
    programs: list[dict] = []
    seen: set[str] = set()

    for item in raw or []:
        try:
            program = normalize_program(source, item)
        except NormalizationError:
            continue
        slug = program["slug"]
        if slug in seen:
            continue
        seen.add(slug)
        programs.append(program)

    return programs


def normalize_local(source: str, raw: dict) -> dict:
    """Normalise the small hand-written JSON files in ``programs/``."""
    name = (raw.get("program_name") or raw.get("name") or "").strip()
    if not name:
        raise NormalizationError("local program without program_name")

    scopes = raw.get("scopes") or raw.get("scope") or []
    out_scopes = raw.get("outScopes") or raw.get("out-scope") or raw.get("out_of_scope") or []

    in_list, in_details, asset_types = _collect({"in_scope": scopes}, "in_scope")
    out_list, out_details, out_types = _collect({"out_of_scope": out_scopes}, "out_of_scope")
    asset_types.update(out_types)

    return {
        "source": source,
        "slug": slugify(raw.get("slug") or name),
        "program_name": name,
        "program_url": raw.get("program_url") or raw.get("url"),
        "scopes": in_list,
        "outScopes": out_list,
        "scope_details": {"in": in_details, "out": out_details},
        "asset_types": asset_types,
        "active": True,
        "meta": raw.get("config") or raw.get("meta") or {},
    }
