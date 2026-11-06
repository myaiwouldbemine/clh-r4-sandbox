# Issue #11 — Formal Plan v3 Simplified

## Revision History
- v1: 2026-11-06 13:13 UTC+8 — Initial Plan Draft (526 lines)
- v2: 2026-11-06 13:35 UTC+8 — Security & Consistency Revision (F-01～F-06)
- v3: 2026-11-06 14:00 UTC+8 — Simplified for Learning Hub (Proportionate Governance)
  - Removed: Complex state machines, arbitrary timeouts, dual executors, approval registry
  - Kept: Minimal merge gates, GitHub Actions workflow_dispatch, fail-closed behavior
  - Focus: Learn Hub's actual use case (knowledge base, markdown, collaboration)

---

## 1. Goal / WHY

After PR #10 merged LIGHT Governance v2, merging approved PRs to main and closing related issues still requires multiple manual steps.

**Goal**: Let Human authorize a merge once (by triggering a GitHub Actions workflow), then automatically:
- Verify the PR is safe to merge (minimal checks)
- Execute the merge (GitHub API)
- Verify success
- Close the related issue
- Handle common failures gracefully

**Constraints**:
- Human keeps merge decision authority
- Only use GitHub-native features (no external services)
- Respect Branch Protection / Rulesets
- Proportionate to a learning/documentation repository

---

## 2. Risk Level

**L3** — Governance / Issue Close Authorization

Requires:
- Pre-implementation: Formal Plan + Human approval
- Per-merge: Human explicitly triggers workflow (act of authorization)

---

## 3. Current State

- ✅ PR #10 merged; LIGHT Governance v2 active
- ✅ GitHub Actions available (governance-tests, docs-check running)
- ⚠️ GOVERNANCE.md L1 clause still says "Cross-Agent Review" (v1 legacy; needs update)
- ⚠️ Branch Protection on main is active (Human must verify exactly what rules)

---

## 4. Design: GitHub Actions workflow_dispatch

**Human Workflow**:
1. Go to: repo Settings → Actions → "Merge and Close" workflow
2. Click: "Run workflow"
3. Enter: PR Number, Head SHA (40-char), Target Base (main), Merge Method (squash/merge/rebase), Issue Number
4. Click: "Run"
5. Watch: Workflow executes, reports success/failure

**Workflow Execution**:
1. Verify Human's GitHub account is authorized
2. Verify PR, Head SHA, Base, and Issue
3. Confirm GitHub says merge is allowed
4. Execute merge via GitHub API (SHA compare-and-swap)
5. Verify merge succeeded
6. Post closure message to issue
7. Close issue
8. Report results

**On Failure**:
- Stop immediately (don't close issue if merge didn't happen)
- Post error to PR
- Human investigates and decides next step

---

## 5. Minimal Merge Gates (Six Checks)

Before merging, verify:

1. **Human Authorization**: `github.actor` (Person who triggered workflow) is in allow-list
   - Allow-list: defined in workflow file or repo settings (e.g., `myaiwouldbemine`)
   - Fail if: person not authorized → ABORT, post error to PR

2. **PR is Open**: PR exists, status is "open"
   - Fail if: PR closed, merged, or not found → ABORT

3. **Head SHA Matches**: The PR's current commit matches what Human authorized
   - Prevents: accidentally merging after new commits added
   - Compare: input SHA == PR.head.sha (normalized case-insensitive)
   - Fail if: mismatch → ABORT, post "SHA changed" message

4. **Base Correct**: PR's base branch is what we expect (usually "main")
   - Fail if: different → ABORT

5. **Required Checks Pass**: GitHub's mandatory CI (governance-tests, docs-check) succeeded on this commit
   - Fail if: any required check pending, failed, or missing → ABORT
   - Don't worry about: arbitrary time limits; GitHub has current state

6. **No Blocking Reviews**: No unresolved "changes requested" reviews
   - Fail if: unresolved blocking review → ABORT

**Result**: All six pass → proceed to merge. Any fail → stop and report.

---

## 6. Human Authorization

**What counts as authorization**:
- Human triggers the workflow via GitHub web UI (authenticated as their GitHub account)
- Workflow logs `github.actor` and timestamp
- Workflow records: PR#, Head SHA, Base, Issue#, Merge Method in logs
- GitHub Actions audit trail preserves everything

**How to confirm authorization is trustworthy**:
- ✅ Human's account is in allow-list (defined in workflow)
- ✅ Workflow code is in main branch (not PR branch; GitHub enforces this)
- ✅ Human has repository access (GitHub verifies)
- ✅ If they request re-run, same logic applies

**NOT required** (remove complexity):
- External approval system
- Second executor
- Persistent state database
- Complex token management

---

## 7. Post-Merge Closure

After merge succeeds:

1. **Read True State**:
   - Is PR merged? (PR.merged == true)
   - What was the merge commit? (PR.merge_commit_sha)
   - Is the commit in main?

2. **Post Closure Message** to the issue (as a comment):
   ```
   ✅ PR #10 merged to main
   Merge Commit: abc123...xyz
   Closed by: Merge and Close workflow
   Time: [timestamp]
   ```

3. **Close the Issue** via GitHub API
   - Only if PR is definitely merged
   - Only if issue was linked to the PR

4. **Verify Issue Closed** by reading issue state

---

## 8. Failure Handling

**If merge preconditions fail**:
- Don't merge
- Post error comment to PR
- Stop (Human investigates)

