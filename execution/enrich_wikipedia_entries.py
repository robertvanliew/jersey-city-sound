# Deepen the Wikipedia-sourced entries with real bio/career prose pulled from
# each subject's Wikipedia intro (via the API), replacing the placeholder
# "Listed in Wikipedia's category..." fact. Also removes Frank Sinatra Sr.
# (Hoboken-born resident; his JC-native children Nancy and Frank Jr. remain).
#
# Only touches entries whose facts still carry the generated placeholder, so
# hand-written entries (Joe Budden, Ransom, the scene DJs) are left intact.
#
# Usage:  py execution/enrich_wikipedia_entries.py

import json
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "entries.json"
UA = "TheJerseyCitySound/1.0 (archive research; jerseycitysound.com)"

PLACEHOLDER = "Listed in Wikipedia's category"

GENRE_KEYS = [
    ("hip hop", "Hip-hop"), ("hip-hop", "Hip-hop"), ("rapper", "Hip-hop"),
    ("jazz", "Jazz"), ("funk", "Funk"), ("soul", "Soul"),
    ("rhythm and blues", "R&B"), ("r&b", "R&B"), ("rock", "Rock"),
    ("punk", "Punk"), ("pop", "Pop"), ("disco", "Disco"),
    ("gospel", "Gospel"), ("blues", "Blues"), ("classical", "Classical"),
    ("folk", "Folk"), ("country", "Country"), ("metal", "Metal"),
    ("electronic", "Electronic"), ("house", "House"),
]


def title_from_url(url):
    m = re.search(r"/wiki/(.+)$", url or "")
    return urllib.parse.unquote(m.group(1)).replace("_", " ") if m else None


def clean(text):
    text = re.sub(r"\s*\([^)]*(?:listen|pronunciation|/[^)]*/)[^)]*\)", "", text, flags=re.I)
    text = re.sub(r"\[\d+\]", "", text)         # ref markers
    text = re.sub(r"\s+", " ", text).strip()
    return text


def first_sentences(text, n=3):
    text = clean(text)
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9\"'])", text)
    out, total = [], 0
    for p in parts:
        p = p.strip()
        if not p:
            continue
        out.append(p)
        total += len(p)
        if len(out) >= n or total > 480:
            break
    return out


def fetch_intros(titles):
    """{title: intro_plaintext} via the Wikipedia extracts API (batched)."""
    out = {}
    for i in range(0, len(titles), 20):
        batch = titles[i:i + 20]
        q = urllib.parse.urlencode({
            "action": "query", "format": "json", "prop": "extracts",
            "exintro": "1", "explaintext": "1", "exlimit": "20", "redirects": "1",
            "titles": "|".join(batch),
        })
        req = urllib.request.Request("https://en.wikipedia.org/w/api.php?" + q,
                                     headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=45) as r:
            data = json.loads(r.read().decode("utf-8"))
        query = data.get("query", {})
        alias = {}
        for norm in query.get("normalized", []):
            alias[norm["to"]] = norm["from"]
        for red in query.get("redirects", []):
            alias[red["to"]] = alias.get(red["from"], red["from"])
        for page in query.get("pages", {}).values():
            t = page.get("title", "")
            src = alias.get(t, t)
            if page.get("extract"):
                out[src] = page["extract"]
        time.sleep(0.3)
    return out


def main():
    d = json.loads(DATA.read_text(encoding="utf-8"))

    # 1) remove Frank Sinatra Sr. (keep Nancy + Frank Jr.)
    before = len(d["entries"])
    d["entries"] = [e for e in d["entries"] if e["slug"] != "frank-sinatra"]
    removed = before - len(d["entries"])

    # 2) targets: entries still carrying the placeholder fact + a Wikipedia source
    targets = []
    for e in d["entries"]:
        if not any(PLACEHOLDER in f for f in e.get("facts", [])):
            continue
        wurl = next((s.get("url") for s in e.get("sources", [])
                     if "wikipedia.org" in (s.get("url") or "")), None)
        t = title_from_url(wurl)
        if t:
            targets.append((e, t))

    print(f"removed {removed} (Sinatra Sr.); enriching {len(targets)} entries…")
    intros = fetch_intros([t for _, t in targets])

    enriched = 0
    for e, title in targets:
        intro = intros.get(title)
        if not intro:
            continue
        sents = first_sentences(intro, n=3)
        if not sents:
            continue
        # ensure the Jersey City tie is explicit
        joined = " ".join(sents)
        if "Jersey City" not in joined:
            sents.append(f"{e['name']} is documented among the notable "
                         f"{'musical groups' if e.get('type') == 'group' else 'musicians'} "
                         f"of Jersey City, New Jersey.")
        e["facts"] = [s if s.endswith((".", "!", "?", '"')) else s + "." for s in sents]

        # genre chips from the prose
        low = joined.lower()
        genres = []
        for key, g in GENRE_KEYS:
            if key in low and g not in genres:
                genres.append(g)
        if genres:
            e["genres"] = genres[:4]
        enriched += 1

    json.dump(d, open(DATA, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    misses = len(targets) - enriched
    print(f"enriched {enriched} entries ({misses} without an intro); "
          f"archive now {len(d['entries'])} entries")


if __name__ == "__main__":
    main()
