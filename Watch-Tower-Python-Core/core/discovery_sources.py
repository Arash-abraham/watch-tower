"""Read-only adapters for third-party DNS, certificate and web indexes."""
from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass, field
from time import monotonic
from urllib.parse import parse_qs, urlsplit

import requests

PUBLIC_PROVIDERS = ('subfinder', 'crtsh', 'commoncrawl')
PROVIDER_KEYS = {name: f'DISCOVERY_{name.upper()}_KEY' for name in (
    'securitytrails', 'dnsdb', 'urlscan', 'chaos', 'certspotter', 'virustotal',
)}
PROVIDERS = (*PUBLIC_PROVIDERS, *PROVIDER_KEYS)
_MAX_BYTES = 16 * 1024 * 1024
_MAX_PAGES = 3


class DiscoveryProviderError(Exception):
    """Provider failure with a safe, operator-facing reason."""


@dataclass
class Lookup:
    names: set[str] = field(default_factory=set)
    limited: bool = False
    error: str | None = None


def provider_key(name):
    return os.getenv(PROVIDER_KEYS[name], '').strip()


def configured_providers():
    return (*PUBLIC_PROVIDERS, *(name for name in PROVIDER_KEYS if provider_key(name)))


class RequestBudget:
    """Use fixed provider URLs with no redirects and one shared lookup budget."""

    def __init__(self, timeout):
        self.deadline = monotonic() + timeout
        self.remaining_bytes = _MAX_BYTES

    def read(self, url, *, params=None, headers=None, empty_status=None):
        remaining = self.deadline - monotonic()
        if remaining <= 0:
            raise DiscoveryProviderError('timed out')
        payload = bytearray()
        try:
            with requests.get(url, params=params, headers=headers, timeout=(min(10, remaining), remaining),
                              stream=True, allow_redirects=False) as response:
                if response.status_code == empty_status:
                    return b''
                if response.status_code != 200:
                    raise DiscoveryProviderError(f'HTTP {response.status_code}')
                for chunk in response.iter_content(65536):
                    if monotonic() >= self.deadline:
                        raise DiscoveryProviderError('timed out')
                    self.remaining_bytes -= len(chunk)
                    if self.remaining_bytes < 0:
                        raise DiscoveryProviderError('response exceeded size limit')
                    payload.extend(chunk)
        except requests.RequestException as exc:
            raise DiscoveryProviderError('request failed') from exc
        return payload

    def json(self, *args, **kwargs):
        return decode(self.read(*args, **kwargs))


def decode(data):
    try:
        return json.loads(data)
    except (ValueError, RecursionError) as exc:
        raise DiscoveryProviderError('invalid JSON response') from exc


def mapping(value):
    if not isinstance(value, dict):
        raise DiscoveryProviderError('unexpected response format')
    return value


def array(value):
    if not isinstance(value, list):
        raise DiscoveryProviderError('unexpected response format')
    return value


def strings(value):
    values = array(value)
    if not all(isinstance(item, str) for item in values):
        raise DiscoveryProviderError('unexpected hostname data')
    return values


def archived_host(value):
    if not isinstance(value, str):
        return None
    try:
        parsed = urlsplit(value)
        if parsed.scheme in ('http', 'https') and not parsed.username and not parsed.password:
            return parsed.hostname
    except ValueError:
        pass
    return None


def relative_hosts(values, root):
    names = set()
    for name in strings(values):
        name = name.strip().lower()
        if name and '*' not in name:
            names.add(name if name.endswith('.') or name.endswith('.' + root) or name == root else f'{name}.{root}')
    return names


def _commoncrawl(root, request, _key):
    origin = 'https://index.commoncrawl.org'
    indexes = array(request.json(f'{origin}/collinfo.json'))
    index = next((row['id'] for row in indexes if isinstance(row, dict) and isinstance(row.get('id'), str)
                  and re.fullmatch(r'CC-MAIN-[0-9]{4}-[0-9]{2}', row['id'])), None)
    if index is None:
        raise DiscoveryProviderError('could not identify the Common Crawl index')
    url = f'{origin}/{index}-index'
    params = {'url': f'*.{root}', 'output': 'json', 'pageSize': 1, 'fl': 'url'}
    count = request.read(url, params={**params, 'showNumPages': 'true'}, empty_status=404)
    if not count:
        return Lookup()
    pages = mapping(decode(count)).get('pages')
    if type(pages) is not int or pages < 0:
        raise DiscoveryProviderError('invalid Common Crawl page count')
    result = Lookup(limited=pages > _MAX_PAGES)
    for page in range(min(pages, _MAX_PAGES)):
        try:
            data = request.read(url, params={**params, 'page': page}, empty_status=404)
            for line in data.splitlines():
                if line.strip() and (host := archived_host(mapping(decode(line)).get('url'))):
                    result.names.add(host)
        except DiscoveryProviderError as exc:
            result.error = str(exc)
            break
    return result


