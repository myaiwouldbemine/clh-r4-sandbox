---
material_id: NYCU-OS-LEC08
course: NYCU Operating Systems
source_document: lec08.pdf
source_pages: 78
layer: RELEARNING
source_type: original_lecture
status: FULL_DRAFT_PENDING_CODE_AND_HISTORICAL_EVIDENCE
language: zh-TW
---
# LEC08 — Relearning Supplements

> 本清單隨 Issue #24 存入 `RELEARNING_SUPPLEMENTS/ISSUE-24/RELEARNING_SUPPLEMENTS.md`，Issue／PR／SHA 已回填（工程中繼資料，非教學語義變更）。此處為教學階段發現的候選關聯，不冒稱已完成重新學習。

- Material: `NYCU-OS-LEC08`
- Issue: [#24](https://github.com/myaiwouldbemine/myaiwouldbemine-Copy-Learning-Hub/issues/24)
- PR: PR_PLACEHOLDER
- Base SHA: `e5ed923` (main at start); source ZIP SHA-256: `d076448acbe4aef5565e2c386304f09a0fa41181a0eb11f59e3316b8dbbdd33c`
- Scan scope: LEC08 PDF pp.1–78；NYCU_OS 歷史學習脈絡 LR03、LR04、LR05、F10、HW01、FS02
- Scan completion: `PARTIAL`（未重新讀取全部舊教材與 NachOS repo）
- Relearning items: **有，5 項**；不得寫「無」
- Learning status: `PENDING RELEARNING`

| Connection ID | LEC08 | 舊教材 | 關聯類型 | 重讀內容 | Code Trace / 證據 | 跨教材 QA | 狀態 |
|---|---|---|---|---|---|---|---|
| RS-LEC08-001 | pp.9–11、39 | F10 Context Switch | Prerequisite / Extension | 切換 thread 與 address space 的差別 | `Scheduler::Run` → `AddrSpace::RestoreState`（待核） | 同 process 兩 thread 是否一定切換 page table？ | PENDING RELEARNING |
| RS-LEC08-002 | pp.31–38 | HW01 FrameTable | Reuse / Related Code | PTE PFN、frame 配置與釋放 | `FrameTable::Allocate/Release`, `Machine::Translate`（待核） | VPN6、PFN9、128B page 如何得 PA？ | PENDING RELEARNING |
| RS-LEC08-003 | pp.39–45 | LR05 Virtual Memory | Comparison | TLB miss、invalid PTE、demand page fault | `translate.cc`, `exception.cc`（待核） | 有效 PTE 的 TLB miss 為何不等於 page fault？ | PENDING RELEARNING |
| RS-LEC08-004 | pp.44–47 | HW01 NOFF Load | Extension | code/data protection 與共享的條件 | `AddrSpace` NOFF page load（待核） | code page readOnly 何時設定？ | PENDING RELEARNING |
| RS-LEC08-005 | pp.48–59 | LR04 Page Table | Comparison | linear、hierarchical、hashed、inverted | `TranslationEntry` / `pageTable[vpn]`（待核） | FrameTable 為何不必然是 inverted page table？ | PENDING RELEARNING |

## Relearning Protocol

1. **Link**：確認新舊教材有可說明的概念／程式碼關聯。
2. **Revisit**：重開舊教材對應章節與已保存的 Evidence。
3. **Reconstruct**：在 VS Code 追現行程式碼，重建 Call Flow 與狀態。
4. **Verify**：計算、執行與跨教材 QA；記錄版本與證據。
5. **Integrate**：ChatGPT + Human 核准後，才把新理解寫回教材並在下一 Issue 發布。

## 工程與學習界線

- 每個教材 Issue **必須**有此清單；若完成搜尋且沒有新關聯，明確寫「再學習補充項目：無」與掃描範圍。
- 尚未完成掃描時標 `PENDING`／`BLOCKED`，不可寫「無」。
- 建立清單與完整檢查是 Merge Gate；**實際再學習完成不是 Merge Gate**。
- 工程 agent 不得擅自核准教材語義；ChatGPT + Human 負責學習與驗收。
