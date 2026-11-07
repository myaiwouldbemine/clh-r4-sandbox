"""Local safety/regression tests; injected APIs are not live E2E."""
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from autonomous_lifecycle import Blocked, process, main, local_lock, read_deployed_sha
from test_autonomous_lifecycle import Fake, HEAD, BASE, MERGE, body

class OnDemandTests(unittest.TestCase):
    def test_read_only_check_keeps_draft_and_issue_open(self):
        f = Fake()
        self.assertIn('read-only', process(f,21,expected_head=HEAD,expected_base=BASE,check_only=True))
        self.assertTrue(f.pr['draft'])
        self.assertTrue(all(method=='GET' for _,method,_ in f.calls))
        self.assertEqual(f.comments,[])

    def test_explicit_stale_inputs_block_before_mutation(self):
        for kw in ({'expected_head':'d'*40},{'expected_base':'d'*40}):
            f=Fake()
            with self.assertRaises(Blocked): process(f,21,**kw)
            self.assertTrue(all(method=='GET' for _,method,_ in f.calls))

    def test_no_cli_target_or_sha_never_calls_api(self):
        for args in ([],['--pr','21'],['--pr','21','--head',HEAD]):
            with patch('autonomous_lifecycle.GitHub.api') as api:
                with self.assertRaises(Blocked): main(['run','--repo','owner/repo']+args)
                api.assert_not_called()

    def test_no_broad_reconcile_command(self):
        with self.assertRaises(SystemExit): main(['reconcile'])

    def test_ready_races_block_merge(self):
        for change in ('head','base','body','issue','ci'):
            f=Fake(); original=f.graphql
            def graphql(query, **kw):
                result=original(query,**kw)
                if query.startswith('mutation'):
                    if change=='head': f.pr['head']['sha']='d'*40
                    if change=='base': f.base='d'*40
                    if change=='body': f.pr['body']+=' changed'
                    if change=='issue': f.issue['body']+=' changed'
                    if change=='ci': f.checks[0]['conclusion']='failure'
                return result
            f.graphql=graphql
            with self.subTest(change=change), self.assertRaises(Blocked): process(f,21)
            self.assertFalse(f.pr['merged'])
            self.assertEqual(f.issue['state'],'open')

    def test_archive_permission_recovery_does_not_remerge(self):
        f=Fake(); f.fail=('issues/20/comments','POST')
        with self.assertRaises(Blocked): process(f,21)
        f.fail=None
        process(f,21)
        self.assertEqual(sum(method=='PUT' for _,method,_ in f.calls),1)
        self.assertEqual(len(f.comments),1)

    def test_issue_edit_during_archive_blocks_close(self):
        f=Fake(); original=f.get
        def get(path, **kw):
            result=original(path,**kw)
            if path.startswith('issues/comments/'): f.issue['body']+=' changed'
            return result
        f.get=get
        with self.assertRaisesRegex(Blocked,'Issue changed before closure'): process(f,21)
        self.assertEqual(f.issue['state'],'open')

    def test_deployed_bytes_mismatch_blocks(self):
        with patch('autonomous_lifecycle.urllib.request.urlopen') as request:
            response = request.return_value.__enter__.return_value
            response.status = 200
            response.geturl.return_value = 'https://example.invalid/'
            response.read.return_value=b'wrong'
            with self.assertRaisesRegex(Blocked,'SHA mismatch'):
                read_deployed_sha('https://example.invalid/',MERGE)
            request.return_value.__enter__.return_value.read.return_value=MERGE.encode()
            read_deployed_sha('https://example.invalid/',MERGE)

    def test_lock_conflict_and_release(self):
        with tempfile.TemporaryDirectory() as directory:
            with patch('autonomous_lifecycle.subprocess.check_output',return_value=directory):
                with local_lock():
                    with self.assertRaisesRegex(Blocked,'active'):
                        with local_lock(): pass
                with local_lock(): pass

    def test_pages_marker_cannot_bypass_fresh_readback(self):
        f=Fake(); f.pr.update(merged=True, state='closed',merge_commit_sha=MERGE)
        f.pr['body']=body(deployment=True)
        f.comments=[{'id':1,'body':f'<!-- clh-deployed:{MERGE} -->\n'+json.dumps({'run_id':'123','url':'https://example.invalid/'})}]
        original=f.get
        def get(path, **kw):
            if path=='pages': return {'html_url':'https://example.invalid/'}
            if path=='actions/runs/123': return {'head_sha':MERGE,'conclusion':'success','path':'.github/workflows/pages.yml','head_branch':'main','html_url':'run'}
            return original(path,**kw)
        f.get=get
        with patch('autonomous_lifecycle.read_deployed_sha',side_effect=Blocked('Remote deployment SHA mismatch')):
            with self.assertRaises(Blocked): process(f,21)
        self.assertEqual(f.issue['state'],'open'); self.assertEqual(len(f.comments),1)

    def test_workflow_boundaries(self):
        for name in ('issue-agent','merge-and-close-pr'):
            text=Path(f'.github/workflows/{name}.yml').read_text()
            self.assertIn("if: github.event_name != 'workflow_dispatch'",text)
            for forbidden in ('schedule:', 'workflow_run:', 'secrets.', 'issues:', 'contents: write'):
                self.assertNotIn(forbidden,text)
        pages=Path('.github/workflows/pages.yml').read_text()
        for forbidden in ('CLH_AUTOMATION_TOKEN','OPENAI_API_KEY','CLH_AUTONOMY_ENABLED'):
            self.assertNotIn(forbidden,pages)
        self.assertIn('expected_sha:',pages)
        self.assertIn('push:\n    branches: [main]',pages)

    def test_hosted_publisher_cli_disabled(self):
        p=subprocess.run(['python3','scripts/agent_job.py','publish','20'],capture_output=True,text=True)
        self.assertNotEqual(p.returncode,0)
        self.assertIn('retired',p.stderr)

if __name__=='__main__': unittest.main()
