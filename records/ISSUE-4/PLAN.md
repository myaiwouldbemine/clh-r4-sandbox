# LIGHT Governance v1.0 — Plan

Issue: https://github.com/myaiwouldbemine/myaiwouldbemine-Copy-Learning-Hub/issues/4
Branch: feat/light-guarded-auto-merge (based on PR #1 head 06e5526)
Status: implementation authorized; production activation NOT authorized

## Goal / WHY / Scope / Boundary
Human opens Issues and defines goals, WHY, boundaries and major decisions. Peer agents implement and review; GitHub verifies and merges eligible PRs. Minimize L0 overhead.
Scope: governance, agent instructions, conditional PR records, policy validation, proposed GitHub enforcement and activation tests.
Boundary (revised by conditional approval): design, implementation, repository configuration and tests are authorized; production auto-merge, PR #1 merge and deployment remain unauthorized. Existing CLH-002 work is separate. PR #1 historical work predates this Plan; this document does not retroactively plan bootstrap.

## Risk Level
L3: governance, permission and deployment control changes. Default ordinary work L0; actual impact always overrides default.

## Implementation Plan
1. Commit this Plan before changing implementation.
2. Replace proposed legacy policy with LIGHT v1.0; integrate plan-triggered records and closure criteria.
3. Prepare a fail-closed policy validator and disabled enforcement configuration; independently specify authenticated review/authorization transport.
4. Remove push-triggered deployment in this proposed branch; preserve explicit manual deployment with a separate approval prerequisite.
5. Provide concrete activation, permission, rollback and end-to-end test package. Do not activate it.
6. Record actual checks and remaining work in RESULT.md; commit and push reviewable branch.

## Acceptance Criteria
L0 does not require Plan/Records or independent review. Formal plans always precede implementation and link Issues/PRs; L2/L3 require them. L1+ review absence blocks. L2 authorized scope and L3 specific authorization are mandatory. Labels/descriptions/self-reports cannot grant eligibility. Auto-merge remains disabled pending one approval and PR #1 dependency resolution.

## Verification Strategy
Local adversarial policy tests: risk escalation, missing records, plan ordering, unavailable review, stale head/base, untrusted issuer, missing/failed/skipped checks and scope mismatch. Validate workflow structure and strict MkDocs build. Production E2E is pending: isolated canary PRs and actual ruleset/API denial tests after approval.

## Human Decisions / Authorization
2026-11-05: user authorized design/build of guarded auto-merge and added mandatory Plan/Result records. Production activation requires one approval of concrete gates, privileges, failure blocking, rollback and E2E. No per-PR Human merge after activation. This task's author is Codex; self-review is not independent review.

## Revision History
2026-11-05: initial pre-implementation Plan; includes both user updates. No older LIGHT Plan exists in the inspected local branches; use this as a traceable implementation plan without inventing prior records.

## Revision 2 — conditional approval and Early Draft PR
2026-11-05, before this revision's implementation: Human conditionally approved design/build/configuration/testing; production activation remains a separate explicit approval. Add Early Draft PR lifecycle to governance, agent instructions, PR template and policy tests. Human supplies WHAT/WHY/DONE (References optional); Builder classifies risk and investigates. Commit any formal Plan first; L2/L3 need required Plan approval before implementation. Draft is not authorization. Ready requires completed implementation, applicable verification and Result when planned; material scope/risk changes invalidate affected plan/review/authorization and require reevaluation. All Drafts and missing gates block merge; no new L0 ceremony.

Next implementation: add fail-closed lifecycle evaluator/tests; test a native ruleset against isolated canary ref using live GitHub API, retaining production disablement; investigate native simplification and credential constraints. Document actual results without claiming trusted services exist. Independent agent work is authorized by the requested independent review workflow, but no independent reviewer is presumed available.

PR #1 dependency step: its copy precedes only the new deployment-trigger fix, not historical bootstrap; commits 0b180ff then f4a429c. Both branch histories are preserved by merge.

## Revision 3 — Independent Review Identity Gate
2026-11-05: user authorizes isolated implementation/tests only. Build versioned attestation schema and fail-closed gate using trusted collector inputs and pinned identity registry; test both peer directions, impersonation, missing/stale review and blocking reviews/threads. Prefer native GitHub reviews with authenticated App provenance; no actual App install, credentials, ruleset edits, merge, deployment or production activation. Produce design, missing integration list and actual CI evidence. Gate is not an authentication service; simulated identities must never be described as provisioned.

## Revision 4 — Trusted Independent Review Integration
2026-11-05: current Human request authorizes read-only discovery, nonprivileged development and offline tests. L3 implementation proposal only; installation, credentials, ruleset changes and production activation need separate specific authorization.
Goal: establish the actual limits of GitHub identity evidence and implement the smallest fail-closed collector boundary without pretending a reviewer is provisioned.
Plan: (1) inspect actual installations/reviews/rules/checks and official API capabilities; (2) add a collector adapter with complete pagination, immutable context binding, current native review/dismissal/thread checks, authenticated expiring/revocable issuer evidence and trusted Builder provenance; (3) run adversarial offline cases and separate real read-only observations from simulations; (4) document credential custody and an isolated canary matrix, update Result and Draft PR #5.
Acceptance: missing or unverifiable provenance never yields PASS; head/base/scope changes invalidate evidence; L0 only exempts independent review and cannot bypass other gates. No registry, secrets or policy may come from candidate code. No real canary writes are authorized by this request.
Verification: existing 26 tests first, then synthetic collector/signature failures and positive cases; inspect resulting CI separately. Live independent review remains NOT RUN without authenticated identities and isolated custody.

## Revision 5 — Canary Authorization Package
2026-11-05: Human authorizes read-only discovery, design and documentation only. This is NOT authorization to create repositories/Apps/keys/secrets, edit protections, run privileged workflows, merge or deploy.
Goal/WHY: turn native App Review plus authenticated context attestation into a minimal, individually approvable Canary package independent of Codex Receipt capability.
Scope: evaluate existing repositories; specify exact proposed resources, permissions, custody, protected Actions boundaries, test matrix, rollback and cost caps in docs/development/CANARY_AUTHORIZATION.md. Preserve all earlier Plan history.
Risk: L3 design; resource/configuration execution deferred to explicit itemized approval.
Implementation: commit this Plan revision before writing the package; record current API facts versus assumptions/NOT RUN; prepare staged authorization IDs and update RESULT. Commit/push documentation to Draft PR #5 only.
Acceptance: no claimed isolation without technical proof, no candidate-controlled trusted policy/code/credentials, original APPROVED gate retained, L0 review-only exemption, first authorization batch contains no secret creation or privileged execution.
Verification: read-only API evidence; documentation consistency/diff check and Git Plan ordering. No production behavior or source changes; existing 55 offline tests were verified in preceding assessment, not real integration evidence.
Human decisions pending: resource names/visibility, named custodians, App permissions, credentials, safeguards, execution/budget. Every configuration item requires separate approval; no blanket activation.
