# On-demand Revision Self-Review

Builder: Codex (sole accountable Builder, no delegation). Date: 2026-11-07 Asia/Taipei.
Reviewed implementation head: `c37275eb05dd80574fd482b3a9a9fc7ee1db66ed`.
Reviewed main/base: `7e530cdc818044ae4f760a021a331f888f993e43`.
Revision comparison starts at `bb577319ba003f3b92ef4fc7cf0cd717e8315cac`.
Final records-only head is rechecked in PR #21 after commit/push/CI. This is actual Builder Self-Review, not independent Human review, native APPROVED or identity attestation.

## Claim / Source / Method / Evidence

| Claim | Source | Method | Evidence / verdict |
|---|---|---|---|
| On-demand, no extra key/token prerequisite | Human architecture comment 6698471618 and current chat | Read every changed workflow, entrypoint and operational document; search credential/trigger references | Inert hosted jobs, no schedule/Issue/workflow_run trigger; native Pages token only; normal Plan/implementation push using existing gh; PASS |
| Gates preserved | GOVERNANCE/AGENTS 08–14, main native rules | Read full lifecycle before/after; live preflight/settings; injected CI/race/permission/archive failures | 68 tests; protection unchanged; incomplete real PR check blocks; PASS locally/read-only, live merge NOT RUN |
| Interruption recovery | Architecture Plan sections 8–11 | Trace pre/post merge, archive-write and lost-close response; lock contention/release tests; remote-state rereads | Existing merge SHA/archive reused, failures keep Issue open; local PASS, live interrupted mutation NOT RUN |
| Publication bound to SHA | Pages workflow/lifecycle | Inspect dispatch inputs, main guard, strict build, artifact marker, native OIDC, run validation and remote byte mock | Wrong bytes stop archival; local PASS; real Pages NOT RUN |
| History/order | User preservation requirement | Blob compare 41 existing records/archive files and #19 remote head; separate Plan push/readback before implementation | PASS; named revision order final check after Result commit |
| Scope and content ownership | Issue #20 WHAT/WHY/DONE/boundary and revision request | Entire 18-file implementation diff and new records read; no educational edits/settings changes | PASS, complete lifecycle acceptance remains blocked, no complete=true block |

## Findings handled

1. Hosted scheduler/scanner could operate on unrelated PRs in local context: remove broad reconcile command; require explicit target/full SHAs.
2. Ready introduced a validation window: reread head/base/PR/Issue and CI/reviews afterward. SHA-bound API/native protections remain authoritative.
3. Comment-only deployment evidence could be stale: independently validate run and fetch remote deployment bytes before archival.
4. Changes during archive could close new requirements: recheck Issue digest and PR evidence before closure.
5. Concurrent local commands: common-Git-dir OS advisory lock, fail closed on contention, release on exit. No distributed-lock claim.
6. Literal disabled condition lint warning and acceptance heading mismatch corrected without weakening gates or rewriting Plan history (see Result).
7. Legacy standalone final_findings assertions were already obsolete at revision start; preserve reported FAIL and document replacement coverage rather than fake PASS.

## Bilingual semantic review

Read all 15 pairs both directions for actor, obligation, prohibition and condition. Clauses 02–13 and 15 are byte-unchanged from the paired prior version. Clause 01 adds the same Human starts-local-Agent condition in both languages and retains complete autonomous engineering authority without repeated approvals. Clause 14 adds identical on-demand availability, existing separate App/gh authentication, no additional named keys, local prerequisites and reread-before-resume/no-double-merge obligations in both languages. Existing missing-prerequisite blocker, Human stop and tested revert requirements remain in both. All 15 paired sections present; this is semantic Builder judgment, not an automated translation proof.

## Verdict / limitations

Implementation candidate and applicable local tests PASS; full live lifecycle **BLOCKED**. Keep PR Draft/Issue open. No finding justifies bypassing required CI or the explicit no-Merge/no-Deploy/no-Close task boundary. New head/base needs revalidation; final records head will be bound in PR. Fresh-Context Challenge omitted: user did not require delegation, and current review uses full source tracing, injected negative transitions, real read-only state and preservation tests. No independent review is claimed.

Build PASS; educational content/provenance unchanged; visual NOT RUN; deployment NOT RUN. Residual limitations: WSL/Linux local lock, no cross-machine atomic archive creation, no atomic REST expected-base CAS, comments need Builder semantic reading, candidate workflow not installed on main and actual mutation permissions not exercised.
