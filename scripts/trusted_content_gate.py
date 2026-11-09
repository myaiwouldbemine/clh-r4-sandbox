"""Base-trusted Content Stop-Ship Gate (Issue #56 B2 proposal).

Runs from the BASE commit under pull_request_target. The PR head is a data-only checkout:
nothing from it is imported or executed. Standard library only. No token is required.

Mechanical checks (Human semantics are bound by exact SHA-256, never inferred):
  G1 governance-sensitive paths changed -> FAIL unless the base approval file lists this head SHA
  G2 each changed guarded lesson file needs a base approval entry with the same SHA-256
  G3 approval rights must be APPROVED
  G4 DRAFT approvals are valid only under DRAFT prefixes; Final paths need scope FINAL
  G5 the approval must bind the exact LINK_REVIEW.json SHA-256 present in the head, and that
     record must list the lesson as changed
  G6 deleting a guarded lesson needs an approval entry with sha256 "DELETE"
"""
import hashlib, json, subprocess, sys
from pathlib import Path

POLICY = 'content_review/approvals.json'
GOVERNANCE = ('.github/', 'content_review/', 'scripts/trusted_content_gate.py',
              'scripts/validate_subject_links.py', 'scripts/validate_os_release.py', 'requirements.txt')


def git(repo, *args):
    return subprocess.run(['git', '-C', str(repo), '-c', 'core.hooksPath=/dev/null', *args],
                          check=True, capture_output=True).stdout.decode()


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main(base, head, base_sha, head_sha):
    base, head = Path(base), Path(head)
    policy = json.loads((base / POLICY).read_text())
    guarded, draft_prefixes = policy['guarded_prefixes'], policy['draft_prefixes']
    approvals = {a['path']: a for a in policy.get('approvals', [])}
    gov_ok = {g.get('head_sha') for g in policy.get('governance_changes', [])}
    rows = git(head, 'diff', '--name-status', '--no-renames', f'{base_sha}...{head_sha}').splitlines()
    changes = [(r.split('\t')[0], r.split('\t')[-1]) for r in rows if r]
    errors, notes = [], []
    names = [n for _, n in changes]
    if any(n.startswith(GOVERNANCE) for n in names):
        if names == [POLICY]:
            notes.append('approval-record-only change: no lesson or gate change in this PR')
        elif head_sha in gov_ok:
            notes.append('governance-sensitive change listed by head SHA in base approval file')
        else:
            errors.append('G1 governance-sensitive path changed without a head-SHA governance approval: '
                          + ', '.join(n for n in names if n.startswith(GOVERNANCE)))
    for status, name in changes:
        if not (name.startswith(tuple(guarded)) and name.endswith('.md')):
            continue
        entry = approvals.get(name)
        if entry is None:
            errors.append(f'G2 no Human approval for {name}'); continue
        if status == 'D':
            if entry.get('sha256') != 'DELETE':
                errors.append(f'G6 deletion not approved: {name}')
            continue
        actual = sha(head / name)
        if entry.get('sha256') != actual:
            errors.append(f'G2 SHA-256 mismatch for {name}: head {actual}, approved {entry.get("sha256")}')
        if entry.get('rights') != 'APPROVED':
            errors.append(f'G3 publication rights not APPROVED for {name}: {entry.get("rights")}')
        scope = entry.get('scope')
        is_draft_path = name.startswith(tuple(draft_prefixes))
        if scope not in ('DRAFT', 'FINAL') or (scope == 'DRAFT' and not is_draft_path):
            errors.append(f'G4 scope {scope} not valid for {name}')
        link = entry.get('link_review') or {}
        lr = head / link.get('path', '\0missing')
        if not link.get('path') or not lr.is_file() or lr.is_symlink():
            errors.append(f'G5 bound LINK_REVIEW missing for {name}')
        elif sha(lr) != link.get('sha256'):
            errors.append(f'G5 LINK_REVIEW SHA-256 mismatch for {name}')
        else:
            try:
                if name not in json.loads(lr.read_text()).get('changed', []):
                    errors.append(f'G5 LINK_REVIEW does not cover {name}')
            except ValueError:
                errors.append(f'G5 LINK_REVIEW unreadable for {name}')
    print(json.dumps({'gate': 'FAIL' if errors else 'PASS', 'base_sha': base_sha, 'head_sha': head_sha,
                      'errors': errors, 'notes': notes,
                      'claim': 'Mechanical binding only; not a semantic, learning or identity certification'},
                     ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == '__main__':
    sys.exit(main(*sys.argv[1:5]))
# weakened
