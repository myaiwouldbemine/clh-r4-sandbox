# myaiwouldbemine Copy Learning Hub — GitHub Pull Request 治理政策 / GitHub Pull Request Governance Policy

**版本 / Version:** 1.1
**狀態 / Status:** 提案中；於 PR 合併且 Repository 保護規則完成設定後生效 / Proposed — effective after PR merge and repository protection configuration
**適用範圍 / Scope:** 網站設定、課程規劃、學習內容、程式碼、工作流程與部署變更 / All website configuration, curricula, learning content, code, workflows, and deployment changes
**儲存庫 / Repository:** `myaiwouldbemine/myaiwouldbemine-Copy-Learning-Hub`

> **語言規則 / Language note:** 本文件以繁體中文與英文逐條對照。若翻譯存在歧義，應於 PR 中釐清並同步修訂兩種語言；不得默默只變更其中一種版本。
> This policy is maintained in Traditional Chinese and English side by side. Any ambiguity must be resolved in a PR, with both language versions updated together.

## 1. 目標 / Goals

**中文：** 為跨學科、Code-First、Evidence-Driven 的學習平台保留透明、可重現的變更歷史。內容正確性驗證與軟體／網站建置驗證必須分開；未取得證據，不得宣稱任一項已完成。

**English:** Preserve a transparent, reproducible change history for a multidisciplinary, Code-First and Evidence-Driven learning platform. Separate content verification from software/build verification; never mark either as complete without evidence.

## 2. 分支政策 / Branch Policy

- **中文：** `main` 是穩定、可發布的分支。日常修改不可直接 Push 至 `main`。

  **English:** `main` is the stable, publishable branch. Do not directly push ordinary changes to it.
- **中文：** 每項範圍一致的變更使用一個短期分支，命名如下。

  **English:** Create one short-lived branch per coherent change, using these names:

  | 分支 / Branch | 用途（中文） / Purpose (English) |
  |---|---|
  | `feat/CLH-NNN-description` | 新網站功能 / New site feature |
  | `fix/CLH-NNN-description` | 錯誤修復 / Bug fix |
  | `docs/CLH-NNN-description` | 課程或文件 / Lesson or documentation |
  | `ci/CLH-NNN-description` | 自動化 / Automation |
  | `chore/CLH-NNN-description` | 維護工作 / Maintenance |
  | `hotfix/CLH-NNN-description` | 緊急修復 / Urgent repair |

- **中文：** 使用可辨識的工作編號；現有 `feat/CLH-001-project-bootstrap` 分支仍有效。

  **English:** Use a descriptive work ID. The established `feat/CLH-001-project-bootstrap` branch remains valid.
- **中文：** 無關變更分開建立 PR，不可改寫 `main` 歷史。

  **English:** Keep unrelated changes in separate PRs. Do not rewrite `main` history.

## 3. Pull Request 生命週期 / Pull Request Lifecycle

1. **中文：** 與 `main` 同步，建立或繼續使用主題分支。
   **English:** Sync from `main` and create or continue a topic branch.
2. **中文：** 在本機修改，保留來源資料並尊重版權。
   **English:** Edit locally; preserve source files and copyrights.
3. **中文：** 執行適用的檢查並記錄真實結果，不得虛構測試紀錄。
   **English:** Run applicable checks and record actual results; do not fabricate test logs.
4. **中文：** 使用具體明確的 Commit 訊息提交變更，再 Push 主題分支。
   **English:** Commit changes with an informative message and push the topic branch.
5. **中文：** 使用 PR Template 建立以 `main` 為目標的 PR。
   **English:** Open a PR targeting `main` using the PR template.
6. **中文：** 等待 CI 並檢查 Files changed、變更範圍、連結、產生的檔案及敏感資訊。
   **English:** Wait for CI; inspect **Files changed**, scope, links, generated assets, and sensitive information.
7. **中文：** 解決審查討論與 CI 失敗項目。
   **English:** Resolve review discussions and CI failures.
