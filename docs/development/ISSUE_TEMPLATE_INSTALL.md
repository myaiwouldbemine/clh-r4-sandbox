# Copy Learning Hub — GitHub Issue Form (v1)

## Files

- `.github/ISSUE_TEMPLATE/01-agent-task.yml`: WHAT, WHY, Acceptance Criteria, Boundary plus risk, references and execution preference.
- `.github/ISSUE_TEMPLATE/config.yml`: discourages blank issues; maintainers can still choose blank.

## Installation (WSL)

Copy the two `.yml` files into the same paths inside your repository. Because CLH-001 PR #1 is already open and almost complete, prefer a new `docs/CLH-002-issue-template` branch after CLH-001 is merged, then create a PR targeting `main`. Do not push directly to main.

```bash
mkdir -p .github/ISSUE_TEMPLATE
# Copy the supplied YAML files to .github/ISSUE_TEMPLATE/
python - <<'PY'
from pathlib import Path
import yaml
for p in sorted(Path('.github/ISSUE_TEMPLATE').glob('*.yml')):
    d = yaml.safe_load(p.read_text(encoding='utf-8'))
    assert isinstance(d, dict)
    if p.name != 'config.yml':
        assert all(k in d for k in ('name', 'description', 'body'))
    print('PASS', p)
PY
git diff --check
```

Once the template is merged into the default branch, visit GitHub > Issues > New issue and choose `Agent Task｜自動化開發任務`.

**Important**: An Issue Form standardizes intake only. It does not itself dispatch a coding agent, execute CI, or enable auto-merge. Those are separate CLH-002 automation requirements.
