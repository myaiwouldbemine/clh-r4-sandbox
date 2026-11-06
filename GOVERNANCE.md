# LIGHT Governance v2 — Minimal Learning Hub

目前採用極簡治理，轉向 Claude Code Single-Builder + Self-Verification 模式。唯一 Human 管理者為 myaiwouldbemine；Claude Code 為指定 Builder。本文件是現行政策；歷史平台與 Canary 設計為 Archived / Not Active，不構成執行授權。

## 工作流程
Issue → Draft PR → Plan（必要時）→ Implementation → Result（必要時）→ Review → Merge。
Issue 說明 WHAT / WHY / DONE 與邊界。提早建立 Draft、持續執行 CI；Draft 不等於實作授權，也不能 Merge。
Builder 依實際影響判定風險。文件不一定是 L0；教材語意修改至少 L1。風險無法判定時先釐清，不以 L0 放行。

## 風險與記錄
| 等級 | 適用範圍 | 必要條件 |
|---|---|---|
| L0 | 錯字、格式等非語意修改 | 適用驗證；免強制 Plan／Result／獨立 Review |
| L1 | 教材語意、一般程式或網站行為 | 適用驗證＋不同 Agent 的可追溯交叉 Review |
| L2 | 重大架構、跨科教材、重要來源鏈 | L1 條件＋事前 Plan／事後 Result＋Human 明確核准 Plan 與範圍 |
| L3 | 權限、安全、治理控制、部署、不可逆或大量刪除 | L2 條件＋Human 對具體操作／候選變更逐項授權 |

L0／L1 沒有正式 Plan 時，不強制新增記錄。若自願建立正式 Plan，須保留對應 Result。
正式 Plan 存於 records/ISSUE-<number>/PLAN.md，包含 Goal、WHY、Scope、Boundary、Risk Level、Implementation Plan、Acceptance Criteria、Verification Strategy、Human Decisions、Revision History，並連結 Issue。
Plan 在對應實作前獨立 commit；L2／L3 必要的 Human 核准先於實作。不得回填假裝事前規劃。
實作後更新同目錄 RESULT.md，記錄 Results、Evidence、PR、Commit、Deviations、Unfinished。未執行寫 NOT RUN，外部檢查待定寫 PENDING。

## Self-Review 與 Verification
Claude Code Builder 負責 Investigation、Plan、Implementation、Self-Review、Tests、Evidence、Result 與 Readback。
Self-Review 須以可追溯 Evidence 支持，包含 Claim、Source、Method、Evidence 及 Commit SHA 之清單；不宣稱此為獨立 Review。
L1–L3 若無法提供必要證據或判定仍有高風險，可按 Risk 選用 Fresh-Context Challenge：由 Claude Code 評估必要性、記錄執行或不執行的理由；Human 明確指定時不得略過。Fresh-Context 非 Agent Handoff 或新治理平台，僅為補充驗證機制。
新 head 必須重新確認 Self-Review；base 或範圍改變須評估影響並重新自審，未確認前不能沿用舊結果。

三種證據不得互相冒充：
- Self-Review Summary／Evidence List：Builder 自審輸出，應列舉實際操作步驟、證據連結與結論；不宣稱已獲獨立 Review。
- GitHub 原生 Review：GitHub 的 APPROVED／CHANGES_REQUESTED 等狀態；不是 Human 授權。
- Human Approval：唯一管理者對 L2 Plan 或 L3 具體操作的明確核准；不是 Bot 結果。

不強制 Self-Review 報告必須轉成原生 APPROVED，也不要求 Attestation、Registry、第二位 Human、新 App、Control Plane 或簽章服務。現有流程沒有可信 Agent 身分自動驗證，必須如實說明審查範圍與限制。

## 驗證與 Merge
執行適用測試與 CI；網站建置使用 MkDocs strict。Build、教材內容／來源／授權與視覺驗證分開記錄。
適用檢查失敗、缺失、pending、skipped、cancelled、證據過期、未解決的阻擋 Review／評論／Thread，或必要授權／記錄缺少，皆禁止 Merge。CI 成功不代表 Review 或授權完成。
必要實作、驗證與 Result 完成後才可提出 Ready；是否切換 PR 狀態依各 PR 的任務邊界及有效授權。
只有非 Draft、適用驗證與 Review 完成、阻擋問題已解決、範圍與授權有效時，才由具備權限且已獲操作授權的執行者 Merge。L1 不要求 Human 逐次內容核准；Merge 操作權限與內容核准分開。
本政策不授權啟用 Auto-Merge、不新增 merge executor，也不假定上述條件已由 GitHub 自動強制。不得 bypass 現有保護、force push 或直接 push main。
重大範圍／風險變動須重新評估 Plan、Review 與 Human 授權，必要時回到 Draft。

## Rollback 與部署
以 revert PR 回復錯誤變更，保留原始記錄並執行適用驗證／審查；不 reset／force push main。重大回復或緊急操作由 Human 明確授權。
Merge 不代表部署授權。Pages 僅有手動入口，執行仍需另行授權；不要求合併前先部署同一 commit。
Issue 只在範圍完成、必要證據完整且已授權合併後結案；未完成的工作繼續標示 pending／blocked。

## 輕量工具與歷史
scripts/merge_lifecycle.py 是本地條件檢查輔助，不是身分驗證或 Merge 服務；scripts/verify_plan_records.py 只檢查記錄結構與 Git 順序。使用者提供的分類與事實仍須人工／Agent 核對。
舊平台原型與專屬測試移至 archive/governance-platform/，不參與正常 CI。歷史 PLAN／RESULT、Canary JSON、Issue／PR 證據保留；C3–C5 與後續平台工作停止，既有資源不在本次修改。
