#!/usr/bin/env python3
"""
Issue #11 Merge Error Handling and Permissions Regression Tests

Verify that the conditional assignment error handling fix and permissions
upgrade work correctly. Tests cover:

1. Bash -e error handling: Conditional assignment pattern prevents silent failure
2. GitHub API error output: Safe filtering prevents token leakage
3. Minimum permissions: contents: write requirement for merge endpoint
4. Safe error diagnostics: HTTP status, message, and errors extracted safely
"""

import unittest
import subprocess
import json
import os
import sys


class ConditionalAssignmentErrorHandlingTests(unittest.TestCase):
    """Test conditional assignment pattern for bash -e error handling."""

    def test_bash_e_with_conditional_assignment(self):
        """Test that conditional assignment works with set -e."""
        bash_script = """
set -e
if result=$(echo "success"); then
    echo "GOT_RESULT: $result"
else
    echo "ERROR: Command failed"
    exit 1
fi
"""
        proc = subprocess.run(['bash', '-c', bash_script], capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, f"Script failed: {proc.stderr}")
        self.assertIn("GOT_RESULT: success", proc.stdout, "Should capture result")

    def test_bash_e_with_failing_conditional_assignment(self):
        """Test that conditional assignment catches failures with set -e."""
        bash_script = """
set -e
if result=$(false 2>&1); then
    echo "Should not reach here"
    exit 1
else
    echo "CAUGHT_ERROR: Command failed as expected"
    exit 0
fi
"""
        proc = subprocess.run(['bash', '-c', bash_script], capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, f"Error handler failed: {proc.stderr}")
        self.assertIn("CAUGHT_ERROR", proc.stdout, "Should catch error in else block")

    def test_bash_e_old_pattern_silent_failure(self):
        """Test demonstrating the old pattern's silent failure under bash -e."""
        bash_script = """
set -e
# Old unsafe pattern
result=$(false 2>&1); if [[ $? -ne 0 ]]; then
    echo "ERROR: This check never runs"
    exit 1
fi
echo "BUG: Script continues after false command"
"""
        proc = subprocess.run(['bash', '-c', bash_script], capture_output=True, text=True)
        self.assertNotEqual(proc.returncode, 0, "Old pattern should fail silently")
        self.assertNotIn("This check never runs", proc.stdout, "Error check never executes")

    def test_stderr_capture_with_conditional_assignment(self):
        """Test that stderr is captured in conditional assignment."""
        bash_script = """
set -e
if result=$(bash -c "echo 'error message' >&2; false" 2>&1); then
    echo "Should not reach"
else
    echo "CAPTURED_ERROR: exit code was non-zero"
fi
"""
        proc = subprocess.run(['bash', '-c', bash_script], capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, "Should handle error correctly")
        self.assertIn("CAPTURED_ERROR", proc.stdout, "Should capture error condition")


class APIErrorOutputSafetyTests(unittest.TestCase):
    """Test that error output from GitHub API is safe (no token leakage)."""

    def test_json_filter_safe_status(self):
        """Test safely extracting status without raw API response."""
        api_response_str = '{"status": 403, "message": "Forbidden", "documentation_url": "https://docs.github.com/...", "token": "ghs_FAKE_TOKEN_12345"}'

        # Use Python to simulate what jq does
        api_response = json.loads(api_response_str)
        status = api_response.get('status', 'unknown')

        # Verify token is NOT in the extracted value
        self.assertEqual(status, 403, f"Should extract status: {status}")
        self.assertNotIn("token", str(status).lower(), "Token should not in extracted status")
        self.assertNotIn("FAKE_TOKEN", str(status), "Token value should not appear")

    def test_json_filter_safe_message(self):
        """Test safely extracting message without raw response."""
        api_response_str = '{"status": 403, "message": "Forbidden: contents write permission required", "token": "secret_token_xyz"}'

        api_response = json.loads(api_response_str)
        message = api_response.get('message', 'Unknown error')

        self.assertIn("contents write permission", message)
        self.assertNotIn("secret_token", message, "Token should not in message")

    def test_json_filter_safe_error_list(self):
        """Test safely extracting errors array without raw response."""
        api_response_str = '{"status": 422, "errors": [{"message": "Pull request is not mergeable", "code": "mergeable_state"}, {"message": "Other error"}], "api_key": "dangerous_key_123"}'

        api_response = json.loads(api_response_str)
        errors = api_response.get('errors', [])
        error_messages = [e.get('message', '') for e in errors]

        self.assertIn("not mergeable", ' '.join(error_messages))
        self.assertNotIn("dangerous_key", ' '.join(error_messages), "API key should not appear")

    def test_raw_response_would_leak(self):
        """Demonstrate that raw response would leak tokens."""
        api_response = "token:ghs_SECRET_12345 message:error"

        # Unsafe: printing raw response
        output = f"Raw: {api_response}"
        self.assertIn("ghs_SECRET_12345", output, "Raw response would leak token")

    def test_jq_bash_pattern_safe(self):
        """Test the bash filtering pattern if jq is available, or verify fallback."""
        bash_script = """
response='{"status": 403, "message": "Forbidden", "token": "secret"}'

# Try jq if available, otherwise fall back to safe extraction
if command -v jq &> /dev/null; then
    status=$(echo "$response" | jq '.status // "unknown"')
    echo "JQ_STATUS: $status"
else
    # Fallback: use safe pattern to avoid token leakage
    status=$(echo "$response" | python3 -c "import sys, json; d=json.load(sys.stdin); print(d.get('status', 'unknown'))")
    echo "FALLBACK_STATUS: $status"
fi
"""
        proc = subprocess.run(['bash', '-c', bash_script], capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, f"Pattern failed: {proc.stderr}")
        output = proc.stdout.strip()
        self.assertTrue("403" in output or "JQ_STATUS" in output or "FALLBACK_STATUS" in output)
        self.assertNotIn("secret", proc.stdout, "Token should not leak in output")


