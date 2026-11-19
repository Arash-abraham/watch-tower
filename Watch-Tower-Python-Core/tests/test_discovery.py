import json
import subprocess
import unittest
from unittest.mock import MagicMock, patch

import mongomock
import requests

import discover
from core.discovery import discover_program, hostname
from database import db


def subfinder_output(*entries):
    return subprocess.CompletedProcess([], 0, stdout='\n'.join(map(json.dumps, entries)), stderr='')


def certificate_response(*names, status=200):
    reply = MagicMock(status_code=status)
    reply.__enter__.return_value = reply
    reply.iter_content.return_value = [json.dumps([{'name_value': name} for name in names]).encode()]
    return reply


class DiscoveryTests(unittest.TestCase):
    def setUp(self):
        self.database = mongomock.MongoClient(tz_aware=True).test
        self.collection = self.database.subdomains
        self.program = {'source': 'hackerone', 'slug': 'example', 'active': True,
                        'scopes': ['*.example.com', 'example.org', '*.example.com'],
                        'outScopes': ['*.private.example.com', 'blocked.example.com']}
        db.ensure_subdomain_indexes(self.database)

    def test_validate_hostnames(self):
        self.assertEqual(hostname('WWW.Example.com.'), 'www.example.com')
        for value in ['*.example.com', 'example.com/path', '127.0.0.1', '-bad.example.com', 'foo']:
            self.assertIsNone(hostname(value))

    @patch('core.discovery.requests.get')
    @patch('core.discovery.subprocess.run')
    def test_merges_provenance_and_filters_both_providers(self, run, get):
        run.return_value = subfinder_output(
            {'host': 'A.example.com', 'sources': ['crtsh', 'certspotter', 'invalid.key']},
            {'host': 'tools.example.com', 'source': 'hackertarget'},
            {'host': 'notexample.com'}, {'host': 'x.private.example.com'},
        )
        get.return_value = certificate_response(
            'a.example.com\nCT.example.com.\nct.example.com\n*.wild.example.com\nblocked.example.com',
            'example.com\napi.example.org\nexample.com.other.org\nhttps://bad.example.com/',
        )
        result = discover_program(self.program, self.collection, providers=('subfinder', 'crtsh'))
        self.assertEqual(result['status'], 'complete')
        self.assertEqual((result['roots'], result['hosts'], result['failures']), (1, 3, 0))
        for counts in result['providers'].values():
            self.assertEqual(counts, {'hosts': 2, 'exclusive_hosts': 1, 'succeeded': 1, 'failures': 0, 'limited': 0})
        self.assertEqual({item['host'] for item in self.collection.find()},
                         {'a.example.com', 'ct.example.com', 'tools.example.com'})
        existing = self.collection.find_one({'host': 'a.example.com'})
        self.assertEqual(existing['observations'], {'crtsh': result['finished_at'], 'certspotter': result['finished_at']})
        self.assertFalse(existing['resolved'])
        self.assertIsNone(existing['ip'])
        self.assertEqual(run.call_args.args[0], ['subfinder', '-d', 'example.com', '-silent', '-oJ', '-cs'])
        get.assert_called_once_with('https://crt.sh/', params={'q': '%.example.com', 'output': 'json'},
                                    timeout=(10, 45), stream=True, allow_redirects=False)

        discover_program(self.program, self.collection, providers=('crtsh',))
        self.assertEqual(self.collection.count_documents({}), 3)
        updated = self.collection.find_one({'host': 'a.example.com'})
        self.assertEqual(updated['first_seen_at'], existing['first_seen_at'])
        self.assertEqual(updated['observations']['certspotter'], existing['observations']['certspotter'])
        discover_program({**self.program, 'slug': 'other'}, self.collection, providers=('crtsh',))
        self.assertEqual(self.collection.count_documents({}), 5)

    @patch('core.discovery.requests.get')
    @patch('core.discovery.subprocess.run')
    def test_partial_run_keeps_other_provider_results(self, run, get):
        run.side_effect = subprocess.TimeoutExpired('subfinder', 1, output='unconfirmed.example.com')
        get.return_value = certificate_response('ct.example.com')
        result = discover_program(self.program, self.collection, providers=('subfinder', 'crtsh'))
        self.assertEqual((result['status'], result['hosts'], result['failures']), ('partial', 1, 1))
        self.assertEqual(self.collection.find_one()['host'], 'ct.example.com')

    @patch('core.discovery.requests.get')
    @patch('core.discovery.subprocess.run')
    def test_all_providers_fail_but_dont_delete_history(self, run, get):
        self.collection.insert_one({'source': 'hackerone', 'program_slug': 'example', 'host': 'old.example.com'})
        run.return_value = subprocess.CompletedProcess([], 0, stdout='not-json', stderr='')
        get.return_value = certificate_response(status=429)
        result = discover_program(self.program, self.collection, providers=('subfinder', 'crtsh'))
        self.assertEqual((result['status'], result['hosts'], result['failures']), ('failed', 0, 2))
        self.assertEqual(self.collection.count_documents({}), 1)

    @patch('core.discovery.requests.get')
    def test_ct_rejects_malformed_large_and_unavailable_responses(self, get):
        reply = certificate_response('a.example.com')
        reply.iter_content.return_value = [b'not JSON']
        large = certificate_response('b.example.com')
        get.side_effect = [reply, large, requests.Timeout()]
        for limit in (100, 8, 100):
            with patch('core.discovery._CT_MAX_BYTES', limit):
                result = discover_program(self.program, self.collection, providers=('crtsh',))
            self.assertEqual(result['status'], 'failed')
        self.assertEqual(self.collection.count_documents({}), 0)

    @patch('core.discovery.requests.get')
    @patch('core.discovery.subprocess.run')
    def test_no_wildcard_or_unparseable_exclusion_never_queries_providers(self, run, get):
        invalid = {**self.program, 'scopes': ['example.com', '*.https://example.com']}
        self.assertEqual(discover_program(invalid, self.collection)['status'], 'no_scope')
        self.program['outScopes'] = ['all other assets are excluded']
        with self.assertRaises(ValueError):
            discover_program(self.program, self.collection, providers=('subfinder', 'crtsh'))
        run.assert_not_called()
        get.assert_not_called()

    @patch('core.discovery.requests.get')
    def test_cli_records_latest_failed_run_with_selected_provider(self, get):
        self.database.programs.insert_one(self.program)
        get.return_value = certificate_response(status=429)
        with patch.object(discover.db, 'get_db', return_value=self.database):
            self.assertEqual(discover.main(['--source', 'hackerone', '--program', 'example', '--provider', 'crtsh']), 1)
        summary = self.database.programs.find_one()['discovery']
        self.assertEqual(summary['status'], 'failed')
        self.assertEqual(set(summary['providers']), {'crtsh'})

    @patch('core.discovery.requests.get')
    @patch('core.discovery.subprocess.run')
    def test_cli_records_blocked_scope_without_contacting_providers(self, run, get):
        self.program['outScopes'] = ['all other assets are excluded']
        self.database.programs.insert_one(self.program)
        with patch.object(discover.db, 'get_db', return_value=self.database):
            self.assertEqual(discover.main(['--source', 'hackerone', '--program', 'example']), 1)
        self.assertEqual(self.database.programs.find_one()['discovery']['status'], 'blocked_scope')
        run.assert_not_called()
        get.assert_not_called()

    def test_upgrade_old_index(self):
        self.collection.drop_indexes()
        self.collection.create_index('host', unique=True)
        db.ensure_subdomain_indexes(self.database)
        self.assertNotIn('host_1', self.collection.index_information())
