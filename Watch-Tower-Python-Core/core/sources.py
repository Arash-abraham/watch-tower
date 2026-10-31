"""Download the public bounty-program datasets.

Only public JSON files are read.  No target is ever scanned or contacted —
Watch Tower monitors *scope definitions*, it does not attack anything.
"""

from __future__ import annotations

import json
import logging
import time
from typing import Any

import requests

from config import config

log = logging.getLogger(__name__)

SOURCE_FILES = {
    "bugcrowd": "bugcrowd_data.json",
    "hackerone": "hackerone_data.json",
    "yeswehack": "yeswehack_data.json",
    "intigriti": "intigriti_data.json",
}


class SourceError(RuntimeError):
    pass


def source_url(source: str, base_url: str | None = None) -> str:
    if source not in SOURCE_FILES:
        raise SourceError(f"unknown source '{source}' (known: {', '.join(SOURCE_FILES)})")
    base = (base_url or config.BOUNTY_DATA_BASE_URL or "").rstrip("/")
    return f"{base}/{SOURCE_FILES[source]}"


def fetch_source(
    source: str,
    base_url: str | None = None,
    timeout: int | None = None,
    retries: int | None = None,
) -> list[dict]:
    url = source_url(source, base_url)
    timeout = timeout or config.REQUEST_TIMEOUT or 60
    retries = retries or config.REQUEST_RETRIES or 3
    last_error: Exception | None = None

    for attempt in range(1, retries + 1):
        try:
            response = requests.get(
                url,
                timeout=timeout,
                headers={"User-Agent": "WatchTower/2.1 (+https://github.com/Arash-abraham/watch-tower)"},
            )
            response.raise_for_status()
            data = response.json()
            if not isinstance(data, list):
                raise SourceError(f"{source}: unexpected payload type {type(data).__name__}")
            log.info("fetched %s: %s programs", source, len(data))
            return data
        except (requests.RequestException, ValueError, SourceError) as exc:
            last_error = exc
            log.warning("fetch %s failed (attempt %s/%s): %s", source, attempt, retries, exc)
            if attempt < retries:
                time.sleep(min(2 ** attempt, 10))

    raise SourceError(f"could not fetch {source}: {last_error}")


def load_source_file(source: str, path: str) -> list[dict]:
    with open(path, "r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, list):
        raise SourceError(f"{path}: expected a JSON list")
    return data


def load_any(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)
