> **ARCHIVED / NOT ACTIVE.** Superseded by Minimal Governance. C3–C5 and later platform implementation are stopped. The original proposal/evidence below is preserved, not current policy or authorization. Prototype code/tests formerly under scripts/ are retained under archive/governance-platform/scripts/.

**繁體中文**

> **已封存／非現行有效。** 已被 Minimal Governance 取代。C3–C5 及之後的平台實作已停止。以下原始提案／證據僅為保存，不是現行政策或授權。原先位於 scripts/ 下的原型程式碼／測試保留於 archive/governance-platform/scripts/。

# Issue #4 — Canary Authorization Package v1
Date: 2026-11-05 Asia/Taipei. Proposal only; no item below is authorized by this document.
Issue: https://github.com/myaiwouldbemine/myaiwouldbemine-Copy-Learning-Hub/issues/4
Draft PR: https://github.com/myaiwouldbemine/myaiwouldbemine-Copy-Learning-Hub/pull/5

**繁體中文**

Issue #4 — Canary Authorization Package v1（Canary 授權套件 v1）

日期：2026-11-05 Asia/Taipei。僅為提案；以下任何項目皆未因本文件而獲得授權。

Issue：見上方英文連結。

Draft PR：見上方英文連結。

Decision: READY FOR AUTHORIZATION of first resource-only batch; trusted runtime remains BLOCKED. Keep native APPROVED plus authenticated context attestation. Ordinary Codex Summary/Receipt cannot PASS. No merge executor, deployment, production settings change or automatic merge is included in any batch.

**繁體中文**

決定：首批僅限資源的項目已 READY FOR AUTHORIZATION（可供授權）；可信的執行期仍為 BLOCKED。維持原生 APPROVED 加上經驗證的 context attestation。一般的 Codex Summary／Receipt 不能 PASS。任何批次皆不包含 merge executor、部署、正式環境設定變更或自動合併。

## Evidence and resource reuse
VERIFIED: PR #5 Draft at discovery head ddf064c5da4648bee22d21bbc80d19074a5ac33c, auto_merge=null. PR #7's prior real Canary authenticated comment actor 199175422 and App 1144995, but no native review; it is not isolated identity proof. Earlier 55 offline tests passed; no new integration tests run for this package.
VERIFIED now: gh can read private myaiwouldbemine/governed-env, main, not archived. GET /repos/myaiwouldbemine/governed-env/rules/branches/main returns 403 'Upgrade to GitHub Pro or make this repository public to enable this feature.' No contents or secrets inspected. Existing protection sufficiency and model custody UNKNOWN. Do not change its visibility or reuse it without a separate assessment.
Connector current installation inventory confirms target learning Repo access; it does not establish App custody.
Existing learning Repo / PR #7: reuse as historical evidence only, not new privileged sandbox. Existing .venv/site and user work remain separate.

**繁體中文**

VERIFIED（已驗證）：PR #5 為 Draft，探索時的 head 為 ddf064c5da4648bee22d21bbc80d19074a5ac33c，auto_merge=null。PR #7 先前的真實 Canary 經驗證留言的 actor 為 199175422、App 為 1144995，但沒有原生 review；它不是隔離身分的證明。先前 55 項離線測試通過；本套件未執行新的整合測試。

VERIFIED（現在）：gh 可讀取私有的 myaiwouldbemine/governed-env，main 分支，未封存。GET /repos/myaiwouldbemine/governed-env/rules/branches/main 回傳 403「Upgrade to GitHub Pro or make this repository public to enable this feature.」。未檢視任何內容或 secrets。既有保護是否足夠及模型保管狀況 UNKNOWN（未知）。未經另行評估，不得變更其可見性或重用它。

Connector 目前的安裝清單確認可存取目標學習 Repo；這並未確立 App 的保管。

既有的學習 Repo／PR #7：僅作為歷史證據重用，不作為新的特權 sandbox。既有的 .venv/site 與使用者工作維持獨立。

Preferred minimum new resources (names proposed; availability NOT CHECKED):
- PUBLIC myaiwouldbemine/clh-review-sandbox: synthetic text/code only; private data prohibited; no secrets, no Pages, no deployment workflows. Apps installed only here.
- PUBLIC myaiwouldbemine/clh-review-control-canary: generic reviewed control code, public keys and synthetic metadata only. Neither Agent App installed here. No agent write/admin permissions; secrets only in protected environments after later approval.
Public visibility avoids requiring a paid private-repository protection upgrade. Human must explicitly approve public visibility. If private is mandatory, STOP and reprice/verify plan capabilities before provisioning. No automatic fallback, upgrade or existing Repo visibility conversion.

**繁體中文**

偏好的最少新資源（名稱為提議；可用性 NOT CHECKED（未檢查））：

