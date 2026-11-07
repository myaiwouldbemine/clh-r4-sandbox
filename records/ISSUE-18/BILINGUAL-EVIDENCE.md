# Issue #18 — Plan v1.2 雙語化 Evidence

日期：2026-11-06；唯一 accountable Builder：Codex；風險：L3。

## Source / Authorization

- 已核准 Plan v1.2：`f0353b0ee784f60319ae54b89086321c7d20e634`；原 17 條來源為該 commit 的 AGENTS.md，與前一實作 Head `d0f400cc56a4aa3db914c0029cd6e9c1f9292038` 相同。
- 實作 Commit：`88e109756faa84ed852e8f135fb33319e29a5e58`；base：`7e530cdc818044ae4f760a021a331f888f993e43`。
- Human 在本聊天「Issue #18 — Formal Plan v1.2 Approval & Bilingual Implementation Authorization」分別核准固定 Plan 與三檔實作。聊天沒有公開 URL；[Issue Timeline 授權參考](https://github.com/myaiwouldbemine/myaiwouldbemine-Copy-Learning-Hub/issues/18#issuecomment-6686502162) 是 Builder 的可追溯紀錄，不冒充原生 Human Review 或自動身分驗證。已讀回固定 SHA 與三檔範圍。
- 只允許 AGENTS.md、新增本證據及 RESULT.md 追加；Plan 不改。Ready／Merge／Close／Deploy／workflow_dispatch 均未授權。

## 三向語義一致性矩陣

方法：Codex 逐條核對原文→繁中、原文→英文、繁中↔英文的主體、義務強度（Mandatory／Optional／Prohibited）、條件／例外、權限、證據與禁止事項。下列 PASS 為 Builder 語義自審，並非自動測試或獨立 Review。兩段各自完整，不新增語言優先權。原文及雙語全文直接取自 Git／AGENTS.md，避免摘要取代核對。

