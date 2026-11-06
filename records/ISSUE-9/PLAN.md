# Issue #9 — LIGHT Governance v2: Claude Code Single-Builder + Self-Verification

## Formal Plan v3 (Revised)

**Issue**: https://github.com/myaiwouldbemine/myaiwouldbemine-Copy-Learning-Hub/issues/9  
**Builder**: Claude Code  
**Risk Level**: L3 (Governance policy semantic change)  
**Status**: PLAN PENDING HUMAN APPROVAL — NO IMPLEMENTATION AUTHORIZED  
**Date**: 2026-11-06 (v3 Revision: 2026-11-06 11:37 UTC+8)  
**Current Main HEAD**: cdab0f8e3171861bcd568a8c4597daf4bff75840 (Plan v2 committed)  
**Records Location**: records/ISSUE-9/PLAN.md

---

## Revision History

### v2 → v3 (Current Revision)

**Changes**:
- F-01：Verified Issue template line count (66 lines, not 100); templates MODIFY status confirmed
- F-02：Clarified Plan commit sequence (v2 already committed; v3 is revision; implementation commits pending)
- F-03：Corrected Rollback strategy (preserve history, no deletion)
- F-04：Distinguished current cross-Agent review requirement from future Self-Verification framework
- F-05：Enhanced verification accuracy (governance semantics, field validation, CI checks)
- F-06：Corrected v1 status from REJECTED to CHANGES REQUESTED (per GitHub evidence)
- **NEW**: Added Formal Plan Dual Persistence rule to Section 11
- **NEW**: Added github Issue Timeline evidence requirements

**v1 Disposition**: CHANGES REQUESTED (Human feedback on Plan v1; Plan v2 submitted as corrected version)

