# Issue 31 plan — Separate Development from subject navigation; feature the workflow image on Pages Home

Issue: https://github.com/myaiwouldbemine/myaiwouldbemine-Copy-Learning-Hub/issues/31
Accountable Builder: Claude Code (sole). Base: 5920566 (origin/main).

## Goal
Keep top navigation to Home and the five subjects; add a "How We Learn｜我們如何學習" section on Home that shows the Human-provided Excalidraw-style workflow image and links to the canonical workflow page; keep Development reachable from a secondary Home entry point.

## Why
CLH is learning-first; Development is supporting project documentation, not a subject. Home should explain the method visually while the detailed content stays in the single source of truth.

## Preflight findings (verified, not assumed)
- Image: `docs/development/Copy Learning Hub Workflow Infographic.png` (filename contains spaces; PNG 1536x1024, 2,250,471 bytes). Currently **untracked**, not gitignored. A `…png:Zone.Identifier` Windows sidecar sits beside it and must NOT be committed.
- Canonical page `docs/development/CLH_LEARNING_TO_PUBLISHING_WORKFLOW.md` exists and is tracked. Other `docs/development/*.md` pages are already outside nav.
- The infographic includes a "網站首頁建議" panel (a homepage proposal). The image is used as provided; it is not edited or regenerated.
- Publishing rights: the Human supplied the image for publication; Issue asks to confirm it is appropriate. Recorded as Human-asserted, not independently verified.

## Scope
- `mkdocs.yml`: remove the `Development` nav group only. Pages stay in `docs/`, so URLs stay valid.
- `docs/index.md`: add "How We Learn｜我們如何學習" (learning-first statement, clickable image with alt text, short Phase A–D summary, explicit text link to the canonical page, link to open full-size image) and an "About / Project" section linking the Development docs.
- Commit the image under its real filename (links URL-encode the spaces).
- `records/ISSUE-31/` Plan, Result, evidence.

## Boundary
No edits to GOVERNANCE.md, AGENTS.md, CI workflows, lifecycle scripts, curriculum content, theme/CSS, or the canonical workflow document (not moved or renamed). No generated/substitute image. No duplicate role matrix or Mermaid diagram on Home. No direct push to main.

## Implementation plan
1. Commit this Plan alone.
2. Add the image (not the Zone.Identifier file); edit `mkdocs.yml` and `docs/index.md`.
3. Verify: strict MkDocs build; built-HTML check that nav has no Development and links/images resolve; old workflow URL exists in `site/`; unit/governance tests; `verify_plan_records`; `git diff --check`.
4. Draft PR, Result, Self-Review, Ready, gated merge, Pages deployment and SHA/HTTPS readback, archive to `records/ISSUE-31/`, close.

## Acceptance criteria
Those of Issue 31: no Development in top nav (desktop/mobile); Home features the real image and links to the workflow page; no invented assets or broken URLs; canonical URL still valid with a secondary entry point; no duplicated canonical content on Home; relative links, responsive behavior, alt text and full-size viewing checked; strict MkDocs, tests, PR CI, post-deploy readback pass; browser visual QA performed only if tooling exists, else NOT RUN with manual steps; archive and closure after verified acceptance.

## Verification strategy
Report build, content, provenance, visual and deployment separately as PASS/FAIL/BLOCKED/PENDING/NOT RUN. No headless browser is known to be installed; if none is found, visual desktop/mobile QA is NOT RUN and static HTML/CSS checks are labelled as such.

## Revision history
- r0: initial plan.
