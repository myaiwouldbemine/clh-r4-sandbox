# Issue #11 — Formal Plan v2 Security & Consistency Revision

## Revision History
- v1: 2026-11-06 13:13 UTC+8 — Initial Plan Draft (526 lines)
- v2: 2026-11-06 13:35 UTC+8 — Security & Consistency Revision (F-01～F-06 corrections)
  - F-01: Trusted Human Authorization boundary clarification
  - F-02: Complete Merge Gates (10 → 12 checks, SHA compare-and-swap, stale evidence detection)
  - F-03: Safe Live Testing (Mock vs Live separation, Human testing authorization)
  - F-04: Closure & Recovery (5-state machine, idempotency, remote readback before retry)
  - F-05: Rollback Strategy (Executor-only, preserve history, no v1 governance reversion)
  - F-06: Permissions & Operational Simplicity (minimal token scope, explicit GitHub settings changes)

---

## 1. Goal / WHY

After PR #10 merged LIGHT Governance v2, the Merge → Readback → Closure workflow still requires manual Human intervention between each step.

**Goal**: Enable Human to authorize Merge once, then automatically execute:
- Merge validation (precondition checks)
- PR merge
- Merge verification (read-back)
- Closure Summary publication
- Issue close
- State recovery on failure

**Non-Goals**:
- Delegate Merge authorization to AI or GitHub Actions alone
- Implement pull-based recovery without Human awareness
- Bypass GitHub's native Branch Protection / Rulesets
- Add trust boundaries outside Human + identified GitHub Actions workflow

---

## 2. Risk Level
**L3** — Governance / Merge Executor / Issue Close Authorization