- PUBLIC（公開）myaiwouldbemine/clh-review-sandbox：僅限合成的文字／程式碼；禁止私人資料；無 secrets、無 Pages、無部署 workflow。App 僅安裝於此。
- PUBLIC（公開）myaiwouldbemine/clh-review-control-canary：僅含通用的已審查 control 程式碼、公鑰與合成中繼資料。此處不安裝任何 Agent App。Agent 無 write／admin 權限；secrets 僅在之後獲核准時放入受保護的 environment。

公開可見性可避免需要付費升級私有 repository 的保護功能。Human 必須明確核准公開可見性。若必須為私有，則 STOP（停止），並在佈建前重新估價／驗證方案功能。不自動退而求其次、不自動升級、不轉換既有 Repo 的可見性。

GitHub docs distinguish availability of private environment secrets and required environment reviewers; private required-reviewer support cannot be assumed:
https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/manage-environments
https://docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments

**繁體中文**

GitHub 文件區分私有 environment secrets 的可用性與必要 environment reviewer；不能假設私有 repository 支援必要 reviewer：

文件連結見上方英文區塊（連結目標不變）。

## Architecture and identities
Control is a fixed reviewed Actions release (full commit SHA) with trusted Registry/Policy/Publisher. It orchestrates separately isolated Codex and Claude execution and a read-only collector. Manual Human workflow_dispatch only; no issue_comment/pull_request_target/workflow_run triggers, cron or candidate-controlled reusable workflow. Inputs are validated repo ID/PR number plus an allowlisted test ID, not scripts, ref names or arbitrary URLs.
Two fixed private App registrations (names proposed; availability UNKNOWN): CLH Canary Codex and CLH Canary Claude. Custom Apps identify our controlled integration, not official vendor certification. Model identity is established by pinned backend/adapter, non-secret model/run metadata and protected execution provenance, not App name.
Roles are assigned per run: Codex Builder -> Claude Reviewer, then reverse. Separate custody applies to both; a shared Human owner is an administrative root, not runtime independence. No Human OAuth token in either Agent environment.

**繁體中文**

Control 是固定且已審查的 Actions 版本（完整 commit SHA），搭配可信的 Registry／Policy／Publisher。它協調分別隔離的 Codex 與 Claude 執行，以及唯讀 collector。僅允許 Human 手動 workflow_dispatch；不使用 issue_comment／pull_request_target／workflow_run 觸發、cron，或由候選程式碼控制的 reusable workflow。輸入為經驗證的 repo ID／PR 編號，加上允許清單中的測試 ID，而非腳本、ref 名稱或任意 URL。

兩個固定的私有 App 註冊（名稱為提議；可用性 UNKNOWN）：CLH Canary Codex 與 CLH Canary Claude。自訂 App 識別的是我們控制的整合，並非廠商官方認證。模型身分由固定的 backend／adapter、非機密的模型／run 中繼資料，以及受保護的執行出處確立，而不是由 App 名稱確立。

角色每次 run 指派一次：Codex Builder -> Claude Reviewer，然後反向。兩者皆採用獨立保管；共用的 Human 擁有者是管理上的根，不是執行期的獨立性。任何 Agent 環境中都不得有 Human OAuth token。

Stages:
1. Control snapshots repo numeric ID/name, PR, head/base and scope v1 using existing collector manifest. Reject incomplete files/API caps. It selects a pinned trusted review rubric; candidate AGENTS.md/prompts are untrusted data, never policy.
2. Builder runs without Reviewer keys. Trusted Builder publisher records execution-bound provenance for the resulting commit; commit author alone is insufficient.
3. Reviewer reads exact immutable snapshot, using only its model credential in a constrained execution environment, no App or signing keys. It never auto-runs candidate scripts, dependencies, hooks or actions.
4. If code execution is needed, separate fresh no-secret job, no credential persistence, no writable cache/shared runner/workspace. Its output is untrusted evidence, not approval. Transport smoke tests need no candidate execution.
5. Trusted publisher job uses only fixed control code. It parses bounded structured model result, requires explicit rubric completion and context match, checks native blockers and re-snapshots. It mints only a sandbox PR-write token, submits APPROVED with explicit commit_id, then reads back native Review ID/actor/state/commit.
6. Signer creates existing schema-v1 attestation including real review ID and head/base/scope; Builder provenance uses its separate purpose. Existing Ed25519 envelopes remain required, max 300 seconds, fresh trusted clock and revocation checks. No fabricated review_id. Publish only bounded non-secret signed evidence.
7. Read-only collector independently verifies native current state, signature/enrollment, Builder identity and all blockers. Result is review-component only, not merge eligibility. No check publication or merge call.

**繁體中文**

階段：

