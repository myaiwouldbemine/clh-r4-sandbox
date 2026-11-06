# Issue #11 — Formal Plan v4: Learning-Centered Automation

## Revision History
- v1: 2026-11-06 13:13 UTC+8 — Initial comprehensive plan (526 lines)
- v2: 2026-11-06 13:35 UTC+8 — Security & consistency revision (987 lines)
- v3: 2026-11-06 14:00 UTC+8 — Proportionate simplification (317 lines)
- **v4: 2026-11-06 14:04 UTC+8 — Learning-centered automation (this version)**
  - Redesigned for Learning Traceability, not Agent Control
  - Focus: Preserve complete Issue → Plan → PR → Result → Merge → Closure learning history
  - Removed: Security-first framing, overengineered gates, complex state machines
  - Kept: Essential safety (SHA binding, idempotency, fail-closed)

---

## 1. Goal / WHY

**Copy Learning Hub's governance exists to preserve learning, not control.**

Current friction: After PR #10 merged LIGHT Governance v2, Merge Decision still required multiple manual steps (Human review + decision + merge + readback + closure summary + issue close).

**Goal**: Automate post-Human-authorization steps (Merge → Verification → Closure Summary → Issue Close), so the **complete learning history from Issue Question → Plan → Implementation → Result → Integrated Change → Consolidation** is preserved automatically.

**Why automation helps learning**:
- Learning Summary captures Why / What Changed / Evidence / What Learned
- Automatic closure comment consolidates the arc
- Issue Timeline shows complete traceability
- Human retains final Merge Decision; automation handles verification + closure

---

## 2. Risk Level

**L3** — Governance / Merge Authorization Change

Requires:
- Pre-implementation: Formal Plan + Human approval
- Per-merge: Human explicitly triggers workflow (decision point)

---

## 3. Learning-Centered Automation Design

### Authorization Boundary

Human's act of **triggering the GitHub Actions workflow_dispatch** with specific parameters (PR number, exact Head SHA, target Issue) constitutes explicit authorization for that merge.

GitHub's native audit trail (workflow run, triggering user, timestamp) is the evidence.

### Workflow Execution (Linear)

```
Human triggers workflow with:
  - PR number
  - Full Head SHA (copy-paste from GitHub)
  - Base branch (typically "main")
  - Merge method (squash / merge / rebase)
  - Issue number

Workflow runs:

  1. Verify authorization
     → Check github.actor is in allow-list
     → If not: ABORT, log failure

  2. Verify PR state
     → Open? (not draft, not closed)
     → Head SHA matches exactly?
     → Base branch matches?
     → If any fail: ABORT, log reason

  3. Verify CI + Merge readiness
     → Required checks passed? (governance-tests, docs-check)
     → No blocking reviews?
     → GitHub allows merge?
     → If any fail: ABORT, log reason

  4. Execute merge
     → Call GitHub Merge API with SHA compare-and-swap
     → Get response (merge commit SHA)
     → If fail: ABORT, log error

  5. Verify merge succeeded
     → Read PR merged_at timestamp
     → Confirm main branch contains merge commit
     → If verification fails: ABORT, log error

  6. Compose Learning Closure Summary
     → Why: Pull Issue / Plan / PR motivation
     → What Changed: Commit summary, files changed
     → Evidence: Merge Commit SHA, CI logs, PR link
     → What Learned: Auto-detect from PR title/body, default to "N/A"
     → Next Steps: Auto-detect from linked issues, default to "None"

  7. Post closure summary to issue
     → Single comment with formatted summary
     → If fails: ABORT, allow manual recovery

  8. Close issue
     → Set state to closed
     → Verify CLOSED status
     → If fails: ABORT, allow manual recovery

Success:
  → Workflow logs "COMPLETED"
  → All evidence in GitHub (PR, Issue timeline, Workflow logs)
  → Learning history preserved

Failure at any step:
  → Workflow stops immediately (fail-closed)
  → Posts error summary to PR
  → Human reviews logs, decides next action
  → If merge succeeded but closure failed: safe to retry after fixing closure
```

