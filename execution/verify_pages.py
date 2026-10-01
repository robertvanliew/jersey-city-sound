# Raw-HTML checks across the built site (no browser): one H1, a self-referencing
# https non-www canonical, no accidental noindex, title and meta description present,
# unique and within length, JSON-LD that parses and carries the expected types, alt
# text on every image, a visible "Last updated" line. Prints a summary and every
# failure. Exit code 1 when any check fails on an indexable page.
#
# Usage:  py execution/verify_pages.py [--max-title 60] [--max-meta 155]

import argparse
import html as htmlmod
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DESIGN = ROOT / "design"
SITE = "https://jerseycitysound.com"
INTENTIONAL_NOINDEX = {"claim.html", "suggest-edit.html", "404.html"}


def check(name, s, max_title, max_meta):
    errs = []
    noindex = bool(re.search(r'<meta name="robots" content="noindex', s))
    if noindex:
        if name not in INTENTIONAL_NOINDEX and not re.match(r"report-\d{3}-", name):
            errs.append("unexpected noindex")
        return errs, noindex, None, None
    h1 = len(re.findall(r"<h1\b", s))
    if h1 != 1:
        errs.append(f"{h1} h1 elements")
    m = re.search(r'<link rel="canonical" href="([^"]+)"', s)
    expected = f"{SITE}/" if name == "index.html" else f"{SITE}/{name}"
    if not m:
        errs.append("no canonical")
    elif m.group(1) != expected:
        errs.append(f"canonical {m.group(1)} != {expected}")
    t = re.search(r"<title>(.*?)</title>", s, re.S)
    title = htmlmod.unescape(t.group(1).strip()) if t else ""
    if not title:
        errs.append("no title")
    elif len(title) > max_title:
        errs.append(f"title {len(title)} chars")
    d = re.search(r'<meta name="description" content="([^"]*)"', s)
    desc = htmlmod.unescape(d.group(1)) if d else ""
    if not desc:
        errs.append("no meta description")
    elif len(desc) > max_meta:
        errs.append(f"meta {len(desc)} chars")
    blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S)
    types = set()
    for b in blocks:
        try:
            ld = json.loads(b)
        except json.JSONDecodeError as ex:
            errs.append(f"json-ld parse error: {ex}")
            continue
        nodes = ld.get("@graph", [ld]) if isinstance(ld, dict) else ld
        for n in nodes:
            tt = n.get("@type")
            for x in (tt if isinstance(tt, list) else [tt]):
                if x:
                    types.add(x)
    if name.startswith("entry-"):
        if not ({"Person", "MusicGroup", "Place", "Movie", "MusicStore", "Organization"} & types):
            errs.append(f"entry schema missing main type ({sorted(types)})")
        if "BreadcrumbList" not in types:
            errs.append("entry schema missing BreadcrumbList")
    for img in re.findall(r"<img\b[^>]*>", s):
        if not re.search(r'\balt="', img):
            errs.append("img without alt: " + img[:60])
            break
    if "Last updated" not in s and name not in ("index.html", "404.html"):
        errs.append("no 'Last updated' line")
    return errs, noindex, title, desc


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-title", type=int, default=60)
    ap.add_argument("--max-meta", type=int, default=155)
    a = ap.parse_args()
    pages = sorted(p.name for p in DESIGN.glob("*.html"))
    titles, descs, failures, skipped = Counter(), Counter(), {}, 0
    for name in pages:
        s = (DESIGN / name).read_text(encoding="utf-8", errors="replace")
        errs, noindex, title, desc = check(name, s, a.max_title, a.max_meta)
        if noindex and not errs:
            skipped += 1
            continue
        if title:
            titles[title] += 1
        if desc:
            descs[desc] += 1
        if errs:
            failures[name] = errs
    dup_t = [t for t, c in titles.items() if c > 1]
    dup_d = [d for d, c in descs.items() if c > 1]
    print(f"{len(pages)} pages checked ({skipped} noindex skipped); {len(failures)} with failures; "
          f"{len(dup_t)} duplicate titles; {len(dup_d)} duplicate descriptions")
    for name, errs in failures.items():
        print(f"  {name}: " + "; ".join(errs))
    for t in dup_t:
        print(f"  duplicate title: {t}")
    for d in dup_d:
        print(f"  duplicate description: {d[:90]}")
    return 1 if (failures or dup_t or dup_d) else 0


if __name__ == "__main__":
    sys.exit(main())