1. Control 以既有 collector 清單擷取 repo 數字 ID／名稱、PR、head／base 與 scope v1 的快照。拒絕不完整的檔案／API 上限。它選用固定且可信的審查準則；候選的 AGENTS.md／prompt 屬不可信資料，絕不是政策。
2. Builder 在沒有 Reviewer 金鑰的情況下執行。可信的 Builder publisher 為產生的 commit 記錄綁定執行的出處；僅有 commit 作者並不足夠。
3. Reviewer 讀取精確的不可變快照，在受限的執行環境中僅使用其模型憑證，不持有 App 或簽署金鑰。它絕不自動執行候選的腳本、相依套件、hook 或 action。
4. 若需要執行程式碼，使用另行啟動的全新、無 secrets 的 job，不保留憑證，無可寫入的快取／共用 runner／工作區。其輸出是不可信的證據，不是核准。傳輸 smoke test 不需要執行候選程式碼。
5. 可信的 publisher job 僅使用固定的 control 程式碼。它解析有界的結構化模型結果，要求明確完成準則且 context 相符，檢查原生阻擋項目並重新擷取快照。它僅鑄造 sandbox 的 PR-write token，以明確的 commit_id 提交 APPROVED，然後讀回原生 Review ID／actor／state／commit。
6. Signer 建立既有的 schema-v1 attestation，包含真實的 review ID 與 head／base／範圍；Builder 出處使用其獨立的 purpose。既有的 Ed25519 封套仍為必要，最長 300 秒，需要最新的可信時鐘與撤銷檢查。不得捏造 review_id。僅發布有界、非機密、已簽署的證據。
7. 唯讀 collector 獨立驗證原生目前狀態、簽章／登記、Builder 身分與所有阻擋項目。結果僅屬 review 元件，不是合併資格。不發布 check，也不呼叫合併。

A full run cannot be attested from PR-uploaded result files. Publisher accepts results only from an allowlisted control workflow commit/job/run/attempt for its own pre-recorded context. It verifies origin and schema; it does not execute artifacts or interpolate model text into shell. Model output remains a claim about review quality, not an infallible guarantee. Transport-fixture APPROVED must be tagged simulation and never pass full semantic-review eligibility.

**繁體中文**

完整的 run 不能由 PR 上傳的結果檔案來證明。Publisher 僅接受來自允許清單中的 control workflow commit／job／run／attempt、且屬於其預先記錄 context 的結果。它驗證來源與 schema；不執行 artifact，也不將模型文字插入 shell。模型輸出仍只是對審查品質的聲明，不是萬無一失的保證。傳輸 fixture 的 APPROVED 必須標記為 simulation（模擬），且絕不得通過完整的語義審查資格。

## Permission matrix
| Principal | Sandbox permissions | Control access | Restrictions |
|---|---|---|---|
| CLH Canary Codex App registration | Metadata read, Contents write, Pull requests write | None | Selected sandbox only; same registration supports role reversal |
| CLH Canary Claude App registration | Metadata read, Contents write, Pull requests write | None | Same; distinct App ID, actor, private key |
| Builder job token | Contents read; write only in separate Builder publisher; PR write only if creating test PR | None | Repo allowlist; cannot edit workflows/control |
| Reviewer model job | Public snapshot only; no write token | None | Model credential scoped/budgeted separately |
| Reviewer Publisher installation token | Pull requests write; Contents read only if needed | None | Downscope per mint; short-lived; revoke after job |
| Collector token | Pull requests read, Contents read; Issues read only for ordinary-comment collection | Control GITHUB_TOKEN contents read | No signing or publication keys |
| Control GITHUB_TOKEN | No sandbox access inherently | contents read; other permissions omitted | persist-credentials=false |

**繁體中文**

| 主體 | Sandbox 權限 | Control 存取 | 限制 |
|---|---|---|---|
| CLH Canary Codex App 註冊 | Metadata read、Contents write、Pull requests write | 無 | 僅限選定的 sandbox；同一註冊支援角色對調 |
| CLH Canary Claude App 註冊 | Metadata read、Contents write、Pull requests write | 無 | 同上；App ID、actor、私鑰皆不同 |
| Builder job token | Contents read；僅在獨立的 Builder publisher 中可 write；僅在建立測試 PR 時才有 PR write | 無 | Repo 允許清單；不得編輯 workflow／control |
| Reviewer 模型 job | 僅公開快照；無 write token | 無 | 模型憑證分別限定範圍／預算 |
| Reviewer Publisher installation token | Pull requests write；僅在需要時才有 Contents read | 無 | 每次鑄造時降權；短效；job 結束後撤銷 |
| Collector token | Pull requests read、Contents read；僅在收集一般留言時才有 Issues read | Control GITHUB_TOKEN contents read | 無簽署或發布金鑰 |
| Control GITHUB_TOKEN | 本身無 sandbox 存取 | contents read；其他權限省略 | persist-credentials=false |

No actions/workflows/administration/secrets/checks/statuses/deployments/Pages permissions requested for Agent Apps. PR write is broader than submit-review: a compromised token could alter PR metadata or attempt other PR operations. API allowlists are defense in depth, not GitHub fine-grained enforcement. Sandbox is disposable; publisher code and key custody are trusted boundary.
Native App Review support:
https://docs.github.com/en/rest/pulls/reviews
App tokens in Actions:
https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/making-authenticated-api-requests-with-a-github-app-in-a-github-actions-workflow