**v2 Status**: PENDING HUMAN APPROVAL (Committed to records/ISSUE-9/PLAN.md; Posted to Issue #9 Timeline)

---

## 1. Goal / WHY

### 1.1 Primary Goal
Adopt Claude Code as the sole **daily Builder** for Learning Hub, replacing mandatory Codex ↔ Claude Code cross-Agent review with explicit **Self-Verification** (Source / Claim / Method / Evidence / Commit SHA).

**Rationale**: Learning Hub's purpose is learning and knowledge documentation, not multi-Agent governance. Simplified responsibility removes overhead while maintaining L2/L3 risk control.

### 1.2 Core Principles (v2)

**Claude Code Builder Lifecycle**:
```
Investigation → Plan (L2/L3) → Implementation → Self-Review + Evidence 
→ [Fresh-Context Challenge, if needed] → Result (L2/L3) → Readback
```

**Self-Verification ≠ Independent Review**:
- Self-Review must cite **Source / Claim / Method / Evidence / Commit SHA**.
- No false claim to independence or autonomous authority.
- Clear, traceable record of who did what.

**Fresh-Context Challenge** (optional, proportional risk):
- Claude Code evaluates necessity per task risk.
- Recorded in Plan with trigger & rationale.
- Human may explicitly require it.
- Cannot omit if necessary verification fails.
- Does NOT create Agent Handoff or new governance platform.

---

## 2. Current-State Evidence (HEAD: cdab0f8, v3 Verified 2026-11-06 11:37 UTC+8)

### 2.1 Existing Governance Framework (v1 — Current)

**File Status** (F-01 Verification):
- **GOVERNANCE.md** (51 lines): v1 mandates Codex ↔ Claude Code mutual cross-review L1–L3 (current active policy)
- **AGENTS.md** (15 lines): Both agents listed as peers; cross-review requirement stated (current active policy)
- **.github/ISSUE_TEMPLATE/01-agent-task.yml** (66 lines, NOT 100): Created by PR #6; contains **WHAT / WHY / Acceptance Criteria / Boundary** (mandatory) + References / Evidence (optional); does NOT include Scope as mandatory field
- **.github/PULL_REQUEST_TEMPLATE.md** (29 lines): Contains "Opposite Agent Review" section (current active policy)

**Correction (F-01 Accuracy)**:
- Plan v2 stated Issue template as 100 lines; actual line count is 66 lines
- Issue template modification status: **MODIFY** (confirmed; created by PR #6, exists in main)
- Template mandatory fields: WHAT, WHY, Acceptance Criteria, Boundary (do NOT add Scope as mandatory)
- Plan v3 will update four-file specs with verified line counts

### 2.2 L0–L3 Framework (Unchanged)
| Level | Scope | Conditions |
|-------|-------|-----------|
| L0 | Nonsemantic (typo/format) | Applicable verification; no mandatory Plan/Result/Review |
| L1 | Substantive content/code | Applicable verification + cross-Agent review |
| L2 | Major architecture | L1 + pre-Plan / post-Result + Human Plan approval |
| L3 | Governance/security/deployment | L2 + Human specific action authorization |

### 2.3 Records Structure
- records/ISSUE-4/ contains PLAN.md (5 revisions) and RESULT.md.
- Pattern: PLAN.md committed **before** implementation; RESULT.md after.
- No retroactive planning or history rewriting.

---

## 3. Risk Level

**L3: Governance Policy Semantic Change**

**Justification**:
- Removes mandatory cross-Agent review (L1–L3) as a gating condition.
- Changes Builder responsibility boundaries.
- Affects future PR merge criteria and review obligations.

**Why NOT Higher**:
- No security/permission/deployment automation changes.
- No repository settings, branch protection, or ruleset edits.
- Human retains full approval authority.
- Rollback via standard revert PR; no force push.

**Risk Control Preserved**:
- L0–L3 definitions unchanged.
- L2/L3 Plan + Human approval mandatory (non-negotiable).
- Self-Review evidence requirements strengthened (not weakened).
- Fresh-Context Challenge available for high-risk tasks.
- L2/L3 cannot default-pass due to removed cross-Agent review.

---

## 4. Scope: Four Files + records/ISSUE-9/

### 4.1 Modifications Required

#### File 1: GOVERNANCE.md (51 → ~65 lines)

**Current** (Lines 7–8):
```
目前採用極簡治理。唯一 Human 管理者為 myaiwouldbemine；Codex 與 Claude Code 為對等 Agent。
```

**Proposed**:
```
目前採用極簡治理。唯一 Human 管理者為 myaiwouldbemine；Claude Code 為唯一日常 Builder。
```

**Current** (Lines 20–22, L1 Risk Condition):
```
| L1 | 教材語意、一般程式或網站行為 | 適用驗證＋不同 Agent 的可追溯交叉 Review |
```

**Proposed**:
```
| L1 | 教材語意、一般程式或網站行為 | 適用驗證 + Claude Code Self-Review（Source/Claim/Method/Evidence/Commit SHA） |
```

**Section "交叉 Review" (Lines 29–43)**: Rename to "Self-Review & Verification"

**Current**:
```
Codex Builder 由 Claude Code Review，反向亦然。L1–L3 缺少另一 Agent 的 Review 時維持 pending，不以自評取代。
```

**Proposed**:
```
Claude Code 負責 Implementation → Self-Review + Evidence。L1–L3 Self-Review 必須記錄 Source、Claim、Method、Evidence、Commit SHA；
不得聲稱為獨立 Review（Self-Review ≠ Independent Review）。
```

**Add after Self-Review section**:
```
## Fresh-Context Challenge（L2／L3 按實際風險選用）
對高風險或不確定的 L2／L3 任務，Claude Code 評估是否需要額外核查。Challenge 在 Plan 中記錄觸發理由、執行方式及結果。
Human 得明確指定需要 Challenge。無法執行必要核查時，不得聲稱 PASS，保持 Draft 並向 Human 回報。
Fresh-Context Challenge 不建立 Agent Handoff、第二 Reviewer 或新的治理平台。
```

**Keep unchanged**:
- L0–L3 定義（Lines 15–26）
- Conditional Plan / Result 規則（Lines 27–28）
- Human Approval 規則（Lines 25, 31–35）
- Rollback, CI, Draft/Ready/Merge, Merge authorization（Lines 44–56 etc.）

#### File 2: AGENTS.md (15 lines → ~18 lines)

**Current Bullet 1**:
```
- Read GOVERNANCE.md and the Issue boundary. Human myaiwouldbemine is the sole administrator; Codex and Claude Code are peers.
```

**Proposed**:
```
- Read GOVERNANCE.md and the Issue boundary. Human myaiwouldbemine is the sole administrator; Claude Code is the designated daily Builder.
```

**Current Bullet 4**:
```
- L1 needs opposite-Agent cross-review.
```

**Proposed**:
```
- L1 needs Claude Code Self-Review with traceable evidence (Source / Claim / Method / Evidence / Commit SHA). Self-Review is not Independent Review.
```

**Add after Bullet 4**:
```
- L2/L3 may require Fresh-Context Challenge per Plan. Human may explicitly mandate Challenge. Cannot omit necessary verification; keep PR Draft if unable to proceed.
```

**Current Bullet 6**:
```
- Record actual Reviewer, full reviewed commit, relevant base/scope, findings/verdict and evidence in the PR. Self-review is not cross-review. Another login/shared Human token alone proves no independence.
```

**Proposed** (clarification only):
```
- Record actual Builder, full Self-Review commit, relevant base/scope, findings/verdict and evidence in the PR. Self-review is not Independent Review. Traceable evidence chain required.
```

**Keep unchanged**:
- Bullet 2 (Draft workflow)
- Bullet 3 (L0–L3 classification)
- Bullet 5 (Plan/Result structure)
- Bullets 7–13 (CI, Merge, Rollback, Platform/C3–C5 stopped)

#### File 3: .github/ISSUE_TEMPLATE/01-agent-task.yml (MODIFY, not CREATE)

**Current state**: Exists (PR #6); has 4 mandatory fields + optional References.

**Modifications**:
- Keep: name, description, title, body, four mandatory text fields (WHAT, WHY, Acceptance Criteria, Boundary)
- Keep: optional References / Evidence field
- **Do NOT add** Scope or any other mandatory field.
- Clarification: Update descriptions to reflect **Claude Code Single-Builder** (not "Codex 與 Claude Code 對等協作").

**Proposed change** in body markdown (line ~4):
```
Current:
## Human 定義需求；Codex 與 Claude Code 對等協作

Proposed:
## Human 定義需求；Claude Code 日常 Builder 負責
```

**Update conditions note** (lines ~8–10):
```
Current:
L1 起需要另一 Agent 可追溯的交叉 Review。

Proposed:
L1 起需要 Claude Code 可追溯的 Self-Review（記錄 Source / Claim / Method / Evidence / Commit SHA）。
```

**Remove reference to "另一 Agent"** and update to clarify Self-Review.

#### File 4: .github/PULL_REQUEST_TEMPLATE.md (MODIFY)

**Current "Review" section**:
```
## Review
Opposite Agent / pending / L0 not required:
Reviewed full commit SHA and relevant base/scope:
Findings / result / evidence link:
Bot Summary, native GitHub Review and Human Approval are distinct.
```

**Proposed**:
```
## Self-Review & Verification
Builder: Claude Code
Self-Review Status: [COMPLETE / PENDING / NOT REQUIRED (L0)]
Source / Claim / Method: [Describe what was checked and how]
Evidence (tests, logs, diffs, commit SHA):
Findings / result / evidence link:
**Note: Self-Review is not Independent Review. Record actual Builder work with traceable evidence.**
Bot Summary, native GitHub Review and Human Approval are distinct.
```

**Add new section** (after Self-Review):
```
## Fresh-Context Challenge (if applicable for L2/L3)
Trigger Reason: [Why challenge is needed]
Execution Method: [How it was performed]
Results: [Outcomes and implications]
Status: [COMPLETE / PENDING / NOT APPLICABLE]
```

**Add new section** (for L2/L3):
```
## Human Approval (L2/L3 only)
Plan Pre-Implementation Commit: [SHA or "NOT APPLICABLE"]
Human Plan Approval Reference: [Issue comment, date, scope]
Human L3 Specific Action Authorization (if applicable): [Issue comment, scope]
```

**Keep unchanged**:
- Purpose, Issue fields
- Risk classification (L0/L1/L2/L3)
- Verification section
- Status / Merge authorization notes

### 4.2 NOT In Scope

- No new files outside records/ISSUE-9/.
- No modification to GOVERNANCE.md L0–L3 definitions, Plan/Result rules, Human approval boundaries, CI checks, Draft/Ready/Merge authorization, or Rollback strategy.
- No AGENTS.md bullets 2–3, 5, 7–13.
- No GitHub Workflows, Actions, Rulesets, Secrets, or Branch Protection edits.
- No Auto-Merge, Pages deployment, or new Apps.
- No Agent Handoff, Review Bot, or governance platform infrastructure.
- No modification of Issue #4 records or other existing docs/code.

---

## 5. Detailed Reconciliation: Current (v1) → Proposed (v2)

| Aspect | v1 (Current) | v2 (Proposed) | Action | Rationale |
|--------|--------------|---------------|--------|-----------|
| **Builder Role** | Codex & Claude Code peers | Claude Code single daily Builder | MODIFY GOVERNANCE.md L1–2, AGENTS.md L1 | Simplify; reduce overhead |
| **Cross-Agent Review** | Mandatory L1–L3; blocks if absent | Removed as mandatory gate | MODIFY GOVERNANCE.md L20, L29–43, AGENTS.md L4 | Streamline; maintain verification via evidence |
| **Self-Review** | Not explicitly defined | Explicit: Source/Claim/Method/Evidence/Commit SHA; ≠ Independent | MODIFY GOVERNANCE.md L29–43, AGENTS.md L4, PR Template | Strengthen traceability |
| **L0 Rules** | No Plan/Result/Review required | No Plan/Result/Review required | KEEP GOVERNANCE.md | No change |
| **L1 Rules** | "Cross-Agent Review 不同 Agent" | "Claude Code Self-Review + Evidence" | MODIFY GOVERNANCE.md L20 | Clearer responsibility |
| **L2 Rules** | "L1 + Plan/Result + Human approval" | "L1 (Self-Review) + Plan/Result + Human approval" | MODIFY GOVERNANCE.md L23 | Maintain control |
| **L3 Rules** | "L2 + Human action auth" | "L2 + Human action auth + optional Challenge" | MODIFY GOVERNANCE.md L25, add Challenge section | Proportional verification |
| **Fresh-Context Challenge** | Not defined | Optional, per Plan; Claude Code evaluates necessity | ADD GOVERNANCE.md, AGENTS.md, PR Template | New v2 mechanism |
| **Evidence Definition** | Generic "可追溯交叉 Review" | Explicit chain: Source/Claim/Method/Evidence/Commit SHA | MODIFY GOVERNANCE.md, AGENTS.md, PR Template | Clearer standards |
| **Issue Template** | Exists (PR #6); dual-Agent language | Exists; update to Single-Builder language | MODIFY .github/ISSUE_TEMPLATE/01-agent-task.yml | Reflect role change |
| **PR Template** | "Opposite Agent Review" field | "Builder Self-Review & Verification" + Fresh-Context Challenge section + Human Approval (L2/L3) | MODIFY .github/PULL_REQUEST_TEMPLATE.md | Reflect single-Builder model |
| **Draft/Ready/Merge** | Unchanged | Unchanged | KEEP | No change |
| **Rollback** | Unchanged | Unchanged | KEEP | No change |
| **Records** | Unchanged | Unchanged | KEEP | No change |
| **CI / Tests** | Governance Tests (15/15 PASS), MkDocs strict | Same CI + optional Challenge per Plan | KEEP | No change |
| **Human Authority** | Full (Sole admin) | Full (Sole admin) | KEEP | No change |

---

## 6. Implementation Sequence (Awaiting Approval)

**Only after Human explicitly approves this Plan v2:**

| # | Files | Commit Message | Notes |
|---|-------|-----------------|-------|
| 1 | records/ISSUE-9/PLAN.md | docs: plan LIGHT Governance v2 — Claude Code Single-Builder (Issue #9) | This Plan v2, committed first |
| 2 | GOVERNANCE.md, AGENTS.md | refactor: adopt LIGHT Governance v2 — Claude Code Single-Builder (Issue #9) | Core policy changes |
| 3 | .github/ISSUE_TEMPLATE/01-agent-task.yml, .github/PULL_REQUEST_TEMPLATE.md | chore: update GitHub templates for v2 Single-Builder model (Issue #9) | Template language alignment |
| 4 | records/ISSUE-9/RESULT.md | docs: record LIGHT Governance v2 implementation results (Issue #9) | After CI pass + Human approval |

**Co-authored**: Copilot <223556219+Copilot@users.noreply.github.com>

---

## 7. Verification Strategy

### Pre-Implementation (Human Review)
- [ ] Plan v2 logically complete; addresses Issue #9 WHAT/WHY/AC.
- [ ] Four-file scope bounded; no unintended side effects.
- [ ] L3 risk justified; L0–L3 control preserved.
- [ ] Self-Verification mechanism (Source/Claim/Method/Evidence/Commit SHA) adequate for L1+ without Cross-Agent review.
- [ ] Fresh-Context Challenge optional mechanism clearly defined.

### Implementation (Claude Code, post-approval)
- [ ] GOVERNANCE.md lines 1–2, 20, 23, 25, 29–43 modified correctly.
- [ ] AGENTS.md bullets 1, 4 modified; new bullet 4a added; others unchanged.
- [ ] 01-agent-task.yml descriptions updated; four mandatory fields preserved; no Scope field added.
- [ ] PULL_REQUEST_TEMPLATE.md: "Opposite Agent" → "Builder Self-Review"; Fresh-Context Challenge section added; Human Approval (L2/L3) section added.
- [ ] No syntax errors (YAML, Markdown).
- [ ] git diff --check PASS (no trailing whitespace).

### CI & Build (Automated)
- [ ] Governance Tests workflow: PASS (existing tests validate policy structure).
- [ ] MkDocs strict build: PASS.
- [ ] records/ISSUE-9/PLAN.md precedes all implementation commits.
- [ ] No git history rewriting; clean linear progression.

### Manual Verification (Human or Claude Code)
- [ ] Four files reviewed for semantic correctness.
- [ ] L2/L3 risk control verified (Plan + Human approval + Evidence + Challenge).
- [ ] Self-Verification definition clear; no false Independence claims.
- [ ] Issue template aligns with v2 language.
- [ ] PR template properly reflects Builder role.

### Post-Merge (Future)
- [ ] New Issues submitted via updated template.
- [ ] First L1+ PRs demonstrate Self-Review + Evidence correctly.
- [ ] No blockers from governance policy change.
- [ ] L2/L3 tasks reference Plan/Result structure correctly.

---

## 8. Acceptance Criteria (Issue #9)

✓ Baseline:
- [x] Current main verified (HEAD a252261; PR #6 merged).
- [x] Four files confirmed to exist.

⏳ Awaiting Approval:
- [ ] Human **explicitly approved this Plan v2** with exact four-file scope.
- [ ] GOVERNANCE.md revised to Claude Code Single-Builder + Self-Verification.
- [ ] AGENTS.md reflects Claude Code Builder role; Self-Review ≠ Independent Review.
- [ ] .github/ISSUE_TEMPLATE/01-agent-task.yml updated to Single-Builder language (MODIFY, not CREATE).
- [ ] .github/PULL_REQUEST_TEMPLATE.md: "Opposite Agent" changed to "Builder Self-Review"; Fresh-Context Challenge & Human Approval sections added.
- [ ] L0–L3, Plan/Result, Human approval, CI, Evidence, Rollback consistent; L2/L3 cannot default-pass.
- [ ] Four-file scope maintained; no platform provisioning.
- [ ] Implementation produces real Results & verification; no blockers.
- [ ] Draft PR maintained until all conditions met.

---

## 9. Rollback Strategy (F-03 Corrected)

**Principle**: Preserve history and evidence; no deletion or force push.

**If implementation fails or requires reversal:**

1. **Standard Revert PR Workflow** (no force push, no history deletion):
   - Create authorized Revert PR (by Human or authorized Builder).
   - Revert only policy/template commits (Commits 2–3).
   - Result/PLAN.md preserved in history as evidence of attempt.
   - Apply same CI & governance verification as forward commits.
   - Human explicitly authorizes Revert PR Merge.

2. **Historical Integrity**:
   - Original PLAN.md, RESULT.md, Issue #9 Timeline, Commit history remain unchanged.
   - Revert commit message references original failed commits (e.g., "Revert cdab0f8…").
   - Rollback reason documented in Issue #9 (new comment or Result Addendum).
   - Future readers can trace: attempt → failure → revert.

3. **Issue Disposition**:
   - If partial rollback: Issue #9 remains OPEN; plan next revision.
   - If full rollback: Label "GOVERNANCE-ROLLBACK-COMPLETED" + summary comment; update records/ISSUE-9/RESULT.md with "Rollback Completed: [date], Reason: [summary]".

4. **Prohibited**:
   - No force push, `git reset --hard`, history rewrite, or deletion of PLAN/RESULT/Timeline.
   - No retroactive modification of PLAN (falsifying evidence).
   - No automated rollback or Auto-Merge on revert.

**Example Revert Commit Message**:
```
Revert: LIGHT Governance v2 implementation (Issue #9)

This reverts commits cdab0f8, [impl-commit-2], [impl-commit-3].

Reason: [specific technical or governance reason]
References: Issue #9, original PLAN.md at [commit SHA]

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>
```

---

## 10. Human Decisions Required (7 Items)

| # | Decision | Question | Options |
|---|----------|----------|---------|
| 1 | Plan Approval | Does Plan v2 align with Issue #9 intent? Is four-file scope correct? Do proposed changes achieve goal without weakening L2/L3 control? | Approve / Request Revisions / Reject |
| 2 | Self-Verification Framework | Is Source/Claim/Method/Evidence/Commit SHA sufficient for L1+ without Cross-Agent review? | Accept / Revise Requirements |
| 3 | Fresh-Context Challenge | Should be optional (RECOMMEND) or mandatory for L2/L3? Trigger & authority? | Optional (per Plan) / Mandatory (specify) |
| 4 | Cross-Agent Review Removal | Acceptable trade-off? Any conditions or mitigations? | Approve / Add Conditions / Reject |
| 5 | Template Updates | Are Issue template & PR template proposed changes suitable? | Approve / Revise / Reject |
| 6 | Implementation Authorization | Once Plan v2 approved, authorize Claude Code to proceed? Pre-implementation conditions? | Authorize / Add Conditions / Require More Approval |
| 7 | Merge Authorization | After implementation & CI pass, authorize PR Merge? Prerequisites? | Authorize (conditional) / (unconditional) / Defer |

---

## 11. Revision History

| Date | Revision | Status | Summary |
|------|----------|--------|---------|
| 2026-11-06 12:xx | Plan v1 | CHANGES REQUESTED | Incorrectly claimed 01-agent-task.yml does not exist; did not verify current main HEAD (corrected in v2) |
| 2026-11-06 11:29 | Plan v2 | PENDING HUMAN APPROVAL | Corrected v1: verified main HEAD cdab0f8; Issue template confirmed MODIFY; refined Self-Verification; issued to Issue #9 Timeline |
| 2026-11-06 11:37 | Plan v3 (Current) | PENDING HUMAN APPROVAL | Incorporated F-01 to F-06 feedback: corrected template line counts, clarified commit sequence, fixed Rollback strategy, distinguished transition from cross-Agent review, enhanced verification specs, added Dual Persistence rule |

---

## 12. NEW: Formal Plan Dual Persistence Rule (v3 Addition)

**Issue**: Learning Hub requires strong evidence trails for governance policies. Plan fallback to session storage or PR descriptions lacks persistent, queryable history.

**Rule: Whenever Formal Plan exists, both Repository Records and GitHub Issue Timeline persistence are mandatory.**

### A. Repository Records Requirement

**Location**: `records/ISSUE-<number>/PLAN.md`

**Requirements**:
- Explicit version (v1, v2, v3, etc.) and date.
- Current commit SHA (immutable reference).
- Plan must be committed **before** corresponding implementation.
- Human Approval (L2/L3) must precede implementation commits.
- Revision history preserved; no retroactive Plan falsification.

**Why**:
- Git log provides auditable history of policy development.
- Commit SHA immutable; linked from Timeline guarantees historical accuracy.
- Future readers/auditors can verify: when was this Plan written, by whom, and what was approved.

### B. GitHub Issue Timeline Requirement

**Location**: Issue #9 comment (independent comment, not buried in PR description)

**Timing**: Posted when Formal Plan ready for Human review (not on every draft revision; consolidate final version before posting).

**Minimum Content**:
- **Plan Version** (e.g., "Formal Plan v3")
- **Status** (DRAFT / PENDING HUMAN APPROVAL / APPROVED / IMPLEMENTATION IN PROGRESS / COMPLETED)
- **Fixed Commit SHA** reference (e.g., "records/ISSUE-9/PLAN.md @ commit cdab0f8")
- **Complete link** (e.g., `https://github.com/.../blob/cdab0f8/records/ISSUE-9/PLAN.md`)
- **Scope summary** (2–3 bullet points: what files change, goal)
- **Human Decisions Required** (link or inline list)
- **Version progression** (if v2/v3: "v1 had [issue]; v2 corrected to [X]; v3 adds [Y]")

**Why**:
- GitHub Timeline is the official audit trail for Issues.
- Timeline leaves permanent history of Plan evolution.
- Fixed Commit SHA prevents "moving target" problem (main branch updates).
- Future Issues can reference prior governance decisions by Timeline comment.

### C. Remote Readback Verification (F-05 Enhanced)

**Post-commit requirement**: After pushing Plan to main, verify both persistence locations are live.

**Readback Checklist**:
- [ ] `git log origin/main --oneline | head -5` shows Plan commit in last 5.
- [ ] `curl` or GitHub API confirms records/ISSUE-9/PLAN.md exists at commit SHA.
- [ ] Issue #9 Timeline shows Plan comment with fixed SHA link.
- [ ] Plan Version, Status, and Scope in Timeline match Records PLAN.md.
- [ ] No redirect or "file not found" when accessing fixed commit link.

**Declaration**: Only after both checks pass:
```
PLAN PERSISTENCE VERIFIED (Records + Timeline)
- Records: [commit SHA]
- Timeline: Issue #9 comment [comment URL]
```

**Clarification**: This ≠ PLAN APPROVED (approval is Human decision).

### D. Applicability

**Applies to**:
- L2/L3 Formal Plans (mandatory by current GOVERNANCE.md).
- L0/L1 Formal Plans (if Builder chooses to create one; no mandatory Plan for L0/L1).

**Does NOT apply to**:
- Session storage, scratch files, or local drafts (reference only).
- PR descriptions or PR body content (too volatile; may be edited/closed).
- Meeting notes or chat history (unless explicitly formalized as records).

### E. Merge of New Plans

**If newer Plan version exists**:
- Old Timeline comments remain (evidence).
- New Plan comment includes cross-reference: "v2 supersedes v1; see comment #XYZ".
- Do NOT delete old Timeline comments.
- records/ISSUE-9/PLAN.md updated with new version; Git history preserves all versions.

---

## Appendix A: Self-Review vs. Independent Review (v2 Definition)

### Self-Review (Claude Code Builder)
- **Who**: Claude Code performing Implementation & Self-Review.
- **Requirement**: Must cite **Source (what code/doc changed) / Claim (what should be verified) / Method (how tested) / Evidence (results/logs/diffs) / Commit SHA**.
- **Record**: In PR as "Builder Self-Review & Verification" section with full evidence chain.
- **No claim to independence**: Clearly marked as Self-Review.
- **When mandatory**: L1–L3 (alongside other checks).
- **Fail condition**: If evidence chain incomplete or inconclusive, keep PR Draft; escalate to Human.

### Independent Review (Optional, L2/L3)
- **Who**: Separate human or agent with no conflict of interest.
- **Requirement**: Actual independent execution; proof of distinct identity.
- **Status**: Optional in v2; not mandated as gate.
- **When invoked**: Fresh-Context Challenge per Plan, or explicit Human requirement.
- **Not available**: No false "Independent Review PASS" claim; issue stays open.

### Fresh-Context Challenge (v2 Optional Mechanism)
- **When triggered**: L2/L3 tasks with high uncertainty or novel risk.
- **How evaluated**: Claude Code assesses necessity per Plan; Human may mandate.
- **Execution**: May involve external expert review, adversarial testing, or deeper verification.
- **Evidence**: Recorded in RESULT.md with clear scope and findings.
- **Failure handling**: If Challenge blocks, update RESULT.md, keep PR Draft, escalate to Human.
- **NOT Agent Handoff**: Remains Builder responsibility; no autonomous new Agent created.

---

**END OF PLAN v3 (Formal Revision)**

**PLAN STATUS**: PENDING HUMAN APPROVAL — NO IMPLEMENTATION AUTHORIZED

**GOVERNANCE IMPLEMENTATION**: NOT AUTHORIZED

**READY / MERGE / DEPLOYMENT**: NOT AUTHORIZED

---

## Next Steps (Human Review)

1. Review records/ISSUE-9/PLAN.md in full (this document).
2. Review Issue #9 comment with Plan v3 summary (to be posted).
3. Address 7 Human Decisions Required (Section 10).
4. Provide explicit approval or revision requests.
5. Upon approval, Claude Code proceeds with 4-commit implementation sequence.
6. Upon implementation completion, Claude Code issues RESULT.md for verification.
7. Human authorizes Merge after CI pass and Result review.

