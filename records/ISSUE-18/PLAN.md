# Issue #18 — Formal Plan v1.2：AGENTS.md 逐條雙語化補充

版本：**v1.2**；日期：2026-11-06（Asia/Taipei）。
狀態：**規劃草案；等待 Human 核准固定 SHA，雙語化實作尚未授權。**
Accountable Builder：**Codex**。
Issue：https://github.com/myaiwouldbemine/myaiwouldbemine-Copy-Learning-Hub/issues/18
Draft PR：https://github.com/myaiwouldbemine/myaiwouldbemine-Copy-Learning-Hub/pull/19

## Goal｜目標

將單一 `AGENTS.md` 的既有 17 條規範整理為逐條「繁體中文 → English」完整對照，兩種語言承載同一組義務、條件、例外、禁止與授權規則。不得新增、刪除、弱化或重新詮釋治理要求，不新增語言優先權。

## WHY｜理由與本次調查

Human 在 Phase 3 Ready Gate Review 後新增正式雙語版要求；既有檔案雖已完成工具中立分工，仍為中英文混用，不能滿足每條完整雙語對應。

本次已重新讀取最新 Issue（包含 Additional Human Request，updated_at：2026-11-06T13:36:27Z）、PR metadata、17 條 AGENTS、Plan v1.1 與 Phase 2 授權。核對時工作樹乾淨，PR 仍 Draft／未合併，Head／Base 未變：

