# On-Demand Autonomous Engineering

Human + ChatGPT plan/approve educational content and create an engineering Issue. Human starts Codex App when needed. One recorded accountable Builder handles planning, implementation, tests, Self-Review, PR and gated lifecycle autonomously. No routine Human merge or per-step approval. GOVERNANCE.md and the complete paired bilingual AGENTS.md remain controlling policy.

繁體中文摘要：按需啟動本機 Builder；保留原有安全與驗證標準。電腦或 App 關閉時不執行新工程，已送出的 GitHub CI／Pages 工作可完成。重啟時讀回遠端實況，不把舊審查當作新 SHA 的證據。教材語義仍由 ChatGPT＋Human 核准。

## Login and execution boundary

Existing App sign-in provides model access; existing `gh auth` provides GitHub access in the local shell. These are separate. [Official authentication documentation](https://learn.chatgpt.com/docs/auth) describes ChatGPT sign-in. Do not inspect credential files or copy tokens into Actions. Check `gh auth status`, repository access and protection with read-only calls; an authenticated account does not prove permission for every mutation. The normal workflow does not require `OPENAI_API_KEY`, `CLH_AUTOMATION_TOKEN` or `CLH_AUTONOMY_ENABLED`.

Hosted Issue Agent and Autonomous Lifecycle workflows are inert manual-only tombstones with skipped jobs; they cannot react to Issues, CI or schedules. Historical `agent_job.py` library and tests remain for provenance, but its CLI is blocked. No model is launched in GitHub Actions. Use ordinary non-force branch push and PR tools from the active session.

Local lifecycle locking requires WSL/Linux (`fcntl`). It locks the common Git directory across worktrees and releases on process exit/crash. It is not a cross-machine lock; only one accountable Builder may operate on the task at a time. Do not start another machine/session until the outgoing operation's outcome is read back.

## Start, implement and review

1. Read latest Issue WHAT/WHY/DONE/boundary, all comments, PR/head/base, governance and records. Record Builder and scope. Stop for unapproved educational semantics.
2. Reuse the existing Issue branch/PR, or create a `codex/` branch and Draft PR. Never reset away local work or force push. Commit a necessary formal Plan independently before implementation; write Result afterward. Revision records use a new prefix and an explicit revision starting commit.
3. Implement, run applicable tests, strict MkDocs, workflow lint and diff check. Push normally and inspect actual current-head CI. Review actual changes, scope and evidence against full head/base. Changed head/base requires fresh tests/review; unresolved blockers retain Draft.
4. Record actual work, Claim/Source/Method/Evidence, findings, verdict and Fresh-Context Challenge inclusion/omission rationale. Review is Builder Self-Review, not independent approval or identity proof. Do not add complete=true before all applicable work is actually complete.

Normal local commands (replace placeholders with observed values):

```bash
python3 scripts/autonomous_lifecycle.py preflight --repo OWNER/REPO
python3 scripts/autonomous_lifecycle.py check --repo OWNER/REPO --pr NUMBER --head FULL_HEAD_SHA --base FULL_BASE_SHA
```

`check` is read-only on GitHub, including on a merged PR; it does not mark Ready, deploy, archive or close. On an already merged PR it reports only observation, not deployment/closure acceptance. The local advisory lock file is not engineering evidence.

## PR evidence contract

After final commit/Self-Review, add exactly one block to the PR body (not a file that changes its own head):

```text
<!-- clh-lifecycle {"issue": 123, "builder": "Codex", "head": "FULL_40_HEX_HEAD", "base": "FULL_40_HEX_MAIN", "issue_body_sha256": "SHA256_OF_EXACT_CURRENT_ISSUE_BODY", "scope_verified": true, "self_review": true, "complete": true, "deployment": true, "evidence": "Actual commands, results, findings, immutable evidence links and scope justification"} -->
```

The block is a Builder record, not an approval token or automatic proof of semantic scope. The digest covers the Issue body; the Builder must separately read all latest comments and stop requests. Do not use auto-closing keywords in PR or commit messages. `Issue: #N` is safe. Site path changes require deployment; non-site tasks do not require unrelated publication.

## Merge gate and explicit local execution

When the task permits lifecycle execution and all required verification is complete, the Builder autonomously runs:

```bash
python3 scripts/autonomous_lifecycle.py run --repo OWNER/REPO --pr NUMBER --head FULL_HEAD_SHA --base FULL_BASE_SHA
```

One explicit PR and expected full SHAs are mandatory. No broad reconciliation CLI exists. It verifies native main protection, current Issue/PR/scope record, required docs-check/governance-tests, all current check/status results, resolved threads, no requested changes, mergeability and exact head/base. Missing/failing/pending/skipped/cancelled evidence blocks. It marks Ready, rereads state and CI/reviews, then calls the merge API with exact head SHA. GitHub enforces protection; no admin/bypass option is used. Native `allow_auto_merge` is not needed for this direct gated merge.

REST has no atomic expected-base input. Fresh base reads and strict native up-to-date checks mitigate the final race; they are not a distributed transaction binding Self-Review to an immutable base. The Builder must not claim stronger guarantees. An ambiguous network outcome requires remote merge readback before retry. No automatic network mutation retries occur.

## Pages and SHA readback

For website work, the first run merges and reports deployment PENDING, keeping the Issue open. Watch the Pages push run for the exact merge SHA. For recovery while that SHA is still main, the Builder can retry manually:

```bash
gh workflow run pages.yml --repo OWNER/REPO --ref main -f expected_sha=FULL_MERGE_SHA
```

This is a Builder engineering action, not a Human approval step. The workflow must first be installed on main. Both events verify current main, effective native protection and the exact merged main PR. Dispatch additionally requires the expected SHA. Every valid protected merge publishes the current tree so consecutive merges can coalesce. Lifecycle deployment metadata controls Issue evidence. The local Builder checks the private bypass list. An advanced main blocks old-SHA dispatch; investigate and prepare a current reviewed recovery PR rather than falsely crediting another SHA. Pages jobs serialize, build strict MkDocs, embed `deployment-sha.txt`, upload artifact and deploy with native GITHUB_TOKEN/OIDC (`pages:write`, `id-token:write` only deployment job). No off-device AI runs.

The verify job reads the configured HTTPS Pages URL with bounded retries and checks homepage status and SHA bytes. Only a lifecycle PR requiring deployment receives a merge-SHA/run marker on its reviewed Issue. The local Builder observes the exact run to completion, then repeats the targeted `run` command with the original reviewed head/base. Already merged PRs reuse their merge SHA; no second merge. The executor verifies successful Pages workflow path/main/merge SHA, configured URL and **fresh remote SHA bytes** before archival. A marker alone is insufficient. Deployment denial, failed run, stale published bytes or missing evidence leave the Issue open.

[GitHub Pages workflow documentation](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages) supports native token/OIDC deployment. [GitHub event documentation](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow) explains GITHUB_TOKEN downstream-event restrictions; the protected merge uses the local Builder’s existing gh identity so its push triggers Pages.

## Archive, close and interruption recovery

Archive uses PR + full merge SHA as a stable key, stores separate merge/deployment/closure results and reads the exact comment back. Changed archive data blocks rather than overwriting. Current Issue digest and PR evidence are checked again before close; then the Issue's closed state is read back. These records do not imply learning mastery or content approval.

| Interrupted stage | Resume action |
|---|---|
| Editing / before push | Inspect worktree and commits; preserve work, reread scope/head/base, test and push normally |
| Pushed / CI pending | Read actual new-head CI; fix bounded failures and invalidate stale review |
| Ready or merge request with lost response | Fetch PR; if unmerged revalidate all gates, if merged use existing merge SHA |
| Merged / Pages pending | Follow the exact push run. Retry only after inspecting the failure and confirming current main. A manual retry provides recovery evidence only |
| Pages running / App off | Existing job may finish; next session reads run and remote SHA |
| Archive write/close response lost | Read existing merge-SHA archive, verify bytes, reuse it, then read Issue state |
| Conflicting archive / changed requirements | Stop, record blocker; no overwrite, duplicate merge or false closure |

For an unchanged failure, record at most three repair attempts with cause/action/outcome before leaving BLOCKED. New investigation or changed conditions can justify a new bounded attempt; merely restarting App does not erase the record. If permissions prevent posting blocker evidence, keep local output and push a record when permitted. Error logs must not expose raw tokens/API secrets. Do not run other Builder sessions concurrently; comment APIs offer no atomic create-if-absent guarantee across machines.

## Installation, acceptance and rollback

Keep CI contents:read and main PR-only, strict required checks, resolved threads, no bypass/force/delete. Pages source must be Actions and its environment main-only. Read settings rather than assuming documentation configures them. Do not add credentials, expand scopes or weaken rules to make validation pass.

PR #21 remains Draft for this revision. The architecture instruction prohibits Merge, Deploy and Issue #20 closure during this task. Real branch publication, CI and read-only gate tests are distinct from full live lifecycle E2E, which remains BLOCKED/NOT RUN. Original #18/#19 and Issue #20 evidence remain historical; new ON-DEMAND-REVISION records describe this design.

Before merge, stopping the session causes no production installation. After future installation, stop local operations, inspect/cancel affected queued Pages jobs, then use a tested revert PR with current Self-Review/required CI and normal merge. Redeploy and read back the revert SHA for website recovery. Do not restore hosted agent/scheduler or the obsolete premature-close path as an active rollback. Git revert does not undo remote settings. Keep the Issue open until recovery evidence is archived and read back; never rewrite history.
