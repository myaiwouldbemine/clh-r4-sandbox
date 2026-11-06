# Copy Learning Hub — GitHub Issue Forms 使用說明

## 兩種入口

- **Learning Record**：記錄學習目標、來源與 V2／V3 歷程。ChatGPT＋Human 擁有教材創作、推導、品質核准及整合定稿權。V2／V3 **製作時分開、定稿時合併、網站上依主題呈現**。
- **Engineering Task**：提交 Repository 工程變更或已核准教材的忠實匯入需求。採 **Tool-Neutral Single-Builder + Self-Verification**，每個工程 Issue／PR 在任一時點只有一位明確指定的 accountable Builder，可為 Claude Code 或 Codex，適用相同治理規則。

Learning Issue 不強制對應工程 PR；只有 Repository 變更需要相應工程流程。GitHub 保存已核准教材、版本及學習軌跡，MkDocs 提供閱讀、搜尋、導覽及展示。Builder 負責工程、網站相容性、CI、PR 與工程驗證，不創作或改寫教材語意；語意問題標記 PENDING，交由 ChatGPT／Human 決定。

## 表單欄位與後續留言

Engineering Task 保留五個 textarea ID：`what`、`why`、`acceptance`、`boundary`、`references`，必填設定依序為 `true, true, true, true, false`。既有工程 Issue 不需搬移或重新提交。

Learning Record 使用以下八個 textarea ID：

| ID | 欄位 | 建立時必填 |
|---|---|---|
| `subject-course-unit` | Subject / Course / Unit | 是 |
| `learning-objectives` | Learning Objectives | 是 |
| `source-materials` | Source Materials；未知可如實填 PENDING | 是 |
| `v2-consolidation` | V2 Knowledge Consolidation | 否 |
| `v3-code-first` | V3 Code-First Deep Dive | 否 |
| `content-quality-evidence` | Content Quality / Evidence | 否 |
| `v2-v3-integration` | V2/V3 Integration | 否 |
| `publication-archive` | Publication / Archive References | 否 |

建立時不要求尚未產生的成果、驗收或歸檔連結。後續可在 Issue Comments 逐步記錄階段、實際狀態、來源／版本、Evidence 與下一步；未執行寫 NOT RUN，待確認寫 PENDING。Issue 建立、CI PASS、PR Merge 或 Issue Closed 均不代表內容品質已核准、學習完成或完全掌握。

## 發佈與驗證

表單位於 `.github/ISSUE_TEMPLATE/01-agent-task.yml` 與 `.github/ISSUE_TEMPLATE/02-learning-record.yml`；設定檔為 `.github/ISSUE_TEMPLATE/config.yml`，保留 `blank_issues_enabled: false`。

修改經審查、授權合併至預設分支後，才在 GitHub **Issues → New issue** 提供相應入口。合併前檢查 YAML 語法、GitHub Issue Forms schema、名稱／ID 唯一性及上述必填設定；合併後再實際核對兩種表單的呈現。YAML／schema 與 PR CI 成功不能替代 GitHub 表單 UI 驗證，不得提前宣稱發佈完成。

## 極簡治理與交接

以目前 main 的 `GOVERNANCE.md`、`AGENTS.md` 與 Issue 邊界為準：

- 依實際影響判定 L0–L3；L0 僅限非語意錯字／格式，仍需適用驗證。
- L1 需要適用驗證、Builder Self-Review 與可追溯 Evidence；Self-Review 不冒充獨立 Review。
- L2 另需事前獨立提交正式 Plan、Human 核准 Plan／範圍及事後 Result；L3 另需具體操作／範圍授權。
- 交接記錄前後 Builder、完整 Commit SHA、base／scope／risk、已完成／未完成、Evidence 與 Blockers。接手者重新確認目前 head 的 Self-Review、證據有效性及適用 Human 授權；工具更換不自動轉移舊審查或授權。
- Draft 不授予實作或 Merge 權限。Plan 核准、實作授權、Ready、Merge 與 Deployment 分別確認；Bot Summary、原生 GitHub Review 與 Human Approval 不可互相替代。

表單僅為資訊入口，不啟用自動派工、身分驗證、Auto-Merge 或部署。Pages 僅有手動入口且需另行授權；歷史 Governance Platform 與 Canary 計畫仍未啟用。