**If merge succeeds but closure fails**:
- Issue stays open
- Post message: "Merge succeeded, but issue close failed; see logs"
- Human can manually close or re-run workflow

**If workflow interrupted/times out**:
- Workflow stops
- Logs are preserved in GitHub Actions
- Human can inspect logs
- If they re-run: Idempotency checks prevent double-merge
  - Already merged? Skip merge, proceed to closure
  - Closure comment already posted? Skip, proceed to close issue
  - Issue already closed? Log as success

**Key**: Never delete/modify existing closure comment or re-close issue. Read state first.

---

## 9. Implementation Scope

### What will be created:

1. **.github/workflows/merge-and-close-pr.yml** (Workflow file)
   - ~100 lines of YAML
   - Inputs: pr_number, head_sha, base_branch, merge_method, issue_number
   - Permissions: contents write, pull-requests write, issues write
   - Steps: validate inputs, check PR, merge, verify, close issue

2. **scripts/merge_lifecycle.py** (Helper script)
   - ~150 lines of Python
   - Functions: check_pr_state, merge_via_api, verify_merge, post_closure, close_issue
   - Uses GitHub CLI (`gh`) or GitHub API via curl
   - No external dependencies beyond standard library

3. **records/ISSUE-11/RESULT.md** (After implementation)
   - Evidence: Test runs, example workflow executions, manual verification
   - Links to Plan v3 commit SHA

### What will NOT be created:

- ❌ Approval registry or persistent state database
- ❌ Second merge executor (Claude Code API calls)
- ❌ Complex state machine with separate recovery workflow
- ❌ External monitoring or notification service
- ❌ Changes to GitHub repository settings or tokens

---

## 10. Verification & Acceptance

### Mock Tests (No GitHub Access)
- ✅ Input validation (PR#, SHA format, merge method, etc.)
- ✅ Merge gate logic (all six checks)
- ✅ Closure message formatting
- ✅ Idempotency logic (no double-merge)

### Live Tests (On Test Repository or Test PR)
- ✅ Workflow actually runs when triggered
- ✅ Can read PR state via GitHub API
- ✅ Can merge test PR
- ✅ Can close test issue
- ✅ Idempotency: re-run doesn't break anything

### Acceptance Criteria
- ✅ Workflow runs successfully with valid inputs
- ✅ All six merge gates work (stop on failure)
- ✅ Merge executes via GitHub API
- ✅ Closure message posts to issue
- ✅ Issue closes
- ✅ Re-run is safe (no double-merge, no duplicate messages)
- ✅ Error messages are clear for Human
- ✅ Workflow logs are preserved

---

## 11. Five Human Decisions

**H-D1: Workflow Trigger Allow-list**
- Who can trigger the merge workflow?
- Recommend: myaiwouldbemine only (for safety)
- Can add others later if needed

**H-D2: Merge Method Preference**
- Default merge method: squash, merge, or rebase?
- Recommend: squash (cleaner history for docs)
- Can be chosen per merge

**H-D3: Required CI Checks**
- Which checks MUST pass before merge?
- Recommend: governance-tests, docs-check (already running)
- Human verifies these are the right ones for Learning Hub

**H-D4: Governance.md L1 Clause Update**
- Old (v1): "Different agents' traceable cross-review"
- New (v2): "Self-review + single-builder model"
- Approve the fix? → YES recommended

**H-D5: Closure Message Template**
- What should the closure message say?
- Recommend: Simple format (PR#, merge commit, timestamp)
- Can include link to main branch or release notes

---

## 12. Rollback

If the merge workflow is not working or needs to be disabled:

1. Delete `.github/workflows/merge-and-close-pr.yml` (or disable it)
2. Delete or archive the helper script
3. Go back to manual merge process

**No governance changes are reverted.** LIGHT Governance v2 stays in place.

---

## Revision History Summary

| Version | Date | Changes |
|---------|------|---------|
| v1 | 13:13 UTC+8 | Initial detailed plan (526 lines) |
| v2 | 13:35 UTC+8 | Security & QA additions (987 lines, complex) |
| v3 | 14:00 UTC+8 | Simplified for Learning Hub (this document) |

**Why v3 is simpler**:
- Removed multi-state recovery machine (use idempotency checks instead)
- Removed arbitrary CI timeout rules (use GitHub's current state)
- Removed dual-executor approach (workflow_dispatch only)
- Removed approval registry (Human's trigger IS authorization)
- Removed overly detailed Python examples (keep functional, not perfect)
- Focused on six essential merge gates, not twelve

**Still maintains**:
- Fail-closed behavior (any check fails → abort)
- GitHub API safety (SHA compare-and-swap, idempotency)
- Human authorization trust boundary (github.actor + allow-list)
- Full audit trail (GitHub Actions logs)
- Proper error handling

---

## Summary

**Formal Plan v3** is a minimal, executable merge automation for LIGHT Learning Hub:

1. **Six merge gates** (not twelve, not complex)
2. **GitHub Actions workflow_dispatch** (one authorization path)
3. **Idempotent closure** (safe to retry)
4. **Proportionate governance** (fits Learning Hub's needs)
5. **No external services** (GitHub native only)

**Next step**: Human reviews, approves five decisions, authorizes implementation.

---

**STATUS: PLAN PENDING HUMAN APPROVAL — NO IMPLEMENTATION AUTHORIZED**

