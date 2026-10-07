"""Execute the documented boundary examples against real validation/metric libraries."""
from contextlib import closing
from pathlib import Path
import re
import sqlite3
import unittest

import yaml
from pydantic import ValidationError
from prometheus_client import REGISTRY


def blocks(path, language):
    return re.findall(r'```' + language + r'\n(.*?)```', Path(path).read_text(), re.S)


class EngineeringExamples(unittest.TestCase):
    def test_http_outcomes_have_matching_counter_and_histogram_labels(self):
        path = 'skills/observability-and-instrumentation/references/metrics-and-alerts.md'
        namespace = {}
        exec(blocks(path, 'python')[0], namespace)
        record = namespace['record_request']
        record('api', 'GET', '/tasks/:id', '2xx', 0.1)
        record('api', 'GET', '/tasks/:id', '5xx', 0.2)
        for status in ['2xx', '5xx']:
            labels = {'service': 'api', 'method': 'GET', 'route': '/tasks/:id', 'status_class': status}
            self.assertEqual(REGISTRY.get_sample_value('http_requests_total', labels), 1)
            self.assertEqual(REGISTRY.get_sample_value('http_request_duration_seconds_count', labels), 1)
        for code in blocks(path, 'yaml'):
            yaml.safe_load(code)

    def test_reported_usage_accumulates_without_inventing_unknown_usage(self):
        namespace = {}
        for code in blocks('skills/observability-and-instrumentation/references/llm-agent.md', 'python'):
            exec(code, namespace)
        record = namespace['record_usage']
        record('configured-model', 'summarize', 100, 20, 0.002)
        record('configured-model', 'summarize', None, 5, None)
        labels = {'model': 'configured-model', 'purpose': 'summarize'}
        self.assertEqual(REGISTRY.get_sample_value('llm_tokens_total', {**labels, 'token_type': 'input'}), 100)
        self.assertEqual(REGISTRY.get_sample_value('llm_tokens_total', {**labels, 'token_type': 'output'}), 25)
        self.assertEqual(REGISTRY.get_sample_value('llm_cost_usd_total', labels), 0.002)
        record('unknown-model', 'summarize', None, None, None)
        self.assertIsNone(REGISTRY.get_sample_value('llm_tokens_total', {'model': 'unknown-model', 'purpose': 'summarize', 'token_type': 'input'}))

    def test_compound_cursor_preserves_rows_with_equal_timestamps(self):
        # SQLite exercises the tuple/order invariant; PostgreSQL query plans are
        # deliberately outside this fixture's scope.
        query = blocks('skills/performance-optimization/references/stack-examples.md', 'sql')[0]
        with closing(sqlite3.connect(':memory:')) as connection:
            connection.execute('CREATE TABLE events (id INTEGER PRIMARY KEY, created_at TEXT NOT NULL, payload TEXT)')
            rows = [(i, '2026-10-07' if i <= 5 else '2026-10-08', 'payload') for i in range(1, 8)]
            connection.executemany('INSERT INTO events VALUES (?, ?, ?)', rows)
            page = connection.execute('SELECT id, created_at, payload FROM events ORDER BY created_at DESC, id DESC LIMIT 2').fetchall()
            seen = []
            while page:
                seen.extend(row[0] for row in page)
                last_id, last_time, _ = page[-1]
                page = connection.execute(query, {'1': last_time, '2': last_id, '3': 2}).fetchall()
            self.assertEqual(seen, [7, 6, 5, 4, 3, 2, 1])

    def test_registration_and_patch_reject_privileged_fields(self):
        namespace = {}
        exec(blocks('skills/security-and-hardening/references/auth-and-input.md', 'python')[0], namespace)
        registration, patch = namespace['Registration'], namespace['TaskPatch']
        valid = {'email': 'user@example.com', 'password': 'long-valid-passphrase'}
        registration(**valid)
        with self.assertRaises(ValidationError):
            registration(**valid, role='admin')
        for field in ['ownerId', 'tenantId', 'role']:
            with self.assertRaises(ValidationError):
                patch(**{field: 'injected'})
        self.assertEqual(patch(title='safe').model_dump(exclude_unset=True), {'title': 'safe'})
        self.assertEqual(patch(completed=False).model_dump(exclude_unset=True), {'completed': False})
        self.assertEqual(patch().model_dump(exclude_unset=True), {})


if __name__ == '__main__':
    unittest.main()
