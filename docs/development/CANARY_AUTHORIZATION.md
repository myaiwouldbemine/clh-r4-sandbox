> **ARCHIVED / NOT ACTIVE.** Superseded by Minimal Governance. C3–C5 and later platform implementation are stopped. The original proposal/evidence below is preserved, not current policy or authorization. Prototype code/tests formerly under scripts/ are retained under archive/governance-platform/scripts/.

# Issue #4 — Canary Authorization Package v1
Date: 2026-11-05 Asia/Taipei. Proposal only; no item below is authorized by this document.
Issue: https://github.com/myaiwouldbemine/myaiwouldbemine-Copy-Learning-Hub/issues/4
Draft PR: https://github.com/myaiwouldbemine/myaiwouldbemine-Copy-Learning-Hub/pull/5

Decision: READY FOR AUTHORIZATION of first resource-only batch; trusted runtime remains BLOCKED. Keep native APPROVED plus authenticated context attestation. Ordinary Codex Summary/Receipt cannot PASS. No merge executor, deployment, production settings change or automatic merge is included in any batch.

## Evidence and resource reuse
VERIFIED: PR #5 Draft at discovery head ddf064c5da4648bee22d21bbc80d19074a5ac33c, auto_merge=null. PR #7's prior real Canary authenticated comment actor 199175422 and App 1144995, but no native review; it is not isolated identity proof. Earlier 55 offline tests passed; no new integration tests run for this package.
VERIFIED now: gh can read private myaiwouldbemine/governed-env, main, not archived. GET /repos/myaiwouldbemine/governed-env/rules/branches/main returns 403 'Upgrade to GitHub Pro or make this repository public to enable this feature.' No contents or secrets inspected. Existing protection sufficiency and model custody UNKNOWN. Do not change its visibility or reuse it without a separate assessment.
Connector current installation inventory confirms target learning Repo access; it does not establish App custody.
Existing learning Repo / PR #7: reuse as historical evidence only, not new privileged sandbox. Existing .venv/site and user work remain separate.

Preferred minimum new resources (names proposed; availability NOT CHECKED):
- PUBLIC myaiwouldbemine/clh-review-sandbox: synthetic text/code only; private data prohibited; no secrets, no Pages, no deployment workflows. Apps installed only here.
- PUBLIC myaiwouldbemine/clh-review-control-canary: generic reviewed control code, public keys and synthetic metadata only. Neither Agent App installed here. No agent write/admin permissions; secrets only in protected environments after later approval.
Public visibility avoids requiring a paid private-repository protection upgrade. Human must explicitly approve public visibility. If private is mandatory, STOP and reprice/verify plan capabilities before provisioning. No automatic fallback, upgrade or existing Repo visibility conversion.

GitHub docs distinguish availability of private environment secrets and required environment reviewers; private required-reviewer support cannot be assumed:
https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/manage-environments
https://docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments

## Architecture and identities
Control is a fixed reviewed Actions release (full commit SHA) with trusted Registry/Policy/Publisher. It orchestrates separately isolated Codex and Claude execution and a read-only collector. Manual Human workflow_dispatch only; no issue_comment/pull_request_target/workflow_run triggers, cron or candidate-controlled reusable workflow. Inputs are validated repo ID/PR number plus an allowlisted test ID, not scripts, ref names or arbitrary URLs.
Two fixed private App registrations (names proposed; availability UNKNOWN): CLH Canary Codex and CLH Canary Claude. Custom Apps identify our controlled integration, not official vendor certification. Model identity is established by pinned backend/adapter, non-secret model/run metadata and protected execution provenance, not App name.
Roles are assigned per run: Codex Builder -> Claude Reviewer, then reverse. Separate custody applies to both; a shared Human owner is an administrative root, not runtime independence. No Human OAuth token in either Agent environment.

