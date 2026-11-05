# Copy Learning Hub — Shared Agent Instructions / 共用 Agent 指令

**Version / 版本:** 1.1
**Repository:** `myaiwouldbemine/myaiwouldbemine-Copy-Learning-Hub`
**Applicable agents / 適用:** Claude Code, Codex, and other authorized coding agents

## 1. Project / 專案

Copy Learning Hub is a multidisciplinary, Code-First, Evidence-Driven learning platform.
Copy Learning Hub 是多學科、程式碼優先、證據導向的學習平台。

- Current site stack / 現行網站：MkDocs Material, Markdown, Mermaid, MathJax, GitHub Actions, GitHub Pages.
- Subjects / 學科：Operating Systems, Machine Learning, Deep Learning, Computer Vision, NLP; new subjects must remain easy to add.
- Canonical content / 主要教材來源：可編輯 Markdown；HTML 與註解 PDF 為衍生輸出，不應成為獨立、互相矛盾的教材版本。
- OS-specific learning instructions / OS 專屬學習規範：use v3.1 OS Edition Code-First when provided; do not impose OS-specific rules on other subjects.

## 2. Authority / 權限及規範

- **Read and follow `GOVERNANCE.md` before changing files, creating a PR, or attempting a merge.** 變更前先閱讀治理政策。
- `GOVERNANCE.md` is the canonical PR, CI, merge, risk and incident policy. This file is the concise agent execution guide. 治理政策優先管理 PR 與風險門檻。
- Agents are peers: Claude Code and Codex may each implement, review, test, document, and merge **only when explicitly authorized and all merge gates pass**. 兩者對等、不固定角色，不能自動獲得合併授權。
- Prefer different agents for implementation and review. Simple, low-risk documentation edits may be self-reviewed with an explicit record. 同一 PR 優先交叉審查；低風險文件可 Self-Review。
- Agent review is **not** GitHub formal Reviewer Approval. Agent 審查不得冒充 GitHub 正式核准。

## 3. Git and Pull Requests / Git 與 PR

Use **Issue (recommended) → Branch → Commit → PR → CI / Review → Authorized Merge**.
建議 Issue 起始，但小修改可直接 PR；所有正式變更都走 PR。

- Never directly push ordinary changes to `main`; never force-push or delete protected `main`.
- Make one coherent change per PR; keep unrelated work separate.
- Branch names: `feat/CLH-NNN-*`, `fix/CLH-NNN-*`, `docs/CLH-NNN-*`, `ci/CLH-NNN-*`, `chore/CLH-NNN-*`, `hotfix/CLH-NNN-*`.
- Record **WHAT, WHY, TEST, EVIDENCE**, out-of-scope, risks and rollback in the PR template.
- Never bypass branch protection or required CI. Never claim a check passed without observed evidence.
- Merge only with traceable prior user authorization for that PR class; confirm required checks, scope and review resolution on the current PR head. High-risk actions require separate case-specific confirmation. If blocked, leave PR open and report why.
- Prefer Squash and merge after the applicable gates; verify deployment afterwards. 優先 Squash Merge 並驗證上線結果。

## 4. Validation / 驗證

- For site / navigation changes run `mkdocs build --strict` inside the project's Python virtual environment when available.
- Run `git diff --check` or `git diff --cached --check` as appropriate.
- Inspect links, Mermaid, MathJax, code formatting and responsive display when affected.
- Separate **build PASS**, **content verified**, and **learner assessment PASS**. They are different claims.
- In reports use `PASS`, `FAIL`, `NOT RUN`, or `N/A` with commands and evidence. Never fabricate CI, source reads, or runtime output.

## 5. Learning Content and Provenance / 教材與來源

- Prefer Code-First explanations with **WHAT / WHY / HOW / EXAMPLE / TRACE / EVIDENCE** when useful.
- Distinguish `PDF SOURCE`, `VERIFIED SOURCE CODE`, `TEACHING EXAMPLE`, `EXTERNAL VERIFIED`, and `UNVERIFIED`.
- Record exact PDF pages / code paths only when actually checked. 不可編造頁碼、行號、執行結果。
- Preserve existing learning evidence and distinguish original annotations from AI explanations.
- For substantial lessons, use appropriate `README.md`, `EVIDENCE.md`, `TERMINOLOGY.md`, optional formulas/code/review files.
- Do not publish private information, secrets, or unlicensed course PDFs and third-party figures.

## 6. High-Risk Actions / 高風險操作

Get **specific user confirmation for the individual action**, even if a class of PRs has merge authorization, before:

- Bulk deletion, relocation, destructive rewrite, history changes.
- Permission, security, secrets, branch protection or ruleset changes.
- Material changes to learning source evidence or validation history.
- Major refactoring, platform migration, irreversible or outage-prone operations.

If approval is absent, stop before the high-risk action and report the PR state. 未獲個別確認不得執行。

## 7. Agent Compatibility / Agent 相容性

- Keep this `AGENTS.md` as the single shared project-instruction source.
- Claude Code **v2.1.277+** can read it directly when no applicable project/ancestor `CLAUDE.md` or `CLAUDE.local.md` takes precedence; verify with `claude --version` and `/memory` or `/config`.
- If older Claude Code or conflicting instructions prevent loading, a minimal `CLAUDE.md` containing `@AGENTS.md` may be used as a compatibility shim. Do not maintain two divergent policies.
- The actual installed Claude Code version and loaded instructions must be verified locally; neither is confirmed merely because this document exists.

## 8. Work Completion / 完成回報

Report changed files, branch, commits/PR links, checks actually performed, evidence, remaining risks, next actions, and whether deployment occurred.
回報實際結果；未 Commit、未 Push、未 Merge、未部署的工作，必須分開標示。

**Reference / 參考：** [Claude Code AGENTS.md](https://code.claude.com/docs/en/memory#agentsmd), [GitHub branch protections](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches).
