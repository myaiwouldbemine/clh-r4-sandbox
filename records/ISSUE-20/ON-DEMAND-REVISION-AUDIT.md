# On-demand read-only audit — 2026-11-07 Asia/Taipei

Accountable Builder: Codex (continuing, no delegation or handoff). Read current Issue #20, PR #21 and its architecture comment 6698471618, #18 and its comments, #19 metadata/evidence and Plan/Result on its branch, current governance, all Issue #20 records, workflows, lifecycle/publisher/verifier and regression tests before implementation.

Verified remote and local head: `bb577319ba003f3b92ef4fc7cf0cd717e8315cac`; main: `7e530cdc818044ae4f760a021a331f888f993e43`. PR #21 Draft/open; #19 Draft/open at `7efb0521d63b646501b83ecafdfb40da473d914b`. Worktree clean. No historical records changed. Re-ran baseline unittest discovery: **53 PASS**, not live E2E. Some older test files use standalone main functions and are not discovered by unittest; retain and report separately.

| Component | Decision | Reason / risk / replacement |
|---|---|---|
| GitHub-hosted Issue Agent | DISABLE | Unneeded off-device model; replace workflow with permanently skipped manual tombstone, no event triggers/model/secrets. Git preserves original. |
| Git bundle publisher / agent_job | DISABLE runtime, KEEP library/tests | Isolated publisher useful historical regression, unnecessary local transport. Disable CLI; no live caller; local normal git push + existing Draft PR. |
| Hosted retry budget | MODIFY | No autonomous model/retry loop. Keep original isolation tests; Builder records at most three attempts per unchanged failure before blocker, new investigation required. |
| Autonomous Lifecycle schedule / workflow_run | DISABLE | No background Ready/merge/close; inert workflow with no writes. |
| Ready / Merge executor | MODIFY | Reuse native protection/CI/thread/scope gates in explicit single-PR local check/run commands, exact expected head/base and OS lock. Never scan/execute all PRs. |
| Pages deployment | MODIFY | Explicit Builder dispatch on main with expected merge SHA; native GITHUB_TOKEN/OIDC; no AI key or PAT; no Issue closure in Actions. |
| SHA readback | KEEP + MODIFY | Keep workflow readback and verify successful exact-SHA run plus fresh remote bytes locally before closure. Prevent stale/comment-only evidence. |
| Archive → Close | KEEP + MODIFY | Preserve merge-SHA key, byte readback, retry after interruption; recheck changed Issue/PR before closing. Local serialization is not cross-machine distributed locking. |
| Actions permissions | KEEP least privilege | CI contents:read; Pages deployment pages/id-token write; verify issues:write only for evidence. No workflow-wide write token or hosted merge credential. |
| Secrets / variables | REMOVE dependency | Lists empty; existing gh OAuth active with repo/workflow scopes. Do not read/copy tokens or add secrets/activation variable. App model login and GitHub login are separate. |
| 53 tests | KEEP + extend | All 53 freshly pass. Six publisher/retry tests become legacy regressions; lifecycle failures, Git order and shell regressions remain relevant. New tests cover explicit local target, read-only gate, post-Ready races, lock/recovery and Pages contract. |
| main ruleset / CI | KEEP | Ruleset 26702419 active, no bypass actors, strict docs-check/governance-tests bound to Actions 15368, no force/delete, resolved threads, zero approvals. Do not weaken or change settings. |
| #18 / #19 / #20 records | KEEP | Preserve original evidence byte-for-byte. Historical missing-key blockers describe old design only; not rewritten as new success. |

## Actual capabilities and gaps

`gh auth status`: active myaiwouldbemine, HTTPS, existing OAuth repo/workflow scopes (no secret values collected). Git fetch and settings reads succeeded. Git write is to be proven by Plan push, not inferred from login. Current Codex session is operating; do not inspect its credential store or claim independent authentication provenance. Official OpenAI authentication docs support ChatGPT sign-in without an API key: https://learn.chatgpt.com/docs/auth .

Settings read: default Actions token read, cannot approve PRs; no secrets/variables/self-hosted runners; Pages workflow source/HTTPS configured, status null; main-only Pages environment. Native Pages permissions supported by https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages . Hosted merge technically can use appropriately permitted GITHUB_TOKEN but downstream events have restrictions (https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow); local gh merge plus explicit Pages dispatch avoids that dependency. No need to add another token for normal local workflow, subject to actual API enforcement.

Found safety gaps to repair: old executor only rereads head/base before Ready, accepts deployment comments without fresh remote SHA read, and CLI reconciles all matching PRs. Local adapter must not inherit those assumptions. REST merge has expected-head but no atomic expected-base parameter: final reread plus strict up-to-date native checks mitigate, not eliminate, the last base race; disclose limitation.

Architecture comment explicitly prohibits Merge/Deploy/Close during this revision. Full positive lifecycle E2E cannot be executed in this task without violating that boundary. Read-only real GitHub gates, real branch push/CI and injected negative scenarios can be verified; full live E2E remains BLOCKED, PR stays Draft. No new fixture repository, credential, ruleset or governance service will be provisioned to evade the boundary.
