# Issue 37 plan — Bilingual EN/繁中 content for four Development docs; restore English homepage labels

Issue: https://github.com/myaiwouldbemine/myaiwouldbemine-Copy-Learning-Hub/issues/37
Accountable Builder: Claude Code (sole). Base: origin/main at branch creation.
Context only (not reopened): closed Issue #34.

## Goal
1. Restore English-only homepage heading/labels in `docs/index.md`.
2. Provide complete, section-aligned Traditional Chinese + English content in the four Development documents.

## Why
Issue #34 misread the request; titles stay English, body content is bilingual.

## Scope
- `docs/index.md`: heading -> `About / Project`; four labels -> `Autonomous Operations`, `Guarded Auto Merge`, `Independent Review`, `Canary Authorization`. All five link targets, the Learning-to-Publishing entry, nav and image unchanged.
- `docs/development/{AUTONOMOUS_OPERATIONS,GUARDED_AUTO_MERGE,INDEPENDENT_REVIEW,CANARY_AUTHORIZATION}.md`.
- `records/ISSUE-37/`.

## Boundary
No change to GOVERNANCE.md, AGENTS.md, CI, scripts, mkdocs.yml, teaching content or other pages. No new policy; ambiguities are flagged, not resolved. No direct push to main.

## Bilingual layout
- Document H1 and every `##`/`###` heading stay English-only (anchors unchanged). Existing ARCHIVED banner stays first, then its Traditional Chinese translation.
- Within each section: the original English text is kept byte-for-byte, followed by a `**繁體中文**` marker line and its Traditional Chinese translation, in the same paragraph/list/table order.
- Tables: English table, then a Traditional Chinese table with the same rows/columns (identifier cells such as R1, C3, `light/review` unchanged).
- Code blocks, commands, file paths, identifiers, SHAs, URLs and link targets are kept verbatim and not translated; Chinese blocks refer to the English code block rather than duplicating it. Link text is translated, targets unchanged.
- Existing 繁體中文摘要 in AUTONOMOUS_OPERATIONS is retained as is.
- Normative terms (MUST/never/only) map consistently: 必須/不得/僅; status words (PASS/BLOCK/NOT RUN/PENDING) stay English.

## Implementation plan
1. Commit this Plan alone.
2. Edit `docs/index.md`; translate the four documents.
3. Verify (below). Draft PR, Result, Self-Review, Ready, gated merge, Pages SHA readback, archive, close.

## Acceptance criteria
Those of Issue 37.

## Verification strategy
- Automated: `git diff --check`; English-preservation check (stripping added Chinese blocks reproduces the original English text of every file exactly); code fences, URLs, link targets and headings identical to original (scripted diff); `mkdocs build --strict`; built-HTML check of homepage labels and links; governance tests; `verify_plan_records.py`; protected PR CI.
- Section-by-section equivalence review: per file, count of sections/paragraphs/list items/table rows/code blocks English vs Chinese must match; then a manual normative-equivalence pass over roles, permissions, conditions, gates, failure/rollback, evidence, commands. Result lists findings per document.
- Translation quality is Builder self-review only; no native Human linguistic review or browser visual QA is claimed. Those are reported NOT RUN/PENDING unless performed.
- Pages: strict build, workflow URL, deployed SHA readback, HTTPS check of the bilingual docs and homepage labels.

## Revision history
- r0: initial plan.
- r1: heading-only rename (Implementation plan, Acceptance criteria, Verification strategy) so scripts/verify_plan_records.py recognises the fields; no content change. Made after implementation; r0 is in afa1430.
