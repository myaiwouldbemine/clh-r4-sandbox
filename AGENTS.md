# Agent Instructions — Minimal Learning Hub

## 01. 政策與責任

**繁體中文**

閱讀 GOVERNANCE.md 與 Issue 的工作邊界。Human myaiwouldbemine 是唯一管理者。採用 Tool-Neutral Single-Builder + Self-Verification：每個工程 Issue／PR 在任一時點只有一位指定的 accountable Builder（Claude Code 或 Codex）；兩者適用相同的風險、驗證、Self-Review、Evidence 與授權規範。

**English**

Read GOVERNANCE.md and the Issue boundary. Human myaiwouldbemine is the sole administrator. Use Tool-Neutral Single-Builder + Self-Verification: each engineering Issue/PR has exactly one designated accountable Builder (Claude Code or Codex) at any time; both tools follow the same risk, verification, Self-Review, Evidence and authorization rules.

## 02. 教材所有權與工程分工

**繁體中文**

ChatGPT＋Human 擁有 V2／V3 教材創作、推導、品質核准與整合定稿權；製作時分開、定稿時合併、網站上依主題呈現。GitHub 保存已核准教材、版本及學習軌跡；MkDocs 提供閱讀、搜尋、導覽與展示。Builder 負責工程及忠實匯入已核准教材，不創作或修改教材語意；語意問題標記 PENDING，交由 ChatGPT／Human 決定。

**English**

ChatGPT + Human own V2/V3 learning content creation, derivation, quality approval and final integration. Produce V2/V3 separately, integrate them when finalizing, and present them by topic on the website. GitHub preserves approved learning content, versions and learning history; MkDocs provides reading, search, navigation and presentation. The Builder handles engineering and faithful import of approved learning content, without authoring or changing its meaning. Mark semantic questions PENDING and refer them to ChatGPT/Human for decisions.

## 03. 學習紀錄與工程流程

**繁體中文**

Learning Record Issue 可透過 Comments 逐步更新，不必對應工程 PR；只有 Repository 變更需要下列工程流程。Issue 建立、CI PASS、PR Merge 或 Issue Closed 均不代表內容品質核准、學習完成或完全掌握。

**English**

A Learning Record Issue may progress through Comments without a corresponding engineering PR. Only Repository changes require the engineering workflow below. Issue creation, CI PASS, PR Merge and Issue Closed do not establish content quality approval, learning completion or mastery.

## 04. Builder 交接

**繁體中文**

工程 Issue／PR 記錄唯一 accountable Builder。交接記錄前後 Builder、完整 Commit SHA、base／scope／risk、已完成／未完成事項、Evidence 與 Blockers。接手者重新確認目前 head 的 Self-Review、證據有效性及適用 Human 授權，評估 base／scope／risk 變化；工具更換不自動轉移舊審查結論或 Human 授權。

**English**

Record the sole accountable Builder in the engineering Issue/PR. For a handoff, record the previous and incoming Builders, full Commit SHA, base/scope/risk, completed and unfinished work, Evidence and Blockers. The incoming Builder reconfirms the current head’s Self-Review, evidence validity and applicable Human authorization, and assesses base/scope/risk changes. Changing tools does not automatically transfer prior review conclusions or Human authorization.

## 05. 工程流程與 Draft

**繁體中文**

採用 Issue → Draft PR → Plan（必要時）→ Implementation → Result（必要時）→ Self-Review → 授權 Merge 的流程。提早建立 Draft；Draft 不授予實作或合併權限。

**English**

Use Issue → Draft PR → conditional Plan → Implementation → conditional Result → Self-Review → authorized Merge. Open Draft early; Draft grants no implementation or merge authority.

## 06. 實際影響與風險分類

**繁體中文**

依實際影響分類：L0 為非語意錯字／格式；L1 為實質內容／程式變更；L2 為重大架構／來源鏈變更；L3 為安全／治理／權限／部署／不可逆操作。風險未知時，阻擋依賴該澄清的工作。

**English**

Classify actual impact: L0 nonsemantic typo/formatting, L1 substantive content/code, L2 major architecture/provenance, L3 security/governance/permissions/deployment/irreversible operations. Unknown risk blocks clarification-dependent work.

## 07. 各風險層級的必要條件

**繁體中文**

L0 不強制要求 Plan／Result 或 Self-Review 證據。L1 需要可追溯的 Self-Review 與書面 Evidence。L2／L3 需要事前 Plan 與 Human 核准；L3 另需具體操作／範圍授權。

**English**