Requires:
- Pre-implementation: L3 Formal Plan + explicit Human Plan approval
- Per-execution: Specific Human Merge authorization (PR#, Head SHA, Base, Scope, Merge Method, Target Issue)

---

## 3. Current-State Evidence

**Already Deployed**:
- ✅ PR #10 merged @ 2799d97 (2026-11-06 04:49:21Z) — LIGHT Governance v2 active
- ✅ AGENTS.md v2 — Single-Builder + Self-Verification model confirmed
- ✅ scripts/merge_lifecycle.py — Local checklist helper (NO GitHub permissions)
- ✅ GitHub Actions — governance-tests.yml, docs-check.yml, pages.yml all active

**Known Issues**:
- ⚠️ GOVERNANCE.md L1 risk clause still contains "Cross-Agent Review" (contradicts v2 Single-Builder model)
- ⚠️ Branch Protection rules unknown (need Human verification)
- ⚠️ GitHub Actions token permissions unknown (need Human configuration)

---

## 4. Design Decision: Option A (workflow_dispatch) as Primary

### Recommended: Option A — GitHub Actions workflow_dispatch

**Rationale**:
1. **Trusted boundary**: Explicit Human action in GitHub UI with GitHub account authentication
2. **Audit trail**: All workflow runs logged in GitHub with triggerer identity
3. **Persistence**: Cross-session execution (Human approves once; workflow executes independently)
4. **Recoverability**: If workflow interrupted, can inspect run logs and retry safely
5. **No new infrastructure**: Uses existing GitHub Actions, no new services
6. **Governance alignment**: Aligns with "Human authorization → Automatic execution" model

**Option B (Claude Code one-shot)**: Kept in records for reference; not implemented here.
- Benefit: Single Human action within session
- Drawback: Session-bound, not cross-session persistent; GitHub MCP write methods unconfirmed

### Selected Implementation Model

```
Human Action (GitHub UI):
  1. Visit: Settings → Actions → "Merge and Close PR" workflow
  2. Click: "Run workflow"
  3. Inputs:
     - PR Number (e.g., 10)
     - Approved Head SHA (full 40-char, e.g., abc123...xyz)
     - Target Base (e.g., "main")
     - Merge Method (e.g., "squash", "merge", "rebase")
     - Target Issue Number (e.g., 9)
  4. Click: "Run workflow"

GitHub Actions Execution:
  1. Verify triggerer has write permissions (fail if not)
  2. Validate inputs (Head SHA format, Base exists, etc.)
  3. Fetch PR and verify (open, correct base, head matches input SHA)
  4. Run Merge Preconditions Gate (12 checks)
  5. Execute merge (GitHub API with SHA compare-and-swap)
  6. Verify merge in main
  7. Publish Closure Summary to issue
  8. Close issue
  9. Log all evidence

On Failure:
  - Fail Closed (stop immediately)
  - Publish failure summary to PR with recovery instructions
  - Preserve all evidence (logs, API responses)
  - Human must review and decide next step
```

---

## 5. F-01: Trusted Human Authorization

### Authorization Boundary Definition

**Who can trigger**:
- Only users with GitHub repository "maintain" or "admin" role (configurable)
- Must authenticate to GitHub
- GitHub Actions workflow_dispatch logs user identity

**How authorization is verified**:
1. GitHub Actions runtime provides `github.actor` (authenticated GitHub username)
2. Compare against allow-list of authorized users (stored in Repository Settings or workflow file)
3. If not in allow-list → Fail Closed with error message

**How to prevent impersonation**:
- ❌ Do NOT trust: Issue comments, PR body, CI status, commit author
- ❌ Do NOT trust: Any input that is user-editable without Git history
- ✅ DO trust: GitHub Actions `github.actor` (comes from GitHub runtime, not user input)
- ✅ DO trust: Fixed allow-list in repository settings or protected workflow file

**How to confirm trusted workflow version**:
- Workflow file must be in `main` branch
- GitHub Actions cannot execute workflow from PR branch (security default)
- Workflow file SHA checked via GitHub Actions context
- If workflow modified in PR, it is NOT executed (only merged version runs)

**Input binding to PR / Scope**:
- User inputs: PR#, Head SHA, Base, Merge Method, Issue#
- Validator checks:
  1. PR# exists and is open
  2. Head SHA is exactly 40-char hex (not alias like "latest" or "HEAD")
  3. Head SHA from PR.head.sha is verified to match input SHA (byte-for-byte)
  4. Base branch matches input (e.g., "main")
  5. Merge Method is in ["merge", "squash", "rebase"]
  6. Issue# exists and is open
  7. PR and Issue are linked (check PR body, linked issues field, or previous closure summary)

**Fail Closed**:
- If any input validation fails → DO NOT MERGE
- If `github.actor` not in allow-list → DO NOT MERGE
- If Head SHA does not match PR state → DO NOT MERGE
- Publish detailed error to PR with "MERGE AUTHORIZATION FAILED" label
- Stop execution; require Human review

---

## 6. F-02: Complete Merge Gates (12-Item Fail-Closed Check)

### Precondition Validation

All checks must PASS. Any UNKNOWN or FAIL → ABORT and Fail Closed.

```
1. AUTHORIZATION
   - github.actor in authorized users list → PASS
   - Fail if not in list

2. PR EXISTS & OPEN
   - PR (from PR#) exists in repository → PASS
   - PR.state == "open" → PASS
   - Fail if closed, merged, or not found

3. HEAD SHA MATCH (Byte-for-Byte)
   - PR.head.sha == input Head SHA (both 40-char hex)
   - Fail if not exact match (prevents stale SHA merge)

4. BASE MATCH
   - PR.base.ref == input Base (e.g., "main")
   - Fail if different branch

5. MERGE METHOD VALID
   - Merge Method in ["merge", "squash", "rebase"]
   - Fail if invalid or not specified

6. DIFF SCOPE UNCHANGED
   - Compute current PR diff (file list + line counts)
   - Compare to last-known approved diff in Plan or Result
   - If files/scope differ significantly → UNKNOWN (require Human re-approval)
   - If scope identical → PASS

7. REQUIRED CHECKS SUCCESS
   - Fetch all Check Runs for this Head SHA
   - For each check in approved list (e.g., "governance-tests", "docs-check"):
     a. Check Run exists for this Head SHA
     b. Check Run.status == "completed" (not "queued" or "in_progress")
     c. Check Run.conclusion == "success" (not "failure", "skipped", "neutral")
   - Fail if any check missing, pending, failed, or skipped
   - Stale check (created > 2 hours ago) → UNKNOWN; re-run CI if available

8. NO BLOCKING REVIEWS
   - Fetch all reviews on this PR
   - For this Head SHA, check if any review has state "changes_requested"
   - Fail if unresolved changes_requested found
   - "approve" reviews → note count (may be useful for audit)

9. NO MERGE CONFLICTS
   - GitHub PR.mergeable field:
     a. mergeable == true → PASS
     b. mergeable == false → FAIL (has conflicts)
     c. mergeable == null (unknown) → UNKNOWN; recompute via GitHub API

10. PLAN & RESULT EVIDENCE
    - Merge Plan (records/ISSUE-X/PLAN.md) exists and is committed to main
    - Merge Result (records/ISSUE-X/RESULT.md) exists, documents evidence
    - Human Merge Authorization is documented (comment SHA in Issue or Plan)
    - Fail if Plan or Result missing or outdated

11. ISSUE EXISTS & OPEN
    - Issue (from Issue#) exists in repository
    - Issue.state == "open"
    - Fail if closed, not found, or issue number mismatch

12. PR-ISSUE LINKAGE
    - PR.linked_issues contains Issue# (or vice versa)
    - OR PR body contains "fixes #<Issue#>" / "closes #<Issue#>"
    - OR previous Closure Summary comment exists on Issue mentioning PR#
    - Fail if no clear linkage found (prevents closing wrong issue)

```

### Merge Execution (SHA compare-and-swap)

**Before merge**:
1. Re-fetch PR.head.sha
2. Compare with stored Head SHA from input
3. If different → FAIL (prevents TOCTOU race)

**Merge call**:
```
POST /repos/{owner}/{repo}/pulls/{pr_number}/merge
{
  "merge_method": "squash",  (from input)
  "sha": "{input_head_sha}"   (compare-and-swap safety)
}
```

**After merge**:
1. Fetch PR again
2. Verify PR.merged == true
3. Verify PR.merged_by == GitHub Actions runner
4. Get PR.merge_commit_sha (record for audit)
5. Fetch main branch HEAD
6. Verify commit reachable from main (PR changes now in main)

---

## 7. F-03: Safe Live Testing

### Test Phases

**Phase 1: Mock Tests (No GitHub Access)**
- Input validation (SHA format, branch names, etc.)
- Merge gate logic (all 12 checks) with dummy data
- Closure and recovery state machine
- All run locally or in CI environment
- NO live GitHub API calls
- ✅ Can proceed without Human testing authorization

**Phase 2: Staged Live Tests (Isolated Resources)**
- Use dedicated test repository or test branch
- Test GitHub API calls (PR read, merge, issue close) on test data
- Verify GitHub Actions token permissions
- Verify workflows execute correctly
- Do NOT use real business PRs or Issues
- ⚠️ Requires explicit Human testing authorization and governance approval

**Phase 3: Integration with Real Workflow**
- After Phase 2 passes, integrate into main branch workflow file
- Deploy to production repository
- ⚠️ Requires explicit Human implementation authorization (separate from Plan approval)

### Authorization for Each Phase

**Mock Tests**:
- No Human authorization needed (no external side effects)
- Part of normal implementation review

**Live Tests (Phase 2)**:
- ✅ Requires explicit Human "test authorization" (separate prompt/form)
- Must specify: test repository/branch, test PR#, test Issue#
- Human confirms: does NOT affect main branch, production PRs, or deployed automation
- Must include: cleanup plan (delete test PR/issue after testing)

**Production Deployment**:
- ✅ Requires explicit Human "production deployment authorization"
- Separate from Plan approval (Plan is design; deployment is execution)
- Must confirm: workflow file location, token permissions, allowed users

---

## 8. F-04: Closure & Recovery State Machine

### State Definitions

```
MERGE_PENDING
  Description: Merge authorization received; precondition checks running
  Transitions:
    → BLOCKED (if any precondition fails)
    → MERGED_VERIFIED (if merge succeeds and verified)

MERGED_VERIFIED
  Description: Merge API succeeded; commit verified in main
  Transitions:
    → CLOSURE_PENDING (proceed to closure)
    → BLOCKED (if verification fails, e.g., commit not in main)

CLOSURE_PENDING
  Description: Closure Summary publishing; Issue close in progress
  Transitions:
    → CLOSED_VERIFIED (if issue closes successfully)
    → BLOCKED (if closure summary fails or issue close fails)

CLOSED_VERIFIED
  Description: Entire workflow complete; Issue closed, evidence recorded
  Transitions:
    → COMPLETED (end state)

BLOCKED
  Description: Failure occurred; workflow stopped
  Transitions:
    → MERGE_PENDING (Human re-approves after fix)
    → COMPLETED (Human decides to abort)
  Contains: error code, stage, evidence, recovery instructions
```

### Idempotency & Recovery

**Merge idempotency**:
- If merge already succeeded (PR.merged == true):
  → Skip merge API call; proceed to Closure_PENDING
  → Do NOT re-merge

**Closure idempotency**:
- If Closure Summary already posted:
  → Check for duplicate comments (do NOT re-post)
  → Proceed to close issue

**Issue close idempotency**:
- If Issue already closed:
  → Log as success (not a failure)
  → Do NOT attempt to re-close

**Remote readback before retry**:
- If workflow interrupted (timeout, cancellation):
  → DO NOT blindly retry
  → Human must inspect logs and confirm state
  → Re-run workflow with same inputs; idempotency prevents double-merge

---

## 9. F-05: Rollback Strategy

### Rollback Scope

Rollback reverts only:
1. `.github/workflows/merge-and-close-pr.yml` (new workflow file)
2. Any GitHub Actions token permission grants (if added)
3. Any repository settings changes (e.g., allow-list of authorized users)
4. `scripts/merge_lifecycle.py` extensions (if added)

Rollback does NOT:
- ❌ Revert LIGHT Governance v2 (stable, already merged in PR #10)
- ❌ Revert GOVERNANCE.md L1 fix (separate decision)
- ❌ Revert PLAN.md or Result records (evidence preservation)
- ❌ Undo any actual PR merges (those are business decisions, not implementation artifacts)

### Rollback Execution

1. Create revert PR (Human-authored or Claude Code draft)
2. Revert commits in order:
   - Remove workflow file addition
   - Remove token permission grants
   - Remove scripts extensions
3. Human reviews and approves revert PR
4. Merge revert PR
5. Disable workflow (if not yet removed)
6. Preserve all commit history, logs, records

---

## 10. F-06: Permissions & Operational Simplicity

### Minimum GitHub Actions Token Permissions

**Required scopes** (narrow scope, Actions-only):
```
permissions:
  contents: write     (Needed to: verify merge, read main branch)
  pull-requests: write (Needed to: check PR state, execute merge, add comments)
  issues: write       (Needed to: post Closure Summary, close issue)
```

**NOT needed**:
- ❌ admin / full repo access
- ❌ workflow permission (read-only)
- ❌ deployments, pages, secrets access

**Token scope enforcement**:
- GitHub Actions token is automatically scoped to workflow job (cannot use for other APIs)
- Token expires at end of workflow run (automatic)
- No permanent credentials needed

### GitHub Settings Changes Required

**Checklist** (Human must verify / configure):

| Setting | Current | Required | Action | L3 Decision |
|---------|---------|----------|--------|------------|
| Repository Visibility | Unknown | Public or Private | Confirm | Human verify |
| Branch Protection (main) | Unknown | Enforced (required) | Verify; do not modify | Human verify |
| Required Checks | Unknown | governance-tests, docs-check | Confirm in Branch Protection | Human verify |
| Rulesets | Unknown | Not bypassed by Actions | Verify; may need Actions exemption | Human decide |
| GitHub Actions | Active | Enabled + workflow_dispatch | Enable if not already | Human enable |
| Token Permissions | Unknown | contents/pull-requests/issues write | Verify in workflow settings | Human configure |
| Authorized Users (Trigger) | N/A | List of allowed GitHub usernames | Define in workflow allow-list | Human decide |

### Operational Simplicity

**For Human**:
- One-time setup:
  1. Enable GitHub Actions (if not already)
  2. Verify/grant minimal token permissions (automatic in v2.5+)
  3. Define allow-list of authorized users (edit workflow file or settings)
  4. Confirm Branch Protection rules

- Per-merge authorization:
  1. Visit workflow_dispatch UI
  2. Copy-paste: PR#, Head SHA (from GitHub PR page), Base, Merge Method, Issue#
  3. Click "Run workflow"
  4. Monitor in Actions tab (optional; automatic email if failure)

**For Implementation**:
- Workflow file is human-readable YAML
- No complex secrets or external services
- No database or state management
- Idempotent (safe to re-run if interrupted)

**What Claude Code does NOT do**:
- ❌ No automatic Merge (always requires explicit workflow_dispatch)
- ❌ No background polling
- ❌ No email/Slack notifications (GitHub Actions does this by default)
- ❌ No changes to GOVERNANCE.md enforcement
- ❌ No new GitHub Apps or OAuth applications

---

## 11. Workflow Architecture (Minimal)

### .github/workflows/merge-and-close-pr.yml

```yaml
name: Merge and Close PR

on:
  workflow_dispatch:
    inputs:
      pr_number:
        description: 'PR number to merge (e.g., 10)'
        required: true
        type: string
      head_sha:
        description: 'Approved full Head SHA (40-char hex, e.g., abc123...)'
        required: true
        type: string
      base_branch:
        description: 'Target base branch (e.g., main)'
        required: true
        type: string
        default: 'main'
      merge_method:
        description: 'Merge method'
        required: true
        type: choice
        options:
          - merge
          - squash
          - rebase
      issue_number:
        description: 'Target Issue number to close (e.g., 9)'
        required: true
        type: string

permissions:
  contents: write
  pull-requests: write
  issues: write

jobs:
  merge_and_close:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repo
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Validate authorization
        run: |
          AUTHORIZED_USERS="myaiwouldbemine"  # Comma-separated list
          if [[ ! "$AUTHORIZED_USERS" =~ "${{ github.actor }}" ]]; then
            echo "ERROR: User ${{ github.actor }} not authorized to trigger merge"
            exit 1
          fi
          echo "✓ Authorized user: ${{ github.actor }}"

      - name: Validate inputs
        run: |
          # PR number
          if ! [[ "${{ inputs.pr_number }}" =~ ^[0-9]+$ ]]; then
            echo "ERROR: PR number must be numeric"
            exit 1
          fi
          
          # Head SHA: 40-char hex
          if ! [[ "${{ inputs.head_sha }}" =~ ^[a-f0-9]{40}$ ]]; then
            echo "ERROR: Head SHA must be 40-char hex"
            exit 1
          fi
          
          # Merge method
          if ! [[ "${{ inputs.merge_method }}" =~ ^(merge|squash|rebase)$ ]]; then
            echo "ERROR: Invalid merge method"
            exit 1
          fi
          
          echo "✓ All inputs valid"

      - name: Run merge precondition gate
        run: |
          python3 scripts/merge_lifecycle.py \
            --check-preconditions \
            --pr-number "${{ inputs.pr_number }}" \
            --head-sha "${{ inputs.head_sha }}" \
            --base-branch "${{ inputs.base_branch }}" \
            --issue-number "${{ inputs.issue_number }}" \
            --token "${{ secrets.GITHUB_TOKEN }}"
          
          if [ $? -ne 0 ]; then
            echo "ERROR: Precondition gate failed"
            exit 1
          fi

      - name: Execute merge
        run: |
          python3 scripts/merge_lifecycle.py \
            --execute-merge \
            --pr-number "${{ inputs.pr_number }}" \
            --head-sha "${{ inputs.head_sha }}" \
            --merge-method "${{ inputs.merge_method }}" \
            --token "${{ secrets.GITHUB_TOKEN }}"

      - name: Verify merge
        run: |
          python3 scripts/merge_lifecycle.py \
            --verify-merge \
            --pr-number "${{ inputs.pr_number }}" \
            --base-branch "${{ inputs.base_branch }}" \
            --token "${{ secrets.GITHUB_TOKEN }}"

      - name: Publish closure summary
        run: |
          python3 scripts/merge_lifecycle.py \
            --publish-closure-summary \
            --pr-number "${{ inputs.pr_number }}" \
            --issue-number "${{ inputs.issue_number }}" \
            --merge-commit "${{ env.MERGE_COMMIT }}" \
            --token "${{ secrets.GITHUB_TOKEN }}"

      - name: Close issue
        run: |
          python3 scripts/merge_lifecycle.py \
            --close-issue \
            --issue-number "${{ inputs.issue_number }}" \
            --token "${{ secrets.GITHUB_TOKEN }}"

      - name: Log success
        run: |
          echo "✓ Merge and close workflow completed successfully"
          echo "PR #${{ inputs.pr_number }} merged to ${{ inputs.base_branch }}"
          echo "Issue #${{ inputs.issue_number }} closed"

  on_failure:
    runs-on: ubuntu-latest
    needs: merge_and_close
    if: failure()
    steps:
      - name: Report failure
        run: |
          echo "ERROR: Merge workflow failed at: ${{ job.status }}"
          echo "See logs for details: ${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}"
```

### scripts/merge_lifecycle.py (Extended)

```python
#!/usr/bin/env python3
"""
Merge Lifecycle: Preconditions, Execution, Verification, Closure
"""

import sys
import subprocess
import json
from dataclasses import dataclass
from typing import Optional, Dict, List

@dataclass
class MergeContext:
    pr_number: int
    head_sha: str
    base_branch: str
    merge_method: str
    issue_number: int
    token: str

class MergeGate:
    """12-item fail-closed merge precondition gate"""
    
    def __init__(self, ctx: MergeContext):
        self.ctx = ctx
        self.checks = []
    
    def check_authorization(self) -> bool:
        """Check 1: Authorization"""
        # Handled by workflow YAML (github.actor)
        # This is a placeholder for extended logic
        return True
    
    def check_pr_exists_and_open(self) -> bool:
        """Check 2: PR exists and is open"""
        result = subprocess.run([
            'gh', 'pr', 'view', str(self.ctx.pr_number),
            '--repo', f'{os.getenv("GITHUB_REPOSITORY")}',
            '--json', 'state,number'
        ], capture_output=True, text=True)
        
        if result.returncode != 0:
            return False
        
        data = json.loads(result.stdout)
        return data['state'] == 'OPEN'
    
    def check_head_sha_match(self) -> bool:
        """Check 3: Head SHA matches exactly"""
        result = subprocess.run([
            'gh', 'pr', 'view', str(self.ctx.pr_number),
            '--repo', f'{os.getenv("GITHUB_REPOSITORY")}',
            '--json', 'headRefOid'
        ], capture_output=True, text=True)
        
        if result.returncode != 0:
            return False
        
        data = json.loads(result.stdout)
        return data['headRefOid'].lower() == self.ctx.head_sha.lower()
    
    def check_required_checks_success(self) -> bool:
        """Check 7: All required checks passed on current Head"""
        result = subprocess.run([
            'gh', 'pr', 'checks', str(self.ctx.pr_number),
            '--repo', f'{os.getenv("GITHUB_REPOSITORY")}',
            '--required'
        ], capture_output=True, text=True)
        
        if result.returncode != 0:
            return False
        
        # Parse check runs: all must be 'success'
        lines = result.stdout.strip().split('\n')
        for line in lines:
            if not line or 'PASS' not in line:
                return False
        
        return True
    
    def check_no_blocking_reviews(self) -> bool:
        """Check 8: No unresolved blocking reviews"""
        result = subprocess.run([
            'gh', 'pr', 'reviews', str(self.ctx.pr_number),
            '--repo', f'{os.getenv("GITHUB_REPOSITORY")}',
            '--json', 'state'
        ], capture_output=True, text=True)
        
        if result.returncode != 0:
            return False
        
        # Look for 'CHANGES_REQUESTED'
        return 'CHANGES_REQUESTED' not in result.stdout
    
    def run_all_checks(self) -> Dict[str, bool]:
        """Run all 12 checks; return results"""
        checks = {
            'authorization': self.check_authorization(),
            'pr_exists_open': self.check_pr_exists_and_open(),
            'head_sha_match': self.check_head_sha_match(),
            # ... (additional checks)
            'required_checks': self.check_required_checks_success(),
            'no_blocking_reviews': self.check_no_blocking_reviews(),
        }
        
        return checks
    
    def all_pass(self) -> bool:
        """All checks passed?"""
        results = self.run_all_checks()
        return all(results.values())


def merge_preconditions_final(ctx: MergeContext) -> bool:
    """Execute complete merge gate; return True if ready to merge"""
    gate = MergeGate(ctx)
    results = gate.run_all_checks()
    
    # Log results
    for check, passed in results.items():
        status = "✓" if passed else "✗"
        print(f"{status} {check}")
    
    if not gate.all_pass():
        print("ERROR: Merge precondition gate FAILED")
        return False
    
    print("✓ All preconditions passed; ready to merge")
    return True

# ... (additional functions for merge, verify, closure, etc.)
```

---

## 12. Human Decisions (Revised — 5 Blocking Items)

**H-D1: Design Approach**
- Question: Accept Option A (workflow_dispatch) as primary, with Option B retained for reference only?
- Options:
  - ✓ Option A (workflow_dispatch) primary
  - Dual-implement A + B (requires more resources)
  - Option B (one-shot) primary (requires GitHub MCP write confirmation)
- Default: Option A
- **REQUIRED APPROVAL**: Yes

**H-D2: GitHub Actions Permissions & Token Configuration**
- Question: Authorize GitHub Actions token scopes (contents:write, pull-requests:write, issues:write)?
- Scope: Minimal, Actions-only, expires per workflow run
- Default: Approved (standard practice)
- Alternative: Custom scopes (requires GitHub Admin configuration)
- **REQUIRED APPROVAL**: Yes (confirms Human understands token security)

**H-D3: Authorized Users Allow-List**
- Question: Define which GitHub users can trigger the merge workflow?
- Options:
  - Single user (e.g., myaiwouldbemine only)
  - Multiple users (e.g., myaiwouldbemine, <co-admin>)
  - Any repository maintainer
- Default: myaiwouldbemine only (recommended for safety)
- **REQUIRED APPROVAL**: Yes (authorization boundary)

**H-D4: Governance Consistency Fix (L1 Clause Update)**
- Question: Approve update to GOVERNANCE.md L1 risk clause?
- Current (outdated): "Different agents' traceable cross-review"
- Proposed (aligned with v2): "Self-review + evidence + single-builder model"
- This is a separate L1 governance change; may be approved separately or deferred
- **REQUIRED APPROVAL**: Yes (to avoid future inconsistency)

**H-D5: Test Authorization & Scope**
- Question: Authorize mock tests during implementation? Authorize live tests on test repository?
- Phase 1 (Mock): Always authorized (no side effects)
- Phase 2 (Live/Staged): Requires explicit authorization + test resource specification
- Phase 3 (Production): Requires separate deployment authorization
- Default: Proceed with Phase 1 after Plan approval; require separate authorization for Phase 2+
- **REQUIRED APPROVAL**: Yes (for Phase 2+ clarity)

---

## 13. Implementation Scope

### What Will Be Implemented (If Approved)

1. ✅ `.github/workflows/merge-and-close-pr.yml` (new file)
2. ✅ `scripts/merge_lifecycle.py` (extend with precondition gate, merge, verify, closure functions)
3. ✅ `scripts/merge_lifecycle_test.py` (mock tests for all 12 checks)
4. ✅ `records/ISSUE-11/RESULT.md` (post-implementation evidence)
5. ✅ `GOVERNANCE.md` Section 3.1 update (L1 clause fix)
6. ✅ `MERGE-EXECUTOR-GUIDE.md` (operational manual)

### What Will NOT Be Implemented

- ❌ GitHub App or OAuth2 integration
- ❌ External state database
- ❌ Automated CI re-run triggers
- ❌ Changes to existing workflows (governance-tests, docs-check, pages)
- ❌ Changes to repository permissions / secrets / branch protection rules
- ❌ Automatic merge scheduling or background polling

---

## 14. Verification Strategy

### Mock Tests (Phase 1)
- All 12 precondition checks with dummy data
- State machine transitions (MERGE_PENDING → MERGED_VERIFIED → CLOSED_VERIFIED)
- Input validation (SHA format, branch names, numeric inputs)
- Idempotency (re-run same workflow; verify no double-merge)
- CI output: Full test report in records/ISSUE-11/TEST-REPORT.md

### Live Tests (Phase 2)
- Use dedicated test repository or test branch (NOT production)
- Create test PR, merge via workflow, close test issue
- Verify: PR merged, commit in main, issue closed, no side effects
- Cleanup: Delete test PR/issue; restore test repository to clean state
- CI output: Live test evidence + cleanup log

### Integration Tests (Phase 3)
- Deploy workflow to production repository
- Dry-run: Publish workflow; verify it appears in Actions tab
- First real merge: Execute workflow with real PR/issue (coordination with Product Owner)

---

## 15. Acceptance Criteria

All of the following must pass before workflow considered "ready":

- ✅ All 12 merge precondition checks implemented and tested
- ✅ Merge API call uses SHA compare-and-swap (no TOCTOU race)
- ✅ Merge verification reads PR.merged==true and verifies commit in main
- ✅ Closure Summary published as issue comment (includes PR#, merge commit, timestamp)
- ✅ Issue close executed; readback confirms issue.state == "CLOSED"
- ✅ All failure modes (BLOCKED state) defined and tested
- ✅ Idempotency: re-running same workflow does not double-merge
- ✅ State machine: 5-state transitions (PENDING → VERIFIED → CLOSURE → CLOSED) implemented
- ✅ Allow-list: Only authorized users can trigger workflow
- ✅ Mock tests: 100% pass rate (all 12 checks + state machine + idempotency)
- ✅ Live tests: Successful merge + closure on test resources
- ✅ Documentation: MERGE-EXECUTOR-GUIDE.md complete, Human-readable
- ✅ Rollback: Verified that removing workflow file cleanly disables automation
- ✅ GitHub Actions token: Verified permissions are minimal (contents/pr/issues write only)

---

## Appendix A: F-01～F-06 Corrections Mapping

| Finding | Section | Change | Impact |
|---------|---------|--------|--------|
| **F-01** | Section 5 | Added "How authorization verified" + "Input binding to PR/Scope" + "Fail Closed conditions" | Trusted boundary now explicit; prevents impersonation |
| **F-02** | Section 6 | Expanded gate from 10 → 12 checks; added "Stale check detection" + "SHA compare-and-swap" + "Diff scope validation" | Complete merge safety; prevents TOCTOU race, stale CI, scope creep |
| **F-03** | Section 7 | Separated Mock (no auth needed) vs Live (explicit auth required) | Safe progression; prevents accidental test-in-prod |
| **F-04** | Section 8 | Added 5-state machine + idempotency rules + "remote readback before retry" | Recoverable on failure; prevents double-merge, double-close |
| **F-05** | Section 9 | Limited rollback to Executor/Workflow only; preserve v2 governance + records | No regression to v1; governance stable |
| **F-06** | Section 10 | Explicit table of GitHub settings changes + Human decision points | Operational clarity; no hidden assumptions |

---

## Appendix B: Failure Recovery Scenarios (Updated)

| Scenario | State | Detection | Action | Recovery |
|----------|-------|-----------|--------|----------|
| **S-B1** | Merge API timeout | MERGE_PENDING | Workflow logs show partial response | Re-run workflow; idempotency check prevents double-merge |
| **S-B2** | Merge succeeds; verify fails | BLOCKED | PR.merged==true but commit not in main | Investigate GitHub sync delay; manual verification via git; document issue |
| **S-B3** | Merge succeeds; closure fails | BLOCKED | Closure Summary post fails (API error) | Retry publishing Closure Summary; check issue permissions |
| **S-B4** | Closure succeeds; issue close fails | BLOCKED | Issue still open after close API | Retry issue close; check issue.state; report to GitHub if API broken |
| **S-B5** | Workflow interrupted mid-execution | BLOCKED | Workflow cancelled or timeout | Inspect logs to determine state; re-run with same inputs; idempotency prevents side effects |
| **S-B6** | Wrong PR head SHA at trigger time | MERGE_PENDING | Precondition check fails (check 3) | Human must review, update inputs with correct SHA, re-trigger |
| **S-B7** | PR base changed after authorization | MERGE_PENDING | Base branch mismatch (check 4) | Investigate why base changed; confirm intended scope; re-trigger if correct |
| **S-B8** | Diff scope expanded after authorization | MERGE_PENDING | File list differs from approved scope (check 6) | Human re-approves new scope, or requests PR revert and re-push; re-trigger after approval |

---

## Appendix C: GitHub Permissions Checklist

**Workflow Token Scopes** (automatic via GitHub Actions):

```yaml
permissions:
  contents: write      # Read: main, head branches
                       # Write: merge commit
  pull-requests: write # Read: PR state, reviews, checks
                       # Write: merge PR
  issues: write        # Read: issue state
                       # Write: close issue, post comment
```

**NOT requested**:
- ❌ `admin` (too broad)
- ❌ `workflows` (not needed; workflow runs action, not modifies workflows)
- ❌ `deployments`, `pages`, `secrets`

**Test / Verification**:
- [ ] GitHub Actions enabled on repository
- [ ] `merge-and-close-pr` workflow file committed to main
- [ ] Branch Protection does NOT block GitHub Actions merge
- [ ] Authorized users list defined (e.g., myaiwouldbemine)
- [ ] Token permissions verified in Actions workflow logs

---

## Appendix D: Closure Summary Template

**Example (to be published as issue comment)**:

```
## ✅ PR #10 Merged & Issue #9 Closed

**Merge Details**:
- PR: #10
- Title: [PR Title]
- Head: abc123def456... (40-char SHA)
- Base: main
- Merge Method: squash
- Merged At: 2026-11-06 13:45:00 UTC
- Merge Commit: xyz789abc123... (new commit SHA)
- Merged By: GitHub Actions (merge-and-close-pr workflow)

**Workflow Run**:
- Run ID: 12345678
- Run URL: https://github.com/myaiwouldbemine/.../actions/runs/12345678
- Status: ✅ SUCCESS

**Verification**:
- ✅ PR merged (PR.merged == true)
- ✅ Merge commit in main (reachable from main HEAD)
- ✅ All checks passed on merged commit
- ✅ No conflicts

**This issue is now closed.**
```

---

## Appendix E: Pre-Implementation Checklist

**GitHub Setup** (Human to verify):
- [ ] GitHub Actions enabled
- [ ] Repository visibility confirmed (public / private)
- [ ] Branch Protection on main is active
- [ ] Required checks defined in Branch Protection
- [ ] Rulesets do not bypass GitHub Actions
- [ ] No force-push on main (Governance v2 compliant)

**Authorization Setup** (Human to define):
- [ ] Authorized users for workflow trigger (e.g., myaiwouldbemine)
- [ ] Approval of 5 Human Decisions (H-D1 through H-D5)
- [ ] Approval of GOVERNANCE.md L1 fix
- [ ] Approval of mock test phase
- [ ] Approval timeline for live test phase (Phase 2)

**Implementation Readiness**:
- [ ] Plan v2 approved by Human
- [ ] All 5 Human Decisions documented and approved
- [ ] Records/ISSUE-11/PLAN.md committed to main (after Plan approval)
- [ ] Mock test framework prepared
- [ ] Workflow file template prepared
- [ ] Merge_lifecycle.py extension ready for review

---

## Summary

**Formal Plan v2** addresses all F-01～F-06 concerns:

1. **F-01**: Trusted Human Authorization — GitHub Actions workflow_dispatch authenticated via `github.actor`; input binding to PR/Scope explicit
2. **F-02**: Complete Merge Gates — 12-item fail-closed check (added: Diff scope, Stale check detection, SHA compare-and-swap)
3. **F-03**: Safe Live Testing — Mock (no auth) vs Live (explicit auth) separated
4. **F-04**: Closure & Recovery — 5-state machine, idempotency rules, remote readback before retry
5. **F-05**: Rollback — Executor/Workflow only; v2 governance preserved
6. **F-06**: Permissions & Simplicity — Minimal token scope, explicit GitHub settings table, clear Human decisions

**Design**: Option A (workflow_dispatch) primary; Option B retained for comparison.

**Status**: **PLAN v2 READY FOR HUMAN APPROVAL**

**Next Steps**:
1. Human reviews Formal Plan v2
2. Human approves 5 Blocking Decisions (H-D1～H-D5)
3. Human approves GOVERNANCE.md L1 fix
4. Human authorizes Implementation phase (separate from Plan approval)
5. Implementation begins (if all approvals obtained)

