# Issue 34 plan — Bilingual labels for homepage project documents

Issue: https://github.com/myaiwouldbemine/myaiwouldbemine-Copy-Learning-Hub/issues/34
Accountable Builder: Claude Code (sole). Base: c4a33929d6a559484f9a440897ac75e29b32fc5a (origin/main).

## Goal
Show bilingual Traditional Chinese｜English labels for the About / Project heading and four engineering document links on the Pages homepage.

## Why
The homepage mainly serves Traditional Chinese readers; bilingual labels aid discovery while keeping English terms and stable URLs.

## Scope
- `docs/index.md` only: heading → `關於專案｜About / Project`; four link labels changed per Issue table; all five link targets and the Learning-to-Publishing Workflow entry unchanged.
- `records/ISSUE-34/` Plan, Result, evidence.

## Boundary
No change to GOVERNANCE.md, AGENTS.md, CI, scripts, teaching content, nav, image, or doc names/URLs. No direct push to main; sutra-wiki untouched.

## Implementation steps
1. Commit this Plan alone.
2. Edit docs/index.md.
3. Verify: git diff --check, mkdocs build --strict, built-HTML link/label check, governance tests, verify_plan_records.
4. Draft PR, Result, Self-Review, Ready, gated merge, Pages deployment SHA readback, archive, close.

## Acceptance criteria
Those of Issue 34.

## Revision history
- r0: initial plan.
