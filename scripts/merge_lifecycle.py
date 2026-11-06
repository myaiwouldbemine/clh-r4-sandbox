#!/usr/bin/env python3
"""
Issue #11 Merge Lifecycle Helper Functions (Archive Record Focus)

Provides minimal utilities for archive closure automation:
- PR-Issue linkage verification
- Prior closure deduplication

Learning Hub governance: Records learning archives without enforcing learning quality.
Issue closure indicates upload/archive completion, not learning conclusion.
"""

import re
from typing import List, Tuple, Optional, Dict


def verify_pr_issue_linkage(pr_body: str, target_issue_number: int) -> Tuple[bool, str]:
    """
    Verify explicit PR ↔ Issue linkage using precise pattern matching.
    
    Args:
        pr_body: PR description text
        target_issue_number: Target Issue number (e.g., 11)
    
    Returns:
        Tuple of (linkage_valid, reason)
        - linkage_valid: True if PR explicitly references target Issue
        - reason: Explanation string
    
    Required patterns:
    - "#N" (exact issue number)
    - "Fixes #N", "Closes #N", "Resolves #N" (keyword + exact number)
    """
    if not pr_body or not pr_body.strip():
        return False, "PR body is empty"
    
    # Pattern 1: "Fixes #N" / "Closes #N" / "Resolves #N" (case-insensitive)
    patterns = [
        rf'\b(Fixes|Closes|Resolves)\s+#{target_issue_number}\b',
        rf'(?:^|\s)#{target_issue_number}(?:\s|$|\.|\n)',
    ]
    
    for pattern in patterns:
        if re.search(pattern, pr_body, re.IGNORECASE | re.MULTILINE):
            return True, f"PR body contains explicit reference to Issue #{target_issue_number}"
    
    # Check what references exist
    issue_refs = re.findall(r'(?:Fixes|Closes|Resolves|#)(?:\s)?#?(\d+)', pr_body, re.IGNORECASE)
    if issue_refs:
        return False, f"PR body references issues {set(issue_refs)}, not #{target_issue_number}"
    
    return False, "PR body contains no explicit issue reference"


def detect_prior_closure(comments: List[Dict], pr_number: int, merge_sha_full: str) -> bool:
    """
    Detect if an archive closure record already exists for this PR+Merge combination.
    
    Args:
        comments: List of issue comments from GitHub API
        pr_number: PR number being merged
        merge_sha_full: Complete merge commit SHA (40 chars)
    
    Returns:
        True if prior closure record found (should skip reposting)
    
    Matching criteria (must match ALL):
    - Comment body contains PR number reference
    - Comment body contains merge commit SHA (short or full)
    - Comment body contains archive/closure marker
    """
    if not comments or not isinstance(comments, list):
        return False
    
    merge_sha_short = merge_sha_full[:8] if len(merge_sha_full) >= 8 else merge_sha_full
    
    for comment in comments:
        body = comment.get("body", "")
        
        # Check all three conditions
        has_pr_ref = f"#{pr_number}" in body or f"PR #{pr_number}" in body
        has_merge_ref = merge_sha_short in body or merge_sha_full in body
        has_archive_marker = "Archive Closure" in body or "Archive" in body.lower() or "Merged & Closed" in body
        
        if has_pr_ref and has_merge_ref and has_archive_marker:
            return True
    
    return False
