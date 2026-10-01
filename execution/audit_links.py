# Internal-link audit for the built site.
#
# Crawls every .html page under design/ (or a directory you pass), counts inbound
# links from OTHER pages, and reports pages with fewer than --min inbound links.
# Nav and footer links count, because they are real links, but a page reachable
# only from site chrome is still flagged separately so hub/related linking can
# be judged on its own.
#
# Usage:  py execution/audit_links.py [design_dir] [--min 3] [--json out.json]

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HREF = re.compile(r'<a\s[^>]*?href="([^"#?]+)(?:[#?][^"]*)?"', re.I)
CHROME = re.compile(r"<(header|footer|nav)\b.*?</\1>", re.I | re.S)


def audit(design_dir, minimum):
    pages = sorted(p.name for p in design_dir.glob("*.html"))
    page_set = set(pages)
    inbound = defaultdict(set)          # page -> set of pages linking to it (anywhere)
    inbound_body = defaultdict(set)     # page -> set of pages linking from body (not chrome)
    for name in pages:
        html = (design_dir / name).read_text(encoding="utf-8", errors="replace")
        body = CHROME.sub("", html)
        for scope, text in (("all", html), ("body", body)):
            for href in HREF.findall(text):
                href = href.strip()
                if href.startswith(("http", "mailto:", "//")):
                    continue
                target = href.lstrip("./") or "index.html"
                if target in page_set and target != name:
                    (inbound if scope == "all" else inbound_body)[target].add(name)
    report = []
    for name in pages:
        n_all, n_body = len(inbound[name]), len(inbound_body[name])
        if n_all < minimum or n_body < minimum:
            report.append({"page": name, "inbound": n_all, "inbound_from_body": n_body})
    return pages, inbound, inbound_body, report


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("design_dir", nargs="?", default=str(ROOT / "design"))
    ap.add_argument("--min", type=int, default=3)
    ap.add_argument("--json")
    a = ap.parse_args()
    design_dir = Path(a.design_dir)
    pages, inbound, inbound_body, report = audit(design_dir, a.min)
    zero = [r for r in report if r["inbound"] == 0]
    thin_body = [r for r in report if r["inbound_from_body"] < a.min]
    print(f"{len(pages)} pages in {design_dir}")
    print(f"{len(zero)} with zero inbound links; {len(thin_body)} with fewer than {a.min} "
          f"inbound links outside nav/footer")
    for r in sorted(report, key=lambda r: (r["inbound_from_body"], r["inbound"], r["page"])):
        print(f"  {r['inbound']:3d} total  {r['inbound_from_body']:3d} body   {r['page']}")
    if a.json:
        Path(a.json).write_text(json.dumps({
            "pages": len(pages), "min": a.min, "flagged": report,
            "inbound": {k: len(v) for k, v in inbound.items()},
            "inbound_from_body": {k: len(v) for k, v in inbound_body.items()},
        }, indent=1), encoding="utf-8")
    return 1 if thin_body else 0


if __name__ == "__main__":
    sys.exit(main())
