"""Derive MkDocs DRAFT preview pages from the flat canonical Obsidian notes (Issue 42).

Canonical source (edited by hand, one per lesson): OBSIDIAN_VAULT/NYCU_OS_LEC0N.md
Generated (never edit): docs/preview/lec0N/index.md + _attachments/*.svg

Usage: python scripts/build_preview_pages.py [--check]
  default  write generated pages
  --check  fail if generated pages differ from the canonical notes, or any link is broken
This script only converts links/paths and adds a DRAFT banner; it never changes lesson text.
"""
import argparse
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VAULT = ROOT / "OBSIDIAN_VAULT"
OUT = ROOT / "docs" / "preview"
LECTURES = ("08", "09")
NOTE = "NYCU_OS_LEC{}"
WIKILINK = re.compile(r"\[\[([^\]|#]+)(?:#([^\]|]+))?(?:\|([^\]]+))?\]\]")
HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*$")
IMAGE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
BANNER = (
    '!!! danger "DRAFT — Under Learning Review"\n'
    "    此頁為 **預覽草稿**，尚未通過 Human 教材語義核准，不是正式 Canonical 教材。"
    "原始 PDF 未公開。Learning Record #{issue} 仍為 OPEN。\n\n"
)
ISSUE = {"08": 26, "09": 41}


def split_front_matter(text):
    m = re.match(r"---\n.*?\n---\n", text, re.S)
    return (m.group(0), text[m.end():]) if m else ("", text)


def headings(text):
    """Heading texts outside fenced code blocks."""
    out, fenced = [], False
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            fenced = not fenced
        elif not fenced and (m := HEADING.match(line)):
            out.append(m.group(2))
    return out


def anchor_id(note, heading):
    """Stable ASCII id; Python-Markdown's default slug drops CJK so we state ids explicitly."""
    lec = note.rsplit("LEC", 1)[1]
    return f"lec{lec}-" + "".join(f"{ord(c):x}" for c in heading)[:60].lower() + f"-{len(heading)}"


def wikilink_targets(texts):
    """{note: {heading,...}} for every WikiLink; raises on unknown note/heading."""
    found = {}
    for text in texts.values():
        for note, head, _ in WIKILINK.findall(text):
            found.setdefault(note.strip(), set())
            if head:
                found[note.strip()].add(head.strip())
    return found


def convert(note, text, texts):
    own = {NOTE.format(n): n for n in LECTURES}
    wanted = wikilink_targets(texts)

    def link(m):
        target, head, label = m.group(1).strip(), (m.group(2) or "").strip(), m.group(3)
        if target not in own:
            raise ValueError(f"WikiLink to unknown note: {target}")
        if head and head not in headings(texts[target]):
            raise ValueError(f"WikiLink anchor not found in {target}: {head}")
        text_label = (label or head or target).strip()
        frag = f"#{anchor_id(target, head)}" if head else ""
        href = frag if target == note else f"../lec{own[target]}/index.md{frag}"
        return f"[{text_label}]({href})"

    fm, body = split_front_matter(text)
    lines, fenced = [], False
    for line in body.splitlines():
        if line.lstrip().startswith("```"):
            fenced = not fenced
        elif not fenced:
            line = WIKILINK.sub(link, line)
            hm = HEADING.match(line)
            if hm and hm.group(2) in wanted.get(note, set()):
                line = f"{line} {{ #{anchor_id(note, hm.group(2))} }}"
        lines.append(line)
    # banner right after the first H1 so it is visible above the fold
    out = "\n".join(lines) + "\n"
    out = re.sub(r"^(# .*\n)", lambda m: m.group(1) + "\n" + BANNER.format(issue=ISSUE[own[note]]), out, 1, re.M)
    return fm + out


def generate():
    texts = {NOTE.format(n): (VAULT / f"{NOTE.format(n)}.md").read_text(encoding="utf-8") for n in LECTURES}
    result = {}
    for n in LECTURES:
        note = NOTE.format(n)
        result[OUT / f"lec{n}" / "index.md"] = convert(note, texts[note], texts)
    return result


def svg_pairs():
    for n in LECTURES:
        for svg in sorted((VAULT / "_attachments").glob(f"lec{n}_*.svg")):
            yield svg, OUT / f"lec{n}" / "_attachments" / svg.name


def check_images():
    problems = []
    for n in LECTURES:
        text = (VAULT / f"{NOTE.format(n)}.md").read_text(encoding="utf-8")
        refs = [r for r in IMAGE.findall(text) if not r.startswith("http")]
        if len(refs) != 4:
            problems.append(f"LEC{n}: expected 4 SVG references, found {len(refs)}")
        for r in refs:
            if not r.endswith(".svg") or not (VAULT / r).is_file():
                problems.append(f"LEC{n}: missing/non-SVG image {r}")
    return problems


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args(argv)
    problems = check_images()
    pages = generate()
    if args.check:
        for path, content in pages.items():
            if not path.is_file() or path.read_text(encoding="utf-8") != content:
                problems.append(f"stale generated page: {path.relative_to(ROOT)}")
        for src, dst in svg_pairs():
            if not dst.is_file() or dst.read_bytes() != src.read_bytes():
                problems.append(f"stale generated asset: {dst.relative_to(ROOT)}")
    else:
        for path, content in pages.items():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
        for src, dst in svg_pairs():
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(src, dst)
    for p in problems:
        print("FAIL:", p)
    print("PASS" if not problems else "FAIL")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
# x