8. **中文：** 符合所有適用條件後才合併，優先使用 **Squash and merge**。
   **English:** Merge only after all applicable requirements pass. Prefer **Squash and merge**.
9. **中文：** 合併後驗證部署，記錄上線網址與後續問題。
   **English:** Verify the deployment after merge; record the deployed URL and any follow-up issues.
10. **中文：** 不再需要時刪除已合併的主題分支；不可刪除 `main`。
    **English:** Delete the merged topic branch when no longer needed; never delete `main`.

## 4. PR 必備紀錄 / Mandatory PR Record

每個 PR 都必須說明以下項目。 / Every PR must describe:

| 項目 / Field | 中文要求 | English requirement |
|---|---|---|
| **Why** | 修改動機、Issue、學習目標 | Motivation, issue, learning goal |
| **What** | 修改的確切檔案及可觀察行為 | Exact files and observable behavior changed |
| **Scope / Out of scope** | 修改範圍及刻意排除的事項 | What was intentionally included and excluded |
| **Validation** | 指令、結果、環境及 CI 紀錄連結 | Commands, results, environment, and CI-run links |
| **Evidence** | 視需要提供 PDF 頁碼、已核對原始碼、測試輸出、截圖或審查筆記 | PDF page references, verified source paths, test outputs, screenshots, or review notes as appropriate |
| **Risk / Rollback** | 相容性、發布風險及安全還原方式 | Breaking changes, publishing risks, and safe revert approach |
| **Checklist** | 自我審查、來源、機密／授權及連結檢查 | Self-review, provenance, secret/license checks, and links |
| **Agent Roles / Review** | 實作者、審查者與審查結果；不得冒充正式 Approval | Implementer, reviewer, review findings; do not claim formal approval |
| **Merge Authorization** | 授權範圍、高風險確認與合併門檻 | Authorized scope, high-risk approval, and merge gates |

**中文：** 未執行的檢查不得標記 `PASS`；請標記 `NOT RUN` 或 `N/A` 並說明理由。

**English:** Do not claim `PASS` for a check not actually run. Mark it `NOT RUN` or `N/A` with a reason.

## 5. 合併門檻 / Merge Gates

### 5.1 軟體與網站變更 / Software and Site Changes

- **中文：** 已定義且可正常運作的相關自動化 CI 必須通過。

  **English:** Relevant automated CI checks pass, once defined and operational.
- **中文：** 網站或導覽變更須通過 `mkdocs build --strict`。

  **English:** `mkdocs build --strict` passes for website or navigation changes.
- **中文：** 新增連結與導覽應有效；受到變更影響的 Code、Mermaid、公式應正確呈現。

  **English:** New links and navigation entries resolve; code, Mermaid, and math examples render when affected.
- **中文：** 審查確認未洩漏機密、Token、私人資料，也未誤提交 `.venv/` 或 `site/` 產物。

  **English:** Review confirms no secrets, tokens, private data, or accidentally committed `.venv/` or `site/` artifacts.

### 5.2 學習教材變更 / Learning Material Changes

- **中文：** 頁碼、程式碼引用及概念必須依據實際來源。

  **English:** Page references, code citations, and concepts are grounded in the actual source.
- **中文：** 明確區分 **PDF SOURCE**、**VERIFIED SOURCE CODE**、**TEACHING EXAMPLE**、**EXTERNAL VERIFIED** 與 **UNVERIFIED**。

  **English:** Explicitly distinguish **PDF SOURCE**, **VERIFIED SOURCE CODE**, **TEACHING EXAMPLE**, **EXTERNAL VERIFIED**, and **UNVERIFIED**.
- **中文：** 適用時提供 `README.md`、`EVIDENCE.md`、`TERMINOLOGY.md` 或其他學習成果；避免沒有實質內容的空白樣板。

  **English:** Include `README.md`, `EVIDENCE.md`, `TERMINOLOGY.md` or other appropriate learning artifacts when applicable; avoid empty boilerplate.
