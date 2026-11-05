# LIGHT Governance v1.0

狀態 / Status：設計與建置中；正式 Guarded Auto-Merge 尚未啟用。取代本分支舊版 proposed v1.1。

## Human 與 Agent / Roles
Human Owner 開立 Issue，定義 Goal / WHY / Boundary，處理重大決策與授權例外；不負責例行 PR Review 或 Merge。Codex 與 Claude Code 為對等 Agent，任一方可擔任 Builder，另一方可用時擔任 Independent Reviewer。同一 Agent 的 Self-Review 必須如實標示，不計入 Independent Review；共用 Human GitHub 帳號也不能證明兩個 Agent 身分。
Human owns goals, boundaries and major decisions, not routine reviews or merges. Codex and Claude Code are peers. Self-review and shared GitHub accounts are not evidence of independent review.

## Risk 與 Auto-Merge / Risk policy
Default L0，每項工作依實際影響重分類；路徑分類只是下限，語意風險可提高等級，不可自行降級。
Default is L0; classify actual impact on every task. Path rules establish floors, not a complete semantic assessment.

| Level | 實際影響 / Impact | Merge gates |
|---|---|---|
| L0 | 非教材語意的 typo、局部格式 / nonsemantic typo or formatting | 必要檢查、Risk/Records Gate；免正式 Plan、免獨立 review / required checks; no mandatory plan or independent review |
| L1 | 局部教材、一般 code/site 行為 / local content or behavior | 適用 Build/Content 驗證 + Independent Review；缺席或未完成即 BLOCKED |
| L2 | 重大架構、跨科內容、重要來源鏈 / major architecture or provenance | 正式 Plan/Records + Human Plan authorization + 範圍一致 + L1 gates |
| L3 | 權限、安全、治理控制、部署身分、不可逆或大量刪除 / security, controls, deployment identity, irreversible operations | 預設禁止 Auto-Merge；需針對具體 PR/head 的 Human 授權 + L2 gates |

L0 不新增人工核准或儀式性文件。正式 Plan 一旦存在，即觸發 Records。未能可靠判斷語意風險時升級／阻擋，不以 Default L0 放行。
L0 adds no human approval or ceremonial records. A formal plan always triggers records. Uncertain semantic classification blocks or escalates.

## Plan-triggered records / 計畫紀錄
凡 Builder 為 Issue 建立正式 Plan，必須在 `records/ISSUE-<number>/PLAN.md` 留存；L0 無正式 Plan 可免，L1 有正式 Plan 必存，L2/L3 必須建立。Plan 必須包含 Goal / WHY / Scope / Boundary、Risk Level、Implementation Plan、Acceptance Criteria、Verification Strategy、Human Decisions / Authorization（如適用）與 Revision History。
Every formal plan must be stored in that path. L2/L3 always require one. Include all fields above.

Plan 必須在實作前以獨立 commit 提交至可追溯 branch，並連結 Issue 與 PR。不得完成後補寫假裝事前規劃。修訂保留 Git 歷史；重大 Scope 變更重新取得授權。Validator 需檢查 Git 祖先順序，不接受 PR checkbox 作為證據。既有工作明確記錄 legacy 狀態，不追溯偽造 Plan。
Commit the plan before implementation and link Issue/PR. Preserve revisions; reauthorize material scope changes. Verify ancestry, not checkboxes. Never fabricate retrospective plans.

完成對應實作後，在相同目錄留下 `RESULT.md`，記錄實際結果、驗證證據、PR/Commit、Plan 差異及未完成事項。PR checks/部署可先標 PENDING，後續依真實結果更新，不得預先宣稱 PASS/CLOSED。最終 head 的 check 證據由 GitHub 保存，避免將自己的 SHA 寫入自己造成無限循環。
After implementation, record actual results, evidence, PR/commits, deviations and outstanding work. Pending external checks remain pending; final-head evidence lives in GitHub.

不另強制 Decision Ledger、逐步 Execution Log 或重複文件；Issue/PR/Commit/Checks 是主要執行證據。
No mandatory decision ledger, step log or duplicate evidence documents.

