# On-demand Verification and E2E Matrix

2026-11-07 Asia/Taipei; Codex. Implementation `c37275eb05dd80574fd482b3a9a9fc7ee1db66ed`; main `7e530cdc818044ae4f760a021a331f888f993e43`.

**Full Live E2E: BLOCKED.** The architecture request prohibits Merge, Deploy and Issue #20 closure during this revision. No fixture repository, extra credential or unsafe write was used to manufacture acceptance. Local mocks never count as live E2E. Read-only live checks are separately identified below.

| Scenario | Local verification | Actual GitHub / live status |
|---|---|---|
| App session + existing gh | Active session and successful gh calls | PASS for observed session/repository access, no claim about internal credential provenance |
| Separate Plan publish/readback | Commit order and bytes | PASS: `51b1c2927b85d7546e59e882f8f46f0e651c75d9` pushed/read before implementation |
| Builder implementation + existing Draft PR | Normal git commits/push | PASS: continued #21, no new token or hosted model |
| Required CI | Unit 68 PASS; strict MkDocs PASS | New-head Actions run links/results in final PR; CI is distinct from lifecycle E2E |
| Failed/missing/pending/skipped/cancelled CI blocks | Injected actual gate functions PASS | NOT RUN: no destructive real negative merge attempted |
| Stale head/base / post-Ready races | Injected gates PASS | NOT RUN: no live concurrent merge race |
| Real native protection | Settings/readback and unchanged rules | PASS: live read-only preflight |
| Incomplete current PR gate | Explicit target `check` | PASS: real #21 rejects missing completed lifecycle record; Draft/open preserved |
| Permission failure | Injected merge/archive API denial PASS | NOT RUN with restricted mutation credential; no new credential installed |
| Duplicate execution / lost response recovery | Reused merge and archive; local lock PASS | NOT RUN: no real merge/archive/close performed |
| Ready / exact-SHA merge | Local state transition PASS | NOT RUN; BLOCKED by revision boundary |
| Pages dispatch / successful native deployment | Workflow lint + input/main guard inspection | NOT RUN; workflow candidate not installed on main; no deployment run/SHA |
| Published SHA mismatch | Mocked remote bytes rejection PASS | NOT RUN against a real deployed revision |
| Archive readback before closure | API sequence/corrupt readback/requirements edits PASS | NOT RUN: repository records pushed/read are not lifecycle closure archive |
| Recovery / rollback | Local retry and lock tests PASS; revert procedure reviewed | Actual revert PR/deployment NOT RUN (production unchanged) |
| Historical records / #19 | 41 blob comparisons | PASS: remote #19 unchanged Draft head; no history rewriting |
| Bilingual / content ownership | 15 pairs reviewed, only 01/14 changed | PASS for Builder Self-Review; no educational approval claimed |

Original 53-test and original E2E records remain unchanged. New tests/logs and live read-only outputs are in ON-DEMAND-REVISION-TESTS.txt and ON-DEMAND-REVISION-EVIDENCE.json. Old standalone final_findings runner returns FAIL for obsolete workflow assertions, also failing on pre-revision baseline; it is neither new lifecycle acceptance nor part of unittest discovery.

## Future live acceptance procedure (not executed)

When lifecycle execution is in scope and verified candidate is installed through normal protected PR flow, use an owner engineering task with approved non-semantic fixture content. Observe intentional failing CI before any merge, repair with current-head review, reject stale parameters and missing evidence via read-only check, then run targeted lifecycle, record Ready/merge SHA, dispatch exact main merge SHA Pages, read successful run and remote bytes, resume archive/readback/close. Record separate outcomes and test duplicate/resume safely from remote state. Native denial must stop mutations; never weaken protection or create wider tokens to demonstrate success. If deployment/main has advanced, stop and prepare a reviewed current recovery change. Actual live failure-injection constraints must be assessed then, not assumed solved now.
