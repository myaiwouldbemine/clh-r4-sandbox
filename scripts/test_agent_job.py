"""Local git-bundle publishing tests; no real GitHub or model calls."""
import os
import subprocess
import tempfile
import unittest
from unittest.mock import patch
from pathlib import Path
from agent_job import publish, prepare
from autonomous_lifecycle import Blocked

class PublishTests(unittest.TestCase):
    def setUp(self):
        self.old=os.getcwd(); self.tmp=tempfile.TemporaryDirectory(); os.chdir(self.tmp.name)
        self.run_git('init','--bare','origin.git')
        self.run_git('init','-b','main','work'); os.chdir('work')
        self.run_git('config','user.name','test'); self.run_git('config','user.email','test@example.invalid')
        Path('README.md').write_text('base')
        self.run_git('add','.'); self.run_git('commit','-m','base')
        self.run_git('remote','add','origin',str(Path('../origin.git').resolve()))
        self.run_git('push','-u','origin','main')
        self.run_git('switch','-c','codex/issue-20')
        Path('candidate-code.py').write_text("raise Exception('MUST NOT EXECUTE')")
        self.run_git('add','.'); self.run_git('commit','-m','engineering work')
        Path('candidate').mkdir(); Path('candidate/pr-body.md').write_text('Issue: #20\nWork is BLOCKED on missing fixture content.')
        self.run_git('bundle','create','candidate/candidate.bundle','codex/issue-20')
        self.run_git('switch','main'); self.run_git('branch','-D','codex/issue-20')
        class API:
            repo='owner/repo'
            def __init__(self): self.prs=[]; self.writes=[]; self.state='open'
            def get(self,path,method='GET',data=None):
                if path=='issues/20': return {'state':self.state,'user':{'login':'owner'}}
                self.writes.append((path,method,data))
                if path=='pulls': self.prs=[{'number':21,'state':'open','merged_at':None}]
                return {}
            def pages(self,path): return self.prs
        self.gh=API()
    def tearDown(self): os.chdir(self.old); self.tmp.cleanup()
    def run_git(self,*args):
        return subprocess.check_output(['git',*args],stderr=subprocess.DEVNULL,text=True).strip()
    def test_publish_only_branch_and_draft_without_checkout(self):
        publish(self.gh,20)
        self.assertEqual(self.run_git('branch','--show-current'),'main')
        self.assertFalse(Path('candidate-code.py').exists())
        self.assertTrue(self.gh.writes[0][2]['draft'])
        self.assertEqual(self.run_git('rev-parse','origin/main'),self.run_git('rev-parse','main'))
    def test_duplicate_reuses_pr(self):
        publish(self.gh,20); publish(self.gh,20)
        self.assertEqual(sum(p=='pulls' for p,_,_ in self.gh.writes),1)
        self.assertEqual(self.gh.writes[-1][0],'pulls/21')
    def test_stopped_issue_never_publishes(self):
        self.gh.state='closed'
        with self.assertRaises(Blocked): publish(self.gh,20)
        self.assertFalse(self.gh.writes)
    def test_automatic_closure_keyword_rejected(self):
        Path('candidate/pr-body.md').write_text('Fixes #20')
        with self.assertRaises(Blocked): publish(self.gh,20)
        self.assertFalse(self.gh.writes)

    def setup_attempt_fixture(self, previous_issue):
        for i in range(1,4):
            self.run_git('commit','--allow-empty','-m',f'CLH agent attempt {i} for Issue {previous_issue}')
        issue={'number':20,'state':'open','user':{'login':'owner'},'body':'## WHAT\nEngineering task'}
        self.gh.get=lambda path: issue
        self.gh.pages=lambda path: []
        return issue
    def test_other_issue_attempts_do_not_exhaust_new_issue(self):
        issue=self.setup_attempt_fixture(19)
        with patch.dict(os.environ,{'GITHUB_OUTPUT':str(Path('outputs').resolve())}):
            prepare(self.gh,{'issue':issue})
        self.assertEqual(self.run_git('log','-1','--format=%s'),'CLH agent attempt 1 for Issue 20')
    def test_same_issue_three_attempts_stop(self):
        issue=self.setup_attempt_fixture(20)
        with patch.dict(os.environ,{'GITHUB_OUTPUT':str(Path('outputs').resolve())}):
            with self.assertRaisesRegex(Blocked,'retry budget exhausted'):
                prepare(self.gh,{'issue':issue})
        self.assertEqual(self.run_git('log','-1','--format=%s'),'CLH agent attempt 3 for Issue 20')

if __name__=='__main__': unittest.main()
