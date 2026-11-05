"""Pure lifecycle decision helper; input must come from trusted collectors.
Not an authentication layer and not a production merge executor.
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
    authorization_valid: bool = False
    review_complete: bool = False
    blocking_review: bool = False
    checks: tuple = ()
    evidence_current: bool = False
    material_change_reassessed: bool = False

def ready_blockers(s):
    reasons = []
    if s.risk not in range(4): reasons.append("unknown risk")
    if not s.implementation_complete: reasons.append("implementation incomplete")
    if not s.verification_complete: reasons.append("verification incomplete")
    if (s.formal_plan or s.risk >= 2) and not s.records_complete:
        reasons.append("records incomplete")
    if s.risk >= 2 and not s.plan_authorized: reasons.append("plan not authorized")
    return reasons

def merge_blockers(s):
    reasons = ready_blockers(s)
    if s.draft: reasons.append("draft")
    if not s.authorization_valid: reasons.append("authorization missing or invalid")
    if not s.checks or any(c != "success" for c in s.checks):
        reasons.append("checks not all successful")
    if s.risk >= 1 and not s.review_complete: reasons.append("independent review incomplete")
    if s.blocking_review: reasons.append("blocking review")
    if not s.evidence_current: reasons.append("stale evidence")
    if not s.material_change_reassessed: reasons.append("scope/risk not assessed")
    return reasons
