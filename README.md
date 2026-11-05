# myaiwouldbemine Copy Learning Hub

**A Multi-Disciplinary, Code-First, Evidence-Driven Learning Platform**

多學科、程式碼優先、證據導向的個人學習與知識管理平台。

## 1. Project Overview｜專案簡介

Copy Learning Hub 旨在將大學課程講義、技術文件、原始碼、數學公式及實作結果整理為可長期維護的線上學習教材。

主要學習流程：

**Source Materials → Deep Understanding → Code / Formula → Verification → Documentation → Web Publishing**

核心原則：

- **Code-First**：盡可能透過實際程式碼解釋理論。
- **Evidence-Driven**：重要結論必須具備可追溯的來源或驗證紀錄。
- **Page-by-Page Learning**：依原始教材頁碼逐頁深入學習。
- **Progressive Validation**：透過理解驗收與實作確認學習成果。
- **Reusable Knowledge**：將學習成果整理成可重複閱讀的文件。
- **Multi-Agent Collaboration**：Claude Code 與 Codex 共同參與開發與審查。

## 2. Learning Subjects｜學科分類

| Subject | Coverage |
|---|---|
| Operating Systems | NYCU OS, NachOS, Linux, Scheduling, Memory, File Systems |
| Machine Learning | Regression, Classification, Model Evaluation |
| Deep Learning | Neural Networks, Backpropagation, Optimization, PyTorch |
| Computer Vision | CNN, ResNet, Object Detection, Vision Transformers |
| Natural Language Processing | Tokenization, Embeddings, Attention, Transformers, LLM |

未來可新增其他學科，而不需要重新設計平台架構。

## 3. Technology Stack｜技術架構

| Component | Technology |
|---|---|
| Learning Content | Markdown |
| Static Website | MkDocs Material |
| Code Highlighting | Pygments / Markdown Extensions |
| Diagrams | Mermaid |
| Mathematics | MathJax |
| Version Control | Git / GitHub |
| CI/CD | GitHub Actions |
| Hosting | GitHub Pages |
| Future Interactive Labs | Streamlit / Python |
| Agent Collaboration | Claude Code / Codex |

目前採用 MkDocs Material 建立網站，未來可另行評估 Zensical 遷移。

## 4. Repository Structure｜專案結構

```text
myaiwouldbemine-Copy-Learning-Hub/
├── .github/
│   ├── PULL_REQUEST_TEMPLATE.md
│   └── workflows/
│       ├── docs-check.yml
│       └── pages.yml
├── docs/
│   ├── index.md
│   ├── subjects/
│   │   ├── operating-systems/
│   │   ├── machine-learning/
│   │   ├── deep-learning/
│   │   ├── computer-vision/
│   │   └── Natural-Language-Processing/
│   └── assets/
├── AGENTS.md
├── GOVERNANCE.md
├── INSTALL.md
├── mkdocs.yml
├── requirements.txt
└── README.md
```

部分 CI/CD 與學習內容仍屬規劃中，實際目錄以目前 Repository 為準。

## 5. Local Development｜本機開發

### Requirements

- Python 3.12+
- Git
- VS Code（建議）
- WSL Ubuntu（建議）

### Installation

```bash
git clone https://github.com/myaiwouldbemine/myaiwouldbemine-Copy-Learning-Hub.git
cd myaiwouldbemine-Copy-Learning-Hub

python3 -m venv .venv
source .venv/bin/activate

python -m pip install -r requirements.txt
```

### Local Preview

```bash
mkdocs serve
```

開啟：

http://127.0.0.1:8000/

### Build Validation

```bash
mkdocs build --strict
```

本機建置成功只代表網站能夠產生，不代表所有教材內容均已完成技術或教學驗收。

## 6. Learning Content Standards｜教材規範

每個完整的學習單元可包含：

- `README.md`：完整學習筆記。
- `EVIDENCE.md`：原始資料、程式碼與驗證證據。
- `TERMINOLOGY.md`：中英文專業術語。
- `CODE_WALKTHROUGH.md`：必要的程式碼分析。
- `FORMULAS.md`：必要的公式推導。
- `assets/`：圖片與教學圖表。

各學科可以採用專屬教學規範，但共用一致的文件與出版原則。

### Operating Systems

使用 **NYCU OS Learning Framework v3.1 OS Edition**。

重點包括：

- PDF 逐頁深入解說。
- NachOS / Linux 原始碼對照。
- MIPS Assembly。
- VS Code Code Walkthrough。
- Execution Flow / State Trace。
- 理解驗收與證據文件化。

## 7. GitHub PR Workflow & Agent Collaboration｜PR 工作流程與 Agent 協作

Copy Learning Hub 採用 **Pull Request First** 的開發模式。所有正式變更原則上均須經由 PR 合併至 `main`，確保修改過程可檢查、可驗證、可追溯。

### 7.1 Standard PR Workflow｜標準流程

**Issue → Branch → Commit → Pull Request → Review / CI → Merge**

```mermaid
flowchart TD
    A["Issue / Change Request<br/>需求與修改目的"]
    B["Feature Branch<br/>建立工作分支"]
    C["Implementation & Commit<br/>實作、測試、保留變更紀錄"]
    D["Pull Request<br/>WHAT / WHY / TEST / Evidence"]
    E["Review<br/>Agent 或人工審查"]
    F["Required CI Checks<br/>自動化驗證"]
    G{"Merge Conditions<br/>全部符合？"}
    H["Merge into main<br/>合併正式分支"]
    I["GitHub Pages Deployment<br/>網站發布"]
    J["Keep PR Open<br/>修正問題並重新驗證"]

    A --> B --> C --> D
    D --> E
    D --> F
    E --> G
    F --> G
    G -->|Yes| H
    G -->|No| J
    J --> C
    H --> I
```

