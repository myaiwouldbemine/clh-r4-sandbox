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

## Minimal integration and remaining work
Keep the proposed single control-plane App and aggregate eligibility check; no additional review database or webhook service is required. Reviewer integrations remain separate trust principals. This patch implements the offline decision component only; no network collector, signature verifier, Bot installation, registry provisioning, credential isolation or production check publication is implemented/claimed.

Required before real integration: verify Codex Bot availability/App ID/actor ID and review capability; establish Claude authenticated reviewer provenance; establish authenticated Builder provenance; provision isolated custody outside Builder access; implement authenticated attestation transport and complete API collector; validate actual native reviews, dismissal/thread aggregation and races in an authorized test repository. Installation/credentials/official Ruleset changes require specific L3 authorization under the current user boundary. No such changes were performed here.

Tests cover both role directions, self-review, shared Human identity, missing reviewer, old head/base/context, requested changes/dismissals, blocking threads, forged/missing facts and L0 other-gate preservation. All are simulated. Readiness: BLOCKED for real independent review identity; implementation may be inspected while PR #5 stays Draft.
