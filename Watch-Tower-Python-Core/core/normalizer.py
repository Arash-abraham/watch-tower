
"""
Normalize the four supported bounty datasets into one shape.

Supported sources:
- bugcrowd: target
- hackerone: asset_identifier
- yeswehack: target
- intigriti: endpoint

The normalized document is the contract shared with the Laravel API:
source, slug, program_name, program_url, scopes, outScopes,
scope_details, asset_types, active and meta.
"""

from __future__ import annotations

import logging
import math
import re
from copy import deepcopy
from typing import Any, Iterable
from urllib.parse import quote

SUPPORTED_SOURCES = (
    "bugcrowd",
    "hackerone",
    "yeswehack",
    "intigriti",
)

IDENTIFIER_KEYS = (
    "target",
    "asset_identifier",
    "endpoint",
    "uri",
    "host",
)

TYPE_KEYS = (
    "type",
    "asset_type",
)

SOURCE_IDENTIFIER_KEYS = {
    "bugcrowd": ("target",),
    "hackerone": ("asset_identifier",),
    "yeswehack": ("target",),
    "intigriti": ("endpoint",),
}

INACTIVE_STATUSES = {
    "closed",
    "disabled",
    "inactive",
    "archived",
    "paused",
    "suspended",
    "rejected",
    "private",
    "unpublished",
    "terminated",
    "ended",
    "expired",
}

ACTIVE_STATUSES = {
    "open",
    "active",
    "published",
    "public",
    "accepting_submissions",
    "live",
}

logger = logging.getLogger(__name__)


class NormalizationError(ValueError):
    """Raised when a program cannot be normalized."""


def _string(value: Any) -> str | None:
    """Convert a value to a usable string."""
    if value is None or isinstance(value, bool):
        return None

    if isinstance(value, str):
        value = value.strip()
        return value or None

    if isinstance(value, (int, float)):
        if isinstance(value, float) and not math.isfinite(value):
            return None
        return str(value)

    return None


def slugify(value: Any) -> str:
    """Create a stable URL/database-friendly slug."""
    text = _string(value) or "unknown"

    text = text.strip().lower()
    text = re.sub(r"[^a-zA-Z0-9]+", "-", text)

    return text.strip("-") or "unknown"


def _first(
    item: dict[str, Any],
    keys: Iterable[str],
) -> str | None:
    """Return the first non-empty string value."""
    for key in keys:
        value = _string(item.get(key))
        if value:
            return value

    return None


def _number(value: Any) -> float | None:
    """
    Normalize numeric values.

    Supports:
    - int / float
    - numeric strings
    - objects such as {"value": 500, "currency": "EUR"}
    """
    if isinstance(value, bool) or value is None:
        return None

    if isinstance(value, dict):
        return _number(value.get("value"))

    if isinstance(value, str):
        value = value.strip().replace(",", "")

        if not value:
            return None

    try:
        number = float(value)

        if not math.isfinite(number):
            return None

        return number

    except (TypeError, ValueError, OverflowError):
        return None


def _as_list(value: Any) -> list:
    """Normalize a value into a list without splitting strings."""
    if value is None:
        return []

    if isinstance(value, list):
        return value

    if isinstance(value, (tuple, set)):
        return list(value)

    return [value]


def _is_active(status: Any, default: bool = True) -> bool:
    """
    Determine whether a program is active.

    Unknown statuses use the provided default. The original status
    is also preserved in metadata.
    """
    normalized = (_string(status) or "").lower()
    normalized = normalized.replace("-", "_").replace(" ", "_")

    if not normalized:
        return default

    if normalized in INACTIVE_STATUSES:
        return False

    if normalized in ACTIVE_STATUSES:
        return True

    return default


