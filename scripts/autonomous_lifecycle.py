#!/usr/bin/env python3
"""Small GitHub lifecycle client. No model identity or semantic-scope proof is claimed."""
import argparse
import hashlib
import json
import os
import re
import subprocess
import urllib.request
from pathlib import Path

REQUIRED = {'docs-check', 'governance-tests'}
SHA = re.compile(r'[0-9a-f]{40}')

class Blocked(RuntimeError):
    pass

def require(condition, message):
    if not condition:
        raise Blocked(message)

class GitHub:
    def __init__(self, repo):
        require(bool(re.fullmatch(r'[\w.-]+/[\w.-]+', repo)), 'Invalid repository')
        self.repo = repo

    def api(self, path, method='GET', data=None):
        command = ['gh', 'api', path, '--method', method]
        if data is not None:
            command += ['--input', '-']
        result = subprocess.run(command, input=json.dumps(data) if data is not None else None,
                                text=True, capture_output=True)
        require(result.returncode == 0, f'API unavailable: {method} {path}')
        return json.loads(result.stdout) if result.stdout.strip() else None

    def get(self, path, **kwargs):
        return self.api(f'repos/{self.repo}/{path}', **kwargs)

    def pages(self, path):
        result = []
        for page in range(1, 101):
            sep = '&' if '?' in path else '?'
            rows = self.get(f'{path}{sep}per_page=100&page={page}')
            require(isinstance(rows, list), 'Invalid pagination response')
            result.extend(rows)
            if len(rows) < 100:
                return result
        raise Blocked('Pagination limit exceeded')

    def graphql(self, query, **variables):
        response = self.api('graphql', 'POST', {'query': query, 'variables': variables})
        require(not response.get('errors'), 'GraphQL errors')
        return response['data']


def metadata(body):
    blocks = re.findall(r'<!-- clh-lifecycle\s*(\{.*?\})\s*-->', body or '', re.S)
    require(len(blocks) == 1, 'Exactly one lifecycle evidence block required')
    try:
        data = json.loads(blocks[0])
    except ValueError as error:
        raise Blocked('Invalid lifecycle JSON') from error
    require(type(data.get('issue')) is int and data['issue'] > 0, 'Invalid Issue')
    for key in ('head', 'base'):
        require(bool(SHA.fullmatch(data.get(key, ''))), f'Invalid {key} SHA')
    require(data.get('builder') in ('Codex', 'Claude Code'), 'One accountable Builder required')
    for key in ('scope_verified', 'self_review', 'complete'):
        require(data.get(key) is True, f'{key} not complete')
    require(bool(re.fullmatch(r'[0-9a-f]{64}', data.get('issue_body_sha256', ''))), 'Issue body digest required')
    require(type(data.get('deployment')) is bool, 'Explicit deployment applicability required')
    require(isinstance(data.get('evidence'), str) and len(data['evidence'].strip()) > 20,
            'Traceable evidence required')
    # All GitHub automatic-closing forms, including URL/cross-repo references, are excluded.
    require(not re.search(r'\b(?:close[sd]?|fix(?:es|ed)?|resolve[sd]?)\s+(?:#|https://|[\w.-]+/)', body, re.I),
            'Auto-closing keywords would bypass archive/closure ordering')
    return data


def protection(gh):
    """Require native enforcement; never activate based on a markdown assertion."""
    rules = gh.get('rules/branches/main')
    types = {rule['type']: rule for rule in rules}
    if {'pull_request', 'required_status_checks', 'non_fast_forward', 'deletion'} <= types.keys():
        for rule_id in {r['ruleset_id'] for r in rules if 'ruleset_id' in r}:
            configured = gh.get(f'rulesets/{rule_id}')
            require('bypass_actors' in configured and not configured['bypass_actors'], 'Ruleset bypass state unavailable or configured')
        params = types['required_status_checks']['parameters']
        checks = {row['context'] for row in params['required_status_checks']}
        require(REQUIRED <= checks and params.get('strict_required_status_checks_policy'), 'Strict native checks required')
        require(types['pull_request']['parameters'].get('required_review_thread_resolution'), 'Resolved threads required')
        return
    # A 404 is a blocker, not permission to proceed.
    p = gh.get('branches/main/protection')
    checks = p.get('required_status_checks') or {}
    names = set(checks.get('contexts', [])) | {c['context'] for c in checks.get('checks', [])}
    require(REQUIRED <= names and checks.get('strict'), 'Strict native required CI missing')
    require(p.get('required_pull_request_reviews') is not None, 'PR protection missing')
    require(p.get('enforce_admins', {}).get('enabled') is True, 'Admin enforcement missing')
    require(p.get('required_conversation_resolution', {}).get('enabled') is True, 'Thread resolution missing')
    require(not p.get('allow_force_pushes', {}).get('enabled') and not p.get('allow_deletions', {}).get('enabled'),
            'Force/delete protection missing')