## Verification / 驗證
Build 與 Content 驗證分開。網站變更執行 strict MkDocs build；教材引用核對實際來源與授權，區分 PDF SOURCE、VERIFIED SOURCE CODE、TEACHING EXAMPLE、EXTERNAL VERIFIED、UNVERIFIED。建置成功不代表教材正確、視覺驗收通過或學習者理解。未執行標 NOT RUN，不能標 PASS。
Separate build and content verification. Preserve provenance and licensing; never conflate successful builds with content accuracy or learning outcomes.

## Enforcement / GitHub 強制執行
正式設定與啟用順序見 [activation package](docs/development/GUARDED_AUTO_MERGE.md)。Required CI 必須由可信執行者對精確 head/base 產生，Risk、Review、Records、Authorization 任一失敗、缺失、過期、略過、取消或無法查證均阻擋。Label、PR 描述與 Agent 宣稱只作索引，不是授權或 PASS。不得 bypass ruleset，禁止 force push/delete main，使用 PR 與 squash merge。
Use trusted, exact-head/base checks. Missing, stale, skipped or failed evidence blocks. Labels and declarations are not authorization. Never bypass protections.

## Merge / Deploy separation
Auto-Merge 不等於 Auto-Deploy。PR #1 合併前須先去除 main push 的部署耦合，再完成其未結 review；本次不授權直接合併 PR #1。正式部署另案設計、核准及驗證；不得要求合併前先成功部署同一 commit。此分支 Pages workflow 僅保留手動入口，不代表已授權執行。
Separate merge from deployment. Remove PR #1 push deployment coupling before merge; complete its outstanding review. Production deployment is separately designed, approved and verified.

## Closure Criteria / 結案
所有適用 Gate 必須通過，實際風險及授權有效、阻擋 review 已解決、符合範圍且已合併；有正式 Plan 必須驗證事前 Plan 與 RESULT。部署只有在 Issue 明確列入 Scope 才是 Closure 條件；否則記錄 NOT IN SCOPE，不讓合併等待合併後部署。未完成、待核准或阻擋工作維持 OPEN/BLOCKED，不得宣稱 PASS/CLOSED。
Close only with all applicable gates, valid authorization, resolved blockers, scope compliance, merge, and required records. Deployment is a closure condition only when explicitly in scope. Pending work stays open.

## Rollback / 回復
先停止 merge executor 並撤銷其 credential，保留 required checks 保護；以 revert PR 回復錯誤 commit，不 reset/force push main。部署 rollback 獨立處理，保留既有網站與稽核證據。Policy/Settings 改動均需具體授權。
Stop the executor first; retain protections and revert by PR. Deployment rollback is independent.

## Early Draft PR / 標準工作流程
**Draft Early, Verify Continuously, Review When Ready, Merge Only When Eligible.**

1. Human 開立 Issue，提供 WHAT / WHY / DONE；References 選填。Builder 調查、依實際影響分類 Risk，決定必要 Plan。
2. 有正式 Plan 時，先獨立提交 `records/ISSUE-<number>/PLAN.md`，再實作。L2/L3 必須先取得必要 Plan 核准。提早建立 Draft PR 不構成實作授權。
3. 優先早期建立 Draft PR，作為 CI、Agent Collaboration、Records 與進度追蹤工作空間；持續驗證，不等待 Ready 才跑 CI。
4. Builder 完成實作、適用驗證與必要 RESULT.md 後，才能轉 Ready for Review。沒有正式 Plan 的 L0 不必新增 Records；L0 不強制獨立審查。
5. Ready 後由適用 Independent Review 與 Policy Gates 驗證，符合資格才由 Guarded Auto-Merge 合併。Draft、未完成 CI、未解決 Blocking Review 或缺少授權一律禁止 Merge。
6. Ready 後重大 Scope / Risk 改變，須重新評估 Plan、Review 與授權有效性；必要時轉回 Draft。任何新 head/base 均重新驗證綁定證據，不沿用過期 PASS。

Human supplies WHAT/WHY/DONE; references are optional. Builder investigates and classifies risk. Commit formal plans first and obtain required L2/L3 plan approval before implementation. Open a Draft early for collaboration and continuous verification; a Draft grants no authorization. Mark Ready only after implementation, applicable verification and required Result records are complete. Enforce applicable independent review and policy gates before merge. Draft, incomplete CI, unresolved blockers and missing authorization always block. Reevaluate material scope/risk changes and invalidate stale evidence. L0 gains no additional mandatory records or review.
