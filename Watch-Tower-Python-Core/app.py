"""Minimal health/status service for the Python core.

The public API is served by Laravel; this Flask app only exists so Docker and
monitoring tools can check that the collector container is alive and can reach
MongoDB.  It intentionally exposes no write endpoints and no user input.
"""

from __future__ import annotations

import os
import sys

from flask import Flask, jsonify

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import config  # noqa: E402
from database import db  # noqa: E402

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False


@app.get("/health")
def health():
    mongo_ok = db.ping()
    status_code = 200 if mongo_ok else 503
    return (
        jsonify(
            {
                "status": "ok" if mongo_ok else "degraded",
                "service": "watch-tower-collector",
                "mongo": mongo_ok,
                "database": config.DB_NAME,
            }
        ),
        status_code,
    )


@app.get("/status")
def status():
    if not db.ping():
        return jsonify({"error": "mongo unavailable"}), 503

    summary = db.stats()
    last_run = summary.pop("last_run", None)
    if last_run:
        last_run["_id"] = str(last_run["_id"])
        for key in ("started_at", "finished_at"):
            if last_run.get(key):
                last_run[key] = last_run[key].isoformat()
    return jsonify({**summary, "last_run": last_run})


@app.get("/")
def index():
    return jsonify(
        {
            "service": "watch-tower-collector",
            "endpoints": ["/health", "/status"],
            "docs": "the public API is served by Watch-Tower-Laravel-Core",
        }
    )


if __name__ == "__main__":
    app.run(host=config.API_HOST, port=config.API_PORT, debug=False)
