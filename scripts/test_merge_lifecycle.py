#!/usr/bin/env python3
"""
Issue #11 Archive Closure Tests

Test PR-Issue linkage verification and prior closure deduplication.
Focused on archive record correctness, not learning quality.
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


def test_prior_closure_deduplication():
    """Test archive closure deduplication with full SHA matching."""
    
    def prior_found():
        comments = [
            {"body": "## 📦 Archive Closure Record\nPR #10 ... Merge Commit abc12345"}
        ]
        found = detect_prior_closure(comments, 10, "abc12345def456abc123def456abc123def456ab")
        assert found, "Should detect prior closure"
    
    def different_pr():
        comments = [
            {"body": "## 📦 Archive Closure Record\nPR #9 ... Merge Commit abc12345"}
        ]
        found = detect_prior_closure(comments, 10, "abc12345def456abc123def456abc123def456ab")
        assert not found, "Should not match different PR"
    
    def different_merge():
        comments = [
            {"body": "## 📦 Archive Closure Record\nPR #10 ... Merge Commit def56789"}
        ]
        found = detect_prior_closure(comments, 10, "abc12345def456abc123def456abc123def456ab")
        assert not found, "Should not match different merge"
    
    def empty_comments():
        found = detect_prior_closure([], 10, "abc12345def456abc123def456abc123def456ab")
        assert not found, "Should handle empty comments"
    
    def no_archive_marker():
        comments = [
            {"body": "Regular comment\nPR #10 abc12345"}
        ]
        found = detect_prior_closure(comments, 10, "abc12345def456abc123def456abc123def456ab")
        assert not found, "Should require archive marker"
    
    prior_found()
    different_pr()
    different_merge()
    empty_comments()
    no_archive_marker()
    print("✅ test_prior_closure_deduplication PASSED")


if __name__ == "__main__":
    try:
        test_pr_issue_linkage_precision()
        test_prior_closure_deduplication()
        print("\n✅ All 2 test groups PASSED (PR linkage + prior closure)")
        sys.exit(0)
    except AssertionError as e:
        print(f"\n❌ Test FAILED: {e}")
        sys.exit(1)
