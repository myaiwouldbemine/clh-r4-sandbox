# Phase A execution Plan

2026-11-07 Asia/Taipei. Accountable Builder: Codex. User explicitly authorized Phase A in the current Codex chat after reviewing commit 910c6c632ea0350eec0abf870790fed9bb1a6866. This new execution Plan supplements, never replaces, MINIMAL-LIVE-E2E-PLAN.md. No Phase B authorization.

## WHAT / WHY / DONE

Execute the reviewed isolated acceptance against real GitHub native rules, CI, Pages, HTTPS, archive and closure, then controlled fixture revert. Distinguish injected negatives from real observations. DONE means candid phase-specific Result/Evidence/Self-Review, including blockers; it does not mean CLH production PASS.

## Preflight / scope

Remote CLH #21 Draft/open, head 910c6c632ea0350eec0abf870790fed9bb1a6866; main 7e530cdc818044ae4f760a021a331f888f993e43; #19 Draft at 7efb0521d63b646501b83ecafdfb40da473d914b; #18/#20 open. Plan-head Docs and Governance CI success. Read Issue/comments, native ruleset 26702419, Pages/environment, token defaults and repository permissions. Existing gh OAuth account myaiwouldbemine has repo/workflow scopes and observed CLH admin access; actual ability to create/configure a new repository must be proven, not inferred. No credential contents copied. Connector lacks repository provisioning/settings endpoints; use existing gh for those.

Source pinned to 910c6c632ea0350eec0abf870790fed9bb1a6866 (runtime identical to reviewed implementation). New public dedicated repository clh-lifecycle-e2e-20261107-phase-a, same owner; public synthetic engineering-only content, no educational material. If name already exists, stop and investigate instead of adopting unknown resources. Only that new repo receives runtime/settings/merge/deployment writes. CLH receives additive records on existing #21 branch and appended PR status only. All old records/branches and protected main/settings unchanged.

## Ordered implementation / bootstrap

1. Commit/push/read back this Plan independently before provisioning. Save read-only preflight separately.
2. Create repo with GitHub auto-init main. Clone separately. Create bootstrap Issue, branch, independently commit its records/ISSUE-N/PLAN.md; early Draft PR. Seed minimal CI/site and reviewed runtime in normal commits. Configure equivalent main rules before any merge; first PR itself supplies required CI. This combines seed/install into one protected PR, avoiding an unprotected seed merge. If first-PR CI cannot run, BLOCKED rather than lowering protection.
3. Copy candidate runtime/pages, both inert workflow tombstones, docs/governance CI, autonomous/on-demand/agent_job tests and retired agent_job dependency. Minimal mkdocs.yml/docs/index.md/requirements.txt are synthetic site scaffolding. Record exact source hashes; dependency additions must be justified. Plan/Result records are not published site content.
4. Configure equivalent ruleset (strict docs-check/governance-tests, Actions integration, no bypass/force/delete, conversations resolved, merge-only, zero approvals), native Pages Actions/HTTPS and main-only environment. Read back full parity before candidate run. No secrets or bypass. Required local tests, strict build, workflow lint, current CI and head/base Self-Review before Ready/exact-SHA merge.
5. Bootstrap merge from pinned local executor; expected deployment-PENDING checkpoint. Dispatch installed main workflow for exact I; successful exact run, HTTPS I, archive readback then installation Issue close. Stop on unrepairable permissions or parity failure.
6. Separate fixture Issue + Draft PR, independent Plan, unique text marker implementation commit, Result, tests/current CI/Self-Review. Safe missing/pending/failing CI and stale input checks; then normal lifecycle merge M. Stop at merged/deployment-PENDING checkpoint, resume in fresh process. Exact Pages M + marker hash, archive-before-close, one duplicate replay.
7. Negative matrix covers CI failure/missing/pending, stale H/B, permission denial, duplicate, wrong deployed SHA, archive readback failure, interrupted recovery and main advancement. Prefer read-only live checks and injected actual functions; never claim mocks are live. No intentional historical corruption or permission weakening. Unexpected failure halts affected writes; evidence remains.
8. Rollback Issue/PR with independent Plan; git revert only the fixture marker commit, preserving its records. Current CI/Self-Review; protected merge R, Pages R, HTTPS R and marker 404, archive/readback/close. Retain repo/branches/evidence, no deletion.
9. Append CLH MINIMAL-LIVE-E2E-RESULT.md, MINIMAL-LIVE-E2E-EVIDENCE.json, MINIMAL-LIVE-E2E-SELF-REVIEW.md and sanitized logs. Commit/push/readback; append #21 Phase A status, keep Draft. Stop, no Phase B.

## Acceptance / evidence / validation

Use original Plan evidence contract: repo IDs/URLs, H/B/I/M/R, check/run/job IDs and URLs, source and fixture hashes, exact HTTPS body/status/time, archive ID/body/readback and closure timestamps, serialized mutation trace. All commands target explicit repository; assertions reject CLH mutation in test harness. Fresh-context challenge omitted (no mandate); direct source/state review and full trace are used, not independent review claims. Build/content/provenance/visual/deployment separated. Recheck original CLH main/#19/#18/#20/#21 and old tracked blobs before final report.

## Budget / failure / rollback

Original cap 120 minutes active execution, 20 minutes each CI/Pages, 3 attempts unchanged failure, 3 successful deployments (bootstrap/fixture/rollback), one extra dispatch only after confirmed failed/no-deploy run. No permission expansion, no settings weakening, no force/direct main push. Permission insufficiency/parity impossibility stops execution and yields BLOCKED with preserved artifacts. Main advance, SHA/archive mismatch or unknown mutation outcome requires remote readback before any retry. No blind repeat. Stop local process and inspect/cancel only isolated pending run on emergency; cancel is not rollback. Tested protected revert retains safe deployment machinery. Partial progress is not overall PASS; unexecuted phases NOT RUN. Phase B recommendation must remain no-go until separate authorization and CLH-specific validation.