- **中文：** 不得將教材已撰寫／發布等同於學習者已通過理解驗收。

  **English:** Do not confuse lesson written/published with learner knowledge check passed.
- **中文：** 公開發布前須確認講義 PDF、截圖、程式碼及第三方圖像的授權。

  **English:** Respect licensing of lecture PDFs, screenshots, code, and third-party figures before public publication.

### 5.3 核准與單人維護 / Approval and Solo Maintenance

- **中文：** 初期單人維護：必須經過 PR，但**不強制外部 Reviewer 核准**；作者或 Agent 應進行並記錄相應的自我審查。

  **English:** Initial solo-maintainer policy: PR required, but **no mandatory external approval**. The author or agent performs and records an appropriate self-review.
- **中文：** 未來加入協作者時，應視需求更新政策與 Repository 規則，要求適當審查。

  **English:** If collaborators are later introduced, update this policy and repository rules to require reviewers where appropriate.
- **中文：** 如無符合資格且實際可核准的 Reviewer，不應啟用強制 Code Owner Approval。

  **English:** Do not enable mandatory Code Owner approval unless a qualified reviewer can actually approve.

## 6. GitHub Repository 強制規則 / GitHub Repository Enforcement

第一次 CI Workflow 成功執行後，對 `main` 設定 Branch Protection 或 Ruleset。
After the first CI workflow runs successfully, configure `main` protection (Branch Protection or Ruleset):

1. **中文：** 合併前必須有 PR。 / **English:** Require a pull request before merging.
2. **中文：** 必須解決審查討論。 / **English:** Require conversation resolution.
3. **中文：** 只要求**實際出現過**的 CI Status Check 名稱；不可要求從未執行過的檢查。 / **English:** Require the **actual observed** CI status-check name; do **not** require a check that has never run.
4. **中文：** 禁止 Force Push 與刪除受保護分支。 / **English:** Block force pushes and branch deletion.
5. **中文：** 日常開發避免使用 Bypass 權限，但實際可用功能依 GitHub 方案與 Repository 權限為準。 / **English:** Avoid bypass allowances for normal development, subject to GitHub plan and repository-role capabilities.
6. **中文：** 在 Repository Merge Settings 優先使用 Squash and merge。 / **English:** Prefer Squash and merge in repository merge settings.
7. **中文：** 設定 GitHub Pages 僅由 `main` 的 GitHub Actions 部署。 / **English:** Configure GitHub Pages to deploy from GitHub Actions only on `main`.

**重要 / Important:** 只新增此 Markdown 檔**不會自動啟用** GitHub Branch Protection；必須另外設定並驗證 Repository Settings。
Merely adding this Markdown file does **not** activate GitHub branch protection. Repository Settings must be configured separately and verified.

## 7. CI / CD 分離 / CI / CD Separation

- **中文：** **PR Checks**：PR 指向 `main` 時執行；只進行 Build／Test，不部署公開網站。

  **English:** **PR checks**: run on pull requests targeting `main`; build/test only, never deploy public pages.
- **中文：** **Pages Deploy**：PR 合併後 Push 到 `main` 時執行，或經授權明確手動執行；不得任意發布 PR 程式碼。

  **English:** **Pages deploy**: run upon push to `main` following a merge, or explicit authorized manual invocation. Deployment must not publish arbitrary PR code.
- **中文：** Job／Check 名稱須唯一且穩定，適當固定 Action 版本並定期檢查依賴。

  **English:** Keep job/check names unique and stable. Pin action versions appropriately and periodically review dependencies.
- **中文：** 合併後若部署失敗，建立追蹤 Issue／PR，並記錄舊版網站是否仍可使用。

  **English:** If deploy fails after merge, open a follow-up issue/PR and record whether the previous site remains available.

## 8. Agent 協作與角色 / Agent Collaboration and Roles

