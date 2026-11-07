"""Injected API/unit tests, deliberately NOT a live GitHub E2E claim."""
import copy
import hashlib
import json
import unittest
from unittest.mock import patch
from types import SimpleNamespace
from autonomous_lifecycle import (Blocked, GitHub, metadata, protection, process,
                                  archive_close, successful_checks, needs_deployment)

HEAD, BASE, MERGE = 'a'*40, 'b'*40, 'c'*40
ISSUE_BODY = '## WHAT\nEngineering fixture\n## WHY\nTest\n## DONE\nTested'

def meta(**changes):
    data = dict(issue=20, builder='Codex', head=HEAD, base=BASE,
                issue_body_sha256=hashlib.sha256(ISSUE_BODY.encode()).hexdigest(),
                scope_verified=True, self_review=True, complete=True, deployment=False,
                evidence='Actual unit fixture evidence; not a real engineering review.')
    data.update(changes)
    return data

def body(**changes):
    return 'Issue: #20\n<!-- clh-lifecycle '+json.dumps(meta(**changes))+' -->'

class Fake:
    repo = 'owner/repo'
    def __init__(self):
        self.pr = dict(number=21, body=body(), base={'ref':'main'}, head={'sha':HEAD,'repo':{'full_name':self.repo}},
                       state='open', merged=False, mergeable=True, draft=True, node_id='node',
                       merge_commit_sha=None, html_url='https://github.com/owner/repo/pull/21')
        self.issue = dict(state='open', user={'login':'owner'}, body=ISSUE_BODY)
        self.checks = [dict(name=name, status='completed', conclusion='success') for name in ('docs-check','governance-tests')]
        self.comments = []; self.calls = []; self.files = ['README.md']; self.fail = None
        self.archive_corrupt = False; self.base = BASE; self.threads = []; self.reviews = []; self.commits = []
    def get(self, path, method='GET', data=None):
        self.calls.append((path, method, data))
        if self.fail == (path, method): raise Blocked('Permission denied')
        if path == 'pulls/21' and method == 'GET': return copy.deepcopy(self.pr)
        if path == 'issues/20' and method == 'GET': return copy.deepcopy(self.issue)
        if path == 'git/ref/heads/main': return {'object': {'sha': self.base}}
        if path == 'rules/branches/main': return []
        if path == 'branches/main/protection':
            return dict(required_status_checks={'contexts':['docs-check','governance-tests'],'strict':True},
                        required_pull_request_reviews={}, enforce_admins={'enabled':True},
                        required_conversation_resolution={'enabled':True})
        if '/check-runs?' in path: return {'check_runs':self.checks}
        if path == 'pulls/21/merge' and method == 'PUT':
            self.pr.update(merged=True, state='closed', merge_commit_sha=MERGE)
            return {'merged':True,'sha':MERGE}
        if path == 'issues/20/comments' and method == 'POST':
            c = dict(id=len(self.comments)+1, body=data['body']); self.comments.append(c); return copy.deepcopy(c)
        if path.startswith('issues/comments/'):
            c = copy.deepcopy(self.comments[int(path.split('/')[-1])-1])
            if self.archive_corrupt: c['body'] += 'changed'
            return c
        if path == 'issues/20' and method == 'PATCH': self.issue['state']=data['state']; return self.issue
        raise AssertionError((path,method,data))
    def pages(self,path):
        if path=='pulls/21/files': return [{'filename':f} for f in self.files]
        if path.endswith('/statuses'): return []
        if path=='pulls/21/reviews': return self.reviews
        if path=='pulls/21/commits': return self.commits
        if path=='issues/20/comments': return copy.deepcopy(self.comments)
        raise AssertionError(path)
    def graphql(self, query, **variables):
        if query.startswith('mutation'):
            self.pr['draft']=False; return {}
        return {'repository':{'pullRequest':{'reviewThreads':{'nodes':self.threads,'pageInfo':{'hasNextPage':False}}}}}

