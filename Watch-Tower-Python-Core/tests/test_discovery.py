import os
import subprocess
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import mongomock
from core.discovery import discover_program, hostname
from database import db


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

    @patch('core.discovery.subprocess.run')
    def test_filters_and_upserts_per_program(self, run):
        run.return_value = subprocess.CompletedProcess([], 0, stdout='A.example.com\na.example.com\nexample.com\nnotexample.com\nx.private.example.com\nblocked.example.com\n', stderr='')
        result = discover_program(self.program, self.collection)
        self.assertEqual(result, {'roots': 1, 'hosts': 1, 'failures': 0})
        first = self.collection.find_one()['first_seen_at']
        discover_program(self.program, self.collection)
        self.assertEqual(self.collection.count_documents({}), 1)
        self.assertEqual(self.collection.find_one()['first_seen_at'], first)
        discover_program({**self.program, 'slug': 'other'}, self.collection)
        self.assertEqual(self.collection.count_documents({}), 2)
        run.assert_called_with(['subfinder', '-d', 'example.com', '-silent'], capture_output=True, text=True, timeout=300, check=True)

    @patch('core.discovery.subprocess.run')
    def test_failure_does_not_write_partial_output(self, run):
        run.side_effect = subprocess.TimeoutExpired('subfinder', 1)
        self.assertEqual(discover_program(self.program, self.collection)['failures'], 1)
        self.assertEqual(self.collection.count_documents({}), 0)

    @patch('core.discovery.subprocess.run')
    def test_unparseable_exclusion_fails_closed(self, run):
        self.program['outScopes'] = ['all other assets are excluded']
        with self.assertRaises(ValueError):
            discover_program(self.program, self.collection)
        run.assert_not_called()

    def test_upgrade_old_index(self):
        self.collection.drop_indexes()
        self.collection.create_index('host', unique=True)
        db.ensure_subdomain_indexes(self.database)
        self.assertNotIn('host_1', self.collection.index_information())
