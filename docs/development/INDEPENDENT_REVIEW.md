> **ARCHIVED / NOT ACTIVE.** Superseded by Minimal Governance. C3–C5 and later platform implementation are stopped. The original proposal/evidence below is preserved, not current policy or authorization. Prototype code/tests formerly under scripts/ are retained under archive/governance-platform/scripts/.

**繁體中文**

> **已封存／非現行有效。** 已被 Minimal Governance 取代。C3–C5 及之後的平台實作已停止。以下原始提案／證據僅為保存，不是現行政策或授權。原先位於 scripts/ 下的原型程式碼／測試保留於 archive/governance-platform/scripts/。

# Independent Review Identity Gate

Status: isolated implementation; production integration BLOCKED. Codex/Claude roles are interchangeable. L0 exempts independent review only, never other gates or unresolved blockers.

**繁體中文**

狀態：隔離的實作；正式環境整合為 BLOCKED。Codex／Claude 角色可互換。L0 僅豁免獨立審查，絕不豁免其他閘門或未解的阻擋項目。

## Trust boundary
Use native GitHub PR reviews for review state, immutable reviewer actor ID, review ID and commit ID. Prefer the existing Codex GitHub Bot if its actual App provenance can be independently verified; do not infer identity from a login/display name. Claude requires an equivalently authenticated integration. A human OAuth token, shared account or text claiming an agent role cannot establish identity.

**繁體中文**

使用原生 GitHub PR review 取得 review 狀態、不可變的 reviewer actor ID、review ID 與 commit ID。若能獨立驗證現有 Codex GitHub Bot 的實際 App 出處，則優先採用；不得從登入名稱／顯示名稱推斷身分。Claude 需要同等經驗證的整合。Human OAuth token、共用帳號，或宣稱某 agent 角色的文字，皆無法確立身分。

A trusted collector, running outside Builder control, supplies the registry, current repository/PR/head/base/diff digest and API facts to scripts/review_identity.py. Registry maps pinned actor/App IDs to agent and isolated credential custody; never load it from the PR branch. Builder provenance must likewise be independently collected, not inferred from a commit author. GitHub App review provenance must be verified from authenticated API/event data; unavailable provenance blocks.

**繁體中文**

在 Builder 控制之外執行的可信 collector，將 registry、目前的 repository／PR／head／base／diff 摘要（digest）及 API 事實提供給 scripts/review_identity.py。Registry 將固定的 actor／App ID 對應到 agent 與隔離的憑證保管；絕不從 PR 分支載入。Builder 的出處同樣必須獨立收集，不得由 commit 作者推斷。GitHub App review 的出處必須由經驗證的 API／事件資料驗證；無法取得出處則阻擋。

Native reviews bind head but do not establish base SHA or complete scope. Versioned attestation supplies repository, PR, head, base, builder/reviewer registered identities, verdict, scope (canonical complete diff SHA-256 digest) and native review ID. Schema: scripts/reviewer-attestation.schema.json. Authenticate the entire attestation through the isolated reviewer integration, binding payload bytes and issuer; a JSON document alone has no authority. The collector verifies authentication before setting attestation_authenticated. Never accept this flag or any facts from Builder/PR HTTP input.

**繁體中文**

原生 review 綁定 head，但不能確立 base SHA 或完整範圍。具版本的 attestation 提供 repository、PR、head、base、builder／reviewer 已註冊身分、verdict、範圍（標準化完整 diff 的 SHA-256 摘要）及原生 review ID。Schema：scripts/reviewer-attestation.schema.json。須透過隔離的 reviewer 整合對整份 attestation 進行驗證，綁定 payload 位元組與簽發者；僅有 JSON 文件不具權威。Collector 在驗證通過後才設定 attestation_authenticated。絕不接受來自 Builder／PR HTTP 輸入的此旗標或任何事實。

Re-fetch all paginated reviews and threads, resolve latest state/dismissal per reviewer, preserve any active CHANGES_REQUESTED and unresolved blocking thread. Unknown/incomplete retrieval blocks. Collect fresh head/base and scope, invalidate on changes and recheck immediately before expected-head merge. Collector must prevent replay against another PR/base/scope. Tests use synthetic IDs and facts; none proves credential isolation or a real GitHub identity.

**繁體中文**

