> **ARCHIVED / NOT ACTIVE.** Superseded by Minimal Governance. C3–C5 and later platform implementation are stopped. The original proposal/evidence below is preserved, not current policy or authorization. Prototype code/tests formerly under scripts/ are retained under archive/governance-platform/scripts/.

**繁體中文**

> **已封存／非現行有效。** 已被 Minimal Governance 取代。C3–C5 及之後的平台實作已停止。以下原始提案／證據僅為保存，不是現行政策或授權。原先位於 scripts/ 下的原型程式碼／測試保留於 archive/governance-platform/scripts/。

# Guarded Auto-Merge — one-time activation approval package

Status: PROPOSED / NOT ENABLED. Issue #4. This is L3 control-plane work.

**繁體中文**

狀態：PROPOSED（已提議）／NOT ENABLED（未啟用）。Issue #4。這是 L3 control-plane 工作。

## Proposed gates and executors

| Required context | Executor / evidence | Failure rule |
|---|---|---|
| `light/risk-authorization` | Dedicated Policy GitHub App: GitHub API full paginated diff, trusted base policy, independently classified semantic impact; L2/L3 authenticated Human authorization | Unknown risk, truncated diff, unauthorized scope or stale binding blocks |
| `light/records` | Policy App runs base-pinned record verifier on Git objects; classifier supplies formal-plan flag and Issue ID | Formal plan missing, incomplete or not committed before implementation, missing Result or unapproved deviation blocks |
| `light/review` | Policy App validates independent reviewer attestation, actual reviewer credential and builder identity | L0 emits verified NOT_REQUIRED success; L1+ missing/unavailable/pending/self/stale review blocks |
| `light/build-content` | Policy App verifies completed trusted validation runs and applicable content-review evidence | No applicable build may be explicitly NOT_REQUIRED; required build/content must actually pass; skip/cancel/timeout/unknown block |

**繁體中文**

| 必要 context | 執行者／證據 | 失敗規則 |
|---|---|---|
| `light/risk-authorization` | 專用 Policy GitHub App：取得 GitHub API 完整分頁 diff、可信 base 政策、獨立分類的語義影響；L2/L3 須經驗證的 Human 授權 | 風險未知、diff 被截斷、範圍未授權或綁定過期，皆阻擋 |
| `light/records` | Policy App 對 Git 物件執行以 base 固定版本的記錄驗證器；分類器提供正式 plan 旗標與 Issue ID | 缺少正式 plan、不完整或未在實作前提交、缺少 Result 或有未核准的偏離，皆阻擋 |
| `light/review` | Policy App 驗證獨立 reviewer 的 attestation、實際 reviewer 憑證及 Builder 身分 | L0 發出經驗證的 NOT_REQUIRED 成功；L1+ 缺少／無法取得／pending／自審／過期的審查，皆阻擋 |
| `light/build-content` | Policy App 驗證已完成的可信驗證 run 及適用的教材審查證據 | 無適用的 build 時可明確標為 NOT_REQUIRED；必要的 build／教材必須實際通過；skip／cancel／timeout／未知，皆阻擋 |

Policy App publishes checks on the current PR head only after verifying current base and all evidence. App ID is pinned in ruleset required check integration_id. Ordinary Actions and Builder cannot publish Policy App checks. No production check may accept a fixture/snapshot or PR-supplied policy code as evidence.

**繁體中文**

Policy App 僅在驗證目前 base 與所有證據之後，才會在目前的 PR head 上發布 check。App ID 固定於 ruleset 必要 check 的 integration_id。一般 Actions 與 Builder 不能發布 Policy App 的 check。任何正式環境的 check 都不得接受 fixture／snapshot 或 PR 提供的政策程式碼作為證據。

### Identity and attestation contract
Separate Builder, Codex Reviewer and Claude Reviewer service identities; a shared Human token cannot prove independence. Reviewer service signs an attestation containing repository, PR, head SHA, base SHA, builder identity, reviewer identity, verdict, scope-diff digest and evidence links. The Policy App verifies registered issuer keys and that reviewer agent differs from builder agent. Fail if the reviewer service cannot be provisioned; do not substitute self-review. Credential isolation is required: Builder must not hold reviewer, Policy App or merge executor credentials.

