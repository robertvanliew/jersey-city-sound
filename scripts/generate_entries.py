#!/usr/bin/env python3
"""The Jersey City Sound — entry generator.
Reads data/entries.json, writes one Markdown entry per person into entries/,
matching the anatomy in JERSEY-CITY-SOUND-DESIGN-SPEC.md (frontmatter feeds
Astro + JSON-LD later). Safe to re-run: regenerates every entry from data.
"""
import json, pathlib, datetime

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = json.loads((ROOT / "data" / "entries.json").read_text(encoding="utf-8"))
OUT = ROOT / "entries"
OUT.mkdir(exist_ok=True)
today = datetime.date.today().isoformat()

TEMPLATE = """---
entry_no: "{entry_no}"
title: "{name}"
slug: "{slug}"
roles: {roles}
genres: {genres}
years_active: "{years_active}"
status: "{status}"            # web-verified | needs-local-verification | published
last_updated: "{today}"
author: "R. Van Liew"
draft: true
---

# {name}

<!-- LEAD: 40–60 words, self-contained. Who they are + Jersey City + role + era.
     This is the passage AI systems will quote. Write it last. -->

{lead}

## Career

{career}

## Notable Works & Credits

{works}

## Sources

{sources}

## Editor's Notes (remove before publishing)

{todos}
"""

def bullets(items, empty="- _To be completed from local knowledge._"):
    return "\n".join(f"- {i}" for i in items) if items else empty

for e in DATA["entries"]:
    lead = ("_" + e["name"] + " is a Jersey City DJ. Entry pending completion — "
            "see Editor's Notes._")
    career = bullets(e["facts"])
    works = "- _Pull from facts above / add releases, residencies, mixtapes._"
    sources = ("\n".join(
               f"{i+1}. [{s['label']}]({s['url']})" if s.get("url")
               else f"{i+1}. {s['label']}"
               for i, s in enumerate(e["sources"]))
               or "_No web sources yet — entry rests on local verification until receipts are added._")
    todos = bullets(e.get("todo_robert", []), empty="- None")
    body = TEMPLATE.format(
        entry_no=e["entry_no"], name=e["name"], slug=e["slug"],
        roles=json.dumps(e["roles"]), genres=json.dumps(e["genres"]),
        years_active=e["years_active"], status=e["status"], today=today,
        lead=lead, career=career, works=works, sources=sources, todos=todos)
    (OUT / f"{e['slug']}.md").write_text(body, encoding="utf-8")
    print(f"wrote entries/{e['slug']}.md  [{e['status']}]")

print(f"\n{len(DATA['entries'])} entries generated.")
