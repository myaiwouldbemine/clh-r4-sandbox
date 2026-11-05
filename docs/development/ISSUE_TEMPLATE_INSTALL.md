# Copy Learning Hub — GitHub Issue Form (v2)

Human Defines Requirements; Agents Execute; Trusted Gates Enforce.

## Fields

| Field | Required |
| --- | --- |
| WHAT | Yes |
| WHY | Yes |
| Acceptance Criteria | Yes |
| Boundary | Yes |
| References / Evidence | No — may be left blank |

Human Owners describe requirements, reasons, verifiable outcomes and boundaries. They do not select L0–L3 or choose Claude Code versus Codex. Risk Level, Execution Preference and Governance Acknowledgement inputs have been removed.

## Installation and publication (WSL)

The files are `.github/ISSUE_TEMPLATE/01-agent-task.yml` and `.github/ISSUE_TEMPLATE/config.yml`. Keep the existing config unchanged. Work on `feat/CLH-002-issue-template`, preserve commit `91662af`, push the branch and open a Draft PR targeting `main`. Do not push directly to main. This branch starts directly from main and does not require PR #1, #3 or #5 to be merged; do not import their changes.

If installing in another checkout, copy the two YAML files to those same paths. Validate the actual installed files:

```bash
python - <<'PY'
from pathlib import Path
import yaml
for p in sorted(Path('.github/ISSUE_TEMPLATE').glob('*.yml')):
    d = yaml.safe_load(p.read_text(encoding='utf-8'))
    assert isinstance(d, dict)
    if p.name != 'config.yml':
        assert all(k in d for k in ('name', 'description', 'body'))
        fields = [x for x in d['body'] if x['type'] != 'markdown']
        assert [x['id'] for x in fields] == ['what', 'why', 'acceptance', 'boundary', 'references']
        assert [x['validations']['required'] for x in fields] == [True, True, True, True, False]
    print('PASS', p)
PY
git diff --check
git status --short --branch
```

The command requires PyYAML; YAML parsing and these assertions do not replace GitHub Issue Forms schema validation. Record unavailable checks as NOT RUN.

The form becomes available after an authorized merge into the default branch. Until then, the Draft PR is the review surface; it does not publish the form. Keep this task's PR as Draft; review and applicable Policy Gates remain required before any future Ready/Merge transition.

## Using GitHub New Issue

After publication, open GitHub > Issues > New issue and choose `Agent Task｜自動化開發任務`. Fill in WHAT, WHY, Acceptance Criteria and Boundary. Add References / Evidence when useful, or leave it blank, then submit. The existing config disables blank issues and presents the structured intake.

## Agent-driven workflow and LIGHT Governance v1.0

Claude Code and Codex are peer Agents. Default Intake Risk is L0, but the Agent must reassess risk from actual changes and impact, including scope changes. The form is intake only and grants no Merge or high-risk operation authorization.

- L0 does not mandate a Formal Plan, Records or Independent Review.
- L1 requires applicable validation and trusted Independent Review. Self-review or a shared GitHub account does not establish reviewer independence.
- L2 requires a Formal Plan and Human Plan Approval before implementation.
- L3 prohibits Auto-Merge by default; exceptions require specific Human Authorization.

Agents assess risk, prepare any required Formal Plan and obtain applicable approval before implementation. When a Formal Plan is needed, commit it separately before implementation; do not create retrospective plan evidence. Open a Draft PR early to track implementation, continuous validation, evidence and progress. Draft status does not authorize implementation or Merge. Complete implementation and applicable validation, then obtain required Review and Policy Gate results. Merge is permitted only under the applicable authorization conditions.

## Automation status and limits

This change supplies an intake interface only. It does not enable an Issue Dispatcher, automatic agent assignment, trusted Independent Review, Guarded Auto-Merge or deployment. Formal production Guarded Auto-Merge is not enabled. Auto-Merge is allowed only after trusted Policy Gates pass and the capability has been formally enabled under separate authorization. Do not treat a submitted form, Draft PR, label or Agent assertion as authorization or trusted gate evidence.