Stages:
1. Control snapshots repo numeric ID/name, PR, head/base and scope v1 using existing collector manifest. Reject incomplete files/API caps. It selects a pinned trusted review rubric; candidate AGENTS.md/prompts are untrusted data, never policy.
2. Builder runs without Reviewer keys. Trusted Builder publisher records execution-bound provenance for the resulting commit; commit author alone is insufficient.
3. Reviewer reads exact immutable snapshot, using only its model credential in a constrained execution environment, no App or signing keys. It never auto-runs candidate scripts, dependencies, hooks or actions.
4. If code execution is needed, separate fresh no-secret job, no credential persistence, no writable cache/shared runner/workspace. Its output is untrusted evidence, not approval. Transport smoke tests need no candidate execution.
5. Trusted publisher job uses only fixed control code. It parses bounded structured model result, requires explicit rubric completion and context match, checks native blockers and re-snapshots. It mints only a sandbox PR-write token, submits APPROVED with explicit commit_id, then reads back native Review ID/actor/state/commit.
6. Signer creates existing schema-v1 attestation including real review ID and head/base/scope; Builder provenance uses its separate purpose. Existing Ed25519 envelopes remain required, max 300 seconds, fresh trusted clock and revocation checks. No fabricated review_id. Publish only bounded non-secret signed evidence.
7. Read-only collector independently verifies native current state, signature/enrollment, Builder identity and all blockers. Result is review-component only, not merge eligibility. No check publication or merge call.

A full run cannot be attested from PR-uploaded result files. Publisher accepts results only from an allowlisted control workflow commit/job/run/attempt for its own pre-recorded context. It verifies origin and schema; it does not execute artifacts or interpolate model text into shell. Model output remains a claim about review quality, not an infallible guarantee. Transport-fixture APPROVED must be tagged simulation and never pass full semantic-review eligibility.

## Permission matrix
| Principal | Sandbox permissions | Control access | Restrictions |
|---|---|---|---|
| CLH Canary Codex App registration | Metadata read, Contents write, Pull requests write | None | Selected sandbox only; same registration supports role reversal |
| CLH Canary Claude App registration | Metadata read, Contents write, Pull requests write | None | Same; distinct App ID, actor, private key |
| Builder job token | Contents read; write only in separate Builder publisher; PR write only if creating test PR | None | Repo allowlist; cannot edit workflows/control |
| Reviewer model job | Public snapshot only; no write token | None | Model credential scoped/budgeted separately |
| Reviewer Publisher installation token | Pull requests write; Contents read only if needed | None | Downscope per mint; short-lived; revoke after job |
| Collector token | Pull requests read, Contents read; Issues read only for ordinary-comment collection | Control GITHUB_TOKEN contents read | No signing or publication keys |
| Control GITHUB_TOKEN | No sandbox access inherently | contents read; other permissions omitted | persist-credentials=false |

No actions/workflows/administration/secrets/checks/statuses/deployments/Pages permissions requested for Agent Apps. PR write is broader than submit-review: a compromised token could alter PR metadata or attempt other PR operations. API allowlists are defense in depth, not GitHub fine-grained enforcement. Sandbox is disposable; publisher code and key custody are trusted boundary.
Native App Review support:
https://docs.github.com/en/rest/pulls/reviews
App tokens in Actions:
https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/making-authenticated-api-requests-with-a-github-app-in-a-github-actions-workflow

## Credential custody and isolation acceptance
Proposed accountable root custodian: Human owner myaiwouldbemine; actual named human confirmation REQUIRED. Two logical custodians below must be explicitly assigned and cannot be Builder-controlled processes:
- Codex custodian: Human-administered environment codex-publisher; Codex App key + Codex provenance/review Ed25519 key; separate codex-model environment for model access.
- Claude custodian: Human-administered environment claude-publisher; Claude App key + Claude Ed25519 key; separate claude-model environment.
- Control administrator: Human only; Registry/public keys/revocation/policy release acceptance. Neither Agent can administer control, dispatch arbitrary refs or bypass protections.

Same administrator is an acknowledged common root. Environments alone do not prove separate trust principals. Distinct jobs, workload identities, backend credentials and secret access policies must be verified; if unacceptable under independence policy, distinct named administrators/accounts are required before running.
Present local gh Human OAuth is powerful. It must not be copied/mounted into Agent runners. No user-home mount, gh hosts.yml, SSH agent, inherited cloud credentials or persistent developer runner. Separate ephemeral GitHub-hosted jobs; no shared self-hosted runner. This package cannot claim Builder isolation until denial tests pass.
Control code allows no Agent App installation, no Agent repository collaborator access and no public fork PR workflow execution. Only reviewed main release may access environments. Environment required Human approval, prevent-self-review and no admin bypass where supported; required approver must be distinct from dispatcher. Second approver availability UNKNOWN; if unavailable use an explicitly accepted alternate custody mechanism in a revised package, do not silently weaken.
Protected main: no force/delete, PR-only, at least one independent Human reviewer, dismiss stale approvals, resolve threads, protect workflow/policy/registry paths, deny Agent bypass. A real second maintainer and account feature support must be confirmed. A bot cannot supply its own control approval.
GitHub environment protection does not prevent a root administrator from changing policy; that root remains trusted. Builder cannot have that administrator credential.
Security guidance:
https://docs.github.com/en/actions/reference/security/secure-use

