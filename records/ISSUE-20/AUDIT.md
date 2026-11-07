# Current-State Audit — Issue #20

Audit date: 2026-11-06 Asia/Taipei. Builder: Codex. Read-only audit preceded implementation.

## Source and historical boundary

Remote main: `7e530cdc818044ae4f760a021a331f888f993e43`. Initial local branch was Issue #11 at `620b42a`; clean worktree. Migration uses a new branch from remote main.
[Issue #18](https://github.com/myaiwouldbemine/myaiwouldbemine-Copy-Learning-Hub/issues/18) and [Draft PR #19](https://github.com/myaiwouldbemine/myaiwouldbemine-Copy-Learning-Hub/pull/19) remain open, unchanged. PR head `7efb0521d63b646501b83ecafdfb40da473d914b`; its records/ISSUE-18 directory is not on main. Read its Plan v1.2, PR evidence, Issue and comments. Preserve v1.1/v1.2, bilingual implementation, Result, BILINGUAL-EVIDENCE, CI and commits in that branch; do not merge or overwrite #19 as part of this migration. Separate migration avoids conflating bilingual completion and new policy.

## Findings

| Surface | Actual finding | Enforcement / disposition |
|---|---|---|
| GOVERNANCE.md / AGENTS.md | Claude-specific Builder, L0–L3, separate Human Plan/action/merge/deploy gates | Text policy; replace under explicit current user instruction |
| README / INSTALL / Issue installation guide | Conflicting older peer-review and approval/deploy instructions | Text only; update active guidance |
| Issue form / PR template | Risk and Human approval fields; no issue runner | Text/form only; retain WHAT/WHY/DONE/boundary, remove engineering approval gates |
| docs-check.yml | PR strict MkDocs build; manual dispatch | Real read-only CI; retain |
| governance-tests.yml | PR unittest discovery | Real read-only CI; retain and add meaningful runtime tests |
| merge-and-close-pr.yml | Manual dispatch, owner allowlist, exact SHA; merge then archive/close without Pages verification | Implemented but not autonomous; replace to prevent premature closure |
| scripts/merge_lifecycle.py / archive_record_builder.py | Linkage and archive utilities, not Agent runner | Legacy helpers; preserve historical tests, do not confuse with live gates |
| scripts/verify_plan_records.py | Requires numeric risk and Human Decisions fields | Migrate record checker to engineering records without approval classification |
| Pages workflow | workflow_dispatch only | Deployment code exists, no automatic trigger |
| Pages API / repository metadata | HTTP 404; has_pages=false | Pages not provisioned; deployment BLOCKED |
| main branch protection | HTTP 404, Branch not protected | No traditional protection |
| rules/branches/main | [] | No effective main rules |
| rulesets | One active isolated Issue #4 canary, refs/heads/canary/light-enforcement-issue-4 only | Not main protection; leave unchanged |
| Actions permissions | enabled=true, allowed_actions=all; default token read; can_approve_pull_request_reviews=false | Do not silently expand defaults; runtime credentials/setup required |
| Repository metadata | allow_auto_merge=false; current gh account reports admin/write | Capability is not proof of configured automation; do not bypass |
| Actions secrets / variables | Lists empty (names only queried) | No configured provider key or automation transport token observed |
| Self-hosted runners | total_count=0 | No existing self-hosted Agent runner; hosted Actions alone is not an AI Agent |
| Archived designs | Existing C3–C5/registry/attestation material marked inactive | Preserve, do not revive or provision platform |

No secret values were requested. CLI used for settings APIs absent from connector capabilities. GitHub connector used for migration Issue creation. No settings changed during audit.

## Technical sources

- https://github.com/openai/codex-action — official action requires provider credentials; availability of Actions does not prove model access.
- https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow — GITHUB_TOKEN event recursion restrictions; ordinary automation transport must support CI/push events, or explicit dispatch must be designed.

Implementation and activation must be assessed separately. Missing runner, native main checks and Pages prevent a truthful full E2E PASS.
