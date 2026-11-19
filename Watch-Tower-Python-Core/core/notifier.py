"""Render and send collector alerts to Telegram and Discord."""

from __future__ import annotations

import logging
import time
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
    """Split at line boundaries when possible, counting UTF-16 code units."""
    chunks: list[str] = []
    current: list[str] = []
    size = 0
    for line in text.splitlines(keepends=True):
        line_size = len(line.encode("utf-16-le")) // 2
        if current and size + line_size > limit:
            chunks.append("".join(current))
            current, size = [], 0
        for char in line:
            width = 2 if ord(char) > 0xFFFF else 1
            if size + width > limit:
                chunks.append("".join(current))
                current, size = [], 0
            current.append(char)
            size += width
    if current:
        chunks.append("".join(current))
    return [chunk for chunk in chunks if chunk.strip()]


def build_message(changes: list[dict]) -> str:
    """Render every event in a batch, grouped by source and program."""
    if not changes:
        return ""

    grouped: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for change in changes:
        grouped[(change.get("source", "?"), change.get("program_name", "?"))].append(change)

    lines = [
        "WATCH TOWER — scope changes detected",
        f"{len(changes)} event(s) across {len(grouped)} program(s)",
        "",
    ]

    for (source, program), events in sorted(grouped.items()):
        lines.append(f"[{source}] {program}")
        for event in events:
            marker = TYPE_MARKERS.get(event["type"], "·")
            target = event.get("target") or ""
            label = TYPE_LABELS.get(event["type"], event["type"])
            line = f"  {marker} {label}: {target}" if target else f"  {marker} {label}"
            if event.get("asset_type") and event.get("target"):
                line += f" ({event['asset_type']})"
            lines.append(line)
        lines.append("")

    lines.append("Open the dashboard for details.")
    return "\n".join(lines).rstrip()


def _retry_delay(response) -> float:
    """Read a provider's rate-limit delay in seconds, if present."""
    try:
        data = response.json()
        if not isinstance(data, dict):
            data = {}
        candidate = data.get("parameters")
        telegram_delay = candidate.get("retry_after") if isinstance(candidate, dict) else None
        return float(response.headers.get("Retry-After") or telegram_delay or data.get("retry_after") or 0)
    except (ValueError, TypeError):
        return 0


def _post(channel: str, url: str, payload: dict) -> bool:
    for attempt in range(2):
        try:
            response = requests.post(
                url, json=payload, timeout=15, allow_redirects=False,
                params={"wait": "true"} if channel == "discord" else None,
            )
        except requests.RequestException as exc:
            # Exception strings and response bodies may contain the webhook or bot token.
            log.error("%s notification request failed (%s)", channel, type(exc).__name__)
            return False

        if response.status_code == 429 and attempt == 0:
            delay = _retry_delay(response)
            if 0 < delay <= 15:
                time.sleep(delay)
                continue
        if not 200 <= response.status_code < 300:
            log.error("%s notification rejected (HTTP %s)", channel, response.status_code)
            return False
        if channel == "telegram":
            try:
                data = response.json()
                if isinstance(data, dict) and data.get("ok") is True:
                    return True
            except ValueError:
                pass
            log.error("telegram did not confirm delivery")
            return False
        return True
    return False


def send_telegram(text: str) -> bool:
    token, chat_id = config.TELEGRAM_BOT_TOKEN, config.TELEGRAM_CHAT_ID
    if not token or not chat_id or not text.strip():
        return False
    return all(
        _post(
            "telegram", f"https://api.telegram.org/bot{token}/sendMessage",
            {"chat_id": chat_id, "text": chunk, "link_preview_options": {"is_disabled": True}},
        )
        for chunk in _chunks(text, TELEGRAM_LIMIT)
    )


def send_discord(text: str) -> bool:
    webhook = config.DISCORD_WEBHOOK_URL
    if not webhook or not text.strip():
        return False
    return all(
        _post("discord", webhook, {"content": chunk, "allowed_mentions": {"parse": []}})
        for chunk in _chunks(text, DISCORD_LIMIT)
    )


def configured_channels() -> tuple[str, ...]:
    return tuple(channel for channel, enabled in (
        ("telegram", config.TELEGRAM_BOT_TOKEN and config.TELEGRAM_CHAT_ID),
        ("discord", config.DISCORD_WEBHOOK_URL),
    ) if enabled)


def send(channel: str, text: str) -> bool:
    return {"telegram": send_telegram, "discord": send_discord}[channel](text)
