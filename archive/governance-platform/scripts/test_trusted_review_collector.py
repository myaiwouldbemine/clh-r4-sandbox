"""SIMULATED only. Public deterministic fixture seeds are NOT service credentials."""
import base64
import copy
import subprocess
import tempfile
import unittest
from pathlib import Path

from trusted_review_collector import canonical, collect, pages, snapshot


class API:
    def __init__(self):
        self.pull = dict(number=5, state="open", changed_files=1,
                         head={"sha": "a"*40},
                         base={"sha": "b"*40, "repo": {"full_name": "fixture/repo"}})
        self.reviews = [dict(id=1, state="APPROVED", user={"id": 12, "type": "Bot"},
                             commit_id="a"*40, submitted_at="2026-11-05T00:00:00Z")]
        self.thread_list = []
        self.files = [dict(filename="test.py", sha="c"*40, status="modified", changes=1)]
        self.fail = False
        self.reads = 0
        self.race = False

    def rest(self, path):
        if self.fail:
            raise OSError("API failure")
        if "/reviews?" in path:
            return copy.deepcopy(self.reviews)
        if "/files?" in path:
            return copy.deepcopy(self.files)
        self.reads += 1
        result = copy.deepcopy(self.pull)
        if self.race and self.reads > 1:
            result["base"]["sha"] = "d"*40
        return result

    def threads(self, repository, pr):
        return copy.deepcopy(self.thread_list)


class CollectorTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.api = API()
        self.registry = {}
        self.private = {}
        for n, agent in enumerate(("codex", "claude"), 1):
            # PKCS8 Ed25519 seed encoding, fixed and intentionally public test material.
            der = bytes.fromhex("302e020100300506032b657004220420") + bytes([n])*32
            pem = "-----BEGIN PRIVATE KEY-----\n" + base64.b64encode(der).decode() + "\n-----END PRIVATE KEY-----\n"
            path = self.root / agent
            path.write_text(pem)
            public = subprocess.run(["openssl", "pkey", "-in", str(path), "-pubout"],
                                    capture_output=True, text=True, check=True).stdout
            self.private[agent] = path
            self.registry[agent] = dict(agent=agent, kind="github_app", isolated=True,
                app_id=n, actor_id=n+10, custody=agent, revoked=False,
                keys={"fixture": {"public_pem": public, "revoked": False}})
        state = snapshot(self.api, "fixture/repo", 5)
        self.context = {k: state[k] for k in ("repository", "pr", "head", "base", "scope")}
        self.context["builder"] = "codex"
        self.subject = dict(self.context, version=1, reviewer="claude",
                            verdict="APPROVED", review_id=1)
        self.builder = self.sign(dict(self.context, purpose="builder-provenance-v1"), "codex")
        self.review = self.sign(self.subject, "claude")

    def sign(self, subject, agent="claude", **updates):
        body = dict(subject=subject, issued_at=1000, expires_at=1200, key_id="fixture")
        body.update(updates)
        data, signature = self.root / "data", self.root / "signature"
        data.write_bytes(canonical(body))
        subprocess.run(["openssl", "pkeyutl", "-sign", "-inkey", str(self.private[agent]),
                        "-rawin", "-in", str(data), "-out", str(signature)], check=True,
                       capture_output=True)
        return dict(body, signature=base64.b64encode(signature.read_bytes()).decode())

    def gate(self, risk=1, now=1100):
        return collect(self.api, "fixture/repo", 5, risk, "codex", self.registry,
                       self.review, self.builder, lambda: now)

    def blocked(self):
        self.assertTrue(self.gate().startswith("BLOCK"))

    def test_valid_signed_independent_reviewer(self):
        self.assertTrue(self.gate().startswith("PASS"))

    def test_self_review(self):
        self.subject["reviewer"] = "codex"
        self.review = self.sign(self.subject, "codex")
        self.blocked()

    def test_shared_human_token(self):
        self.api.reviews[0]["user"].update(id=275012389, type="User")
        self.blocked()

    def test_forged_signature(self):
        self.review["subject"]["base"] = "d"*40
        self.blocked()

    def test_wrong_signer(self):
        self.review = self.sign(self.subject, "codex")
        self.blocked()

    def test_missing_reviewer(self):
        self.review = None
        self.blocked()

    def test_stale_head_base_scope(self):
        for field in ("head", "base", "scope", "repository", "pr"):
            with self.subTest(field=field):
                subject = dict(self.subject, **{field: "stale"})
                self.review = self.sign(subject)
                self.blocked()

    def test_dismissed_review(self):
        self.api.reviews[0]["state"] = "DISMISSED"
        self.blocked()

    def test_blocking_review(self):
        self.api.reviews.append(dict(self.api.reviews[0], id=2, state="CHANGES_REQUESTED"))
        self.blocked()

    def test_blocking_thread(self):
        self.api.thread_list = [{"id": "thread1", "isResolved": False}]
        self.blocked()

    def test_incomplete_collection(self):
        self.api.pull["changed_files"] = 2
        self.blocked()

    def test_api_failure(self):
        self.api.fail = True
        self.blocked()

    def test_revoked_identity_and_key(self):
        self.registry["claude"]["revoked"] = True
        self.blocked()
        self.registry["claude"]["revoked"] = False
        self.registry["claude"]["keys"]["fixture"]["revoked"] = True
        self.blocked()

    def test_expired_future_long_lived(self):
        for start, end in ((800, 1000), (1200, 1300), (1000, 2000)):
            self.review = self.sign(self.subject, issued_at=start, expires_at=end)
            self.blocked()

    def test_unknown_key(self):
        self.review["key_id"] = "not-enrolled"
        self.blocked()

    def test_builder_signature_and_binding(self):
        self.builder = self.sign(dict(self.context, purpose="builder-provenance-v1"))
        self.blocked()

    def test_shared_custody(self):
        self.registry["claude"]["custody"] = "codex"
        self.blocked()

    def test_wrong_native_actor(self):
        self.api.reviews[0]["user"]["id"] = 99
        self.blocked()

    def test_race(self):
        self.api.reads = 0
        self.api.race = True
        self.blocked()

    def test_unknown_review_thread(self):
        self.api.reviews[0]["state"] = "UNKNOWN"
        self.blocked()
        self.api.reviews[0]["state"] = "APPROVED"
        self.api.thread_list = [{"id": "thread1"}]
        self.blocked()

    def test_duplicate_reviews(self):
        self.api.reviews *= 2
        self.blocked()

    def test_l0_still_checks_blockers(self):
        self.review = self.builder = None
        self.assertTrue(self.gate(risk=0).startswith("NOT_REQUIRED"))
        self.api.thread_list = [{"id": "thread1", "isResolved": False}]
        self.assertTrue(self.gate(risk=0).startswith("BLOCK"))

    def test_full_rest_pagination(self):
        class Paginated:
            def rest(self, path):
                return list(range(100)) if path.endswith("&page=1") else []
        self.assertEqual(len(pages(Paginated(), "repos/fixture/reviews")), 100)

    def test_pagination_never_completes(self):
        class Truncated:
            def rest(self, path):
                return list(range(100))
        with self.assertRaises(ValueError):
            pages(Truncated(), "repos/fixture/reviews")

    def test_stale_native_commit(self):
        self.api.reviews[0]["commit_id"] = "d"*40
        self.blocked()

    def test_superseded_dismissal(self):
        self.api.reviews.append(dict(self.api.reviews[0], id=2, state="DISMISSED"))
        self.blocked()

    def test_reverse_roles(self):
        context = dict(self.context, builder="claude")
        self.api.reviews[0]["user"]["id"] = 11
        reviewer = self.sign(dict(context, version=1, reviewer="codex",
                                 verdict="APPROVED", review_id=1), "codex")
        builder = self.sign(dict(context, purpose="builder-provenance-v1"), "claude")
        result = collect(self.api, "fixture/repo", 5, 1, "claude", self.registry,
                         reviewer, builder, lambda: 1100)
        self.assertTrue(result.startswith("PASS"))

    def test_expiry_during_collection(self):
        times = iter((1100, 1100, 1200))
        result = collect(self.api, "fixture/repo", 5, 1, "codex", self.registry,
                         self.review, self.builder, lambda: next(times))
        self.assertTrue(result.startswith("BLOCK"))

    def test_graphql_pagination_and_errors(self):
        import json
        from types import SimpleNamespace
        from unittest.mock import patch
        from trusted_review_collector import GitHubReadOnly
        def response(nodes, more, cursor, count):
            connection = dict(nodes=nodes, totalCount=count,
                              pageInfo=dict(hasNextPage=more, endCursor=cursor))
            return SimpleNamespace(stdout=json.dumps({"data": {"repository": {
                "pullRequest": {"reviewThreads": connection}}}}))
        first = response([{"id": "a", "isResolved": True}], True, "next", 2)
        last = response([{"id": "b", "isResolved": True}], False, None, 2)
        with patch("trusted_review_collector.subprocess.run", side_effect=[first, last]):
            self.assertEqual(len(GitHubReadOnly().threads("fixture/repo", 5)), 2)
        with patch("trusted_review_collector.subprocess.run", return_value=SimpleNamespace(
                stdout=json.dumps({"errors": [{"message": "partial"}]}))):
            with self.assertRaises(ValueError):
                GitHubReadOnly().threads("fixture/repo", 5)
        with patch("trusted_review_collector.subprocess.run",
                   return_value=response([], False, None, 1)):
            with self.assertRaises(ValueError):
                GitHubReadOnly().threads("fixture/repo", 5)
