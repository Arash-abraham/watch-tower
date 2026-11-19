#!/usr/bin/env python3
"""Run passive, multi-source discovery for a single, explicitly selected program."""
import argparse
import logging
import sys

from core.diff import utcnow
from core.discovery import DiscoveryScopeError, discover_program
from core.discovery_sources import PROVIDERS, PROVIDER_KEYS, configured_providers, provider_key
from database import db


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', required=True, help='program source')
    parser.add_argument('--program', required=True, help='program slug')
    parser.add_argument('--subfinder', default='subfinder', help='path to subfinder executable')
    parser.add_argument('--provider', action='append', choices=PROVIDERS,
                        help='select a provider (repeatable; default: public providers plus providers with configured keys)')
    parser.add_argument('--timeout', type=int, default=300, help='timeout per provider and wildcard root (HTTP providers capped at 45 seconds)')
    args = parser.parse_args(argv)
    if args.timeout <= 0:
        parser.error('--timeout must be positive')
    for provider in args.provider or ():
        if provider in PROVIDER_KEYS and not provider_key(provider):
            parser.error(f'{provider} requires {PROVIDER_KEYS[provider]} in the collector environment')
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    try:
        database = db.get_db()
        program = database[db.PROGRAMS].find_one({'source': args.source, 'slug': args.program, 'active': True})
        if not program:
            raise ValueError('active program not found; sync it first')
        db.ensure_subdomain_indexes(database)
        try:
            result = discover_program(program, database[db.SUBDOMAINS], binary=args.subfinder,
                                      timeout=args.timeout, providers=args.provider or configured_providers())
        except DiscoveryScopeError as exc:
            logging.warning('discovery blocked: %s', exc)
            result = {'status': 'blocked_scope', 'finished_at': utcnow().isoformat(timespec='milliseconds'),
                      'roots': 0, 'hosts': 0, 'failures': 0, 'limited': 0, 'providers': {}}
        database[db.PROGRAMS].update_one({'_id': program['_id']}, {'$set': {'discovery': result}})
    except Exception as exc:
        logging.error('discovery failed: %s', exc)
        return 1
    logging.info('discovery (%(status)s): %(roots)s wildcard roots, %(hosts)s distinct hosts, %(failures)s failed and %(limited)s limited attempts', result)
    for provider, counts in result['providers'].items():
        logging.info('%s: %s accepted hosts (%s exclusive to this path); %s failed, %s limited roots',
                     provider, counts['hosts'], counts['exclusive_hosts'], counts['failures'], counts['limited'])
    return 1 if result['failures'] or result['status'] == 'blocked_scope' else 0


if __name__ == '__main__':
    sys.exit(main())
