# Promote the staged Wikipedia notables (discovered_candidates.wikipedia_notables)
# into full archive entries, fetching each subject's short description from the
# Wikipedia API so every entry carries a real, cited lead.
#
# Safe to re-run: skips any name whose slug already has an entry.
#
# Usage:  py execution/import_wikipedia_entries.py

import json
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "entries.json"
UA = "TheJerseyCitySound/1.0 (archive research; jerseycitysound.com)"

# Subjects who are Jersey City residents/associates rather than natives.
RESIDENT_NOTE = {
    "Frank Sinatra": "resided in Jersey City after his marriage to Nancy Barbato (born in Hoboken)",
}


def slugify(name):
    s = re.sub(r"\s*\([^)]*\)", "", name)          # drop disambiguation parenthetical
    s = s.lower().replace("&", "and").replace(".", "").replace("'", "").replace('"', "")
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s


def display_name(name):
    return re.sub(r"\s*\([^)]*\)", "", name).strip()


def role_hint(name):
    m = re.search(r"\(([^)]*)\)", name)
    if not m:
        return None
    tag = m.group(1).lower()
    for key, role in [("rapper", "Rapper"), ("band", "Musical group"),
                      ("pianist", "Pianist"), ("saxophonist", "Saxophonist"),
                      ("singer", "Singer"), ("producer", "Producer"),
                      ("musician", "Musician")]:
        if key in tag:
            return role
    return None


def fetch_descriptions(titles):
    """Return {title: short_description} via the Wikipedia query API (batched)."""
    out = {}
    for i in range(0, len(titles), 40):
        batch = titles[i:i + 40]
        q = urllib.parse.urlencode({
            "action": "query", "format": "json", "prop": "description",
            "titles": "|".join(batch), "redirects": "1",
        })
        req = urllib.request.Request("https://en.wikipedia.org/w/api.php?" + q,
                                     headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=30) as r:
            data = json.loads(r.read().decode("utf-8"))
        query = data.get("query", {})
        # map any redirected/normalized titles back to what we asked for
        alias = {}
        for norm in query.get("normalized", []):
            alias[norm["to"]] = norm["from"]
        for red in query.get("redirects", []):
            alias[red["to"]] = alias.get(red["from"], red["from"])
        for page in query.get("pages", {}).values():
            t = page.get("title", "")
            src = alias.get(t, t)
            desc = page.get("description")
            if desc:
                out[src] = desc
        time.sleep(0.3)
    return out


def main():
    d = json.loads(DATA.read_text(encoding="utf-8"))
    existing_slugs = {e["slug"] for e in d["entries"]}
    existing_names = {e["name"].lower() for e in d["entries"]}
    next_no = max(int(e["entry_no"]) for e in d["entries"]) + 1

    wn = d["discovered_candidates"]["wikipedia_notables"]
    buckets = [
        ("musicians", "person", []),
        ("groups", "group", []),
        ("rappers", "person", ["Rapper"]),
    ]
    items = []  # (wiki_title, type, default_roles)
    for key, etype, roles in buckets:
        for rec in wn.get(key, []):
            items.append((rec["name"], etype, roles))
    for rec in wn.get("from_people_list", {}).get("names", []):
        items.append((rec["name"], "person", []))

    # de-dup by slug, skip anything already an entry
    seen = set()
    todo = []
    for wiki_title, etype, roles in items:
        slug = slugify(wiki_title)
        dname = display_name(wiki_title)
        if slug in existing_slugs or slug in seen or dname.lower() in existing_names:
            continue
        seen.add(slug)
        todo.append((wiki_title, dname, slug, etype, roles))

    print(f"fetching descriptions for {len(todo)} subjects…")
    descs = fetch_descriptions([t[0] for t in todo])

    added = 0
    for wiki_title, dname, slug, etype, roles in todo:
        desc = descs.get(wiki_title, "")
        roles = list(roles)
        if not roles:
            hint = role_hint(wiki_title)
            roles = [hint] if hint else (["Musical group"] if etype == "group" else ["Musician"])

        wiki_url = "https://en.wikipedia.org/wiki/" + wiki_title.replace(" ", "_")
        desc_clean = desc.strip().rstrip(".") if desc else ""

        if dname in RESIDENT_NOTE:
            lead = (f"{dname}" + (f" is {article(desc_clean)} {desc_clean}." if desc_clean else ".")
                    + f" {dname} {RESIDENT_NOTE[dname]}, and is documented among the notable "
                      f"musicians associated with Jersey City, New Jersey.")
        elif etype == "group":
            lead = ((f"{dname} is {article(desc_clean)} {desc_clean} " if desc_clean
                     else f"{dname} is a musical group ")
                    + "from Jersey City, New Jersey.")
        else:
            lead = ((f"{dname} is {article(desc_clean)} {desc_clean} " if desc_clean
                     else f"{dname} is a musician ")
                    + "from Jersey City, New Jersey.")

        entry = {
            "entry_no": f"{next_no:03d}",
            "name": dname,
            "slug": slug,
            "status": "web-verified",
            "roles": roles,
            "genres": [],
            "years_active": "",
            "facts": [
                lead,
                f"Listed in Wikipedia's category of {'musical groups' if etype=='group' else 'musicians'} "
                f"from Jersey City, New Jersey.",
            ],
            "sources": [
                {"label": f"Wikipedia — {dname}", "url": wiki_url},
                {"label": "Archive research: The Jersey City Sound, 2026"},
            ],
            "todo_robert": ["Local detail, scene connections, and receipts from memory",
                            "Photo permission", "Confirm Jersey City ties and era"],
            "links": {},
        }
        if etype == "group":
            entry["type"] = "group"
        d["entries"].append(entry)
        next_no += 1
        added += 1

    json.dump(d, open(DATA, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(f"added {added} entries; archive now {len(d['entries'])} entries "
          f"(missing descriptions: {len(todo) - len([t for t in todo if t[0] in descs])})")


def article(word):
    return "an" if word[:1].lower() in "aeiou" else "a"


if __name__ == "__main__":
    main()
