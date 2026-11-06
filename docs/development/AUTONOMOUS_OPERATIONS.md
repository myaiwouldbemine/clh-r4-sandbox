# Autonomous engineering operation

Policy: GOVERNANCE.md and paired bilingual AGENTS.md. Status: implementation candidate; activation and live E2E are blocked until the installation prerequisites below are proven. Issue #20 / PR #21 record the migration; #18/#19 remain historical and untouched.

## Startup and credentials

Owner creates an Engineering Task with WHAT/WHY/DONE/boundary. `Issue Agent` runs the official pinned openai/codex-action on a GitHub-hosted runner. It reads the current Issue, checks protection, uses deterministic `codex/issue-N`, commits an attempt marker, and runs Codex without a GitHub write token. Publishing uses a separate job, trusted main scripts, a Git bundle and normal non-force push. AI-generated code is not executed by the publish/merge jobs. Codex and Claude Code may follow the same evidence contract; the supplied hosted adapter currently runs Codex only.

`OPENAI_API_KEY` supplies model access. `CLH_AUTOMATION_TOKEN` is an existing, repository-scoped automation transport with contents/pull-requests/issues write, Actions/checks/statuses/Pages read, metadata read, and workflow update permission only if engineering workflows must be modified. Do not copy the current local gh OAuth credential into Actions, broaden its scopes, create a new governance App or disclose secret values. Prefer native rulesets so runtime does not need administration permission. The optional traditional branch-protection read API needs Administration:read; if unavailable, configure equivalent readable rulesets rather than expand runtime permissions. No Administration:write is required. A suitable transport is needed because ordinary GITHUB_TOKEN events do not reliably trigger autonomous downstream CI/push workflows; current GitHub behavior may require approval for PRs it creates. Missing credentials are BLOCKED, not a claim of Agent startup.

CI failure on an Agent branch triggers another attempt, at most three recorded attempt commits. Edits/reopened Issues may trigger processing but do not reset that budget. Global concurrency prevents simultaneous Builders. A failed runner before publication may consume a workflow run without persisting its attempt marker; it leaves a failed run, never a merge. No periodic model retries occur. Requirement changes invalidate the body digest. Closed Issues or closed/merged PRs stop publication.

## PR evidence contract

After final commit and Self-Review, the Builder appends one block to its PR body (not a file that changes its own head). Replace example strings with real values:

```text
<!-- clh-lifecycle {"issue": 123, "builder": "Codex", "head": "FULL_40_HEX_HEAD", "base": "FULL_40_HEX_MAIN", "issue_body_sha256": "SHA256_OF_EXACT_CURRENT_ISSUE_BODY", "scope_verified": true, "self_review": true, "complete": true, "deployment": true, "evidence": "Actual commands, results, findings, immutable evidence links and scope justification"} -->
```

This is Builder Self-Review evidence, not Human approval, an approval token, independent review or a semantic classifier. Missing requirements, unapproved educational semantics or blockers mean `complete` must not be true. The executor checks metadata, current Issue body, head/base, real CI, required native protection, unresolved threads and requested changes. GitHub still enforces native merge restrictions. All latest checks must succeed (neutral/skipped are not success). Required checks are `docs-check` and `governance-tests`. New head/base requires new evidence. The GitHub merge API receives the exact head SHA; native strict checks protect the concurrent-base window.

No auto-closing keywords in PR/commit text. `Issue: #N` is safe. Website paths force deployment applicability; other changes can request deployment when the task requires it. The executor checks code paths but cannot prove semantic scope automatically.

## Merge, deployment, archival and closure

`Autonomous Lifecycle` runs after CI/deployment completion, every fifteen minutes for recovery, and on dispatch. It reads current state from GitHub using main code only. Draft becomes Ready only after the gates pass. Merge is an API operation respecting native checks; GitHub's separate `allow_auto_merge` feature is not required.

For site tasks, a main push triggers native Pages build/deploy. The artifact includes `deployment-sha.txt`. Verification reads the configured HTTPS Pages URL and requires the exact merge SHA, with three bounded readback attempts. A deployment comment records the run ID and URL. Lifecycle independently requires that exact Pages workflow run to finish successfully for the merge SHA before archive/close. Non-site tasks skip unrelated deployment.

Archive comments use PR + full merge SHA keys and are read back before closure. Retry reuses the existing archive and merged commit. Changed evidence causes a blocker rather than overwriting history. Final Issue state is read back after closure. Comments are engineering evidence, not trusted identity attestation. Failure to read or write GitHub data fails closed; failed workflow logs and deduplicated PR blocker comments remain available. If even blocker posting lacks permission, the failed run is the evidence.

## Installation and activation

1. Configure an existing provider credential and narrowly scoped automation transport as the two named Actions secrets. Confirm the token can perform normal branch/PR/check operations without bypass. Repository default token permission stays read-only.
2. Protect main with PR-only, strict required `docs-check` and `governance-tests`, resolved conversations, no force pushes/deletions and no bypass actors. Required approving reviews can be zero; no Human approval gate is introduced. Traditional protection must enforce administrators too. Do not alter the isolated canary ruleset.
3. Configure Settings → Pages → Build and deployment → Source: GitHub Actions. Ensure github-pages environment allows main deployment without routine reviewers. Preserve unrelated environment/settings restrictions; report incompatible restrictions rather than bypassing them.
4. Validate CI and negative-case tests on the candidate. Merge the installation only when its applicable completion conditions are satisfied. The new workflows must exist on default branch for automatic Issue triggers.
5. With prerequisites verified and a rollback path available, set Actions repository variable `CLH_AUTONOMY_ENABLED=true` once. This installation/emergency switch is not a per-Issue approval. Run the documented live E2E with an owner-created engineering fixture, collect run URLs and SHA evidence. Do not claim production readiness until it passes.

Current audit found no secrets/variables/runners, no main protection and no Pages. No settings have been changed by the migration implementation. The actual missing credential cannot be manufactured by code. First-install live E2E remains BLOCKED until the prerequisites and default-branch installation are available; local tests do not resolve that blocker.

## Rollback

Stop new work by setting the activation variable false or disabling Issue Agent / Autonomous Lifecycle / Pages workflows; cancel queued/running affected jobs (a running merge cannot be undone by cancellation). Create a revert PR for the offending commit, run required CI and Self-Review, merge normally without bypass. For website rollback, build/deploy the revert commit and read back its SHA; never claim the previous deployment was restored merely because Git reverted. Keep Issues open until recovery evidence is archived. Preserve all prior comments, Plan/Result and Git history. Verify settings after code revert: Git changes do not undo GitHub settings. Avoid restoring the obsolete premature-close workflow as an active recovery path.

## Primary technical references

- [Official Codex Action](https://github.com/openai/codex-action): pinned action/input contract and provider credentials.
- [GitHub event triggering](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow): token/event recursion restrictions.
- [Branch protection API](https://docs.github.com/en/rest/branches/branch-protection): traditional protection read requires Administration:read.
- [Pages API](https://docs.github.com/en/rest/pages/pages): Pages settings/read permissions.
