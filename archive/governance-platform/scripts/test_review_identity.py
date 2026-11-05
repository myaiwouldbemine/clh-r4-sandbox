import unittest
from review_identity import review_gate
from merge_lifecycle import State, merge_blockers

class IdentityTests(unittest.TestCase):
    def setUp(self):
        self.c = dict(risk=1, repository="fixture/repo", pr=5, head="a"*40, base="b"*40, builder="codex", scope="sha256:fixture")
        self.a = {k:v for k,v in self.c.items() if k != "risk"}
        self.a.update(version=1, reviewer="claude", verdict="APPROVED", review_id=1)
        self.r = {agent:dict(agent=agent,kind="github_app",isolated=True,app_id=n,actor_id=n+10) for n,agent in enumerate(("codex","claude"),1)}
        self.f = dict(blocking_review=False,blocking_thread=False,builder_identity="codex",builder_verified=True,attestation_authenticated=True,issuer_app_id=2,review_actor_id=12,review_app_id=2,review_id=1,review_head="a"*40,review_state="APPROVED",complete_current_snapshot=True)
    def gate(self): return review_gate(self.c,self.a,self.r,self.f)
    def test_codex_builder(self): self.assertTrue(self.gate().startswith("PASS"))
    def test_claude_builder(self):
        self.c["builder"]=self.a["builder"]="claude"; self.a["reviewer"]="codex"
        self.f.update(builder_identity="claude",issuer_app_id=1,review_actor_id=11,review_app_id=1)
        self.assertTrue(self.gate().startswith("PASS"))
    def test_self_review(self):
        self.a["reviewer"]="codex"; self.assertTrue(self.gate().startswith("BLOCK"))
    def test_human_token(self):
        self.r["claude"]["kind"]="human"; self.assertTrue(self.gate().startswith("BLOCK"))
    def test_missing(self):
        self.a=None; self.assertTrue(self.gate().startswith("BLOCK"))
    def test_stale_context(self):
        for key in ("repository","pr","head","base","builder","scope"):
            original=self.a[key]; self.a[key]="stale"
            self.assertTrue(self.gate().startswith("BLOCK"),key); self.a[key]=original
    def test_negative_facts(self):
        for key,value in (("blocking_review",True),("blocking_thread",True),("review_state","CHANGES_REQUESTED"),("review_state","DISMISSED"),("attestation_authenticated",False),("issuer_app_id",99),("review_actor_id",99),("complete_current_snapshot",False),("builder_verified",False)):
            original=self.f[key]; self.f[key]=value
            self.assertTrue(self.gate().startswith("BLOCK"),key); self.f[key]=original
    def test_missing_fact(self):
        for key in list(self.f):
            value=self.f.pop(key); self.assertTrue(self.gate().startswith("BLOCK"),key); self.f[key]=value
    def test_shared_app(self):
        self.r["claude"]["app_id"]=1; self.assertTrue(self.gate().startswith("BLOCK"))
    def test_l2_l3(self):
        for risk in (2,3):
            self.c["risk"]=risk; self.assertTrue(self.gate().startswith("PASS"))
    def test_l0_only_exempts_review(self):
        self.c["risk"]=0; self.a=None
        self.assertTrue(self.gate().startswith("NOT_REQUIRED"))
        self.assertTrue(merge_blockers(State(risk=0)))
        self.f["blocking_thread"]=True
        self.assertTrue(self.gate().startswith("BLOCK"))
