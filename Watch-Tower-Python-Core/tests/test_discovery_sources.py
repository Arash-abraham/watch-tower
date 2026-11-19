import json
import os
import unittest
from unittest.mock import MagicMock, patch

import mongomock
import requests

from core import discovery_sources as sources
from core.discovery import discover_program


def reply(data, status=200):
    response = MagicMock(status_code=status)
    response.__enter__.return_value = response
    response.iter_content.return_value = [data if isinstance(data, bytes) else json.dumps(data).encode()]
    return response


class SourceTests(unittest.TestCase):
    def setUp(self):
        env = patch.dict(os.environ, {key: f'fake-{name}' for name, key in sources.PROVIDER_KEYS.items()})
        env.start()
        self.addCleanup(env.stop)
        mock = patch.object(sources.requests, 'get')
        self.get = mock.start()
        self.addCleanup(mock.stop)

    def lookup(self, name):
        return sources.lookup(name, 'example.com', 10)

    def test_commoncrawl_reads_latest_index_only_and_keeps_bounded_results(self):
        self.get.side_effect = [reply([{'id': 'CC-MAIN-2026-40', 'cdx-api': 'https://untrusted.test'}]),
                                reply({'pages': 6}), reply(b'{"url":"https://a.example.com/page"}\n'),
                                reply(b'{"url":"https://b.example.com/page"}\n'), reply(b'')]
        result = self.lookup('commoncrawl')
        self.assertEqual(result.names, {'a.example.com', 'b.example.com'})
        self.assertTrue(result.limited)
        self.assertEqual(self.get.call_count, 5)
        self.assertEqual({call.args[0] for call in self.get.call_args_list}, {
            'https://index.commoncrawl.org/collinfo.json', 'https://index.commoncrawl.org/CC-MAIN-2026-40-index',
        })
        self.assertFalse(self.get.call_args.kwargs['allow_redirects'])

    def test_commoncrawl_no_matches(self):
        self.get.side_effect = [reply([{'id': 'CC-MAIN-2026-40'}]), reply(b'', 404)]
        self.assertEqual(self.lookup('commoncrawl'), sources.Lookup())

    def test_securitytrails_and_chaos_use_relative_labels_and_auth_headers(self):
        for name, header in [('securitytrails', 'APIKEY'), ('chaos', 'Authorization')]:
            self.get.return_value = reply({'subdomains': ['one', 'nested.one', '*', 'a.example.com', 'external.org.']})
            self.assertEqual(self.lookup(name).names, {'one.example.com', 'nested.one.example.com', 'a.example.com', 'external.org.'})
            self.assertEqual(self.get.call_args.kwargs['headers'][header], f'fake-{name}')

    def test_dnsdb_requires_terminal_frame_and_surfaces_truncation(self):
        frames = b'{"cond":"begin"}\n{"obj":{"rrname":"api.example.com."}}\n'
        self.get.side_effect = [reply(frames + b'{"cond":"limited"}\n'), reply(frames)]
        self.assertEqual(self.lookup('dnsdb'), sources.Lookup({'api.example.com.'}, limited=True))
        with self.assertRaisesRegex(sources.DiscoveryProviderError, 'incomplete DNSDB stream'):
            self.lookup('dnsdb')

    def test_certspotter_keeps_results_if_later_page_fails(self):
        self.get.side_effect = [reply([{'id': '12', 'dns_names': ['api.example.com']}]), reply({}, 429)]
        result = self.lookup('certspotter')
        self.assertEqual(result, sources.Lookup({'api.example.com'}, error='HTTP 429'))
        self.assertEqual(self.get.call_args.kwargs['params']['after'], '12')
        self.assertEqual(self.get.call_args.kwargs['headers']['Authorization'], 'Bearer fake-certspotter')

    def test_urlscan_queries_search_index_with_sort_cursor(self):
        self.get.side_effect = [reply({'results': [{'page': {'domain': 'one.example.com'}, 'sort': [4, '"id"']}], 'has_more': False, 'total': 2}),
                                reply({'results': [{'page': {'domain': 'two.example.com'}}], 'has_more': False})]
        self.assertEqual(self.lookup('urlscan').names, {'one.example.com', 'two.example.com'})
        self.assertEqual(self.get.call_args.args[0], 'https://urlscan.io/api/v1/search/')
        self.assertEqual(self.get.call_args.kwargs['params']['search_after'], '4,id')
        self.assertIn('task.visibility:public', self.get.call_args.kwargs['params']['q'])

    def test_virustotal_uses_cursor_but_never_follows_response_url(self):
        self.get.side_effect = [reply({'data': [{'id': 'one.example.com'}], 'links': {'next': 'https://untrusted.test/?cursor=abc'}}),
                                reply({'data': [{'id': 'two.example.com'}], 'links': {}})]
        self.assertEqual(self.lookup('virustotal').names, {'one.example.com', 'two.example.com'})
        self.assertEqual(self.get.call_args.args[0], 'https://www.virustotal.com/api/v3/domains/example.com/subdomains')
        self.assertEqual(self.get.call_args.kwargs['params']['cursor'], 'abc')

    def test_missing_keys_are_not_auto_selected_or_requested(self):
        with patch.dict(os.environ, {key: '' for key in sources.PROVIDER_KEYS.values()}):
            self.assertEqual(sources.configured_providers(), ('subfinder', 'crtsh', 'commoncrawl'))
            with self.assertRaisesRegex(sources.DiscoveryProviderError, 'missing DISCOVERY_CHAOS_KEY'):
                self.lookup('chaos')
        self.get.assert_not_called()

    def test_http_errors_do_not_expose_credentials(self):
        self.get.side_effect = requests.ConnectionError('fake-securitytrails should not be logged')
        with self.assertRaisesRegex(sources.DiscoveryProviderError, '^request failed$'):
            self.lookup('securitytrails')

    def test_limited_results_are_saved_and_scope_is_enforced(self):
        self.get.return_value = reply(b'{"cond":"begin"}\n{"obj":{"rrname":"a.example.com."}}\n'
                                      b'{"obj":{"rrname":"blocked.example.com."}}\n'
                                      b'{"obj":{"rrname":"outside.test."}}\n{"cond":"limited"}\n')
        collection = mongomock.MongoClient().test.subdomains
        program = {'source': 'local', 'slug': 'example', 'scopes': ['*.example.com'], 'outScopes': ['blocked.example.com']}
        result = discover_program(program, collection, providers=('dnsdb',))
        self.assertEqual((result['status'], result['hosts'], result['failures'], result['limited']), ('partial', 1, 0, 1))
        self.assertEqual(collection.find_one()['observations'], {'dnsdb': result['finished_at']})
        self.assertEqual(collection.count_documents({}), 1)
