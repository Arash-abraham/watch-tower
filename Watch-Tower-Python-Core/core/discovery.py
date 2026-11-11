"""Opt-in, passive subdomain discovery for explicitly wildcarded scopes."""
from __future__ import annotations

import logging
import re
import subprocess
from urllib.parse import urlsplit

from core.diff import utcnow

log = logging.getLogger(__name__)
_LABEL = r"[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?"
_HOST = re.compile(rf"{_LABEL}(?:\.{_LABEL})+\Z", re.ASCII)


def hostname(value: str) -> str | None:
    """Accept hostnames (or HTTP URLs), not paths, IPs, prose or patterns."""
    if not isinstance(value, str):
        return None
    value = value.strip().lower().rstrip('.')
    if value.startswith(('http://', 'https://')):
        try:
            parsed = urlsplit(value)
            if parsed.username or parsed.password or not parsed.hostname:
                return None
            value = parsed.hostname.rstrip('.')
        except ValueError:
            return None
    if not _HOST.fullmatch(value) or value.rsplit('.', 1)[-1].isdigit():
        return None
    return value


def excluded(host: str, exclusions: list[tuple[str, bool]]) -> bool:
    return any(host == domain or (wildcard and host.endswith('.' + domain))
               for domain, wildcard in exclusions)


def discover_program(program: dict, collection, *, binary='subfinder', timeout=300) -> dict:
    """Persist only results within explicit wildcard scope, never delete old results.

    Fail closed if an exclusion is not machine-readable. External tools cannot
    interpret program-specific legal terms; users must review those separately.
    """
    exclusions = []
    for entry in program.get('outScopes') or []:
        if not isinstance(entry, str):
            raise ValueError('unparseable out-of-scope entry')
        entry = entry.strip()
        wildcard = entry.startswith('*.')
        domain = hostname(entry[2:] if wildcard else entry)
        if not domain:
            raise ValueError(f'unparseable out-of-scope entry: {entry!r}')
        exclusions.append((domain, wildcard))

    roots = set()
    for scope in program.get('scopes') or []:
        if isinstance(scope, str) and scope.strip().startswith('*.'):
            root = hostname(scope.strip()[2:])
            if root and not excluded(root, exclusions):
                roots.add(root)

    found = set()
    failures = 0
    for root in sorted(roots):
        try:
            result = subprocess.run([binary, '-d', root, '-silent'], capture_output=True,
                                    text=True, timeout=timeout, check=True)
        except (OSError, subprocess.SubprocessError) as exc:
            log.error('subfinder failed for %s: %s', root, exc)
            failures += 1
            continue
        for line in result.stdout.splitlines():
            host = hostname(line)
            if host and host.endswith('.' + root) and not excluded(host, exclusions):
                found.add(host)

    now = utcnow()
    for host in sorted(found):
        key = {'source': program['source'], 'program_slug': program['slug'], 'host': host}
        collection.update_one(key, {'$set': {'last_seen_at': now},
                                    '$setOnInsert': {'first_seen_at': now, 'resolved': False, 'ip': None}},
                              upsert=True)
    return {'roots': len(roots), 'hosts': len(found), 'failures': failures}
