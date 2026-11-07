# Issue 31 result

Issue: https://github.com/myaiwouldbemine/myaiwouldbemine-Copy-Learning-Hub/issues/31
Builder: Claude Code (sole). Plan: records/ISSUE-31/PLAN.md (commit 8afc795, committed before implementation).

## Results
- Nav: `Development` group removed from `mkdocs.yml`; built top tabs are Home + 5 subjects (PASS, checked in built `site/index.html`).
- Home: "How We Learn｜我們如何學習" section with clickable image (opens full-size, new tab), alt text, Phase A–D summary, text link to the canonical workflow, and "About / Project" list linking the five Development pages (PASS, static).
- Image: real file `docs/development/Copy Learning Hub Workflow Infographic.png`, committed under its real name (spaces URL-encoded). Zone.Identifier sidecar not committed.
- SSOT: workflow document unchanged; no matrix or Mermaid duplicated on Home.

## Evidence
| Check | Result |
| --- | --- |
| `mkdocs build --strict` | PASS |
| Built HTML: tabs lack Development; image and development links resolve in `site/` | PASS |
| Old workflow URL `development/CLH_LEARNING_TO_PUBLISHING_WORKFLOW/` exists in build | PASS (local build); live HTTPS check PENDING |
| `python -m unittest discover -s scripts` | PASS |
| Responsive image | PASS by static check only (Material theme sets `img{max-width:100%}`; click-through gives full-size file). Real viewport rendering NOT RUN |
| Desktop / mobile visual QA | NOT RUN: no browser tooling (no Chromium/Playwright). Manual: open the Pages home at 1280px and 375px widths, confirm tabs list Home + 5 subjects, open the drawer, tap the image and confirm full-size view, tap the workflow link |
| PR CI, Pages deploy, SHA readback | PENDING |

## PR
PENDING

## Commit
Plan 8afc795; implementation see PR.

## Deviations
- The image is 2.25 MB and its filename has spaces; kept as supplied per the Issue (no rename). Image publishing rights are Human-asserted.
- Other Development pages remain outside nav (as before); reachable from Home.

## Unfinished
CI, merge, deployment readback, archive readback, closure.
