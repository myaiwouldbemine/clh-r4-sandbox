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
| Old workflow URL `development/CLH_LEARNING_TO_PUBLISHING_WORKFLOW/` | PASS (local build and live HTTP 200) |
| `python -m unittest discover -s scripts` | PASS |
| Responsive image | PASS by static check only (Material theme sets `img{max-width:100%}`; click-through gives full-size file). Real viewport rendering NOT RUN |
| Desktop / mobile visual QA | NOT RUN: no browser tooling (no Chromium/Playwright). Manual: open the Pages home at 1280px and 375px widths, confirm tabs list Home + 5 subjects, open the drawer, tap the image and confirm full-size view, tap the workflow link |
| PR CI on head 1f67ad2102372123b1d3bbb715482482dd048c73 (base 5920566) | PASS: docs-check, governance-tests |
| Merge | PASS: PR #32 merged with exact head match, merge SHA b3e521bcad080d9d62414da9ed9badb9fccb9527 |
| Pages deployment | PASS: https://github.com/myaiwouldbemine/myaiwouldbemine-Copy-Learning-Hub/actions/runs/42352403237 (applicability, build, deploy, verify success) |
| Remote SHA readback | PASS: workflow verify step read deployed SHA b3e521bcad080d9d62414da9ed9badb9fccb9527 |
| Live HTTPS | PASS: home, canonical workflow URL, image, AUTONOMOUS_OPERATIONS all 200; live home contains How We Learn; live top tabs lack Development |

## PR
https://github.com/myaiwouldbemine/myaiwouldbemine-Copy-Learning-Hub/pull/32

## Commit
Plan 8afc795; reviewed head 1f67ad2102372123b1d3bbb715482482dd048c73; merge b3e521bcad080d9d62414da9ed9badb9fccb9527.

## Deviations
- The image is 2.25 MB and its filename has spaces; kept as supplied per the Issue (no rename). Image publishing rights are Human-asserted.
- Other Development pages remain outside nav (as before); reachable from Home.

## Unfinished
Visual desktop/mobile QA remains NOT RUN. Archive readback and Issue closure follow this archive PR.
