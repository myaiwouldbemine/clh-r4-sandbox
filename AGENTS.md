# Agent Instructions — Issue-Driven Autonomous Governance

## 01. 任務與責任

**繁體中文**

先讀 GOVERNANCE.md 與 Issue 的 WHAT／WHY／DONE／邊界。Human myaiwouldbemine 保留管理權，開立工程 Issue 並在需要時啟動 Codex App／本機 Agent；範圍內的調查、規劃、實作、測試、自審、PR、Ready、Merge、部署、歸檔及結案由 Agent 自主完成，不需重複 Human 核准。

**English**

Read GOVERNANCE.md and the Issue WHAT/WHY/DONE/boundary. Human myaiwouldbemine retains administration, opens an engineering Issue and starts Codex App / the local Agent when needed; the Agent autonomously performs investigation, planning, implementation, tests, Self-Review, PR, Ready, merge, deployment, archival and closure within scope, without repeated Human approval.

## 02. 單一 Builder

**繁體中文**

Claude Code 與 Codex 適用相同規範。每個工程 Issue／PR 任一時點只有一位明確記錄的 accountable Builder。

**English**

Claude Code and Codex follow the same rules. Each engineering Issue/PR has exactly one explicitly recorded accountable Builder at a time.

## 03. 教材所有權

**繁體中文**

ChatGPT＋Human 保有 V2 Knowledge Consolidation、V3 Code-First Deep Dive 的教材創作、推導、語義品質、核准及最終整合權。V2／V3 製作時分開、定稿時合併、網站依主題呈現。工程 Agent 只忠實匯入已核准教材及處理排版、工程、測試與部署；未核准語義標記 PENDING 或 BLOCKED，不自行創作。

**English**

ChatGPT + Human retain ownership of V2 Knowledge Consolidation and V3 Code-First Deep Dive content creation, derivation, semantic quality, approval and final integration. Produce V2/V3 separately, combine at finalization, and present by topic on the website. Engineering Agents only faithfully import approved content and handle layout, engineering, tests and deployment; mark unapproved semantics PENDING or BLOCKED and do not author them.

## 04. 學習紀錄

**繁體中文**

Learning Record 可用留言逐步更新，不必對應工程 PR；只有 Repository 變更進入工程流程。Issue 建立、CI PASS、Merge 或結案都不代表教材品質核准或學習掌握。

**English**

Learning Records may be updated incrementally through comments and need no engineering PR; only repository changes enter the engineering workflow. Issue creation, CI PASS, merge or closure does not imply content quality approval or learning mastery.

## 05. 工程流程

**繁體中文**

依 Issue → 調查 → 必要 Plan → Draft PR／實作 → 測試與 Self-Review／Evidence → Ready → Merge → 適用部署與讀回 → 歸檔與讀回 → Close 執行。提早建立 Draft；完成實作、適用驗證與必要 Result 後自主切換 Ready。

**English**

Follow Issue → investigation → Plan when needed → Draft PR/implementation → tests and Self-Review/evidence → Ready → merge → applicable deployment and readback → archival and readback → close. Open Draft early; autonomously mark Ready after implementation, applicable verification and any required Result are complete.

## 06. 規劃與歷史

**繁體中文**

不使用 L0–L3 分級或 Human 工程審批。必要正式 Plan 存於 records/ISSUE-<number>/PLAN.md，必須在實作前獨立提交；有 Plan 就於實作後寫 RESULT.md。記錄用於追溯，不是核准關卡；保留歷史，不偽造順序。

**English**

Do not use L0–L3 classification or Human engineering approval gates. Store a needed formal Plan in records/ISSUE-<number>/PLAN.md and commit it separately before implementation; when a Plan exists, write RESULT.md after implementation. Records provide traceability, not approval gates; preserve history and never fabricate ordering.

## 07. 交接

**繁體中文**

交接記錄前後 Builder、完整 Commit SHA、base／scope、進度、已完成與待辦、Evidence 及未解問題。接手者重新確認目前 head 與 base 的 Self-Review、證據及範圍；更換工具不使舊審查自動有效。

**English**

Record outgoing/incoming Builders, full commit SHA, base/scope, progress, completed and remaining work, evidence and unresolved issues at handoff. The incoming Builder reconfirms Self-Review, evidence and scope for the current head and base; changing tools does not make old reviews valid.

## 08. 自審

**繁體中文**

PR 記錄實際工作、完整 reviewed head／base SHA、範圍、發現、結論及 Claim／Source／Method／Evidence。Self-Review、CI、Bot Summary、原生 GitHub Review 與 Human 意見不得互相冒充，不宣稱獨立人工審查或可信身分驗證。

**English**

Record actual work, full reviewed head/base SHAs, scope, findings, verdict and Claim/Source/Method/Evidence in the PR. Do not conflate Self-Review, CI, Bot Summary, native GitHub Review or Human feedback, or claim independent Human review or trusted identity verification.

## 09. 補充驗證

**繁體中文**