**繁體中文**

不向 Agent App 要求 actions／workflows／administration／secrets／checks／statuses／deployments／Pages 權限。PR write 比提交 review 更廣泛：被入侵的 token 可能變更 PR 中繼資料或嘗試其他 PR 操作。API 允許清單屬縱深防禦，不是 GitHub 細粒度權限的強制執行。Sandbox 是可拋棄的；publisher 程式碼與金鑰保管是信任邊界。

原生 App Review 支援：

文件連結見上方英文區塊（連結目標不變）。

Actions 中的 App token：

文件連結見上方英文區塊（連結目標不變）。

## Credential custody and isolation acceptance
Proposed accountable root custodian: Human owner myaiwouldbemine; actual named human confirmation REQUIRED. Two logical custodians below must be explicitly assigned and cannot be Builder-controlled processes:
- Codex custodian: Human-administered environment codex-publisher; Codex App key + Codex provenance/review Ed25519 key; separate codex-model environment for model access.
- Claude custodian: Human-administered environment claude-publisher; Claude App key + Claude Ed25519 key; separate claude-model environment.
- Control administrator: Human only; Registry/public keys/revocation/policy release acceptance. Neither Agent can administer control, dispatch arbitrary refs or bypass protections.

**繁體中文**

建議的最終負責保管者：Human 擁有者 myaiwouldbemine；必須有實際具名的人員確認。下列兩個邏輯保管者須明確指派，且不得是 Builder 控制的程序：

- Codex 保管者：由 Human 管理的 environment codex-publisher；Codex App 金鑰 + Codex 出處／review 的 Ed25519 金鑰；另設 codex-model environment 供模型存取。
- Claude 保管者：由 Human 管理的 environment claude-publisher；Claude App 金鑰 + Claude 的 Ed25519 金鑰；另設 claude-model environment。
- Control 管理者：僅限 Human；Registry／公鑰／撤銷／政策版本接受。兩個 Agent 都不能管理 control、dispatch 任意 ref 或 bypass 保護。

Same administrator is an acknowledged common root. Environments alone do not prove separate trust principals. Distinct jobs, workload identities, backend credentials and secret access policies must be verified; if unacceptable under independence policy, distinct named administrators/accounts are required before running.
Present local gh Human OAuth is powerful. It must not be copied/mounted into Agent runners. No user-home mount, gh hosts.yml, SSH agent, inherited cloud credentials or persistent developer runner. Separate ephemeral GitHub-hosted jobs; no shared self-hosted runner. This package cannot claim Builder isolation until denial tests pass.
Control code allows no Agent App installation, no Agent repository collaborator access and no public fork PR workflow execution. Only reviewed main release may access environments. Environment required Human approval, prevent-self-review and no admin bypass where supported; required approver must be distinct from dispatcher. Second approver availability UNKNOWN; if unavailable use an explicitly accepted alternate custody mechanism in a revised package, do not silently weaken.
Protected main: no force/delete, PR-only, at least one independent Human reviewer, dismiss stale approvals, resolve threads, protect workflow/policy/registry paths, deny Agent bypass. A real second maintainer and account feature support must be confirmed. A bot cannot supply its own control approval.
GitHub environment protection does not prevent a root administrator from changing policy; that root remains trusted. Builder cannot have that administrator credential.
Security guidance:
https://docs.github.com/en/actions/reference/security/secure-use

**繁體中文**

相同的管理者是已承認的共同根。僅有 environment 並不能證明是獨立的信任主體。必須驗證不同的 job、workload 身分、後端憑證與 secret 存取政策；若依獨立性政策無法接受，則在執行前需要不同具名的管理者／帳號。

目前本機的 gh Human OAuth 權限很大。不得複製／掛載到 Agent runner。不得有使用者家目錄掛載、gh hosts.yml、SSH agent、繼承的雲端憑證或持續存在的開發者 runner。使用分開的臨時性 GitHub 託管 job；不使用共用的自架 runner。在拒絕測試通過之前，本套件不能宣稱 Builder 已隔離。

Control 程式碼不允許安裝任何 Agent App、不允許 Agent repository 協作者存取，也不允許公開 fork PR 執行 workflow。只有已審查的 main 版本才能存取 environment。在支援之處，environment 須要求 Human 核准、prevent-self-review 且無 admin bypass；必要核准者必須與 dispatch 者不同。第二位核准者是否可用 UNKNOWN；若不可用，須在修訂的套件中使用明確接受的替代保管機制，不得悄悄放寬。

受保護的 main：不得 force／刪除、僅允許 PR、至少一位獨立 Human reviewer、撤銷過期核准、解決討論串、保護 workflow／政策／registry 路徑，並拒絕 Agent bypass。必須確認真有第二位維護者及帳號功能支援。Bot 不能為自己提供 control 核准。

