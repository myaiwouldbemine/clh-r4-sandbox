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

PR #1 dependency step: this copy precedes only the new deployment-trigger fix. It does not retroactively plan bootstrap. Human conditional approval authorizes this configuration fix; no merge/deployment is authorized.
