# Issue #18 — Learning Issue Forms + Tool-Neutral Single-Builder

Version: **v1.1** · Date: 2026-11-06 (Asia/Taipei)
Status: **DRAFT — PENDING HUMAN PLAN APPROVAL AND SEPARATE IMPLEMENTATION AUTHORIZATION**
Issue: https://github.com/myaiwouldbemine/myaiwouldbemine-Copy-Learning-Hub/issues/18
Phase 1 authority: https://github.com/myaiwouldbemine/myaiwouldbemine-Copy-Learning-Hub/issues/18#issuecomment-6684903154
Accountable Phase 1 Builder: **Codex**. Phase 2 Builder: proposed Codex, requires explicit designation/authorization; no automatic handoff or inherited authority.
Base: `main @ 7e530cdc818044ae4f760a021a331f888f993e43`.
Read-only report and risk evidence: [INVESTIGATION.md](INVESTIGATION.md).
Documentation audit: [Documentation Consistency Matrix](DOCUMENTATION-CONSISTENCY.md), with baseline line matches in [MATCHES.txt](MATCHES.txt). Latest Issue body re-read after Human additional requirement (updated_at 2026-11-06T12:38:44Z).
This Plan's full immutable commit SHA will be supplied in the Draft PR and final handoff after its independent commit. No implementation is included in that commit.

## Goal

Provide Learning Record and Engineering Task entry points, and adopt **Tool-Neutral Single-Builder + Self-Verification** with one accountable Claude Code or Codex Builder at any time per engineering Issue/PR. Preserve existing risk, review, evidence and operation boundaries.

## WHY

Current intake conflates learning and engineering and hardcodes Claude Code; README/install instructions contradict current main policy. ChatGPT + Human own V2/V3 learning, material creation, quality acceptance and integrated final content. GitHub stores approved material, versions and learning history. MkDocs provides reading/search/navigation/display. Engineering Builder handles faithful import and engineering verification. V2/V3: **製作時分開、定稿時合併、網站上依主題呈現**.

## Scope

Only after Human approval of this fixed Plan and specific implementation authorization:

| File | Exact proposed change |
|---|---|
| `.github/ISSUE_TEMPLATE/02-learning-record.yml` (new) | Learning Record, required initial subject/course/unit, objectives and source description (sources may honestly say pending); optional V2, V3, quality/evidence, integration and publication/archive references; explicit comment-based progression and author/engineering boundaries |
| `.github/ISSUE_TEMPLATE/01-agent-task.yml` | Engineering Task name/description/instructions/examples; no tool-specific default; preserve five textarea IDs/order and required flags; describe engineering or faithful approved-content import, not material creation |
| `.github/ISSUE_TEMPLATE/config.yml` | Comment-only adjustment for two forms; retain `blank_issues_enabled: false` |
| `GOVERNANCE.md` | Tool-neutral single accountable Builder, same L0–L3/verification rules, responsibility separation, explicit handoff and no automatic permission/review transfer; optional challenge evaluated by designated Builder |
| `AGENTS.md` | Mirror that policy concisely; preserve main-policy precedence, records and authorization gates |
| `.github/PULL_REQUEST_TEMPLATE.md` | Expand existing Builder field and add optional handoff details plus incoming current-head Self-Review/base/scope/risk/authorization reassessment |
| `docs/development/ISSUE_TEMPLATE_INSTALL.md` | Two entry points, contracts, creation vs comments, schema vs post-merge UI evidence; remove obsolete mandatory opposite-Agent review |
| `INSTALL.md` | Correct stale v1.1/peer-Agent package and copy-before-approval instructions; align current main/Issue/Draft/Plan and specific L3 authority; preserve vendor compatibility section and no-main-push guidance; no settings provisioning |
| `README.md` | Necessary role/process paragraphs including Issue-first and complete Merge conditions, workflow diagram/summary and manual/separately authorized deployment wording; explain V2/V3 division/integration and archive vs mastery; leave unrelated roadmap/status history alone |

`records/ISSUE-18/` may contain Plan revisions, verification evidence and post-implementation RESULT.md. No new scripts/tests/dependencies/workflows are proposed; use existing tools and one-off checks with evidence. Any need for additional production paths requires a revised Plan and renewed applicable approval.

### Proposed Learning Record contract

| ID | Meaning | Required at creation |
|---|---|---|
| `subject-course-unit` | Subject / Course / Unit | true |
| `learning-objectives` | Learning Objectives | true |
| `source-materials` | Source Materials; honest unknown/pending allowed | true |
| `v2-consolidation` | V2 Knowledge Consolidation progress/reference | false |
| `v3-code-first` | V3 Code-First Deep Dive progress/reference | false |
| `content-quality-evidence` | Human/ChatGPT quality acceptance and evidence | false |
| `v2-v3-integration` | Integrated final version/reference | false |
| `publication-archive` | Publication / Archive / PR references | false |

