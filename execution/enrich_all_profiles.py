# Full-archive profile pass: give every thin, Wikipedia-sourced entry a fuller,
# multi-paragraph bio pulled from its Wikipedia intro. Uses an abbreviation-safe
# sentence boundary so names like "P.M. Dawn" and "Heather B." are never split.
#
# Only touches entries that (a) cite Wikipedia and (b) currently have <= 2 facts,
# so hand-written rich entries (DJ DX, Mary Brown, Ransom, etc.) are left alone.
#
# Usage:  py execution/enrich_all_profiles.py

import json, re, time, urllib.parse, urllib.request
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data" / "entries.json"
UA = "TheJerseyCitySound/1.0 (archive research; jerseycitysound.com)"


def clean(t):
    t = re.sub(r"\s*\([^)]*(?:listen|pronunciation|/[^)]*/|born\s+[^)]*née[^)]*)\)", "", t, flags=re.I)
    t = re.sub(r"\[\d+\]", "", t)
    t = re.sub(r"[ \t]+", " ", t)
    return t.strip()


def sentence_cut(text, limit):
    """Return text trimmed to <= limit at a real sentence boundary.
    A boundary is '. ' where the period follows a lowercase letter, digit,
    or closing quote/paren — never a single capital (abbreviation)."""
    if len(text) <= limit:
        return text.strip()
    window = text[:limit]
    ends = [m.end() for m in re.finditer(r"(?<=[a-z0-9)\"'])\.\s", window)]
    if ends:
        return text[:ends[-1]].strip()
    # fallback: cut at last space
    return window.rsplit(" ", 1)[0].strip() + "…"


def to_facts(intro):
    intro = clean(intro)
    paras = [p.strip() for p in intro.split("\n") if p.strip()]
    facts = []
    if not paras:
        return facts
    facts.append(sentence_cut(paras[0], 520))
    # second paragraph, or a second slice of a single long paragraph
    if len(paras) > 1:
        facts.append(sentence_cut(paras[1], 460))
    else:
        rest = paras[0][len(facts[0]):].strip()
        if len(rest) > 80:
            facts.append(sentence_cut(rest, 460))
    return [f.rstrip() for f in facts if f]


def title_from(url):
    m = re.search(r"/wiki/(.+)$", url or "")
    return urllib.parse.unquote(m.group(1)).replace("_", " ") if m else None


def fetch_intros(titles):
    out = {}
    for i in range(0, len(titles), 18):
        batch = titles[i:i + 18]
        q = urllib.parse.urlencode({
            "action": "query", "format": "json", "prop": "extracts",
            "exintro": "1", "explaintext": "1", "exlimit": "20", "redirects": "1",
            "titles": "|".join(batch)})
        req = urllib.request.Request("https://en.wikipedia.org/w/api.php?" + q,
                                     headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=45) as r:
            data = json.loads(r.read().decode("utf-8"))
        query = data.get("query", {})
        alias = {}
        for n in query.get("normalized", []):
            alias[n["to"]] = n["from"]
        for red in query.get("redirects", []):
            alias[red["to"]] = alias.get(red["from"], red["from"])
        for page in query.get("pages", {}).values():
            if page.get("extract"):
                out[alias.get(page["title"], page["title"])] = page["extract"]
        time.sleep(0.3)
    return out


def main():
    d = json.loads(DATA.read_text(encoding="utf-8"))
    targets = []
    for e in d["entries"]:
        if len(e.get("facts", [])) > 2:
            continue
        wurl = next((s.get("url") for s in e.get("sources", [])
                     if "wikipedia.org" in (s.get("url") or "")), None)
        t = title_from(wurl)
        if t:
            targets.append((e, t))

    print(f"enriching {len(targets)} thin Wikipedia-sourced profiles…")
    intros = fetch_intros([t for _, t in targets])
    done = 0
    for e, title in targets:
        intro = intros.get(title)
        if not intro:
            continue
        facts = to_facts(intro)
        if facts and len(facts[0]) >= 40:
            e["facts"] = facts
            done += 1

    json.dump(d, open(DATA, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(f"enriched {done} profiles ({len(targets) - done} without a usable intro)")


if __name__ == "__main__":
    main()
