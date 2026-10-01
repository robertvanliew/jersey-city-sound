# Fill hub-tag fields on entries from the sourced text already in each entry.
#
# Fields (snake_case, matching the rest of entries.json):
#   neighborhoods        list; from explicit neighborhood names in facts/card/origin
#   born_in_jersey_city  true only when the text says born in / native of Jersey City
#   notability           "national" when the entry has a chart record, a confirmed
#                        Wikipedia/Wikidata identity, or a Wikipedia source; otherwise
#                        left unset for the editor (local vs regional is a judgment)
# Existing values are never overwritten. Prints a report of what it set and what
# is still missing. Nothing is inferred beyond the entry's own wording.
#
# Usage:  py execution/tag_entries.py [--dry-run]

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from entries_io import load_entries, save_entries  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent

# Text that names a neighborhood -> the hub it belongs to. Only explicit names and
# containments that are not in doubt; streets, parks and projects whose neighborhood
# could be argued are left for the editor.
NEIGHBORHOODS = {
    "Greenville": "Greenville", "Curries Woods": "Greenville",
    "The Heights": "The Heights", "Jersey City Heights": "The Heights",
    "Journal Square": "Journal Square",
    "Bergen-Lafayette": "Bergen-Lafayette", "Communipaw": "Bergen-Lafayette",
    "Downtown Jersey City": "Downtown", "Hamilton Park": "Downtown", "Paulus Hook": "Downtown",
    "West Side": "West Side",
    "McGinley Square": "McGinley Square",
}
# place names seen in the data that need an editor's call on neighborhood
UNRESOLVED_PLACES = ["Duncan", "Park Street", "Audubon Park", "Ocean Avenue", "Bergen Avenue",
                     "Marion", "Armstrong Park", "The Hill", "Lafayette"]

BORN_RE = re.compile(r"\bborn\b[^.]{0,80}?\bin Jersey City|\bJersey City native\b|\bnative of Jersey City\b", re.I)


def entry_text(e):
    return " ".join((e.get("facts") or []) + [c.get("value", "") for c in e.get("card", [])]
                    + [e.get("origin") or ""])


def main():
    dry = "--dry-run" in sys.argv
    data = load_entries()
    entries = data["entries"]
    charts = json.loads((ROOT / "data" / "chart-data.json").read_text(encoding="utf-8"))
    sameas = json.loads((ROOT / "data" / "sameas.json").read_text(encoding="utf-8"))
    set_n = set_b = set_not = 0
    missing_not, unresolved = [], []
    for e in entries:
        text = entry_text(e)
        key = f"entry-{e['slug']}"
        if "neighborhoods" not in e:
            found = []
            for needle, hub in NEIGHBORHOODS.items():
                if re.search(rf"(?<!\w){re.escape(needle)}(?!\w)", text) and hub not in found:
                    found.append(hub)
            if found:
                e["neighborhoods"] = found
                set_n += 1
            hits = [p for p in UNRESOLVED_PLACES if re.search(rf"(?<!\w){re.escape(p)}(?!\w)", text)]
            if hits and not found:
                unresolved.append((e["name"], hits))
        if "born_in_jersey_city" not in e:
            born_card = next((c.get("value", "") for c in e.get("card", []) if c.get("label") == "Born"), "")
            if BORN_RE.search(text) or "jersey city" in born_card.lower():
                e["born_in_jersey_city"] = True
                set_b += 1
        if "notability" not in e:
            charted = bool((charts.get(f"{key}.html") or charts.get(key) or {}).get("render"))
            wiki_id = (sameas.get(key) or {}).get("confidence") == "confirmed"
            wiki_src = any("wikipedia.org" in (s.get("url") or "") for s in e.get("sources", []))
            if charted or wiki_id or wiki_src:
                e["notability"] = "national"
                set_not += 1
            else:
                missing_not.append(e["name"])
    print(f"neighborhoods set: {set_n}   born_in_jersey_city set: {set_b}   notability set: {set_not}")
    print(f"\n{len(missing_not)} entries with no notability value (editor: local / regional / national):")
    print("  " + ", ".join(missing_not))
    print(f"\n{len(unresolved)} entries name a place whose neighborhood needs an editor's call:")
    for name, hits in unresolved:
        print(f"  {name}: {', '.join(hits)}")
    if not dry:
        save_entries(data)
        print("\nsaved data/entries.json")


if __name__ == "__main__":
    main()
