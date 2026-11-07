# Issue 27 plan — Learning-to-Publishing workflow documentation

Issue: https://github.com/myaiwouldbemine/myaiwouldbemine-Copy-Learning-Hub/issues/27
Accountable Builder: Claude Code (sole). Base: b4d9d74 (main).

## Goal
Document the confirmed Learning-to-Publishing workflow, roles and the two independent Issue lifecycles in `README.md`, and move `RAW_DATA/README.md` to the ORIGINAL/GENERATED layout.

## Why
The root README lacks the operating sequence, role split and lifecycle relationship; RAW_DATA README still describes the old single-layer layout. Documenting them avoids repeated discussion and responsibility confusion.

## Scope (documentation only)
- `README.md`: new section "Learning-to-Publishing Workflow｜教材製作與發布流程" with Phases A–D, a full Mermaid flowchart, a role-responsibility matrix, and a Mermaid diagram of the Learning Record and Engineering Task lifecycles (one-to-many, independent closure). Existing sections are kept; only section numbers after the insertion shift, and the stable explicit anchor `#learning-to-publishing-workflow` is added. Repository-structure example gains RAW_DATA, records, RELEARNING_SUPPLEMENTS. LEC08 case: Learning #26 / Engineering #24 / PR #25.
- `RAW_DATA/README.md`: `RAW_DATA/<subject>/<unit>/ORIGINAL|GENERATED/`, read-only, SHA-256, versioning, licence, Git exclusion, local backup, relative link to the root README workflow section; existing rules preserved.
- `records/ISSUE-27/` Plan and Result.

## Boundary
Documentation only. Must not commit RAW_DATA PDFs or ZIPs, push main directly, bypass protections, or present Draft engineering success as learning completion.

## Out of scope
GOVERNANCE.md, AGENTS.md, CI, lifecycle scripts, Issue templates, teaching content semantics, any RAW_DATA PDF/ZIP commit. `.gitignore` already excludes `/RAW_DATA/**` except its README, so no change.

## Implementation plan
1. Commit this Plan alone.
2. Edit the two READMEs.
3. Verify: `git diff --check`, link/anchor check, `mkdocs build --strict`, unit tests, `verify_plan_records`, Mermaid syntax check if a renderer is available (else NOT RUN, with GitHub rendering checked on the PR), `git ls-files RAW_DATA`.
4. Draft PR, Result, Self-Review block, Ready, gated merge, Pages run and SHA readback, archive and readback, close.

## Acceptance criteria
The Issue 27 acceptance criteria: README phases A-D with full Mermaid flowchart; role matrix; Learning Record and Engineering Task lifecycle diagram with one-to-many relation; RAW_DATA/README ORIGINAL/GENERATED with a valid link to the root workflow section; existing README content preserved; diff check, link check, strict MkDocs and required CI PASS; protected PR, Pages SHA readback, archive and closure.

## Verification strategy
Each criterion reported separately as PASS/FAIL/BLOCKED/PENDING/NOT RUN. README is not part of the MkDocs site, so MkDocs only proves the build is unaffected; GitHub Mermaid rendering is checked separately.

## Revision history
- r0: initial plan (rebuilt on a new branch after the first draft lacked required headings; PR #28 superseded).

## Supplement r1 — Single Source of Truth document (Human-directed, same Issue)
Human placed `docs/development/CLH_LEARNING_TO_PUBLISHING_WORKFLOW.md` (SSOT) and asked that Issue 27 be integrated around it. Why: avoid duplicating diagrams in two places.

### Differences from Issue 27 acceptance criteria, recorded before implementation
| Issue 27 text | Supplement | Handling without relaxing the criterion |
| --- | --- | --- |
| README has Phases A-D, full Mermaid flowchart, role matrix, lifecycle diagram | README keeps a brief summary and a link; diagrams live in the SSOT | The content requirements are met by the SSOT, which is published in MkDocs nav; README summarizes Phases A-D and links. Reported as a literal-location deviation |
| Scope: only README.md, RAW_DATA/README.md, records | Also adds the SSOT file and a mkdocs.yml nav entry | Human-authorized addition; recorded here and in Result. No GOVERNANCE, AGENTS, CI, scripts or template changes |
| RAW_DATA link to root README section | Link to the SSOT | Both kept: RAW_DATA/README links to the SSOT and to the README summary anchor |
| Issue state | Issue 27 was already closed | Reopened for this supplement (no new Issue); re-closed after merge, deployment and archive readback |

### Steps
1. Commit this Plan revision alone.
2. Import the SSOT byte-identical (Zone.Identifier sidecar excluded), shorten README section 7 (keep anchor), update RAW_DATA/README links, add nav entry.
3. Verify relative links and Mermaid syntax across the three Markdown files, `git diff --check`, strict MkDocs, unit tests, verify_plan_records, `git ls-files RAW_DATA`.
4. Draft PR, Result update, Self-Review, Ready, lifecycle merge, Pages SHA readback, archive, close.
- r1: added supplement and difference table.
