# Agent Instructions — Minimal Learning Hub

- Read GOVERNANCE.md and the Issue boundary. Human myaiwouldbemine is the sole administrator; 採 Tool-Neutral Single-Builder + Self-Verification：每個工程 Issue／PR 在任一時點只有一位指定 accountable Builder（Claude Code 或 Codex），兩者適用相同風險、驗證、Self-Review、Evidence 與授權規範。
- ChatGPT＋Human 擁有 V2／V3 教材創作、推導、品質核准與整合定稿權；製作時分開、定稿時合併、網站上依主題呈現。GitHub 保存已核准教材、版本及學習軌跡；MkDocs 提供閱讀、搜尋、導覽與展示。Builder 負責工程及忠實匯入已核准教材，不創作或修改教材語意；語意問題標記 PENDING，交由 ChatGPT／Human 決定。
- Learning Record Issue 可透過 Comments 逐步更新，不必對應工程 PR；只有 Repository 變更需要下列工程流程。Issue 建立、CI PASS、PR Merge 或 Issue Closed 均不代表內容品質核准、學習完成或完全掌握。
- 工程 Issue／PR 記錄唯一 accountable Builder。交接記錄前後 Builder、完整 Commit SHA、base／scope／risk、已完成／未完成、Evidence 與 Blockers。接手者重新確認目前 head 的 Self-Review、證據有效性及適用 Human 授權，評估 base／scope／risk 變化；工具更換不自動轉移舊審查結論或 Human 授權。
- Use Issue → Draft PR → conditional Plan → Implementation → conditional Result → Self-Review → authorized Merge. Open Draft early; Draft grants no implementation or merge authority.
- Classify actual impact: L0 nonsemantic typo/formatting, L1 substantive content/code, L2 major architecture/provenance, L3 security/governance/permissions/deployment/irreversible operations. Unknown risk blocks clarification-dependent work.
- L0 needs no mandatory Plan/Result or Self-Review evidence. L1 needs traceable Self-Review with documented Evidence. L2/L3 need pre-implementation Plan and Human approval; L3 also needs specific action/scope authorization.
- Fresh-Context Challenge: Optional verification per risk; not mandatory daily review. 由指定 Builder 評估必要性並記錄執行或省略理由。 Human-mandated challenges cannot be skipped. Not an Agent Handoff or governance platform.
- Formal Plans go in records/ISSUE-<number>/PLAN.md and must be committed before their implementation; preserve history. If a formal Plan exists, write RESULT.md after implementation. Do not fabricate historical ordering.
- Record actual Builder work, full reviewed commit, relevant base/scope, findings/verdict and evidence in the PR. Self-review is not cross-review; distinguish Self-Review Evidence from independent Review. Document Fresh-Context Challenge if applied.
- Distinguish Bot Summary, native GitHub Review and Human Approval. No mandatory native APPROVED conversion, App/Registry/Attestation/Control Plane/second Human. Do not claim automated trusted identity verification.
- Run applicable tests/CI and strict MkDocs for site changes. Report build/content/provenance/visual/deployment separately. Missing, failed, skipped, pending, stale evidence or unresolved blockers prevents Merge.
- New head requires Review reconfirmation; base/scope/risk changes require reassessment and renewed authorization where necessary.
- Ready requires completed implementation, applicable verification and conditional Result; follow explicit PR status boundaries and authorization.
- Merge only with explicit operation authority, non-Draft and all applicable conditions met. L1 has no mandatory per-PR Human content approval. No direct main push, force push, bypass, unauthorized Merge/deployment or Auto-Merge activation.
- Roll back using an authorized revert PR and applicable checks. Human handles L2 Plan/L3 action approval and emergency stop.
- Archived platform designs/tests and historical records are evidence, not active instructions. C3-C5 and later platform work are stopped. Do not provision new governance infrastructure.
