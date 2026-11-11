#!/usr/bin/env python3
"""Run passive subfinder discovery for a single, explicitly selected program."""
import argparse
import logging
import sys

from core.discovery import discover_program
from database import db


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', required=True, help='program source')
    parser.add_argument('--program', required=True, help='program slug')
    parser.add_argument('--subfinder', default='subfinder', help='path to subfinder executable')
    parser.add_argument('--timeout', type=int, default=300, help='timeout per wildcard domain in seconds')
    args = parser.parse_args(argv)
    if args.timeout <= 0:
        parser.error('--timeout must be positive')
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    try:
        database = db.get_db()
        program = database[db.PROGRAMS].find_one({'source': args.source, 'slug': args.program, 'active': True})
        if not program:
            raise ValueError('active program not found; sync it first')
        db.ensure_subdomain_indexes(database)
        result = discover_program(program, database[db.SUBDOMAINS], binary=args.subfinder, timeout=args.timeout)
    except Exception as exc:
        logging.error('discovery failed: %s', exc)
        return 1
    logging.info('discovery: %(roots)s wildcard roots, %(hosts)s hosts, %(failures)s failures', result)
    return 1 if result['failures'] else 0


if __name__ == '__main__':
    sys.exit(main())
