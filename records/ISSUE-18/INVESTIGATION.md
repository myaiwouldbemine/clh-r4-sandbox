# Issue #18 — Read-only Investigation & Risk Assessment

Date: 2026-11-06 (Asia/Taipei). Investigator / accountable Phase 1 Builder: Codex.

## Authority and baseline

- Request: https://github.com/myaiwouldbemine/myaiwouldbemine-Copy-Learning-Hub/issues/18
- Human Phase 1 instruction: https://github.com/myaiwouldbemine/myaiwouldbemine-Copy-Learning-Hub/issues/18#issuecomment-6684903154 (read with Issue body; both restrict work to investigation, Plan and Draft PR).
- Fetched main: `7e530cdc818044ae4f760a021a331f888f993e43`. All repository findings below refer to that immutable baseline, not the initial local branch.
- Current main GOVERNANCE/AGENTS designate Claude Code. The explicit task appoints this Codex session for Phase 1 only; it does not enact tool-neutral governance or grant implementation authority. No prior Issue #18 Builder work/handoff was identified in its body/comment or the open-PR search.
- Original workspace was clean on `issue-11-fix-merge-error-handling`; investigation used main and a separate `codex/issue-18-plan` worktree. No implementation files were edited.

## Findings and evidence

| Source at baseline | Finding | Planned response |
|---|---|---|
| GOVERNANCE.md; AGENTS.md | Claude Code-specific Builder and Fresh-Context evaluator; L0–L3, Plan/Result, Self-Review, separate authorizations already defined | Replace brand-specific responsibility with one designated Builder; preserve safeguards and optional challenge semantics |
| .github/ISSUE_TEMPLATE/01-agent-task.yml | Only form; learning/development title, Claude-only instructions, content-creation example | Engineering Task label and faithful-import engineering examples; preserve IDs `what`, `why`, `acceptance`, `boundary`, `references`, types and required flags `true,true,true,true,false` |
| .github/ISSUE_TEMPLATE/config.yml | Blank issues disabled; comment says one Agent Task form | Comment describes two entries; preserve false |
| .github/PULL_REQUEST_TEMPLATE.md | Builder and evidence fields already exist; no explicit handoff record | Minimal expansion for accountable Builder, handoff SHA/scope/completed/remaining/evidence/blockers and incoming review |
| docs/development/ISSUE_TEMPLATE_INSTALL.md | Describes one form and obsolete opposite-Agent review requirements | Explain both forms, optional learning milestones, current Self-Review and publication boundary |
| README.md §§1, 7, 8 and English summary | Peer/multi-Agent review and教材實作 language; implementation-before-PR diagram; automatic deployment language conflicts with main policy | Targeted role/process/deployment wording and diagram corrections; no learning-content edits or deployment changes |
| .github/workflows/docs-check.yml | PR strict MkDocs build | Preserve and collect head-specific CI |
| .github/workflows/governance-tests.yml | unittest discovery over scripts/test_*.py | Preserve; report actual discovered coverage |
| .github/workflows/pages.yml | workflow_dispatch only, deployment restricted to main | No dispatch or edits; documentation must describe separate deployment authority |
| .github/workflows/merge-and-close-pr.yml | Human allowlist, non-Draft/head/base/check/review gates, linkage, merge/archive/close; manual dispatch | No edits or live E2E in this task; compare exact blob and offline regression evidence |
| scripts/merge_lifecycle.py; scripts/archive_record_builder.py | Linkage uses PR body issue reference, not form field names; archive closure explicitly differs from learning completion | Existing Issues need no migration; no helper changes |
| scripts/verify_plan_records.py; scripts/test_verify_plan_records.py | Verifier requires both Plan and Result; checks first-parent ordering, not approval identity | Do not fabricate Result in Phase 1; use verifier after implementation; record Plan SHA independently |
| scripts/test_merge_error_handling_regression.py and remaining scripts/test_*.py | unittest covers classes; several files use standalone functions/runners; test_final_findings.py also reads old PR #12 and expects historical recovery behavior | Do not claim discovery ran every test; triage applicability before later standalone execution; no historical test rewrites |
| records/ISSUE-9/PLAN.md, RESULT.md | Historical role transition and Plan-publication correction | Evidence only; main is policy; unapproved Plan stays in Records/Draft PR, not an Issue Timeline Plan comment |
| records/ISSUE-11-MERGE-FIX/PLAN.md; records/ISSUE-11/ correction record references; records/ISSUE-13/ARCHIVE-E2E-TEST.md; records/ISSUE-16/ARCHIVE-E2E-REPEAT.md | Prior merge/closure fixes and separately authorized E2E artifacts; some historical instructions differ from main | Preserve historical records; no inherited authorization or repeated live E2E |