**繁體中文**

Builder、Codex Reviewer 與 Claude Reviewer 使用各自獨立的服務身分；共用的 Human token 無法證明獨立性。Reviewer 服務簽署一份 attestation，內容包含 repository、PR、head SHA、base SHA、Builder 身分、Reviewer 身分、verdict、範圍 diff 摘要（digest）及證據連結。Policy App 驗證已註冊的簽發者金鑰，並驗證 reviewer agent 與 builder agent 不同。若無法佈建 reviewer 服務則失敗；不得以自審取代。必須有憑證隔離：Builder 不得持有 reviewer、Policy App 或 merge executor 的憑證。

Human L2 authorization is an authenticated Issue comment from the configured owner, approving the exact Plan Git blob and allowed paths/operations/acceptance criteria. Collector records comment ID, author ID, Plan blob, scope digest and time; re-fetch before merge. L3 additionally requires exact PR/head authorization and explicit auto-merge permission. Edited/deleted/revoked authorization invalidates eligibility. Human approval of this activation package is not blanket L3 approval for future PRs. Agent-written records cannot create authorization.

**繁體中文**

Human L2 授權是由已設定的擁有者所發出、經驗證的 Issue 留言，核准精確的 Plan Git blob 以及允許的路徑／操作／驗收標準。Collector 記錄留言 ID、作者 ID、Plan blob、範圍摘要與時間；合併前重新取得。L3 另外要求精確的 PR／head 授權及明確的 auto-merge 權限。被編輯／刪除／撤銷的授權使資格失效。Human 對本啟用套件的核准不是對未來 PR 的概括性 L3 核准。Agent 撰寫的記錄不能產生授權。

L0 eligibility is deliberately narrow: trusted classifier verifies actual nonsemantic edits, not merely Markdown extensions. Lesson meaning, examples, executable code and site behavior are at least L1; important source/provenance rewrites or broad architecture changes at least L2; workflow/policy/permission/deploy controls at least L3. Bulk deletion/unknown file types block for classification. No new Human paperwork for ordinary L0; if no trusted semantic classifier is available, hold eligibility rather than guess L0. All formal plans trigger records even at L0/L1; creating a plan outside records is a policy violation, not an exemption. Semantic review must detect this; a Git path checker alone cannot.

**繁體中文**

L0 資格刻意設得很窄：可信分類器驗證實際為非語義的編輯，而不僅是看 Markdown 副檔名。課程意義、範例、可執行程式碼與網站行為至少為 L1；重要的來源／出處改寫或廣泛的架構變更至少為 L2；workflow／政策／權限／部署控制至少為 L3。大量刪除／未知檔案類型須阻擋以待分類。一般 L0 不增加新的 Human 文書作業；若沒有可信的語義分類器，則暫停資格而不是猜測為 L0。所有正式 plan 即使在 L0／L1 也會觸發記錄檢查；在 records 之外建立 plan 屬於政策違規，不是豁免。必須由語義審查偵測此情況；僅靠 Git 路徑檢查器無法做到。

## Branch ruleset (to apply after approval and observed check runs)
Target refs/heads/main; enforcement active; bypass_actors empty. Require PR; zero global required approvals (risk-specific App gate handles L1+ without burdening L0); require resolved conversations; block deletion and non-fast-forward. Require the four contexts above from the dedicated Policy App; strict up-to-date policy. Squash merge only. Archive actual API request and response in Issue #4 evidence; re-read effective rules including inherited rules. If repository plan cannot enforce required checks/App source, activation is BLOCKED.

**繁體中文**

目標為 refs/heads/main；enforcement 為 active；bypass_actors 為空。要求 PR；全域必要核准數為零（依風險的 App 閘門處理 L1+，不增加 L0 的負擔）；要求討論已解決；阻擋刪除與非 fast-forward。要求上述四個 context 來自專用 Policy App；採嚴格 up-to-date 政策。僅允許 squash merge。將實際的 API 請求與回應歸檔於 Issue #4 證據；重新讀取有效規則，包含繼承而來的規則。若 repository 方案無法強制執行必要 check／App 來源，則啟用為 BLOCKED。

