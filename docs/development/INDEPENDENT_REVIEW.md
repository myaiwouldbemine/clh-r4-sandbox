> **ARCHIVED / NOT ACTIVE.** Superseded by Minimal Governance. C3–C5 and later platform implementation are stopped. The original proposal/evidence below is preserved, not current policy or authorization. Prototype code/tests formerly under scripts/ are retained under archive/governance-platform/scripts/.

# Independent Review Identity Gate

Status: isolated implementation; production integration BLOCKED. Codex/Claude roles are interchangeable. L0 exempts independent review only, never other gates or unresolved blockers.

## Trust boundary
Use native GitHub PR reviews for review state, immutable reviewer actor ID, review ID and commit ID. Prefer the existing Codex GitHub Bot if its actual App provenance can be independently verified; do not infer identity from a login/display name. Claude requires an equivalently authenticated integration. A human OAuth token, shared account or text claiming an agent role cannot establish identity.

A trusted collector, running outside Builder control, supplies the registry, current repository/PR/head/base/diff digest and API facts to scripts/review_identity.py. Registry maps pinned actor/App IDs to agent and isolated credential custody; never load it from the PR branch. Builder provenance must likewise be independently collected, not inferred from a commit author. GitHub App review provenance must be verified from authenticated API/event data; unavailable provenance blocks.

Native reviews bind head but do not establish base SHA or complete scope. Versioned attestation supplies repository, PR, head, base, builder/reviewer registered identities, verdict, scope (canonical complete diff SHA-256 digest) and native review ID. Schema: scripts/reviewer-attestation.schema.json. Authenticate the entire attestation through the isolated reviewer integration, binding payload bytes and issuer; a JSON document alone has no authority. The collector verifies authentication before setting attestation_authenticated. Never accept this flag or any facts from Builder/PR HTTP input.

Re-fetch all paginated reviews and threads, resolve latest state/dismissal per reviewer, preserve any active CHANGES_REQUESTED and unresolved blocking thread. Unknown/incomplete retrieval blocks. Collect fresh head/base and scope, invalidate on changes and recheck immediately before expected-head merge. Collector must prevent replay against another PR/base/scope. Tests use synthetic IDs and facts; none proves credential isolation or a real GitHub identity.

## Four distinct concepts
- GitHub Review: native submitted review and its current state; authenticated actor alone does not prove which agent performed work.
- Agent Attestation: authenticated context/scope/agent binding supplementing native review; never a Human approval.
- Policy Check: trusted service's decision after collection and validation; test CI is not this service.
- Human Approval: separately authenticated authorization for L2 plans/L3 actions; cannot be supplied by Agent attestation or PASS check.

## Revision 3 baseline — superseded by Revision 4 prototype
Keep the proposed single control-plane App and aggregate eligibility check; no additional review database or webhook service is required. Reviewer integrations remain separate trust principals. This patch implements the offline decision component only; no network collector, signature verifier, Bot installation, registry provisioning, credential isolation or production check publication is implemented/claimed.

Required before real integration: verify Codex Bot availability/App ID/actor ID and review capability; establish Claude authenticated reviewer provenance; establish authenticated Builder provenance; provision isolated custody outside Builder access; implement authenticated attestation transport and complete API collector; validate actual native reviews, dismissal/thread aggregation and races in an authorized test repository. Installation/credentials/official Ruleset changes require specific L3 authorization under the current user boundary. No such changes were performed here.

Tests cover both role directions, self-review, shared Human identity, missing reviewer, old head/base/context, requested changes/dismissals, blocking threads, forged/missing facts and L0 other-gate preservation. All are simulated. Readiness: BLOCKED for real independent review identity; implementation may be inspected while PR #5 stays Draft.

## Revision 4 — Trusted Collector prototype (2026-11-05)

### Real read-only discovery, separate from simulations
PR #5 is OPEN/Draft at discovery head 879c3704abc2a9ae07d05ec7875f8c1988e470d8, base f4a429c9ea51f1542c85d92571b5d4a5c15e86b5. PR #5 reviews/threads and PR #1 reviews are empty. records/ISSUE-4/trusted-review-discovery.json contains a real API snapshot and missing-identity BLOCK; it predates this revision and cannot authorize new heads.

The GitHub plugin can access this repository and lists installation 133111057 for owner account 275012389 with repository_selection=all. This establishes connector access, not enabled Codex Code Review. The result exposes neither App ID nor bot actor ID. No actual Codex or Claude reviewer App/actor pair was verified. Installation ID and owner ID are not reviewer App/actor IDs.

Local gh authenticates as Human OAuth account myaiwouldbemine, actor 275012389, scopes repo/workflow/read:org/gist. No token values or key stores were read/copied. /user/installations returned 403 requiring GitHub App user authentication; repository /installation returned 401 requiring App authentication. Neither proves App absence. Builder operations currently use Human credentials; isolated Builder App provenance and Reviewer custody are unverified. Two agents sharing this token cannot establish independence.

Ruleset 26612260 is active ONLY for refs/heads/canary/light-enforcement-issue-4, no bypass actors; deletion/non-fast-forward restrictions plus PR/thread resolution, zero required approvals, no required_status_checks rule. Effective rules for main and feat/CLH-001-project-bootstrap are []; classic protection returns 404 'Branch not protected' for both. No Required Checks observed on either target. Existing governance-tests SUCCESS is from GitHub Actions App 15368, not a Reviewer identity or trusted eligibility check. No settings changed.

