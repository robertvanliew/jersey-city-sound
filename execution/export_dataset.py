# Public dataset export: design/data/entries.json and design/data/entries.csv.
#
# The public JSON is the entries list only. The private research queue
# (discovered_candidates) and editor to-dos (todo_robert) are never exported.
# The CSV carries the record-card fields plus sources, one row per entry.
# Called by the generator on every build; safe to run alone.
#
# Usage:  py execution/export_dataset.py

import csv
import io
import json
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from entries_io import load_entries  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "design" / "data"
SITE = "https://jerseycitysound.com"
PRIVATE_FIELDS = {"todo_robert"}
LICENSE = "https://creativecommons.org/licenses/by-sa/4.0/"


def card(e, label):
    return next((c.get("value", "") for c in e.get("card", []) if c.get("label") == label), "")


def public_entry(e):
    out = {k: v for k, v in e.items() if k not in PRIVATE_FIELDS}
    out["url"] = f"{SITE}/entry-{e['slug']}.html"
    return out


def export(entries, handcrafted=()):
    OUT.mkdir(exist_ok=True)
    rows = [public_entry(e) for e in list(handcrafted) + entries]
    rows.sort(key=lambda r: r["entry_no"])
    payload = {
        "name": "The Jersey City Sound: entries",
        "description": "Every entry in the cited encyclopedia-archive of Jersey City, New Jersey music culture.",
        "license": LICENSE,
        "attribution": "The Jersey City Sound, jerseycitysound.com, CC BY-SA 4.0",
        "generated": date.today().isoformat(),
        "count": len(rows),
        "entries": rows,
    }
    (OUT / "entries.json").write_text(json.dumps(payload, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    fields = ["entry_no", "name", "slug", "type", "roles", "genres", "years_active", "real_name", "born",
              "raised", "died", "origin", "neighborhoods", "known_for", "crew_or_label", "born_in_jersey_city",
              "notability", "status", "address", "lat", "lng", "url", "sources"]
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=fields, lineterminator="\n")
    w.writeheader()
    for e in rows:
        w.writerow({
            "entry_no": e["entry_no"], "name": e["name"], "slug": e["slug"], "type": e.get("type") or "person",
            "roles": "; ".join(e.get("roles") or []), "genres": "; ".join(e.get("genres") or []),
            "years_active": e.get("years_active") or "", "real_name": card(e, "Real name"),
            "born": card(e, "Born"), "raised": card(e, "Raised"), "died": card(e, "Died"),
            "origin": e.get("origin") or "", "neighborhoods": "; ".join(e.get("neighborhoods") or []),
            "known_for": e.get("known_for") or card(e, "Known for"),
            "crew_or_label": "; ".join(v for v in (card(e, "Crew"), card(e, "Label"), card(e, "Group"), card(e, "Band")) if v),
            "born_in_jersey_city": "true" if e.get("born_in_jersey_city") else "",
            "notability": e.get("notability") or "", "status": e.get("status") or "",
            "address": e.get("address") or "", "lat": e.get("lat") if e.get("lat") is not None else "",
            "lng": e.get("lng") if e.get("lng") is not None else "", "url": e["url"],
            "sources": " | ".join((s.get("label", "") + (f" <{s['url']}>" if s.get("url") else "")) for s in e.get("sources", [])),
        })
    (OUT / "entries.csv").write_text("﻿" + buf.getvalue(), encoding="utf-8")   # BOM so Excel reads UTF-8
    return len(rows)


if __name__ == "__main__":
    n = export(load_entries()["entries"])
    print(f"exported {n} entries to design/data/entries.json and entries.csv")