GitHub environment 保護無法阻止 root 管理者變更政策；該 root 仍屬受信任。Builder 不得持有該管理者的憑證。

安全指引：

文件連結見上方英文區塊（連結目標不變）。

## App/key lifecycle (requires later itemized approval)
Register each App under Human ownership, no webhook initially, no user OAuth flow, request exact permissions above. Install each using selected-repository scope ONLY sandbox. Do not install on learning Repo/control or all repositories.
Create one App private key per App and one Ed25519 attestation key per Agent (four independent private keys total); generate only in authorized custody tooling, never chat/repository files. Record only public fingerprints/key IDs. Key values must never be logged/uploaded as artifacts.
Verify App JWT GET /app ID/slug; verify installation App association/repository/token downscope; submit controlled smoke Review and pin numeric Bot actor from authenticated response. Enrollment binds backend adapter, App, installation, actor, custody owner, signing public key, key ID, revocation/version. Human accepts exact enrollment before full gate runs. Installation ID is not App ID.
Rotate: enroll new public key with explicit validity, test, then revoke old; any unknown revocation state blocks. Do not reuse GitHub App RSA private key for Ed25519 signing.
Revoke: stop all workflows, cancel active jobs, revoke minted tokens, delete/revoke compromised App private key, disable installation/remove sandbox grant if approved for incident response, revoke signing key in external registry, invalidate outstanding evidence. Token revocation alone is insufficient if root key survives.

**繁體中文**

每個 App 在 Human 擁有下註冊，起初不設 webhook、無使用者 OAuth 流程，並要求上述精確權限。每個以選定 repository 範圍安裝，且僅限 sandbox。不得安裝到學習 Repo／control 或所有 repository。

每個 App 建立一把 App 私鑰，每個 Agent 建立一把 Ed25519 attestation 金鑰（共四把獨立私鑰）；僅在獲授權的保管工具中產生，絕不放在聊天或 repository 檔案中。僅記錄公開指紋／金鑰 ID。金鑰值絕不得被記錄或上傳為 artifact。

驗證 App JWT GET /app 的 ID／slug；驗證 installation 與 App 的關聯／repository／token 降權；提交受控的 smoke Review，並從經驗證的回應固定數字 Bot actor。登記綁定 backend adapter、App、installation、actor、保管擁有者、簽署公鑰、金鑰 ID、撤銷／版本。完整閘門執行前，Human 接受確切的登記。Installation ID 不是 App ID。

輪替：以明確有效期登記新公鑰、測試，然後撤銷舊金鑰；任何未知的撤銷狀態皆阻擋。不得將 GitHub App 的 RSA 私鑰重用於 Ed25519 簽署。

撤銷：停止所有 workflow、取消進行中的 job、撤銷已鑄造的 token、刪除／撤銷被入侵的 App 私鑰，若獲核准則為事件應變停用 installation／移除 sandbox 授權，在外部 registry 撤銷簽署金鑰，並使未決證據失效。若 root 金鑰仍存在，僅撤銷 token 並不足夠。

（本節需於之後逐項核准。）

## Individually approvable L3 checklist
All PENDING / NOT AUTHORIZED. Each ID authorizes only that row, not subsequent dependencies. Exact later manifests/releases and named approvers must be supplied before their batch is executed.
| ID | Exact proposed operation | Dependency |
|---|---|---|
| R1 | Create PUBLIC myaiwouldbemine/clh-review-sandbox, synthetic-only; no secrets | Confirm name/public disclosure |
| R2 | Create PUBLIC myaiwouldbemine/clh-review-control-canary, synthetic-only; no secrets | Same |
| C1 | Disable Actions execution in sandbox during setup; keep Pages/auto-merge disabled | R1 |
| C2 | Keep Control Actions disabled during bootstrap | R2 |
| C3 | Assign named Human-only Control admin and distinct approver; remove any Agent write/admin grant if present | Named people/permission diff |
| C4 | Configure Control main PR/review/force/delete/path protections and no Agent bypass | Capability check and exact rules diff |
| C5 | Create four protected environments, main-only, required approver, prevent-self-review, no bypass | Exact settings; real second human |
| A1 | Register private CLH Canary Codex with matrix permissions, no webhook | Name/owner accepted |
| A2 | Register private CLH Canary Claude with matrix permissions, no webhook | Same |
| I1 | Install Codex App on sandbox only | A1, R1 |
| I2 | Install Claude App on sandbox only | A2, R1 |
| K1 | Generate/store Codex App private key in codex-publisher only | C5, named custodian |
| K2 | Generate/store Claude App private key in claude-publisher only | C5, named custodian |
| K3 | Generate/store Codex Ed25519 key; enroll public key | Codex custodian accepted |
| K4 | Generate/store Claude Ed25519 key; enroll public key | Claude custodian accepted |
| M1 | Add/use Codex model credential in codex-model, exact backend/scope/budget | Hard budget verified |
| M2 | Add/use Claude model credential in claude-model, exact backend/scope/budget | Same |
| W1 | Bootstrap Human-reviewed fixed Control release, Actions allowlist, full-SHA pins, manual trigger only | Reviewed artifact and C3-C5 |
| W2 | Enable Control Actions for that exact release; run at most four authorized runs | Budget and all isolation prerequisites |
| E1 | Accept actual App/actor/installation/key/custody enrollment after smoke test | Human acceptance of API evidence |
| T1 | Create synthetic sandbox branches/Draft PRs and submit/dismiss test reviews, modify synthetic head/base, resolve test threads | Exact fixtures/test script; sandbox only |
| T2 | Test key revocation/denied access and rollback | Specific key IDs; no production keys |
| B1 | Configure maximum Actions paid-spend blocking and model hard budgets | Exact scope, prevent impact on unrelated work |

