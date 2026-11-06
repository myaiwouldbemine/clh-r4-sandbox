#!/usr/bin/env python3
"""
Issue #11 Merge Lifecycle Mock Tests

Tests merge gate validation, closure summary composition, idempotency.
These are MOCK tests (no real GitHub API calls).
Live tests require explicit Human authorization (not covered by this Plan).

All tests verify evidence-based, fail-closed behavior per Plan v4a2.
"""

import sys
import os
import json

# Add scripts directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from merge_lifecycle import (
    MergeAuthorizationError,
    MergeGateError,
    check_authorization,
    validate_pr_open,
    validate_sha_match,
    validate_base_branch,
    validate_ci_checks,
    validate_no_blocking_reviews,
    compose_closure_summary,
    check_prior_closure_summary,
    extract_learning_evidence,
    create_mock_pr_data,
    create_mock_check_runs,
    create_mock_reviews,
)


class TestRunner:
    """Simple test runner."""
    
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.tests = []
    
    def test(self, name, fn):
        """Run a test function."""
        try:
            fn()
            self.passed += 1
            self.tests.append((name, "✅ PASS"))
            print(f"✅ {name}")
        except AssertionError as e:
            self.failed += 1
            self.tests.append((name, f"❌ FAIL: {e}"))
            print(f"❌ {name}: {e}")
        except Exception as e:
            self.failed += 1
            self.tests.append((name, f"❌ ERROR: {e}"))
            print(f"❌ {name}: ERROR: {e}")
    
    def summary(self):
        """Print test summary."""
        print("")
        print("=" * 70)
        print(f"Test Results: {self.passed} passed, {self.failed} failed")
        print("=" * 70)
        for name, result in self.tests:
            print(f"{result} — {name}")
        return self.failed == 0


def test_authorization():
    """Test Gate 1: Authorization."""
    
    def pass_case():
        result = check_authorization("myaiwouldbemine", ["myaiwouldbemine"])
        assert result is True, "Should return True"
    
    def fail_case():
        try:
            check_authorization("unauthorized", ["myaiwouldbemine"])
            assert False, "Should raise MergeAuthorizationError"
        except MergeAuthorizationError:
            pass  # Expected
    
    pass_case()
    fail_case()


def test_pr_open():
    """Test Gate 2: PR Open."""
    
    def pass_case():
        result = validate_pr_open("open", False)
        assert result is True, "Should return True"
    
    def fail_closed():
        try:
            validate_pr_open("closed", False)
            assert False, "Should raise MergeGateError"
        except MergeGateError:
            pass  # Expected
    
    def fail_draft():
        try:
            validate_pr_open("open", True)
            assert False, "Should raise MergeGateError"
        except MergeGateError:
            pass  # Expected
    
    pass_case()
    fail_closed()
    fail_draft()


def test_sha_match():
    """Test Gate 3: SHA Match."""
    
    test_sha = "abc123def456abc123def456abc123def456abc1"
    
    def pass_case():
        result = validate_sha_match(test_sha, test_sha)
        assert result is True, "Should return True"
    
    def fail_case():
        try:
            validate_sha_match(test_sha, "different_sha12345678901234567890123456")
            assert False, "Should raise MergeGateError"
        except MergeGateError:
            pass  # Expected
    
    pass_case()
    fail_case()


def test_base_branch():
    """Test Gate 4: Base Branch."""
    
    def pass_case():
        result = validate_base_branch("main", "main")
        assert result is True, "Should return True"
    
    def fail_case():
        try:
            validate_base_branch("main", "develop")
            assert False, "Should raise MergeGateError"
        except MergeGateError:
            pass  # Expected
    
    pass_case()
    fail_case()


def test_ci_checks():
    """Test Gate 5: CI Checks."""
    
    required = ["governance-tests", "docs-check"]
    
    def pass_case():
        checks = create_mock_check_runs(required, all_success=True)
        result = validate_ci_checks(checks, required)
        assert result is True, "Should return True"
    
    def fail_missing():
        try:
            checks = [{"name": "governance-tests", "conclusion": "success"}]
            validate_ci_checks(checks, required)
            assert False, "Should raise MergeGateError"
        except MergeGateError:
            pass  # Expected
    
    def fail_not_success():
        try:
            checks = [
                {"name": "governance-tests", "conclusion": "failure"},
                {"name": "docs-check", "conclusion": "success"},
            ]
            validate_ci_checks(checks, required)
            assert False, "Should raise MergeGateError"
        except MergeGateError:
            pass  # Expected
    
    pass_case()
    fail_missing()
    fail_not_success()


def test_blocking_reviews():
    """Test Gate 6: No Blocking Reviews."""
    
    def pass_case():
        reviews = create_mock_reviews(blocking=False)
        result = validate_no_blocking_reviews(reviews)
        assert result is True, "Should return True"
    
    def fail_case():
        try:
            reviews = create_mock_reviews(blocking=True)
            validate_no_blocking_reviews(reviews)
            assert False, "Should raise MergeGateError"
        except MergeGateError:
            pass  # Expected
    
    pass_case()
    fail_case()


