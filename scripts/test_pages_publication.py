import unittest
from unittest.mock import Mock, patch

from autonomous_lifecycle import Blocked, deployment_verified, publication_check
from test_autonomous_lifecycle import BASE, HEAD, MERGE, body


class PublicationTests(unittest.TestCase):
    def setUp(self):
        self.gh = Mock(repo='owner/repo')
        self.pr = {'merged_at': 'now', 'merge_commit_sha': MERGE, 'body': None,
                   'base': {'ref': 'main', 'repo': {'full_name': self.gh.repo}},
                   'head': {'sha': HEAD, 'repo': {'full_name': self.gh.repo}}}
        self.gh.pages.return_value = [self.pr]
        self.gh.get.side_effect = {
            'git/ref/heads/main': {'object': {'sha': MERGE}},
            f'git/commits/{MERGE}': {'parents': [{'sha': BASE}, {'sha': HEAD}]},
            'pages': {'html_url': 'https://example.invalid/'}
        }.__getitem__

    @patch('autonomous_lifecycle.protection')
    def test_events(self, protection):
        for pr_body in (None, body(deployment=True), body(deployment=False)):
            self.pr['body'] = pr_body
            publication_check(self.gh, MERGE, 'push', None)
            publication_check(self.gh, MERGE, 'workflow_dispatch', MERGE)
        protection.assert_called_with(self.gh, deployment=True)
        for sha, event, expected in [(MERGE, 'workflow_dispatch', HEAD),
                                     (HEAD, 'push', None), (MERGE, 'schedule', None)]:
            with self.assertRaises(Blocked):
                publication_check(self.gh, sha, event, expected)

    @patch('autonomous_lifecycle.protection')
    def test_invalid_pr(self, protection):
        for changes in ({'merged_at': None}, {'merge_commit_sha': HEAD},
                        {'body': '<!-- clh-lifecycle broken -->'}, {'body': body(base=HEAD)}):
            with self.subTest(changes=changes), patch.dict(self.pr, changes), self.assertRaises(Blocked):
                publication_check(self.gh, MERGE, 'push', None)

    @patch('autonomous_lifecycle.read_deployed_sha')
    def test_ordinary_and_non_site_have_no_issue_writes(self, read):
        for pr_body in (None, body(deployment=False)):
            self.pr['body'] = pr_body
            deployment_verified(self.gh, MERGE, '123')
        self.assertEqual(read.call_count, 2)