Required contexts must first be observed in real canary runs before making them required. Check-name presence alone does not establish trust; verify App identity, exact head/base and run identity. Query all pages. Duplicate unexpected check writers are a failure.

**繁體中文**

必要 context 必須先在真實的 canary run 中被觀察到，才能設為必要。僅有 check 名稱存在不足以建立信任；須驗證 App 身分、精確的 head／base 及 run 身分。查詢所有分頁。出現非預期的重複 check 寫入者即為失敗。

## Permissions and guarded merge mechanism
- Builder: contents write on topic branches and PR write; no administration, environments, checks write or protected-branch bypass.
- Reviewer service: read repository and independent review/attestation; no merge or admin permission.
- Policy GitHub App: contents/read, PR/read, issues/read, actions/read, checks/write, metadata/read; no contents/write or administration. Private key kept outside Builder access.
- Merge executor GitHub App: contents/write and PR/write only; no admin, Pages, OIDC, secrets or bypass. Before each merge, read fresh PR/head/base, authenticated policy evidence, all required checks, unresolved threads and blocking reviews. Require all conclusions success with matching head/base and trusted App; reject drafts, forks until explicitly supported, conflicts, unknown mergeability, authorization revocation or disabled activation flag. Serialize execution and use GitHub merge API with expected head SHA and squash. GitHub's strict ruleset is the final atomic guard against base movement. On mismatch/409/405, stop and re-evaluate; never retry using admin bypass.
- Dedicated executor performs an automatic guarded merge; native auto-merge is not needed and remains disabled to avoid an alternate pending merge path. Human does not merge each eligible PR.

**繁體中文**

- Builder：在 topic branch 上有 contents write、PR write；無 administration、environments、checks write 或受保護分支 bypass。
- Reviewer 服務：讀取 repository 與獨立審查／attestation；無 merge 或 admin 權限。
- Policy GitHub App：contents/read、PR/read、issues/read、actions/read、checks/write、metadata/read；無 contents/write 或 administration。私鑰置於 Builder 無法存取之處。
- Merge executor GitHub App：僅有 contents/write 與 PR/write；無 admin、Pages、OIDC、secrets 或 bypass。每次合併前，讀取最新的 PR／head／base、經驗證的政策證據、所有必要 check、未解決的討論串與阻擋性的 review。要求所有結論為 success，且 head／base 與可信 App 相符；拒絕 draft、fork（在明確支援之前）、衝突、未知的可合併性、授權已撤銷或啟用旗標已停用。序列化執行，並使用附帶預期 head SHA 的 GitHub merge API 與 squash。GitHub 的嚴格 ruleset 是防止 base 移動的最終原子性防護。遇到不符／409／405 時，停止並重新評估；絕不使用 admin bypass 重試。
- 專用執行器執行自動的受控合併；不需要原生 auto-merge，並保持停用，以避免出現另一條待決的合併路徑。Human 不須逐一合併符合資格的 PR。

Use webhook events for PR synchronize, base pushes, reviews/dismissals, Issue authorization edits/deletions, check completion and rules changes; also reconcile pending PRs periodically for missed webhooks. Invalidate eligibility on new head/base before reevaluation. Production service code, transport, key provisioning and authenticated runtime integration remain to be built/verified after this architecture is approved; the local record verifier is not that service.

**繁體中文**

針對 PR synchronize、base push、review／dismissal、Issue 授權的編輯／刪除、check 完成與規則變更使用 webhook 事件；並定期對待決的 PR 進行 reconcile，以處理漏掉的 webhook。在重新評估前，遇到新的 head／base 時，須在重新評估前立即使資格失效。正式環境的服務程式碼、傳輸、金鑰佈建與經驗證的執行期整合，在本架構被核准後仍須建置／驗證；本機記錄驗證器不是該服務。

