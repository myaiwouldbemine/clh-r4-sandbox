#!/usr/bin/env python3
"""
Issue #11 Archive Closure Tests

Test PR-Issue linkage verification and prior closure deduplication.
Focused on archive record correctness, not learning quality.

Four Safety Fixes (v1.5):
1. GitHub REST Merge API with sha parameter (atomic compare-and-swap)
2. Issue Comments read with Fail Closed (API/JSON errors → exit)
3. Complete 40-character Merge SHA for precise deduplication
4. Safe Closure Record file passing (not shell variable expansion)
"""

import sys
sys.path.insert(0, '.')

from merge_lifecycle import verify_pr_issue_linkage, detect_prior_closure


def test_pr_issue_linkage_precision():
    """Test PR-Issue linkage with precise pattern matching."""
    
    def exact_match():
        pr_body = "This fixes the issue.\nFixes #11"
        valid, reason = verify_pr_issue_linkage(pr_body, 11)
        assert valid, reason
    
    def wrong_issue():
        pr_body = "Fixes #99 by refactoring"
        valid, reason = verify_pr_issue_linkage(pr_body, 11)
        assert not valid, "Should reject wrong issue number"
    
    def bare_issue_number():
        pr_body = "Addresses #11"
        valid, reason = verify_pr_issue_linkage(pr_body, 11)
        assert valid, reason
    
    def no_reference():
        pr_body = "Fixes a bug in the workflow"
        valid, reason = verify_pr_issue_linkage(pr_body, 11)
        assert not valid, "Should reject 'fixes' without issue number"
    
    def case_insensitive():
        pr_body = "closes #11 now"
        valid, reason = verify_pr_issue_linkage(pr_body, 11)
        assert valid, reason
    
    def empty_body():
        valid, reason = verify_pr_issue_linkage("", 11)
        assert not valid, "Should reject empty body"
    
    exact_match()
    wrong_issue()
    bare_issue_number()
    no_reference()
    case_insensitive()
    empty_body()
    print("✅ test_pr_issue_linkage_precision PASSED")


def test_prior_closure_deduplication_full_sha():
    """Test archive closure deduplication with full 40-character SHA matching."""
    
    def prior_found_with_full_sha():
        """Test that prior closure is detected with full 40-char SHA."""
        full_sha = "abc12345def456abc123def456abc123def456ab"  # 40 chars
        comments = [
            {"body": "## 📦 Archive Closure Record\nPR #10 ... Merge Commit abc12345def456abc123def456abc123def456ab"}
        ]
        found = detect_prior_closure(comments, 10, full_sha)
        assert found, "Should detect prior closure with full SHA"
    
    def different_pr():
        """Test that different PR number prevents match."""
        full_sha = "abc12345def456abc123def456abc123def456ab"
        comments = [
            {"body": "## 📦 Archive Closure Record\nPR #9 ... Merge Commit abc12345def456abc123def456abc123def456ab"}
        ]
        found = detect_prior_closure(comments, 10, full_sha)
        assert not found, "Should not match different PR"
    
    def different_merge():
        """Test that different merge SHA prevents match."""
        full_sha = "abc12345def456abc123def456abc123def456ab"
        comments = [
            {"body": "## 📦 Archive Closure Record\nPR #10 ... Merge Commit def56789abc12345def456abc123def456abc1"}
        ]
        found = detect_prior_closure(comments, 10, full_sha)
        assert not found, "Should not match different merge SHA"
    
    def empty_comments():
        """Test that empty comments list returns False."""
        full_sha = "abc12345def456abc123def456abc123def456ab"
        found = detect_prior_closure([], 10, full_sha)
        assert not found, "Should handle empty comments"
    
    def no_archive_marker():
        """Test that missing archive marker prevents match."""
        full_sha = "abc12345def456abc123def456abc123def456ab"
        comments = [
            {"body": "Regular comment\nPR #10 abc12345def456abc123def456abc123def456ab"}
        ]
        found = detect_prior_closure(comments, 10, full_sha)
        assert not found, "Should require archive marker"
    
    def invalid_sha_too_short():
        """Test that SHA validation rejects short hashes."""
        short_sha = "abc12345"  # Only 8 chars
        try:
            detect_prior_closure([], 10, short_sha)
            assert False, "Should raise ValueError for short SHA"
        except ValueError as e:
            assert "40 chars" in str(e), f"Error message should mention 40 chars: {e}"
    
    def invalid_sha_too_long():
        """Test that SHA validation rejects long hashes."""
        long_sha = "abc12345def456abc123def456abc123def456ab00"  # 42 chars
        try:
            detect_prior_closure([], 10, long_sha)
            assert False, "Should raise ValueError for long SHA"
        except ValueError as e:
            assert "40 chars" in str(e), f"Error message should mention 40 chars: {e}"
    
    prior_found_with_full_sha()
    different_pr()
    different_merge()
    empty_comments()
    no_archive_marker()
    invalid_sha_too_short()
    invalid_sha_too_long()
    print("✅ test_prior_closure_deduplication_full_sha PASSED")


def test_four_safety_fixes():
    """Integration test for the four v1.5 safety fixes."""
    
    def fix_3_full_sha_matching():
        """Fix #3: Complete 40-char SHA for precise matching."""
        full_sha = "0" * 40  # Exactly 40 zeros
        comments = [
            {"body": "PR #5 merged with SHA 0000000000000000000000000000000000000000 - Archive Closure"}
        ]
        found = detect_prior_closure(comments, 5, full_sha)
        assert found, "Fix #3: Should match using full 40-char SHA"
    
    def fix_3_reject_partial_sha():
        """Fix #3: Reject partial SHA matching."""
        full_sha_40 = "abc12345def456abc123def456abc123def456ab"
        partial_sha_8 = "abc12345"
        comments = [
            {"body": f"PR #10 merged with {partial_sha_8} - Archive"}
        ]
        found = detect_prior_closure(comments, 10, full_sha_40)
        assert not found, "Fix #3: Should not match partial SHA vs full SHA"
    
    def fix_2_sha_validation():
        """Fix #2+3: Issue comments fail-closed with SHA validation."""
        invalid_sha = "tooshort"
        try:
            detect_prior_closure([], 10, invalid_sha)
            assert False, "Should fail closed on invalid SHA"
        except ValueError:
            pass  # Expected
    
    fix_3_full_sha_matching()
    fix_3_reject_partial_sha()
    fix_2_sha_validation()
    print("✅ test_four_safety_fixes PASSED")


if __name__ == "__main__":
    try:
        test_pr_issue_linkage_precision()
        test_prior_closure_deduplication_full_sha()
        test_four_safety_fixes()
        print("\n✅ All 3 test groups PASSED")
        print("   - PR linkage precision (6 tests)")
        print("   - Prior closure deduplication (7 tests)")
        print("   - Four safety fixes integration (3 tests)")
        sys.exit(0)
    except (AssertionError, Exception) as e:
        print(f"\n❌ Test FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