重新取得所有分頁的 review 與討論串，解析每位 reviewer 的最新狀態／dismissal，保留任何有效的 CHANGES_REQUESTED 及未解決的阻擋性討論串。未知或不完整的取得結果即阻擋。收集最新的 head／base 與範圍，變更時使其失效，並在附預期 head 的合併前立即重新檢查。Collector 必須防止對另一個 PR／base／範圍重放。測試使用合成的 ID 與事實；沒有任何一項能證明憑證隔離或真實的 GitHub 身分。

## Four distinct concepts
- GitHub Review: native submitted review and its current state; authenticated actor alone does not prove which agent performed work.
- Agent Attestation: authenticated context/scope/agent binding supplementing native review; never a Human approval.
- Policy Check: trusted service's decision after collection and validation; test CI is not this service.
- Human Approval: separately authenticated authorization for L2 plans/L3 actions; cannot be supplied by Agent attestation or PASS check.

**繁體中文**

- GitHub Review：原生提交的 review 及其目前狀態；僅憑經驗證的 actor 不能證明是哪個 agent 執行了工作。
- Agent Attestation：補充原生 review、經驗證的 context／範圍／agent 綁定；絕不是 Human 核准。
- Policy Check：可信服務在收集與驗證後作出的決定；測試 CI 不是此服務。
- Human Approval：針對 L2 plan／L3 動作，另行經驗證的授權；不能由 Agent attestation 或 PASS check 提供。

## Revision 3 baseline — superseded by Revision 4 prototype
Keep the proposed single control-plane App and aggregate eligibility check; no additional review database or webhook service is required. Reviewer integrations remain separate trust principals. This patch implements the offline decision component only; no network collector, signature verifier, Bot installation, registry provisioning, credential isolation or production check publication is implemented/claimed.

**繁體中文**

保留所提議的單一 control-plane App 與彙總的資格 check；不需要額外的 review 資料庫或 webhook 服務。Reviewer 整合仍是各自獨立的信任主體。本 patch 僅實作離線的決策元件；未實作也不宣稱任何網路 collector、簽章驗證器、Bot 安裝、registry 佈建、憑證隔離或正式環境的 check 發布。

Required before real integration: verify Codex Bot availability/App ID/actor ID and review capability; establish Claude authenticated reviewer provenance; establish authenticated Builder provenance; provision isolated custody outside Builder access; implement authenticated attestation transport and complete API collector; validate actual native reviews, dismissal/thread aggregation and races in an authorized test repository. Installation/credentials/official Ruleset changes require specific L3 authorization under the current user boundary. No such changes were performed here.

**繁體中文**

真實整合之前必須：驗證 Codex Bot 的可用性／App ID／actor ID 與 review 能力；建立 Claude 經驗證的 reviewer 出處；建立經驗證的 Builder 出處；在 Builder 無法存取之處佈建隔離的保管；實作經驗證的 attestation 傳輸與完整的 API collector；在獲授權的測試 repository 中驗證實際的原生 review、dismissal／討論串彙總與競態。安裝／憑證／正式 Ruleset 變更在目前使用者邊界下，需要具體的 L3 授權。此處未進行任何此類變更。

Tests cover both role directions, self-review, shared Human identity, missing reviewer, old head/base/context, requested changes/dismissals, blocking threads, forged/missing facts and L0 other-gate preservation. All are simulated. Readiness: BLOCKED for real independent review identity; implementation may be inspected while PR #5 stays Draft.

**繁體中文**

測試涵蓋雙向角色、自審、共用 Human 身分、缺少 reviewer、舊的 head／base／context、requested changes／dismissal、阻擋性討論串、偽造／缺失的事實，以及 L0 對其他閘門的保留。全部為模擬。就緒狀態：真實獨立 review 身分為 BLOCKED；PR #5 維持 Draft 期間可檢視此實作。

## Revision 4 — Trusted Collector prototype (2026-11-05)

### Real read-only discovery, separate from simulations
PR #5 is OPEN/Draft at discovery head 879c3704abc2a9ae07d05ec7875f8c1988e470d8, base f4a429c9ea51f1542c85d92571b5d4a5c15e86b5. PR #5 reviews/threads and PR #1 reviews are empty. records/ISSUE-4/trusted-review-discovery.json contains a real API snapshot and missing-identity BLOCK; it predates this revision and cannot authorize new heads.