Use simple textareas and markdown guidance. No prefilled successful results, mandatory completed milestones, automatic assignment, dispatch or new labels. Later comments can identify milestone, current state, source/version, actual evidence and next step; submitting a form never asserts completion or grants authority.

### Proposed accountability / handoff contract

Record designated Builder explicitly in engineering Issue/PR. Handoff records previous and incoming Builder, full handoff commit SHA, base, scope, risk, completed and unfinished work, evidence links/status and blockers. Incoming Builder rechecks current-head Self-Review and evidence freshness, assesses base/scope/risk changes and confirms applicable Human authorization; previous review conclusions and authorizations never automatically transfer with the tool. Existing evidence may be inspected as sources, not assumed valid. No registry, attestation, trusted identity mechanism, parallel accountable Builders or mandatory cross-review.

## Boundary

Phase 1 changes only this Plan and investigation records on a branch, commits them and opens a Draft PR. STOP after reporting SHA/URL/scope. Do not post an unapproved Plan to the Issue Timeline; main policy allows only an approved Plan there, with version/SHA/Records/scope/approval reference and remote readback.

Implementation is NOT authorized. No V2/V3 authorship, derivation or semantic editing; semantic questions go PENDING to ChatGPT/Human. CI PASS, PR Merge and Issue Closed do not establish content quality or mastery. No direct main push, force push, Auto-Merge, workflow dispatch, merge/closure/deploy, settings/permission changes, archived platform changes or new infrastructure. All `.github/workflows/`, existing scripts/tests and historical records stay unchanged. Draft status never grants work or merge authority.

## Risk Level

**L3 candidate, handled with L3 gates**: governance/accountability/authorization semantics. See investigation risk assessment. Nine implementation files form the proposed action scope. Human must approve the fixed Plan and separately authorize those edits with an accountable Builder before they begin. Existing main is the sole active repository policy until an authorized change; this Plan is not policy.

## Implementation Plan

1. Phase 1: preserve read-only findings, independently commit Plan and report (v1.0 already independently committed; v1.1 adds audit and scope clarification); open Draft PR to main, record SHA and actual verification. Stop for Human.
2. After explicit Plan approval and implementation authorization: fetch main/current head, reassess changes against this baseline, confirm one Builder and record approval references. If scope/risk/base changes materially, revise Plan in a new commit and obtain renewed authorization before dependent work.
3. Publish only the approved Plan to the Issue Timeline with fixed SHA, version, records link, scope and Human approval reference; read back both sources and record consistency.
4. Implement the nine scoped files, preserving engineering field contract and all workflow/helper bytes. Keep learning fields honest and optional after initial information. Review role/authority wording across all nine files.
5. Execute applicable checks below, resolve failures within scope or report blockers. Do not repair unrelated historical tests/workflow under this authorization.
6. Write `records/ISSUE-18/RESULT.md` after implementation with Results, Evidence, PR, full Commit, Deviations and Unfinished; preserve chronological Plan history. Bind final-head Self-Review in PR after any evidence/Result commit.
7. Keep Draft until implementation, applicable verification and Result are complete and PR-status authority is confirmed. Human Merge authorization is separate and must identify the actual candidate. Deployment and any live merge/closure E2E need separate scope/authority. This Plan grants none.

## Acceptance Criteria

- Two named forms, distinct purpose; all nine Learning Record topics, only initial information mandatory; milestones can be updated in comments without fabricated evidence.
- Engineering IDs/types/order/required flags remain compatible; existing Issues need no migration and PR-to-Issue linkage remains supported.
- Documentation Consistency Matrix covers current operating documents and records per-hit disposition/rationale; preserve archived documents even outside archive/, all historical records and merged PR evidence. Repeat audit at final head.
- All nine files consistently define content ownership and exactly one tool-neutral accountable Builder; identical risk/evidence/Self-Review/authorization rules.
- Handoff records all required fields; incoming current-head review and base/scope/risk/authorization reassessment are explicit.
- No CI/mastery conflation, implicit merge/deploy permission or archived-platform activation.
- YAML/schema checks, applicable tests, strict MkDocs and head-specific CI succeed; workflow/helper/history preservation confirmed.
- Plan commit predates implementation; explicit Human approval/implementation authority precede edits; Result follows implementation; final Self-Review binds full head and relevant base/scope.
- Actual GitHub New Issue chooser/forms readback is **PENDING until authorized merge**. Pre-merge schema acceptance does not claim UI completion; this explicitly post-merge criterion is not a substitute for missing pre-merge checks. Any publication failure keeps acceptance unresolved and requires a scoped fix.

## Verification Strategy

All implementation checks below are **NOT RUN** in Phase 1 unless explicitly identified as baseline evidence in INVESTIGATION.md. Future external/head-specific checks are **PENDING**. No unexecuted PASS claims.

