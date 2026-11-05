# Pull Request / 變更申請

## 1. Issue / Work ID · 工作編號

- Work ID / 工作編號：`CLH-___`
- Related Issue / 關聯 Issue：`#___`（optional / 可選）
- Base / 目標分支：`main`

## 2. Why · 變更原因

<!-- Why is this necessary? / 為何需要此修改？ -->

## 3. What · 修改內容

<!-- List exact changed files, behavior, course pages / 列出受影響檔案、功能與教材頁面 -->

## 4. Scope / Out of Scope · 範圍與排除項目

- In scope / 本次範圍：
- Out of scope / 本次不處理：

## 5. Validation & Evidence · 驗收與證據

<!-- PASS / FAIL / NOT RUN / N/A. Do not invent results. / 未執行不得寫 PASS -->

| Check / 檢查 | Status / 狀態 | Evidence / 證據 |
|---|---|---|
| `git diff --check` / staged check | NOT RUN | |
| `mkdocs build --strict` (if applicable) | NOT RUN | |
| GitHub Actions Required CI | NOT RUN | |
| Web rendering (links / code / Mermaid / math / mobile) | NOT RUN | |
| Content source & technical accuracy | NOT RUN | |

## 6. Provenance & Publication · 來源與發布

- [ ] Original source / PDF page / repository path identified where applicable / 已記錄來源
- [ ] Verified code distinguished from teaching examples / 已區分驗證原始碼與教學示例
- [ ] Publication rights checked / 公開授權已檢查
- [ ] No secrets, private data, `.venv/`, or `site/` artifacts / 未洩漏機密及建置產物

## 7. Roles & Review · 角色與審查

- Implementer / 實作者（Human / Claude Code / Codex）：
- Reviewer / 審查者（Human / Claude Code / Codex / Self-Review）：
- Agent review findings & resolution / Agent 審查發現及處理：
- [ ] Agent review is not represented as GitHub formal approval / 未冒充正式核准
- [ ] Blocking comments resolved / 阻擋性意見已解決

## 8. Merge Authorization / 合併授權

- Authorization reference / 使用者事先授權依據（PR link / issue / explicit message）：
- Scope of authorized PR class / 授權範圍：
- Required CI at latest head / 最新 Commit 必要檢查：
- [ ] Scope unchanged / 無額外修改
- [ ] No unresolved blocking reviews / 無阻擋意見
- [ ] No branch-rule bypass / 不繞過保護
- [ ] High-risk change? / 是否高風險：No / Yes
- If Yes: specific user approval / 若是，個別核准依據：

> Blank authorization means **do not agent-merge**. / 授權留白時 Agent 不得 Merge。

## 9. Risk & Rollback · 風險與回復

- Risks / 風險：
- Rollback plan / 還原方式：

## 10. Post-Merge / 合併後

- Deployment URL / 部署網址：
- Pages deployment status / 部署狀態：NOT RUN
- Follow-up / 後續事項：