**繁體中文**

PR #5 為 OPEN／Draft，探索時的 head 為 879c3704abc2a9ae07d05ec7875f8c1988e470d8，base 為 f4a429c9ea51f1542c85d92571b5d4a5c15e86b5。PR #5 的 review／討論串以及 PR #1 的 review 皆為空。records/ISSUE-4/trusted-review-discovery.json 包含真實的 API 快照及缺少身分的 BLOCK；它早於本修訂，不能授權新的 head。

The GitHub plugin can access this repository and lists installation 133111057 for owner account 275012389 with repository_selection=all. This establishes connector access, not enabled Codex Code Review. The result exposes neither App ID nor bot actor ID. No actual Codex or Claude reviewer App/actor pair was verified. Installation ID and owner ID are not reviewer App/actor IDs.

**繁體中文**

GitHub plugin 可存取此 repository，並列出擁有者帳號 275012389 的安裝 133111057，repository_selection=all。這只能確立連接器的存取，不能確立已啟用 Codex Code Review。結果並未揭露 App ID 或 bot actor ID。尚未驗證任何實際的 Codex 或 Claude reviewer App／actor 配對。安裝 ID 與擁有者 ID 不是 reviewer 的 App／actor ID。

Local gh authenticates as Human OAuth account myaiwouldbemine, actor 275012389, scopes repo/workflow/read:org/gist. No token values or key stores were read/copied. /user/installations returned 403 requiring GitHub App user authentication; repository /installation returned 401 requiring App authentication. Neither proves App absence. Builder operations currently use Human credentials; isolated Builder App provenance and Reviewer custody are unverified. Two agents sharing this token cannot establish independence.

**繁體中文**

本機 gh 以 Human OAuth 帳號 myaiwouldbemine（actor 275012389，scopes 為 repo/workflow/read:org/gist）驗證。未讀取／複製任何 token 值或金鑰儲存。/user/installations 回傳 403，需要 GitHub App 使用者驗證；repository /installation 回傳 401，需要 App 驗證。兩者都不能證明 App 不存在。Builder 操作目前使用 Human 憑證；隔離的 Builder App 出處與 Reviewer 保管皆未經驗證。兩個 agent 共用此 token 無法確立獨立性。

Ruleset 26612260 is active ONLY for refs/heads/canary/light-enforcement-issue-4, no bypass actors; deletion/non-fast-forward restrictions plus PR/thread resolution, zero required approvals, no required_status_checks rule. Effective rules for main and feat/CLH-001-project-bootstrap are []; classic protection returns 404 'Branch not protected' for both. No Required Checks observed on either target. Existing governance-tests SUCCESS is from GitHub Actions App 15368, not a Reviewer identity or trusted eligibility check. No settings changed.

**繁體中文**

Ruleset 26612260 僅對 refs/heads/canary/light-enforcement-issue-4 為 active，無 bypass actor；包含刪除／非 fast-forward 限制，以及 PR／討論串解決，必要核准數為零，無 required_status_checks 規則。main 與 feat/CLH-001-project-bootstrap 的有效規則皆為 []；傳統保護對兩者皆回傳 404「Branch not protected」。在兩個目標上均未觀察到必要 Check。既有的 governance-tests SUCCESS 來自 GitHub Actions App 15368，不是 Reviewer 身分，也不是可信的資格 check。未變更任何設定。

