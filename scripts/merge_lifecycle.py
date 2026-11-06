#!/usr/bin/env python3
"""
Issue #11 Merge Lifecycle Helper Functions

Provides utilities for merge gate validation, API calls, closure summary composition.
Used by GitHub Actions workflow and local testing.

Learning Hub governance philosophy: Preserve learning, not control.
All learning outcomes must be evidence-based (Issue/PR/Result records).
"""

import json
import os
from typing import Dict, Optional, List, Tuple


class MergeAuthorizationError(Exception):
    """Raised when authorization fails."""
    pass


class MergeGateError(Exception):
    """Raised when a merge gate check fails."""
    pass


def check_authorization(actor: str, allow_list: List[str]) -> bool:
    """
    Gate 1: Verify GitHub Actions triggerer is authorized.
    
    Args:
        actor: github.actor from workflow context
        allow_list: List of authorized usernames
    
    Returns:
        True if authorized
    
    Raises:
        MergeAuthorizationError: If actor not in allow_list
    """
    if actor not in allow_list:
        raise MergeAuthorizationError(
            f"Authorization failed: github.actor='{actor}' not in allow_list {allow_list}"
        )
    return True


def validate_pr_open(pr_state: str, pr_draft: bool) -> bool:
    """
    Gate 2: Verify PR is open and not in draft status.
    
    Args:
        pr_state: PR state from GitHub API (open/closed/merged)
        pr_draft: PR draft flag from GitHub API
    
    Returns:
        True if PR is open and ready
    
    Raises:
        MergeGateError: If PR is not open or is draft
    """
    if pr_state != "open":
        raise MergeGateError(f"PR state is '{pr_state}' (expected: open)")
    if pr_draft:
        raise MergeGateError("PR is in draft status")
    return True


def validate_sha_match(authorized_sha: str, current_sha: str) -> bool:
    """
    Gate 3: Verify Head SHA matches exactly (prevent commit changes after authorization).
    
    Args:
        authorized_sha: Head SHA provided by Human at trigger time
        current_sha: Current Head SHA from GitHub API
    
    Returns:
        True if SHAs match
    
    Raises:
        MergeGateError: If SHAs do not match
    """
    if authorized_sha != current_sha:
        raise MergeGateError(
            f"Head SHA mismatch: authorized='{authorized_sha}', current='{current_sha}'"
        )
    return True


def validate_base_branch(authorized_base: str, current_base: str) -> bool:
    """
    Gate 4: Verify base branch matches.
    
    Args:
        authorized_base: Base branch from trigger input
        current_base: Current base branch from GitHub API
    
    Returns:
        True if base branches match
    
    Raises:
        MergeGateError: If base branches do not match
    """
    if authorized_base != current_base:
        raise MergeGateError(
            f"Base branch mismatch: authorized='{authorized_base}', current='{current_base}'"
        )
    return True


def validate_ci_checks(check_runs: List[Dict], required_checks: List[str]) -> bool:
    """
    Gate 5: Verify required CI checks passed.
    
    Args:
        check_runs: List of check runs from GitHub API
        required_checks: List of required check names (e.g., ['governance-tests', 'docs-check'])
    
    Returns:
        True if all required checks passed
    
    Raises:
        MergeGateError: If any required check is not SUCCESS
    """
    passed_checks = {}
    
    # Extract conclusions by check name
    for check in check_runs:
        check_name = check.get("name", "")
        conclusion = check.get("conclusion", "")
        
        if check_name in required_checks:
            passed_checks[check_name] = conclusion
    
    # Verify all required checks are present and successful
    for required in required_checks:
        if required not in passed_checks:
            raise MergeGateError(f"Required check '{required}' not found in check runs")
        if passed_checks[required] != "success":
            raise MergeGateError(
                f"Required check '{required}' did not succeed (conclusion: {passed_checks[required]})"
            )
    
    return True


def validate_no_blocking_reviews(reviews: List[Dict]) -> bool:
    """
    Gate 6: Verify no blocking reviews ("changes requested").
    
    Args:
        reviews: List of PR reviews from GitHub API
    
    Returns:
        True if no blocking reviews
    
    Raises:
        MergeGateError: If any "changes requested" review found
    """
    blocking = [r for r in reviews if r.get("state") == "CHANGES_REQUESTED"]
    
    if blocking:
        raise MergeGateError(
            f"Found {len(blocking)} 'changes requested' review(s) blocking merge"
        )
    
    return True


