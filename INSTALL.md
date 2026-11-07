# On-Demand Autonomous Engineering｜按需自主工程

閱讀 [GOVERNANCE.md](GOVERNANCE.md)、[完整雙語 AGENTS.md](AGENTS.md) 與 [操作手冊](docs/development/AUTONOMOUS_OPERATIONS.md)。Human + ChatGPT 規劃教材／建立 Issue，Human 在需要時啟動 Codex App；單一 Builder 自主處理工程與符合 Gate 的生命週期，不需 Human 日常 Merge 或重複批准。

Use the existing Codex App sign-in for model access and existing `gh auth` for GitHub. They are separate logins. No extra `OPENAI_API_KEY`, `CLH_AUTOMATION_TOKEN`, activation variable, resident service or hosted model runner is required. Never copy App/gh credentials into Actions or expand privileges to pass a gate.

```bash
gh auth status
git fetch origin
python3 scripts/autonomous_lifecycle.py preflight --repo myaiwouldbemine/myaiwouldbemine-Copy-Learning-Hub
python3 -m unittest discover -s scripts -p 'test_*.py'
.venv/bin/python -m mkdocs build --strict
git diff --check
```

保留 main 的 strict docs-check／governance-tests、PR-only、無 bypass／force/delete 與 resolved threads；Pages 使用 GitHub Actions 來源及 main-only environment。CI 僅讀取，Pages 部署以原生 GITHUB_TOKEN／OIDC 執行，不使用額外 PAT。既有設定仍需讀回，不以文件代替權限驗證。

Install changes through a normal PR. Commit formal Plans separately before implementation and write Results afterward. A protected merge to main triggers Pages automatically. Verify the published SHA over HTTPS, archive the evidence and read it back before closing the Issue.

關閉 App 不承諾繼續工程；已送出的 CI／Pages 工作可完成。重啟後讀取 Issue／留言、PR、head／base、CI、部署及歸檔證據再恢復。中斷與回復步驟見操作手冊；不重複 Merge、不提早 Close。
