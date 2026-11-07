"""Validate built preview HTML under site/preview (Issue 42). Run after `mkdocs build --strict`.
Checks: DRAFT label, no raw [[WikiLink]], 4 SVG <img> per lesson that exist, internal links and
fragments resolve, and LEC08<->LEC09 cross links exist. Usage: python scripts/validate_preview_site.py [site_dir]"""
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urldefrag, urlparse

class Page(HTMLParser):
    def __init__(self):
        super().__init__(); self.ids, self.links, self.imgs = set(), [], []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get("id"): self.ids.add(a["id"])
        if tag == "a" and a.get("href"): self.links.append(a["href"])
        if tag == "img" and a.get("src"): self.imgs.append(a["src"])

def parse(path):
    p = Page(); p.feed(path.read_text(encoding="utf-8")); return p

def validate(site):
    site, problems = Path(site), []
    pages = {n: site / "preview" / n / "index.html" for n in ("lec08", "lec09")}
    parsed = {}
    for n, f in pages.items():
        if not f.is_file():
            problems.append(f"missing {f}"); continue
        text = f.read_text(encoding="utf-8"); parsed[n] = parse(f)
        if "DRAFT — Under Learning Review" not in text: problems.append(f"{n}: no DRAFT label")
        if "[[" in text.replace("[[]]", ""): problems.append(f"{n}: raw WikiLink syntax in HTML")
        svgs = [s for s in parsed[n].imgs if s.endswith(".svg")]
        if len(svgs) != 4: problems.append(f"{n}: {len(svgs)} SVG images (expected 4)")
        for s in svgs:
            if not (f.parent / unquote(s)).is_file(): problems.append(f"{n}: SVG missing {s}")
    cross = {"lec08": 0, "lec09": 0}
    for n, p in parsed.items():
        for href in p.links:
            u = urlparse(href)
            if u.scheme or href.startswith("mailto:"): continue
            path, frag = urldefrag(href)
            target = pages[n] if not path else (pages[n].parent / unquote(path))
            if target.is_dir(): target = target / "index.html"
            target = target.resolve()
            if not target.is_file(): problems.append(f"{n}: broken link {href}"); continue
            if frag and target.suffix == ".html":
                ids = p.ids if target == pages[n].resolve() else parse(target).ids
                if frag not in ids: problems.append(f"{n}: missing anchor {href}")
            other = "lec09" if n == "lec08" else "lec08"
            if target == pages[other].resolve(): cross[n] += 1
    for n, c in cross.items():
        if c == 0: problems.append(f"{n}: no link to the other lecture")
    return problems, cross

if __name__ == "__main__":
    probs, cross = validate(sys.argv[1] if len(sys.argv) > 1 else "site")
    for x in probs: print("FAIL:", x)
    print(("PASS" if not probs else "FAIL"), "cross-links (from page):", cross)
    sys.exit(1 if probs else 0)
