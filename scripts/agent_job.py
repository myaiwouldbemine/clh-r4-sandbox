"""Prepare an owner engineering Issue; publish commits without executing candidate code."""
import hashlib
import json
import os
import subprocess
from pathlib import Path
from autonomous_lifecycle import GitHub, Blocked, require


def git(*args):
    return subprocess.check_output(['git', *args], text=True).strip()


def prepare(gh, event):
    issue = event.get('issue')
    if issue is None:
        run = event['workflow_run']
        require(run['conclusion'] == 'failure', 'Not a CI failure')
        prs = gh.pages(f'commits/{run["head_sha"]}/pulls')
        prs = [p for p in prs if p['state'] == 'open' and p['head']['ref'].startswith('codex/issue-')]
        require(len(prs) == 1, 'No unique Agent PR for retry')
        branch = prs[0]['head']['ref']
        suffix = branch.removeprefix('codex/issue-')
        require(suffix.isdigit(), 'Invalid issue branch')
        issue = gh.get(f'issues/{int(suffix)}')
    require('pull_request' not in issue and issue['state'] == 'open', 'Not an open Issue')
    require(issue['user']['login'] == gh.repo.split('/')[0], 'Only owner-created Issues start engineering')
    require('### WHAT' in issue['body'] or '## WHAT' in issue['body'], 'Not an engineering task')
    # Read current Issue, never a stale event payload.
    issue = gh.get(f'issues/{issue["number"]}')
    branch = f'codex/issue-{issue["number"]}'
    refs = gh.pages('branches')
    if any(r['name'] == branch for r in refs):
        subprocess.run(['git', 'fetch', 'origin', branch], check=True)
        subprocess.run(['git', 'switch', '-C', branch, 'FETCH_HEAD'], check=True)
    else:
        subprocess.run(['git', 'switch', '-c', branch], check=True)
    attempts = git('log', '--format=%s', '--grep=^CLH agent attempt ').splitlines()
    require(len(attempts) < 3, 'Automatic retry budget exhausted (3 attempts)')
    prs = gh.pages(f'pulls?state=all&head={gh.repo.split("/")[0]}:{branch}')
    require(not any(p['merged_at'] or p['state'] == 'closed' for p in prs), 'Branch already completed or stopped')
    feedback = {'prs': prs, 'issue_comments': gh.pages(f'issues/{issue["number"]}/comments')}
    if prs:
        feedback['pr_comments'] = gh.pages(f'issues/{prs[0]["number"]}/comments')
        feedback['checks'] = gh.get(f'commits/{prs[0]["head"]["sha"]}/check-runs')
    Path('issue.json').write_text(json.dumps(issue, ensure_ascii=False))
    Path('feedback.json').write_text(json.dumps(feedback, ensure_ascii=False))
    with open('.git/info/exclude', 'a') as f:
        f.write('\nissue.json\nfeedback.json\npr-body.md\ncandidate.bundle\nagent-output.md\n')
    subprocess.run(['git', 'config', 'user.name', 'CLH Codex Builder'], check=True)
    subprocess.run(['git', 'config', 'user.email', 'codex-builder@users.noreply.github.com'], check=True)
    subprocess.run(['git', 'commit', '--allow-empty', '-m', f'CLH agent attempt {len(attempts)+1} for Issue {issue["number"]}'], check=True)
    with open(os.environ['GITHUB_OUTPUT'], 'a') as out:
        out.write(f'branch={branch}\nissue={issue["number"]}\n')


def publish(gh, number):
    issue = gh.get(f'issues/{number}')
    require(issue['state'] == 'open' and issue['user']['login'] == gh.repo.split('/')[0], 'Issue stopped or invalid')
    branch = f'codex/issue-{number}'
    subprocess.run(['git', 'bundle', 'verify', 'candidate/candidate.bundle'], check=True)
    subprocess.run(['git', 'fetch', 'candidate/candidate.bundle', f'{branch}:refs/heads/{branch}'], check=True)
    # Use trusted main scripts only; never checkout or execute the candidate tree here.
    body = Path('candidate/pr-body.md').read_text()
    require(len(body) < 60000 and f'#{number}' in body, 'Invalid PR body')
    # Prevent native auto-close even for a blocked Agent report.
    import re
    require(not re.search(r'\b(?:close[sd]?|fix(?:es|ed)?|resolve[sd]?)\s+(?:#|https://|[\w.-]+/)', body, re.I), 'Premature closure keyword')
    require(subprocess.run(['git', 'merge-base', '--is-ancestor', 'origin/main', branch]).returncode == 0,
            'Candidate must include current main; retry/reconcile base first')
    subprocess.run(['git', 'push', 'origin', f'{branch}:{branch}'], check=True)  # Never force.
    prs = gh.pages(f'pulls?state=all&head={gh.repo.split("/")[0]}:{branch}')
    require(len(prs) <= 1, 'Ambiguous existing PR')
    if prs:
        require(prs[0]['state'] == 'open' and not prs[0]['merged_at'], 'Existing PR stopped/completed')
        gh.get(f'pulls/{prs[0]["number"]}', method='PATCH', data={'body': body})
    else:
        gh.get('pulls', method='POST', data={'title': f'Issue #{number}: engineering implementation',
               'head': branch, 'base': 'main', 'draft': True, 'body': body})

if __name__ == '__main__':
    import sys
    gh = GitHub(os.environ['GITHUB_REPOSITORY'])
    try:
        if sys.argv[1] == 'prepare':
            prepare(gh, json.loads(Path(os.environ['GITHUB_EVENT_PATH']).read_text()))
        else:
            publish(gh, int(sys.argv[2]))
    except Blocked as error:
        raise SystemExit(f'BLOCKED: {error}')
