"""Prototype trusted-runtime adapter, never import/execute candidate PR code in service.
Only read-only GitHub calls. Trust/clock inputs belong to an isolated control plane.
No CLI, check publication, token provisioning or merge capability is provided.
"""
import base64
import hashlib
import json
import re
import subprocess
import tempfile
from pathlib import Path

from review_identity import review_gate


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode()


def authenticate(envelope, identity, now):
    """Ed25519 signature over canonical envelope excluding signature; pinned external key."""
    if set(envelope) != {"subject", "issued_at", "expires_at", "key_id", "signature"}:
        raise ValueError("envelope shape")
    key = identity["keys"][envelope["key_id"]]
    start, end = envelope["issued_at"], envelope["expires_at"]
    if (type(now) is not int or type(start) is not int or type(end) is not int
            or not start <= now < end or end - start > 300
            or key["revoked"] is not False or identity["revoked"] is not False):
        raise ValueError("expired, future or revoked")
    payload = {k: v for k, v in envelope.items() if k != "signature"}
    signature = base64.b64decode(envelope["signature"], validate=True)
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        (root / "key").write_text(key["public_pem"])
        (root / "data").write_bytes(canonical(payload))
        (root / "signature").write_bytes(signature)
        subprocess.run(
            ["openssl", "pkeyutl", "-verify", "-pubin", "-inkey", str(root / "key"),
             "-rawin", "-in", str(root / "data"), "-sigfile", str(root / "signature")],
            check=True, capture_output=True, timeout=10)
    return envelope["subject"]


class GitHubReadOnly:
    """gh OAuth is suitable for discovery only, never proof of Builder/Reviewer identity."""
    def rest(self, path):
        if not path.startswith("repos/") or ".." in path:
            raise ValueError("invalid API path")
        return json.loads(subprocess.run(
            ["gh", "api", "--method", "GET", path], check=True,
            capture_output=True, text=True, timeout=30).stdout)

    def threads(self, repository, pr):
        owner, name = repository.split("/")
        query = """query($owner:String!,$name:String!,$pr:Int!,$cursor:String){
          repository(owner:$owner,name:$name){pullRequest(number:$pr){
            reviewThreads(first:100,after:$cursor){totalCount
              nodes{id isResolved} pageInfo{hasNextPage endCursor}}}}}"""
        cursor, result, seen = None, [], set()
        for _ in range(101):
            body = {"query": query, "variables":
                    {"owner": owner, "name": name, "pr": pr, "cursor": cursor}}
            response = json.loads(subprocess.run(
                ["gh", "api", "graphql", "--input", "-"], input=json.dumps(body),
                check=True, capture_output=True, text=True, timeout=30).stdout)
            if response.get("errors"):
                raise ValueError("GraphQL partial response")
            page = response["data"]["repository"]["pullRequest"]["reviewThreads"]
            result.extend(page["nodes"])
            more = page["pageInfo"]["hasNextPage"]
            if type(more) is not bool:
                raise ValueError("missing pagination")
            if not more:
                if len(result) != page["totalCount"]:
                    raise ValueError("incomplete threads")
                return result
            cursor = page["pageInfo"]["endCursor"]
            if not cursor or cursor in seen:
                raise ValueError("pagination loop")
            seen.add(cursor)
        raise ValueError("thread pagination limit")


def pages(api, path):
    result = []
    for number in range(1, 102):
        page = api.rest(path + f"?per_page=100&page={number}")
        if not isinstance(page, list) or len(page) > 100:
            raise ValueError("invalid page")
        result.extend(page)
        if len(page) < 100:
            return result
    raise ValueError("pagination limit")