- **中文：** Claude Code 與 Codex 為**對等 Agent**；兩者皆可執行程式實作、文件修改、測試、Code Review 與符合條件的 Merge，不預先固定實作者或審查者。

  **English:** Claude Code and Codex are **peer agents**. Either may implement code, edit documentation, test, review, or merge when authorized and eligible. Implementation and review roles are not permanently assigned.
- **中文：** 同一個 PR 優先由**不同 Agent** 實作與審查；簡單、低風險的學習文件修改可使用 Self-Review，並在 PR 中明確註記。

  **English:** Prefer **different agents** for implementation and review of the same PR. Self-review is acceptable for simple, low-risk lesson or documentation edits and must be explicitly recorded in the PR.
- **中文：** Agent Review 屬於輔助技術驗收，**不得冒充 GitHub 正式 Reviewer Approval**；只有 GitHub 實際記錄且符合保護規則的審查才可計入 Required Approvals。

  **English:** Agent reviews are supplementary technical evidence, **not GitHub reviewer approvals**. Only actual GitHub-recorded reviews satisfying repository rules count toward required approvals.
- **中文：** Agent 不得因其角色或審查意見而自行取得 GitHub 授權；任何寫入、合併與部署行為仍受帳號權限、Repository Rules 與使用者授權約束。

  **English:** Agent roles and review comments do not grant GitHub privileges. Write, merge, and deployment actions remain subject to account permissions, repository rules, and user authorization.
- **中文：** PR 紀錄應註明 Implementer、Reviewer（Agent 或 Human）、審查時間、主要發現及處理結果。

  **English:** The PR record should identify implementer, reviewer (agent or human), review time, significant findings, and resolution.

## 9. Agent Merge 授權與門檻 / Agent Merge Authorization and Gates

**中文：** Agent 只有在**以下條件全部符合**時才可執行 Merge；此為必要條件而非自動授權。

**English:** An agent may merge a PR **only when all conditions below hold**; these are prerequisites, not an implicit authorization.

1. **中文：** 使用者已**明確且事先授權**該類 PR 由 Agent Merge；授權範圍須可追溯，未授權即保留 PR。
   **English:** The user has **explicitly authorized in advance** agent merging for this PR class, with traceable scope; otherwise leave the PR open.
2. **中文：** 所有適用且已配置的 Required CI Checks 均通過；Pending、Failed、Cancelled 均不可當作 PASS。
   **English:** All applicable configured required CI checks have passed. Pending, failed, and cancelled checks are not passes.
3. **中文：** 沒有未解決的阻擋性審查意見；需符合 GitHub Required Review 與 Conversation Resolution 規則。
   **English:** No unresolved blocking review comments remain; GitHub review and conversation-resolution requirements are satisfied.
4. **中文：** 變更範圍與 Issue／PR 原定目標一致，沒有混入未經審查的額外修改。
   **English:** The change stays within the Issue/PR's intended scope with no unreviewed extra changes.
5. **中文：** 不涉及第 10 節的高風險操作，或已就**該次高風險操作取得個別確認**。
   **English:** No Section 10 high-risk action is involved, or specific approval for that action has been obtained.
6. **中文：** 合併前應重新確認 PR Head Commit、Checks 與 Review 的有效性，避免審查後又新增變更。
   **English:** Reconfirm the PR head commit, check results, and review validity immediately before merging to avoid unreviewed post-review changes.

**中文：** 任一條件不符合時，Agent 應**保留 PR、回報缺口與下一步**，不得繞過 Branch Protection、以管理員特權強行合併，或假稱獲得核准。

**English:** If any condition fails, the agent must **leave the PR open and report the blocker and next step**; it must not bypass protection, force an admin merge, or fabricate approval.

**中文：** `auto-merge` 是可選的 GitHub 功能，啟用時同樣需要授權，且不得取代上述合併門檻。

**English:** GitHub auto-merge is optional and likewise requires authorization; it does not supersede these merge gates.

## 10. 高風險操作與個別確認 / High-Risk Actions and Specific Approval

以下操作必須在執行前取得使用者**針對該次變更的個別確認**：