| Check | Method / required evidence |
|---|---|
| YAML and GitHub schema | Parse both YAML files/config; compare supported top-level/body keys, IDs, labels/types, booleans and uniqueness against official Issue Forms and form-schema docs; record commands/tool versions and results. YAML parsing alone is insufficient |
| Two intake contracts | Inspect both definitions, required/optional matrix and no fabricated defaults; preserve exactly engineering `what/why/acceptance/boundary/references` flags T/T/T/T/F; retain blank issue setting |
| Documentation consistency | Repeat tracked-file inventory and keyword/semantic audit from DOCUMENTATION-CONSISTENCY.md; reconcile every MODIFY row and verify KEEP/PRESERVE paths unchanged; exclude historical evidence from policy rewrites |
| Tool-neutral roles and ownership | Read and search nine scoped files for Claude/Codex/Builder/review/deployment language; assess semantics, not blind brand replacement; verify ChatGPT+Human content boundary |
| Handoff | Tabletop both Claude→Codex and Codex→Claude; new head, changed base/scope/risk and missing authorization cases must require reassessment, not inherited approval |
| Existing Issue compatibility | Compare engineering contract against fixed base; exercise existing linkage helper with non-closing `Issue: #18` reference; no edits/migration of existing Issue bodies |
| Workflow preservation | `git diff 7e530cdc818044ae4f760a021a331f888f993e43 HEAD -- .github/workflows scripts archive` must be empty; verify merge workflow blob remains `9b014e67583818e03442f136b3aedf80f05620fc`; no live dispatch |
| Existing tests | `python3 -m unittest discover -s scripts -p 'test_*.py'`; `python3 scripts/test_merge_lifecycle.py`; assess other standalone runners individually for current-scope relevance; report omitted historical PR/recovery checks and limitations, never call all tests passed from discovery alone |
| Website/build | `python -m mkdocs build --strict` using requirements.txt environment; `git diff --check`; inspect changed documentation rendering separately if feasible; build success is not content or visual acceptance |
| Records/order | Phase 1: required Plan headings, records-only diff and independent commit. After implementation/Result: `python3 scripts/verify_plan_records.py 7e530cdc818044ae4f760a021a331f888f993e43 HEAD 18 3 --formal-plan`; separately verify approval references (verifier cannot authenticate them) |
| Remote CI/readback | Capture `docs-check`/`governance-tests` run URLs and actual head, compare PR base/head/draft and file scope; pending/failed/stale required checks block readiness/merge |
| Post-merge UI | After separately authorized merge, read actual chooser and both rendered forms, required flags and milestone instructions without creating fake learning records. PENDING before publication |

Official references (consulted 2026-11-06; recheck before implementation):
- https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-issue-forms
- https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-githubs-form-schema

Report build, content, provenance, visual and deployment separately. No content import is proposed, so no material-quality acceptance claim. Fresh-Context Challenge omitted in Phase 1 for reasons in INVESTIGATION.md; reassess during implementation; Human-mandated challenge cannot be skipped. No mandatory independent/native APPROVED review is added.

## Human Decisions

| Decision | Current status / exact scope |
|---|---|
| Phase 1 investigation, records commit and Draft PR | AUTHORIZED by linked Human task only |
| Plan v1.1 approval at reported immutable SHA | PENDING — review this Plan and investigation |
| L3 implementation action/scope | NOT AUTHORIZED — separately designate one Builder and authorize nine scoped files plus Issue #18 Result/evidence; clarify any requested changes via Plan revision |
| Ready transition | NOT AUTHORIZED by Phase 1; confirm later task boundary after verification |
| Merge / Close Issue #18 | NOT AUTHORIZED; separate operation decision for final candidate and applicable conditions |
| Deployment / live E2E | NOT AUTHORIZED; outside implementation scope |

Remaining risks for Human: documentation-only role rules cannot automatically verify agent identity or enforce permission; schema checks cannot prove unpublished GitHub UI; stale README wording must be corrected without general redesign; existing test discovery is incomplete for standalone runners; base/head evolution requires renewed assessment. Unknowns block dependent work, not invented success.

Rollback, if later needed: separately authorized revert PR for scoped implementation changes with applicable checks; preserve Plan/Result and Git history. No reset/force push or emergency operation is authorized here.

## Revision History

| Version | Date | Change | Authorization |
|---|---|---|---|
| v1.0 | 2026-11-06 | Initial pre-implementation Plan and main-baseline investigation; records-only independent commit | Phase 1 only; Plan approval and implementation PENDING |
| v1.1 | 2026-11-06 | Human requested repository-wide current documentation audit; re-read updated Issue; add consistency matrix/search evidence and INSTALL.md to bounded scope; v1.0 remains at efe0fedf7490781f53e6467dfc4b848cafbd37fb | Phase 1 only; revised Plan and implementation PENDING |
