from dataclasses import replace
import unittest
from merge_lifecycle import State, ready_blockers, merge_blockers


class LifecycleTests(unittest.TestCase):
    def setUp(self):
        self.ok = State(draft=False, implementation_complete=True,
            verification_complete=True, merge_authorized=True,
            checks=("success",), evidence_current=True, material_change_reassessed=True)
        self.reviewed = replace(self.ok, risk=1, builder="codex", reviewer="claude",
            review_complete=True, review_reference="https://example.invalid/pr/review",
            head="a"*40, reviewed_head="a"*40)

    def test_l0_no_plan_result_or_review(self):
        self.assertEqual(merge_blockers(self.ok), [])

    def test_l1_both_cross_review_directions(self):
        self.assertEqual(merge_blockers(self.reviewed), [])
        self.assertEqual(merge_blockers(replace(self.reviewed, builder="claude", reviewer="codex")), [])

    def test_l1_missing_self_unknown_or_untraceable_review_blocks(self):
        for changes in ({"review_complete":False}, {"reviewer":"codex"},
                        {"reviewer":"unknown"}, {"review_reference":""},
                        {"review_reference":" "}, {"reviewed_head":"b"*40}):
            with self.subTest(changes=changes):
                self.assertTrue(merge_blockers(replace(self.reviewed, **changes)))

    def test_l2_requires_records_and_human_plan(self):
        state = replace(self.reviewed, risk=2)
        self.assertTrue(merge_blockers(state))
        self.assertTrue(merge_blockers(replace(state, records_complete=True)))
        self.assertEqual(merge_blockers(replace(state, records_complete=True, plan_authorized=True)), [])

    def test_l3_requires_specific_action_beyond_plan(self):
        state = replace(self.reviewed, risk=3, records_complete=True, plan_authorized=True)
        self.assertIn("Human specific action approval missing", merge_blockers(state))
        self.assertEqual(merge_blockers(replace(state, action_authorized=True)), [])

    def test_human_approval_cannot_replace_agent_review(self):
        for risk in (2, 3):
            self.assertTrue(merge_blockers(replace(self.ok, risk=risk,
                records_complete=True, plan_authorized=True, action_authorized=True)))

    def test_merge_operation_is_separate_from_content_approval(self):
        self.assertTrue(merge_blockers(replace(self.reviewed, merge_authorized=False)))

    def test_draft_blocks_all_levels(self):
        for risk in range(4):
            state = replace(self.reviewed, risk=risk, records_complete=True,
                plan_authorized=True, action_authorized=True, draft=True)
            self.assertIn("draft", merge_blockers(state))

    def test_unfinished_cannot_be_ready(self):
        for key in ("implementation_complete", "verification_complete"):
            self.assertTrue(ready_blockers(replace(self.ok, **{key:False})))

    def test_voluntary_formal_plan_requires_result(self):
        self.assertIn("records incomplete", ready_blockers(replace(self.ok, formal_plan=True)))

    def test_ci_fail_closed(self):
        for checks in ((), ("pending",), ("skipped",), ("cancelled",),
                       ("failure",), ("success", "pending"), ("unknown",)):
            self.assertTrue(merge_blockers(replace(self.ok, checks=checks)))

    def test_blockers_and_base_scope_evidence_not_confirmed(self):
        for key, value in (("blocking_review", True), ("blocking_review", None),
                           ("evidence_current", False), ("material_change_reassessed", False)):
            self.assertTrue(merge_blockers(replace(self.reviewed, **{key:value})))

    def test_unknown_risk_fails_closed(self):
        for risk in (-1, 4, True, None, "0"):
            self.assertEqual(merge_blockers(replace(self.ok, risk=risk)), ["unknown risk"])


if __name__ == "__main__":
    unittest.main()
