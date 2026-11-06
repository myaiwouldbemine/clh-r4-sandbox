# On-Demand Architecture Revision Plan

Version 1; 2026-11-07 Asia/Taipei. Single accountable Builder: Codex.
Issue: https://github.com/myaiwouldbemine/myaiwouldbemine-Copy-Learning-Hub/issues/20
PR: https://github.com/myaiwouldbemine/myaiwouldbemine-Copy-Learning-Hub/pull/21
Source decision: https://github.com/myaiwouldbemine/myaiwouldbemine-Copy-Learning-Hub/pull/21#issuecomment-6698471618
Audit: ON-DEMAND-REVISION-AUDIT.md. Revision starting head `bb577319ba003f3b92ef4fc7cf0cd717e8315cac`; base `7e530cdc818044ae4f760a021a331f888f993e43`.

## 1. WHAT / WHY / DONE (Goal)

Replace unattended engineering with on-demand local Codex engineering. Human + ChatGPT plan content and create Issues; Human starts Codex when needed. Builder autonomously performs engineering, PR, gates and applicable lifecycle; no routine Human merge or repeated approval. DONE: no normal OPENAI_API_KEY/CLH_AUTOMATION_TOKEN dependency, inactive hosted agent/scheduler, retained native gates and history, local targeted/recoverable executor, native Pages dispatch/readback, tests and candid revision records. Complete live lifecycle is a separate unmet acceptance item while this request forbids Merge/Deploy/Close.

## 2. Current Architecture

Issue events/failed CI → hosted Codex action → bundle publisher; workflow completion/15-minute schedule → lifecycle reconciliation → Ready/merge → main-push Pages → deployment marker → archive/close. Activation/secrets absent; never enabled. Main protection exists, old 53 tests now re-run PASS, deployed site not demonstrated. Read audit matrix for each component.

## 3. Proposed Architecture

Active local session reads latest Issue/comments/PR/records, records one Builder, commits formal Plan then implementation and Result, pushes branch and maintains Draft. Required GitHub CI runs. After actual evidence is complete, Builder records full reviewed head/base/scope in PR and calls explicit local check/run for one PR. Executor revalidates and uses SHA-bound merge, then waits for applicable deployment. Builder dispatches Pages on main for exact merge SHA, observes run and remote bytes, then resumes executor to archive/readback/close. App off means no new engineering or lifecycle reconciliation; submitted CI/Pages jobs can finish, and the next session resumes from remote state.

## 4. Architecture Comparison

| Option | Credentials / availability | Decision |
|---|---|---|
| Local Codex App + existing gh | Existing model session plus existing GitHub login; active session only | Chosen; smallest change, no new secrets |
| Manually triggered hosted model | API key + transport still required | Rejected; no benefit for stated need |
| Hosted merge with native token | Possible permissions, event recursion and orchestration obligations | Not chosen; retain native token only for CI/Pages |
| Always-on hosted agent | Model/transport keys and off-device scheduling | Disabled per Human decision |

## 5. Component Migration Matrix

Audit table is normative migration matrix: KEEP native CI/protection, archives/content/history; MODIFY lifecycle/Pages/retry/docs; DISABLE hosted Issue Agent, scheduler and publisher CLI; REMOVE active secret/activation dependencies and broad reconciliation CLI. Preserve helper code/tests where useful, clearly label legacy, not active runtime.

## 6. Exact File Change List / Scope / Boundary

- `.github/workflows/issue-agent.yml`, `merge-and-close-pr.yml`: inert manual-only skipped tombstones, no credentials or mutation.
- `.github/workflows/pages.yml`: dispatch-only main/exact-SHA checks, keep strict build/artifact/OIDC/deploy/readback.
- `scripts/autonomous_lifecycle.py`: explicit check/run/expected-head/base, local lock, post-Ready revalidation, fresh remote readback, recovery checks; retain low-level gates.
- `scripts/agent_job.py`, `.github/prompts/engineering.md`: mark legacy; block hosted CLI entrypoint.
- `scripts/verify_plan_records.py`, `scripts/test_verify_plan_records.py`: support named revision Plan/Result and revision start; preserve existing default behavior.
- `scripts/test_autonomous_lifecycle.py`: adapt deployment test to explicit mocked remote bytes, add relevant safety regressions.
- `scripts/test_on_demand.py` (new): read-only target, lock, stale inputs, CLI and workflow contract/recovery tests.
- `GOVERNANCE.md`, `AGENTS.md`, `README.md`, `INSTALL.md`, `docs/development/AUTONOMOUS_OPERATIONS.md`, `docs/development/ISSUE_TEMPLATE_INSTALL.md`, `.github/ISSUE_TEMPLATE/01-agent-task.yml`, `.github/PULL_REQUEST_TEMPLATE.md`: consistent on-demand startup/credentials/lifecycle; preserve full 15 ZH/EN AGENTS pairs and all safeguards.
- New records only: `records/ISSUE-20/ON-DEMAND-REVISION-{AUDIT,PLAN,RESULT,SELF-REVIEW,E2E}.md`, `ON-DEMAND-REVISION-EVIDENCE.json`, `ON-DEMAND-REVISION-TESTS.txt`, `ON-DEMAND-REVISION-BUILD.txt`, `ON-DEMAND-REVISION-LINT.txt` and append-only supplemental revision records if needed.
- Existing `docs-check.yml`, `governance-tests.yml`, all 53 baseline test cases (apart from necessary explicit mock adaptation), historical records/archive and #19 branch remain intact.