- 現行政策基準：`main @ 7e530cdc818044ae4f760a021a331f888f993e43`。
- 本補充變更的直接比較基準與原條款來源：`d0f400cc56a4aa3db914c0029cd6e9c1f9292038`。
- 已核准 v1.1 固定版本：[70acc21a5d15a9061c8b2a896b5b9a9987cda7cd](https://github.com/myaiwouldbemine/myaiwouldbemine-Copy-Learning-Hub/blob/70acc21a5d15a9061c8b2a896b5b9a9987cda7cd/records/ISSUE-18/PLAN.md)。
- 原 Phase 2 實作 commit：`d32c5b57d4f5313a247fa34db547d08463c078a5`；原 [Result](RESULT.md)、[Evidence](VERIFICATION.md)、[授權來源](AUTHORIZATION.md) 保留。

v1.1 已核准且已實作的九檔工作不重新包裝成未來工作。本版是其雙語補充規劃，保留原驗收要求，包括合併後才可執行的表單 UI readback。原 Plan 的「nine topics」筆誤已由 AUTHORIZATION／Result 說明依八個明列欄位執行，本版不另增加學習欄位。

## Scope｜修改範圍

| 階段 | 允許範圍 | 明確不包含 |
|---|---|---|
| 本次規劃授權 | 僅修訂 `records/ISSUE-18/PLAN.md`，獨立 commit／push 至既有 PR 分支，唯讀檢查及 CI readback；必要規劃說明置於本 Plan | 不修改 AGENTS、Result、其他正式檔案或歷史 Records；不發佈未核准 v1.2 為 Approved Plan |
| 待 Human 另行授權的實作 | `AGENTS.md` 17 條雙語化；`records/ISSUE-18/BILINGUAL-EVIDENCE.md`（新增）、`records/ISSUE-18/RESULT.md`（追加補充結果，保留 Phase 2 區段）；PR 自審／Evidence 更新 | 不修改其餘八個既有實作檔案、其他 Records、Workflows、Scripts、設定、教材或 Archived Platform |

授權後如需額外證據檔案、變更政策或其他路徑，先回報並取得適用修訂／授權，不以本 Plan 推定允許。原 v1.1、Phase 2 證據與本版修訂完整保留於 Git 歷史，不 amend、rebase 或 force push。

## Boundary｜治理與授權邊界

本次 Human「Issue #18 — Phase 2 Supplement: Formal Plan v1.2」聊天訊息只授權規劃、獨立提交與核對 CI。訊息無可公開聊天 URL；來源是本聊天明確指示，不把 Builder 記錄當作 Human 原生核准或自動身分驗證。

本版是待核准 Plan，不是生效政策。對已完成分支的 17 條文字作忠實對照，不藉翻譯讓 main 尚未合併的內容提前生效。以 main 治理及有效 Human 任務授權為操作依據；若原文存在歧義或與政策衝突，不以翻譯自行裁決，停下回報。

不得 Ready、Merge、Close Issue #18、Deploy、啟用 Auto-Merge、執行任何 Merge／Close／Deploy workflow_dispatch、改 GitHub Settings、直接推 main 或 bypass。舊 Head 的 READY_ELIGIBLE 只作歷史證據；新要求尚未完成，新 Head 必須重新審查。PR #19 維持 Draft。

## Risk Level｜風險評估

維持 **L3**，不因翻譯／Markdown 外觀而降為 L0。改的是治理指令全文，主要風險如下：

| 風險 | 控制與阻擋條件 |
|---|---|
| must／may／must not 強度漂移 | 每條拆解義務／可選／禁止；條件及例外逐項對照，任何不等義阻擋完成 |
| L0 豁免、L2／L3 核准條件被漏譯 | 逐項檢查風險分類、事前 Plan、具體實作授權，不以「一般授權」概括 |
| Content Ownership／交接範圍漂移 | 保存主體、唯一 Builder、內容權利、交接欄位及不自動繼承義務 |
| Ready／Merge／Deployment 被合併成同一決策 | 保留原有獨立條件，對照 GOVERNANCE／原已核准流程；不得新增或省略權限 |
| 雙語兩套規則長期漂移 | 一個文件、17 組同位置對照、共同條款編號；不拆成兩份文件或兩套清單 |
| 舊 CI／審查錯用於新 head | 所有新證據綁定新完整 SHA；新 head 再確認，自動 CI 不等同語義驗收 |

沒有新增 runtime、平台或權限設定需求；風險控制依直接證據與 Human 核准，不聲稱自動驗證語義等價或可信身分。

## Implementation Plan｜雙語設計與執行順序

1. 本次：完成 v1.2 規劃、17 條來源盤點與下列矩陣，僅 Plan 獨立提交；讀回固定 SHA、Records diff、Draft 與適用 CI；回報後 STOP。
2. Human 核准固定 v1.2 SHA，並另行授權具體雙語實作／證據路徑後，才開始依賴該授權的工作；先重新核對 Head／Base／scope／risk。
3. 依既有政策於 Issue Timeline 發佈已核准 v1.2（版本、SHA、Records、scope、Human Approval 參考），完成雙向 readback。未核准版本不得發佈為 Approved Plan。
4. 只在單一 `AGENTS.md` 中保留原序 17 條，使用 01–17 對應編號與下列格式；每段完整表達該條，不以另一語言段落補足遺漏。可保留英文術語與原路徑，不引入新概念。

```markdown
## 01. 條款主題

**繁體中文**

完整表達原條款的規範。

**English**

Complete corresponding instruction with identical meaning.
```

此為格式示意，不是實作翻譯；標題僅導覽，不承載新增規則。兩個段落必須包含相同主體、義務強度、觸發條件、例外、禁止、授權及證據範圍。

5. 補齊 BILINGUAL-EVIDENCE 的 17 條完整三向矩陣，執行語義審查、文件一致性、適用驗證；翻譯有疑義就標記 PENDING 並回報。
6. 獨立提交實作後，在 Result 追加本補充的 Results／Evidence／PR／Commit／Deviations／Unfinished，保留原 Phase 2 結果。最後 records commit 後再確認新 Head Self-Review／CI／remote readback。
7. 回報固定新 Head 與驗證，STOP 等待 Human；不自動恢復 READY_ELIGIBLE、不切換 Ready 或 Merge。

## 語義一致性矩陣設計

正式 Evidence 每列須含：條款 ID、來源固定 SHA／原文、完整繁體中文、完整 English、主體、Mandatory／Optional／Prohibited、條件／例外、授權／Evidence、雙向核對結果與發現。不可只用關鍵詞出現或字數比對宣稱等義。

以下原文取自直接基準的 17 個條目；ZH／EN 欄位是未實作的驗證位置。實作後必須填入完整文字／精確位置，逐項判定；現在全部為 NOT RUN。每列「不可遺漏」僅供檢查，原條款全文為對照依據。

| ID | 原條款（來源固定 Head） | 繁體中文對照 | English 對照 | 不可遺漏的語義／驗證重點 |
|---|---|---|---|---|
| 01 | Read GOVERNANCE.md and the Issue boundary. Human myaiwouldbemine is the sole administrator; 採 Tool-Neutral Single-Builder + Self-Verification：每個工程 Issue／PR 在任一時點只有一位指定 accountable Builder（Claude Code 或 Codex），兩者適用相同風險、驗證、Self-Review、Evidence 與授權規範。 | ZH-01：待授權，NOT RUN | EN-01：待授權，NOT RUN | 讀取 GOVERNANCE／Issue 邊界；唯一 Human 管理者；每個工程 Issue／PR 任一時點只有一位指定 Claude Code 或 Codex；兩工具適用相同規範。 |
| 02 | ChatGPT＋Human 擁有 V2／V3 教材創作、推導、品質核准與整合定稿權；製作時分開、定稿時合併、網站上依主題呈現。GitHub 保存已核准教材、版本及學習軌跡；MkDocs 提供閱讀、搜尋、導覽與展示。Builder 負責工程及忠實匯入已核准教材，不創作或修改教材語意；語意問題標記 PENDING，交由 ChatGPT／Human 決定。 | ZH-02：待授權，NOT RUN | EN-02：待授權，NOT RUN | ChatGPT＋Human 擁有創作、推導、品質核准與定稿權；V2／V3 三階段原則；GitHub／MkDocs 分工；Builder 僅工程及忠實匯入；語意問題 PENDING。 |
| 03 | Learning Record Issue 可透過 Comments 逐步更新，不必對應工程 PR；只有 Repository 變更需要下列工程流程。Issue 建立、CI PASS、PR Merge 或 Issue Closed 均不代表內容品質核准、學習完成或完全掌握。 | ZH-03：待授權，NOT RUN | EN-03：待授權，NOT RUN | 學習 Issue 可逐步留言、不強制工程 PR；只有 Repository 變更走工程流程；建立／CI／Merge／Closed 不等於品質、完成或掌握。 |
| 04 | 工程 Issue／PR 記錄唯一 accountable Builder。交接記錄前後 Builder、完整 Commit SHA、base／scope／risk、已完成／未完成、Evidence 與 Blockers。接手者重新確認目前 head 的 Self-Review、證據有效性及適用 Human 授權，評估 base／scope／risk 變化；工具更換不自動轉移舊審查結論或 Human 授權。 | ZH-04：待授權，NOT RUN | EN-04：待授權，NOT RUN | 唯一責任及交接所有欄位；目前 head 自審、證據、base／scope／risk 與適用授權再確認；工具更換不自動移轉舊結論或授權。 |
| 05 | Use Issue → Draft PR → conditional Plan → Implementation → conditional Result → Self-Review → authorized Merge. Open Draft early; Draft grants no implementation or merge authority. | ZH-05：待授權，NOT RUN | EN-05：待授權，NOT RUN | Issue→Draft→條件 Plan→實作→條件 Result→Self-Review→授權 Merge；早開 Draft；Draft 無實作或合併授權。 |
| 06 | Classify actual impact: L0 nonsemantic typo/formatting, L1 substantive content/code, L2 major architecture/provenance, L3 security/governance/permissions/deployment/irreversible operations. Unknown risk blocks clarification-dependent work. | ZH-06：待授權，NOT RUN | EN-06：待授權，NOT RUN | L0 非語意；L1 實質內容／程式；L2 重大架構／來源鏈；L3 安全／治理／權限／部署／不可逆；未知風險阻擋依賴澄清的工作。 |
| 07 | L0 needs no mandatory Plan/Result or Self-Review evidence. L1 needs traceable Self-Review with documented Evidence. L2/L3 need pre-implementation Plan and Human approval; L3 also needs specific action/scope authorization. | ZH-07：待授權，NOT RUN | EN-07：待授權，NOT RUN | L0 無強制 Plan／Result／Self-Review Evidence；L1 可追溯自審證據；L2／L3 事前 Plan＋Human 核准；L3 另需具體操作／範圍授權。 |
| 08 | Fresh-Context Challenge: Optional verification per risk; not mandatory daily review. 由指定 Builder 評估必要性並記錄執行或省略理由。 Human-mandated challenges cannot be skipped. Not an Agent Handoff or governance platform. | ZH-08：待授權，NOT RUN | EN-08：待授權，NOT RUN | Fresh-Context 依風險可選、非每日必做；指定 Builder 評估並記錄採用／省略理由；Human 指定不得省略；不是交接或新平台。 |
| 09 | Formal Plans go in records/ISSUE-<number>/PLAN.md and must be committed before their implementation; preserve history. If a formal Plan exists, write RESULT.md after implementation. Do not fabricate historical ordering. | ZH-09：待授權，NOT RUN | EN-09：待授權，NOT RUN | 正式 Plan 固定 records 路徑且實作前提交、保存歷史；存在正式 Plan 就須事後 Result；不得偽造時間順序。 |
| 10 | Record actual Builder work, full reviewed commit, relevant base/scope, findings/verdict and evidence in the PR. Self-review is not cross-review; distinguish Self-Review Evidence from independent Review. Document Fresh-Context Challenge if applied. | ZH-10：待授權，NOT RUN | EN-10：待授權，NOT RUN | PR 記錄實際 Builder 工作、完整 reviewed commit、base／scope、發現／結論／證據；自審非交叉／獨立審查；適用時記錄 challenge。 |
| 11 | Distinguish Bot Summary, native GitHub Review and Human Approval. No mandatory native APPROVED conversion, App/Registry/Attestation/Control Plane/second Human. Do not claim automated trusted identity verification. | ZH-11：待授權，NOT RUN | EN-11：待授權，NOT RUN | Bot Summary／原生 Review／Human Approval 區分；不強制原生 APPROVED、App／Registry／Attestation／Control Plane／第二 Human；不宣稱自動可信身分驗證。 |
| 12 | Run applicable tests/CI and strict MkDocs for site changes. Report build/content/provenance/visual/deployment separately. Missing, failed, skipped, pending, stale evidence or unresolved blockers prevents Merge. | ZH-12：待授權，NOT RUN | EN-12：待授權，NOT RUN | 適用測試／CI；網站變更 strict MkDocs；build／內容／來源／visual／deployment 分開；缺失／失敗／skipped／pending／stale／未解阻擋不能 Merge。 |
| 13 | New head requires Review reconfirmation; base/scope/risk changes require reassessment and renewed authorization where necessary. | ZH-13：待授權，NOT RUN | EN-13：待授權，NOT RUN | 新 head 必須重新確認 Review；base／scope／risk 變化重新評估，必要時重新授權。 |
| 14 | Ready requires completed implementation, applicable verification and conditional Result; follow explicit PR status boundaries and authorization. | ZH-14：待授權，NOT RUN | EN-14：待授權，NOT RUN | Ready 需要實作完成、適用驗證與條件 Result；依明確 PR 狀態邊界及授權辦理。 |
| 15 | Merge only with explicit operation authority, non-Draft and all applicable conditions met. L1 has no mandatory per-PR Human content approval. No direct main push, force push, bypass, unauthorized Merge/deployment or Auto-Merge activation. | ZH-15：待授權，NOT RUN | EN-15：待授權，NOT RUN | Merge 須明確操作授權、非 Draft 且條件完整；L1 無逐 PR Human 內容核准；禁止 direct main push／force push／bypass／未授權 Merge 或部署／Auto-Merge 啟用。 |
| 16 | Roll back using an authorized revert PR and applicable checks. Human handles L2 Plan/L3 action approval and emergency stop. | ZH-16：待授權，NOT RUN | EN-16：待授權，NOT RUN | 授權 revert PR 與適用檢查；Human 處理 L2 Plan／L3 操作核准及緊急停止。 |
| 17 | Archived platform designs/tests and historical records are evidence, not active instructions. C3-C5 and later platform work are stopped. Do not provision new governance infrastructure. | ZH-17：待授權，NOT RUN | EN-17：待授權，NOT RUN | Archived 設計／測試／歷史為證據而非現行指令；C3–C5 及後續平台停止；不建新治理基礎設施。 |

## Acceptance Criteria｜驗收標準

- 單一 AGENTS.md，恰為 17 條規範／17 組繁中與英文對照；原順序與逐條追溯保留，無整條遺漏或重複。
- 每個語言段落單獨閱讀都完整傳達該條；11 類 Human 必保內容及全部原始子要求都有覆蓋。
- 17 列三向矩陣全部完成，主體、Mandatory／Optional／Prohibited、風險、條件／例外、權限與證據均等義；未解歧義或翻譯差異阻擋完成。
- Human Plan Approval 與具體 Implementation Authorization 不互相取代；Ready／Merge／Deployment 的獨立性、非 Draft 前提、L1 內容核准豁免、禁止未授權操作完整保留。
- main／現有 GOVERNANCE／README／表單／PR Template 的一致性重新檢查；不藉翻譯修正其他文件或擴大規範。
- 相對前一 Head，實作增量僅 AGENTS 及已明確授權的本 Issue 證據；其他正式文件與歷史證據不變。
- v1.2 規劃 commit 在雙語實作之前；Human 核准與具體授權先於實作；補充 Result 在實作之後；新完整 head 有適用測試／CI、Self-Review 及遠端 readback。
- GitHub 表單 UI 仍依既有 Plan 留待授權合併後；不能因本次雙語化而冒稱已完成。PR 維持 Draft，所有未執行標示 NOT RUN、待定標示 PENDING。

## Verification Strategy｜驗證方法

| 項目 | 方法及證據 | 本次規劃狀態 |
|---|---|---|
| 基準與來源 | 重新讀 Issue／PR，核對 main、前一 Head、原 17 條；固定來源及 v1.1 授權歷史 | 已核對；未變 |
| 規劃範圍 | 前一 Head→新 Plan commit 只允許 PLAN.md；AGENTS、Result 及其他檔案 blob 均相同；git diff --check | 提交前／後核對，結果在 PR／回報綁定 SHA |
| 雙語結構 | 讀取 Markdown，確認 17 個條款編號及各一個繁中／English 段落；無空段、跨條補足或語言拆檔 | NOT RUN，尚未實作 |
| 語義等價 | 原文→ZH、原文→EN、ZH↔EN 三向核對；逐項主體、義務、條件、例外、禁止、授權與 Evidence；完整記錄發現 | NOT RUN |
| 關鍵情境 | L0 豁免；L3 未授權不得實作；兩工具互換但不繼承；Human 強制 challenge；新 head；缺 CI；Draft 不可 Merge；Merge 不授權部署；學習 Issue 無 PR | NOT RUN |
| 文件一致性 | 唯讀核對 GOVERNANCE、README、兩表單、PR Template、INSTALL／安裝說明；只改 AGENTS；歧義停止回報 | NOT RUN，待實作後重驗 |
| 適用測試 | 重新執行 `python3 -m unittest discover -s scripts -p 'test_*.py'`；語義與路徑檢查另記，不稱 unittest 證明翻譯正確 | NOT RUN，待雙語實作 |
| Build／格式 | `python -m mkdocs build --strict`、`git diff --check`；AGENTS 不在網站輸入內，另查 Markdown 對照結構／可讀性 | NOT RUN，待雙語實作；本次規劃遠端 CI 另回報 |
| 既有額外 runner | lifecycle／歸檔 helper 未變，原執行證據保留；重新評估適用性，不為翻譯宣稱它們證明等義；新失敗／風險才擴大驗證 | 依實作差異判斷並記錄，不虛報重跑 |
| Git 順序／Result | 既有 verify_plan_records 檢查＋額外確認 v1.2 commit 早於首個雙語 AGENTS commit，補充 Result 晚於它；舊 Result 存在不代表新增工作完成 | 待實作與補充 Result 後執行 |
| CI／遠端 | 每個待審新 head 的 docs-check／governance-tests，記錄完整 SHA、run URL、結論；讀回 PR Draft、head／base、Plan／Result，檢查 Review／Threads | 本次 Plan 提交後 PENDING，實際結果在 PR／最終回報 |
| Self-Review | Codex 記錄 Claim／Source／Method／Evidence／完整 SHA／base／scope、發現與結論；records 新 commit 後也重新確認 | 本次只審規劃；雙語實作 NOT RUN |

Fresh-Context Challenge：本次 Plan-only 省略，因未改規範正文且僅規劃明確對照驗證；在雙語實作後按實際翻譯疑義重新評估並記錄理由。Human 明確要求時不可省略。不新增 mandatory cross-review、原生 APPROVED、第二 Human 或治理平台，不把同一 Builder 的雙向核對冒充獨立 Review。

Build、內容、來源、visual、deployment 分開記錄；沒有教材創作／匯入，CI 不代表內容品質。Browser／視覺若未執行如實 NOT RUN；表單 post-merge UI 為 PENDING。適用 Gate 缺證據或失敗時不得放行。

## Human Decisions｜授權狀態

| 決策 | 狀態與具體範圍 |
|---|---|
| v1.1 原 Phase 2 Plan 與實作 | 已獲原 Human 授權且完成；固定歷史不改寫 |
| v1.2 規劃及獨立提交 | 本聊天 Human 明確 AUTHORIZED；Codex 繼續 accountable Builder |
| v1.2 固定 SHA Plan 核准 | PENDING；待本次提交後由 Human 審閱 |
| 雙語化具體實作 | NOT AUTHORIZED；需另行授權 AGENTS 及本 Plan 所列 BILINGUAL-EVIDENCE／Result 補充、PR Evidence |
| Ready／Merge／Close Issue／Deployment／workflow_dispatch | NOT AUTHORIZED；本次與後續實作都不自動包含 |

任何新增路徑或重大 scope／risk 變動先停止、修訂 Plan 並取得必要核准。若日後需要回復雙語變更，採另行授權 revert PR 與適用驗證，保留 Plan／Result／Git 歷史；本版不授予 rollback 操作權。

## Revision History｜版本歷史

| 版本 | 日期 | 說明／固定歷史 | 狀態 |
|---|---|---|---|
| v1.0 | 2026-11-06 | 首次調查及獨立 Plan，`efe0fedf7490781f53e6467dfc4b848cafbd37fb` | 歷史規劃版本，保留 |
| v1.1 | 2026-11-06 | 一致性稽核與九檔 scope；Human 審閱固定 SHA `70acc21a5d15a9061c8b2a896b5b9a9987cda7cd` | 已核准並完成原 Phase 2；不涵蓋此次新增雙語實作 |
| v1.2 | 2026-11-06 | 增補 17 條單檔雙語設計、三向矩陣、L3 風險、驗收／新 Head 驗證及明確補充 scope；本次獨立 commit SHA 於 PR／回報提供 | 僅規劃授權；Plan 核准及實作 PENDING |
