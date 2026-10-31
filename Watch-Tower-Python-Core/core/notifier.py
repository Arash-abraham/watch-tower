"""Notification channels (Telegram + Discord).

The notifier is deliberately dumb: it receives the list of change documents
produced by the collector, renders a readable message and pushes it to every
configured channel.  Channels without credentials are skipped, never fatal.
"""

from __future__ import annotations

import logging
from collections import defaultdict

import requests

from config import config

log = logging.getLogger(__name__)

TELEGRAM_LIMIT = 3800
DISCORD_LIMIT = 1900

TYPE_LABELS = {
    "program_added": "NEW PROGRAM",
    "program_removed": "PROGRAM CLOSED",
    "scope_added": "SCOPE ADDED",
    "scope_removed": "SCOPE REMOVED",
    "out_scope_added": "OUT-OF-SCOPE ADDED",
    "out_scope_removed": "OUT-OF-SCOPE REMOVED",
    "conflict": "CONFLICT",
}

TYPE_MARKERS = {
    "program_added": "+",
    "program_removed": "x",
    "scope_added": "+",
    "scope_removed": "-",
    "out_scope_added": "+",
    "out_scope_removed": "-",
    "conflict": "!",
}


def _chunks(text: str, limit: int) -> list[str]:
    chunks: list[str] = []
    current = ""
    for line in text.splitlines(keepends=True):
        if current and len(current) + len(line) > limit:
            chunks.append(current.rstrip())
            current = ""
        current += line
    if current.strip():
        chunks.append(current.rstrip())
    return chunks or [text[:limit]]


def build_message(changes: list[dict], max_items: int | None = None) -> str:
    """Render a human-readable summary grouped by source and program."""
    if not changes:
        return ""

    max_items = max_items or config.NOTIFY_MAX_ITEMS or 40
    grouped: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for change in changes:
        grouped[(change.get("source", "?"), change.get("program_name", "?"))].append(change)

    lines = [
        "WATCH TOWER — scope changes detected",
        f"{len(changes)} event(s) across {len(grouped)} program(s)",
        "",
    ]

    shown = 0
    for (source, program), events in sorted(grouped.items()):
        if shown >= max_items:
            lines.append(f"... and {len(changes) - shown} more event(s)")
            break
        lines.append(f"[{source}] {program}")
        for event in events:
            marker = TYPE_MARKERS.get(event["type"], "·")
            target = event.get("target") or ""
            label = TYPE_LABELS.get(event["type"], event["type"])
            line = f"  {marker} {label}: {target}" if target else f"  {marker} {label}"
            if event.get("asset_type") and event.get("target"):
                line += f" ({event['asset_type']})"
            lines.append(line)
            shown += 1
        lines.append("")

    lines.append("Open the dashboard for details.")
    return "\n".join(lines).rstrip()


def _post(url: str, payload: dict, timeout: int = 15) -> bool:
    try:
        response = requests.post(url, json=payload, timeout=timeout)
        if response.status_code >= 300:
            log.error("notification failed (%s): %s", response.status_code, response.text[:300])
            return False
        return True
    except requests.RequestException as exc:
        log.error("notification request failed: %s", exc)
        return False


def send_telegram(text: str) -> bool:
    token = config.TELEGRAM_BOT_TOKEN
    chat_id = config.TELEGRAM_CHAT_ID
    if not token or not chat_id:
        return False

    ok = True
    for chunk in _chunks(text, TELEGRAM_LIMIT):
        ok = _post(
            f"https://api.telegram.org/bot{token}/sendMessage",
            {"chat_id": chat_id, "text": chunk, "disable_web_page_preview": True},
        ) and ok
    return ok


def send_discord(text: str) -> bool:
    webhook = config.DISCORD_WEBHOOK_URL
    if not webhook:
        return False

    ok = True
    for chunk in _chunks(text, DISCORD_LIMIT):
        ok = _post(webhook, {"content": chunk[:2000]}) and ok
    return ok


def notify(changes: list[dict]) -> dict[str, str]:
    """Send changes to every configured channel.

    Returns a mapping ``channel -> status`` where status is one of
    ``sent``, ``failed`` or ``not_configured``.
    """
    results: dict[str, str] = {}
    if not changes:
        return results

    message = build_message(changes)
    if not message:
        return results

    results["telegram"] = "not_configured"
    if config.TELEGRAM_BOT_TOKEN and config.TELEGRAM_CHAT_ID:
        results["telegram"] = "sent" if send_telegram(message) else "failed"

    results["discord"] = "not_configured"
    if config.DISCORD_WEBHOOK_URL:
        results["discord"] = "sent" if send_discord(message) else "failed"

    return results