### 7.2 Agent Roles｜Agent 角色

**Claude Code 與 Codex 是對等 Agent。**

兩者均可參與：

- Implementation（程式碼或教材實作）
- Documentation（文件維護）
- Testing（測試與驗證）
- Code Review（程式碼審查）
- Merge（符合授權條件後合併）

不固定誰負責實作、誰負責審查。同一個 PR 優先由不同 Agent 進行實作與審查；簡單的學習文件修改可採 Self-Review。

Agent Review 屬於輔助驗收，**不得冒充 GitHub 正式 Reviewer Approval**。

### 7.3 Branch & Commit｜分支與提交

所有日常修改須在獨立工作分支執行，不直接 Push 至 `main`。

建議 Branch Naming：

```text
feat/CLH-001-project-bootstrap
fix/CLH-002-navigation
docs/CLH-003-os-learning
ci/CLH-004-build-validation
```

每個 Commit 應說明清楚的修改目的，且避免將無關變更混在一起。

### 7.4 Pull Request Requirements｜PR 必要資訊

每個 PR 至少應包含：

| Field | Requirement |
|---|---|
| WHAT | 修改了什麼 |
| WHY | 為什麼需要修改 |
| TEST | 執行哪些測試及其結果 |
| Evidence | 原始碼、測試輸出或教材驗證依據 |
| Risk | 已知風險與影響 |
| Review | 審查結果及未解決問題 |

PR 優先關聯 Issue，簡單修改可以直接建立 PR。

### 7.5 Review & CI｜審查與自動化檢查

PR 應完成適用的測試及審查。

對 MkDocs 網站的基本驗證：

```bash
mkdocs build --strict
git diff --check
```

GitHub Actions 將負責執行設定好的自動化檢查。

網站 Build 成功並不代表教材的技術內容、程式碼解釋或證據鏈已完成驗收，兩者必須分別確認。

### 7.6 Agent Merge Authorization｜Agent 合併授權

Agent 只有在以下條件**全部符合**時，才可以執行 Merge：

1. 使用者已事先授權該類 PR 可由 Agent Merge。
2. 所有 Required CI Checks 均已通過。
3. 沒有未解決的阻擋性審查意見。
4. 修改範圍符合 Issue 或 PR 的原始目的。
5. 未涉及需要使用者個別確認的高風險操作。

若任一條件未滿足，Agent 必須保留 PR 並回報，不得繞過 Branch Protection 或未通過的必要 CI。

### 7.7 High-Risk Changes｜高風險變更

以下操作需要使用者個別確認：

- 大量刪除或搬移資料。
- 修改 Repository 權限或安全設定。
- 修改重要資料的來源或證據。
- 大規模重構。
- 可能造成不可逆結果的操作。

### 7.8 Governance References｜治理文件

- [GOVERNANCE.md](GOVERNANCE.md) — 正式治理政策。
- [AGENTS.md](AGENTS.md) — Claude Code / Codex 共用執行指令。
- [.github/PULL_REQUEST_TEMPLATE.md](.github/PULL_REQUEST_TEMPLATE.md) — PR 紀錄模板。

**Governance Principle：** PR 的目的在於保存清楚、可檢查、可追溯的學習與修改歷程，而非增加不必要的行政流程。

---

*English summary: All formal changes follow the Issue → Branch → Commit → PR → Review/CI → Merge workflow. Claude Code and Codex are peer agents. Merge requires prior authorization, passing required checks, resolved blocking feedback, scope alignment, and separate approval for high-risk operations. The authoritative policy is maintained in GOVERNANCE.md.*

## 8. Deployment｜網站部署

預計透過 GitHub Actions 自動部署至 GitHub Pages。

預計網址：

https://myaiwouldbemine.github.io/myaiwouldbemine-Copy-Learning-Hub/

部署流程：

1. 在 Feature Branch 修改內容。
2. 建立 Pull Request。
3. 執行 CI 驗證。
4. 完成 Review 並合併至 `main`。
5. GitHub Actions 建立靜態網站。
6. GitHub Pages 發布網站。

**目前部署狀態：尚未完成正式 GitHub Pages 上線驗收。**

## 9. Project Status｜目前進度

**CLH-001 — Project Bootstrap**

- [x] Git Repository 初始化。
- [x] Feature Branch 建立。
- [x] Python / MkDocs 環境安裝。
- [x] 基本網站建置驗證。
- [ ] Governance v1.1 合併至 main。
- [ ] GitHub Actions CI/CD 驗證。
- [ ] 首次 Pull Request 審查及合併。
- [ ] GitHub Pages 部署驗收。
- [ ] 匯入第一份完整 Code-First 學習教材。

以上進度依目前已提供的開發證據整理。

## 10. Roadmap｜未來發展

**Phase 1 — Documentation Portal**

建立穩定的多學科 Markdown 學習網站。

**Phase 2 — Learning Content Integration**

匯入 OS、ML、DL、CV、NLP 的正式學習教材。

**Phase 3 — Interactive Learning Labs**

建立 Streamlit / Python 互動模擬器與練習工具。

**Phase 4 — Personal Learning System**

加入學習進度、錯題複習、知識關聯及跨裝置同步。

---

**Project:** myaiwouldbemine Copy Learning Hub
**Repository:** https://github.com/myaiwouldbemine/myaiwouldbemine-Copy-Learning-Hub
**Development Policy:** Pull Request First
**Learning Philosophy:** Code-First · Evidence-Driven · Deep Understanding
