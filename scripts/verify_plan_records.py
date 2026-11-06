"""Read-only Git record verifier. Local assistance only; caller decides whether a formal Plan is needed.
Usage: python scripts/verify_plan_records.py BASE HEAD ISSUE [--formal-plan]
This is a local verifier, not a production authorization/merge service.
"""
import argparse
import subprocess
from pathlib import PurePosixPath

FIELDS = ("goal", "why", "scope", "boundary", "implementation plan",
          "acceptance criteria", "verification strategy", "revision history")
RESULT_FIELDS = ("results", "evidence", "pr", "commit", "deviations", "unfinished")

def git(*args):
    return subprocess.check_output(["git", *args], text=True).strip()

def verify(base, head, issue, formal_plan=False, record_prefix=""):
    if type(issue) is not int or issue <= 0:
        raise ValueError("invalid issue")
    # Validate revisions as commit objects before using them in Git expressions.
    base = git("rev-parse", "--verify", base + "^{commit}")
    head = git("rev-parse", "--verify", head + "^{commit}")
    git("merge-base", "--is-ancestor", base, head)
    if record_prefix and (not record_prefix.endswith("-") or not all(c.isupper() or c.isdigit() or c == "-" for c in record_prefix)):
        raise ValueError("invalid record prefix")
    prefix = f"records/ISSUE-{issue}/"
    plan, result = prefix + record_prefix + "PLAN.md", prefix + record_prefix + "RESULT.md"
    files = git("ls-tree", "-r", "--name-only", head).splitlines()
    required = formal_plan or plan in files
    if not required:
        return "NOT REQUIRED: no formal plan"
    assert plan in files and result in files, "Plan and Result are required"
    body = git("show", f"{head}:{plan}").lower()
    assert all(field in body for field in FIELDS), "Missing Plan fields"
    assert f"/issues/{issue}" in body, "Plan must link the Issue"
    output = git("show", f"{head}:{result}").lower()
    assert all(field in output for field in RESULT_FIELDS), "Missing Result fields"
    assert "/pull/" in output, "Result must link the PR"
    introduced = plan in git("ls-tree", "-r", "--name-only", base).splitlines()
    prior_plan = introduced
    # First-parent history prevents a late merge of a backfilled side-branch Plan
    # from making it appear to precede implementation.
    for commit in git("rev-list", "--first-parent", "--reverse", f"{base}..{head}").splitlines():
        changed = git("diff-tree", "--root", "--no-commit-id", "--name-only", "-r", "-m", commit).splitlines()
        implementation = any(not PurePosixPath(p).is_relative_to("records") for p in changed)
        assert prior_plan or not implementation, "Implementation precedes Plan commit"
        if not prior_plan and plan in changed:
            initial = git("show", f"{commit}:{plan}").lower()
            assert all(field in initial for field in FIELDS), "Initial Plan was incomplete"
            assert f"/issues/{issue}" in initial, "Initial Plan lacked Issue link"
            prior_plan = True
    assert prior_plan, "No traceable Plan commit"
    return "PASS: record structure and Git order only; not semantic approval or closure"

if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("base"); p.add_argument("head")
    p.add_argument("issue", type=int)
    p.add_argument("--formal-plan", action="store_true")
    p.add_argument("--record-prefix", default="")
    a = p.parse_args()
    print(verify(a.base, a.head, a.issue, a.formal_plan, a.record_prefix))
