# Copy Learning Hub — 治理文件維護說明

以目前 main 的 `GOVERNANCE.md`、`AGENTS.md` 與 Issue 邊界為準；本文件說明授權後的文件維護方式，不授予 GitHub 設定或工程操作權限。

## Files / 檔案

- `GOVERNANCE.md` — 正式政策（Tool-Neutral Single-Builder + Self-Verification 與獨立操作授權）
- `AGENTS.md` — Claude Code / Codex 共用的精簡執行規則
- `.github/PULL_REQUEST_TEMPLATE.md` — 工程 PR 與 Self-Review 紀錄模板

## Apply / 套用

每個工程 Issue／PR 只有一位指定 accountable Builder（Claude Code 或 Codex），適用相同規範。ChatGPT＋Human 負責教材創作與品質核准；Builder 僅忠實匯入已核准教材及處理工程。Learning Issue 可獨立記錄，不必對應 PR；只有 Repository 變更需要工程流程。

先確認 Issue 與工作邊界、建立工作分支並提早開 Draft PR。治理變更屬 L3，須在實作前獨立提交正式 Plan，取得 Human 對 Plan 及具體操作／範圍的明確授權。Draft 不等於實作授權。授權後才在 WSL 專案根目錄、正確 Feature Branch 上修改指定檔案並檢查差異：

```bash
cd /home/copylearning/myaiwouldbemine-Copy-Learning-Hub
git branch --show-current
# 僅在本次授權包含以下檔案時暫存。
git add GOVERNANCE.md AGENTS.md .github/PULL_REQUEST_TEMPLATE.md
git diff --cached --check
git diff --cached --stat
git diff --cached -- GOVERNANCE.md AGENTS.md .github/PULL_REQUEST_TEMPLATE.md
```

請先審閱 Staged Diff，確認範圍正確後才 Commit。保留已提交的 Plan 與修訂歷史，不將 Plan 與其實作放在同一初始提交。

```bash
git commit -m "docs: align authorized governance documentation"
```

不要直接 Push `main`。將工作分支推送至既有 Draft PR，完成適用 MkDocs strict／測試／CI、Result 與目前 head 的 Self-Review／Evidence；新 head 或 Builder 交接須依治理重新確認，不能自動沿用審查或 Human 授權。Ready、Merge 與 Deployment 仍各依有效授權辦理。

## Claude Code compatibility / Claude Code 相容性

```bash
claude --version
```

新版 Claude Code 可以直接載入 `AGENTS.md`，但若有適用的專案或上層 `CLAUDE.md`，預設可能優先採用它。到 Claude Code 的 `/memory` 查看實際載入檔案；必要時使用最小 `CLAUDE.md`（唯一內容 `@AGENTS.md`）作相容性處理。

## Enforcement caveat / 治理生效注意

文件合併不等於 GitHub Rulesets / Branch Protection 已啟用。本文件不授權變更 GitHub Settings／權限或啟用 Auto-Merge；如需變更，另依 L3 具體授權辦理。Merge 須另有操作授權；Pages 只有手動入口且 Deployment 需獨立授權。
