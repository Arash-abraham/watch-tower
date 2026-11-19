"""Manual, passive asset inventory for explicitly wildcarded scopes."""
from __future__ import annotations

import json
import logging
import re
import subprocess
from collections import defaultdict
from time import monotonic
from urllib.parse import urlsplit

import requests

from core.diff import utcnow
from core.discovery_sources import PROVIDERS, DiscoveryProviderError, configured_providers, lookup

log = logging.getLogger(__name__)
_CT_URL = 'https://crt.sh/'
_CT_MAX_BYTES = 16 * 1024 * 1024
_LABEL = r'[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?'
_HOST = re.compile(rf'{_LABEL}(?:\.{_LABEL})+\Z', re.ASCII)
_SOURCE = re.compile(r'[a-z0-9][a-z0-9_-]{0,63}\Z', re.ASCII)


class DiscoveryScopeError(ValueError):
    """The program exclusions could not be applied safely."""


def hostname(value: str, *, allow_url: bool = True) -> str | None:
    """Accept hostnames (or HTTP URLs), not paths, IPs, prose or patterns."""
    if not isinstance(value, str):
        return None
    value = value.strip().lower().rstrip('.')
    if allow_url and value.startswith(('http://', 'https://')):
        try:
            parsed = urlsplit(value)
            if parsed.username or parsed.password or not parsed.hostname:
                return None
            value = parsed.hostname.rstrip('.')
        except ValueError:
            return None
    if len(value) > 253 or not _HOST.fullmatch(value) or value.rsplit('.', 1)[-1].isdigit():
        return None
    return value


def excluded(host: str, exclusions: list[tuple[str, bool]]) -> bool:
    return any(host == domain or (wildcard and host.endswith('.' + domain))
               for domain, wildcard in exclusions)


def scope_roots(program: dict) -> tuple[set[str], list[tuple[str, bool]]]:
    exclusions = []
    for entry in program.get('outScopes') or []:
        if not isinstance(entry, str):
            raise DiscoveryScopeError('unparseable out-of-scope entry')
        entry = entry.strip()
        wildcard = entry.startswith('*.')
        domain = hostname(entry[2:] if wildcard else entry)
        if not domain:
            raise DiscoveryScopeError(f'unparseable out-of-scope entry: {entry!r}')
        exclusions.append((domain, wildcard))

    roots = set()
    for scope in program.get('scopes') or []:
        if isinstance(scope, str) and scope.strip().startswith('*.'):
            root = hostname(scope.strip()[2:], allow_url=False)
            if root and not excluded(root, exclusions):
                roots.add(root)
    return roots, exclusions


def _source_id(value: str) -> str | None:
    if not isinstance(value, str):
        return None
    value = value.strip().lower()
    if value in ('crt.sh', 'crtsh'):
        return 'crtsh'
    return value if _SOURCE.fullmatch(value) else None


def _subfinder(root: str, *, binary: str, timeout: int):
    try:
        result = subprocess.run([binary, '-d', root, '-silent', '-oJ', '-cs'], capture_output=True,
                                text=True, encoding='utf-8', errors='replace', timeout=timeout, check=True)
    except subprocess.TimeoutExpired as exc:
        raise DiscoveryProviderError('timed out') from exc
    except subprocess.CalledProcessError as exc:
        raise DiscoveryProviderError(f'exited with code {exc.returncode}') from exc
    except OSError as exc:
        raise DiscoveryProviderError('could not start Subfinder') from exc

    observations = []
    for line in result.stdout.splitlines():
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except ValueError as exc:
            raise DiscoveryProviderError('invalid Subfinder JSON output') from exc
        if not isinstance(row, dict) or not isinstance(row.get('host'), str):
            raise DiscoveryProviderError('invalid Subfinder JSON output')
        sources = row.get('sources')
        labels = sources if isinstance(sources, list) else []
        sources = {name for value in [*labels, row.get('source')] if (name := _source_id(value))}
        observations.append((row['host'], sources or {'subfinder'}))
    return observations