def test_closure_summary_evidence_based():
    """Test Closure Summary: Evidence-Based Learning Outcomes."""
    
    def with_evidence():
        summary = compose_closure_summary(
            issue_body="We learned how to structure governance",
            pr_title="Governance refactor",
            pr_number=10,
            merge_sha="abcd1234" * 5,
            pr_url="https://github.com/test/repo/pull/10",
            merge_url="https://github.com/test/repo/commit/abcd",
            workflow_url="https://github.com/test/repo/actions/runs/123",
            learned_evidence="See Issue description",
            next_steps_evidence="See PR description",
        )
        assert "See Issue description" in summary, "Should include learned evidence"
        assert "See PR description" in summary, "Should include next steps evidence"
        assert "未記錄" not in summary, "Should not mark as not recorded"
    
    def without_evidence():
        summary = compose_closure_summary(
            issue_body="",
            pr_title="Test PR",
            pr_number=1,
            merge_sha="abcd1234" * 5,
            pr_url="https://github.com/test/repo/pull/1",
            merge_url="https://github.com/test/repo/commit/abcd",
            workflow_url="https://github.com/test/repo/actions/runs/123",
        )
        assert "未記錄" in summary, "Should mark as not recorded when evidence missing"
        assert "None identified" in summary, "Should mark next steps as None identified"
    
    with_evidence()
    without_evidence()


def test_prior_closure_detection():
    """Test: Detect Prior Closure Summary (Idempotency)."""
    
    def find_prior():
        comments = [
            {"id": 1, "body": "Some comment"},
            {"id": 2, "body": "## ✅ Merged & Closed: Learning Consolidation\n..."},
            {"id": 3, "body": "Another comment"},
        ]
        result = check_prior_closure_summary(comments)
        assert result is True, "Should find prior closure"
    
    def no_prior():
        comments = [
            {"id": 1, "body": "Some comment"},
            {"id": 2, "body": "Another comment"},
        ]
        result = check_prior_closure_summary(comments)
        assert result is False, "Should not find prior closure"
    
    find_prior()
    no_prior()


def test_learning_evidence_extraction():
    """Test: Extract Learning Evidence (Evidence-Based Only)."""
    
    def from_issue():
        what, next = extract_learning_evidence(
            issue_body="We learned how to structure the codebase",
            pr_body="",
        )
        assert "See Issue description" in what, "Should reference Issue"
    
    def from_pr():
        what, next = extract_learning_evidence(
            issue_body="",
            pr_body="Future work: consider performance optimization",
        )
        assert "See PR description" in next, "Should reference PR"
    
    def not_recorded():
        what, next = extract_learning_evidence(
            issue_body="",
            pr_body="",
        )
        assert "未記錄" in what, "Should mark as not recorded"
        assert "None identified" in next, "Should mark next steps"
    
    from_issue()
    from_pr()
    not_recorded()


def test_mock_data_creation():
    """Test: Mock Data Creation."""
    
    def pr_data():
        pr = create_mock_pr_data(pr_number=5, pr_state="open")
        assert pr["number"] == 5, "Should set PR number"
        assert pr["state"] == "open", "Should set state"
        assert pr["draft"] is False, "Should not be draft"
        assert len(pr["head"]["sha"]) == 36, "Should have valid SHA"
    
    def checks():
        checks = create_mock_check_runs(
            required_checks=["governance-tests", "docs-check"],
            all_success=True
        )
        assert len(checks) == 2, "Should create both checks"
        assert all(c["conclusion"] == "success" for c in checks), "All should succeed"
    
    def reviews():
        approved = create_mock_reviews(blocking=False)
        assert approved[0]["state"] == "APPROVED", "Should be approved"
        
        blocking = create_mock_reviews(blocking=True)
        assert blocking[0]["state"] == "CHANGES_REQUESTED", "Should block"
    
    pr_data()
    checks()
    reviews()


def main():
    """Run all tests."""
    runner = TestRunner()
    
    print("=" * 70)
    print("Issue #11 Merge Lifecycle Mock Tests")
    print("Learning Hub: Evidence-Based, Fail-Closed Automation")
    print("=" * 70)
    print("")
    
    # Gate tests
    runner.test("Gate 1: Authorization", test_authorization)
    runner.test("Gate 2: PR Open", test_pr_open)
    runner.test("Gate 3: SHA Match", test_sha_match)
    runner.test("Gate 4: Base Branch", test_base_branch)
    runner.test("Gate 5: CI Checks", test_ci_checks)
    runner.test("Gate 6: Blocking Reviews", test_blocking_reviews)
    
    # Closure & idempotency tests
    runner.test("Closure Summary: Evidence-Based", test_closure_summary_evidence_based)
    runner.test("Closure Detection: Idempotency", test_prior_closure_detection)
    runner.test("Learning Evidence: Extraction", test_learning_evidence_extraction)
    
    # Mock data tests
    runner.test("Mock Data: Creation", test_mock_data_creation)
    
    print("")
    success = runner.summary()
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