def _securitytrails(root, request, key):
    data = mapping(request.json(f'https://api.securitytrails.com/v1/domain/{root}/subdomains',
                                headers={'APIKEY': key}))
    return Lookup(relative_hosts(data.get('subdomains'), root))


def _chaos(root, request, key):
    data = mapping(request.json(f'https://dns.projectdiscovery.io/dns/{root}/subdomains',
                                headers={'Authorization': key}))
    return Lookup(relative_hosts(data.get('subdomains'), root))


def _dnsdb(root, request, key):
    data = request.read(f'https://api.dnsdb.info/dnsdb/v2/lookup/rrset/name/*.{root}', params={'limit': 5000},
                        headers={'Accept': 'application/x-ndjson', 'X-API-Key': key})
    frames = [mapping(decode(line)) for line in data.splitlines() if line.strip()]
    if len(frames) < 2 or frames[0].get('cond') != 'begin' or frames[-1].get('cond') not in ('succeeded', 'limited'):
        raise DiscoveryProviderError('incomplete DNSDB stream')
    names = set()
    for frame in frames[1:-1]:
        if 'obj' in frame:
            name = mapping(frame['obj']).get('rrname')
            if not isinstance(name, str):
                raise DiscoveryProviderError('invalid DNSDB owner name')
            names.add(name)
    return Lookup(names, limited=frames[-1]['cond'] == 'limited')


def paginate(fetch):
    result = Lookup()
    cursor = None
    for _ in range(_MAX_PAGES):
        try:
            names, following = fetch(cursor)
            result.names.update(names)
            if following is None:
                return result
            if following == cursor:
                raise DiscoveryProviderError('pagination did not advance')
            cursor = following
        except DiscoveryProviderError as exc:
            result.error = str(exc)
            return result
    result.limited = True
    return result


def _certspotter(root, request, key):
    def fetch(after):
        params = {'domain': root, 'include_subdomains': 'true', 'expand': 'dns_names'}
        if after is not None:
            params['after'] = after
        rows = array(request.json('https://api.certspotter.com/v1/issuances', params=params,
                                  headers={'Authorization': f'Bearer {key}'}))
        names = {name for row in rows for name in strings(mapping(row).get('dns_names'))}
        following = mapping(rows[-1]).get('id') if rows else None
        if rows and not isinstance(following, str):
            raise DiscoveryProviderError('invalid Cert Spotter cursor')
        return names, following
    return paginate(fetch)


def _virustotal(root, request, key):
    def fetch(cursor):
        data = mapping(request.json(f'https://www.virustotal.com/api/v3/domains/{root}/subdomains',
                                    params={'limit': 40, 'cursor': cursor}, headers={'x-apikey': key}))
        next_link = mapping(data.get('links', {})).get('next')
        following = None
        if next_link:
            try:
                following = parse_qs(urlsplit(next_link).query).get('cursor', [None])[0]
            except (ValueError, TypeError, AttributeError):
                pass
            if not following:
                raise DiscoveryProviderError('invalid VirusTotal cursor')
        names = {name for row in array(data.get('data')) if isinstance(name := mapping(row).get('id'), str)}
        return names, following
    return paginate(fetch)


def _urlscan(root, request, key):
    consumed = 0

    def fetch(after):
        nonlocal consumed
        # Read the search index only; never submit new scans.
        params = {'q': f'page.domain:{root} AND task.visibility:public', 'size': 100, 'search_after': after}
        data = mapping(request.json('https://urlscan.io/api/v1/search/', params=params, headers={'API-Key': key}))
        rows = array(data.get('results'))
        names = set()
        for row in rows:
            page = mapping(mapping(row).get('page', {}))
            if isinstance(page.get('domain'), str):
                names.add(page['domain'])
        following = None
        consumed += len(rows)
        total = data.get('total')
        if rows and (data.get('has_more') or (type(total) is int and total > consumed)):
            sort = mapping(rows[-1]).get('sort') if rows else None
            if not isinstance(sort, list) or not sort or not all(isinstance(value, (str, int, float)) for value in sort):
                raise DiscoveryProviderError('invalid urlscan pagination token')
            following = ','.join(str(value).strip('"') for value in sort)
        return names, following
    return paginate(fetch)


_ADAPTERS = {
    'commoncrawl': _commoncrawl, 'securitytrails': _securitytrails, 'dnsdb': _dnsdb, 'urlscan': _urlscan,
    'chaos': _chaos, 'certspotter': _certspotter, 'virustotal': _virustotal,
}


def lookup(provider, root, timeout):
    key = provider_key(provider) if provider in PROVIDER_KEYS else None
    if provider in PROVIDER_KEYS and not key:
        raise DiscoveryProviderError(f'missing {PROVIDER_KEYS[provider]}')
    return _ADAPTERS[provider](root, RequestBudget(timeout), key)
