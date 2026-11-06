# Issue-Driven Autonomous Governance

Human-Issue-Only：Human myaiwouldbemine 定義 WHAT／WHY／DONE 及邊界，保留管理、需求修改及緊急停止權。工程 Agent 自主完成其餘生命週期，不使用 L0–L3，不再要求 Plan、Implementation、Ready、Merge、Deployment 或 Closure 的重複 Human Approval。Issue／PR 是記錄與追溯，不是人工審批程序。

## 責任與教材

Claude Code 與 Codex 適用相同規範；每個工程 Issue／PR 同一時間只有一位 accountable Builder。交接記錄前後 Builder、完整 SHA、base／scope、進度、Evidence 及未解問題，接手者重新確認目前版本。

ChatGPT＋Human 擁有 V2 Knowledge Consolidation、V3 Code-First Deep Dive 的教材創作、推導、語義品質、核准與最終整合權。V2／V3 製作時分開、定稿時合併、網站依主題呈現。工程 Agent 僅忠實匯入已核准教材，處理排版、工程、測試與部署；未核准教材語義標記 PENDING／BLOCKED。工程自主權不等於教材創作權。Learning Record 可逐步留言，不必對應工程 PR；CI／Merge／結案都不代表學習掌握。

## 工程流程與記錄

Issue → Investigation → 必要 Plan → Draft PR／Implementation → Tests → Self-Review／Evidence → Ready → Merge → 適用 Pages Deployment／Readback → Archive／Readback → Close。

提早建立 Draft。必要 Plan 放在 records/ISSUE-<number>/PLAN.md，實作前獨立 commit；有 Plan 就於實作後寫 RESULT.md。Plan 記錄目標、理由、範圍、邊界、步驟、驗收、驗證與修訂，不是等待核准。完整 Git 歷史與舊 Records 不改寫。

Builder 記錄實際工作、完整 reviewed head／base SHA、Issue 範圍、Claim／Source／Method／Evidence、發現與結論。Self-Review／CI 不冒充獨立人工審查、原生 Review 或可信身分驗證。Fresh-Context Challenge 可依需要選用，記錄理由；Human 明確要求則執行，不要求每日審查或第二位 Human。

## 自主 Merge

完成實作、適用測試、Self-Review、Evidence 與必要 Result 後自主 Ready。所有必要 CI 成功、目前 head／base 自審有效、無衝突／未解阻擋、範圍符合 Issue，才以精確 head SHA 合併。新 head 或 base 必須重新驗證與自審。缺失、失敗、pending、skipped、cancelled 或 stale 的必要證據禁止放行。CI 不能自動證明語義符合 Issue，仍由 Builder 負責。

遵守 Branch Protection／Rulesets／Required Checks，不直接 push main、force push 或 bypass。不需原生 APPROVED 或 Human 逐 PR 核准；不得偽裝已滿足既有 GitHub 強制限制。

## 自主部署、歸檔與結案

網站發布使用 strict MkDocs 及正式 GitHub Pages，保存 deployment SHA、Workflow URL、結果及遠端 SHA 讀回。非網站任務依實際條件完成，不強制無關部署。Build、教材、來源、視覺及部署分開報告；Merge 不等於部署成功。

Merge、Deployment、Archive、Closure 各有獨立結果。必要工程與部署驗證完成後，Evidence 歸檔並讀回成功才結案；歸檔或部署失敗保持 Issue open。PR 不使用 GitHub 自動結案關鍵字。重試已 Merge 的任務要沿用 merge SHA，不再 Merge；重複事件不能錯誤結案。

## 失敗、安全、啟用與回復

失敗即停止受影響操作並留下 Blocker Evidence；Agent 在既有權限內自主修正、有限重試，不要求一般修正逐項核准。不得任意擴張 Token 權限、未授權讀取或外洩 Secrets。

實作與啟用分開驗證；只有 Runner、權限、CI、main 保護、重試及回復路徑確認後才正式啟用。技術條件缺少時如實 BLOCKED；安裝開關只用於首次啟用與緊急停止，不是每個 Issue 的核准 Token。需要管理員才能完成的設定列明精確操作，不假裝已完成。詳見 INSTALL.md 與 docs/development/AUTONOMOUS_OPERATIONS.md。

回復用適用測試及自審的 revert PR，保留歷史，不 reset／force push main。Human 可主動停止任務或調整需求。

## 歷史與範圍

不新增 Approval Token、Trusted Reviewer、Attestation、Registry、Control Plane 或新治理平台。Archived 設計與歷史 Records 僅為證據；C3–C5 及後續平台工作仍停止。Issue #18／PR #19 的 Plan、雙語化、Result 與證據不被此遷移覆寫。

政策描述目標與責任；實際啟用狀態以 Issue #20 Result／E2E 和 GitHub 設定證據為準，不能由 Markdown 推定已上線。