def successful_checks(gh, head):
    checks = []
    for page in range(1, 101):
        response = gh.get(f'commits/{head}/check-runs?filter=latest&per_page=100&page={page}')
        rows = response['check_runs']
        checks.extend(rows)
        if len(rows) < 100:
            break
    else:
        raise Blocked('Check pagination limit')
    require(REQUIRED <= {c['name'] for c in checks}, 'Required CI missing')
    require(all(c['status'] == 'completed' and c['conclusion'] == 'success' for c in checks),
            'CI failed, pending, skipped or cancelled')
    statuses = gh.pages(f'commits/{head}/statuses')
    latest = {}
    for status in statuses:
        latest.setdefault(status['context'], status)
    require(all(s['state'] == 'success' for s in latest.values()), 'Commit status not successful')


def threads_clear(gh, number):
    owner, repo = gh.repo.split('/')
    cursor = None
    while True:
        data = gh.graphql('''query($owner:String!,$repo:String!,$number:Int!,$cursor:String){
          repository(owner:$owner,name:$repo){pullRequest(number:$number){
            reviewThreads(first:100,after:$cursor){nodes{isResolved} pageInfo{hasNextPage endCursor}}
          }}}''', owner=owner, repo=repo, number=number, cursor=cursor)
        threads = data['repository']['pullRequest']['reviewThreads']
        require(all(t['isResolved'] for t in threads['nodes']), 'Unresolved review threads')
        if not threads['pageInfo']['hasNextPage']:
            break
        cursor = threads['pageInfo']['endCursor']
    latest = {}
    for review in gh.pages(f'pulls/{number}/reviews'):
        if review['state'] != 'COMMENTED':
            latest[review['user']['login']] = review['state']
    require('CHANGES_REQUESTED' not in latest.values(), 'Changes requested')


def needs_deployment(files):
    return any(p.startswith(('docs/', 'overrides/')) or p in ('mkdocs.yml', 'requirements.txt', '.github/workflows/pages.yml')
               for p in files)


def archive_close(gh, pr, m, deployment):
    issue = m['issue']
    marker = f'<!-- clh-archive:{pr["number"]}:{pr["merge_commit_sha"]} -->'
    record = marker + '\n' + json.dumps({
        'merge': {'status': 'PASS', 'sha': pr['merge_commit_sha'], 'pr': pr['html_url']},
        'deployment': deployment,
        'archive': 'PASS only after remote readback',
        'closure': 'PENDING until archive readback; final Issue state is authoritative',
        'reviewed_head': m['head'], 'reviewed_base': m['base'], 'builder': m['builder'],
        'evidence': m['evidence'], 'workflow': os.environ.get('CLH_RUN_URL', 'local execution')}, sort_keys=True)
    prior = [c for c in gh.pages(f'issues/{issue}/comments') if c['body'].startswith(marker)]
    if prior:
        # A duplicate marker alone cannot fabricate deployment evidence.
        existing = prior[-1]
        old_data = json.loads(existing['body'][len(marker)+1:])
        new_data = json.loads(record[len(marker)+1:])
        old_data.pop('workflow', None); new_data.pop('workflow', None)
        require(old_data == new_data, 'Archive differs; inspect existing evidence before retry')
        record = existing['body']
        comment = existing
    else:
        comment = gh.get(f'issues/{issue}/comments', method='POST', data={'body': record})
    readback = gh.get(f'issues/comments/{comment["id"]}')
    require(readback['body'] == record, 'Archive remote readback mismatch')
    gh.get(f'issues/{issue}', method='PATCH', data={'state': 'closed', 'state_reason': 'completed'})
    require(gh.get(f'issues/{issue}')['state'] == 'closed', 'Closure readback failed')