## Failure blocking and rollback
Missing API permission, pagination failure, service outage, unavailable reviewer, stale result, revoked auth, incomplete records, check skip/fail/cancel or mismatched issuer => no merge, report exact blocker in PR/check. A single kill switch stops executor; revoke its installation token/private key if compromised. Do not remove required checks to unstick PRs. Disable any queued native auto-merge if one exists. Keep ruleset active; use a revert PR for code rollback. Preserve logs and previous Pages site. Never rewrite main history. Emergency bypass requires specific Human incident authorization and an audit record.

**繁體中文**

缺少 API 權限、分頁失敗、服務中斷、reviewer 無法取得、結果過期、授權被撤銷、記錄不完整、check 被 skip／fail／cancel，或簽發者不符 => 不合併，並在 PR／check 中回報確切的阻擋原因。不得為了讓 PR 通過而移除必要 check。若有排隊中的原生 auto-merge，須停用之。保持 ruleset 為 active；程式碼回復使用 revert PR。保留日誌與先前的 Pages 網站。絕不重寫 main 歷史。緊急 bypass 需要具體的 Human 事件授權及稽核記錄。

## PR #1 / deployment dependency resolution
Observed 2026-11-05: PR #1 open at 06e5526; description says second independent review pending; Pages API 404; repository rulesets []. No runtime Pages success established. Existing pages.yml deploys on main push, so merging can publish unexpectedly.
This branch removes push trigger and retains manual entry only. Before PR #1 merges, transplant that isolated change to its branch (or supersede PR #1 with this branch), obtain independent re-review and rerun its Docs Check. Confirm diff on the actual merge candidate. No current authorization to merge or deploy PR #1 is inferred. Manual Pages invocation also needs separate deployment authorization. Do not require post-merge Pages success as a pre-merge check.
Production deployment strategy, environment protection, artifact identity, permissions and rollback need a separate approved plan and real deployment test. Never enable unattended merges until PR #1 coupling and review are actually resolved.

**繁體中文**

2026-11-05 觀察：PR #1 處於開啟狀態，head 為 06e5526；描述指出第二次獨立審查待辦；Pages API 回傳 404；repository rulesets 為 []。尚未建立任何執行期 Pages 成功證據。既有的 pages.yml 在 main push 時部署，因此合併可能意外發布。
本分支移除 push 觸發器，僅保留手動入口。在 PR #1 合併之前，須將該隔離的變更移植到其分支（或以本分支取代 PR #1）、取得獨立重新審查，並重新執行其 Docs Check。須在實際的合併候選上確認 diff。不從現況推論出任何合併或部署 PR #1 的授權。手動呼叫 Pages 也需要另外的部署授權。不得將合併後 Pages 成功列為合併前的必要檢查。

## End-to-end acceptance and enablement sequence
1. Human approves this package once, including App identities, exact permissions, no-bypass ruleset and tests. Capture authenticated approval. Keep executor disabled.
2. Complete/provision trusted services and issuer registration; independent control-plane review. Dry-run on real canary PRs; publish checks without merging; verify actual App IDs and effective repository rules.
3. L0 typo/no plan: no new paperwork/reviewer, all gates succeed. L1 valid independent content/build evidence succeeds. L2 approved Plan/scope succeeds. L3 blocks until head-specific approval.
4. Negative canaries: missing/unavailable reviewer; Builder posing as reviewer; forged PASS label/comment/check; skipped/cancelled/failed CI; missing Plan/Result; Plan committed with/after implementation; plan outside records; changed Plan blob/scope; authorization deleted/edited/revoked; new head/base after review; duplicate check issuer; API outage; unresolved thread/CHANGES_REQUESTED; draft; conflict. Every case must refuse merge.
5. Attempt direct push, force push, branch delete and merge with a failing required App check using ordinary Builder/executor identities. All denied. Validate race by changing head/base between decision and merge. No admin bypass.
6. Exercise kill switch and revoke credentials; verify no pending PR merges. Revert a canary via PR without deployment. Record actual URLs, SHAs, API responses and check runs in RESULT; do not mark unrun tests PASS.
7. Resolve PR #1 dependency and deployment trigger issue, prove merging does not start Pages. Only then enable executor and observe one eligible canary auto-merge and one blocked PR. Report results. Human involvement thereafter is major decisions, authorization exceptions and unsolved blockers.

**繁體中文**

