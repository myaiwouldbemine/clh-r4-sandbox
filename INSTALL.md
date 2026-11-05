# CLH Governance v1.1 — Installation / 安裝說明

此套件準備放入目前的 `feat/CLH-001-project-bootstrap` 分支，並透過 PR 合併；不會自行修改 GitHub。

## Files / 檔案

- `GOVERNANCE.md` — 雙語 PR 政策（含對等 Agent 與 Merge 授權）
- `AGENTS.md` — Claude Code / Codex 共用的精簡執行規則
- `.github/PULL_REQUEST_TEMPLATE.md` — 雙語 PR 驗收表

## Apply / 套用

在 WSL 專案根目錄、正確 Feature Branch 上，將檔案複製到對應路徑（不要複製 `INSTALL.md` 也可以）：

```bash
cd /home/copylearning/myaiwouldbemine-Copy-Learning-Hub
git branch --show-current
# Copy the 3 files into the repository while preserving .github/ path.
git add GOVERNANCE.md AGENTS.md .github/PULL_REQUEST_TEMPLATE.md
git diff --cached --check
git diff --cached --stat
git diff --cached -- GOVERNANCE.md AGENTS.md .github/PULL_REQUEST_TEMPLATE.md
```

請先審閱 Staged Diff，確認內容正確後才 Commit。若前次 Governance 尚未 Commit，可一次提交三份文件；若已 Commit，可另外建立政策升級 Commit，保留歷史。

```bash
git commit -m "docs: adopt bilingual PR governance and shared agent instructions"
```

不要直接 Push `main`。在 CLH-001 Feature Branch 完成 MkDocs / CI 後，再 Push Branch 建立 PR。

## Claude Code compatibility / Claude Code 相容性

```bash
claude --version
```

新版 Claude Code 可以直接載入 `AGENTS.md`，但若有適用的專案或上層 `CLAUDE.md`，預設可能優先採用它。到 Claude Code 的 `/memory` 查看實際載入檔案；必要時使用最小 `CLAUDE.md`（唯一內容 `@AGENTS.md`）作相容性處理。

## Enforcement caveat / 治理生效注意

文件合併不等於 GitHub Rulesets / Branch Protection 已啟用。須在 GitHub Settings 額外設定，且 Required Check 應在 CI 第一次實際運行後再指定。Agent Merge 須另有使用者授權。