def process(gh, number):
    pr = gh.get(f'pulls/{number}')
    m = metadata(pr['body'])
    require(pr['base']['ref'] == 'main' and pr['head']['repo']['full_name'] == gh.repo, 'Unsupported PR source/base')
    require(pr['head']['sha'] == m['head'], 'Stale reviewed head')
    issue = gh.get(f'issues/{m["issue"]}')
    require(hashlib.sha256(issue['body'].encode()).hexdigest() == m['issue_body_sha256'], 'Issue requirements changed')
    require('pull_request' not in issue and issue['user']['login'] == gh.repo.split('/')[0], 'Not an owner engineering Issue')
    require('### WHAT' in issue['body'] or '## WHAT' in issue['body'], 'Engineering WHAT required')
    files = [name for f in gh.pages(f'pulls/{number}/files')
             for name in (f['filename'], f.get('previous_filename', ''))]
    commits = gh.pages(f'pulls/{number}/commits')
    require(not any(re.search(r'\b(?:close[sd]?|fix(?:es|ed)?|resolve[sd]?)\s+(?:#|https://|[\w.-]+/)',
                              c['commit']['message'], re.I) for c in commits),
            'Commit message would prematurely close an Issue')
    require(m['deployment'] or not needs_deployment(files), 'Site changes require deployment')
    if not pr['merged']:
        require(issue['state'] == 'open' and pr['state'] == 'open', 'Issue/PR not open')
        protection(gh)
        base = gh.get('git/ref/heads/main')['object']['sha']
        require(m['base'] == base, 'Stale reviewed base')
        require(pr['mergeable'] is True, 'Mergeability unknown or conflict')
        successful_checks(gh, m['head'])
        threads_clear(gh, number)
        current = gh.get(f'pulls/{number}')
        require(current['head']['sha'] == m['head'] and current['body'] == pr['body'], 'PR changed during validation')
        require(gh.get('git/ref/heads/main')['object']['sha'] == base, 'Base changed during validation')
        if current['draft']:
            gh.graphql('''mutation($id:ID!){markPullRequestReadyForReview(input:{pullRequestId:$id}){pullRequest{isDraft}}}''', id=pr['node_id'])
        require(not gh.get(f'pulls/{number}')['draft'], 'Still Draft')
        merged = gh.get(f'pulls/{number}/merge', method='PUT', data={'sha': m['head'], 'merge_method': 'merge'})
        require(merged.get('merged') is True, 'GitHub refused merge')
        pr = gh.get(f'pulls/{number}')
    require(pr['merged'] is True and bool(SHA.fullmatch(pr['merge_commit_sha'])), 'Merge readback invalid')
    if m['deployment']:
        # Deployment job records a marker only after remote SHA readback. Verify run independently.
        prefix = f'<!-- clh-deployed:{pr["merge_commit_sha"]} -->\n'
        entries = [c for c in gh.pages(f'issues/{m["issue"]}/comments') if c['body'].startswith(prefix)]
        require(bool(entries), 'Deployment verification PENDING')
        d = json.loads(entries[-1]['body'][len(prefix):])
        require(d['url'] == gh.get('pages')['html_url'], 'Deployment URL differs from configured Pages')
        run = gh.get(f'actions/runs/{int(d["run_id"])}')
        require(run['head_sha'] == pr['merge_commit_sha'] and run['conclusion'] == 'success'
                and run['path'] == '.github/workflows/pages.yml' and run['head_branch'] == 'main', 'Deployment workflow not successful for merge SHA')
        deployment = {'status': 'PASS', 'sha': run['head_sha'], 'workflow': run['html_url'], 'url': d['url']}
    else:
        deployment = {'status': 'NOT RUN', 'reason': 'Not applicable to this task'}
    archive_close(gh, pr, m, deployment)


def deployment_verified(gh, sha, run_id):
    require(bool(SHA.fullmatch(sha)), 'Invalid deployment SHA')
    page = gh.get('pages')
    url = page['html_url'].rstrip('/') + '/deployment-sha.txt'
    require(url.startswith('https://'), 'HTTPS Pages URL required')
    with urllib.request.urlopen(url + '?sha=' + sha, timeout=30) as response:
        actual = response.read(128).decode().strip()
    require(actual == sha, 'Remote deployment SHA mismatch')
    for pr in gh.pages(f'commits/{sha}/pulls'):
        if not pr['merged_at'] or pr['merge_commit_sha'] != sha:
            continue
        m = metadata(pr['body'])
        if not m['deployment']:
            continue
        body = f'<!-- clh-deployed:{sha} -->\n' + json.dumps({'run_id': str(run_id), 'url': page['html_url']}, sort_keys=True)
        prior = gh.pages(f'issues/{m["issue"]}/comments')
        if not any(c['body'] == body for c in prior):
            gh.get(f'issues/{m["issue"]}/comments', method='POST', data={'body': body})


def reconcile(gh):
    # Includes merged-but-not-closed work. Avoid unrelated historical PRs.
    failures = []
    for pr in gh.pages('pulls?state=all&sort=updated&direction=desc'):
        if '<!-- clh-lifecycle' not in (pr['body'] or ''):
            continue
        try:
            m = metadata(pr['body'])
            if gh.get(f'issues/{m["issue"]}')['state'] == 'closed':
                continue
            process(gh, pr['number'])
        except (Blocked, KeyError, ValueError) as error:
            message = f'BLOCKED PR #{pr["number"]}: {error}'
            print(message)
            failures.append(message)
            # No secrets/raw API output. Deduplicate identical blocker records.
            body = '<!-- clh-blocker -->\n' + message
            comments = gh.pages(f'issues/{pr["number"]}/comments')
            if not any(c['body'] == body for c in comments):
                gh.get(f'issues/{pr["number"]}/comments', method='POST', data={'body': body})
    require(not failures, 'One or more lifecycle operations blocked; see PR evidence')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['reconcile', 'deployment', 'preflight'])
    parser.add_argument('--sha'); parser.add_argument('--run-id')
    args = parser.parse_args()
    github = GitHub(os.environ['GITHUB_REPOSITORY'])
    try:
        if args.command == 'deployment':
            deployment_verified(github, args.sha, args.run_id)
        elif args.command == 'preflight':
            protection(github)
        else:
            reconcile(github)
    except (Blocked, KeyError, ValueError) as error:
        raise SystemExit(f'BLOCKED: {error}')