---

## 4. Essential Merge Gates (Six Checks)

| # | Gate | Verification | Fail Condition |
|---|------|-------------|----------------|
| 1 | Human Authorization | `github.actor` exactly matches allow-list | Not in allow-list → ABORT |
| 2 | PR Open | PR status "open", not draft, not closed | PR is draft/closed → ABORT |
| 3 | SHA Match | Head SHA exactly equals authorized SHA | SHA changed → ABORT |
| 4 | Base Branch | Base branch equals "main" (or authorized) | Base is wrong → ABORT |
| 5 | Required CI | `governance-tests` + `docs-check` = SUCCESS | Any check failed/pending → ABORT |
| 6 | No Blockers | No "changes requested" reviews, no blocking threads | Blocking review exists → ABORT |

If all six pass → proceed to merge. If any fails → stop.

---

## 5. Merge Execution (GitHub API)

Use GitHub REST API `/repos/{owner}/{repo}/pulls/{pr_number}/merge`:

```
POST /repos/myaiwouldbemine/myaiwouldbemine-Copy-Learning-Hub/pulls/{pr_number}/merge
{
  "commit_title": "Issue #<number>: <title>",
  "commit_message": "<body>",
  "sha": "<authorized-head-sha>",  // Compare-and-swap: prevents concurrent changes
  "merge_method": "squash"          // From Human's decision
}

Response success:
  {
    "sha": "<merge-commit-sha>",
    "merged": true,
    "message": "Pull Request successfully merged"
  }
```

The `sha` parameter ensures the merged commit is exactly what was authorized.

---

## 6. Post-Merge Verification

After merge API succeeds:

1. **Read PR state** → Confirm `merged: true`, `merged_at` is recent
2. **Read main branch HEAD** → Confirm latest commit is merge commit SHA
3. **Confirm closure not already posted** → Check if issue already has Closure Summary comment from previous run (prevent double-posting)

---

## 7. Learning Closure Summary (Issue Comment)

Automatic comment posted to issue:

```markdown
## ✅ Merged & Closed: Learning Consolidation

**Learning Motivation**
[Copy from Issue body]

**What Changed**
- PR: #<number>
- Commit: <merge-sha>
- Files: N changed
- [Auto-detect from diff or use "See PR for details"]

**Evidence**
- PR Link: #<number>
- Merge Commit: <sha>
- CI Results: All required checks passed
- GitHub Actions Workflow: <run link>

**What Learned**
[Auto-detect from PR title/labels, or "See PR discussion"]

**Remaining Questions / Next Steps**
[Auto-detect from linked issues, or "None identified"]

---
*Closure Summary generated automatically by Issue #11 workflow.*
```

**Why this format**:
- Captures the learning arc (Why → What → Evidence → Learned)
- Preserves traceability (links to PR, commit, CI)
- Blocks accidental double-posting (checks for prior Closure Summary)
- Human can edit/add detail after if needed

---

## 8. Failure Handling & Recovery

### Merge Not Yet Executed

Failure at gates 1–5: Stop, don't merge. Human fixes issue, re-triggers workflow.

Example:
- Gate 5 (CI failed) → Human pushes fix → Re-triggers workflow

### Merge Succeeded, Closure Failed

If merge API succeeded (gate 7) but closure fails (gates 8–9):

1. Workflow records merge commit SHA in error log
2. Human re-triggers workflow **with same parameters**
3. Workflow:
   - Reads PR state
   - Detects merged=true
   - Skips merge (already done)
   - Attempts closure again
   - If closure fails again: posts error to PR, allows manual completion

**Idempotency principle**: Re-running with same parameters never double-merges or double-posts closure.

### If Closure Summary Already Posted

Before posting closure comment:

1. Query issue comments
2. Search for existing "Merged & Closed: Learning Consolidation" comment
3. If found: Skip re-post, verify issue is closed
4. If issue is not closed: Log error, don't double-post

---

## 9. Implementation Scope

Will create / modify:

1. **`.github/workflows/merge-and-close-pr.yml`** (~120 lines YAML)
   - `workflow_dispatch` trigger with inputs
   - Six merge gate checks
   - Merge API call
   - Closure summary composition
   - Issue close

2. **`scripts/merge_lifecycle.py`** (~150 lines)
   - Helper: Check authorization
   - Helper: Validate PR state
   - Helper: Query CI status
   - Helper: Call merge API (with error handling)
   - Helper: Compose closure summary
   - Helper: Post comment + close issue
   - Helper: Idempotency checks (detect prior merge, prior closure)

3. **`scripts/merge_lifecycle_test.py`** (~100 lines)
   - Mock test: Gate checks work
   - Mock test: Merge API call structure
   - Mock test: Closure summary formatting
   - Mock test: Idempotency logic

Will NOT create / modify:

- ❌ GitHub repository settings
- ❌ Branch protection rules
- ❌ Approval registry or bot platform
- ❌ Additional governance documents
- ❌ New workflow triggers (only `merge-and-close-pr.yml`)

---

## 10. Verification & Acceptance Criteria

### Implementation Verification

1. ✅ Workflow file is valid YAML, parseable by GitHub
2. ✅ Python helpers have no syntax errors
3. ✅ Mock tests pass (all gates, merges, closures, idempotency)
4. ✅ Workflow can be triggered from GitHub UI
5. ✅ Inputs are received correctly

### Integration Verification (Mock Test PR)

1. ✅ Create mock PR with dummy commit
2. ✅ Run workflow with mock PR number
3. ✅ Verify all gates check correctly
4. ✅ Verify closure summary is formatted correctly (before posting)
5. ✅ Verify idempotency: re-run produces same output
6. ✅ Clean up mock PR

### Acceptance Criteria

- ✅ Human triggers workflow with PR + SHA + Issue
- ✅ Workflow validates six gates
- ✅ If all pass: merge executed, closure posted, issue closed
- ✅ If any gate fails: abort immediately, post error, preserve PR/Issue
- ✅ Learning history is complete and traceable
- ✅ GitHub audit trail shows all actions

---

## 11. Five Human Decisions

### H-D1: Workflow Trigger Allow-List

**Question**: Who is authorized to trigger the merge-and-close workflow?

**Options**:
- Only myaiwouldbemine (most restrictive)
- myaiwouldbemine + Codex (least restrictive for LIGHT Governance v2)
- Other users (specify)

**Recommendation**: Only **myaiwouldbemine** (sole administrator per GOVERNANCE.md)

**Rationale**: Merge is L3 operation; should remain tightly controlled.

---

### H-D2: Merge Method Preference

**Question**: When merging, which Git merge strategy?

**Options**:
- `squash` — Flatten PR commits into one (good for learning docs)
- `merge` — Keep full commit history (preserves exploration)
- `rebase` — Rebase onto main (cleaner history)

**Recommendation**: **squash** for Copy Learning Hub

**Rationale**: Learning Hub prioritizes narrative clarity. Squashing makes merged PR tell one coherent story.

---

### H-D3: Required CI Checks for Merge Gate

**Question**: Which GitHub Check Runs must be SUCCESS before merge?

**Current checks in repository**:
- `governance-tests` (runs AGENTS.md / GOVERNANCE.md tests)
- `docs-check` (validates Markdown / MkDocs)
- (Other checks if any)

**Recommendation**: Both **governance-tests** + **docs-check** must pass

**Rationale**: Learning Hub's primary artifacts are governance docs + markdown. Both matter.

---

### H-D4: GOVERNANCE.md L1 Clause Fix

**Question**: Update the L1 risk level description?

**Current text** in GOVERNANCE.md L1 risk:
> "不同 Agent 的可追溯交叉 Review"
> (Traceable Cross-Agent Review between different Agents)

**Issue**: This contradicts LIGHT Governance v2's Single-Builder model (Claude Code sole builder, Self-Review).

**Recommendation**: Change to:
> "Self-Review by Builder，確保可理解與可追溯"
> (Self-Review by Builder to ensure readability and traceability)