| 條款 | 原文 | 繁體中文 | English | 三向核對結果 |
|---|---|---|---|---|
| 01 | Read GOVERNANCE.md and the Issue boundary. Human myaiwouldbemine is the sole administrator; 採 Tool-Neutral Single-Builder + Self-Verification：每個工程 Issue／PR 在任一時點只有一位指定 accountable Builder（Claude Code 或 Codex），兩者適用相同風險、驗證、Self-Review、Evidence 與授權規範。 | 閱讀 GOVERNANCE.md 與 Issue 的工作邊界。Human myaiwouldbemine 是唯一管理者。採用 Tool-Neutral Single-Builder + Self-Verification：每個工程 Issue／PR 在任一時點只有一位指定的 accountable Builder（Claude Code 或 Codex）；兩者適用相同的風險、驗證、Self-Review、Evidence 與授權規範。 | Read GOVERNANCE.md and the Issue boundary. Human myaiwouldbemine is the sole administrator. Use Tool-Neutral Single-Builder + Self-Verification: each engineering Issue/PR has exactly one designated accountable Builder (Claude Code or Codex) at any time; both tools follow the same risk, verification, Self-Review, Evidence and authorization rules. | PASS：唯一管理者、任一時點唯一 Builder、兩工具同規則。 |
| 02 | ChatGPT＋Human 擁有 V2／V3 教材創作、推導、品質核准與整合定稿權；製作時分開、定稿時合併、網站上依主題呈現。GitHub 保存已核准教材、版本及學習軌跡；MkDocs 提供閱讀、搜尋、導覽與展示。Builder 負責工程及忠實匯入已核准教材，不創作或修改教材語意；語意問題標記 PENDING，交由 ChatGPT／Human 決定。 | ChatGPT＋Human 擁有 V2／V3 教材創作、推導、品質核准與整合定稿權；製作時分開、定稿時合併、網站上依主題呈現。GitHub 保存已核准教材、版本及學習軌跡；MkDocs 提供閱讀、搜尋、導覽與展示。Builder 負責工程及忠實匯入已核准教材，不創作或修改教材語意；語意問題標記 PENDING，交由 ChatGPT／Human 決定。 | ChatGPT + Human own V2/V3 learning content creation, derivation, quality approval and final integration. Produce V2/V3 separately, integrate them when finalizing, and present them by topic on the website. GitHub preserves approved learning content, versions and learning history; MkDocs provides reading, search, navigation and presentation. The Builder handles engineering and faithful import of approved learning content, without authoring or changing its meaning. Mark semantic questions PENDING and refer them to ChatGPT/Human for decisions. | PASS：創作／推導／品質／整合所有權、V2/V3 三階段、GitHub/MkDocs 分工、禁止 Builder 改語意及 PENDING。 |
| 03 | Learning Record Issue 可透過 Comments 逐步更新，不必對應工程 PR；只有 Repository 變更需要下列工程流程。Issue 建立、CI PASS、PR Merge 或 Issue Closed 均不代表內容品質核准、學習完成或完全掌握。 | Learning Record Issue 可透過 Comments 逐步更新，不必對應工程 PR；只有 Repository 變更需要下列工程流程。Issue 建立、CI PASS、PR Merge 或 Issue Closed 均不代表內容品質核准、學習完成或完全掌握。 | A Learning Record Issue may progress through Comments without a corresponding engineering PR. Only Repository changes require the engineering workflow below. Issue creation, CI PASS, PR Merge and Issue Closed do not establish content quality approval, learning completion or mastery. | PASS：Comments 可更新、無強制 PR；僅 Repository 變更需工程流程；四事件不等於三種學習成果。 |
| 04 | 工程 Issue／PR 記錄唯一 accountable Builder。交接記錄前後 Builder、完整 Commit SHA、base／scope／risk、已完成／未完成、Evidence 與 Blockers。接手者重新確認目前 head 的 Self-Review、證據有效性及適用 Human 授權，評估 base／scope／risk 變化；工具更換不自動轉移舊審查結論或 Human 授權。 | 工程 Issue／PR 記錄唯一 accountable Builder。交接記錄前後 Builder、完整 Commit SHA、base／scope／risk、已完成／未完成事項、Evidence 與 Blockers。接手者重新確認目前 head 的 Self-Review、證據有效性及適用 Human 授權，評估 base／scope／risk 變化；工具更換不自動轉移舊審查結論或 Human 授權。 | Record the sole accountable Builder in the engineering Issue/PR. For a handoff, record the previous and incoming Builders, full Commit SHA, base/scope/risk, completed and unfinished work, Evidence and Blockers. The incoming Builder reconfirms the current head’s Self-Review, evidence validity and applicable Human authorization, and assesses base/scope/risk changes. Changing tools does not automatically transfer prior review conclusions or Human authorization. | PASS：前後 Builder／完整 SHA／base scope risk／完成未完成／Evidence Blockers 全保留；新接手再確認且不繼承授權。 |
| 05 | Use Issue → Draft PR → conditional Plan → Implementation → conditional Result → Self-Review → authorized Merge. Open Draft early; Draft grants no implementation or merge authority. | 採用 Issue → Draft PR → Plan（必要時）→ Implementation → Result（必要時）→ Self-Review → 授權 Merge 的流程。提早建立 Draft；Draft 不授予實作或合併權限。 | Use Issue → Draft PR → conditional Plan → Implementation → conditional Result → Self-Review → authorized Merge. Open Draft early; Draft grants no implementation or merge authority. | PASS：完整流程順序、conditional Plan/Result、Draft 無實作或 Merge 權。 |
| 06 | Classify actual impact: L0 nonsemantic typo/formatting, L1 substantive content/code, L2 major architecture/provenance, L3 security/governance/permissions/deployment/irreversible operations. Unknown risk blocks clarification-dependent work. | 依實際影響分類：L0 為非語意錯字／格式；L1 為實質內容／程式變更；L2 為重大架構／來源鏈變更；L3 為安全／治理／權限／部署／不可逆操作。風險未知時，阻擋依賴該澄清的工作。 | Classify actual impact: L0 nonsemantic typo/formatting, L1 substantive content/code, L2 major architecture/provenance, L3 security/governance/permissions/deployment/irreversible operations. Unknown risk blocks clarification-dependent work. | PASS：L0–L3 全類別、依實際影響分類；未知風險僅阻擋依賴澄清的工作。 |
| 07 | L0 needs no mandatory Plan/Result or Self-Review evidence. L1 needs traceable Self-Review with documented Evidence. L2/L3 need pre-implementation Plan and Human approval; L3 also needs specific action/scope authorization. | L0 不強制要求 Plan／Result 或 Self-Review 證據。L1 需要可追溯的 Self-Review 與書面 Evidence。L2／L3 需要事前 Plan 與 Human 核准；L3 另需具體操作／範圍授權。 | L0 needs no mandatory Plan/Result or Self-Review evidence. L1 needs traceable Self-Review with documented Evidence. L2/L3 need pre-implementation Plan and Human approval; L3 also needs specific action/scope authorization. | PASS：L0 豁免、L1 可追溯證據、L2/L3 事前 Plan 核准、L3 額外具體授權。 |
| 08 | Fresh-Context Challenge: Optional verification per risk; not mandatory daily review. 由指定 Builder 評估必要性並記錄執行或省略理由。 Human-mandated challenges cannot be skipped. Not an Agent Handoff or governance platform. | Fresh-Context Challenge 是依風險選用的驗證，不是強制每日審查。由指定 Builder 評估必要性並記錄執行或省略理由。Human 明確指定的 challenge 不得省略。它不是 Agent Handoff 或治理平台。 | Fresh-Context Challenge is optional verification based on risk, not mandatory daily review. The designated Builder evaluates necessity and documents the reason for inclusion or omission. Human-mandated challenges cannot be skipped. It is not an Agent Handoff or governance platform. | PASS：Optional 非每日強制；指定 Builder 記錄採用或省略理由；Human 指定不得省略；非交接／平台。 |
| 09 | Formal Plans go in records/ISSUE-&lt;number&gt;/PLAN.md and must be committed before their implementation; preserve history. If a formal Plan exists, write RESULT.md after implementation. Do not fabricate historical ordering. | 正式 Plan 存於 `records/ISSUE-&lt;number&gt;/PLAN.md`，且必須在其對應實作之前提交；保留歷史。若有正式 Plan，實作後須撰寫 RESULT.md。不得偽造歷史順序。 | Formal Plans go in `records/ISSUE-&lt;number&gt;/PLAN.md` and must be committed before their implementation; preserve history. If a formal Plan exists, write RESULT.md after implementation. Do not fabricate historical ordering. | PASS：固定路徑、Plan 先於實作、歷史保留、正式 Plan 對應事後 Result、禁止偽造順序。 |
| 10 | Record actual Builder work, full reviewed commit, relevant base/scope, findings/verdict and evidence in the PR. Self-review is not cross-review; distinguish Self-Review Evidence from independent Review. Document Fresh-Context Challenge if applied. | 在 PR 記錄實際 Builder 工作、完整 reviewed commit、相關 base／scope、發現／結論及證據。Self-Review 不是交叉審查；須區分 Self-Review Evidence 與獨立 Review。若採用 Fresh-Context Challenge，須記錄該驗證。 | Record actual Builder work, full reviewed commit, relevant base/scope, findings/verdict and evidence in the PR. Self-review is not cross-review; distinguish Self-Review Evidence from independent Review. Document Fresh-Context Challenge if applied. | PASS：實際工作／完整 reviewed commit／base scope／發現結論證據；自審不冒充交叉或獨立 Review；採用 challenge 要記錄。 |
| 11 | Distinguish Bot Summary, native GitHub Review and Human Approval. No mandatory native APPROVED conversion, App/Registry/Attestation/Control Plane/second Human. Do not claim automated trusted identity verification. | 區分 Bot Summary、原生 GitHub Review 與 Human Approval。不強制轉為原生 APPROVED，也不強制要求 App／Registry／Attestation／Control Plane／第二位 Human。不得宣稱自動可信身分驗證。 | Distinguish Bot Summary, native GitHub Review and Human Approval. No mandatory native APPROVED conversion, App/Registry/Attestation/Control Plane/second Human. Do not claim automated trusted identity verification. | PASS：Bot／原生 Review／Human Approval 區分；非強制項不翻成禁止項；禁止宣稱自動可信身分驗證。 |
| 12 | Run applicable tests/CI and strict MkDocs for site changes. Report build/content/provenance/visual/deployment separately. Missing, failed, skipped, pending, stale evidence or unresolved blockers prevents Merge. | 執行適用測試／CI；網站變更須執行 MkDocs strict。Build／內容／來源／視覺／部署分別回報。檢查缺失、失敗、略過、待定、證據過期或仍有未解阻擋事項時，不得 Merge。 | Run applicable tests/CI and strict MkDocs for site changes. Report build/content/provenance/visual/deployment separately. Missing, failed, skipped, pending, stale evidence or unresolved blockers prevents Merge. | PASS：適用測試 CI／網站 strict；五類分報；缺失失敗略過待定過期與 blocker 均阻擋 Merge。 |
| 13 | New head requires Review reconfirmation; base/scope/risk changes require reassessment and renewed authorization where necessary. | 新 head 必須重新確認 Review；base／scope／risk 變化須重新評估，必要時重新取得授權。 | New head requires Review reconfirmation; base/scope/risk changes require reassessment and renewed authorization where necessary. | PASS：新 head 重新確認；base scope risk 變動再評估，必要時重新授權。 |
| 14 | Ready requires completed implementation, applicable verification and conditional Result; follow explicit PR status boundaries and authorization. | Ready 需要完成實作、適用驗證及必要時的 Result；須遵守明確的 PR 狀態邊界與授權。 | Ready requires completed implementation, applicable verification and conditional Result; follow explicit PR status boundaries and authorization. | PASS：完成實作／適用驗證／conditional Result；狀態邊界及授權保留。 |
| 15 | Merge only with explicit operation authority, non-Draft and all applicable conditions met. L1 has no mandatory per-PR Human content approval. No direct main push, force push, bypass, unauthorized Merge/deployment or Auto-Merge activation. | 只有具備明確操作授權、PR 為非 Draft 且所有適用條件均滿足時，才可 Merge。L1 不強制逐 PR 的 Human 內容核准。禁止直接 push main、force push、bypass、未授權的 Merge／部署或啟用 Auto-Merge。 | Merge only with explicit operation authority, non-Draft and all applicable conditions met. L1 has no mandatory per-PR Human content approval. No direct main push, force push, bypass, unauthorized Merge/deployment or Auto-Merge activation. | PASS：Merge 三前提、L1 逐 PR 內容核准豁免、六項禁止操作完整保留。 |
| 16 | Roll back using an authorized revert PR and applicable checks. Human handles L2 Plan/L3 action approval and emergency stop. | 使用已授權的 revert PR 及適用檢查進行回復。Human 負責 L2 Plan／L3 操作核准及緊急停止。 | Roll back using an authorized revert PR and applicable checks. Human handles L2 Plan/L3 action approval and emergency stop. | PASS：授權 revert PR 加適用檢查；Human 的 L2 Plan／L3 操作核准及緊急停止權。 |
| 17 | Archived platform designs/tests and historical records are evidence, not active instructions. C3-C5 and later platform work are stopped. Do not provision new governance infrastructure. | 已封存的平台設計／測試與歷史紀錄是證據，不是現行指令。C3–C5 及後續平台工作已停止。不得建置新的治理基礎設施。 | Archived platform designs/tests and historical records are evidence, not active instructions. C3-C5 and later platform work are stopped. Do not provision new governance infrastructure. | PASS：封存設計測試及歷史只作證據；C3–C5 及後續工作停止；禁止新治理基礎設施。 |