Builder 可依工程需要選擇 Fresh-Context Challenge，並記錄採用或省略理由；Human 明確要求時不得省略。它不是每日強制審查、交接或治理平台。

**English**

The Builder may choose a Fresh-Context Challenge based on engineering needs and records the reason for inclusion or omission; an explicit Human request must be honored. It is not mandatory daily review, a handoff or a governance platform.

## 10. 驗證

**繁體中文**

執行適用測試／CI，網站變更使用 strict MkDocs。分別報告 build、教材、來源、視覺與部署。使用 PASS／FAIL／BLOCKED／PENDING／NOT RUN；mock 不冒充真實 E2E。

**English**

Run applicable tests/CI and strict MkDocs for website changes. Report build, content, provenance, visual and deployment separately. Use PASS/FAIL/BLOCKED/PENDING/NOT RUN; never present mocks as live E2E.

## 11. 合併條件

**繁體中文**

必要 CI 必須全部成功；缺失、失敗、pending、skipped、cancelled、過期證據、衝突或未解阻擋都禁止 Merge。新 head 或 base 需重新驗證及自審，範圍變化需重新核對 Issue。確認精確 head SHA、Issue 範圍與非 Draft 狀態後自主 Merge，遵守 GitHub 保護與 Required Checks。

**English**

All required CI must succeed; missing, failed, pending, skipped or cancelled checks, stale evidence, conflicts or unresolved blockers prohibit merge. Revalidate and repeat Self-Review for a new head or base; reassess Issue alignment when scope changes. Autonomously merge after verifying the exact head SHA, Issue scope and non-Draft status, respecting GitHub protections and required checks.

## 12. 部署與結案

**繁體中文**

Merge 不等於部署成功。需要網站發布時，自主執行 GitHub Pages、遠端讀回部署 SHA，記錄 Workflow URL 與結果；非網站任務不強制無關部署。Merge、Deployment、Archive、Closure 分別記錄；必要工作與部署驗證成功且 Evidence 歸檔讀回完成後才 Close。禁止使用會在 Merge 時提前結案的關鍵字。

**English**

Merge does not imply deployment success. When publication is needed, autonomously run GitHub Pages, remotely read back the deployed SHA and record the workflow URL and result; non-site tasks do not require unrelated deployment. Record merge, deployment, archive and closure separately; close only after necessary work and deployment verification succeed and archived evidence is read back. Do not use keywords that prematurely close Issues on merge.

## 13. 安全與失敗

**繁體中文**

不得直接 push main、force push、bypass、任意擴張 Token 權限或未授權讀取／外洩 Secrets。失敗時停止受影響操作並留下 Blocker Evidence，保留未完成 Issue；在既有權限內自主修正與有限重試，重複事件不得重複 Merge 或錯誤結案。

**English**

Never push main directly, force push, bypass protections, arbitrarily expand token permissions, or access/disclose secrets without authorization. On failure, stop the affected operation, record blocker evidence and keep unfinished Issues open; autonomously repair and retry within existing permissions with bounded attempts, without duplicate merges or incorrect closure on repeated events.

## 14. 啟用與回復

**繁體中文**

分開驗證實作與正式啟用。採 On-Demand Autonomous Engineering，不要求關機或 App 關閉後繼續工程；正常本機流程使用既有 App 登入與 gh auth，不依賴額外 OPENAI_API_KEY 或 CLH_AUTOMATION_TOKEN。確認本機執行環境、權限、CI、保護規則、重試與回復路徑後才啟用；中斷後重新讀取遠端 head／base、Issue、PR、部署與歸檔狀態再恢復，不重複合併；缺少技術條件如實標記 BLOCKED，不虛構完成或要求逐項工程核准。Human 可修改需求或主動停止；回復用經適用測試的 revert PR，不重寫 Git 歷史。

**English**

Verify implementation separately from activation. Use On-Demand Autonomous Engineering; engineering need not continue when the computer or App is off. The normal local workflow uses existing App sign-in and gh auth without an additional OPENAI_API_KEY or CLH_AUTOMATION_TOKEN. Enable only after confirming the local execution environment, permissions, CI, protection rules, retries and rollback path; after interruption, reread remote head/base, Issue, PR, deployment and archive state before resuming, without merging again; report missing technical prerequisites as BLOCKED, never fabricate completion or demand per-step engineering approval. Human may change requirements or stop work; roll back through a revert PR with applicable tests, without rewriting Git history.

## 15. 輕量治理

**繁體中文**

不以 Approval Token、Trusted Reviewer、Attestation、Registry、Control Plane、第二位 Human 或新 App 重建審批。歷史與 archived 設計只作證據；C3–C5 及後續平台工作維持停止，不建立新治理基礎設施。

**English**

Do not rebuild approval gates using approval tokens, trusted reviewers, attestations, registries, control planes, a second Human or a new App. Historical and archived designs are evidence only; C3–C5 and subsequent platform work remain stopped; do not provision new governance infrastructure.