### Official capability evidence
- [Codex GitHub review](https://learn.chatgpt.com/docs/third-party/github): requires connection/review enablement; supports @codex review. No documented promise of APPROVED verdict, signed scope attestation or isolated custody. No trigger comment sent.
- [Claude GitHub Actions](https://code.claude.com/docs/en/github-actions): supports official/custom GitHub App; github_token override changes authentication. Model subscription/API credentials are separate from GitHub principal. This does not establish repository installation or identity.
- [GitHub Review REST API](https://docs.github.com/en/rest/pulls/reviews): review ID, numeric user ID/type, state, submitted_at and commit_id. DISMISSED invalidates approval. Native review does not bind base/scope or expose reliable issuing App ID.
- [Review webhooks](https://docs.github.com/en/webhooks/webhook-events-and-payloads#pull_request_review): delivery signature authenticates transport; installation denotes receiving installation and must not be treated as author App. Timeline/events can provide dismissal actor/reason; this prototype checks current DISMISSED state and does not claim a dismissal history audit.
- GraphQL reviewThreads provides isResolved/cursor pagination. All unresolved threads, including outdated ones, conservatively block.

**繁體中文**

- [Codex GitHub review](https://learn.chatgpt.com/docs/third-party/github)：需要連接／啟用 review；支援 @codex review。文件未承諾 APPROVED verdict、簽署的範圍 attestation 或隔離保管。未發送任何觸發留言。
- [Claude GitHub Actions](https://code.claude.com/docs/en/github-actions)：支援官方／自訂 GitHub App；覆寫 github_token 會改變驗證。模型訂閱／API 憑證與 GitHub 主體是分開的。這並未確立 repository 安裝或身分。
- [GitHub Review REST API](https://docs.github.com/en/rest/pulls/reviews)：review ID、數字 user ID／類型、state、submitted_at 與 commit_id。DISMISSED 使核准失效。原生 review 不綁定 base／範圍，也不揭露可靠的簽發 App ID。
- [Review webhooks](https://docs.github.com/en/webhooks/webhook-events-and-payloads#pull_request_review)：投遞簽章驗證的是傳輸；installation 表示接收事件的安裝，不得視為作者 App。Timeline／事件可提供 dismissal 的 actor／原因；本原型檢查目前的 DISMISSED 狀態，並不宣稱具有 dismissal 歷史稽核。
- GraphQL reviewThreads 提供 isResolved／cursor 分頁。所有未解決的討論串（包含已過時者）一律保守地阻擋。

### Implementation and limits
scripts/trusted_review_collector.py collects REST reviews/files and GraphQL threads with complete pagination/count checks, rejects duplicates/unknown states/partial GraphQL, and recollects the entire snapshot. Every active CHANGES_REQUESTED blocks conservatively even if superseded; selected approval must be latest decisive review for pinned actor.

**繁體中文**

scripts/trusted_review_collector.py 以完整分頁／數量檢查收集 REST review／檔案與 GraphQL 討論串，拒絕重複項／未知狀態／不完整的 GraphQL，並重新收集整個快照。每一個有效的 CHANGES_REQUESTED 即使已被取代也保守地阻擋；被選用的核准必須是該固定 actor 最新的決定性 review。

Scope v1 is SHA256 of canonical JSON with repository/PR/head/base and sorted complete file manifest (filename, sha, status, changes, previous_filename). Both commits bind complete trees including binaries. This defines the earlier unspecified diff digest; all signers must use this exact manifest algorithm. Files API cap of 3000 blocks.

**繁體中文**

Scope v1 是標準化 JSON 的 SHA256，內容包含 repository／PR／head／base 及排序後的完整檔案清單（filename、sha、status、changes、previous_filename）。兩個 commit 皆綁定包含二進位檔在內的完整 tree。這定義了先前未明確規定的 diff 摘要；所有簽署者必須使用此確切的清單演算法。Files API 上限 3000 即阻擋。

Reviewer subject is existing schema-v1 attestation. Builder subject is purpose=builder-provenance-v1 plus repository/PR/head/base/scope/builder. Envelope fields: subject, issued_at, expires_at, key_id, signature. Integer UTC Unix times, max lifetime 300 seconds. Base64 Ed25519 signature over canonical JSON of other four fields. Canonical JSON uses sorted keys, compact separators, ASCII escapes. OpenSSL verifies against externally pinned public key. Missing, invalid, wrong signer, unknown key, revoked key/identity, future/expired envelopes block; trusted host clock rechecks expiry after API collection.

**繁體中文**

Reviewer 的 subject 是既有的 schema-v1 attestation。Builder 的 subject 是 purpose=builder-provenance-v1 加上 repository／PR／head／base／範圍／builder。封套欄位：subject、issued_at、expires_at、key_id、signature。時間為整數 UTC Unix 時間，最長有效期 300 秒。簽章為對其他四個欄位的標準化 JSON 所做的 Base64 Ed25519 簽章。標準化 JSON 使用排序的鍵、緊湊分隔符號及 ASCII 跳脫。OpenSSL 以外部固定的公鑰驗證。缺失、無效、簽署者錯誤、未知金鑰、已撤銷的金鑰／身分，或未來／已過期的封套皆阻擋；可信主機時鐘於 API 收集後重新檢查有效期。

Registry additionally requires active identity/key revocation state, distinct App/actor IDs, kind=github_app, isolated=true, agent and distinct nonempty custody IDs. Key-to-App/actor binding MUST be independently enrolled from authenticated App/token evidence and audited custody. Bot type alone grants no trust. review_app_id is derived from enrolled signature identity, NOT a native REST field. Custody IDs are enrolled assertions, not technical proof by this code. Builder provenance issuer must observe actual execution/commit context, not sign Builder claims. Neither real issuer exists here.

**繁體中文**

Registry 另外要求：身分／金鑰撤銷狀態為 active、App／actor ID 彼此不同、kind=github_app、isolated=true、agent，以及彼此不同且非空的保管 ID。金鑰與 App／actor 的綁定必須由經驗證的 App／token 證據與已稽核的保管獨立登記。僅憑 Bot 類型不授予任何信任。review_app_id 來自已登記的簽章身分，不是原生 REST 欄位。保管 ID 是登記的聲明，並非本程式碼提供的技術證明。Builder 出處的簽發者必須觀察實際的執行／commit context，而不是簽署 Builder 的聲明。此處兩種真實簽發者皆不存在。

No production CLI/endpoint, privileged workflow, check publisher, registry/secret loader or merge executor exists. Host must execute a pinned reviewed release outside candidate control; policy, registry and keys stay outside PR/repository. Never import this module from candidate checkout in a trusted service. gh Human OAuth is discovery transport only. L0 still checks blockers and returns review NOT_REQUIRED only; Draft/CI/Records/risk/authorization gates remain mandatory.

**繁體中文**

不存在正式環境的 CLI／endpoint、特權 workflow、check 發布器、registry／secret 載入器或 merge executor。主機必須在候選程式碼控制之外執行固定且經審查的版本；政策、registry 與金鑰留在 PR／repository 之外。絕不在可信服務中從候選 checkout 匯入此模組。gh Human OAuth 僅作為探索用傳輸。L0 仍檢查阻擋項目，且 review 僅回傳 NOT_REQUIRED；Draft／CI／Records／風險／授權閘門仍然必要。

Two matching API collections are not atomic and may miss changes followed by reverts. PASS is only a bounded observation of review component. Production requires event invalidation for head/base/review/thread/revocation, serialized decisions, short TTL and immediate rechecks before any separately authorized action. Merge race protection and required-check source enforcement are unproven.

**繁體中文**

兩次相符的 API 收集不是原子性的，可能漏掉先變更後又還原的情況。PASS 僅是對 review 元件的有限觀察。正式環境需要針對 head／base／review／討論串／撤銷的事件失效機制、序列化決策、短 TTL，以及在任何另行授權的動作之前立即重新檢查。合併競態保護與必要 check 來源的強制執行尚未證實。

### Credential isolation proposal — not provisioned
| Principal | Separate custody and least privilege | Required evidence |
|---|---|---|
| Builder App | Builder runner/vault; contents/PR write where needed | App/actor/token identity and execution-bound provenance |
| Reviewer App | Reviewer runner/vault; contents read, PR review write; no Builder keys | App/actor/installation enrollment, native review plus signature |
| Collector | Protected control-plane deployment; contents/PR read | Pinned code/policy/registry and current revocation |
| Future publisher/executor | Separate later approval | No keys or permissions granted here |

**繁體中文**

| 主體 | 獨立保管與最小權限 | 必要證據 |
|---|---|---|
| Builder App | Builder runner／vault；必要處有 contents／PR write | App／actor／token 身分及綁定執行的出處 |
| Reviewer App | Reviewer runner／vault；contents read、PR review write；無 Builder 金鑰 | App／actor／安裝登記、原生 review 加簽章 |
| Collector | 受保護的 control-plane 部署；contents／PR read | 固定的程式碼／政策／registry 及目前的撤銷狀態 |
| 未來的 publisher／executor | 另行於之後核准 | 此處不授予金鑰或權限 |

Signing keys must never enter PR jobs/artifacts, candidate-readable repository secrets, or each other's runners. Collector holds public keys only. Product App availability is insufficient unless authenticated context attestation and execution provenance are supported. If unsupported, propose a separate enrolled broker before provisioning; never substitute a Human token.

**繁體中文**

簽署金鑰絕不得進入 PR job／artifact、候選程式碼可讀取的 repository secrets，或彼此的 runner。Collector 僅持有公鑰。除非支援經驗證的 context attestation 與執行出處，否則產品 App 的可用性並不足夠。若不支援，須在佈建前提議另行登記的 broker；絕不以 Human token 取代。

### Isolated real Canary — ALL NOT RUN
Use dedicated private sandbox repository, synthetic branches, no deploy workflows or auto-merge. Authorize exact App enrollment/custody before tests. Installations, credentials, rules or permission changes each need Human approval.

**繁體中文**

使用專用的私有 sandbox repository、合成分支，且無部署 workflow 或 auto-merge。在測試前授權精確的 App 登記／保管。安裝、憑證、規則或權限變更各自需要 Human 核准。

Record actual repo ID/name, PR, head/base/scope, review ID/actor, App/installation/key IDs (no secrets), API pagination/counts, signature/time/revocation decisions, expected/actual result and CI URL separately from fixtures.

**繁體中文**

記錄實際的 repo ID／名稱、PR、head／base／範圍、review ID／actor、App／installation／金鑰 ID（不含機密）、API 分頁／數量、簽章／時間／撤銷決定、預期／實際結果，以及與 fixture 分開的 CI URL。

| Case | Expected |
|---|---|
| Valid enrolled independent reviewer and fresh scope, no blockers | Review component PASS; other gates remain |
| Same App/actor or shared Human token/custody | BLOCK |
| Forged identity/signature, unknown key, missing reviewer/provenance | BLOCK |
| New head/base or scope | BLOCK until new signed evidence |
| Selected review dismissed/superseded | BLOCK |
| Changes requested or unresolved/outdated thread | BLOCK |
| Timeout/denial/partial response/missing page/count/file cap | BLOCK |
| Revoked issuer/key, invalid/expired/future attestation | BLOCK |
| Mutable state changes during collection or expiry mid-collection | BLOCK |
| L0 without attestation | NOT_REQUIRED only; other gates/blockers remain |

**繁體中文**

| 案例 | 預期 |
|---|---|
| 有效的已登記獨立 reviewer 與最新範圍，無阻擋項目 | Review 元件 PASS；其他閘門仍然存在 |
| 相同 App／actor 或共用 Human token／保管 | BLOCK |
| 偽造的身分／簽章、未知金鑰、缺少 reviewer／出處 | BLOCK |
| 新的 head／base 或範圍 | BLOCK，直到有新的已簽署證據 |
| 被選用的 review 被 dismiss／取代 | BLOCK |
| Changes requested 或未解決／已過時的討論串 | BLOCK |
| 逾時／拒絕／不完整的回應／缺少分頁／數量／檔案上限 | BLOCK |
| 已撤銷的簽發者／金鑰、無效／已過期／未來的 attestation | BLOCK |
| 收集期間可變狀態改變，或收集中途過期 | BLOCK |
| L0 無 attestation | 僅 NOT_REQUIRED；其他閘門／阻擋項目仍然存在 |

No real positive reviewer Canary or ruleset enforcement test ran in this revision. Live missing-evidence BLOCK is discovery only.

**繁體中文**

本修訂未執行任何真實的正向 reviewer Canary 或 ruleset 強制執行測試。即時的缺少證據 BLOCK 僅是探索。

### Smallest next Human action
Provide read-only non-secret existing Codex/Claude installation details: actual App ID, installation ID, selected repository, permissions, canonical bot actor ID and credential custody owner/location. No installation or permission increase is requested yet. If those integrations cannot issue context attestations/provenance, present a separate exact sandbox App manifest/credential/custody authorization request before any change. Production remains BLOCKED, not READY.

**繁體中文**

請提供現有 Codex／Claude 安裝的唯讀、非機密詳細資料：實際 App ID、installation ID、選定的 repository、權限、標準 bot actor ID 及憑證保管的擁有者／位置。目前不要求任何安裝或權限提升。若這些整合無法簽發 context attestation／出處，則須在任何變更之前，另行提出精確的 sandbox App manifest／憑證／保管授權請求。正式環境維持 BLOCKED，而非 READY。