1. Human 一次性核准本套件，包含 App 身分、精確權限、無 bypass 的 ruleset 與測試。擷取經驗證的核准。執行器保持停用。
2. 完成／佈建可信服務與簽發者註冊；獨立的 control-plane 審查。在真實的 canary PR 上 dry-run；發布 check 但不合併；驗證實際的 App ID 與有效的 repository 規則。
3. L0 錯字／無 plan：無新增文書作業／reviewer，所有閘門成功。L1 具有效的獨立教材／build 證據則成功。L2 具已核准的 Plan／範圍則成功。L3 在取得特定 head 核准前阻擋。
4. 負面 canary：缺少／無法取得 reviewer；Builder 冒充 reviewer；偽造的 PASS 標籤／留言／check；skip／cancel／失敗的 CI；缺少 Plan／Result；Plan 與實作一起或之後才提交；plan 位於 records 之外；Plan blob／範圍改變；授權被刪除／編輯／撤銷；審查後出現新 head／base；重複的 check 簽發者；API 中斷；未解決的討論串／CHANGES_REQUESTED；draft；衝突。每個案例都必須拒絕合併。
5. 以一般 Builder／executor 身分嘗試直接 push、force push、刪除分支，以及在必要 App check 失敗時合併。全部皆被拒絕。藉由在決策與合併之間改變 head／base 驗證競態。不使用 admin bypass。
6. 演練 kill switch 並撤銷憑證；驗證沒有待決的 PR 被合併。透過 PR 回復一個 canary，且不部署。在 RESULT 中記錄實際的 URL、SHA、API 回應與 check run；未執行的測試不得標為 PASS。
7. 解決 PR #1 的耦合與部署觸發問題，證明合併不會啟動 Pages。之後才啟用執行器，並觀察一次符合資格的 canary 自動合併與一次被阻擋的 PR。回報結果。此後 Human 的參與限於重大決策、授權例外與未解的阻擋問題。

Approval request covers the concrete design and subsequent implementation/settings/testing sequence above. It does not authorize deployment or routine bypass. Any inability to provision trustworthy independent identities is an explicit blocker, not permission to weaken gates.

**繁體中文**

核准請求涵蓋上述具體設計及後續的實作／設定／測試順序。它不授權部署或例行的 bypass。無法佈建可信的獨立身分，是明確的阻擋，不是放寬閘門的許可。

## Primary references
- https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets
- https://docs.github.com/en/actions/reference/security/securely-using-pull_request_target
- https://docs.github.com/en/rest/pulls/pulls#merge-a-pull-request

Privileged services must never execute PR code. The local verifier reads Git blobs only and its syntax checks cannot establish content correctness or authenticated authorization.

**繁體中文**

具特權的服務絕不得執行 PR 程式碼。本機驗證器僅讀取 Git blob，其語法檢查無法確立內容的正確性或經驗證的授權。

## Conditional approval revision — 2026-11-05
Human authorized implementation/configuration/tests, but explicitly withheld production activation. Early Draft PR is the standard workspace; Ready requires completed implementation, applicable verification and Result records. Drafts always block merging even when CI passes. New material scope/risk changes require reevaluation. No extra L0 records/reviewer.

**繁體中文**

Human 授權實作／設定／測試，但明確保留正式環境啟用。提早建立 Draft PR 是標準工作區；Ready 要求實作完成、適用的驗證及 Result 記錄。即使 CI 通過，Draft 一律阻擋合併。新的重大範圍／風險變更須重新評估。L0 不增加額外記錄／reviewer。

### Native simplification assessment
Use native PR Draft state, conversation resolution, no-bypass Ruleset, exact-SHA squash merge and GitHub Actions for unprivileged tests. These eliminate a custom workflow state database and custom build service. Propose **one control-plane App installation** combining policy publication and the disabled merge executor, with one required `light/eligible` check containing risk/authorization, records, review and build/content subresults. This replaces four required contexts and separate Policy/Executor Apps without allowing Builder to mint this App's checks. App gets contents/write, PR/write, checks/write, issues/read and actions/read; no administration/Pages/OIDC/bypass. The previous read-only Policy App privilege boundary is traded for a single trusted control plane; this revision requires independent review before adoption. Never give its key to Builder. Reviewer still needs separate authenticated issuer identity; native approvals from the shared Human account cannot establish agent independence. A single reconciliation loop can poll GitHub and re-fetch before merge; webhooks are an optional latency optimization, not a separate required service.

