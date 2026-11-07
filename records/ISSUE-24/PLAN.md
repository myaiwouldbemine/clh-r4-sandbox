# Issue 24 plan — LEC08 Draft Web publication pilot

Issue: https://github.com/myaiwouldbemine/myaiwouldbemine-Copy-Learning-Hub/issues/24
Accountable Builder: Claude Code (sole). Base: e5ed923 (main).

## Goal
Publish the four approved-for-draft LEC08 Markdown files as a clearly labelled **Draft / Preview** on the MkDocs site through the normal protected PR and push-triggered Pages path.

## Why
Exercise Markdown navigation, Mermaid, formulas and the per-Issue relearning list on the real pipeline, without blocking later content refinement.

## Scope
- Verify `RAW_DATA/operating-systems/LEC08/LEC08_FULL_DRAFT.zip` exists; record its SHA-256 and the four inner Markdown SHA-256 values. The ZIP is read-only input and is never modified or committed.
- Add `RAW_DATA/README.md` (centralized raw-data policy); `.gitignore` excludes everything else under `RAW_DATA/` so the original ZIP and unlicensed material stay out of the public repository.
- Import V2, V3, REVIEW_MANIFEST byte-for-byte to `docs/subjects/operating-systems/lec08/`, plus a Draft landing page and nav entries. Import RELEARNING_SUPPLEMENTS to `RELEARNING_SUPPLEMENTS/ISSUE-24/`, filling only Issue/PR/SHA metadata and keeping five PENDING items and PARTIAL scope.
- Records: this Plan, Result, evidence.

## Boundary
No change to educational semantics, no source PDF/slides/images, no new secrets, no direct push to main, no bypass, no edits to Issues 18/20/22 records. Draft status never implies content approval; PDF/Obsidian remain not built.

## Implementation plan
1. Commit this Plan alone.
2. Add RAW_DATA README, `.gitignore` rule, imported files, landing page, nav; verify imported bytes equal ZIP contents (except documented supplements metadata).
3. Run strict MkDocs, unit tests, diff check; inspect rendered Mermaid/math in the built HTML; visual check NOT RUN unless a browser is available.
4. Draft PR, Result, Self-Review block, Ready, gated lifecycle merge, observe push-triggered Pages run, HTTPS 200 and `deployment-sha.txt` equal to merge SHA, archive and readback, then close.

## Acceptance criteria
The Issue's Draft Publication Acceptance Criteria; each reported separately as PASS/FAIL/BLOCKED/PENDING/NOT RUN.

## Verification strategy
sha256 comparison with ZIP; `git check-ignore` on RAW_DATA ZIP and `git ls-files RAW_DATA`; strict MkDocs; repo unit tests; link and rendered-HTML checks; required CI; remote HTTPS and SHA readback.

## Revision history
- r0: initial plan.