## App/key lifecycle (requires later itemized approval)
Register each App under Human ownership, no webhook initially, no user OAuth flow, request exact permissions above. Install each using selected-repository scope ONLY sandbox. Do not install on learning Repo/control or all repositories.
Create one App private key per App and one Ed25519 attestation key per Agent (four independent private keys total); generate only in authorized custody tooling, never chat/repository files. Record only public fingerprints/key IDs. Key values must never be logged/uploaded as artifacts.
Verify App JWT GET /app ID/slug; verify installation App association/repository/token downscope; submit controlled smoke Review and pin numeric Bot actor from authenticated response. Enrollment binds backend adapter, App, installation, actor, custody owner, signing public key, key ID, revocation/version. Human accepts exact enrollment before full gate runs. Installation ID is not App ID.
Rotate: enroll new public key with explicit validity, test, then revoke old; any unknown revocation state blocks. Do not reuse GitHub App RSA private key for Ed25519 signing.
Revoke: stop all workflows, cancel active jobs, revoke minted tokens, delete/revoke compromised App private key, disable installation/remove sandbox grant if approved for incident response, revoke signing key in external registry, invalidate outstanding evidence. Token revocation alone is insufficient if root key survives.

## Individually approvable L3 checklist
All PENDING / NOT AUTHORIZED. Each ID authorizes only that row, not subsequent dependencies. Exact later manifests/releases and named approvers must be supplied before their batch is executed.
| ID | Exact proposed operation | Dependency |
|---|---|---|
| R1 | Create PUBLIC myaiwouldbemine/clh-review-sandbox, synthetic-only; no secrets | Confirm name/public disclosure |
| R2 | Create PUBLIC myaiwouldbemine/clh-review-control-canary, synthetic-only; no secrets | Same |
| C1 | Disable Actions execution in sandbox during setup; keep Pages/auto-merge disabled | R1 |
| C2 | Keep Control Actions disabled during bootstrap | R2 |
| C3 | Assign named Human-only Control admin and distinct approver; remove any Agent write/admin grant if present | Named people/permission diff |
| C4 | Configure Control main PR/review/force/delete/path protections and no Agent bypass | Capability check and exact rules diff |
| C5 | Create four protected environments, main-only, required approver, prevent-self-review, no bypass | Exact settings; real second human |
| A1 | Register private CLH Canary Codex with matrix permissions, no webhook | Name/owner accepted |
| A2 | Register private CLH Canary Claude with matrix permissions, no webhook | Same |
| I1 | Install Codex App on sandbox only | A1, R1 |
| I2 | Install Claude App on sandbox only | A2, R1 |
| K1 | Generate/store Codex App private key in codex-publisher only | C5, named custodian |
| K2 | Generate/store Claude App private key in claude-publisher only | C5, named custodian |
| K3 | Generate/store Codex Ed25519 key; enroll public key | Codex custodian accepted |
| K4 | Generate/store Claude Ed25519 key; enroll public key | Claude custodian accepted |
| M1 | Add/use Codex model credential in codex-model, exact backend/scope/budget | Hard budget verified |
| M2 | Add/use Claude model credential in claude-model, exact backend/scope/budget | Same |
| W1 | Bootstrap Human-reviewed fixed Control release, Actions allowlist, full-SHA pins, manual trigger only | Reviewed artifact and C3-C5 |
| W2 | Enable Control Actions for that exact release; run at most four authorized runs | Budget and all isolation prerequisites |
| E1 | Accept actual App/actor/installation/key/custody enrollment after smoke test | Human acceptance of API evidence |
| T1 | Create synthetic sandbox branches/Draft PRs and submit/dismiss test reviews, modify synthetic head/base, resolve test threads | Exact fixtures/test script; sandbox only |
| T2 | Test key revocation/denied access and rollback | Specific key IDs; no production keys |
| B1 | Configure maximum Actions paid-spend blocking and model hard budgets | Exact scope, prevent impact on unrelated work |

No production Rule/Secrets/Branch Protection changes are requested. A sandbox native enforcement Ruleset, if later needed, requires a separate exact rule diff; API review-component tests do not prove merge enforcement.