Continue PR #21: same Issue and accountable Builder, no technical reason for another PR. No main push, force/rebase/history rewrite, settings changes, activation, unrelated content, new service, new token, Merge/Deploy/Close in this revision.

## 7. Credentials and Permission Model

Codex model uses existing App session; GitHub uses existing gh authentication in the same shell. Verify via read-only calls and normal Plan push, never print/copy credential contents. Current gh account and read APIs observed working; do not equate App sign-in with GitHub authorization. Local API denial blocks operation, no permission escalation. Existing repo/workflow OAuth scopes observed; actual merge remains untested. CI contents:read. Pages native GITHUB_TOKEN plus OIDC pages:write/id-token:write only deployment job; evidence job issues:write. No OPENAI_API_KEY, CLH_AUTOMATION_TOKEN or CLH_AUTONOMY_ENABLED prerequisite. No new installs for model/transport.

## 8. GitHub CI / Merge / Deployment Lifecycle

Keep strict docs-check/governance-tests and full Self-Review. Local read-only check never marks Ready; run requires explicit PR + expected head/base, complete evidence and no blockers. Refresh PR, Issue, main and checks before irreversible merge, exact head in API, native strict protection final authority. Missing/failing/pending/skipped/cancelled checks fail closed. Pages dispatch accepts expected merge SHA only on main, validates merged PR applicability; no automatic push deployment. Verify successful correct workflow/run/main SHA and actual remote deployment-sha.txt; archive exact data then readback before Issue close. No auto-close keywords. Normal Builder issues commands autonomously; command arguments are race guards, not approval tokens.

## 9. Race Conditions and Failure Handling

Non-force push rejects concurrent branch change. New head/base/scope requires fresh review/testing. Serialize local execution using repository common Git-dir advisory lock (WSL/Linux supported); crash releases lock, no stale lock deletion. One Builder across machines is an operational requirement; no distributed governance platform. Stop on lock conflict. Revalidate after Ready; unknown API outcome requires readback before retry. Reuse remote merged SHA and archive marker; no duplicate merge. If main advanced before dispatch, stop rather than publish unrelated content. If Pages changed before closure, block. Hash Issue body and compare PR evidence before closing; comments still require Builder semantic review. Up to three repair attempts for unchanged failure, recorded with cause/action/outcome; repeated failure stays BLOCKED. REST has no atomic base CAS: retain strict checks, disclose residual server boundary. Archive/close cross-machine races are not solved by a local lock.

## 10. Test Plan / Verification Strategy / E2E Acceptance

Fresh baseline 53 already PASS. Re-run all discovery tests; extend actual functions for missing/failed/pending CI, stale head/base after Ready, permission failure, duplicate/resume, archive mismatch/close denial, remote deployment mismatch. Test explicit CLI targeting and lock release/conflict; record mocks as unit tests. Run standalone legacy runners separately with applicability notes, strict MkDocs, actionlint and diff check. Verify named revision Plan precedes any implementation, Result follows, and all old record bytes unchanged. Verify all 15 bilingual pairs structurally and semantically.

Live within scope: Plan commit/push/readback, GitHub settings/preflight, read-only incomplete PR gate, new-head GitHub CI and final record readback. Do not inject unsafe production mutations to demonstrate denial. Full live negative merge races/permission failure, Ready/merge/Pages/archive/close/revert cannot be claimed from mocks. Report Local PASS, GitHub CI PASS, Live read-only PASS separately; full Live E2E BLOCKED/NOT RUN, keep Draft. No complete=true block for PR #21.

## 11. Rollback Plan

Before merge, stop this session and preserve pushed work; no production change occurred. After future installation, stop local lifecycle, cancel affected pending Pages runs, use tested revert PR + required CI/self-review and normal exact-SHA merge. Redeploy revert SHA and read back when applicable. Do not resurrect hosted workflows or premature close path; settings are not reverted by Git. Keep Issues open until recovery is verified.

## 12. Historical Evidence Preservation

Never overwrite original AUDIT/PLAN/RESULT/SELF-REVIEW/E2E or prior logs, #18/#19 history, archive. New named revision records and normal descendant commits only. Snapshot current PR description for traceability if replacing it; old body also remains in prior evidence/Issue comment. SHA binds every result; final record commit's own review/CI lives in PR to avoid circular self-SHA.

## 13. Risks / Blockers / Open Questions

Full deployment E2E blocked by explicit no-Merge/no-Deploy boundary and candidate absent from main, not missing API keys. Current model session works; unattended availability neither promised nor needed. Local lock is WSL/Linux, native Windows port not in scope. Native GitHub enforcement and account access may change and must be reread. No assumption that successful read calls prove future merge/deploy permission. No new Human architecture decision needed; document limitations and leave Draft.

## Implementation Plan / Revision History

v1: finish read-only audit → commit this Plan (records only) → push existing branch → verify remote Plan bytes and SHA → implement listed files → tests/self-review → separate Result/evidence commit → push → observe current-head CI and readback → update PR status honestly. Plan is an execution record, no additional Human approval gate.