## 結構與情境驗證

- PASS：17 個依序編號的條款，每條恰一個繁體中文段落及一個 English 段落，均非空。
- PASS：原本完整英文的第 05、06、07、09、10、11、12、13、14、15、16、17 條，英文文字逐字保留（第 09 條路徑新增 Markdown code 標記，防止 `<number>` 被視為 HTML）。
- PASS：第 01、02、03、04、08 條以矩陣逐項人工語義核對；全部 17 條再作雙向閱讀。
- PASS：L0 仍免強制 Plan／Result／自審證據；L3 Plan approval 不取代具體實作授權。
- PASS：Claude Code ↔ Codex 不轉移舊結論或授權；交接需完整證據及目前 head 再確認。
- PASS：Human 強制 challenge 不能省略；新 head 重確認；缺適用 CI 不可 Merge；Draft 不可 Merge。
- PASS：Learning Issue 無須 PR；Merge 不授予 Deployment（AGENTS 第 01 條要求閱讀 GOVERNANCE，其獨立授權規範未變）。沒有透過翻譯新增規則。

可重現結構檢查：Python 以 `^## (\d{2})` 擷取 01–17，逐節核對 `**繁體中文**`、`**English**` 各一次及非空；用 `git show f0353b0ee784f60319ae54b89086321c7d20e634:AGENTS.md` 的 17 行原條款比對。此檢查只證明結構／文字保留，不證明翻譯正確。