## Cost and run limits
First batch R1/R2/C1/C2: USD 0 incremental paid spend; no plan upgrade, model calls or enabled privileged workflow.
Later trial proposed ceiling: USD 5 total incremental model cost, combined Codex+Claude; USD 0 paid Actions/runner/artifact spend. Max four manually authorized runs, one at a time, 10 minutes each (40 runner-minutes total); no automatic retry. Standard hosted Linux only; no larger runners; artifacts <=10 MB/run, retention 1 day.
These are requested limits, NOT configured controls. Enable model runs only if provider-side enforceable remaining spend caps (including concurrent charges) fit the shared USD 5 ceiling. Token limits alone are not a hard monetary cap. If no enforceable provider cap exists, paid model runs BLOCK; transport-only fixtures must stay marked simulation.
Verify available included Actions/storage allowance and effective stop-spend policy before execution. Account-wide budget changes that affect unrelated work need separate B1 approval; no plan upgrade/credit purchase.
Control checks run count, elapsed time and remaining budget before dispatch; timeout/error stops issuance. Unexpected charge or uncertain usage => cancel remaining runs and BLOCK.

## Canary matrix — all NOT RUN
| Case | Expected result / required evidence |
|---|---|
| App transport smoke both Apps | Native Review read-back ID/actor/type/state/head; authenticated token enrollment; fixture only, NOT independent semantic PASS |
| Codex Builder / Claude Reviewer | Full fresh context/signature/provenance/native APPROVED; review-only PASS |
| Claude Builder / Codex Reviewer | Same in reverse |
| Same agent/App/actor/custody, shared Human token | BLOCK |
| Human comment with matching App provenance, fake Receipt/Review ID | BLOCK |
| Wrong signature/key/Repo/PR; replay | BLOCK |
| New head/base/scope | Old approval evidence BLOCK; fresh review required |
| Dismissed/changes-requested/superseded review | BLOCK |
| Unresolved/outdated thread or unresolved trusted blocker | BLOCK; ordinary ambiguous blocker => manual resolution, no inferred PASS |
| Missing/partial/denied API, page/cap mismatch | BLOCK |
| Unknown/revoked/expired/future evidence; expiry during API collection | BLOCK |
| Candidate AGENTS/workflow/registry edits; shell/path/artifact injection | Cannot modify trusted policy or issue credentials; BLOCK suspicious result |
| Builder attempts Control write/env access/Reviewer key access | Access denied; no secrets printed; safe canary markers only |
| Reviewer attempts Builder key access | Denied |
| Model output malformed/incomplete or error | No APPROVED issued; BLOCK |
| Race between review/context collections | BLOCK observed changes; no atomic merge guarantee claimed |
| L0 / L1-L3 missing review | L0 review NOT_REQUIRED only; L1-L3 BLOCK |
| Draft / other gates even with valid review | Remain unmergeable by policy; no merge attempted |
| Budget exhausted / rollback | No further tokens/signatures/runs; old evidence revoked |

Record synthetic vs real results separately, exact repo ID/PR/head/base/scope/review/App/actor/run/key IDs, expected/actual, timestamps and URLs; never secret values. No tests on PR #1/#3/#5/#6/#7 by this authorization batch. No new review triggers on existing PRs.

## Rollback
1. Human disables Control Actions, cancels queued/running jobs, prevents dispatch. This emergency stop must be included in execution authorization.
2. Revoke installation tokens and App keys if compromise suspected; remove installation access or suspend/uninstall only under explicit rollback authorization.
3. Revoke affected signing keys/identity enrollment; collector freshness/revocation unknown => BLOCK. Preserve signed/public evidence and logs, do not delete audit records.
4. Mark sandbox results invalid, leave Draft PRs unmerged. No force push/reset or production changes.
5. Restore reviewed control release via a Human-reviewed change only after cause and custody revalidated. Re-enabling requires new approval.
No resource deletion or unrelated account changes in rollback. Proposed R1/R2 first batch rollback is leave empty repos with Actions disabled; archive/delete requires separate approval.

## First authorization request (resource-only)
Approve separately R1, R2, C1, C2:
- two exact proposed PUBLIC repositories, synthetic data only, Human owner myaiwouldbemine;
- Actions disabled in both immediately during setup, no credentials/Apps/workflows executed;
- no paid spend or plan changes.
GitHub defaults may enable Actions on creation: no workflows are added before disabling and confirming settings.
If a name is unavailable, STOP and request alternate name; no substitution. No App registration, installation, key generation, secrets, protections or live test execution is included.
This creates a reviewable isolated resource baseline; remaining C/A/I/K/M/W/E/T/B rows need subsequent individual authorization.