The following actions require **specific user confirmation for the particular change** before execution:

- **中文：** 大量刪除、搬移、覆寫學習資料、檔案或 Repository 歷史。

  **English:** Bulk deletion, relocation, or overwriting of learning data, files, or repository history.
- **中文：** 變更 Repository 權限、Branch Protection、Rulesets、Secrets、安全性或部署身分設定。

  **English:** Changes to repository permissions, branch protection, rulesets, secrets, security controls, or deployment identities.
- **中文：** 改寫重要教材來源、PDF 頁碼、原始碼證據、驗收紀錄或其來源鏈。

  **English:** Rewriting important learning sources, PDF page references, source-code evidence, validation records, or their provenance chain.
- **中文：** 大規模重構、架構遷移，或跨多學科的大範圍內容改動。

  **English:** Major refactors, architecture migrations, or broad cross-subject content changes.
- **中文：** 可能造成不可逆結果、網站長時間不可用、公開機密／未授權教材的操作。

  **English:** Potentially irreversible actions, extended outages, or exposure of secrets or unlicensed learning materials.

**中文：** 應於 PR 記錄風險、影響範圍、Rollback Plan 與明確核准；**一般類別 Merge 授權不等於高風險個別核准**。

**English:** Document risks, scope, rollback plan, and explicit approval in the PR. **General merge authorization is not specific high-risk approval**.

## 11. 例外變更與事件 / Exceptional Changes and Incidents

- **中文：** 緊急修復仍應儘可能走 `hotfix/` 分支與 PR。

  **English:** Urgent fixes still use a `hotfix/` branch and PR whenever feasible.
- **中文：** 若管理員於事件中繞過保護規則，必須記錄原因、執行者、時間、受影響 Commits、風險及後續修正 PR。這屬於例外事件，不是一般工作流程。

  **English:** If a repository administrator overrides protection during an incident, record reason, actor, time, affected commits, risks, and a follow-up corrective PR. This is an exceptional incident, not an ordinary workflow.
- **中文：** 若 Commit 洩漏 Secret，應先撤銷／輪替憑證並依事件程序處理；之後刪除檔案並不會消除 Git 歷史中的洩漏。

  **English:** If a secret appears in a commit, revoke/rotate it first and follow the appropriate incident process; deleting the file in a subsequent commit does not remove its historical exposure.

## 12. 政策變更 / Policy Changes

**中文：** 本政策生效後的修改原則上使用專用 PR，記錄理由及對現有分支規則的影響。政策文件變更與相應的 GitHub Settings 變更，必須分開追蹤並驗證。CLH-001 首次制定政策屬 Bootstrap 範圍，依第 13 節處理。

**English:** Once this policy is effective, subsequent changes should use a dedicated PR with rationale and impact on existing branch rules. Policy changes and corresponding GitHub Settings changes must be tracked separately and verified. The initial CLH-001 policy adoption is covered by Section 13.

## 13. CLH-001 Bootstrap 適用性 / CLH-001 Bootstrap Applicability

**中文：** 初始 `main` 基準 Commit `70e84f5` 早於本政策。Bootstrap 分支 `feat/CLH-001-project-bootstrap` 應加入此政策、`.github/PULL_REQUEST_TEMPLATE.md`、網站骨架及 CI 設定。請等 CI Check 第一次實際出現後，再將其設為 Required Status Check，以免意外阻擋第一個 PR。

**English:** Initial `main` baseline commit `70e84f5` predates this policy. The bootstrap feature branch `feat/CLH-001-project-bootstrap` should add this policy and `.github/PULL_REQUEST_TEMPLATE.md` together with site and CI scaffolding. Configure the required CI status check only after the check first appears, so the first PR is not unintentionally blocked.

## 參考資料 / References

- [GitHub: Managing a branch protection rule](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/managing-a-branch-protection-rule)
- [GitHub: Creating a pull request template](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/creating-a-pull-request-template-for-your-repository)
- [GitHub: Managing rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets)