def snapshot(api, repository, pr):
    path = f"repos/{repository}/pulls/{pr}"
    pull = api.rest(path)
    if (pull["number"] != pr or pull["base"]["repo"]["full_name"] != repository
            or pull["state"] != "open"):
        raise ValueError("PR binding")
    head, base = pull["head"]["sha"], pull["base"]["sha"]
    if any(not re.fullmatch("[0-9a-f]{40}", sha) for sha in (head, base)):
        raise ValueError("invalid SHA")
    files = pages(api, path + "/files")
    # GitHub caps this endpoint at 3000. Refuse its cap, duplicates and missing data.
    if len(files) != pull["changed_files"] or len(files) >= 3000:
        raise ValueError("incomplete files")
    manifest = [{k: item[k] for k in ("filename", "sha", "status", "changes")}
                | {"previous_filename": item.get("previous_filename")} for item in files]
    if len({f["filename"] for f in manifest}) != len(files):
        raise ValueError("duplicate file")
    scope = "sha256:" + hashlib.sha256(canonical(
        {"repository": repository, "pr": pr, "head": head, "base": base,
         "files": sorted(manifest, key=lambda f: f["filename"])})).hexdigest()
    reviews = pages(api, path + "/reviews")
    threads = api.threads(repository, pr)
    if len({r["id"] for r in reviews}) != len(reviews):
        raise ValueError("duplicate review")
    if len({t["id"] for t in threads}) != len(threads):
        raise ValueError("duplicate thread")
    for review in reviews:
        if (review["state"] not in {"APPROVED", "CHANGES_REQUESTED", "COMMENTED", "DISMISSED", "PENDING"}
                or type(review["user"]["id"]) is not int or not review["submitted_at"]
                and review["state"] != "PENDING"):
            raise ValueError("unknown review")
    for thread in threads:
        if type(thread["isResolved"]) is not bool:
            raise ValueError("unknown thread")
    return dict(repository=repository, pr=pr, head=head, base=base, scope=scope,
                reviews=reviews, threads=threads)


def collect(api, repository, pr, risk, builder, registry, reviewer_envelope,
            builder_envelope, now):
    """registry/envelopes/clock supplied by trusted host; never PR files or HTTP flags.
    Each issuer key must be pinned out of band to verified App/actor/custody.
    PASS proves only this review component; Draft/authorization/CI gates remain separate.
    """
    try:
        if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repository):
            raise ValueError("repository")
        if type(pr) is not int or pr <= 0 or type(risk) is not int or risk not in range(4):
            raise ValueError("context")
        first = snapshot(api, repository, pr)
        context = {k: first[k] for k in ("repository", "pr", "head", "base", "scope")}
        context.update(risk=risk, builder=builder)
        # Conservative: retain every active change request, including older requests.
        facts = dict(
            blocking_review=any(r["state"] == "CHANGES_REQUESTED" for r in first["reviews"]),
            blocking_thread=any(not t["isResolved"] for t in first["threads"]))
        if risk != 0:
            a = reviewer_envelope["subject"]
            b, r = registry[builder], registry[a["reviewer"]]
            for identity in (b, r):
                for key in ("app_id", "actor_id"):
                    if type(identity[key]) is not int or identity[key] <= 0:
                        raise ValueError("invalid identity")
                if not isinstance(identity["custody"], str) or not identity["custody"] or identity["revoked"] is not False:
                    raise ValueError("custody/revocation")
            if b["custody"] == r["custody"]:
                raise ValueError("shared credential custody")
            if authenticate(reviewer_envelope, r, now()) != a:
                raise ValueError("review attestation")
            expected_builder = {k: context[k] for k in
                                ("repository", "pr", "head", "base", "scope", "builder")}
            expected_builder["purpose"] = "builder-provenance-v1"
            if authenticate(builder_envelope, b, now()) != expected_builder:
                raise ValueError("builder provenance")
            review = next(item for item in first["reviews"] if item["id"] == a["review_id"])
            decisive = [item for item in first["reviews"]
                        if item["user"]["id"] == r["actor_id"]
                        and item["state"] not in {"COMMENTED", "PENDING"}]
            if not decisive or max(decisive, key=lambda item: (item["submitted_at"], item["id"]))["id"] != review["id"]:
                raise ValueError("superseded review")
            if review["user"]["type"] != "Bot":
                raise ValueError("human review")
            # REST review has no trustworthy App ID. This association comes ONLY
            # from independently enrolled issuer key + pinned actor, never login.
            facts.update(builder_identity=builder, builder_verified=True,
                         attestation_authenticated=True, issuer_app_id=r["app_id"],
                         review_actor_id=review["user"]["id"], review_app_id=r["app_id"],
                         review_id=review["id"], review_head=review["commit_id"],
                         review_state=review["state"])
        # Recollect all mutable state, not merely head; API is not atomic.
        if first != snapshot(api, repository, pr):
            raise ValueError("snapshot changed")
        if risk != 0:
            # Check expiry again after network collection; now is the trusted host clock.
            authenticate(reviewer_envelope, r, now())
            authenticate(builder_envelope, b, now())
        facts["complete_current_snapshot"] = True
        return review_gate(context, None if risk == 0 else a, registry, facts)
    except (KeyError, TypeError, ValueError, StopIteration, OSError,
            subprocess.SubprocessError):
        return "BLOCK: unverified or incomplete collector evidence"
