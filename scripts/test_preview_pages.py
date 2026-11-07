import tempfile
import unittest
from pathlib import Path

import build_preview_pages as b
import validate_preview_site as v

class PreviewTests(unittest.TestCase):
    def test_generated_pages_in_sync_with_canonical(self):
        self.assertEqual(b.main(["--check"]), 0)

    def test_canonical_vault_is_flat_and_has_no_stale_md_links(self):
        names = sorted(p.name for p in b.VAULT.iterdir())
        self.assertEqual(names, ["NYCU_OS_LEC08.md", "NYCU_OS_LEC09.md", "_attachments"])
        for n in b.LECTURES:
            text = (b.VAULT / f"NYCU_OS_LEC{n}.md").read_text(encoding="utf-8")
            self.assertNotIn("NYCU_OS_LEC08.md)", text)
            self.assertNotIn("../lec0", text)
        self.assertEqual(len(list((b.VAULT / "_attachments").glob("*.svg"))), 8)

    def test_unknown_anchor_and_note_rejected(self):
        texts = {"NYCU_OS_LEC08": "# a\n[[NYCU_OS_LEC09#nope|x]]\n", "NYCU_OS_LEC09": "# b\n"}
        with self.assertRaises(ValueError):
            b.convert("NYCU_OS_LEC08", texts["NYCU_OS_LEC08"], texts)
        texts["NYCU_OS_LEC08"] = "# a\n[[Other]]\n"
        with self.assertRaises(ValueError):
            b.convert("NYCU_OS_LEC08", texts["NYCU_OS_LEC08"], texts)

    def test_wikilink_in_code_fence_untouched_and_banner_added(self):
        texts = {"NYCU_OS_LEC08": "# T\n```\n[[X]]\n```\n[[NYCU_OS_LEC09|L9]]\n", "NYCU_OS_LEC09": "# b\n"}
        out = b.convert("NYCU_OS_LEC08", texts["NYCU_OS_LEC08"], texts)
        self.assertIn("[[X]]", out)
        self.assertIn("[L9](../lec09/index.md)", out)
        self.assertIn("DRAFT — Under Learning Review", out)

    def test_validator_catches_broken_anchor_and_raw_wikilink(self):
        with tempfile.TemporaryDirectory() as d:
            for n, other in (("lec08", "lec09"), ("lec09", "lec08")):
                p = Path(d, "preview", n); (p / "_attachments").mkdir(parents=True)
                imgs = ""
                for i in range(4):
                    (p / "_attachments" / f"{i}.svg").write_text("<svg/>")
                    imgs += f'<img src="_attachments/{i}.svg">'
                bad = '<a href="../lec09/#missing">x</a>[[Raw]]' if n == "lec08" else ""
                (p / "index.html").write_text(f'DRAFT — Under Learning Review {imgs}<a href="../{other}/">o</a>{bad}')
            probs, _ = v.validate(d)
            self.assertTrue(any("missing anchor" in x for x in probs))
            self.assertTrue(any("raw WikiLink" in x for x in probs))

if __name__ == "__main__":
    unittest.main()