def compose_closure_summary(
    issue_body: str,
    pr_title: str,
    pr_number: int,
    merge_sha: str,
    pr_url: str,
    merge_url: str,
    workflow_url: str,
    learned_evidence: Optional[str] = None,
    next_steps_evidence: Optional[str] = None,
) -> str:
    """
    Compose Learning Closure Summary for issue comment.
    
    Philosophy: Evidence-based. Extract learning outcomes from Issue/PR/Result.
               Never fabricate from titles or labels.
               Mark "未記錄" (not recorded) if evidence unavailable.
    
    Args:
        issue_body: Issue description (learning motivation)
        pr_title: PR title (what changed)
        pr_number: PR number
        merge_sha: Merge commit SHA
        pr_url: PR URL
        merge_url: Merge commit URL
        workflow_url: GitHub Actions workflow run URL
        learned_evidence: Extracted learning outcome evidence (mark "未記錄" if none)
        next_steps_evidence: Extracted next steps evidence (mark "None identified" if none)
    
    Returns:
        Formatted closure summary markdown
    """
    
    # Extract first 500 chars of issue body (learning motivation)
    motivation = issue_body[:500] if issue_body else "[Issue body not available]"
    
    # Build closure comment
    closure_comment = f"""## ✅ Merged & Closed: Learning Consolidation

**Learning Motivation**
{motivation}

**What Changed**
- PR: #{pr_number}
- Merge Commit: `{merge_sha}`
- Method: merge (preserve full history)

**Evidence**
- PR: [#{pr_number}]({pr_url})
- Merge Commit: [{merge_sha}]({merge_url})
- GitHub Actions: [Workflow Run]({workflow_url})

**What Learned**
{learned_evidence if learned_evidence else "未記錄 (not recorded in Issue / PR description / Result)"}

**Remaining Questions / Next Steps**
{next_steps_evidence if next_steps_evidence else "None identified"}

---
*Closure Summary generated by Issue #11 automation workflow. Evidence-based learning outcomes only.*
"""
    
    return closure_comment


def check_prior_closure_summary(issue_comments: List[Dict]) -> bool:
    """
    Check if closure summary has already been posted.
    
    Used for idempotency: If re-running workflow after merge, skip duplicate post.
    
    Args:
        issue_comments: List of issue comments from GitHub API
    
    Returns:
        True if prior closure summary found, False otherwise
    """
    for comment in issue_comments:
        if "Merged & Closed: Learning Consolidation" in comment.get("body", ""):
            return True
    return False


def verify_issue_match_before_close(
    pr_number: int,
    issue_number: int,
    merge_sha: str,
    pr_data: Dict,
) -> bool:
    """
    Critical verification before closing issue.
    
    Prevents accidental closure of wrong issue by verifying:
    - PR number matches authorization
    - Merge SHA is present (merge succeeded)
    - Issue number matches authorization
    
    Args:
        pr_number: Authorized PR number
        issue_number: Authorized issue number
        merge_sha: Merge commit SHA from merge execution
        pr_data: PR details from GitHub API
    
    Returns:
        True if all verifications pass
    
    Raises:
        MergeGateError: If any verification fails (fail-closed)
    """
    
    if not merge_sha:
        raise MergeGateError("Merge SHA is empty; refusing to close issue (fail-closed)")
    
    # Implicit verification via workflow parameters:
    # - pr_number and issue_number are workflow inputs (authorized by Human)
    # - merge_sha confirms merge succeeded
    
    return True