**繁體中文**

全部為 PENDING／NOT AUTHORIZED（待定／未授權）。每個 ID 只授權該列，不含後續相依項。執行其批次前，必須提供確切之後的 manifest／版本及具名核准者。

| ID | 精確的提議操作 | 相依 |
|---|---|---|
| R1 | 建立 PUBLIC myaiwouldbemine/clh-review-sandbox，僅限合成；無 secrets | 確認名稱／公開揭露 |
| R2 | 建立 PUBLIC myaiwouldbemine/clh-review-control-canary，僅限合成；無 secrets | 同上 |
| C1 | 設定期間停用 sandbox 的 Actions 執行；保持 Pages／auto-merge 停用 | R1 |
| C2 | 引導期間保持 Control Actions 停用 | R2 |
| C3 | 指派具名且僅限 Human 的 Control 管理者與不同的核准者；若有任何 Agent write／admin 授權則移除 | 具名人員／權限差異 |
| C4 | 設定 Control main 的 PR／review／force／刪除／路徑保護，且無 Agent bypass | 功能檢查與確切的規則差異 |
| C5 | 建立四個受保護 environment，僅限 main、必要核准者、prevent-self-review、無 bypass | 確切設定；真正的第二位 Human |
| A1 | 以矩陣權限註冊私有 CLH Canary Codex，無 webhook | 名稱／擁有者已接受 |
| A2 | 以矩陣權限註冊私有 CLH Canary Claude，無 webhook | 同上 |
| I1 | 僅在 sandbox 安裝 Codex App | A1、R1 |
| I2 | 僅在 sandbox 安裝 Claude App | A2、R1 |
| K1 | 僅在 codex-publisher 中產生／儲存 Codex App 私鑰 | C5、具名保管者 |
| K2 | 僅在 claude-publisher 中產生／儲存 Claude App 私鑰 | C5、具名保管者 |
| K3 | 產生／儲存 Codex Ed25519 金鑰；登記公鑰 | Codex 保管者已接受 |
| K4 | 產生／儲存 Claude Ed25519 金鑰；登記公鑰 | Claude 保管者已接受 |
| M1 | 在 codex-model 中新增／使用 Codex 模型憑證，確切 backend／範圍／預算 | 已驗證硬性預算 |
| M2 | 在 claude-model 中新增／使用 Claude 模型憑證，確切 backend／範圍／預算 | 同上 |
| W1 | 引導由 Human 審查的固定 Control 版本、Actions 允許清單、完整 SHA 固定、僅手動觸發 | 已審查的 artifact 與 C3-C5 |
| W2 | 為該確切版本啟用 Control Actions；最多執行四次已授權的 run | 預算與所有隔離前提 |
| E1 | smoke test 後接受實際的 App／actor／installation／金鑰／保管登記 | Human 接受 API 證據 |
| T1 | 建立合成 sandbox 分支／Draft PR，並提交／dismiss 測試 review、修改合成 head／base、解決測試討論串 | 確切的 fixture／測試腳本；僅限 sandbox |
| T2 | 測試金鑰撤銷／拒絕存取與回復 | 特定金鑰 ID；不用正式金鑰 |
| B1 | 設定 Actions 付費支出上限的阻擋與模型硬性預算 | 確切範圍，避免影響無關工作 |

No production Rule/Secrets/Branch Protection changes are requested. A sandbox native enforcement Ruleset, if later needed, requires a separate exact rule diff; API review-component tests do not prove merge enforcement.

**繁體中文**

不要求任何正式環境的 Rule／Secrets／Branch Protection 變更。若之後需要 sandbox 的原生強制執行 Ruleset，需另行提出確切的規則差異；API review 元件測試無法證明合併強制執行。

