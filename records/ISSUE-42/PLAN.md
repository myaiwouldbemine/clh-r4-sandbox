# Issue 42 plan — Publish LEC08/LEC09 v4.1 DRAFT preview and fix Knowledge Connection links

Issue: https://github.com/myaiwouldbemine/myaiwouldbemine-Copy-Learning-Hub/issues/42
Learning Records (stay OPEN, not owned by this Issue): #26 (LEC08), #41 (LEC09).
Accountable Builder: Claude Code (sole). Base: origin/main (8937de5) at branch creation.
Source Artifact: `CLH_V4_REFINED_LEC08_LEC09_HTML_MD.zip` (24 entries), supplied by the Human; read-only candidate. Learning Record owns knowledge; Engineering Issue owns publication.

## Goal
Publish the existing v4.1 candidate for LEC08 and LEC09 as clearly labelled DRAFT pages for Human Learning Review, and make every cross-lecture link (Markdown, Obsidian WikiLink, built HTML, anchors) resolve.

## Why
The Human needs a browser-viewable preview. Investigation of the ZIP shows: (a) `lec09/index.md` lines 298 and 533 link `../lec08/NYCU_OS_LEC08.md` (wrong target filename, stale "V3" label); (b) the `docs/` copy still contains raw `[[NYCU_OS_LEC0x|...]]` WikiLinks that MkDocs would print as plain text; (c) the ZIP's `docs/.../lec08/index.md` would overwrite the existing public LEC08 Draft index.

## Scope
- Canonical Markdown, one per lesson, at flat root `OBSIDIAN_VAULT/NYCU_OS_LEC08.md`, `NYCU_OS_LEC09.md` and `OBSIDIAN_VAULT/_attachments/` (8 SVG), imported byte-faithfully from the ZIP except for the link/anchor fixes below.
- Generated MkDocs pages `docs/preview/lec08/index.md`, `docs/preview/lec09/index.md` (+ SVGs) derived from the canonical files by a small script (WikiLink to relative Markdown link, DRAFT banner), with a test that fails if they drift. No hand-edited duplicate bodies.
- `mkdocs.yml` nav entry "Preview (DRAFT)" only; link/asset validation script and tests; `records/ISSUE-42/`.

## Boundary
- No change to existing `docs/subjects/operating-systems/lec08/` content, Final lessons, GOVERNANCE.md, AGENTS.md, workflows, or the verifier.
- No RAW PDF or RAW_DATA published; no lesson PDF generated; standalone ZIP HTML not published (avoids duplicated bodies).
- No rewriting of lesson semantics. Only mechanical link-target corrections are made. Any new or changed Knowledge Connection (the five candidate pairs in the task) is NOT added by the Builder; they are verified against body text and reported, and proposals go to Learning Records #26/#41 as comments for Human Review.
- No Relearning Supplements created under Issue 42 (they stay under RELEARNING_SUPPLEMENTS/ISSUE-26 and ISSUE-41, which are not touched).
- No direct push to main; no claim that a Draft PR creates a live preview.

## Implementation plan
1. Commit this Plan alone (records only) before any other change; run `plan_fields_present` on it.
2. Preview strategy: Pages deploys only from main via pages.yml, so a live URL exists only after a normal PR merge. Least-invasive route: isolated `/preview/lec08/` and `/preview/lec09/` directories merged through the normal gated PR. Before merge, verify via `mkdocs build --strict` plus `mkdocs serve`/local static server for browser QA. Use the existing pages workflow; no new workflow.
3. Import canonical files and SVGs; fix `../lec08/NYCU_OS_LEC08.md` targets and verify each `[[...#Anchor]]` and Markdown anchor against actual headings; do not invent anchors. If no heading exists for a desired target, link to the page only and record it.
4. Add generator + validation script and tests (Markdown links, WikiLink targets, SVG presence, anchors, DRAFT label, sync).
5. Evaluate the five candidate connections against the lesson text/PDF page evidence; report PASS/PENDING per pair with the six required fields; propose, do not apply, new ones.
6. Verify, browser QA (desktop and mobile, Mermaid/Math/SVG), Draft PR, RESULT.md, Self-Review, Ready, gated merge, Pages SHA readback, evidence archive.

## Acceptance criteria
Those of Issue 42: both previews openable and visibly DRAFT; existing LEC08 unchanged; 8 SVGs, formulas, code, Mermaid render on desktop and mobile; LEC08 to LEC09 and back links clickable; `mkdocs build --strict` passes; PR, CI, Pages SHA readback and archive recorded; #26 and #41 remain open.

## Verification strategy
`git diff --check`; `mkdocs build --strict`; `python scripts/verify_plan_records.py <base> <head> 42` (after RESULT.md); repo unit/governance tests; link/anchor/WikiLink/SVG validation on source and built HTML; real browser QA (anything not done is NOT RUN); CI; post-merge deployed SHA readback. Merge, Pages and Closure require existing gates; if any needs authorization I lack, stop and report BLOCKED.

## Rollback
Revert PR of the merge commit (no history rewrite); preview paths are isolated, so reverting removes them without affecting existing content.

## Evidence archive
`records/ISSUE-42/RESULT.md` records source ZIP info, file list, link validation results, preview URLs, CI, deployment SHA, browser QA evidence, remaining risks.

## Revision history
- r0: initial Plan.