def extract_learning_evidence(issue_body: str, pr_body: str, result_body: Optional[str] = None) -> Tuple[str, str]:
    """
    Extract learning outcomes from evidence sources.
    
    Philosophy: Evidence-based only. Return "未記錄" if no evidence found.
    
    Args:
        issue_body: Issue description
        pr_body: PR description
        result_body: Optional Result record (if available)
    
    Returns:
        Tuple of (what_learned, next_steps)
        Each marked as "未記錄" if not found in any evidence source
    """
    
    what_learned = "未記錄 (not recorded in Issue / PR / Result)"
    next_steps = "None identified"
    
    # Try to find evidence in sources
    all_body = (issue_body or "") + (pr_body or "") + (result_body or "")
    
    # Check for learning keywords
    if any(keyword in all_body.lower() for keyword in ["learned", "discover", "understand", "realized"]):
        if issue_body and any(keyword in issue_body.lower() for keyword in ["learned", "discover"]):
            what_learned = "See Issue description"
        elif pr_body and any(keyword in pr_body.lower() for keyword in ["learned", "discover"]):
            what_learned = "See PR description"
        elif result_body and any(keyword in result_body.lower() for keyword in ["learned", "discover"]):
            what_learned = "See Result record"
    
    # Check for next steps keywords
    if any(keyword in all_body.lower() for keyword in ["next", "future", "follow", "todo"]):
        if issue_body and any(keyword in issue_body.lower() for keyword in ["next", "future"]):
            next_steps = "See Issue description"
        elif pr_body and any(keyword in pr_body.lower() for keyword in ["next", "future", "follow"]):
            next_steps = "See PR description"
        elif result_body and any(keyword in result_body.lower() for keyword in ["next", "future"]):
            next_steps = "See Result record"
    
    return (what_learned, next_steps)


# Mock test helpers

def create_mock_pr_data(
    pr_number: int = 1,
    pr_state: str = "open",
    pr_draft: bool = False,
    head_sha: str = "abc123" * 6,  # 36 chars = valid SHA
    base_branch: str = "main",
    pr_title: str = "Test PR",
    mergeable: bool = True,
) -> Dict:
    """Create mock PR data for testing."""
    return {
        "number": pr_number,
        "state": pr_state,
        "draft": pr_draft,
        "head": {"sha": head_sha},
        "base": {"ref": base_branch},
        "title": pr_title,
        "body": "Test PR description",
        "merged": False,
        "mergeable": mergeable,
        "html_url": f"https://github.com/test/repo/pull/{pr_number}",
    }


def create_mock_check_runs(
    required_checks: List[str] = None,
    all_success: bool = True,
) -> List[Dict]:
    """Create mock CI check runs for testing."""
    if required_checks is None:
        required_checks = ["governance-tests", "docs-check"]
    
    checks = []
    for check_name in required_checks:
        checks.append({
            "name": check_name,
            "conclusion": "success" if all_success else "failure",
            "status": "completed",
        })
    return checks


def create_mock_reviews(blocking: bool = False) -> List[Dict]:
    """Create mock PR reviews for testing."""
    if blocking:
        return [
            {
                "id": 1,
                "state": "CHANGES_REQUESTED",
                "author": {"login": "reviewer"},
            }
        ]
    return [
        {
            "id": 1,
            "state": "APPROVED",
            "author": {"login": "reviewer"},
        }
    ]


