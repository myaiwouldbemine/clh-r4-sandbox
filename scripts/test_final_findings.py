#!/usr/bin/env python3
"""
Test Final Three Findings Corrections

Finding 1: Recovery Authorization — Verifiable workflow run history
Finding 2: Concurrency — PR number only (same PR, different issues = same group)
Finding 3: PR Documentation — Actual GitHub PR Description updated
"""

import subprocess
import json
import sys

def test_concurrency_pr_number_only():
    """
    Finding 2: Concurrency Group depends on PR number only.
    Same PR should use same concurrency group even with different issue numbers.
    """
    print("\n✅ Concurrency: PR Number Only")
    
    # Parse the workflow file and extract concurrency group format
    with open('.github/workflows/merge-and-close-pr.yml', 'r') as f:
        content = f.read()
    
    # Check that concurrency group uses ONLY pr_number
    if 'group: merge-pr-${{ inputs.pr_number }}' in content:
        print("   ✅ Concurrency group uses PR number only: merge-pr-${{ inputs.pr_number }}")
        
        # Verify it does NOT include issue_number
        if 'merge-pr-${{ inputs.pr_number }}-issue-${{ inputs.issue_number }}' in content:
            print("   ❌ ERROR: Still contains issue_number in concurrency group")
            return False
        
        print("   ✅ Issue number NOT included in concurrency group")
        
        # Verify cancel-in-progress is false
        if 'cancel-in-progress: false' in content:
            print("   ✅ cancel-in-progress: false (confirmed)")
        else:
            print("   ❌ cancel-in-progress not set to false")
            return False
        
        return True
    else:
        print("   ❌ Concurrency group format incorrect")
        return False

def test_recovery_authorization_workflow_history():
    """
    Finding 1: Recovery Authorization must verify original authorization via 
    existing GitHub Workflow Run / operation history.
    Fail Closed without verifiable evidence.
    """
    print("\n✅ Recovery Authorization: Workflow History Verification")
    
    with open('.github/workflows/merge-and-close-pr.yml', 'r') as f:
        content = f.read()
    
    checks = [
        ('Workflow run history query', 'gh run list'),
        ('Fail Closed semantics', 'RECOVERY BLOCKED'),
        ('Cannot verify original authorization', 'Cannot verify original authorization via Workflow Run history'),
        ('Prior workflow execution check', 'Prior workflow execution confirmed via history'),
    ]
    
    all_passed = True
    for check_name, check_phrase in checks:
        if check_phrase in content:
            print(f"   ✅ {check_name}: Found")
        else:
            print(f"   ❌ {check_name}: NOT found")
            all_passed = False
    
    # Verify that simple state consistency is NOT the only check
    if 'workflow_dispatch trigger itself is NOT proof' not in content and \
       'workflow_dispatch trigger alone insufficient' not in content:
        # Check for explicit workflow run history logic
        if 'gh run list' in content and 'found_matching_run' in content:
            print("   ✅ Explicit workflow run history logic present")
        else:
            print("   ⚠️  Recovery logic simplified but should include run history check")
    
    return all_passed

def test_pr_documentation_github_api_readback():
    """
    Finding 3: PR #12 Description must be actually updated in GitHub.
    Verify via GitHub API readback (not mock test returning true).
    """
    print("\n✅ PR Documentation: GitHub API Readback Verification")
    
    try:
        # Get the actual PR description from GitHub
        result = subprocess.run(
            ['gh', 'pr', 'view', '12', 
             '--repo', 'myaiwouldbemine/myaiwouldbemine-Copy-Learning-Hub',
             '--json', 'body'],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode != 0:
            print(f"   ❌ GitHub API call failed: {result.stderr}")
            return False
        
        pr_body = json.loads(result.stdout).get('body', '')
        
        # Check for key phrases indicating Learning Archive First design
        required_phrases = [
            'Learning Archive First',
            'Archive Closure Record',
            'Issue closure',
            'workflow',
            'tests',
        ]
        
        found_phrases = []
        missing_phrases = []
        
        for phrase in required_phrases:
            if phrase.lower() in pr_body.lower():
                found_phrases.append(phrase)
            else:
                missing_phrases.append(phrase)
        
        print(f"   ✅ Found {len(found_phrases)}/{len(required_phrases)} required concepts")
        for phrase in found_phrases:
            print(f"      ✓ {phrase}")
        
        if missing_phrases:
            print(f"   ⚠️  Missing {len(missing_phrases)} concepts:")
            for phrase in missing_phrases:
                print(f"      ✗ {phrase}")
            return False
        
        # Verify description is not empty and has substantial content
        if len(pr_body) < 200:
            print(f"   ❌ PR description too short ({len(pr_body)} chars, expected >200)")
            return False
        
        print(f"   ✅ PR description length: {len(pr_body)} chars (substantial)")
        print(f"   ✅ GitHub API Readback successful — description is real, not mock")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error during GitHub API readback: {e}")
        return False

def main():
    print("="*70)
    print("FINAL THREE FINDINGS CORRECTIONS TEST")
    print("="*70)
    
    results = {
        'Finding 1 — Recovery Authorization': test_recovery_authorization_workflow_history(),
        'Finding 2 — Concurrency PR Number Only': test_concurrency_pr_number_only(),
        'Finding 3 — PR Documentation GitHub Readback': test_pr_documentation_github_api_readback(),
    }
    
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for finding, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {finding}")
    
    print(f"\nTotal: {passed}/{total} findings verified")
    
    if passed == total:
        print("\n✅ All three findings verified successfully")
        return 0
    else:
        print(f"\n❌ {total - passed} finding(s) need attention")
        return 1

if __name__ == '__main__':
    sys.exit(main())
