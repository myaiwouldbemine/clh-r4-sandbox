"""Local checklist helper for Minimal Governance.
Inputs are assessed evidence, not authenticated facts. No network, registry,
signature verification, check publication or merge capability.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class State:
    draft: bool = True
    implementation_complete: bool = False
    verification_complete: bool = False
    formal_plan: bool = False
    records_complete: bool = False
    risk: int = 0
    plan_authorized: bool = False
    action_authorized: bool = False
    merge_authorized: bool = False
    builder: str = ""
    reviewer: str = ""
    review_complete: bool = False
    review_reference: str = ""
    head: str = ""
    reviewed_head: str = ""
    blocking_review: bool = False
    checks: tuple = ()
    evidence_current: bool = False
    material_change_reassessed: bool = False


def known_risk(risk):
    return type(risk) is int and risk in range(4)


def ready_blockers(s):
    if not known_risk(s.risk):
        return ["unknown risk"]
    reasons = []
    if s.implementation_complete is not True:
        reasons.append("implementation incomplete")
    if s.verification_complete is not True:
        reasons.append("verification incomplete")
    if (s.formal_plan or s.risk >= 2) and s.records_complete is not True:
        reasons.append("records incomplete")
    if s.risk >= 2 and s.plan_authorized is not True:
        reasons.append("Human Plan approval missing")
    if s.risk == 3 and s.action_authorized is not True:
        reasons.append("Human specific action approval missing")
    return reasons


def merge_blockers(s):
    reasons = ready_blockers(s)
    if not known_risk(s.risk):
        return reasons
    if s.draft is not False:
        reasons.append("draft")
    if s.merge_authorized is not True:
        reasons.append("merge operation not authorized")
    if not s.checks or any(c != "success" for c in s.checks):
        reasons.append("checks not all successful")
    if s.risk >= 1:
        if (s.review_complete is not True
                or {s.builder, s.reviewer} != {"codex", "claude"}
                or not isinstance(s.review_reference, str) or not s.review_reference.strip()
                or not isinstance(s.head, str) or not s.head
                or s.reviewed_head != s.head):
            reasons.append("traceable cross-Agent review incomplete")
    if s.blocking_review is not False:
        reasons.append("blocking review/comment/thread unresolved or unknown")
    if s.evidence_current is not True:
        reasons.append("stale or unconfirmed evidence")
    if s.material_change_reassessed is not True:
        reasons.append("scope/risk not assessed")
    return reasons
