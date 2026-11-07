import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from verify_plan_records import verify, FIELDS, RESULT_FIELDS, plan_fields_present

class RecordTests(unittest.TestCase):
    def setUp(self):
        self.old = os.getcwd()
        self.tmp = tempfile.TemporaryDirectory()
        os.chdir(self.tmp.name)
        self.git("init", "-q")
        self.git("config", "user.email", "test@example.invalid")
        self.git("config", "user.name", "test")
        self.write("README.md", "base")
        self.commit()
        self.base = self.git("rev-parse", "HEAD")
    def tearDown(self):
        os.chdir(self.old)
        self.tmp.cleanup()
    def git(self, *args):
        return subprocess.check_output(["git", *args], text=True).strip()
    def write(self, name, text):
        p = Path(name); p.parent.mkdir(parents=True, exist_ok=True); p.write_text(text)
    def commit(self):
        self.git("add", "."); self.git("commit", "-qm", "test")
    def plan(self):
        self.write("records/ISSUE-4/PLAN.md", "\n".join(FIELDS) + " /issues/4")
    def result(self):
        self.write("records/ISSUE-4/RESULT.md", "\n".join(RESULT_FIELDS) + " /pull/5")
    def test_no_plan(self):
        self.assertIn("NOT REQUIRED", verify(self.base, "HEAD", 4))
    def test_required_missing_plan(self):
        with self.assertRaises(AssertionError): verify(self.base, "HEAD", 4, formal_plan=True)
    def test_invalid_issue(self):
        with self.assertRaises(ValueError): verify(self.base, "HEAD", -1)
    def test_revision_acceptance_heading_alias(self):
        body="\n".join(FIELDS).replace("acceptance criteria", "e2e acceptance")
        self.assertTrue(plan_fields_present(body, True))
        self.assertFalse(plan_fields_present(body, False))
        self.assertFalse(plan_fields_present(body.replace("e2e acceptance", ""), True))
    def test_named_revision_order(self):
        self.write("records/ISSUE-4/ON-DEMAND-REVISION-PLAN.md", "\n".join(FIELDS) + " /issues/4")
        self.commit()
        self.write("app.py", "print(1)"); self.commit()
        self.write("records/ISSUE-4/ON-DEMAND-REVISION-RESULT.md", "\n".join(RESULT_FIELDS) + " /pull/5")
        self.commit()
        self.assertIn("PASS", verify(self.base, "HEAD", 4, True, "ON-DEMAND-REVISION-"))
    def test_named_revision_backfill_rejected(self):
        self.write("app.py", "print(1)"); self.commit()
        self.write("records/ISSUE-4/ON-DEMAND-REVISION-PLAN.md", "\n".join(FIELDS) + " /issues/4")
        self.write("records/ISSUE-4/ON-DEMAND-REVISION-RESULT.md", "\n".join(RESULT_FIELDS) + " /pull/5")
        self.commit()
        with self.assertRaises(AssertionError): verify(self.base, "HEAD", 4, True, "ON-DEMAND-REVISION-")
    def test_valid_order(self):
        self.plan(); self.commit()
        self.write("app.py", "print(1)"); self.result(); self.commit()
        self.assertIn("PASS", verify(self.base, "HEAD", 4, formal_plan=True))
    def test_same_commit_plan_rejected(self):
        self.plan(); self.result(); self.write("app.py", "print(1)"); self.commit()
        with self.assertRaises(AssertionError): verify(self.base, "HEAD", 4, formal_plan=True)
    def test_backfill_rejected(self):
        self.write("app.py", "print(1)"); self.commit()
        self.plan(); self.result(); self.commit()
        with self.assertRaises(AssertionError): verify(self.base, "HEAD", 4, formal_plan=True)
    def test_formal_plan_requires_result(self):
        self.plan(); self.commit()
        with self.assertRaises(AssertionError): verify(self.base, "HEAD", 4)
    def test_initial_incomplete_plan_rejected(self):
        self.write("records/ISSUE-4/PLAN.md", "placeholder"); self.commit()
        self.plan(); self.result(); self.write("app.py", "print(1)"); self.commit()
        with self.assertRaises(AssertionError): verify(self.base, "HEAD", 4, formal_plan=True)

if __name__ == "__main__": unittest.main()
