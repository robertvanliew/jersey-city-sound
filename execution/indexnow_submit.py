# Submit changed URLs to IndexNow (Bing, Yandex, Naver, Seznam, Yep share one endpoint).
#
# Google does not use IndexNow; the sitemap and Search Console still cover Google.
# The key is the public key file already served from the web root
# (design/<32 hex chars>.txt, whose content is the key), so nothing secret is needed.
#
# Which URLs:
#   --since <git-ref>   pages under design/ changed between <git-ref> and HEAD (CI uses
#                       the pre-push SHA), plus the sitemap itself
#   --all               every URL in design/sitemap.xml (use sparingly; fine after a
#                       template change that touched every page)
#   --urls a.html b.html ...
# Add --dry-run to print the payload without sending. Only run after the pages are
# live; IndexNow fetches the URLs and ignores ones that 404.
#
# Usage:  py execution/indexnow_submit.py --since abc123
#         py execution/indexnow_submit.py --all --dry-run

import argparse
import json
import re
import subprocess
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DESIGN = ROOT / "design"
SITE = "https://jerseycitysound.com"
HOST = "jerseycitysound.com"
ENDPOINT = "https://api.indexnow.org/indexnow"
BATCH = 10000   # IndexNow's per-request ceiling


def find_key():
    for f in DESIGN.glob("*.txt"):
        if re.fullmatch(r"[0-9a-f]{32}", f.stem):
            key = f.read_text(encoding="utf-8").strip()
            if key == f.stem:
                return key, f"{SITE}/{f.name}"
    sys.exit("no IndexNow key file in design/ (expected <key>.txt containing the key)")


def url_for(rel):
    rel = rel.replace("\\", "/")
    if rel.startswith("design/"):
        rel = rel[len("design/"):]
    return f"{SITE}/" if rel == "index.html" else f"{SITE}/{rel}"


def sitemap_urls():
    xml = (DESIGN / "sitemap.xml").read_text(encoding="utf-8")
    return re.findall(r"<loc>([^<]+)</loc>", xml)


def changed_since(ref):
    out = subprocess.run(["git", "diff", "--name-only", "--diff-filter=AMR", f"{ref}..HEAD", "--", "design"],
                         cwd=ROOT, check=True, capture_output=True, text=True).stdout
    files = [f for f in out.split("\n") if f.endswith(".html") and not f.endswith("/404.html")]
    urls = [url_for(f) for f in files]
    if urls:
        urls.append(f"{SITE}/sitemap.xml")
    return urls


def submit(urls, key, key_location, dry_run):
    payload = {"host": HOST, "key": key, "keyLocation": key_location, "urlList": urls}
    if dry_run:
        print(json.dumps(payload, indent=1))
        return 0
    req = urllib.request.Request(ENDPOINT, data=json.dumps(payload).encode("utf-8"),
                                 headers={"Content-Type": "application/json; charset=utf-8"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            print(f"IndexNow: HTTP {resp.status} for {len(urls)} URLs")
            return 0
    except urllib.error.HTTPError as e:
        # 200 OK, 202 Accepted (key validation pending), 400 bad request, 403 key invalid,
        # 422 URLs not on host, 429 too many requests
        print(f"IndexNow: HTTP {e.code} {e.reason}: {e.read().decode('utf-8', 'replace')[:300]}")
        return 1


def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--since", metavar="GIT_REF")
    g.add_argument("--all", action="store_true")
    g.add_argument("--urls", nargs="+")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    if a.all:
        urls = sitemap_urls()
    elif a.urls:
        urls = [u if u.startswith("http") else url_for(u) for u in a.urls]
    else:
        urls = changed_since(a.since)
    urls = sorted(set(urls))
    if not urls:
        print("IndexNow: nothing changed, nothing sent")
        return 0
    key, key_location = find_key()
    rc = 0
    for i in range(0, len(urls), BATCH):
        rc |= submit(urls[i:i + BATCH], key, key_location, a.dry_run)
    return rc


if __name__ == "__main__":
    sys.exit(main())