**Rationale**: v2 doesn't require multi-agent review for L1; this aligns text with actual policy.

---

### H-D5: Closure Comment Template Choice

**Question**: What detail level in the automatic closure summary?

**Options**:
- Minimal: Just PR link, commit SHA, status
- Standard: Minimal + files changed + issue link
- Detailed: Standard + CI logs, discussion summary, learned lessons

**Recommendation**: **Standard**

**Rationale**: Preserves learning arc (Why → What → Evidence) without overwhelming detail. Human can edit/expand if needed.

---

## 12. Rollback Strategy

If the automated merge-and-close workflow needs to be disabled:

1. **Disable workflow**: Uncheck "Enable workflow" in GitHub UI, or set `if: false` in YAML
2. **Return to manual process**: Human merges PR directly, manually closes issue
3. **Keep records**: Don't delete `records/ISSUE-11/PLAN.md`, Result, or GOVERNANCE.md changes

**Governance rollback**: None required. LIGHT Governance v2 stays in place.

**Code rollback**: Only if implementation introduces bugs:
1. Create `merge-and-close-pr-revert.md` explaining revert
2. Revert commit in new PR
3. Close Issue #11 as "ROLLED BACK"

---

## 13. GitHub Permissions & Settings

### Required GitHub Actions Token Permissions

The workflow will need a token with:
- `contents: read` — Read PR info, branch state
- `pull-requests: read` — Read PR state, reviews, checks
- `issues: write` — Post closure comment, close issue
- `statuses: read` — Read CI check status

**How to provide**: Use repository's existing `GITHUB_TOKEN` (GitHub Actions automatically provides this) with appropriate scopes. No separate token creation needed.

### Branch Protection Rules (Existing)

- **Require PR reviews**: Already enforced
- **Require status checks**: Already enforced
- **Dismiss stale reviews**: Already configured
- **Allow force pushes**: No (correct)
- **Allow deletions**: No (correct)

The workflow respects these rules; no changes needed.

### Workflow Activation

Workflow will be disabled initially (`if: false` or manual trigger only).

**Human must explicitly enable** after approval:
1. Review implementation PR
2. Merge to main
3. GitHub UI → Actions → Enable workflow

---

## Summary

**Formal Plan v4** reframes Issue #11's automation as **Learning Traceability**, not Agent Control:

✅ **Learning-centered**:
- Preserves complete Issue → Plan → PR → Result → Merge → Closure arc
- Closure summary consolidates learning (Why / What / Evidence / Learned)

✅ **Proportionate for Learning Hub**:
- Six essential gates (not twelve)
- Single trigger path (workflow_dispatch)
- GitHub-native (no external services)

✅ **Safe and trustworthy**:
- Human keeps merge decision
- Fail-closed (any check fails → abort)
- SHA binding (prevent commit changes after auth)
- Idempotent (safe to re-run)

✅ **Maintainable**:
- ~270 lines of YAML + Python (vs. v2's 987-line plan)
- Easy to understand (linear workflow)
- Easy to debug (clear gate checks)

---

## Revision History Summary

| Version | Date | Lines | Focus |
|---------|------|-------|-------|
| v1 | 13:13 UTC+8 | 526 | Comprehensive, security-first |
| v2 | 13:35 UTC+8 | 987 | Complex QA, multi-state machine |
| v3 | 14:00 UTC+8 | 317 | Simplified, proportionate |
| **v4** | **14:04 UTC+8** | **~250** | **Learning-centered, human-kept authority** |

---

**STATUS: PLAN PENDING HUMAN APPROVAL**

- ✅ Formal Plan v4 complete
- ✅ Learning-centered design (not Agent Control)
- ✅ Five human decisions identified
- ✅ Ready for human review and approval

**No implementation authorized yet. No workflow created. No PR merged. No issue closed.**

---

*Prepared by: Claude Code (Builder)*
*Repository: myaiwouldbemine/myaiwouldbemine-Copy-Learning-Hub*
*Issue: #11 — Authorized PR Merge → Verified Closure Automation*
