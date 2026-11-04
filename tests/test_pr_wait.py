"""Exercise the watcher CLI with a local gh double, never a live GitHub PR."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / 'skills/babysit-pr/scripts/pr-wait'
HEAD = 'a' * 40

FAKE_GH = r'''#!/usr/bin/env python3
import json, os, sys
from pathlib import Path
fixture = json.loads(os.environ['PR_WAIT_FIXTURE'])
args = sys.argv[1:]
if args[:2] == ['pr', 'view']:
    print(json.dumps({'number': 1, 'headRefOid': fixture['pr']['headRefOid']}))
elif args[:2] == ['pr', 'checks']:
    print(json.dumps(fixture['checks']))
elif args[:2] == ['api', 'graphql']:
    pr = fixture['pr']
    if 'pr_snapshots' in fixture:
        counter = Path(os.environ['HOME']) / 'graphql-calls'
        count = int(counter.read_text()) if counter.exists() else 0
        pr = fixture['pr_snapshots'][min(count, len(fixture['pr_snapshots']) - 1)]
        counter.write_text(str(count + 1))
    if 'cursor=threads-next' in args:
        pr = dict(pr, reviewThreads=fixture['next_threads'])
    if 'cursor=reviews-next' in args:
        pr = dict(pr, reviews=fixture['next_reviews'])
    print(json.dumps({'data': {'viewer': {'login': 'operator'},
                              'repository': {'pullRequest': pr}}}))
elif args[0] == 'api' and '/rules/branches/' in args[1]:
    if fixture.get('rules_error'):
        print('HTTP 403: forbidden', file=sys.stderr)
        sys.exit(1)
    print('\n'.join(fixture['required']))
elif args[0] == 'api' and '/protection/required_status_checks' in args[1]:
    pass
elif args[0] == 'api' and '/compare/' in args[1]:
    print(fixture.get('behind_by', 0))
else:
    print('Unexpected gh invocation: ' + repr(args), file=sys.stderr)
    sys.exit(3)
'''

RUNNER = '''import runpy, sys, time
polls = 0
def bounded_sleep(seconds):
    global polls
    polls += 1
    if polls > 4:
        print('Fixture polling budget ended')
        sys.exit(75)
time.sleep = bounded_sleep
sys.argv = [sys.argv[1], *sys.argv[2:]]
runpy.run_path(sys.argv[0], run_name='__main__')
'''


def connection(nodes=(), more=False):
    return {'nodes': list(nodes), 'pageInfo': {'hasNextPage': more,
                                            'endCursor': 'threads-next' if more else None}}


def fixture():
    return {
        'required': ['ci'],
        'checks': [{'name': 'ci', 'bucket': 'pass', 'link': 'https://ci.example/1', 'description': ''},
                   {'name': 'Greptile', 'bucket': 'pass', 'link': 'https://ci.example/2', 'description': ''}],
        'pr': {'state': 'OPEN', 'url': 'https://github.com/example/repo/pull/1',
               'headRefOid': HEAD, 'baseRefName': 'main', 'mergeStateStatus': 'CLEAN',
               'isDraft': False, 'reviewDecision': 'APPROVED',
               'author': {'login': 'author'}, 'viewer': 'operator',
               'baseRef': {'target': {'oid': 'b' * 40}},
               'comments': connection(), 'reviews': connection(), 'reviewThreads': connection()}}


class WatcherCliTests(unittest.TestCase):
    def run_watcher(self, data, until='ready'):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            executable = root / 'gh'
            executable.write_text(FAKE_GH)
            executable.chmod(0o755)
            environment = dict(os.environ, HOME=temp, PATH=temp + os.pathsep + os.environ['PATH'],
                               PR_WAIT_FIXTURE=json.dumps(data))
            return subprocess.run([sys.executable, '-c', RUNNER, str(SCRIPT), '1',
                                   '--repo', 'example/repo', '--until', until],
                                  env=environment, capture_output=True, text=True, timeout=10)

    def assert_blocked(self, data, reason):
        result = self.run_watcher(data)
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertNotIn('Traceback', result.stderr)
        self.assertIn(reason, result.stdout)
        self.assertNotIn('ready on', result.stdout)

    def test_clean_pr_is_ready(self):
        result = self.run_watcher(fixture())
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('ready on', result.stdout)

    def test_human_changes_requested_blocks_ready(self):
        data = fixture()
        data['pr']['mergeStateStatus'] = 'BLOCKED'
        data['pr']['reviewDecision'] = 'CHANGES_REQUESTED'
        self.assert_blocked(data, 'changes requested')

    def test_failed_review_bot_blocks_ready(self):
        data = fixture()
        data['checks'][1]['bucket'] = 'fail'
        self.assert_blocked(data, 'review check failed')

    def test_outstanding_human_review_without_required_review_policy_blocks(self):
        data = fixture()
        data['pr']['reviewDecision'] = None
        data['pr']['reviews'] = connection([{'id': 'review', 'url': 'https://review.example/1',
            'body': 'Still incorrect', 'state': 'CHANGES_REQUESTED', 'commit': {'oid': 'c' * 40},
            'author': {'login': 'reviewer', '__typename': 'User'}}])
        self.assert_blocked(data, 'changes requested')

    def test_later_approval_supersedes_same_reviewers_change_request(self):
        data = fixture()
        data['pr']['reviews'] = connection([{'id': str(i), 'url': 'https://review.example/1',
            'body': '', 'state': state, 'commit': {'oid': HEAD},
            'author': {'login': 'reviewer', '__typename': 'User'}}
            for i, state in enumerate(('CHANGES_REQUESTED', 'APPROVED'))])
        result = self.run_watcher(data)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_pending_ci_does_not_treat_blocked_as_a_permanent_failure(self):
        data = fixture()
        data['checks'][0]['bucket'] = 'pending'
        data['pr']['mergeStateStatus'] = 'BLOCKED'
        result = self.run_watcher(data)
        self.assertEqual(result.returncode, 75, result.stdout + result.stderr)
        self.assertNotIn('ready on', result.stdout)

    def test_second_active_review_bot_must_finish(self):
        data = fixture()
        data['checks'].append({'name': 'Macroscope', 'bucket': 'pending', 'link': '', 'description': ''})
        result = self.run_watcher(data)
        self.assertEqual(result.returncode, 75, result.stdout + result.stderr)
        self.assertNotIn('ready on', result.stdout)

    def test_unreadable_required_rules_does_not_fall_back_to_green(self):
        data = fixture()
        data['rules_error'] = True
        result = self.run_watcher(data)
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn('cannot establish required checks', result.stdout)
        self.assertNotIn('ready on', result.stdout)

    def test_base_can_be_behind_even_when_merge_state_is_clean(self):
        data = fixture()
        data['behind_by'] = 2
        self.assert_blocked(data, '2 commits behind')

    def test_unknown_mergeability_does_not_report_ready(self):
        data = fixture()
        data['pr']['mergeStateStatus'] = 'UNKNOWN'
        result = self.run_watcher(data)
        self.assertEqual(result.returncode, 75, result.stdout + result.stderr)
        self.assertNotIn('ready on', result.stdout)

    def test_head_changed_during_final_read_is_rechecked(self):
        data = fixture()
        newer = json.loads(json.dumps(data['pr']))
        newer['headRefOid'] = 'c' * 40
        data['pr_snapshots'] = [data['pr'], data['pr'], newer, newer, newer]
        result = self.run_watcher(data)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('ready on ccccccc', result.stdout)
        self.assertNotIn('ready on aaaaaaa', result.stdout)

    def test_human_change_request_on_later_review_page_blocks(self):
        data = fixture()
        data['pr']['reviewDecision'] = None
        data['pr']['reviews'] = {'nodes': [], 'pageInfo': {
            'hasNextPage': True, 'endCursor': 'reviews-next'}}
        data['next_reviews'] = connection([{'id': 'late-review', 'url': 'https://review.example/late',
            'body': 'Incorrect', 'state': 'CHANGES_REQUESTED', 'commit': {'oid': HEAD},
            'author': {'login': 'reviewer', '__typename': 'User'}}])
        self.assert_blocked(data, 'changes requested')

    def test_no_ci_checks_can_finish_without_claiming_ci_passed(self):
        data = fixture()
        data['required'], data['checks'] = [], []
        data['pr']['reviews'] = connection([{'id': 'bot-review', 'url': 'https://review.example/1',
            'body': 'Reviewed', 'state': 'COMMENTED', 'commit': {'oid': HEAD},
            'author': {'login': 'greptile[bot]', '__typename': 'Bot'}}])
        result = self.run_watcher(data)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('no CI checks reported', result.stdout)

    def test_missing_required_approval_blocks_ready(self):
        data = fixture()
        data['pr']['mergeStateStatus'] = 'BLOCKED'
        data['pr']['reviewDecision'] = 'REVIEW_REQUIRED'
        self.assert_blocked(data, 'required approval')

    def test_draft_blocks_ready(self):
        data = fixture()
        data['pr']['isDraft'] = True
        self.assert_blocked(data, 'draft')

    def test_unresolved_thread_on_later_page_blocks_ready(self):
        data = fixture()
        data['pr']['reviewThreads'] = connection(more=True)
        data['next_threads'] = connection([{'id': 'thread-101', 'isResolved': False,
            'path': 'app.py', 'line': 4, 'comments': connection([{
                'id': 'comment-101', 'url': 'https://review.example/thread-101', 'body': 'Please fix',
                'author': {'login': 'reviewer', '__typename': 'User'}}])}])
        self.assert_blocked(data, 'unresolved threads')

    def test_green_mode_does_not_claim_merge_readiness(self):
        data = fixture()
        data['pr']['isDraft'] = True
        data['pr']['mergeStateStatus'] = 'BLOCKED'
        result = self.run_watcher(data, 'green')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('green on', result.stdout)
        self.assertNotIn('ready on', result.stdout)


if __name__ == '__main__':
    unittest.main()