**繁體中文**

使用原生的 PR Draft 狀態、討論解決、無 bypass 的 Ruleset、精確 SHA 的 squash merge，以及用於無特權測試的 GitHub Actions。這些可免去自訂的 workflow 狀態資料庫與自訂 build 服務。提議**單一 control-plane App 安裝**，結合 policy 發布與已停用的 merge executor，並以單一必要的 `light/eligible` check 包含 risk/authorization、records、review 與 build/content 的子結果。此做法取代四個必要 context 以及分開的 Policy／Executor App，同時不允許 Builder 產生此 App 的 check。App 取得 contents/write、PR/write、checks/write、issues/read 與 actions/read；無 administration／Pages／OIDC／bypass。先前唯讀 Policy App 的權限邊界換成單一可信 control plane；此修訂在採用前需要獨立審查。絕不將其金鑰交給 Builder。Reviewer 仍需獨立且經驗證的簽發者身分；共用 Human 帳號的原生核准無法確立 agent 的獨立性。單一 reconciliation 迴圈可輪詢 GitHub 並於合併前重新取得；webhook 是選用的延遲最佳化，不是另外必要的服務。

Current executable lifecycle helper is intentionally not the trusted collector, semantic classifier or authorization layer. Governance Tests CI exercises PR code with read-only credentials; it is **not** the trusted eligibility check and must never satisfy `light/eligible`. GitHub native capability cannot independently authenticate which model performed a review under one shared account. No trustworthy reviewer credential or App installation key has been provisioned in this work; do not invent one or reuse the Human token as the service identity.

**繁體中文**

目前可執行的 lifecycle helper 刻意不是可信的 collector、語義分類器或授權層。Governance Tests CI 以唯讀憑證執行 PR 程式碼；它**不是**可信的資格 check，絕不得滿足 `light/eligible`。GitHub 原生功能無法在共用帳號下獨立驗證是哪個模型執行了審查。在本工作中未佈建任何可信的 reviewer 憑證或 App 安裝金鑰；不得捏造，也不得將 Human token 重用為服務身分。

Live canary Ruleset 26612260 targets only `canary/light-enforcement-issue-4`, active with empty bypass list. GitHub rejected direct ref update and branch deletion (422), ref unchanged. Effective rules and responses are in records/ISSUE-4/canary-enforcement.json. Required-check source isolation, merge denial, force-push denial and production main enforcement remain NOT RUN. Canary protection is retained; no protection was lowered for cleanup. Production native auto-merge remains false. Rollback/executor kill switch remains NOT RUN because no executor is provisioned.

**繁體中文**

實際的 canary Ruleset 26612260 僅以 `canary/light-enforcement-issue-4` 為目標，狀態 active，bypass 清單為空。GitHub 拒絕直接更新 ref 與刪除分支（422），ref 未改變。有效規則與回應位於 records/ISSUE-4/canary-enforcement.json。必要 check 來源隔離、合併拒絕、force-push 拒絕與正式 main 的強制執行仍為 NOT RUN。Canary 保護予以保留；為了清理並未降低任何保護。正式環境的原生 auto-merge 仍為 false。因未佈建 executor，回復／executor kill switch 仍為 NOT RUN。

PR #1 actual branch now has pre-change Plan commit 0b180ff and deployment-trigger fix f4a429c. Verify its CI at that head. This fixes the actual candidate's push trigger, but outstanding independent review and any merge/runtime acceptance remain separate blockers. No deployment or merge has occurred.

**繁體中文**

PR #1 的實際分支現在有變更前的 Plan commit 0b180ff 與部署觸發修正 f4a429c。須驗證該 head 的 CI。這修正了實際候選的 push 觸發器，但尚未完成的獨立審查，以及任何合併／執行期驗收，仍是各自獨立的阻擋項目。目前沒有發生任何部署或合併。