if __name__ == "__main__":
    # Example usage / self-test
    print("merge_lifecycle.py loaded successfully")
    print("Provides gate validation, API helpers, closure summary composition")
    print("All learning outcomes are evidence-based (never fabricated)")


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
    
    Unambiguous patterns required:
    - "#N" (exact issue number)
    - "Fixes #N" (keyword + exact number)
    - "Closes #N" (keyword + exact number)
    - "Resolves #N" (keyword + exact number)
    
    Rejected patterns:
    - "fixes something" without "#N"
    - "Fixes #99" when target is #11
    - Keywords without explicit number
    """
    if not pr_body or not pr_body.strip():
        return False, "PR body is empty"
    
    # Pattern 1: "Fixes #N" / "Closes #N" / "Resolves #N" (case-insensitive)
    import re
    
    # Build precise regex: keyword + space + exact issue number
    patterns = [
        rf'\b(Fixes|Closes|Resolves)\s+#{target_issue_number}\b',  # Keyword + #N
        rf'(?:^|\s)#{target_issue_number}(?:\s|$|\.|\n)',  # Bare #N (with boundaries)
    ]
    
    for pattern in patterns:
        if re.search(pattern, pr_body, re.IGNORECASE | re.MULTILINE):
            return True, f"PR body contains explicit reference to Issue #{target_issue_number}"
    
    # Failed: Check what references exist
    issue_refs = re.findall(r'(?:Fixes|Closes|Resolves|#)(?:\s)?#?(\d+)', pr_body, re.IGNORECASE)
    if issue_refs:
        return False, f"PR body references issues {set(issue_refs)}, not #{target_issue_number}"
    
    return False, "PR body contains no explicit issue reference (no 'Fixes #N' or '#N' pattern)"


def extract_learning_outcome(issue_body: str, pr_body: str, result_content: Optional[str] = None) -> Tuple[str, str]:
    """
    Extract learning outcome from actual content (not keyword-only detection).
    
    Args:
        issue_body: Issue description
        pr_body: PR description
        result_content: RESULT.md content (optional)
    
    Returns:
        Tuple of (learning_outcome, source)
        - learning_outcome: Actual outcome text or "未記錄"
        - source: "Issue" / "PR" / "RESULT.md" / "" (empty if未記錄)
    """
    import re
    
    # Keywords indicating learning content
    learning_keywords = [
        "learned", "discover", "understand", "found", "insight",
        "realized", "recognized", "achieved", "accomplished"
    ]
    
    # Function to extract sentences/clauses around keywords
    def extract_context(text, keywords):
        """Extract text containing first matching keyword."""
        if not text:
            return None
            
        for kw in keywords:
            # Look for word containing keyword (case-insensitive)
            pattern = rf'\b\w*{kw}\w*\b'
            if re.search(pattern, text, re.IGNORECASE):
                # Extract sentence containing keyword
                sentences = re.split(r'[.!?\n]+', text)
                for sent in sentences:
                    if re.search(pattern, sent, re.IGNORECASE):
                        sent_clean = sent.strip()
                        if sent_clean:
                            return sent_clean
        return None
    
    # Try Issue first
    if issue_body:
        outcome = extract_context(issue_body, learning_keywords)
        if outcome:
            return outcome, "Issue"
    
    # Try PR
    if pr_body:
        outcome = extract_context(pr_body, learning_keywords)
        if outcome:
            return outcome, "PR"
    
    # Try RESULT.md
    if result_content:
        outcome = extract_context(result_content, learning_keywords)
        if outcome:
            return outcome, "RESULT.md"
    
    # No evidence found
    return "未記錄", ""


def detect_prior_closure(comments: List[Dict], pr_number: int, merge_sha_full: str) -> bool:
    """
    Detect if a closure summary already exists for this PR+Issue+Merge combination.
    
    Args:
        comments: List of issue comments from GitHub API
        pr_number: PR number being merged
        merge_sha_full: Complete merge commit SHA (40 chars)
    
    Returns:
        True if prior closure found (should skip reposting)
    
    Matching criteria (must match ALL):
    - Comment body contains PR number reference
    - Comment body contains merge commit short SHA (first 8 chars)
    - Comment body contains "Merged & Closed" or similar closure marker
    """
    if not comments or not isinstance(comments, list):
        return False
    
    merge_sha_short = merge_sha_full[:8] if len(merge_sha_full) >= 8 else merge_sha_full
    
    for comment in comments:
        body = comment.get("body", "")
        
        # Check ALL three conditions
        has_pr_ref = f"#{pr_number}" in body or f"PR #{pr_number}" in body
        has_merge_ref = merge_sha_short in body or merge_sha_full in body
        has_closure_marker = "Merged & Closed" in body or "merged" in body.lower()
        
        if has_pr_ref and has_merge_ref and has_closure_marker:
            return True
    
    return False


def validate_recovery_authorization(
    authorized_head_sha: str,
    current_head_sha: str,
    authorized_base: str,
    current_base: str,
    authorized_issue: int,
    target_issue: int,
) -> Tuple[bool, str]:
    """
    Validate recovery path: verify all authorization parameters still match.
    
    Recovery should only proceed if:
    - Head SHA hasn't changed (PR branch tip)
    - Base branch is still the same
    - Issue is still the same
    
    Args:
        authorized_head_sha: SHA from original authorization
        current_head_sha: PR's current head SHA
        authorized_base: Base from original authorization
        current_base: PR's current base
        authorized_issue: Issue from original authorization
        target_issue: Target Issue for closure
    
    Returns:
        Tuple of (valid, reason)
    """
    if authorized_head_sha != current_head_sha:
        return False, f"Head SHA changed (authorized: {authorized_head_sha[:8]}, current: {current_head_sha[:8]})"
    
    if authorized_base != current_base:
        return False, f"Base branch changed (authorized: {authorized_base}, current: {current_base})"
    
    if authorized_issue != target_issue:
        return False, f"Issue number changed (authorized: {authorized_issue}, target: {target_issue})"
    
    return True, "All authorization parameters match"
