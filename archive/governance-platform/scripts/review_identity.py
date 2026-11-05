"""Offline policy evaluator. All arguments except attestation require trusted collection.
Never expose this function as an endpoint accepting caller-supplied registry or facts.
"""
FIELDS = {"version", "repository", "pr", "head", "base", "builder", "reviewer", "verdict", "scope", "review_id"}

def review_gate(context, attestation, registry, facts):
    try:
        if type(context["risk"]) is not int or context["risk"] not in range(4):
            return "BLOCK: unknown risk"
        if facts.get("blocking_review") is not False or facts.get("blocking_thread") is not False:
            return "BLOCK: blocking state unresolved or unknown"
        if context["risk"] == 0:
            return "NOT_REQUIRED: review only; other gates still apply"
        a = attestation
        if not isinstance(a, dict) or set(a) != FIELDS or type(a["version"]) is not int or a["version"] != 1:
            return "BLOCK: malformed attestation"
        if type(a["pr"]) is not int or a["pr"] <= 0 or type(a["review_id"]) is not int or a["review_id"] <= 0:
            return "BLOCK: invalid identifiers"
        for key in ("repository", "head", "base", "builder", "scope"):
            if not isinstance(a[key], str) or not a[key] or a[key] != context[key]:
                return "BLOCK: stale or mismatched context"
        if a["pr"] != context["pr"] or a["verdict"] != "APPROVED":
            return "BLOCK: PR or verdict"
        builder, reviewer = registry[a["builder"]], registry[a["reviewer"]]
        if {builder["agent"], reviewer["agent"]} != {"codex", "claude"}:
            return "BLOCK: self-review or unknown agent"
        for identity in (builder, reviewer):
            if identity["kind"] != "github_app" or identity["isolated"] is not True:
                return "BLOCK: untrusted identity"
        if builder["app_id"] == reviewer["app_id"] or builder["actor_id"] == reviewer["actor_id"]:
            return "BLOCK: shared identity"
        # Collector independently binds Builder provenance and fetches the current review.
        if facts["builder_identity"] != a["builder"] or facts["builder_verified"] is not True:
            return "BLOCK: builder provenance"
        if facts["attestation_authenticated"] is not True or facts["issuer_app_id"] != reviewer["app_id"]:
            return "BLOCK: unauthenticated attestation"
        if facts["review_actor_id"] != reviewer["actor_id"] or facts["review_app_id"] != reviewer["app_id"]:
            return "BLOCK: review issuer"
        if facts["review_id"] != a["review_id"] or facts["review_head"] != a["head"] or facts["review_state"] != "APPROVED":
            return "BLOCK: native review stale or not approved"
        if facts["complete_current_snapshot"] is not True:
            return "BLOCK: incomplete collection"
        return "PASS: independent review only"
    except (KeyError, TypeError, ValueError):
        return "BLOCK: missing or invalid evidence"