## 文件一致性與範圍

唯讀核對 GOVERNANCE.md、README.md、INSTALL.md、兩個 Issue Forms、config.yml、PR Template、docs/development/ISSUE_TEMPLATE_INSTALL.md：工具中立責任、教材所有權、學習與工程分工、交接、風險、Plan/Result、Self-Review、操作授權一致，未發現此次翻譯引入的衝突。main 的舊 Claude 指定文字是 PR 原有待審變更，非本次雙語化另改政策。main 為現行政策基準，Codex 身分依本次 Human 明確授權；未採 Archived Platform 為指令。

相對已核准 Plan 僅三個允許路徑；實作 commit 僅 AGENTS.md，後續 records commit 僅本證據及 RESULT.md。Plan blob 保留；舊 Result 以 bytes prefix 驗證完整保留；其他檔案、Workflows、Scripts、歷史 Records、Archived Platform 不變。

## Tests / Build / 適用性

| 項目 | 實際結果 |
|---|---|
| `python3 -B -m unittest discover -s scripts -p 'test_*.py'` | PASS，27 tests |
| `.venv/bin/python -m mkdocs build --strict --site-dir /tmp/clh-issue18-bilingual-site` | PASS，exit 0；使用主工作目錄既有 .venv；Material EOL 提示及既有未列 nav 頁面資訊不構成 strict 失敗 |
| `git diff --check` | PASS |
| AGENTS Markdown 結構與完整段落 | PASS；根目錄 AGENTS 不由 MkDocs 驗證，因此另驗 17 組結構與 Markdown HTML |
| Git 記錄 verifier／額外新實作順序 | records 提交後執行，最終完整 SHA 與結果記於 PR Self-Review；舊 Result 存在不視為本次完成 |
| Governance Tests／Docs Check | 最終 records Head 提交後 PENDING；以 PR 最新完整 SHA 的 CI 及遠端 readback 結果為準 |
| lifecycle／Archived helper 額外 runner | NOT RUN；此次未變 runtime、workflow 或 helper，既有歷史證據保留，27 tests 已涵蓋適用治理檢查 |
| Browser／GitHub Markdown 視覺 | NOT RUN；未宣稱瀏覽器驗收 |
| 合併後 GitHub Issue Forms UI | PENDING，仍需後續授權合併才可核對；非此次雙語化前置實作 |
| 教材品質／來源 | 無教材創作或匯入；本次來源為固定 AGENTS 17 條。CI 不代表教材品質核准 |
| Deployment | NOT RUN，未授權 |

## Self-Review / 剩餘事項

Claim：17 條語義／順序及全部治理要求保留。Source：固定 Plan／原文／現行治理及 Human 授權。Method：三向逐條矩陣、關鍵情境、文件一致性、差異白名單、測試與 Git 順序。Evidence：本文件、AGENTS diff、Result 補充、PR 最新 Head CI。

實作 SHA 的語義自審無未解歧義或 blocker；最終 records Head 必須在 PR 再作 Self-Review 與遠端 Readback，不能沿用原 READY_ELIGIBLE。Fresh-Context Challenge 本次省略：未改政策，17 列完整三向核對、12 條英文文字保留、測試與限定差異提供可追溯證據，未發現需額外 challenge 的翻譯歧義；Human 未指定 challenge。此理由不降低 L3 或取代 Human 審查，亦不宣稱獨立 Review。

風險仍為 L3：自然語言翻譯可能有細微理解差異，矩陣供 Human 逐條審閱。若發現歧義或需擴大範圍，停止並重新取得授權。回復須另行授權 revert PR；本次不執行。PR 保持 Draft，等待 Human 下一次審查。
