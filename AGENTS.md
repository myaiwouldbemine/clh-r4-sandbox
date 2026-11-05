# Shared Agent Instructions — LIGHT Governance v1.0

- Read GOVERNANCE.md and the Issue boundary before work. Codex and Claude Code are equal peers; assign Builder and Independent Reviewer per task.
- Human defines goals/WHY/boundaries and major decisions, not routine PR review/merge.
- Default L0; reassess actual risk. Never treat labels, PR text, self-review or a shared user account as authenticated independent approval.
- L0 needs no mandatory plan or independent review. L1+ requires independent review; unavailable/pending reviewer blocks. L2 requires Human-approved plan; L3 blocks auto-merge unless specifically authorized.
- Every formal Plan belongs in records/ISSUE-<number>/PLAN.md. L2/L3 require one. Include Goal/WHY/Scope/Boundary, Risk Level, Implementation Plan, Acceptance Criteria, Verification Strategy, Human Decisions/Authorization and Revision History.
- Commit the Plan on a traceable topic branch BEFORE implementation. Link Issue and PR. Never backfill a plan as if it existed earlier; preserve revisions and reauthorize scope expansion.
- After planned implementation, write RESULT.md beside PLAN.md: actual results, verification evidence, PR/commits, deviations, unfinished items. Pending means pending, never PASS/CLOSED.
- Use Issues/PRs/Commits/Checks as execution evidence. No mandatory ledger or step-by-step log.
- Keep build/content/provenance/visual/deployment checks distinct; report NOT RUN honestly.
- No direct main push, force push, rule bypass, or unauthorized deployment. Auto-merge is disabled until the activation package receives one Human approval and runtime verification succeeds.
- Self-review does not count as independent review. Record the actual agent identity and do not impersonate another reviewer.
- For closure, enforce all applicable gates, required Plan/Result records, risk/scope/authorization and resolved blockers. Deployment is separately authorized; do not close unfinished work.

## Draft-first lifecycle
- Human Issue input: WHAT / WHY / DONE; References optional. Builder owns investigation, risk classification and necessary planning.
- Open Draft PR early for CI, collaboration, records and progress. Commit formal Plan before implementation; L2/L3 must have necessary Plan authorization first. Draft creation grants no implementation authority.
- Run verification continuously. Mark Ready only after implementation, applicable verification and required Result record are complete.
- Drafts, pending/incomplete CI, unresolved blocking review and missing authorization cannot merge. After Ready, applicable independent review and all Policy Gates must pass.
- Material scope/risk changes after Ready require plan/review/authorization reevaluation; return to Draft when appropriate. Invalidate stale head/base evidence.
- L0 without formal Plan requires no new records or independent review. Principle: Draft Early, Verify Continuously, Review When Ready, Merge Only When Eligible.
