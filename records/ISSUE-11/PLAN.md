# Issue #11 — Formal Plan v1 SUMMARY

## Revision History
- v1: 2026-11-06 13:13 UTC+8 — Initial Plan Draft

---

## 1. Goal / WHY
After PR #10 merged LIGHT Governance v2, Merge → Readback → Closure Summary → Issue Close still requires manual Human intervention for each step.

**Goal**: Automate steps 2–5 (Merge execution, CI readback, Closure Summary, Issue Close) while preserving:
- Human decision authority on Merge (not delegated to AI)
- Complete audit trail & evidence
- Fail-Closed behavior
- Single-Builder + Self-Verification model

---

## 2. Risk Level
**L3** — Governance / Merge Executor / Issue Close / Authorization Gate

Requires:
- L2: Pre-implementation Formal Plan + Human Plan approval
- L3: Specific action/scope authorization (per Merge execution)

---

## 3. Current-State Evidence
- PR #10: Merged @ 2799d97 (2026-11-06 04:49:21Z) by myaiwouldbemine
- GOVERNANCE.md v2: Active on main, but L1 risk clause contains old "Cross-Agent Review" text (inconsistency #1)
- AGENTS.md v2: Reflects Single-Builder model
- scripts/merge_lifecycle.py: Local checklist only, NO GitHub permissions
- GitHub Actions: governance-tests.yml, docs-check.yml, pages.yml all active
- Repository: main branch protection unknown (need Human verification)
- GitHub Token: Merge + Close permissions UNKNOWN (need testing)

---

## 4. Design Comparison: Two Options

### OPTION A: GitHub Actions workflow_dispatch + Manual Human Trigger

**Flow**:
1. Human goes to GitHub repo Settings → Actions
2. Selects `merge-and-close-pr` workflow
3. Inputs: PR#, approved Head SHA, base, merge method, target Issue#
4. Hits "Run workflow"
5. GitHub Actions runs: Precondition checks → Merge → Readback → Closure Summary → Close Issue

**Pros**:
- GitHub-native authorization boundary (Human's GitHub account + workflow_dispatch permission)
- Persistent audit trail (workflow run logs, triggered by human login)
- Can be audited via GitHub UI
- Familiar interface for repository operators

**Cons**:
- Requires new workflow file + GitHub Actions permissions review
- Does NOT automatically prevent stale/old SHAs (Human must copy-paste correctly)
- workflow_dispatch UI does not enforce SHA format validation
- Cannot distinguish "approved authorization" from "accidental re-trigger"
- Requires separate Human action (no single-point approval)
- Workflow logs may have sensitive commit SHAs (public if repo is public)

**Assumptions to Test**:
- GitHub Actions has sufficient permissions to: github.event.pull_request.merge()
- github.event.pull_request.merge() respects Branch Protection
- Issue.close() can be invoked by Actions with repo token
- Token permissions can be scoped to this workflow only

---

### OPTION B: Claude Code Authorized One-Shot Execution (Same Session)

**Flow**:
1. Human explicitly approves PR#, Head SHA, base, scope, Merge method in chat
2. Claude Code validates approval message against explicit criteria (contains exact SHA, PR#, base, scope, merge method)
3. In same session, Claude Code calls GitHub API:
   - github-mcp-server-pull_request_read (verify PR state, head, base, merge status)
   - github-mcp-server-merge (execute merge with SHA compare-and-swap if available)
   - [closure workflow: issue read, comment, close]
4. Readback to Human: Full evidence of each step

**Pros**:
- Single Human action = authorization point
- No new infrastructure (GitHub Actions, tokens, secrets)
- Idempotent per session (can retry safely within same session with same evidence)
- Evidence collected in real-time in chat
- Clear authorization -> execution -> readback chain

**Cons**:
- Cross-session: Human must approve in same session; if session closes, authorization evidence lost
- GitHub MCP tool availability: Merge + Close via MCP? (Not confirmed; may only be read-only)
- Session interruption: Cannot resume stalled execution in new session without re-approval
- No persistent audit trail in GitHub (approval only visible in chat session)
- Burden on Human to provide full, exact SHA every time
- If session token expires, operations fail with unclear auth error

**Assumptions to Test**:
- github-mcp-server has write methods for Merge + Close (not just read)
- GitHub MCP authenticates as Human (not service bot)
- Token inherits Human's permissions (can Merge if Human can)
- Session persistence across network/interruption (likely NO — session-bound)

---

## 5. Recommended Approach

**HYBRID**: Use Option A (GitHub Actions workflow_dispatch) as primary, with fallback to Option B for single-session testing.

**Rationale**:
- Option A provides durable, auditable authorization boundary
- Option B adds risk of session-bound state loss without clear recovery
- Combination allows testing Option A workflows before full rollout

**Minimum Viable Scope**:
1. New file: `.github/workflows/merge-and-close-pr.yml`
   - Inputs: pr_number, head_sha (full), base_branch, merge_method, issue_number
   - Precondition checks (via merge_lifecycle.py)
   - Merge execution with SHA validation
   - Closure Summary + Issue Close
   - Failure handling

2. Governance.md L1 consistency fix:
   - Replace "Cross-Agent Review" → "Self-Review + Evidence"
   - Update Merge Executor reference (currently says "no merge executor")

3. Updated scripts/merge_lifecycle.py:
   - New function: merge_preconditions_final() — detailed final checks before Merge
   - No network calls; only local state validation

4. Tests in scripts/test_merge_lifecycle.py:
   - Mock workflow execution flow
   - Live GitHub API tests (if authorized by Human)

5. Documentation: `records/ISSUE-11/MERGE-EXECUTOR-GUIDE.md`
   - How Human triggers workflow_dispatch
   - What to verify before authorizing
   - What happens if Merge fails
   - How to recover

---

## 6. Merge Preconditions (Fail-Closed Gate)

Must ALL pass before executing Merge:

1. [ ] PR is OPEN (not already merged, not closed)
2. [ ] Head SHA **exactly** matches approved SHA (full 40-char)
3. [ ] Base branch matches approved base
4. [ ] PR has not changed risk classification
5. [ ] Formal Plan exists and is approved by Human
6. [ ] RESULT.md exists with evidence (if L2+)
7. [ ] All required GitHub Actions checks are SUCCESS on that exact Head SHA
8. [ ] No unresolved Blocking Review or Thread
9. [ ] No stale evidence (checks older than X hours)
10. [ ] Human explicitly approved BOTH Merge authorization AND closure scope

**If ANY condition fails**: ABORT. Do not Merge. Record reason and stop.

---

## 7. Post-Merge Closure Workflow

```
Merge Execute
  ↓
[SUCCESS] → Read PR: merged=true, merge_commit_sha
  ↓
Read main branch: does it contain merge_commit_sha?
  ↓
[YES] → Verify GOVERNANCE.md, AGENTS.md, records/ intact
  ↓
Publish Closure Summary to Issue:
  - Head SHA (approved)
  - Merge SHA (actual)
  - CI checks (all names + status)
  - Plan/Result links
  - Human decision reference
  - Completed items
  ↓
[SUCCESS] → Close Issue
  ↓
Readback: Issue state = CLOSED
  ↓
DONE
```

**Failure Recovery**:
- Merge success + Closure Summary fail → Mark CLOSURE_PENDING, allow safe retry
- Closure Summary success + Close fail → Same; CLOSURE_PENDING
- Any failure → Do NOT auto-recover; log and wait for Human to acknowledge

---

## 8. Governance Consistency Fixes

### Current Issue
`main/GOVERNANCE.md` line ~25 (L1 risk clause):
```
| L1 | 教材語意、一般程式或網站行為 | 適用驗證＋不同 Agent 的可追溯交叉 Review |
```

**But** Issue #9 / LIGHT v2 removed Cross-Agent requirement. Inconsistency.

### Fix (Issue #11 scope)
Replace with:
```
| L1 | 教材語意、一般程式或網站行為 | 適用驗證＋Claude Code Self-Review with traced Evidence |
```

Also update Merge section reference from "不授權啟用 Auto-Merge、不新增 merge executor" to:
```
不授權全域 Auto-Merge; 允許 Human-Authorization-Bound PR Merge executor 
（於 Plan 明確設計且經 Human L3 具體核准後）
```

---

## 9. GitHub Permissions Required

**New Permissions** (to request from Human):
- `actions` permission to register new `merge-and-close-pr.yml` workflow
- GitHub Actions on `merge-and-close-pr.yml` can:
  - `contents:write` (to merge PR)
  - `pull-requests:write` (to comment / manage PR state)
  - `issues:write` (to close Issue)

**Not Requested** (remaining limits):
- No Personal Access Token outside GitHub Actions
- No new Secrets stored in repo
- No modification to branch protection rules
- No direct main push

---

## 10. Testing Strategy

### Phase 1: Mock Tests (local, no GitHub)
- Test merge_preconditions_final() with various State combinations
- Verify Fail-Closed logic
- Mock GitHub API responses

### Phase 2: Staged Live Tests (if Human approves)
- Create test PR on non-main branch
- Run workflow_dispatch with test PR
- Verify checks without actually merging
- Mock Closure Summary (do NOT close actual Issue)

### Phase 3: Production Merge (Human-Authorized)
- Same workflow but with real PR → issue pairing
- Full execution with live GitHub API
- Readback verification

---

## 11. Acceptance Criteria (From Issue #11)

- [x] 唯讀 Recon 完成
- [x] 設計方案比較 (Option A/B)
- [x] Merge Preconditions 清單
- [x] Post-Merge Closure 工作流
- [x] Governance consistency 修正確認
- [x] GitHub 權限需求列明
- [ ] Formal Plan committed to records/ISSUE-11/PLAN.md
- [ ] Human approves Plan + Scope + Permissions
- [ ] Approved Plan published to Issue Timeline (only after Human approval)
- [ ] Implementation & Testing (FUTURE - not in PLAN stage)

---

## 12. Human Decisions Required (BLOCKING)

1. **Option Selection**: Option A (workflow_dispatch) or Option B (One-Shot) or Hybrid?
2. **Governance Consistency Fix**: Approve proposed GOVERNANCE.md L1 + Merge section updates?
3. **GitHub Permissions**: Authorize new GitHub Actions workflow + Token permissions?
4. **Merge Preconditions**: Approve the 10-item Fail-Closed gate list?
5. **Test Scope**: Live tests on real/test PR, or mock-only before implementation?

---

## 13. Implementation Scope (NEXT STAGE - if approved)

Estimated changes:
- NEW: `.github/workflows/merge-and-close-pr.yml` (~80 lines)
- EDIT: `scripts/merge_lifecycle.py` (+~30 lines)
- EDIT: `scripts/test_merge_lifecycle.py` (+~50 lines)
- NEW: `records/ISSUE-11/MERGE-EXECUTOR-GUIDE.md` (~100 lines)
- EDIT: `main/GOVERNANCE.md` (~5 lines)
- NEW: Draft PR with above + tests

---

## 14. Rollback Strategy

If implementation introduces issues:
1. Revert `.github/workflows/merge-and-close-pr.yml` (disable workflow)
2. Revert `GOVERNANCE.md` changes (restore Cross-Agent language if needed)
3. Restore previous `merge_lifecycle.py` (fallback to local-only checks)
4. Preserve all records/ history (no deletion)

---

## 15. Revision History

- v1 (2026-11-06 13:13): Initial comprehensive Plan Draft


---

## APPENDIX A: Option A vs Option B Detailed Comparison

| Aspect | Option A (workflow_dispatch) | Option B (One-Shot) | Winner |
|--------|------------------------------|-------------------|--------|
| **Authorization boundary** | GitHub account + Actions (verifiable) | Chat approval (session-bound) | A |
| **Audit trail persistence** | Workflow logs (GitHub UI) | Session logs only | A |
| **Human effort** | 1 manual action (click "Run") | 1 message approval | B |
| **Cross-session recovery** | Yes (workflow logs) | No (session ends) | A |
| **Token management** | Centralized (repo secrets) | Session-based | B |
| **Infrastructure needed** | New workflow file + permissions | No new infra | B |
| **Idempotent retry** | Safe (stateless workflow) | Within session only | A |
| **Spoofing risk** | Low (GitHub account verifiable) | High (chat text forgery) | A |
| **Implementation time** | ~2-3 hours | ~1 hour | B |
| **Long-term maintainability** | High (standard GH practice) | Low (session-dependent) | A |

**Consensus**: Option A is better for production. Option B acceptable for testing/validation only.

---

## APPENDIX B: Failure Recovery Scenarios & Handling

### Scenario 1: PR state changed before Merge

**Condition**: Head SHA changed (new commit pushed after approval)  
**Detection**: Pre-merge check fails (current head ≠ approved SHA)  
**Action**: ABORT, log new SHA, notify Human  
**Recovery**: Human re-approves new SHA, re-triggers workflow

### Scenario 2: Merge API succeeds but response lost

**Condition**: API call times out or network dropped  
**Detection**: Retry Merge → PR already merged  
**Check**: Read PR.merged == true  
**Action**: Extract merge_commit_sha from PR, continue to Closure Summary  
**Recovery**: Idempotent — no duplicate merge, proceed to step 2

### Scenario 3: Merge success, CI checks changed (pending/failed)

**Condition**: CI workflow triggered AFTER Merge (race condition)  
**Detection**: Pre-merge checks show SUCCESS, post-merge checks show PENDING  
**Action**: Log the race condition; Closure Summary will note checks were SUCCESS at time of merge  
**Recovery**: Re-run CI manually; if fails, document in Closure Summary as "post-merge check failure"

### Scenario 4: Merge success, Closure Summary publish fails

**Condition**: Issue.create_comment() fails (permissions, rate limit, etc)  
**Detection**: API error response  
**Action**: ABORT post-merge closure; mark Issue as `CLOSURE_PENDING`  
**Recovery**: Manual retry (Human or Claude Code in new session); post Closure Summary manually if needed

### Scenario 5: Closure Summary success, Issue.close() fails

**Condition**: Issue.close() fails (wrong Issue ID, already closed, etc)  
**Detection**: API error  
**Action**: ABORT; mark as `CLOSURE_PENDING`; Closure Summary already published  
**Recovery**: Retry close() with verified Issue ID; update Closure Summary if needed

### Scenario 6: Duplicate workflow trigger (Human re-ran by accident)

**Condition**: workflow_dispatch triggered twice with same PR#/SHA  
**Detection**: Second run reads PR.merged == true  
**Action**: Skip merge; go directly to Closure Summary check  
**Recovery**: If Closure Summary already exists, verify content; if not, regenerate; do NOT duplicate Issue comment

### Scenario 7: Wrong Issue# provided in workflow input

**Condition**: Workflow tries to close Issue #99 but PR is for Issue #10  
**Detection**: PR body scanned for "Closes #10", finds no match  
**Action**: ABORT; log mismatch; do NOT close Issue #99  
**Recovery**: Correct Issue # and retry; manually verify Issue #99 state

### Scenario 8: Workflow cancelled mid-execution

**Condition**: Human or GitHub cancels workflow run  
**Detection**: Workflow status = `cancelled`  
**Action**: Stop all pending operations; record last successful step  
**Recovery**: Manual review of logs; verify PR.merged status; retry from last known point (Merge check or Closure Summary)

---

## APPENDIX C: Example Merge Preconditions Checklist (Automated)

```python
def final_merge_preconditions(pr_number, approved_sha, base_branch, issue_number):
    """
    Fail-Closed precondition check. Returns (pass: bool, blockers: list, evidence: dict)
    """
    evidence = {}
    blockers = []
    
    # 1. PR is OPEN
    pr = github_read_pr(pr_number)
    evidence['pr_state'] = pr['state']
    if pr['state'] != 'OPEN':
        blockers.append(f"PR #{pr_number} is {pr['state']}, not OPEN")
    
    # 2. Head SHA exactly matches approved SHA
    evidence['current_head_sha'] = pr['head']['sha']
    evidence['approved_sha'] = approved_sha
    if pr['head']['sha'] != approved_sha:
        blockers.append(f"Head SHA mismatch: current {pr['head']['sha'][:7]} != approved {approved_sha[:7]}")
    
    # 3. Base branch matches
    evidence['current_base'] = pr['base']['ref']
    evidence['approved_base'] = base_branch
    if pr['base']['ref'] != base_branch:
        blockers.append(f"Base branch mismatch: current {pr['base']['ref']} != approved {base_branch}")
    
    # 4. All required checks are SUCCESS
    checks = github_read_checks(pr_number, approved_sha)
    evidence['checks'] = {c['name']: c['status'] for c in checks}
    failed_checks = [c['name'] for c in checks if c['status'] != 'SUCCESS']
    if failed_checks:
        blockers.append(f"Checks failed/pending: {failed_checks}")
    
    # 5. No unresolved blocking reviews
    reviews = github_read_reviews(pr_number)
    blocking = [r for r in reviews if r['state'] == 'CHANGES_REQUESTED']
    if blocking:
        blockers.append(f"Blocking reviews from: {[r['user'] for r in blocking]}")
    evidence['blocking_reviews'] = blocking
    
    # 6. Formal Plan exists
    plan_file = f"records/ISSUE-{issue_number}/PLAN.md"
    if not file_exists(plan_file):
        blockers.append(f"Plan not found: {plan_file}")
    evidence['plan_exists'] = file_exists(plan_file)
    
    # 7. RESULT.md exists (if L2+)
    result_file = f"records/ISSUE-{issue_number}/RESULT.md"
    issue_risk = determine_risk(issue_number)
    if issue_risk >= 2 and not file_exists(result_file):
        blockers.append(f"Result not found for L{issue_risk} issue: {result_file}")
    evidence['result_exists'] = file_exists(result_file)
    evidence['risk_level'] = issue_risk
    
    # 8. No stale evidence (checks < 30 min old)
    check_age_minutes = (now() - pr['updated_at']).total_seconds() / 60
    evidence['check_age_minutes'] = check_age_minutes
    if check_age_minutes > 30:
        blockers.append(f"Checks are stale ({check_age_minutes:.0f} min old)")
    
    return (len(blockers) == 0, blockers, evidence)
```

---

## APPENDIX D: Closure Summary Template

```markdown
## Closure Summary: Issue #<N> — PR #<M> Merged

**Date**: [timestamp]
**Status**: ✅ COMPLETED

### Merge Authorization
- **Approved Head SHA**: [full 40-char]
- **Approved Base**: main
- **Merge Method**: [squash/merge/rebase]
- **Human Authorizer**: [username]
- **Authorization Reference**: [Issue comment / message reference]

### Merge Execution
- **Merge Commit SHA**: [merge commit hash]
- **Merged At**: [timestamp]
- **Branch**: main now includes all commits from approved head

### Verification
- **All Preconditions**: PASSED
  - PR Open: ✅
  - Head SHA Match: ✅ 
  - Base Match: ✅
  - CI Checks**: ✅ (governance-tests.yml, docs-check.yml)
  - No Blocking Reviews: ✅
  - Plan + Result: ✅

### Linked Records
- Formal Plan: `records/ISSUE-<N>/PLAN.md` (approved @ commit [SHA])
- Implementation Result: `records/ISSUE-<N>/RESULT.md`
- PR: #<M>
- Merge Commit: [link]

### Completed Items
- ✅ Merge preconditions validated
- ✅ PR merged to main
- ✅ CI passed on merge commit
- ✅ Records verified intact
- ✅ Closure Summary published

### Known Limitations / Future Work
- [if any]

---

**This Issue is now CLOSED.**
```

---

## APPENDIX E: Live GitHub API Test Checklist (When Authorized)

Before attempting first live Merge, validate:

- [ ] Test GitHub token has `contents:write` permission (create test file on branch)
- [ ] Test token can merge PR (merge test PR without authorization gate first)
- [ ] Test token can comment on Issue (post test comment)
- [ ] Test token can close Issue (close dummy test Issue)
- [ ] Token permissions are scoped to Actions (not Personal Access Token)
- [ ] Branch Protection rules allow merge from workflow (or exempt it)
- [ ] Merge commit SHA is correctly returned by API
- [ ] PR.merged state updates immediately after merge call
- [ ] Issue.state changes to CLOSED after close call
- [ ] Idempotent retry: second merge call on merged PR fails gracefully
- [ ] Idempotent retry: second close call on closed Issue succeeds (no-op)

All tests should be logged and results provided to Human before production authorization.

