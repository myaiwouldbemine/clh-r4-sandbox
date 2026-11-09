"""Base-trusted Content Stop-Ship Gate (Issue #56 B2 proposal).

Runs from the BASE commit under pull_request_target. The PR head is a data-only checkout:
nothing from it is imported or executed. Standard library only. No token is required.

Mechanical checks (Human semantics are bound by exact SHA-256, never inferred):
  G1 governance-sensitive paths changed -> FAIL unless one base `governance_changes` entry binds
     exactly the changed governance paths: {path: sha256 | "DELETE"} (policy file: "policy-keys:<sha256>")
  G2 each changed guarded lesson file needs a base approval entry with the same SHA-256
  G3 approval rights must be APPROVED
  G4 DRAFT approvals are valid only under DRAFT prefixes; Final paths need scope FINAL
  G5 the approval must bind the exact LINK_REVIEW.json SHA-256 present in the head, and that
     record must list the lesson as changed
  G6 deleting a guarded lesson needs an approval entry with sha256 "DELETE"
  G7 guarded paths must be regular files (no symlinks or submodules)
  G8 an approval-record-only change may edit only `approvals` and `governance_changes`;
     gate policy keys (guarded/draft prefixes, schema) need a content-bound governance approval
Every file type under a guarded prefix is guarded (not only .md). Paths are parsed with -z so
quoted/non-ASCII names cannot escape prefix matching.
"""
import hashlib, json, subprocess, sys
from pathlib import Path

POLICY = 'content_review/approvals.json'
# Everything that can change the GitHub Pages output or the gate itself (R1 / O8 extension):
# workflows, policy, MkDocs config, dependency pins, and every script the Pages workflow or a
# generator runs. Any .py/.pth file is also sensitive because `python -m mkdocs` puts the repo
# root on sys.path, so a root-level module could shadow a build dependency.
GOVERNANCE = ('.github/', 'content_review/', 'scripts/', 'mkdocs.yml', 'requirements.txt')
GOVERNANCE_SUFFIXES = ('.py', '.pth')
# Floor that a policy file can never lower (defence in depth on top of G8).
MIN_GUARDED = ('docs/',)


def is_governance(name):
    return name.startswith(GOVERNANCE) or name.endswith(GOVERNANCE_SUFFIXES)


def git(repo, *args):
    return subprocess.run(['git', '-C', str(repo), '-c', 'core.hooksPath=/dev/null', *args],
                          check=True, capture_output=True).stdout.decode()


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


RECORD_KEYS = ('approvals', 'governance_changes', 'note')


def policy_keys(d):
    return {k: v for k, v in d.items() if k not in RECORD_KEYS}


def governance_digest(head, name, status):
    """Content identity of one changed governance path, stable across merges of main.

    The policy file is identified by its gate keys only, so later approval records added to
    main do not invalidate an approval (strict up-to-date rulesets would otherwise deadlock)."""
    if status == 'D':
        return 'DELETE'
    path = head / name
    if path.is_symlink() or not path.is_file():
        return 'NOT_REGULAR_FILE'
    if name == POLICY:
        try:
            data = json.loads(path.read_text())
        except ValueError:
            return 'INVALID_POLICY'
        return 'policy-keys:' + hashlib.sha256(
            json.dumps(policy_keys(data), sort_keys=True, ensure_ascii=False).encode()).hexdigest()
    return sha(path)


def governance_approved(policy, head, changes):
    """G1: one governance_changes entry must bind every changed governance path, exactly."""
    wanted = {n: governance_digest(head, n, st) for st, n, _ in changes if is_governance(n)}
    for entry in policy.get('governance_changes', []):
        files = entry.get('files')
        if isinstance(files, dict) and files == wanted:
            return True
    return False


def policy_only_records_changed(policy, head):
    """G8: the head policy must keep every gate key of the base policy unchanged."""
    try:
        new = json.loads((head / POLICY).read_text())
    except (OSError, ValueError):
        return False
    return isinstance(new, dict) and policy_keys(new) == policy_keys(policy)


def main(base, head, base_sha, head_sha):
    base, head = Path(base), Path(head)
    policy = json.loads((base / POLICY).read_text())
    guarded = tuple(policy['guarded_prefixes']) + MIN_GUARDED
    draft_prefixes = policy['draft_prefixes']
    approvals = {a['path']: a for a in policy.get('approvals', [])}
    fields = git(head, 'diff', '--raw', '-z', '--no-renames', '--no-abbrev',
                 f'{base_sha}...{head_sha}').split('\0')
    changes = []  # (status, path, new_mode)
    for meta, name in zip(fields[0::2], fields[1::2]):
        parts = meta.lstrip(':').split()
        changes.append((parts[4][0], name, parts[1]))
    errors, notes = [], []
    names = [n for _, n, _ in changes]
    if any(is_governance(n) for n in names):
        if names == [POLICY] and policy_only_records_changed(policy, head):
            notes.append('approval-record-only change: no lesson or gate change in this PR')
        elif governance_approved(policy, head, changes):
            notes.append('governance-sensitive change bound by exact content in base approval file')
        else:
            errors.append('G1 governance-sensitive path changed without a content-bound governance approval (G8 if policy keys): '
                          + ', '.join(n for n in names if is_governance(n)))
    for status, name, mode in changes:
        if not name.startswith(guarded):
            continue
        if status != 'D' and mode != '100644' and mode != '100755':
            errors.append(f'G7 guarded path is not a regular file (mode {mode}): {name}'); continue
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
        if not name.endswith('.md'):
            continue  # assets/CSS/HTML: exact SHA + rights + scope; LINK_REVIEW binds pages only
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
