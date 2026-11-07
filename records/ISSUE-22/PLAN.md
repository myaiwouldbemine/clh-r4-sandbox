# Issue 22 implementation plan

Codex is the sole accountable Builder. Production base is ba3091011cb6f165ff3a483a48353b957fd141d5. Phase A and production Phase B established manual Pages and lifecycle readback. Both repositories currently pass local native protection preflight and use workflow Pages.

1. Accept main pushes and exact-SHA manual retries. Require current main, effective protection and a unique exact merged PR to main. Ordinary PRs can publish without Issue mutation. Validate declared lifecycle metadata and honor deployment applicability.
2. Serialize publication, recheck main immediately before deploy and during HTTPS verification. Keep archive and closure in the local lifecycle with independent live readback.
3. Test event selection, metadata, stale main and evidence boundaries. Run actionlint, unit tests and strict build. Exercise the candidate via protected PR in the existing Phase A repository first.
4. Record Result and exact-head/base self-review. Install through protected production PR, observe push run, check homepage and SHA over HTTPS, archive and read back before closure. Recover via exact-current-SHA retry or tested revert PR. Leave Issue open on failed acceptance.