L0 needs no mandatory Plan/Result or Self-Review evidence. L1 needs traceable Self-Review with documented Evidence. L2/L3 need pre-implementation Plan and Human approval; L3 also needs specific action/scope authorization.

## 08. Fresh-Context Challenge

**繁體中文**

Fresh-Context Challenge 是依風險選用的驗證，不是強制每日審查。由指定 Builder 評估必要性並記錄執行或省略理由。Human 明確指定的 challenge 不得省略。它不是 Agent Handoff 或治理平台。

**English**

Fresh-Context Challenge is optional verification based on risk, not mandatory daily review. The designated Builder evaluates necessity and documents the reason for inclusion or omission. Human-mandated challenges cannot be skipped. It is not an Agent Handoff or governance platform.

## 09. Formal Plan 與 Result 歷史

**繁體中文**

正式 Plan 存於 `records/ISSUE-<number>/PLAN.md`，且必須在其對應實作之前提交；保留歷史。若有正式 Plan，實作後須撰寫 RESULT.md。不得偽造歷史順序。

**English**

Formal Plans go in `records/ISSUE-<number>/PLAN.md` and must be committed before their implementation; preserve history. If a formal Plan exists, write RESULT.md after implementation. Do not fabricate historical ordering.

## 10. Self-Review 與 Evidence 紀錄

**繁體中文**

在 PR 記錄實際 Builder 工作、完整 reviewed commit、相關 base／scope、發現／結論及證據。Self-Review 不是交叉審查；須區分 Self-Review Evidence 與獨立 Review。若採用 Fresh-Context Challenge，須記錄該驗證。

**English**

Record actual Builder work, full reviewed commit, relevant base/scope, findings/verdict and evidence in the PR. Self-review is not cross-review; distinguish Self-Review Evidence from independent Review. Document Fresh-Context Challenge if applied.

## 11. 審查與授權證據的區分

**繁體中文**

區分 Bot Summary、原生 GitHub Review 與 Human Approval。不強制轉為原生 APPROVED，也不強制要求 App／Registry／Attestation／Control Plane／第二位 Human。不得宣稱自動可信身分驗證。

**English**

Distinguish Bot Summary, native GitHub Review and Human Approval. No mandatory native APPROVED conversion, App/Registry/Attestation/Control Plane/second Human. Do not claim automated trusted identity verification.

## 12. 適用驗證與阻擋條件

**繁體中文**

執行適用測試／CI；網站變更須執行 MkDocs strict。Build／內容／來源／視覺／部署分別回報。檢查缺失、失敗、略過、待定、證據過期或仍有未解阻擋事項時，不得 Merge。

**English**

Run applicable tests/CI and strict MkDocs for site changes. Report build/content/provenance/visual/deployment separately. Missing, failed, skipped, pending, stale evidence or unresolved blockers prevents Merge.

## 13. 新 Head 與變更再確認

**繁體中文**

新 head 必須重新確認 Review；base／scope／risk 變化須重新評估，必要時重新取得授權。

**English**

New head requires Review reconfirmation; base/scope/risk changes require reassessment and renewed authorization where necessary.

## 14. Ready 條件與狀態授權

**繁體中文**

Ready 需要完成實作、適用驗證及必要時的 Result；須遵守明確的 PR 狀態邊界與授權。

**English**

Ready requires completed implementation, applicable verification and conditional Result; follow explicit PR status boundaries and authorization.

## 15. Merge 與禁止操作

**繁體中文**

只有具備明確操作授權、PR 為非 Draft 且所有適用條件均滿足時，才可 Merge。L1 不強制逐 PR 的 Human 內容核准。禁止直接 push main、force push、bypass、未授權的 Merge／部署或啟用 Auto-Merge。

**English**

Merge only with explicit operation authority, non-Draft and all applicable conditions met. L1 has no mandatory per-PR Human content approval. No direct main push, force push, bypass, unauthorized Merge/deployment or Auto-Merge activation.

## 16. Rollback 與 Human 決策

**繁體中文**

使用已授權的 revert PR 及適用檢查進行回復。Human 負責 L2 Plan／L3 操作核准及緊急停止。

**English**

Roll back using an authorized revert PR and applicable checks. Human handles L2 Plan/L3 action approval and emergency stop.

## 17. Archived Governance

**繁體中文**

已封存的平台設計／測試與歷史紀錄是證據，不是現行指令。C3–C5 及後續平台工作已停止。不得建置新的治理基礎設施。

**English**

Archived platform designs/tests and historical records are evidence, not active instructions. C3-C5 and later platform work are stopped. Do not provision new governance infrastructure.
