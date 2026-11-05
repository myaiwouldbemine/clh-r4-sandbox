# Guarded Auto-Merge — one-time activation approval package

Status: PROPOSED / NOT ENABLED. Issue #4. This is L3 control-plane work.

## Proposed gates and executors

| Required context | Executor / evidence | Failure rule |
|---|---|---|
| `light/risk-authorization` | Dedicated Policy GitHub App: GitHub API full paginated diff, trusted base policy, independently classified semantic impact; L2/L3 authenticated Human authorization | Unknown risk, truncated diff, unauthorized scope or stale binding blocks |
| `light/records` | Policy App runs base-pinned record verifier on Git objects; classifier supplies formal-plan flag and Issue ID | Formal plan missing, incomplete or not committed before implementation, missing Result or unapproved deviation blocks |
| `light/review` | Policy App validates independent reviewer attestation, actual reviewer credential and builder identity | L0 emits verified NOT_REQUIRED success; L1+ missing/unavailable/pending/self/stale review blocks |
| `light/build-content` | Policy App verifies completed trusted validation runs and applicable content-review evidence | No applicable build may be explicitly NOT_REQUIRED; required build/content must actually pass; skip/cancel/timeout/unknown block |

Policy App publishes checks on the current PR head only after verifying current base and all evidence. App ID is pinned in ruleset required check integration_id. Ordinary Actions and Builder cannot publish Policy App checks. No production check may accept a fixture/snapshot or PR-supplied policy code as evidence.

### Identity and attestation contract
Separate Builder, Codex Reviewer and Claude Reviewer service identities; a shared Human token cannot prove independence. Reviewer service signs an attestation containing repository, PR, head SHA, base SHA, builder identity, reviewer identity, verdict, scope-diff digest and evidence links. The Policy App verifies registered issuer keys and that reviewer agent differs from builder agent. Fail if the reviewer service cannot be provisioned; do not substitute self-review. Credential isolation is required: Builder must not hold reviewer, Policy App or merge executor credentials.

Human L2 authorization is an authenticated Issue comment from the configured owner, approving the exact Plan Git blob and allowed paths/operations/acceptance criteria. Collector records comment ID, author ID, Plan blob, scope digest and time; re-fetch before merge. L3 additionally requires exact PR/head authorization and explicit auto-merge permission. Edited/deleted/revoked authorization invalidates eligibility. Human approval of this activation package is not blanket L3 approval for future PRs. Agent-written records cannot create authorization.

L0 eligibility is deliberately narrow: trusted classifier verifies actual nonsemantic edits, not merely Markdown extensions. Lesson meaning, examples, executable code and site behavior are at least L1; important source/provenance rewrites or broad architecture changes at least L2; workflow/policy/permission/deploy controls at least L3. Bulk deletion/unknown file types block for classification. No new Human paperwork for ordinary L0; if no trusted semantic classifier is available, hold eligibility rather than guess L0. All formal plans trigger records even at L0/L1; creating a plan outside records is a policy violation, not an exemption. Semantic review must detect this; a Git path checker alone cannot.

## Branch ruleset (to apply after approval and observed check runs)
Target refs/heads/main; enforcement active; bypass_actors empty. Require PR; zero global required approvals (risk-specific App gate handles L1+ without burdening L0); require resolved conversations; block deletion and non-fast-forward. Require the four contexts above from the dedicated Policy App; strict up-to-date policy. Squash merge only. Archive actual API request and response in Issue #4 evidence; re-read effective rules including inherited rules. If repository plan cannot enforce required checks/App source, activation is BLOCKED.

Required contexts must first be observed in real canary runs before making them required. Check-name presence alone does not establish trust; verify App identity, exact head/base and run identity. Query all pages. Duplicate unexpected check writers are a failure.

## Permissions and guarded merge mechanism
- Builder: contents write on topic branches and PR write; no administration, environments, checks write or protected-branch bypass.
- Reviewer service: read repository and independent review/attestation; no merge or admin permission.
- Policy GitHub App: contents/read, PR/read, issues/read, actions/read, checks/write, metadata/read; no contents/write or administration. Private key kept outside Builder access.
- Merge executor GitHub App: contents/write and PR/write only; no admin, Pages, OIDC, secrets or bypass. Before each merge, read fresh PR/head/base, authenticated policy evidence, all required checks, unresolved threads and blocking reviews. Require all conclusions success with matching head/base and trusted App; reject drafts, forks until explicitly supported, conflicts, unknown mergeability, authorization revocation or disabled activation flag. Serialize execution and use GitHub merge API with expected head SHA and squash. GitHub's strict ruleset is the final atomic guard against base movement. On mismatch/409/405, stop and re-evaluate; never retry using admin bypass.
- Dedicated executor performs an automatic guarded merge; native auto-merge is not needed and remains disabled to avoid an alternate pending merge path. Human does not merge each eligible PR.

Use webhook events for PR synchronize, base pushes, reviews/dismissals, Issue authorization edits/deletions, check completion and rules changes; also reconcile pending PRs periodically for missed webhooks. Invalidate eligibility on new head/base before reevaluation. Production service code, transport, key provisioning and authenticated runtime integration remain to be built/verified after this architecture is approved; the local record verifier is not that service.

## Failure blocking and rollback
Missing API permission, pagination failure, service outage, unavailable reviewer, stale result, revoked auth, incomplete records, check skip/fail/cancel or mismatched issuer => no merge, report exact blocker in PR/check. A single kill switch stops executor; revoke its installation token/private key if compromised. Do not remove required checks to unstick PRs. Disable any queued native auto-merge if one exists. Keep ruleset active; use a revert PR for code rollback. Preserve logs and previous Pages site. Never rewrite main history. Emergency bypass requires specific Human incident authorization and an audit record.