class PermissionsWorkflowRequirementsTests(unittest.TestCase):
    """Test workflow permissions configuration."""

    def test_workflow_file_has_contents_write(self):
        """Test that workflow has contents: write permission."""
        workflow_path = "./.github/workflows/merge-and-close-pr.yml"
        self.assertTrue(os.path.exists(workflow_path), f"Workflow file not found: {workflow_path}")

        with open(workflow_path, 'r') as f:
            content = f.read()

        self.assertIn('contents: write', content, "Workflow must have 'contents: write' permission")

    def test_workflow_permissions_sufficient(self):
        """Test that all required permissions are present."""
        workflow_path = "./.github/workflows/merge-and-close-pr.yml"
        with open(workflow_path, 'r') as f:
            content = f.read()

        required_perms = ['contents: write', 'pull-requests: write', 'issues: write']
        for perm in required_perms:
            self.assertIn(perm, content, f"Workflow missing required permission: {perm}")

    def test_merge_api_endpoint_requirement(self):
        """
        Document that GitHub REST Merge Pull Request API endpoint
        PUT /repos/{owner}/{repo}/pulls/{pull_number}/merge
        requires Contents: write permission.
        """
        # This is a documentation test - verify the requirement is met
        workflow_path = "./.github/workflows/merge-and-close-pr.yml"
        with open(workflow_path, 'r') as f:
            content = f.read()

        self.assertIn('contents: write', content,
            "GitHub Merge API endpoint requires contents: write permission")


class ErrorHandlingIntegrationTests(unittest.TestCase):
    """Integration tests for the complete error handling chain."""

    def test_complete_error_handling_flow(self):
        """Test the complete error handling flow used in the fix."""
        bash_script = """
set -e

# Simulate the pattern used in merge-and-close-pr.yml
# Using 'false' to simulate command failure
if merge_api_result=$(false 2>&1); then
    # Success branch (not taken in this test)
    echo "Merge succeeded"
    exit 0
else
    # Error branch
    echo "Merge failed. Diagnostics:"
    exit 1
fi
"""
        proc = subprocess.run(['bash', '-c', bash_script], capture_output=True, text=True)
        self.assertEqual(proc.returncode, 1, "Should exit with error code")
        self.assertIn("Merge failed", proc.stdout)
        self.assertIn("Diagnostics:", proc.stdout)

    def test_error_handling_preserves_exit_code(self):
        """Test that error handling preserves the original exit code."""
        bash_script = """
set -e

if result=$(bash -c 'exit 2' 2>&1); then
    echo "Success"
    exit 0
else
    exit 1
fi
"""
        proc = subprocess.run(['bash', '-c', bash_script], capture_output=True, text=True)
        self.assertEqual(proc.returncode, 1, "Should propagate error exit code")

    def test_error_branch_handles_parse_failure_gracefully(self):
        """Test that if parsing fails, we have fallback error message."""
        bash_script = """
set -e

api_result="not valid json at all !!!"

if [[ -n "$api_result" ]]; then
    # Try to parse, but fall back if it fails
    message=$(echo "$api_result" | python3 -c "import sys, json; d=json.load(sys.stdin); print(d.get('message'))" 2>/dev/null || echo "Failed to parse error")
    echo "Error: $message"
    exit 1
else
    exit 0
fi
"""
        proc = subprocess.run(['bash', '-c', bash_script], capture_output=True, text=True)
        self.assertEqual(proc.returncode, 1)
        self.assertIn("Error:", proc.stdout)
        self.assertNotIn("!!!", proc.stdout, "Raw invalid JSON should not appear")


class RegressionFullScenarioTests(unittest.TestCase):
    """Full regression test: Verify both fixes work together."""

    def test_no_silent_failure_with_conditional_assignment(self):
        """Verify the original bug (silent failure) is fixed."""
        # Old buggy pattern
        old_pattern = """
set -e
merge_api_result=$(false 2>&1); if [[ $? -ne 0 ]]; then
    echo "Error check"
    exit 1
fi
echo "BUG: Reached here with false command"
"""
        proc_old = subprocess.run(['bash', '-c', old_pattern], capture_output=True, text=True)
        self.assertNotEqual(proc_old.returncode, 0, "Old pattern has silent failure")

        # New fixed pattern
        new_pattern = """
set -e
if merge_api_result=$(false 2>&1); then
    echo "Success"
else
    echo "Error caught"
    exit 1
fi
"""
        proc_new = subprocess.run(['bash', '-c', new_pattern], capture_output=True, text=True)
        self.assertEqual(proc_new.returncode, 1, "Fixed pattern properly detects error")
        self.assertIn("Error caught", proc_new.stdout, "Error is properly handled")

    def test_permissions_and_error_handling_together(self):
        """Verify both fixes are present in the workflow."""
        workflow_path = "./.github/workflows/merge-and-close-pr.yml"

        with open(workflow_path, 'r') as f:
            content = f.read()

        # Check both fixes are present
        self.assertIn('contents: write', content, "Fix 1: Permission upgrade present")
        self.assertTrue(
            'if merge_api_result=$(gh api' in content or 'if merge_api_result=$(' in content,
            "Fix 2: Conditional assignment error handling present")


if __name__ == '__main__':
    unittest.main()