## Cost and run limits
First batch R1/R2/C1/C2: USD 0 incremental paid spend; no plan upgrade, model calls or enabled privileged workflow.
Later trial proposed ceiling: USD 5 total incremental model cost, combined Codex+Claude; USD 0 paid Actions/runner/artifact spend. Max four manually authorized runs, one at a time, 10 minutes each (40 runner-minutes total); no automatic retry. Standard hosted Linux only; no larger runners; artifacts <=10 MB/run, retention 1 day.
These are requested limits, NOT configured controls. Enable model runs only if provider-side enforceable remaining spend caps (including concurrent charges) fit the shared USD 5 ceiling. Token limits alone are not a hard monetary cap. If no enforceable provider cap exists, paid model runs BLOCK; transport-only fixtures must stay marked simulation.
Verify available included Actions/storage allowance and effective stop-spend policy before execution. Account-wide budget changes that affect unrelated work need separate B1 approval; no plan upgrade/credit purchase.
Control checks run count, elapsed time and remaining budget before dispatch; timeout/error stops issuance. Unexpected charge or uncertain usage => cancel remaining runs and BLOCK.

**繁體中文**

第一批 R1/R2/C1/C2：增量付費支出 USD 0；不升級方案、不呼叫模型、不啟用特權 workflow。

之後試驗的提議上限：增量模型成本合計 USD 5（Codex+Claude 合計）；付費 Actions／runner／artifact 支出 USD 0。最多四次手動授權的 run，一次一個，每次 10 分鐘（合計 40 runner 分鐘）；不自動重試。僅限標準託管 Linux；不使用較大的 runner；artifact 每次 run <=10 MB，保留 1 天。

這些是所要求的限制，NOT configured controls（並非已設定的控制）。僅在供應商端有可強制執行的剩餘支出上限（含並行費用）且符合共用的 USD 5 上限時，才啟用模型 run。僅限制 token 並非硬性的金額上限。若不存在可強制執行的供應商上限，付費模型 run 即 BLOCK；僅傳輸的 fixture 必須維持標示為 simulation。

執行前，驗證可用的 Actions／儲存內含額度及有效的停止支出政策。影響無關工作的帳號層級預算變更需另行 B1 核准；不升級方案、不購買額度。

Control 於 dispatch 前檢查 run 次數、經過時間與剩餘預算；逾時／錯誤即停止簽發。非預期的費用或用量不確定 => 取消剩餘 run 並 BLOCK。

## Canary matrix — all NOT RUN
| Case | Expected result / required evidence |
|---|---|
| App transport smoke both Apps | Native Review read-back ID/actor/type/state/head; authenticated token enrollment; fixture only, NOT independent semantic PASS |
| Codex Builder / Claude Reviewer | Full fresh context/signature/provenance/native APPROVED; review-only PASS |
| Claude Builder / Codex Reviewer | Same in reverse |
| Same agent/App/actor/custody, shared Human token | BLOCK |
| Human comment with matching App provenance, fake Receipt/Review ID | BLOCK |
| Wrong signature/key/Repo/PR; replay | BLOCK |
| New head/base/scope | Old approval evidence BLOCK; fresh review required |
| Dismissed/changes-requested/superseded review | BLOCK |
| Unresolved/outdated thread or unresolved trusted blocker | BLOCK; ordinary ambiguous blocker => manual resolution, no inferred PASS |
| Missing/partial/denied API, page/cap mismatch | BLOCK |
| Unknown/revoked/expired/future evidence; expiry during API collection | BLOCK |
| Candidate AGENTS/workflow/registry edits; shell/path/artifact injection | Cannot modify trusted policy or issue credentials; BLOCK suspicious result |
| Builder attempts Control write/env access/Reviewer key access | Access denied; no secrets printed; safe canary markers only |
| Reviewer attempts Builder key access | Denied |
| Model output malformed/incomplete or error | No APPROVED issued; BLOCK |
| Race between review/context collections | BLOCK observed changes; no atomic merge guarantee claimed |
| L0 / L1-L3 missing review | L0 review NOT_REQUIRED only; L1-L3 BLOCK |
| Draft / other gates even with valid review | Remain unmergeable by policy; no merge attempted |
| Budget exhausted / rollback | No further tokens/signatures/runs; old evidence revoked |

**繁體中文**