def _crtsh(root: str, *, timeout: int):
    # Query the public certificate index, never the discovered host itself.
    deadline = monotonic() + timeout
    payload = bytearray()
    try:
        with requests.get(_CT_URL, params={'q': f'%.{root}', 'output': 'json'},
                          timeout=(min(timeout, 10), timeout), stream=True, allow_redirects=False) as response:
            if response.status_code != 200:
                raise DiscoveryProviderError(f'HTTP {response.status_code}')
            for chunk in response.iter_content(65536):
                if monotonic() > deadline:
                    raise DiscoveryProviderError('timed out')
                if len(payload) + len(chunk) > _CT_MAX_BYTES:
                    raise DiscoveryProviderError('response exceeded size limit')
                payload.extend(chunk)
    except requests.RequestException as exc:
        raise DiscoveryProviderError('request failed') from exc

    try:
        rows = json.loads(payload)
    except ValueError as exc:
        raise DiscoveryProviderError('invalid certificate index response') from exc
    if not isinstance(rows, list):
        raise DiscoveryProviderError('invalid certificate index response')
    observations = []
    for row in rows:
        if not isinstance(row, dict) or not isinstance(row.get('name_value'), str):
            raise DiscoveryProviderError('invalid certificate index response')
        # A wildcard on a certificate is not evidence of an exact hostname.
        observations.extend((name, {'crtsh'}) for name in row['name_value'].splitlines()
                            if not name.lstrip().startswith('*.'))
    return observations


def discover_program(program: dict, collection, *, binary='subfinder', timeout=300, providers=None) -> dict:
    """Store accepted results across providers; retain earlier observations on partial runs."""
    selected = tuple(dict.fromkeys(configured_providers() if providers is None else providers))
    if not selected or any(provider not in PROVIDERS for provider in selected):
        raise ValueError('select at least one supported discovery provider')
    if timeout <= 0:
        raise ValueError('timeout must be positive')
    roots, exclusions = scope_roots(program)
    found = defaultdict(set)
    per_provider = {}
    appearances = defaultdict(set)
    failures = 0
    for provider in selected:
        accepted = set()
        failed = limited = 0
        for root in sorted(roots):
            try:
                if provider == 'subfinder':
                    results = _subfinder(root, binary=binary, timeout=timeout)
                elif provider == 'crtsh':
                    results = _crtsh(root, timeout=min(timeout, 45))
                else:
                    outcome = lookup(provider, root, timeout=min(timeout, 45))
                    limited += int(outcome.limited)
                    if outcome.error:
                        log.warning('%s incomplete for %s: %s', provider, root, outcome.error)
                        failed += 1
                    results = ((name, {provider}) for name in outcome.names)
            except DiscoveryProviderError as exc:
                log.warning('%s failed for %s: %s', provider, root, exc)
                failed += 1
                continue
            for value, sources in results:
                host = hostname(value, allow_url=False)
                if host and host.endswith('.' + root) and not excluded(host, exclusions):
                    found[host].update(sources)
                    accepted.add(host)
                    appearances[host].add(provider)
        per_provider[provider] = {'hosts': len(accepted), 'exclusive_hosts': 0, 'failures': failed,
                                  'limited': limited, 'succeeded': len(roots) - failed}
        failures += failed

    for via in appearances.values():
        if len(via) == 1:
            per_provider[next(iter(via))]['exclusive_hosts'] += 1

    now = utcnow()
    seen = now.isoformat(timespec='milliseconds')
    for host, sources in sorted(found.items()):
        key = {'source': program['source'], 'program_slug': program['slug'], 'host': host}
        collection.update_one(key, {
            '$max': {'last_seen_at': now, **{f'observations.{source}': seen for source in sorted(sources)}},
            '$setOnInsert': {'first_seen_at': now, 'resolved': False, 'ip': None},
        }, upsert=True)
    limited = sum(item['limited'] for item in per_provider.values())
    status = ('no_scope' if not roots else 'failed' if failures == len(roots) * len(selected) and not found
              else 'partial' if failures or limited else 'complete')
    return {'status': status, 'finished_at': seen, 'roots': len(roots), 'hosts': len(found),
            'failures': failures, 'limited': limited, 'providers': per_provider}
