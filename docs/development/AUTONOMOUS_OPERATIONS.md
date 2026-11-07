# On-Demand Autonomous Engineering

Human + ChatGPT plan/approve educational content and create an engineering Issue. Human starts Codex App when needed. One recorded accountable Builder handles planning, implementation, tests, Self-Review, PR and gated lifecycle autonomously. No routine Human merge or per-step approval. GOVERNANCE.md and the complete paired bilingual AGENTS.md remain controlling policy.

**繁體中文**

Human 與 ChatGPT 規劃並核准教材內容，並建立工程 Issue。需要時由 Human 啟動 Codex App。一位有明確記錄的 accountable Builder 自主處理規劃、實作、測試、Self-Review、PR 及受閘門管控的生命週期。沒有例行性的 Human 合併或逐步核准。GOVERNANCE.md 與完整成對雙語的 AGENTS.md 仍為具控制力的政策。

繁體中文摘要：按需啟動本機 Builder；保留原有安全與驗證標準。電腦或 App 關閉時不執行新工程，已送出的 GitHub CI／Pages 工作可完成。重啟時讀回遠端實況，不把舊審查當作新 SHA 的證據。教材語義仍由 ChatGPT＋Human 核准。

## Login and execution boundary

Existing App sign-in provides model access; existing `gh auth` provides GitHub access in the local shell. These are separate. [Official authentication documentation](https://learn.chatgpt.com/docs/auth) describes ChatGPT sign-in. Do not inspect credential files or copy tokens into Actions. Check `gh auth status`, repository access and protection with read-only calls; an authenticated account does not prove permission for every mutation. The normal workflow does not require `OPENAI_API_KEY`, `CLH_AUTOMATION_TOKEN` or `CLH_AUTONOMY_ENABLED`.

**繁體中文**

既有的 App 登入提供模型存取；既有的 `gh auth` 在本機 shell 中提供 GitHub 存取。兩者互相獨立。[官方驗證文件](https://learn.chatgpt.com/docs/auth)說明 ChatGPT 登入。不得檢視憑證檔案，也不得將 token 複製到 Actions。以唯讀呼叫檢查 `gh auth status`、Repository 存取權限與保護設定；已通過驗證的帳號並不代表具有每一種變更操作的權限。正常工作流程不需要 `OPENAI_API_KEY`、`CLH_AUTOMATION_TOKEN` 或 `CLH_AUTONOMY_ENABLED`。

Hosted Issue Agent and Autonomous Lifecycle workflows are inert manual-only tombstones with skipped jobs; they cannot react to Issues, CI or schedules. Historical `agent_job.py` library and tests remain for provenance, but its CLI is blocked. No model is launched in GitHub Actions. Use ordinary non-force branch push and PR tools from the active session.

**繁體中文**

Hosted Issue Agent 與 Autonomous Lifecycle workflow 是僅能手動觸發、已失效的墓碑（tombstone）檔案，其 job 皆被略過；它們不會對 Issue、CI 或排程作出反應。歷史性的 `agent_job.py` 函式庫與測試保留作為來源追溯，但其 CLI 已被封鎖。GitHub Actions 中不會啟動任何模型。請在目前 session 中使用一般、非 force 的 branch push 與 PR 工具。

Local lifecycle locking requires WSL/Linux (`fcntl`). It locks the common Git directory across worktrees and releases on process exit/crash. It is not a cross-machine lock; only one accountable Builder may operate on the task at a time. Do not start another machine/session until the outgoing operation's outcome is read back.

**繁體中文**

本機 lifecycle 鎖定需要 WSL／Linux（`fcntl`）。它會鎖定跨 worktree 共用的 Git 目錄，並在程序結束或當機時釋放。它不是跨機器的鎖；同一時間僅可有一位 accountable Builder 對該任務進行操作。在前一個操作的結果被讀回確認之前，不得啟動另一台機器或另一個 session。

## Start, implement and review

1. Read latest Issue WHAT/WHY/DONE/boundary, all comments, PR/head/base, governance and records. Record Builder and scope. Stop for unapproved educational semantics.
2. Reuse the existing Issue branch/PR, or create a `codex/` branch and Draft PR. Never reset away local work or force push. Commit a necessary formal Plan independently before implementation; write Result afterward. Revision records use a new prefix and an explicit revision starting commit.
3. Implement, run applicable tests, strict MkDocs, workflow lint and diff check. Push normally and inspect actual current-head CI. Review actual changes, scope and evidence against full head/base. Changed head/base requires fresh tests/review; unresolved blockers retain Draft.
4. Record actual work, Claim/Source/Method/Evidence, findings, verdict and Fresh-Context Challenge inclusion/omission rationale. Review is Builder Self-Review, not independent approval or identity proof. Do not add complete=true before all applicable work is actually complete.

**繁體中文**

1. 讀取最新的 Issue WHAT／WHY／DONE／邊界、所有留言、PR／head／base、治理文件與記錄。記錄 Builder 與範圍。遇到未核准的教材語義時停止。
2. 重用既有的 Issue branch／PR，或建立 `codex/` branch 與 Draft PR。不得捨棄本機工作（reset），也不得 force push。必要的正式 Plan 須在實作前獨立提交；實作後撰寫 Result。修訂記錄使用新的前綴，並明確標示修訂起始 commit。
3. 實作、執行適用的測試、strict MkDocs、workflow lint 與 diff check。以一般方式 push，並檢視目前 head 的實際 CI。依完整的 head／base 審查實際變更、範圍與證據。head／base 改變時須重新測試並重新審查；未解的阻擋項目須維持 Draft。
4. 記錄實際工作、Claim／Source／Method／Evidence、發現、結論，以及納入或省略 Fresh-Context Challenge 的理由。審查為 Builder Self-Review，不是獨立核准或身分證明。在所有適用工作實際完成之前，不得加入 complete=true。

Normal local commands (replace placeholders with observed values):

**繁體中文**

一般本機命令如下（請將佔位符號替換為實際觀察到的值；命令與上方英文區塊相同，不翻譯）：

```bash
python3 scripts/autonomous_lifecycle.py preflight --repo OWNER/REPO
python3 scripts/autonomous_lifecycle.py check --repo OWNER/REPO --pr NUMBER --head FULL_HEAD_SHA --base FULL_BASE_SHA
```

`check` is read-only on GitHub, including on a merged PR; it does not mark Ready, deploy, archive or close. On an already merged PR it reports only observation, not deployment/closure acceptance. The local advisory lock file is not engineering evidence.

**繁體中文**

`check` 對 GitHub 為唯讀，對已合併的 PR 亦同；它不會標記 Ready、部署、歸檔或結案。對已合併的 PR，它僅回報觀察結果，不代表部署／結案已被接受。本機的 advisory lock 檔案不是工程證據。

## PR evidence contract

After final commit/Self-Review, add exactly one block to the PR body (not a file that changes its own head):

**繁體中文**

在最終 commit／Self-Review 之後，於 PR 描述中加入恰好一個區塊（不是會改變自身 head 的檔案）。區塊內容如上方英文區塊所示，格式不翻譯：

```text
<!-- clh-lifecycle {"issue": 123, "builder": "Codex", "head": "FULL_40_HEX_HEAD", "base": "FULL_40_HEX_MAIN", "issue_body_sha256": "SHA256_OF_EXACT_CURRENT_ISSUE_BODY", "scope_verified": true, "self_review": true, "complete": true, "deployment": true, "evidence": "Actual commands, results, findings, immutable evidence links and scope justification"} -->
```

The block is a Builder record, not an approval token or automatic proof of semantic scope. The digest covers the Issue body; the Builder must separately read all latest comments and stop requests. Do not use auto-closing keywords in PR or commit messages. `Issue: #N` is safe. Site path changes require deployment; non-site tasks do not require unrelated publication.

**繁體中文**

此區塊是 Builder 的記錄，不是核准 token，也不是範圍語義的自動證明。摘要（digest）涵蓋 Issue 內文；Builder 仍須另行讀取所有最新留言與停止要求。不得在 PR 或 commit 訊息中使用自動結案關鍵字。`Issue: #N` 是安全的寫法。網站路徑變更需要部署；非網站任務不需要無關的發布。

## Merge gate and explicit local execution

When the task permits lifecycle execution and all required verification is complete, the Builder autonomously runs:

**繁體中文**

當任務允許執行 lifecycle 且所有必要驗證皆已完成時，Builder 自主執行下列命令（與上方英文區塊相同，不翻譯）：

```bash
python3 scripts/autonomous_lifecycle.py run --repo OWNER/REPO --pr NUMBER --head FULL_HEAD_SHA --base FULL_BASE_SHA
```

One explicit PR and expected full SHAs are mandatory. No broad reconciliation CLI exists. It verifies native main protection, current Issue/PR/scope record, required docs-check/governance-tests, all current check/status results, resolved threads, no requested changes, mergeability and exact head/base. Missing/failing/pending/skipped/cancelled evidence blocks. It marks Ready, rereads state and CI/reviews, then calls the merge API with exact head SHA. GitHub enforces protection; no admin/bypass option is used. Native `allow_auto_merge` is not needed for this direct gated merge.

**繁體中文**

必須指定一個明確的 PR 及預期的完整 SHA。不存在廣泛的 reconciliation CLI。它會驗證原生 main 保護、目前的 Issue／PR／範圍記錄、必要的 docs-check／governance-tests、所有目前的 check／status 結果、已解決的討論串、無要求變更、可合併性，以及精確的 head／base。缺失、失敗、pending、skipped 或 cancelled 的證據皆會阻擋。它會標記 Ready，重新讀取狀態與 CI／review，然後以精確的 head SHA 呼叫 merge API。保護由 GitHub 強制執行；不使用 admin／bypass 選項。此直接受閘門管控的合併不需要原生的 `allow_auto_merge`。

REST has no atomic expected-base input. Fresh base reads and strict native up-to-date checks mitigate the final race; they are not a distributed transaction binding Self-Review to an immutable base. The Builder must not claim stronger guarantees. An ambiguous network outcome requires remote merge readback before retry. No automatic network mutation retries occur.

**繁體中文**

REST 沒有原子性的預期 base 輸入。重新讀取 base 以及嚴格的原生 up-to-date 檢查可降低最後的競態風險；但它們不是將 Self-Review 綁定到不可變 base 的分散式交易。Builder 不得宣稱更強的保證。網路結果不明確時，須先讀回遠端的合併狀態再重試。不會自動重試網路變更操作。

## Pages and SHA readback

For website work, the first run merges and reports deployment PENDING, keeping the Issue open. Watch the Pages push run for the exact merge SHA. For recovery while that SHA is still main, the Builder can retry manually:

**繁體中文**

對於網站工作，第一次執行會進行合併並回報部署為 PENDING，Issue 保持開啟。請監看該精確 merge SHA 對應的 Pages push run。若要在該 SHA 仍為 main 時進行復原，Builder 可手動重試（命令與上方英文區塊相同，不翻譯）：

```bash
gh workflow run pages.yml --repo OWNER/REPO --ref main -f expected_sha=FULL_MERGE_SHA
```

This is a Builder engineering action, not a Human approval step. The workflow must first be installed on main. Both events verify current main, effective native protection and the exact merged main PR. Dispatch additionally requires the expected SHA. Every valid protected merge publishes the current tree so consecutive merges can coalesce. Lifecycle deployment metadata controls Issue evidence. The local Builder checks the private bypass list. An advanced main blocks old-SHA dispatch; investigate and prepare a current reviewed recovery PR rather than falsely crediting another SHA. Pages jobs serialize, build strict MkDocs, embed `deployment-sha.txt`, upload artifact and deploy with native GITHUB_TOKEN/OIDC (`pages:write`, `id-token:write` only deployment job). No off-device AI runs.

**繁體中文**

這是 Builder 的工程動作，不是 Human 核准步驟。該 workflow 必須已安裝在 main 上。兩種事件皆會驗證目前的 main、有效的原生保護，以及精確的已合併 main PR。手動觸發另外要求提供預期 SHA。每一次有效的受保護合併都會發布目前的 tree，因此連續合併可以合併為一次發布。Lifecycle 的部署中繼資料控制 Issue 證據。本機 Builder 檢查私有的 bypass 清單。若 main 已前進，則舊 SHA 的手動觸發會被阻擋；應調查並準備目前的已審查復原 PR，而不是錯誤地將功勞歸給其他 SHA。Pages job 為序列化執行、以 strict MkDocs 建置、嵌入 `deployment-sha.txt`、上傳 artifact，並使用原生 GITHUB_TOKEN／OIDC 部署（僅部署 job 擁有 `pages:write`、`id-token:write`）。不會執行任何機外 AI。

The verify job reads the configured HTTPS Pages URL with bounded retries and checks homepage status and SHA bytes. Only a lifecycle PR requiring deployment receives a merge-SHA/run marker on its reviewed Issue. The local Builder observes the exact run to completion, then repeats the targeted `run` command with the original reviewed head/base. Already merged PRs reuse their merge SHA; no second merge. The executor verifies successful Pages workflow path/main/merge SHA, configured URL and **fresh remote SHA bytes** before archival. A marker alone is insufficient. Deployment denial, failed run, stale published bytes or missing evidence leave the Issue open.

**繁體中文**

verify job 以有限次數重試讀取已設定的 HTTPS Pages URL，並檢查首頁狀態與 SHA 位元組。只有需要部署的 lifecycle PR，才會在其已審查的 Issue 上取得 merge-SHA／run 標記。本機 Builder 觀察該精確 run 直到完成，然後以原本已審查的 head／base 重複執行指定的 `run` 命令。已合併的 PR 沿用其 merge SHA；不會再次合併。執行器在歸檔前會驗證 Pages workflow 成功、路徑／main／merge SHA、已設定的 URL，以及**最新讀取的遠端 SHA 位元組**。僅有標記並不足夠。部署被拒、run 失敗、已發布位元組過期或證據缺失時，Issue 保持開啟。

[GitHub Pages workflow documentation](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages) supports native token/OIDC deployment. [GitHub event documentation](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow) explains GITHUB_TOKEN downstream-event restrictions; the protected merge uses the local Builder’s existing gh identity so its push triggers Pages.

**繁體中文**

[GitHub Pages workflow 文件](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)支援以原生 token／OIDC 部署。[GitHub 事件文件](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow)說明 GITHUB_TOKEN 對下游事件的限制；受保護的合併使用本機 Builder 既有的 gh 身分，因此其 push 會觸發 Pages。

## Archive, close and interruption recovery

Archive uses PR + full merge SHA as a stable key, stores separate merge/deployment/closure results and reads the exact comment back. Changed archive data blocks rather than overwriting. Current Issue digest and PR evidence are checked again before close; then the Issue's closed state is read back. These records do not imply learning mastery or content approval.

**繁體中文**

歸檔以 PR 加完整 merge SHA 作為穩定鍵，分別儲存 merge／deployment／closure 的結果，並讀回該確切留言。歸檔資料若有變動則阻擋，不覆寫。結案前會再次檢查目前的 Issue digest 與 PR 證據；之後讀回 Issue 的已關閉狀態。這些記錄並不代表學習掌握或教材核准。

| Interrupted stage | Resume action |
|---|---|
| Editing / before push | Inspect worktree and commits; preserve work, reread scope/head/base, test and push normally |
| Pushed / CI pending | Read actual new-head CI; fix bounded failures and invalidate stale review |
| Ready or merge request with lost response | Fetch PR; if unmerged revalidate all gates, if merged use existing merge SHA |
| Merged / Pages pending | Follow the exact push run. Retry only after inspecting the failure and confirming current main. A manual retry provides recovery evidence only |
| Pages running / App off | Existing job may finish; next session reads run and remote SHA |
| Archive write/close response lost | Read existing merge-SHA archive, verify bytes, reuse it, then read Issue state |
| Conflicting archive / changed requirements | Stop, record blocker; no overwrite, duplicate merge or false closure |

**繁體中文**

| 中斷的階段 | 恢復動作 |
|---|---|
| 編輯中／push 之前 | 檢查 worktree 與 commit；保留工作、重新讀取範圍／head／base、測試並以一般方式 push |
| 已 push／CI pending | 讀取新 head 的實際 CI；修正有限的失敗，並使過時的審查失效 |
| Ready 或合併請求的回應遺失 | 取得 PR；若尚未合併則重新驗證所有閘門，若已合併則使用既有的 merge SHA |
| 已合併／Pages pending | 追蹤精確的 push run。僅在檢查失敗原因並確認目前 main 後才重試。手動重試僅提供復原證據 |
| Pages 執行中／App 已關閉 | 既有 job 可完成；下一個 session 讀取 run 與遠端 SHA |
| 歸檔寫入／結案回應遺失 | 讀取既有的 merge-SHA 歸檔、驗證位元組並重用，然後讀取 Issue 狀態 |
| 歸檔衝突／需求已變更 | 停止並記錄阻擋；不覆寫、不重複合併、不錯誤結案 |

For an unchanged failure, record at most three repair attempts with cause/action/outcome before leaving BLOCKED. New investigation or changed conditions can justify a new bounded attempt; merely restarting App does not erase the record. If permissions prevent posting blocker evidence, keep local output and push a record when permitted. Error logs must not expose raw tokens/API secrets. Do not run other Builder sessions concurrently; comment APIs offer no atomic create-if-absent guarantee across machines.

**繁體中文**

對於未改變的失敗，在標示為 BLOCKED 之前，最多記錄三次修復嘗試，包含原因／動作／結果。新的調查或改變的條件可以支持新的有限嘗試；僅重新啟動 App 不會抹除記錄。若權限使 blocker 證據無法張貼，保留本機輸出，並在允許時 push 一份記錄。錯誤日誌不得暴露原始 token／API 機密。不得同時執行其他 Builder session；留言 API 不提供跨機器的原子性「不存在才建立」保證。

## Installation, acceptance and rollback

Keep CI contents:read and main PR-only, strict required checks, resolved threads, no bypass/force/delete. Pages source must be Actions and its environment main-only. Read settings rather than assuming documentation configures them. Do not add credentials, expand scopes or weaken rules to make validation pass.

**繁體中文**

維持 CI 為 contents:read、main 僅允許 PR、嚴格的必要檢查、已解決的討論串，以及不允許 bypass／force／刪除。Pages 來源須為 Actions，且其 environment 僅限 main。請讀取實際設定，而非假設文件已完成設定。不得為了使驗證通過而新增憑證、擴大權限範圍或放寬規則。

Issue #20 / PR #21 records the on-demand lifecycle implementation. Issue #22 / PR #23 records automatic Pages publication. Verify each subsequent merge against its own checks, run and published SHA.

**繁體中文**

Issue #20／PR #21 記錄按需 lifecycle 的實作。Issue #22／PR #23 記錄自動 Pages 發布。後續每次合併，皆須依其自身的檢查、run 與已發布 SHA 進行驗證。

Before merge, stopping the session causes no production installation. After future installation, stop local operations, inspect/cancel affected queued Pages jobs, then use a tested revert PR with current Self-Review/required CI and normal merge. Redeploy and read back the revert SHA for website recovery. Do not restore hosted agent/scheduler or the obsolete premature-close path as an active rollback. Git revert does not undo remote settings. Keep the Issue open until recovery evidence is archived and read back; never rewrite history.

**繁體中文**

合併之前，停止 session 不會造成任何正式環境的安裝。未來安裝之後，須停止本機操作、檢查／取消受影響且排隊中的 Pages job，然後使用經過測試的 revert PR，並具備目前的 Self-Review／必要 CI，再以一般方式合併。網站復原須重新部署並讀回 revert SHA。不得將 hosted agent／排程器或已過時的提前結案路徑恢復為有效的回復手段。Git revert 不會還原遠端設定。在復原證據歸檔並讀回之前，Issue 保持開啟；絕不重寫歷史。
