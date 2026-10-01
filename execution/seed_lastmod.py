# Seed data/lastmod.json from git history (one-off; the generator maintains it after).
#
# For every entry, walks each commit that touched data/entries.json and records the
# date of the last commit in which that entry's JSON changed. Hand-edited pages get
# the date of their last commit. The report issue gets its date with a null hash,
# which tells the generator to adopt its current content hash without bumping.
#
# Usage:  py execution/seed_lastmod.py

import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DESIGN = ROOT / "design"
OUT = ROOT / "data" / "lastmod.json"

HAND_PAGES = ["index.html", "history.html", "chilltown.html", "jersey-city-djs.html",
              "report.html", "about.html", "verify.html", "privacy.html", "terms.html",
              "corrections.html", "entry-dj-dx.html"]


def git(*args):
    return subprocess.run(["git", *args], cwd=ROOT, check=True,
                          capture_output=True, text=True, encoding="utf-8").stdout


def entry_hash(e):
    return hashlib.sha256(json.dumps(e, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()


def main():
    lastmod = {}

    # entries: oldest commit first, so later changes overwrite earlier dates
    log = git("log", "--reverse", "--format=%H %cs", "--", "data/entries.json").split("\n")
    prev = {}
    for line in filter(None, log):
        sha, day = line.split()
        try:
            data = json.loads(git("show", f"{sha}:data/entries.json"))
        except (subprocess.CalledProcessError, json.JSONDecodeError):
            continue
        for e in data.get("entries", []):
            h = entry_hash(e)
            key = f"entry-{e['slug']}"
            if prev.get(key) != h:
                lastmod[key] = {"hash": h, "date": day}
                prev[key] = h
    # entries that no longer exist drop out
    current = json.loads((ROOT / "data" / "entries.json").read_text(encoding="utf-8"))["entries"]
    live = {f"entry-{e['slug']}" for e in current}
    lastmod = {k: v for k, v in lastmod.items() if k in live}
    for e in current:                       # uncommitted edits count as today
        key = f"entry-{e['slug']}"
        if key not in lastmod or lastmod[key]["hash"] != entry_hash(e):
            from datetime import date
            lastmod[key] = {"hash": entry_hash(e), "date": date.today().isoformat()}

    def file_record(path, rel):
        """Last commit date for the file; today if the working copy differs from HEAD."""
        from datetime import date
        h = hashlib.sha256(path.read_bytes()).hexdigest()
        committed = subprocess.run(["git", "diff", "--quiet", "HEAD", "--", rel],
                                   cwd=ROOT).returncode == 0   # line endings handled by git
        day = git("log", "-1", "--format=%cs", "--", rel).strip() if committed else ""
        return {"hash": h, "date": day or date.today().isoformat()}

    for name in HAND_PAGES:
        path = DESIGN / name
        if path.exists():
            lastmod[name] = file_record(path, f"design/{name}")
    lastmod["charts.html"] = file_record(ROOT / "data" / "chart-data.json", "data/chart-data.json")

    day = git("log", "-1", "--format=%cs", "--", "design/report-001-not-from-jersey-city.html").strip()
    if day:
        lastmod["report-001-not-from-jersey-city.html"] = {"hash": None, "date": day}

    OUT.write_text(json.dumps(lastmod, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    print(f"seeded {len(lastmod)} pages -> {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
