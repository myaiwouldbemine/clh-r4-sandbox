# Issue 39 plan — Fix Canary L3 checklist table rendering; Plan-first verifier compliance

Issue: https://github.com/myaiwouldbemine/myaiwouldbemine-Copy-Learning-Hub/issues/39
Accountable Builder: Claude Code (sole). Base: origin/main (127ac09) at branch creation.
Context only (not reopened): closed Issue #37 / PR #38.

## Goal
1. Insert the missing blank line so the English L3 checklist table in `docs/development/CANARY_AUTHORIZATION.md` renders as an HTML table.
2. Land this Plan as the first commit, containing every heading required by `scripts/verify_plan_records.py`.

## Why
Issue #37 disclosed that the English L3 table rendered as plain text, and that its first Plan commit lacked verifier-required headings.

## Scope
- `docs/development/CANARY_AUTHORIZATION.md`: one blank line after the paragraph under `## Individually approvable L3 checklist`.
- `records/ISSUE-39/` (PLAN.md, RESULT.md).

## Boundary
No change to table cells, IDs, dependencies, row order, English text or Traditional Chinese translation. No change to GOVERNANCE.md, AGENTS.md, CI, scripts (including the verifier), mkdocs.yml, teaching content, sutra-wiki or other pages. No history rewrite, no direct push to main.

## Implementation plan
1. Commit this Plan alone (records only), before any other change.
2. Add the blank line; nothing else.
3. Verify, open Draft PR, write RESULT.md, Self-Review, Ready, gated merge, Pages SHA/HTTPS/table readback, archive evidence, close Issue.

## Acceptance criteria
Those of Issue 39.

## Verification strategy
- Initial Plan: before implementation, call `plan_fields_present()` from the verifier on the first Plan commit (Result is not yet expected); also confirm the Issue link and that the commit touches only `records/`.
- Final: `python scripts/verify_plan_records.py <base> <head> 39` (needs RESULT.md with PR link, so run after Result); `git diff --check`; diff shows exactly one added blank line; `mkdocs build --strict`; built HTML contains English and Chinese L3 tables with identical cell data; governance/unit tests; protected PR CI; post-merge Pages HTTPS, deployed SHA, and live table check. Browser visual QA: NOT RUN unless performed.

## Revision history
- r0: initial Plan.
