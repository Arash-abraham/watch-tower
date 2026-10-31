"""Central configuration for the Watch Tower collector.

Every value can be overridden through environment variables (or a local
``.env`` file).  Nothing here is required for the collector to start: the
defaults point at a local MongoDB instance created by ``docker compose``.
"""

from __future__ import annotations

import os
from urllib.parse import quote_plus

from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))


def _get(name: str, default: str | None = None) -> str | None:
    value = os.getenv(name)
    if value is None or value.strip() == "":
        return default
    return value.strip()


def _get_int(name: str, default: int) -> int:
    try:
        return int(str(_get(name, str(default))).strip())
    except (TypeError, ValueError):
        return default


def _get_bool(name: str, default: bool = False) -> bool:
    raw = _get(name)
    if raw is None:
        return default
    return raw.lower() in {"1", "true", "yes", "on"}


def _get_list(name: str, default: list[str]) -> list[str]:
    raw = _get(name)
    if not raw:
        return list(default)
    return [item.strip().lower() for item in raw.split(",") if item.strip()]


def build_mongo_uri() -> str:
    """Build a Mongo connection string.

    ``MONGO_URI`` (or the Laravel-compatible ``DB_URI``) wins when present,
    otherwise the discrete ``DB_*`` variables are used.  This keeps the
    collector compatible with both ``.env`` styles in the repository.
    """
    explicit = _get("MONGO_URI") or _get("DB_URI")
    if explicit:
        return explicit

    host = _get("DB_HOST", "localhost")
    port = _get_int("DB_PORT", 27017)
    user = _get("DB_USER")
    password = _get("DB_PASS")
    credentials = ""
    if user:
        credentials = quote_plus(user)
        if password:
            credentials += f":{quote_plus(password)}"
        credentials += "@"

    uri = f"mongodb://{credentials}{host}:{port}/"
    auth_source = _get("DB_AUTH_SOURCE", "admin")
    if credentials and auth_source:
        uri += f"?authSource={auth_source}"
    return uri


class Config(dict):
    """Dict with attribute access, kept for backwards compatibility."""

    def __init__(self) -> None:
        super().__init__()
        self.update(
            {
                # --- storage -------------------------------------------------
                "MONGO_URI": build_mongo_uri(),
                "DB_NAME": _get("DB_NAME", "watch-tower"),
                "DB_HOST": _get("DB_HOST", "localhost"),
                "DB_PORT": _get_int("DB_PORT", 27017),
                "DB_USER": _get("DB_USER"),
                "DB_PASS": _get("DB_PASS"),
                "MONGO_TIMEOUT_MS": _get_int("MONGO_TIMEOUT_MS", 8000),
                # --- collection ---------------------------------------------
                "SOURCES": _get_list(
                    "SOURCES", ["bugcrowd", "hackerone", "yeswehack", "intigriti"]
                ),
                "BOUNTY_DATA_BASE_URL": _get(
                    "BOUNTY_DATA_BASE_URL",
                    "https://raw.githubusercontent.com/arkadiyt/"
                    "bounty-targets-data/main/data",
                ),
                "REQUEST_TIMEOUT": _get_int("REQUEST_TIMEOUT", 60),
                "REQUEST_RETRIES": _get_int("REQUEST_RETRIES", 3),
                "SCAN_INTERVAL_SECONDS": _get_int("SCAN_INTERVAL_SECONDS", 1800),
                "WATCH_DIR": _get("WATCH_DIR", BASE_DIR),
                "DEACTIVATE_MISSING": _get_bool("DEACTIVATE_MISSING", True),
                # --- notifications ------------------------------------------
                "TELEGRAM_BOT_TOKEN": _get("TELEGRAM_BOT_TOKEN"),
                "TELEGRAM_CHAT_ID": _get("TELEGRAM_CHAT_ID"),
                "DISCORD_WEBHOOK_URL": _get("DISCORD_WEBHOOK_URL"),
                "NOTIFY_ON_FIRST_SEEN": _get_bool("NOTIFY_ON_FIRST_SEEN", True),
                "NOTIFY_MAX_ITEMS": _get_int("NOTIFY_MAX_ITEMS", 40),
                # --- service ------------------------------------------------
                "API_HOST": _get("API_HOST", "0.0.0.0"),
                "API_PORT": _get_int("API_PORT", 8080),
                "LOG_LEVEL": (_get("LOG_LEVEL", "INFO") or "INFO").upper(),
            }
        )

    def __getattr__(self, key: str):
        try:
            return self[key]
        except KeyError:
            return None

    def __setattr__(self, key: str, value) -> None:
        self[key] = value


config = Config()
