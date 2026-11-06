# Results — Issue #20 autonomous governance migration

PR: https://github.com/myaiwouldbemine/myaiwouldbemine-Copy-Learning-Hub/pull/21
Issue: https://github.com/myaiwouldbemine/myaiwouldbemine-Copy-Learning-Hub/issues/20
Builder: Codex. **Implementation candidate delivered; activation / complete E2E BLOCKED.**

## Commit and ordering

- Base main: `7e530cdc818044ae4f760a021a331f888f993e43`.
- Audit and formal Plan committed independently before implementation: `716ef32d583335338c3671040df6844d720a47aa`.
- Governance, complete bilingual AGENTS, templates, minimal Agent/lifecycle/Pages workflows and production client/tests: `4dafc7d4a398770479beaadcf51264a3fc1e5a63`.
- Publisher tests and current installation documentation: `445e707e9ed67e6c89cf7bac2240ee5886026b95`.
- This Result is committed after implementation; final full reviewed records SHA, current CI runs and remote readback are recorded in PR #21. No circular/fabricated self-SHA.

## Results

Removed mandatory L0–L3 and repeated engineering Human approval from active policy, agent instructions, forms, PR template and guides. AGENTS contains 15 full paired Traditional Chinese/English clauses. Preserved tool-neutral one Builder, content ownership, tests, evidence, git history and fail-closed merge constraints.

Added owner-Issue hosted Codex adapter, separate bundle publisher, bounded CI-failure retry, automatic current-SHA Ready/merge reconciliation, applicable Pages build/deploy/readback and idempotent archive-before-close. Existing premature merge-and-close executor was replaced. Workflows remain disabled because the installation flag is absent and credentials are not configured; candidate code remains in Draft PR.

After tests passed, configured [main ruleset 26702419](https://github.com/myaiwouldbemine/myaiwouldbemine-Copy-Learning-Hub/rules/26702419), native PR-only/strict GitHub Actions checks, zero required approvals, resolved threads, no bypass/force/delete. Configured Pages build_type=workflow with main-only github-pages environment and no reviewer gate; HTTPS enforced. **This is setup, not deployment.** Existing canary, default read token permission, repository auto-merge setting and credentials were not changed. New rules apply to all PRs targeting main; existing Draft #19 was not edited or merged.

## Evidence

- AUDIT.md: original current-state audit; historical finding remains unmodified.
- PLAN.md: scope, architecture, startup/merge/deploy/close, permissions, retry, rollback, E2E and acceptance.
- UNIT-TESTS.txt: **51 tests PASS**, including real local Git bundle tests and injected API lifecycle tests. These are not GitHub E2E.
- BUILD.txt: strict MkDocs PASS; site content quality and browser visuals are separate.
- WORKFLOW-LINT.txt: actionlint 1.7.12 PASS. DIFF-CHECK.txt: PASS.
- MAIN-RULESET.json / PAGES-SETUP.json: actual API mutations and results.
- SETTINGS-READBACK.json: live settings, environment and protected main; preflight now PASS after initially failing closed.
- SELF-REVIEW.md: actual Builder work, findings, 15-clause bilingual matrix, scope and limitations.
- E2E.md: all fifteen requested scenarios with honest local versus live status.
- GitHub CI: final-head run links posted in PR after this commit; PENDING here until then.

## Deployment Evidence

Pages API returns configured site with status null; no deployment SHA or deployment Workflow URL exists. Deployment, remote rendered-site readback and autonomous closure: **NOT RUN / BLOCKED**. Do not infer deployment success from build, provisioning, merge readiness or unit tests.

## Deviations

Used a separate Issue #20 / Draft PR #21 from main rather than extending #19. Existing #18 records remain on #19's original branch, byte-for-byte untouched; not copied onto main or rewritten.

The runtime uses a separate existing automation transport secret because GitHub's built-in token has downstream event restrictions; no new App, Registry, attestation platform or token privilege expansion was performed. Model access and transport were not available. Runtime startup supports Codex; Claude follows the same policy but no alternate hosted adapter is claimed.

The initial audit's settings gaps were resolvable with existing access, so native protection and Pages setup were completed after tests without another approval. The installation guide records the actual state. Optional traditional-protection read needs Administration:read; recommended rulesets avoid that fallback. No administrative write permission is required by runtime.

## Unfinished / Remaining Blockers

1. `OPENAI_API_KEY` absent: administrator must supply an existing valid provider key as this repository Actions secret; do not paste it into chat or source.
2. `CLH_AUTOMATION_TOKEN` absent: supply an existing repository-scoped automation credential with the precise runtime permissions in AUTONOMOUS_OPERATIONS.md. No credential was copied from local gh or fabricated.
3. Candidate installation, activation and live E2E remain incomplete. Keep `CLH_AUTONOMY_ENABLED` unset/false until prerequisites and rollback are verified. No Ready, Merge, deployment or closure has been falsely claimed. This is a technical installation blocker, not a request to approve Plan/implementation/Ready/Merge/deployment/closure again.
4. Before activation, run the documented live fixture and capture actual Issue→Agent→CI repair→Ready→Merge→Pages→readback→archive→close plus duplicate/race/permission cases. Local tests cannot substitute for these runs.

## Rollback Procedure

Disable the installation variable/workflows and cancel affected queued/running jobs. Revert faulty code via a normal tested PR with current-head Self-Review and strict CI; never rewrite main or bypass native rules. Website rollback must deploy and read back the revert SHA. Preserve records and Issue history. Settings are outside Git: inspect native ruleset and Pages separately; do not remove protections just to complete a merge. Do not reactivate the old premature-close workflow. Full procedure: docs/development/AUTONOMOUS_OPERATIONS.md.
