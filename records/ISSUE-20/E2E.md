# E2E Verification — Issue #20

Implementation tested: `445e707e9ed67e6c89cf7bac2240ee5886026b95`, based on main `7e530cdc818044ae4f760a021a331f888f993e43`.

**Overall: BLOCKED. No hosted Agent or real autonomous lifecycle has been run.** Missing OPENAI_API_KEY and CLH_AUTOMATION_TOKEN; activation variable absent; candidate workflows remain in Draft PR #21. No simulated test is a real GitHub E2E PASS.

| # | Requested acceptance scenario | Local / repository evidence | Real GitHub E2E status |
|---|---|---|---|
| 1 | Issue starts Agent | Owner engineering trigger, pinned action, credential preflight implemented | BLOCKED — provider/transport unavailable, candidate not installed on main |
| 2 | Agent implements and opens PR | Real local Git bundle publish tests PASS; model execution NOT RUN | BLOCKED — this migration PR was created by interactive Codex, not an Issue-triggered runner |
| 3 | CI failure blocks merge | Injected failed/pending/missing/skipped/neutral/cancelled checks PASS; real native rules configured | BLOCKED — no live negative merge attempt; do not infer from unit tests |
| 4 | Fixed CI reenters | Fail then successful check transition PASS; failure-triggered bounded retry code | BLOCKED — no live model retry |
| 5 | Automatic Ready | State transition tests PASS, stale head/base stops before Ready | BLOCKED — migration PR remains Draft |
| 6 | Automatic merge | Exact head API test PASS, conflict/permission errors block | BLOCKED — no live merge |
| 7 | Automatic Pages | Workflow lint and strict build PASS; Pages Actions setup/readback PASS | BLOCKED — no deployment run |
| 8 | Remote deployed result | SHA marker/readback implemented; Pages status null | NOT RUN — no deployed artifact to verify |
| 9 | Evidence archived | Local archive/readback/retry/error tests PASS; migration records committed in PR | BLOCKED for autonomous live archival |
| 10 | Automatic Issue closure | Local ordering tests PASS; archive failure leaves Issue open | BLOCKED — #20 stays open |
| 11 | Duplicate events safe | Repeated merge/closure and real local Git bundle publish tests PASS | NOT RUN on real event delivery |
| 12 | Head mismatch blocks | Static and in-flight head/base mutation tests PASS | NOT RUN with a live GitHub race |
| 13 | Insufficient permission stops | Injected GitHub API errors PASS, secret response not exposed; live initial protection preflight failed closed | NOT RUN with restricted runtime credential, which is absent |
| 14 | Content ownership retained | AGENTS 03/04 and GOVERNANCE reviewed; no docs/subjects or approved educational source changed | PASS for this repository diff; model behavior not exercised |
| 15 | Chinese/English equivalent | 15 clauses checked structurally and semantically; SELF-REVIEW.md matrix | PASS for Builder Self-Review; not independent review |

## Actual remote checks and settings

Native ruleset [26702419](https://github.com/myaiwouldbemine/myaiwouldbemine-Copy-Learning-Hub/rules/26702419): main only, active, no bypass actors, PR required, zero approving reviews, resolved threads, strict docs-check/governance-tests from GitHub Actions App 15368, no force push/delete. Existing canary ruleset unchanged. Settings response/readback: MAIN-RULESET.json and SETTINGS-READBACK.json.

Pages source is workflow; HTTPS site URL configured; environment has main-only branch policy and no reviewer rule. PAGES-SETUP.json / SETTINGS-READBACK.json. **Provisioned is not deployed.** Workflow default token stays read-only; no secrets/variables added or credential scopes expanded.

Current-head PR CI run URLs and remote readback are published in PR #21 after final records commit. They prove real CI on the migration PR, not Issue-triggered engineering or deployment.

## Live test procedure once prerequisites exist

With the two credentials configured, confirm their actual access without revealing values. Confirm ruleset, Pages, disabled-by-default candidate and rollback. Install verified candidate via normal PR, then enable the one-time installation switch. Use an owner-created bounded engineering fixture importing no educational semantics. Collect its Issue, branch/PR, initial intentional failing CI, automatic repair and exact SHA checks; observe Ready/merge, applicable Pages SHA readback, archive and Issue state separately. Re-deliver events and test stale SHA/permission-denied paths without weakening main rules. Save run URLs and immutable SHAs. Mark any failure FAIL/BLOCKED and stop affected actions. Never reset/force push or loosen protections to make a test pass.
