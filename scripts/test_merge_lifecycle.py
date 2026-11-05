from dataclasses import replace
import unittest
from merge_lifecycle import State, ready_blockers, merge_blockers

class LifecycleTests(unittest.TestCase):
    def setUp(self):
        self.ok = State(draft=False, implementation_complete=True,
            verification_complete=True, authorization_valid=True,
            checks=("success",), evidence_current=True, material_change_reassessed=True)
    def test_l0_no_records_or_reviewer(self):
        self.assertEqual(merge_blockers(self.ok), [])
    def test_draft_blocks_even_all_checks_pass(self):
        self.assertIn("draft", merge_blockers(replace(self.ok, draft=True)))
    def test_unfinished_cannot_be_ready(self):
        for key in ("implementation_complete", "verification_complete"):
            self.assertTrue(ready_blockers(replace(self.ok, **{key:False})))
    def test_formal_plan_needs_result(self):
        self.assertTrue(ready_blockers(replace(self.ok, formal_plan=True)))
    def test_l2_l3_require_plan_approval(self):
        for risk in (2, 3):
            self.assertIn("plan not authorized", ready_blockers(replace(self.ok, risk=risk, records_complete=True)))
    def test_l1_review_unavailable_blocks(self):
        self.assertIn("independent review incomplete", merge_blockers(replace(self.ok, risk=1)))
    def test_ci_fail_closed(self):
        for checks in ((), ("pending",), ("skipped",), ("cancelled",), ("failure",), ("success", "pending")):
            self.assertTrue(merge_blockers(replace(self.ok, checks=checks)))
    def test_blockers_and_stale_evidence(self):
        for key,value in (("blocking_review",True), ("authorization_valid",False),
                          ("evidence_current",False), ("material_change_reassessed",False)):
            self.assertTrue(merge_blockers(replace(self.ok, **{key:value})))

if __name__ == "__main__": unittest.main()
