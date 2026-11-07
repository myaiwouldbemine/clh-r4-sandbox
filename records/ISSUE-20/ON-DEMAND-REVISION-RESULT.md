# On-demand Revision Results

Issue: https://github.com/myaiwouldbemine/myaiwouldbemine-Copy-Learning-Hub/issues/20
PR: https://github.com/myaiwouldbemine/myaiwouldbemine-Copy-Learning-Hub/pull/21
Date: 2026-11-07 Asia/Taipei. Accountable Builder: Codex.

**Implementation and applicable local verification complete; full live lifecycle acceptance BLOCKED. Keep Draft/open. No Merge, Deploy or Close performed.**

## Commit order

- Revision start: `bb577319ba003f3b92ef4fc7cf0cd717e8315cac`.
- Audit + Plan independently committed/pushed: `51b1c2927b85d7546e59e882f8f46f0e651c75d9`. GitHub Plan content bytes and PR head read back before implementation.
- Implementation: `90643309cc87978b7720cdb629f31ed95c7c7c0b`.
- Verifier heading compatibility: `c37275eb05dd80574fd482b3a9a9fc7ee1db66ed` (current reviewed implementation).
- Base/main: `7e530cdc818044ae4f760a021a331f888f993e43`.
- This Result/evidence commit follows implementation; its full final SHA and current-head CI/readback go in PR #21, avoiding circular self-SHA claims.

## Implementation Summary / Results

Hosted Issue Agent and periodic lifecycle are inert manual-only, skipped workflows; no model action or token references. Historical publisher library and six regressions remain, but publisher CLI is blocked. The broad reconcile CLI is removed. Local check/run requires explicit repository, PR and full expected head/base; shared Git-directory OS lock serializes local worktrees. Read-only check has no GitHub mutation.

Preserved protection/CI/thread/Issue gates and exact-head merge. Added revalidation after Ready and before archive/closure, plus fresh remote deployment SHA verification rather than accepting comments alone. Pages is explicit main-only dispatch with expected merge SHA, native token/OIDC, strict build, serialized deployment and bounded readback. Existing login works for reads and actual branch publication; no credentials, activation flags, services or settings were added.

Updated operational docs and both languages of AGENTS clauses 01/14; all 15 pairs preserved. Added named revision Plan/Result verification, safety and recovery tests. No educational content changed. Human remains administrator/content owner; Builder performs normal lifecycle without per-step approvals when task scope permits it.

## Changed Files

18 implementation paths:

- `.github/ISSUE_TEMPLATE/01-agent-task.yml`, `.github/PULL_REQUEST_TEMPLATE.md`, `.github/prompts/engineering.md`
- `.github/workflows/issue-agent.yml`, `.github/workflows/merge-and-close-pr.yml`, `.github/workflows/pages.yml`
- `AGENTS.md`, `GOVERNANCE.md`, `INSTALL.md`, `README.md`
- `docs/development/AUTONOMOUS_OPERATIONS.md`, `docs/development/ISSUE_TEMPLATE_INSTALL.md`
- `scripts/agent_job.py`, `scripts/autonomous_lifecycle.py`, `scripts/verify_plan_records.py`
- `scripts/test_autonomous_lifecycle.py`, `scripts/test_verify_plan_records.py`, new `scripts/test_on_demand.py`

New revision-only records: AUDIT, PLAN, RESULT, SELF-REVIEW, E2E, EVIDENCE.json, TESTS.txt, BUILD.txt, LINT.txt with ON-DEMAND-REVISION prefix. Original records untouched. Full changed-file list also in EVIDENCE.json.

## Evidence / Test Results

| Surface | Status and scope |
|---|---|
| Original baseline | 53 tests freshly PASS before editing; historical count not reused for acceptance |
| New unittest discovery | **68 PASS**, all original 53 retained (one deployment case explicitly mocks newly required remote readback), 15 new tests |
| Standalone legacy runners | merge_lifecycle, two_defects_fix, human_review_corrections, runtime_cleanup exit 0; simulations/historical helper evidence only |
| Obsolete final_findings runner | **FAIL**, 2 old workflow authorization/concurrency assertions; same two assertions fail on pre-revision workflow. Third reads unrelated historical PR #12. Not an applicable gate; preserved without rewriting to green |
| Strict MkDocs | PASS, operational docs built; excluded-from-nav INFO is not a strict warning |
| actionlint 1.7.12 / diff check | PASS, no lint suppression |
| Plan/Result ordering | Named revision verifier executed after this Result commit; final outcome in PR/readback supplement |
| Historical records / archive | 41 previously existing tracked files byte-identical; #19 unchanged at `7efb0521d63b646501b83ecafdfb40da473d914b` |
| AGENTS bilingual structure | 15 complete pairs PASS; semantic Self-Review in separate record |
| Real GitHub read-only | Existing login, settings, protection preflight PASS; incomplete PR gate correctly BLOCKED before mutation |
| Real branch publish | Plan and implementation normal push/readback PASS; no main push/force |
| GitHub CI | Implementation runs created: Governance 42313060669, Docs 42313060701. Final-head CI is separately checked and linked in PR; these are not final-head evidence |
| Live Ready/Merge/Deploy/Archive→Close | NOT RUN; overall live lifecycle acceptance BLOCKED |

Separate categories: build PASS; educational content/provenance unchanged (no semantic quality approval); browser/visual NOT RUN; deployment NOT RUN. Full logs: ON-DEMAND-REVISION-TESTS/BUILD/LINT and EVIDENCE.json. See E2E matrix for real versus injected evidence.

## Deviations / Findings corrected

- Literal `if: false` in tombstones caused actionlint's constant-condition warning. Use the only allowed trigger (`workflow_dispatch`) with the opposite event predicate so jobs are skipped without lint suppression. No other trigger exists.
- Named revision Plan uses “E2E Acceptance” as its acceptance heading. The verifier now recognizes that explicit synonym for named revisions only, tests missing-heading rejection and retains original strict default contract. Original Plan bytes and actual commit order were not altered.
- Probed legacy standalone runners beyond discovery; preserved the preexisting obsolete FAIL result rather than presenting all historical scripts as passing. Replacement behavior is exercised by the applicable local lifecycle tests.

## Risks / Unfinished / Blockers

Full positive lifecycle cannot be demonstrated under this request's explicit no-Merge/no-Deploy/no-Close boundary; candidate workflow also remains off main. Missing model/automation secrets are **not** a blocker for this local design. Existing permissions have not been proven by an actual merge or deployment. No new fixture repo/settings or credential was provisioned to evade the boundary.

OS lock requires WSL/Linux and is not distributed; single Builder responsibility still applies across machines. REST merge lacks atomic expected-base CAS; fresh reads/native strict checks mitigate but cannot prove an indivisible review-to-merge transaction. Issue comments/stop requests require Builder reading; body digest is not semantic verification. If main advances before old-SHA deployment, block and investigate current reviewed recovery instead of crediting unrelated content. Remote deployment may change after readback; no cross-service transaction is claimed.

Rollback procedure is documented and history preserved; actual revert PR/deployment is NOT RUN because production has not changed. Emergency stop means stop local operations and inspect/cancel relevant pending jobs, not remove protection. Required future evidence: real Ready/exact-SHA merge, actual Pages job + SHA readback, archive readback before closure and live negative/recovery scenarios within a permitted lifecycle task.