| 案例 | 預期結果／必要證據 |
|---|---|
| 兩個 App 的傳輸 smoke | 讀回原生 Review 的 ID／actor／類型／state／head；經驗證的 token 登記；僅 fixture，NOT 獨立語義 PASS |
| Codex Builder / Claude Reviewer | 完整的全新 context／簽章／出處／原生 APPROVED；僅 review PASS |
| Claude Builder / Codex Reviewer | 反向相同 |
| 相同 agent／App／actor／保管、共用 Human token | BLOCK |
| 具相符 App 出處的 Human 留言、偽造 Receipt／Review ID | BLOCK |
| 錯誤的簽章／金鑰／Repo／PR；重放 | BLOCK |
| 新的 head／base／範圍 | 舊核准證據 BLOCK；需要新的 review |
| 已 dismiss／changes-requested／被取代的 review | BLOCK |
| 未解決／已過時的討論串或未解決的可信阻擋項目 | BLOCK；一般含糊的阻擋項目 => 手動解決，不推論 PASS |
| 缺失／不完整／被拒絕的 API、分頁／上限不符 | BLOCK |
| 未知／已撤銷／已過期／未來的證據；API 收集期間過期 | BLOCK |
| 候選的 AGENTS／workflow／registry 編輯；shell／路徑／artifact 注入 | 不能修改可信政策或簽發憑證；對可疑結果 BLOCK |
| Builder 嘗試 Control write／env 存取／Reviewer 金鑰存取 | 存取被拒；不印出 secrets；僅安全的 canary 標記 |
| Reviewer 嘗試 Builder 金鑰存取 | 被拒絕 |
| 模型輸出格式錯誤／不完整或錯誤 | 不簽發 APPROVED；BLOCK |
| review／context 收集之間的競態 | 對觀察到的變更 BLOCK；不宣稱原子性合併保證 |
| L0 / L1-L3 缺少 review | L0 僅 review NOT_REQUIRED；L1-L3 BLOCK |
| Draft／其他閘門，即使有有效 review | 依政策仍不可合併；不嘗試合併 |
| 預算用盡／回復 | 不再有 token／簽章／run；舊證據撤銷 |

Record synthetic vs real results separately, exact repo ID/PR/head/base/scope/review/App/actor/run/key IDs, expected/actual, timestamps and URLs; never secret values. No tests on PR #1/#3/#5/#6/#7 by this authorization batch. No new review triggers on existing PRs.

**繁體中文**

分開記錄合成與真實結果、確切的 repo ID／PR／head／base／範圍／review／App／actor／run／金鑰 ID、預期／實際、時間戳記與 URL；絕不記錄機密值。本授權批次不對 PR #1/#3/#5/#6/#7 進行測試。不對既有 PR 發出新的 review 觸發。

## Rollback
1. Human disables Control Actions, cancels queued/running jobs, prevents dispatch. This emergency stop must be included in execution authorization.
2. Revoke installation tokens and App keys if compromise suspected; remove installation access or suspend/uninstall only under explicit rollback authorization.
3. Revoke affected signing keys/identity enrollment; collector freshness/revocation unknown => BLOCK. Preserve signed/public evidence and logs, do not delete audit records.
4. Mark sandbox results invalid, leave Draft PRs unmerged. No force push/reset or production changes.
5. Restore reviewed control release via a Human-reviewed change only after cause and custody revalidated. Re-enabling requires new approval.
No resource deletion or unrelated account changes in rollback. Proposed R1/R2 first batch rollback is leave empty repos with Actions disabled; archive/delete requires separate approval.

**繁體中文**

1. Human 停用 Control Actions、取消排隊中／執行中的 job，並阻止 dispatch。此緊急停止必須納入執行授權。
2. 若懷疑遭入侵，撤銷 installation token 與 App 金鑰；僅在明確的回復授權下移除 installation 存取或暫停／解除安裝。
3. 撤銷受影響的簽署金鑰／身分登記；collector 的新鮮度／撤銷狀態未知 => BLOCK。保留已簽署／公開的證據與日誌，不刪除稽核記錄。
4. 將 sandbox 結果標為無效，Draft PR 不合併。不 force push／reset，不變更正式環境。
5. 僅在原因與保管重新驗證之後，透過 Human 審查的變更恢復已審查的 control 版本。重新啟用需要新的核准。

回復時不刪除資源，也不變更無關的帳號。提議的 R1/R2 首批回復方式為保留空的 repo 並停用 Actions；封存／刪除需另行核准。

## First authorization request (resource-only)
Approve separately R1, R2, C1, C2:
- two exact proposed PUBLIC repositories, synthetic data only, Human owner myaiwouldbemine;
- Actions disabled in both immediately during setup, no credentials/Apps/workflows executed;
- no paid spend or plan changes.
GitHub defaults may enable Actions on creation: no workflows are added before disabling and confirming settings.
If a name is unavailable, STOP and request alternate name; no substitution. No App registration, installation, key generation, secrets, protections or live test execution is included.
This creates a reviewable isolated resource baseline; remaining C/A/I/K/M/W/E/T/B rows need subsequent individual authorization.

**繁體中文**

分別核准 R1、R2、C1、C2：

- 兩個確切提議的 PUBLIC repository，僅限合成資料，Human 擁有者為 myaiwouldbemine；
- 設定期間立即停用兩者的 Actions，不執行憑證／App／workflow；
- 無付費支出或方案變更。

GitHub 預設可能在建立時啟用 Actions：在停用並確認設定之前，不加入任何 workflow。

若名稱不可用，STOP 並請求替代名稱；不自行替換。不包含 App 註冊、安裝、金鑰產生、secrets、保護或即時測試執行。

這會建立可供審查的隔離資源基線；其餘 C/A/I/K/M/W/E/T/B 各列需要之後逐項授權。
