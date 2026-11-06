# Migration Plan — Issue #20

Version 1; 2026-11-06 Asia/Taipei. Accountable Builder: Codex.
Issue: https://github.com/myaiwouldbemine/myaiwouldbemine-Copy-Learning-Hub/issues/20

## Goal / WHY / Current State
Human opens an engineering Issue with WHAT/WHY/DONE and boundary; Agent owns the remaining lifecycle. See AUDIT.md for actual main/settings, inactive Pages, missing runner and historical #18/#19. User explicitly authorizes this migration in current chat; this Plan records engineering decisions and needs no additional approval.

## Target State
Issue → one Builder → optional Plan committed before implementation → Draft PR → implementation/tests/Self-Review/evidence → successful CI → Ready → SHA-bound merge → applicable Pages deployment/readback → evidence archive/readback → Issue closure. Normal engineering never waits for Human approval. Learning semantics remain ChatGPT + Human owned.

## Scope / Boundary / Files
Update GOVERNANCE.md, complete paired Traditional Chinese/English AGENTS.md, README.md, INSTALL.md, active docs/development/ISSUE_TEMPLATE_INSTALL.md, Issue/PR templates, .github/workflows/{docs-check,governance-tests,merge-and-close-pr,pages}.yml; add issue-agent workflow, runner prompt, minimal lifecycle script and tests, operation guide. Update record verifier/tests to remove mandatory risk/approval fields. Add records/ISSUE-20/{AUDIT,PLAN,RESULT,E2E,SELF-REVIEW}.md and evidence logs. Preserve all prior records, archive platform, content and #18/#19 history. No direct main push, force push, protection bypass, new governance service, privilege expansion or token copying.

## Implementation Plan / Agent startup
Use GitHub-hosted Actions with official openai/codex-action on owner-created engineering Issues. Accountable Builder Codex; Claude can use same documented contract. Model key and narrowly scoped automation transport must already exist before activation; do not obtain secrets from local credential stores. Separate read-only model execution from publish/merge credentials where feasible. Deterministic issue branch and concurrency prevent duplicate work. Prompt requires scope, committed Plan when needed, tests, Result, current-head Self-Review and no unapproved content. Agent reports blockers rather than inventing completion. Bounded retries; no infinite charge loop.

## Automatic merge design / CI Gates
Native main PR/check protection is a prerequisite, not a Human approval gate. Use current-head CI, no failures/pending/skips, resolved review threads, no CHANGES_REQUESTED, current base, explicit Issue linkage, scope/evidence in PR. Verify head immediately before Ready and SHA-bound merge API. Use explicit lifecycle metadata for reviewed head/base and applicable deployment; semantic scope remains Builder responsibility, not an asserted automatic proof. Fail closed on missing/invalid API data or conflicts. Never execute candidate code in privileged merge job; use main checkout. Disabled until prerequisites validated.

## Pages / closure
Pages native build/deploy on main push after enabled activation; strict MkDocs, embed deployment SHA in site, remote readback must equal deployed SHA. Archive separate merge/deploy/verification results with run URL and immutable SHA. Only close linked engineering Issue after archived record readback. No GitHub auto-closing keywords. Non-site tasks can archive/close after merge without unrelated deployment. Retry merged work from existing merge SHA; do not merge again. Serialize Pages and lifecycle; errors leave Issue open and blocker evidence.

## Permissions / activation
Existing read-only CI retained. Runner needs provider secret plus repository-scoped transport able to publish branch/PR and trigger CI; never silently grant administration or read secrets. Merge token requires contents/pull-requests/issues writes and checks/actions reads, not admin. Pages uses pages:write and id-token:write only in deploy job. Main required checks and resolved conversations, no force/delete/bypass, Pages Actions source and no routine environment approvals must be confirmed. No settings modifications before implementation verification; missing administrator-only configuration is documented precisely. Activation flag is an installation/emergency-stop switch, never a per-Issue approval token.

## Failure / retry / rollback
Fail affected operation with recorded blocker; keep PR Draft/Issue open. Re-run safely against exact SHA, reuse existing branch/PR/archive. A changed head/base invalidates Self-Review. Bounded Agent retry handles CI failure; unresolved requirements/content stop. Roll back through tested revert PR, retain commits and archived evidence. Emergency stop disables automation flag/workflows, cancel in-flight work, then revert PR; never rewrite main. Old merge/close must not remain an alternative premature closure path.

## Verification Strategy / E2E
Run Python unittest including injected API failures and state transitions; YAML/action syntax validation; strict MkDocs; git diff --check; bilingual per-clause semantic review; preservation checks. Unit/fake tests are not live E2E. E2E report separately marks all fifteen requested acceptance scenarios PASS/FAIL/BLOCKED/PENDING/NOT RUN. Live tests only after preconditions; no claim of Agent startup, real merge, deployment or closure without actual run URLs/remote readback. Publish current-head CI and Self-Review in PR; Result after implementation. If required activation/E2E cannot run, retain Draft/open Issue and explain precise blockers.

## Acceptance Criteria
All active approval/risk gates removed without changing content ownership; bilingual clauses equivalent; minimal functional automation candidate with safe failure/retry; required checks cannot be bypassed; Plan precedes implementation and Result follows; history intact; all evidence honest; full autonomous lifecycle only PASS after live E2E.

## Revision History
v1: initial audit-backed migration plan, committed independently before implementation. Later discoveries recorded as revisions or Result deviations, never backdated.