Merge workflow baseline Git blob: `9b014e67583818e03442f136b3aedf80f05620fc`.
Archived platform is excluded from active instructions, execution and proposed edits.

## Risk Assessment

Overall candidate: **L3**, retained for Human review because Builder accountability, handoff and authorization interpretation are governance controls even when expressed in Markdown. Not downgraded to a formatting change.

- Role-transition risk: brand substitution could weaken accountability. Mitigation: exactly one named Builder per engineering Issue/PR; identical rules for both tools; explicit incoming head review.
- Authorization risk: handoff could appear to transfer permission. Mitigation: record previous/new Builder, full SHA, base, scope, risk, completed/unfinished work, Evidence and Blockers; revalidate applicable Human authorization without automatic inheritance.
- Learning ownership risk: examples could invite content creation or equate archiving/CI with mastery. Mitigation: ChatGPT + Human own content, quality and final integration; Builder imports only approved content; semantic questions remain PENDING.
- Compatibility risk: form IDs or requirements may break expectations. Mitigation: retain engineering contract and blank-issue setting; optional later learning milestones; no existing Issue migration.
- Verification risk: YAML parse alone is not GitHub schema/UI validation; existing CI has limited discovery coverage. Mitigation: separate structural/schema checks, actual test counts, and post-merge UI readback.
- Scope risk: documentation drift could expand to workflow/platform repairs. Mitigation: eight implementation files only, plus Issue #18 records; stop for revised approval if more is needed.
- Remaining uncertainty: actual GitHub form rendering is unavailable before publication; remote settings/branch protection were not audited and must not be claimed enforced; later head/base changes invalidate this baseline assessment as needed.

## Executed verification (baseline, not implementation acceptance)

- PASS: `python3 -m unittest discover -s scripts -p 'test_*.py'` — 27 tests, exit 0.
- PASS: `python3 scripts/test_merge_lifecycle.py` — 3 groups, reported 6 linkage + 7 deduplication + 3 integration cases, exit 0.
- PASS: read Issue body and its one comment; fetched main; inspected source inventory and relevant records/scripts/tests; open PR search for Issue #18 returned none.
- NOT RUN: new-form YAML/schema validation (form does not exist yet); strict MkDocs local build; other standalone test runners; browser/visual validation; full Plan+Result verifier.
- PENDING: Draft PR remote CI and readback at report-writing time; final Phase 1 PR evidence will bind actual head SHA.
- Content: no V2/V3 authored, imported or accepted. Provenance: repository and Human request references above, not a教材來源驗收. Visual: NOT RUN. Deployment/live merge/closure: NOT RUN, not authorized.

## Fresh-Context Challenge

Omitted for this records-only Phase 1: no implementation is authorized, source/boundary checks are direct and Human reviews the fixed Plan before proceeding. This is Codex Self-Review, not independent Review or a claim that Claude Code evaluated it. Reassess challenge necessity before later L3 implementation verification; any Human-mandated challenge is mandatory. No subagent or governance platform was introduced.

## Additional requirement — v1.1 investigation supplement

Re-read updated Issue #18 body (updated_at 2026-11-06T12:38:44Z) and Human chat instruction. Completed tracked-file inventory, full active operating-document read and keyword audit; see [Documentation Consistency Matrix](DOCUMENTATION-CONSISTENCY.md) and [baseline matches](MATCHES.txt). Newly identified INSTALL.md requires minimal correction; planned scope expands from eight to nine files, still L3 candidate and unapproved. Three docs/development files are explicitly ARCHIVED / NOT ACTIVE and will remain byte-identical, as will historical records/merged PR evidence. Earlier eight-file description records the initial investigation; Plan v1.1 supersedes its scope count.

Additional phase changes are records only. No production docs/templates have been modified. Existing baseline tests remain relevant to unchanged code; the new Plan head requires renewed records-only Self-Review and remote CI readback.