## PR #1 / deployment dependency resolution
Observed 2026-11-05: PR #1 open at 06e5526; description says second independent review pending; Pages API 404; repository rulesets []. No runtime Pages success established. Existing pages.yml deploys on main push, so merging can publish unexpectedly.
This branch removes push trigger and retains manual entry only. Before PR #1 merges, transplant that isolated change to its branch (or supersede PR #1 with this branch), obtain independent re-review and rerun its Docs Check. Confirm diff on the actual merge candidate. No current authorization to merge or deploy PR #1 is inferred. Manual Pages invocation also needs separate deployment authorization. Do not require post-merge Pages success as a pre-merge check.
Production deployment strategy, environment protection, artifact identity, permissions and rollback need a separate approved plan and real deployment test. Never enable unattended merges until PR #1 coupling and review are actually resolved.

## End-to-end acceptance and enablement sequence
1. Human approves this package once, including App identities, exact permissions, no-bypass ruleset and tests. Capture authenticated approval. Keep executor disabled.
2. Complete/provision trusted services and issuer registration; independent control-plane review. Dry-run on real canary PRs; publish checks without merging; verify actual App IDs and effective repository rules.
3. L0 typo/no plan: no new paperwork/reviewer, all gates succeed. L1 valid independent content/build evidence succeeds. L2 approved Plan/scope succeeds. L3 blocks until head-specific approval.
4. Negative canaries: missing/unavailable reviewer; Builder posing as reviewer; forged PASS label/comment/check; skipped/cancelled/failed CI; missing Plan/Result; Plan committed with/after implementation; plan outside records; changed Plan blob/scope; authorization deleted/edited/revoked; new head/base after review; duplicate check issuer; API outage; unresolved thread/CHANGES_REQUESTED; draft; conflict. Every case must refuse merge.
5. Attempt direct push, force push, branch delete and merge with a failing required App check using ordinary Builder/executor identities. All denied. Validate race by changing head/base between decision and merge. No admin bypass.
6. Exercise kill switch and revoke credentials; verify no pending PR merges. Revert a canary via PR without deployment. Record actual URLs, SHAs, API responses and check runs in RESULT; do not mark unrun tests PASS.
7. Resolve PR #1 dependency and deployment trigger issue, prove merging does not start Pages. Only then enable executor and observe one eligible canary auto-merge and one blocked PR. Report results. Human involvement thereafter is major decisions, authorization exceptions and unsolved blockers.

Approval request covers the concrete design and subsequent implementation/settings/testing sequence above. It does not authorize deployment or routine bypass. Any inability to provision trustworthy independent identities is an explicit blocker, not permission to weaken gates.

## Primary references
- https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets
- https://docs.github.com/en/actions/reference/security/securely-using-pull_request_target
- https://docs.github.com/en/rest/pulls/pulls#merge-a-pull-request

Privileged services must never execute PR code. The local verifier reads Git blobs only and its syntax checks cannot establish content correctness or authenticated authorization.

## Conditional approval revision — 2026-11-05
Human authorized implementation/configuration/tests, but explicitly withheld production activation. Early Draft PR is the standard workspace; Ready requires completed implementation, applicable verification and Result records. Drafts always block merging even when CI passes. New material scope/risk changes require reevaluation. No extra L0 records/reviewer.

### Native simplification assessment
Use native PR Draft state, conversation resolution, no-bypass Ruleset, exact-SHA squash merge and GitHub Actions for unprivileged tests. These eliminate a custom workflow state database and custom build service. Propose **one control-plane App installation** combining policy publication and the disabled merge executor, with one required `light/eligible` check containing risk/authorization, records, review and build/content subresults. This replaces four required contexts and separate Policy/Executor Apps without allowing Builder to mint this App's checks. App gets contents/write, PR/write, checks/write, issues/read and actions/read; no administration/Pages/OIDC/bypass. The previous read-only Policy App privilege boundary is traded for a single trusted control plane; this revision requires independent review before adoption. Never give its key to Builder. Reviewer still needs separate authenticated issuer identity; native approvals from the shared Human account cannot establish agent independence. A single reconciliation loop can poll GitHub and re-fetch before merge; webhooks are an optional latency optimization, not a separate required service.

Current executable lifecycle helper is intentionally not the trusted collector, semantic classifier or authorization layer. Governance Tests CI exercises PR code with read-only credentials; it is **not** the trusted eligibility check and must never satisfy `light/eligible`. GitHub native capability cannot independently authenticate which model performed a review under one shared account. No trustworthy reviewer credential or App installation key has been provisioned in this work; do not invent one or reuse the Human token as the service identity.

Live canary Ruleset 26612260 targets only `canary/light-enforcement-issue-4`, active with empty bypass list. GitHub rejected direct ref update and branch deletion (422), ref unchanged. Effective rules and responses are in records/ISSUE-4/canary-enforcement.json. Required-check source isolation, merge denial, force-push denial and production main enforcement remain NOT RUN. Canary protection is retained; no protection was lowered for cleanup. Production native auto-merge remains false. Rollback/executor kill switch remains NOT RUN because no executor is provisioned.

PR #1 actual branch now has pre-change Plan commit 0b180ff and deployment-trigger fix f4a429c. Verify its CI at that head. This fixes the actual candidate's push trigger, but outstanding independent review and any merge/runtime acceptance remain separate blockers. No deployment or merge has occurred.
