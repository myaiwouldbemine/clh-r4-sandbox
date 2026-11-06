# Copy Learning Hub — GitHub Issue Form

## Purpose

Collect work requests with four required fields (**WHAT**, **WHY**, **Acceptance Criteria**, **Boundary**) and one optional field (**References / Evidence**). Human describes the desired outcome and boundaries; Codex and Claude Code are peer Agents.

## Publication

The form lives at `.github/ISSUE_TEMPLATE/01-agent-task.yml` and its configuration at `.github/ISSUE_TEMPLATE/config.yml`. It becomes available from GitHub **Issues → New issue** only after this PR is reviewed, authorized and merged into the default branch. The configuration deliberately disables blank issues (`blank_issues_enabled: false`).

Before merge, validate the YAML syntax and GitHub Issue Forms schema. Verify the form has exactly five textarea IDs: `what`, `why`, `acceptance`, `boundary`, `references`, with required flags `true, true, true, true, false`. After an authorized merge, check actual GitHub New Issue rendering; do not claim UI validation before publication.

## Minimal Governance

Follow the current `GOVERNANCE.md` and `AGENTS.md` on `main`, not historical LIGHT platform designs:

- L0 is strictly nonsemantic formatting or typo changes; applicable checks still apply. Risk is **assessed from actual impact**, not a default L0 intake classification.
- L1 requires applicable validation and a traceable review by the opposite Agent.
- L2 requires an approved **pre-implementation Plan**, a post-implementation Result, and opposite-Agent review.
- L3 adds Human authorization for the specific governance, permission, security, deployment or other high-risk action.
- Draft PR does not authorize work or Merge. Check CI, Review, blockers and operation authorization before Merge. Agent summaries, native GitHub Reviews and Human approval are different evidence types.

This Issue Form is **intake only**. It does not enable issue dispatch, automated reviewer identity verification, trusted Policy Gates, Auto-Merge or deployment. Merging and Pages deployment require separate authorization. Archived governance platform and Canary plans remain inactive.

## Validation boundary

YAML syntax/schema checks and Pull Request CI do not demonstrate browser-rendered issue form behavior. Record any test that was not executed as **NOT RUN**.
