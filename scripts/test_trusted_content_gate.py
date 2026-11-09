"""Unit tests for the base-trusted content gate (Issue #56 B2). Fixtures only; no lesson content."""
import contextlib
import hashlib
import io
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

import trusted_content_gate as gate

LESSON = 'docs/preview/fixture/index.md'
LINK = 'records/ISSUE-0/LINK_REVIEW.json'


def git(repo, *args):
    return subprocess.run(['git', '-C', str(repo), *args], check=True, capture_output=True, text=True).stdout.strip()


def sha(data):
    return hashlib.sha256(data.encode()).hexdigest()


class GateTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        self.repo, self.base = root / 'repo', root / 'base'
        self.repo.mkdir()
        git(self.repo, 'init', '-q')
        git(self.repo, 'config', 'user.email', 't@example.invalid')
        git(self.repo, 'config', 'user.name', 'test')
        (self.repo / 'content_review').mkdir()
        self.policy = {'schema_version': 1, 'guarded_prefixes': ['docs/'],
                       'draft_prefixes': ['docs/preview/'], 'approvals': [], 'governance_changes': []}
        self.write('content_review/approvals.json', json.dumps(self.policy))
        self.write('README.md', 'base\n')
        self.commit('base')
        self.base_sha = git(self.repo, 'rev-parse', 'HEAD')
        git(self.repo, 'worktree', 'add', '-q', str(self.base), self.base_sha)

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, name, text, root=None):
        path = (root or self.repo) / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)

    def commit(self, message):
        git(self.repo, 'add', '-A')
        git(self.repo, 'commit', '-qm', message)

    def approve(self, **entry):
        row = {'path': LESSON, 'sha256': sha('lesson\n'), 'scope': 'DRAFT', 'rights': 'APPROVED',
               'link_review': {'path': LINK, 'sha256': sha(self.link_text)}}
        row.update(entry)
        self.policy['approvals'] = [row]
        self.write('content_review/approvals.json', json.dumps(self.policy), root=self.base)

    def lesson_pr(self, path=LESSON):
        self.link_text = json.dumps({'changed': [path]})
        self.write(path, 'lesson\n')
        self.write(LINK, self.link_text)
        self.commit('lesson')

    def run_gate(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = gate.main(self.base, self.repo, self.base_sha, git(self.repo, 'rev-parse', 'HEAD'))
        return code, json.loads(out.getvalue())

    def assertFails(self, prefix):
        code, report = self.run_gate()
        self.assertEqual(code, 1)
        self.assertTrue(any(e.startswith(prefix) for e in report['errors']), report['errors'])

    def test_missing_approval_blocks(self):
        self.lesson_pr()
        self.assertFails('G2 no Human approval')

    def test_sha_mismatch_blocks(self):
        self.lesson_pr()
        self.approve(sha256='0' * 64)
        self.assertFails('G2 SHA-256 mismatch')

    def test_rights_pending_blocks(self):
        self.lesson_pr()
        self.approve(rights='PENDING')
        self.assertFails('G3')

    def test_draft_scope_on_final_path_blocks(self):
        path = 'docs/subjects/operating-systems/x/index.md'
        self.lesson_pr(path)
        self.approve(path=path)
        self.assertFails('G4')

    def test_link_review_mismatch_blocks(self):
        self.lesson_pr()
        self.approve(link_review={'path': LINK, 'sha256': '0' * 64})
        self.assertFails('G5 LINK_REVIEW SHA-256 mismatch')

    def test_link_review_missing_blocks(self):
        self.lesson_pr()
        self.approve(link_review={'path': 'records/none.json', 'sha256': '0' * 64})
        self.assertFails('G5 bound LINK_REVIEW missing')

    def test_gate_or_workflow_edit_blocks(self):
        for name in ('.github/workflows/spoof.yml', 'scripts/trusted_content_gate.py',
                     'scripts/validate_subject_links.py'):
            with self.subTest(name=name):
                self.write(name, 'x\n')
                self.commit(name)
                self.assertFails('G1')

    def test_approved_exact_sha_passes(self):
        self.lesson_pr()
        self.approve()
        code, report = self.run_gate()
        self.assertEqual((code, report['errors']), (0, []))

    def test_approval_record_only_passes_with_note(self):
        self.policy['approvals'] = []
        self.write('content_review/approvals.json', json.dumps({**self.policy, 'note': 'x'}))
        self.commit('approval only')
        code, report = self.run_gate()
        self.assertEqual(code, 0)
        self.assertTrue(report['notes'])

    def test_non_ascii_path_is_guarded(self):
        self.lesson_pr('docs/preview/教材/index.md')
        self.assertFails('G2 no Human approval')

    def test_non_markdown_guarded_file_blocks(self):
        self.write('docs/subjects/x/slides.html', '<p>x</p>\n')
        self.commit('html')
        self.assertFails('G2 no Human approval')

    def test_symlink_in_guarded_path_blocks(self):
        self.write('unguarded.md', 'x\n')
        target = self.repo / 'docs/preview/link.md'
        target.parent.mkdir(parents=True, exist_ok=True)
        target.symlink_to('../../unguarded.md')
        self.commit('symlink')
        self.assertFails('G7')

    def test_approval_only_cannot_weaken_policy(self):
        self.write('content_review/approvals.json', json.dumps({**self.policy, 'guarded_prefixes': []}))
        self.commit('weaken')
        self.assertFails('G1')

    def test_approval_only_cannot_delete_policy(self):
        git(self.repo, 'rm', '-q', 'content_review/approvals.json')
        self.commit('delete policy')
        self.assertFails('G1')

    # --- R1: whole publication surface ---
    def unapproved_change(self, name, text='x\n'):
        self.write(name, text)
        self.commit(name)

    def test_r1_docs_index_blocks(self):
        self.unapproved_change('docs/index.md')
        self.assertFails('G2 no Human approval for docs/index.md')

    def test_r1_assets_image_and_html_block(self):
        for name in ('docs/assets/x.png', 'docs/assets/x.html', 'docs/stylesheets/x.css'):
            with self.subTest(name=name):
                self.unapproved_change(name)
                self.assertFails('G2 no Human approval')

    def test_r1_new_docs_page_blocks(self):
        self.unapproved_change('docs/other/page.md')
        self.assertFails('G2 no Human approval')

    def test_r1_policy_floor_cannot_be_lowered(self):
        # Even a base policy that lost docs/ keeps the hard-coded floor.
        self.policy['guarded_prefixes'] = []
        self.write('content_review/approvals.json', json.dumps(self.policy), root=self.base)
        self.unapproved_change('docs/index.md')
        self.assertFails('G2 no Human approval')

    def test_r1_build_inputs_are_governance(self):
        for name in ('mkdocs.yml', 'requirements.txt', 'scripts/build_preview_pages.py',
                     'scripts/validate_os_release.py', 'scripts/autonomous_lifecycle.py',
                     'markdown.py', 'material/__init__.py', 'x.pth', '.github/workflows/pages.yml'):
            with self.subTest(name=name):
                self.unapproved_change(name)
                self.assertFails('G1')

    def test_r1_approved_asset_passes_without_link_review(self):
        name = 'docs/assets/fig.svg'
        self.unapproved_change(name, '<svg/>\n')
        self.policy['approvals'] = [{'path': name, 'sha256': sha('<svg/>\n'), 'scope': 'FINAL',
                                     'rights': 'APPROVED'}]
        self.write('content_review/approvals.json', json.dumps(self.policy), root=self.base)
        code, report = self.run_gate()
        self.assertEqual((code, report['errors']), (0, []))

    def test_governance_change_needs_head_sha(self):
        self.unapproved_change('mkdocs.yml', 'site_name: x\n')
        self.assertFails('G1')
        self.policy['governance_changes'] = [{'head_sha': git(self.repo, 'rev-parse', 'HEAD')}]
        self.write('content_review/approvals.json', json.dumps(self.policy), root=self.base)
        code, report = self.run_gate()
        self.assertEqual((code, report['errors']), (0, []))

    def test_governance_approval_for_other_sha_blocks(self):
        self.policy['governance_changes'] = [{'head_sha': '0' * 40}]
        self.write('content_review/approvals.json', json.dumps(self.policy), root=self.base)
        self.unapproved_change('mkdocs.yml', 'site_name: x\n')
        self.assertFails('G1')

    def test_unapproved_deletion_blocks(self):
        self.lesson_pr()
        self.approve()
        git(self.repo, 'rm', '-q', LESSON)
        self.commit('delete')
        # The base never had the lesson, so a delete relative to base is a no-op: re-base on the lesson commit.
        self.base_sha = git(self.repo, 'rev-parse', 'HEAD~1')
        self.assertFails('G6')


if __name__ == '__main__':
    unittest.main()