### Official capability evidence
- [Codex GitHub review](https://learn.chatgpt.com/docs/third-party/github): requires connection/review enablement; supports @codex review. No documented promise of APPROVED verdict, signed scope attestation or isolated custody. No trigger comment sent.
- [Claude GitHub Actions](https://code.claude.com/docs/en/github-actions): supports official/custom GitHub App; github_token override changes authentication. Model subscription/API credentials are separate from GitHub principal. This does not establish repository installation or identity.
- [GitHub Review REST API](https://docs.github.com/en/rest/pulls/reviews): review ID, numeric user ID/type, state, submitted_at and commit_id. DISMISSED invalidates approval. Native review does not bind base/scope or expose reliable issuing App ID.
- [Review webhooks](https://docs.github.com/en/webhooks/webhook-events-and-payloads#pull_request_review): delivery signature authenticates transport; installation denotes receiving installation and must not be treated as author App. Timeline/events can provide dismissal actor/reason; this prototype checks current DISMISSED state and does not claim a dismissal history audit.
- GraphQL reviewThreads provides isResolved/cursor pagination. All unresolved threads, including outdated ones, conservatively block.

### Implementation and limits
scripts/trusted_review_collector.py collects REST reviews/files and GraphQL threads with complete pagination/count checks, rejects duplicates/unknown states/partial GraphQL, and recollects the entire snapshot. Every active CHANGES_REQUESTED blocks conservatively even if superseded; selected approval must be latest decisive review for pinned actor.

Scope v1 is SHA256 of canonical JSON with repository/PR/head/base and sorted complete file manifest (filename, sha, status, changes, previous_filename). Both commits bind complete trees including binaries. This defines the earlier unspecified diff digest; all signers must use this exact manifest algorithm. Files API cap of 3000 blocks.

Reviewer subject is existing schema-v1 attestation. Builder subject is purpose=builder-provenance-v1 plus repository/PR/head/base/scope/builder. Envelope fields: subject, issued_at, expires_at, key_id, signature. Integer UTC Unix times, max lifetime 300 seconds. Base64 Ed25519 signature over canonical JSON of other four fields. Canonical JSON uses sorted keys, compact separators, ASCII escapes. OpenSSL verifies against externally pinned public key. Missing, invalid, wrong signer, unknown key, revoked key/identity, future/expired envelopes block; trusted host clock rechecks expiry after API collection.

Registry additionally requires active identity/key revocation state, distinct App/actor IDs, kind=github_app, isolated=true, agent and distinct nonempty custody IDs. Key-to-App/actor binding MUST be independently enrolled from authenticated App/token evidence and audited custody. Bot type alone grants no trust. review_app_id is derived from enrolled signature identity, NOT a native REST field. Custody IDs are enrolled assertions, not technical proof by this code. Builder provenance issuer must observe actual execution/commit context, not sign Builder claims. Neither real issuer exists here.

No production CLI/endpoint, privileged workflow, check publisher, registry/secret loader or merge executor exists. Host must execute a pinned reviewed release outside candidate control; policy, registry and keys stay outside PR/repository. Never import this module from candidate checkout in a trusted service. gh Human OAuth is discovery transport only. L0 still checks blockers and returns review NOT_REQUIRED only; Draft/CI/Records/risk/authorization gates remain mandatory.

Two matching API collections are not atomic and may miss changes followed by reverts. PASS is only a bounded observation of review component. Production requires event invalidation for head/base/review/thread/revocation, serialized decisions, short TTL and immediate rechecks before any separately authorized action. Merge race protection and required-check source enforcement are unproven.

### Credential isolation proposal — not provisioned
| Principal | Separate custody and least privilege | Required evidence |
|---|---|---|
| Builder App | Builder runner/vault; contents/PR write where needed | App/actor/token identity and execution-bound provenance |
| Reviewer App | Reviewer runner/vault; contents read, PR review write; no Builder keys | App/actor/installation enrollment, native review plus signature |
| Collector | Protected control-plane deployment; contents/PR read | Pinned code/policy/registry and current revocation |
| Future publisher/executor | Separate later approval | No keys or permissions granted here |

Signing keys must never enter PR jobs/artifacts, candidate-readable repository secrets, or each other's runners. Collector holds public keys only. Product App availability is insufficient unless authenticated context attestation and execution provenance are supported. If unsupported, propose a separate enrolled broker before provisioning; never substitute a Human token.

### Isolated real Canary — ALL NOT RUN
Use dedicated private sandbox repository, synthetic branches, no deploy workflows or auto-merge. Authorize exact App enrollment/custody before tests. Installations, credentials, rules or permission changes each need Human approval.

Record actual repo ID/name, PR, head/base/scope, review ID/actor, App/installation/key IDs (no secrets), API pagination/counts, signature/time/revocation decisions, expected/actual result and CI URL separately from fixtures.

| Case | Expected |
|---|---|
| Valid enrolled independent reviewer and fresh scope, no blockers | Review component PASS; other gates remain |
| Same App/actor or shared Human token/custody | BLOCK |
| Forged identity/signature, unknown key, missing reviewer/provenance | BLOCK |
| New head/base or scope | BLOCK until new signed evidence |
| Selected review dismissed/superseded | BLOCK |
| Changes requested or unresolved/outdated thread | BLOCK |
| Timeout/denial/partial response/missing page/count/file cap | BLOCK |
| Revoked issuer/key, invalid/expired/future attestation | BLOCK |
| Mutable state changes during collection or expiry mid-collection | BLOCK |
| L0 without attestation | NOT_REQUIRED only; other gates/blockers remain |

No real positive reviewer Canary or ruleset enforcement test ran in this revision. Live missing-evidence BLOCK is discovery only.

### Smallest next Human action
Provide read-only non-secret existing Codex/Claude installation details: actual App ID, installation ID, selected repository, permissions, canonical bot actor ID and credential custody owner/location. No installation or permission increase is requested yet. If those integrations cannot issue context attestations/provenance, present a separate exact sandbox App manifest/credential/custody authorization request before any change. Production remains BLOCKED, not READY.