def _collect(
    targets: dict[str, Any],
    key: str,
    source: str | None = None,
) -> tuple[list[str], list[dict], dict[str, str]]:
    """
    Collect asset identifiers and preserve their original metadata.

    Returns:
        identifiers:
            Unique asset identifiers.

        details:
            Full asset objects with normalized target and type fields.

        asset_types:
            Mapping of target -> asset type.
    """
    seen: dict[str, int] = {}
    identifiers: list[str] = []
    details: list[dict] = []
    asset_types: dict[str, str] = {}

    raw_items = _as_list(targets.get(key))

    preferred_keys = SOURCE_IDENTIFIER_KEYS.get(source, ())
    identifier_keys = tuple(
        dict.fromkeys(preferred_keys + IDENTIFIER_KEYS)
    )

    for raw_item in raw_items:
        if isinstance(raw_item, str):
            target = raw_item.strip()

            if not target:
                continue

            detail = {
                "target": target,
                "type": "unknown",
            }

            asset_type = "unknown"

        elif isinstance(raw_item, dict):
            target = _first(raw_item, identifier_keys)

            if not target:
                logger.debug(
                    "Skipping scope without identifier: %s",
                    raw_item,
                )
                continue

            asset_type = _first(raw_item, TYPE_KEYS) or "unknown"

            # Preserve all original scope metadata.
            detail = deepcopy(raw_item)

            # Guarantee normalized fields.
            detail["target"] = target
            detail["type"] = asset_type

        else:
            continue

        # Merge duplicate assets instead of silently losing metadata.
        if target in seen:
            index = seen[target]

            existing = details[index]
            existing.update(detail)

            # Keep the first known, meaningful asset type.
            if asset_types[target] == "unknown" and asset_type != "unknown":
                asset_types[target] = asset_type
                existing["type"] = asset_type

            continue

        seen[target] = len(details)

        identifiers.append(target)
        details.append(detail)
        asset_types[target] = asset_type

    return identifiers, details, asset_types


def _get_program_targets(item: dict[str, Any]) -> dict[str, Any]:
    """Safely retrieve the targets object."""
    targets = item.get("targets")

    if isinstance(targets, dict):
        return targets

    return {}


def _program_url(value: Any) -> str | None:
    """Return a non-empty URL string when available."""
    return _string(value)


def normalize_program(
    source: str,
    item: dict[str, Any],
) -> dict:
    """Convert one raw program entry into the shared document shape."""

    source = (_string(source) or "").lower()

    if source not in SUPPORTED_SOURCES:
        raise NormalizationError(
            f"Unsupported source: {source}"
        )

    if not isinstance(item, dict):
        raise NormalizationError(
            f"{source}: program entry is not an object"
        )

    name = _string(item.get("name"))

    if not name:
        raise NormalizationError(
            f"{source}: program without a name"
        )

    targets = _get_program_targets(item)

    scopes, in_details, asset_types = _collect(
        targets,
        "in_scope",
        source,
    )

    out_scopes, out_details, out_types = _collect(
        targets,
        "out_of_scope",
        source,
    )

    # Preserve asset types from both in-scope and out-of-scope assets.
    asset_types.update(out_types)

    active = True
    meta: dict[str, Any] = {}

    # ---------------------------------------------------------
    # Bugcrowd
    # ---------------------------------------------------------

    if source == "bugcrowd":
        original_url = _program_url(item.get("url"))

        slug = (
            original_url.rstrip("/").split("/")[-1]
            if original_url
            else slugify(name)
        )

        url = original_url

        meta = {
            "allows_disclosure": bool(
                item.get("allows_disclosure")
            ),
            "managed": bool(
                item.get("managed_by_bugcrowd")
            ),
            "safe_harbor": deepcopy(
                item.get("safe_harbor")
            ),
            "max_payout": _number(
                item.get("max_payout")
            ),
        }

    # ---------------------------------------------------------
    # HackerOne
    # ---------------------------------------------------------

    elif source == "hackerone":
        slug = (
            _string(item.get("handle"))
            or slugify(name)
        )

        url = _program_url(item.get("url"))

        if not url:
            url = (
                "https://hackerone.com/"
                + quote(slug, safe="")
            )

        severities = []

        for target in _as_list(targets.get("in_scope")):
            if not isinstance(target, dict):
                continue

            severity = _string(
                target.get("max_severity")
            )

            if severity:
                severities.append(severity)

        meta = {
            "offers_bounties": bool(
                item.get("offers_bounties")
            ),
            "managed": bool(
                item.get("managed_program")
            ),
            "allows_bounty_splitting": bool(
                item.get("allows_bounty_splitting")
            ),
            "submission_state": item.get(
                "submission_state"
            ),
            "max_severity": (
                severities[0] if severities else None
            ),
            "website": _program_url(
                item.get("website")
            ),
        }

        active = _is_active(
            item.get("submission_state"),
            default=True,
        )

    # ---------------------------------------------------------
    # YesWeHack
    # ---------------------------------------------------------

    elif source == "yeswehack":
        external_id = _string(item.get("id"))

        slug = external_id or slugify(name)

        url = _program_url(item.get("url"))

        if not url:
            url = (
                "https://yeswehack.com/programs/"
                + quote(slug, safe="")
            )

        meta = {
            "min_bounty": _number(
                item.get("min_bounty")
            ),
            "max_bounty": _number(
                item.get("max_bounty")
            ),
            "managed": bool(
                item.get("managed")
            ),
            "public": bool(
                item.get("public", True)
            ),
        }

        active = not bool(
            item.get("disabled")
        )

    # ---------------------------------------------------------
    # Intigriti
    # ---------------------------------------------------------

    elif source == "intigriti":
        slug = (
            _string(item.get("handle"))
            or slugify(name)
        )

        company = (
            _string(item.get("company_handle"))
            or "programs"
        )

        url = _program_url(item.get("url"))

        if not url:
            url = (
                "https://app.intigriti.com/programs/"
                f"{quote(company, safe='')}/"
                f"{quote(slug, safe='')}/detail"
            )

        max_bounty = item.get("max_bounty")
        min_bounty = item.get("min_bounty")

        currency = None

        if isinstance(max_bounty, dict):
            currency = _string(
                max_bounty.get("currency")
            )

        if not currency and isinstance(min_bounty, dict):
            currency = _string(
                min_bounty.get("currency")
            )

        meta = {
            "min_bounty": _number(min_bounty),
            "max_bounty": _number(max_bounty),
            "currency": currency,
            "confidentiality": item.get(
                "confidentiality_level"
            ),
            "status": item.get("status"),
        }

        active = _is_active(
            item.get("status"),
            default=True,
        )

    # ---------------------------------------------------------
    # Shared normalized document
    # ---------------------------------------------------------

    return {
        "source": source,
        "slug": slugify(slug),
        "program_name": name,
        "program_url": url,
        "scopes": scopes,
        "outScopes": out_scopes,
        "scope_details": {
            "in": in_details,
            "out": out_details,
        },
        "asset_types": asset_types,
        "active": bool(active),
        "meta": meta,
    }


