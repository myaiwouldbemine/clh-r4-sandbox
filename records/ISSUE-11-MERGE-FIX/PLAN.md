# Issue #11 Merge Error Handling Fix — Plan

**Issue:** #11 — Live E2E Run #14 Merge Failure Diagnosis  
**Related Test:** PR #14, Issue #13  
**Failure:** Exit code 1 in Execute Merge step (silent failure, no merge commit created)

## Problem Statement

The merge-and-close-pr.yml workflow's Execute Merge step fails silently with no diagnostic output. The root cause is a **bash -e (set -e) interaction with command substitution**:

When `gh api` fails inside `merge_api_result=$(gh api ...)`, the bash -e causes immediate exit without running the subsequent `if [[ $? -ne 0 ]]` error check. This results in:
- Exit code 1
- No merge commit created
- No error message printed
- PR #14 and Issue #13 remain Open

## Impact Classification

**L3 SECURITY/GOVERNANCE CHANGE** (Revised)
- Affects workflow **write permissions** (contents: read → contents: write)
- Governs Merge Executor's write access to repository contents
- Requires explicit Human authorization (per GOVERNANCE.md L3 rules)
- Cross-agent code review required
- New test Issue linkage required for E2E acceptance

**Rationale for L3:**
- Original classification as L1 was incomplete
- Discovered during review: GitHub REST Merge Pull Request API requires `contents: write`
- Current workflow declares `contents: read` only
- Upgrading to `contents: write` is a permission boundary change
- Per GOVERNANCE.md: Permission/governance changes are L3
- Requires explicit action scope authorization before execution

## Scope

### In Scope
1. Fix Execute Merge step error handling to use conditional assignment
2. Add safe error output (HTTP status, error message, no token leakage)
3. **Upgrade workflow permissions: `contents: read` → `contents: write`** (per GitHub API requirements)
4. Preserve all 6 gates and Head SHA Compare-and-Swap logic
5. Preserve Archive Record generation and Concurrency control
6. Create separate fix PR from #14 (independent diagnostic work)
7. Formal documentation of two-part problem:
   - **Confirmed:** bash -e + command substitution causes silent failure
   - **Hypothesis (awaiting E2E verification):** Missing `contents: write` permission prevents API success

### Out of Scope
- Changes to Gates 1-6 validation logic
- Changes to Archive Record composition
- Changes to other GitHub settings beyond workflow permissions
- Re-triggering failed workflow run #42194575325
- Closing/modifying PR #14 or Issue #13 directly

## Implementation Strategy

### Phase 1: Minimal Error Handling Fix
**File:** `.github/workflows/merge-and-close-pr.yml` (Execute Merge step)

**Changes:**
1. Replace unsafe pattern:
   ```bash
   merge_api_result=$(gh api ... 2>&1)
   if [[ $? -ne 0 ]]; then ...
   ```
   
   With conditional assignment (bash -e safe):
   ```bash
   if merge_api_result=$(gh api ... 2>&1); then
     # success path
   else
     # error path with diagnostics
   fi
   ```

2. Add safe error output:
   - Extract HTTP status via jq: `.status // "unknown"`
   - Extract error message via jq: `.message // "Unknown error"`
   - Extract sub-errors via jq: `.errors[]?.message // empty`
   - Never output raw response (may leak token)

3. Preserve success path:
   - Extract `.sha` for merge commit
   - Validate 40-char SHA
   - Set output `merge_sha` for Archive Record step
   - Echo success confirmation

### Phase 2: Testing
1. Commit fix to separate branch
2. Create Draft PR with fix
3. Run governance-tests and docs-check
4. Create test E2E run on fix PR with Issue linkage
5. Verify merge succeeds and Archive Record is created
6. Document results in RESULT.md

### Phase 3: Documentation
1. Record actual Reviewer (opposite agent)
2. Document reviewed commit hash
3. Link to failed run #42194575325 and fix run
4. Record findings: root cause, fix verification, token permissions

## Success Criteria

1. ✅ Fix PR passes governance-tests and docs-check
2. ✅ Execute Merge step properly handles API errors (no silent failures)
3. ✅ Diagnostic output includes HTTP status and error message
4. ✅ No token/secrets leakage in error output
5. ✅ Live E2E run on fix PR succeeds (merge, archive record, issue close)
6. ✅ Head SHA Compare-and-Swap logic preserved
7. ✅ All 6 gates preserved and functional
8. ✅ Archive Record generation step executes
9. ✅ Concurrency control unchanged
10. ✅ RESULT.md documents findings and fix verification

## Token Permissions Assessment

**Critical Finding:** GitHub REST Merge Pull Request API requires `contents: write` permission.

**Current Workflow:**
- `contents: read` ← INSUFFICIENT for PR merge
- `pull-requests: write` ← Necessary but not sufficient alone
- `issues: write` ← For closing issues
- `statuses: read` ← For check validation

**Fix Applied:**
- Upgrade to `contents: write` ← Required by GitHub API

**Assessment Before Fix:** 
- Status: INSUFFICIENT (missing required permission)
- Root cause of Run #42194575325 failure: Very likely `contents: read` insufficient
- Error message never visible due to bash -e + subst bug (silent failure)

**Assessment After Fix:**
- Status: SHOULD BE SUFFICIENT (both bash error handling + permissions fixed)
- Next: Live E2E test will confirm API succeeds with both fixes
- If API still fails: Error message will now be visible (conditional assignment + diagnostics)

**Two-Part Root Cause Analysis:**
1. **Confirmed:** bash -e + command substitution causes silent failure (error check never runs)
2. **Hypothesis:** Missing `contents: write` permission prevented API success (error message was hidden by bash bug)
3. **Verification:** Live E2E test will print actual GitHub API error, confirming hypothesis

## Related Artifacts

- **Failed run:** https://github.com/myaiwouldbemine/myaiwouldbemine-Copy-Learning-Hub/actions/runs/42194575325
- **Test PR:** #14
- **Test Issue:** #13
- **Workflow file:** `.github/workflows/merge-and-close-pr.yml` (Execute Merge step, lines 258–333)

## Notes

- This is diagnostic + minimal fix work (not implementation of new features)
- No L2/L3 authorization needed for error handling improvement
- Fix is backward compatible (same success behavior, better failure diagnostics)
- Silent failure is the primary bug; fix enables visibility