class LifecycleTests(unittest.TestCase):
    def assert_no_merge(self, fake):
        self.assertFalse(any(method=='PUT' for _,method,_ in fake.calls))
        self.assertEqual(fake.issue['state'],'open')
    def test_deployment_effective_rules_and_local_bypass_visibility(self):
        rules = [dict(type=t, ruleset_id=1) for t in ('deletion','non_fast_forward')]
        rules += [dict(type='pull_request', ruleset_id=1, parameters={'required_review_thread_resolution':True}),
                  dict(type='required_status_checks', ruleset_id=1, parameters={'strict_required_status_checks_policy':True,
                       'required_status_checks':[{'context':n} for n in ('docs-check','governance-tests')]})]
        class Rules:
            def get(self, path):
                if path == 'rules/branches/main': return rules
                if path == 'rulesets/1': return {}
                raise Blocked('Unavailable')
        gh = Rules()
        protection(gh, deployment=True)
        with self.assertRaisesRegex(Blocked, 'bypass state unavailable'):
            protection(gh)
        rules[-1]['parameters']['strict_required_status_checks_policy'] = False
        with self.assertRaises(Blocked): protection(gh, deployment=True)
        rules.clear()
        with self.assertRaises(Blocked): protection(gh, deployment=True)

    def test_non_site_full_sequence_and_duplicate(self):
        f=Fake(); process(f,21); process(f,21)
        self.assertEqual(f.issue['state'],'closed')
        self.assertEqual(sum(method=='PUT' for _,method,_ in f.calls),1)
        self.assertEqual(len(f.comments),1)
        mutations=[(p,m) for p,m,_ in f.calls if m!='GET']
        self.assertLess(mutations.index(('pulls/21/merge','PUT')),mutations.index(('issues/20/comments','POST')))
        self.assertLess(mutations.index(('issues/20/comments','POST')),mutations.index(('issues/20','PATCH')))
    def test_all_non_success_ci_blocks(self):
        for result in ('failure','skipped','neutral','cancelled',None):
            with self.subTest(result=result):
                f=Fake(); f.checks[0]['conclusion']=result
                with self.assertRaises(Blocked): process(f,21)
                self.assert_no_merge(f)
    def test_ci_repair_reenters(self):
        f=Fake(); f.checks[0]['conclusion']='failure'
        with self.assertRaises(Blocked): process(f,21)
        f.checks[0]['conclusion']='success'; process(f,21)
        self.assertTrue(f.pr['merged'])
    def test_missing_check_blocks(self):
        f=Fake(); f.checks.pop()
        with self.assertRaises(Blocked): process(f,21)
        self.assert_no_merge(f)
    def test_pending_check_blocks(self):
        f=Fake(); f.checks[0]['status']='in_progress'
        with self.assertRaises(Blocked): process(f,21)
        self.assert_no_merge(f)
    def test_stale_head_and_base(self):
        for field in ('head','base'):
            f=Fake(); f.pr['body']=body(**{field:'d'*40})
            with self.assertRaises(Blocked): process(f,21)
            self.assert_no_merge(f)
    def test_changed_issue(self):
        f=Fake(); f.issue['body']+=' new requirements'
        with self.assertRaises(Blocked): process(f,21)
        self.assert_no_merge(f)
    def test_conflict_blocks(self):
        f=Fake(); f.pr['mergeable']=False
        with self.assertRaises(Blocked): process(f,21)
        self.assert_no_merge(f)
    def test_unknown_mergeability_blocks(self):
        f=Fake(); f.pr['mergeable']=None
        with self.assertRaises(Blocked): process(f,21)
        self.assert_no_merge(f)
    def test_threads_and_changes_requested(self):
        for kind in ('threads','reviews'):
            f=Fake()
            if kind=='threads': f.threads=[{'isResolved':False}]
            else: f.reviews=[{'user':{'login':'reviewer'},'state':'CHANGES_REQUESTED'}]
            with self.assertRaises(Blocked): process(f,21)
            self.assert_no_merge(f)
    def test_missing_protection_blocks(self):
        f=Fake(); f.fail=('branches/main/protection','GET')
        with self.assertRaises(Blocked): process(f,21)
        self.assert_no_merge(f)
    def test_merge_permission_denied_does_not_archive_close(self):
        f=Fake(); f.fail=('pulls/21/merge','PUT')
        with self.assertRaises(Blocked): process(f,21)
        self.assertFalse(f.pr['merged']); self.assertEqual(f.comments,[]); self.assertEqual(f.issue['state'],'open')
    def test_archive_permission_denied_does_not_close(self):
        f=Fake(); f.fail=('issues/20/comments','POST')
        with self.assertRaises(Blocked): process(f,21)
        self.assertTrue(f.pr['merged']); self.assertEqual(f.issue['state'],'open')
    def test_archive_corrupt_readback_does_not_close(self):
        f=Fake(); f.archive_corrupt=True
        with self.assertRaises(Blocked): process(f,21)
        self.assertEqual(f.issue['state'],'open')
    def test_close_failure_retry_reuses_archive(self):
        f=Fake(); f.fail=('issues/20','PATCH')
        with self.assertRaises(Blocked): process(f,21)
        f.fail=None
        with patch.dict('os.environ',{'CLH_RUN_URL':'different retry run'}): process(f,21)
        self.assertEqual(len(f.comments),1); self.assertEqual(f.issue['state'],'closed')
    def test_site_cannot_skip_deploy(self):
        f=Fake(); f.files=['docs/index.md']
        with self.assertRaises(Blocked): process(f,21)
        self.assert_no_merge(f)
    def test_deployment_pending_after_merge(self):
        f=Fake(); f.pr['body']=body(deployment=True)
        with self.assertRaisesRegex(Blocked,'Deployment verification PENDING'): process(f,21)
        self.assertTrue(f.pr['merged']); self.assertEqual(f.issue['state'],'open'); self.assertEqual(f.comments,[])
    def test_auto_closing_forms_rejected(self):
        for text in ('Fixes #20','closed owner/repo#20','Resolves https://github.com/owner/repo/issues/20'):
            with self.assertRaises(Blocked): metadata(body()+'\n'+text)
    def test_incomplete_scope_never_merges(self):
        f=Fake(); f.pr['body']=body(scope_verified=False)
        with self.assertRaises(Blocked): process(f,21)
        self.assert_no_merge(f)
    def test_api_error_never_discloses_raw_response(self):
        with patch('subprocess.run',return_value=SimpleNamespace(returncode=1,stdout='secret',stderr='secret')):
            with self.assertRaises(Blocked) as error: GitHub('owner/repo').get('pulls/21')
            self.assertNotIn('secret',str(error.exception))
    def test_commit_auto_close_rejected(self):
        f=Fake(); f.commits=[{'commit':{'message':'Fixes #20'}}]
        with self.assertRaises(Blocked): process(f,21)
        self.assert_no_merge(f)
    def test_deploy_success_requires_real_run_contract(self):
        f=Fake(); f.pr['body']=body(deployment=True)
        original=f.get
        def get(path, **kw):
            if path=='pages': return {'html_url':'https://owner.github.io/repo/'}
            if path=='actions/runs/123':
                return {'head_sha':MERGE,'conclusion':'success','path':'.github/workflows/pages.yml',
                        'head_branch':'main','html_url':'https://github.com/owner/repo/actions/runs/123'}
            return original(path,**kw)
        f.get=get
        f.comments=[{'id':1,'body':f'<!-- clh-deployed:{MERGE} -->\n'+json.dumps({'run_id':'123','url':'https://owner.github.io/repo/'})}]
        with patch('autonomous_lifecycle.read_deployed_sha') as readback:
            process(f,21)
        readback.assert_called_once_with('https://owner.github.io/repo/', MERGE)
        self.assertEqual(f.issue['state'],'closed')
    def test_deploy_failed_run_does_not_archive(self):
        f=Fake(); f.pr['body']=body(deployment=True)
        original=f.get
        def get(path, **kw):
            if path=='pages': return {'html_url':'https://owner.github.io/repo/'}
            if path=='actions/runs/123': return {'head_sha':MERGE,'conclusion':'failure'}
            return original(path,**kw)
        f.get=get
        f.comments=[{'id':1,'body':f'<!-- clh-deployed:{MERGE} -->\n'+json.dumps({'run_id':'123','url':'https://owner.github.io/repo/'})}]
        with self.assertRaises(Blocked): process(f,21)
        self.assertEqual(len(f.comments),1); self.assertEqual(f.issue['state'],'open')
    def test_head_race_before_ready_blocks(self):
        f=Fake(); original=f.get; reads=0
        def get(path, **kw):
            nonlocal reads
            if path=='pulls/21':
                reads+=1
                if reads==2: f.pr['head']['sha']='d'*40
            return original(path,**kw)
        f.get=get
        with self.assertRaises(Blocked): process(f,21)
        self.assertTrue(f.pr['draft']); self.assert_no_merge(f)
    def test_base_race_before_ready_blocks(self):
        f=Fake(); original=f.get; reads=0
        def get(path, **kw):
            nonlocal reads
            if path=='git/ref/heads/main':
                reads+=1
                if reads==2: f.base='d'*40
            return original(path,**kw)
        f.get=get
        with self.assertRaises(Blocked): process(f,21)
        self.assertTrue(f.pr['draft']); self.assert_no_merge(f)
    def test_sha_bound_merge(self):
        f=Fake(); process(f,21)
        self.assertEqual(next(d for p,m,d in f.calls if p=='pulls/21/merge')['sha'],HEAD)

if __name__=='__main__': unittest.main()