def normalize_many(
    source: str,
    raw: Iterable[dict],
) -> list[dict]:
    """
    Normalize multiple programs.

    Duplicate slugs are removed only within the same source.
    Invalid records are logged instead of being silently ignored.
    """
    source = (_string(source) or "").lower()

    if source not in SUPPORTED_SOURCES:
        raise NormalizationError(
            f"Unsupported source: {source}"
        )

    programs: list[dict] = []
    seen: set[str] = set()

    for index, item in enumerate(raw or []):
        try:
            program = normalize_program(source, item)

        except (
            NormalizationError,
            TypeError,
            ValueError,
            AttributeError,
        ) as exc:
            logger.warning(
                "Skipping invalid program: source=%s index=%s error=%s",
                source,
                index,
                exc,
            )
            continue

        # Source-specific deduplication.
        key = f"{source}:{program['slug']}"

        if key in seen:
            logger.debug(
                "Duplicate program skipped: %s",
                key,
            )
            continue

        seen.add(key)
        programs.append(program)

    logger.info(
        "Normalization completed: source=%s total=%s",
        source,
        len(programs),
    )

    return programs


def normalize_local(
    source: str,
    raw: dict,
) -> dict:
    """
    Normalize hand-written local JSON program files.

    Supported local fields:
    - program_name / name
    - scopes / scope
    - outScopes / out-scope / out_of_scope
    - program_url / url
    - slug
    - config / meta
    """

    source = _string(source) or "local"

    if not isinstance(raw, dict):
        raise NormalizationError(
            "Local program entry is not an object"
        )

    name = (
        _string(raw.get("program_name"))
        or _string(raw.get("name"))
    )

    if not name:
        raise NormalizationError(
            "Local program without program_name"
        )

    scopes = (
        raw.get("scopes")
        if raw.get("scopes") is not None
        else raw.get("scope")
    )

    out_scopes = (
        raw.get("outScopes")
        if raw.get("outScopes") is not None
        else raw.get("out-scope")
    )

    if out_scopes is None:
        out_scopes = raw.get("out_of_scope")

    in_list, in_details, asset_types = _collect(
        {"in_scope": _as_list(scopes)},
        "in_scope",
    )

    out_list, out_details, out_types = _collect(
        {"out_of_scope": _as_list(out_scopes)},
        "out_of_scope",
    )

    asset_types.update(out_types)

    meta = (
        raw.get("config")
        or raw.get("meta")
        or {}
    )

    if not isinstance(meta, dict):
        meta = {}

    return {
        "source": source,
        "slug": slugify(
            raw.get("slug") or name
        ),
        "program_name": name,
        "program_url": (
            _program_url(raw.get("program_url"))
            or _program_url(raw.get("url"))
        ),
        "scopes": in_list,
        "outScopes": out_list,
        "scope_details": {
            "in": in_details,
            "out": out_details,
        },
        "asset_types": asset_types,
        "active": True,
        "meta": deepcopy(meta),
    }
