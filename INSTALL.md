# Install Issue-Driven Autonomous Governance

Read [GOVERNANCE.md](GOVERNANCE.md), [AGENTS.md](AGENTS.md) and the [operation guide](docs/development/AUTONOMOUS_OPERATIONS.md). Human opens an engineering Issue once; no repeated Plan/Ready/Merge/Deploy/Close approval is required. Codex or Claude Code is the single accountable Builder. ChatGPT + Human retain教材創作、語義品質與核准權。

Install through a PR, never push main directly. Run `python -m unittest discover -s scripts -p 'test_*.py'`, `python -m mkdocs build --strict` and `git diff --check`. Needed Plans are committed before implementation and followed by Result.

Code installation does not configure GitHub. The operation guide lists exact provider/transport credentials, native main protection, Pages Actions source and activation-variable requirements. Keep automation disabled until those prerequisites, CI, retries and rollback are verified. Use existing permissions only; never copy local credentials, broaden scopes, bypass protections or invent an available runner.

The initial Issue #20 audit found no configured model/transport secrets, main protection or Pages. See [migration PR #21](https://github.com/myaiwouldbemine/myaiwouldbemine-Copy-Learning-Hub/pull/21) for current-head evidence and blockers. A successful build is not E2E, deployment or educational quality approval.
