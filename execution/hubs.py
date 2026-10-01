# Hub pages generated from data/entries.json: role, era, neighborhood, birthplace,
# genre and place hubs. Copy (intro paragraphs, FAQ, sources, research notes) lives
# in data/hubs.json so the editor can change wording without touching code.
#
# Every hub: H1 in the search phrasing, a 40 to 60 word direct answer as the lead,
# the sourced intro, every matching entry as a card in chronological then
# alphabetical order (never ranked), FAQ, sibling-hub links, sources, and
# CollectionPage + ItemList + FAQPage + BreadcrumbList JSON-LD.
#
# Imported by generate_entry_pages.py, which passes itself in as `g` so the hub
# writer can reuse its escaping, linking, shell and lastmod helpers.

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
COPY_FILE = ROOT / "data" / "hubs.json"

RAP_ROLE = re.compile(r"\b(rapper|mc|emcee|rap|hip-hop (group|crew|duo|collective|artist))\b", re.I)
DJ_ROLE = re.compile(r"\bdj\b", re.I)

ERAS = [  # key, label, decade test
    ("pre-1960s", "Before 1960", lambda d: d < 1960),
    ("1960s", "the 1960s", lambda d: d == 1960),
    ("1970s", "the 1970s", lambda d: d == 1970),
    ("1980s", "the 1980s", lambda d: d == 1980),
    ("1990s", "the 1990s", lambda d: d == 1990),
    ("2000s", "the 2000s", lambda d: d == 2000),
    ("2010s", "the 2010s", lambda d: d == 2010),
    ("2020s", "the 2020s", lambda d: d == 2020),
]
NEIGHBORHOOD_MIN = 3   # a neighborhood page needs this many entries to exist

PLACE_TYPES = ("venue", "place")


# ---------------------------------------------------------------- membership

RAP_LEAD = re.compile(r"\b(rapper|emcee|MC|hip-hop (duo|group|trio|crew))\b")


def is_rapper(e):
    """Roles say rapper/MC/crew, or the entry is hip-hop and its own lead calls it one."""
    if any(RAP_ROLE.search(r) for r in (e.get("roles") or [])):
        return True
    facts = e.get("facts") or []
    return (any("hip-hop" in x.lower() for x in (e.get("genres") or []))
            and bool(facts) and bool(RAP_LEAD.search(facts[0])))


def is_dj(e):
    return any(DJ_ROLE.search(r) for r in (e.get("roles") or []))


def is_place(e):
    return e.get("type") in PLACE_TYPES


ERA_ROWS = ("Era", "Active since", "Years", "Years active", "Active", "Years open", "Released")


def decades_of(e, g):
    """Decades of documented activity only: years_active, else an Era / Active since card
    row. Birth and death dates in the lead never count; being born in 1931 is not being
    active before 1960."""
    d = g._decades(e.get("years_active") or "")
    if not d:
        for c in e.get("card", []):
            if c.get("label") in ERA_ROWS:
                d |= g._decades(c.get("value", ""))
    if not d:
        d = {y // 10 * 10 for y in activity_years(e)}
    return d


_MONTHS = r"(?:January|February|March|April|May|June|July|August|September|October|November|December)"
_LIFE_DATES = re.compile(
    # any parenthetical that holds a month name or "born" and a year: "(born X, DATE -- DATE)",
    # "(December 31, 1898, Jersey City -- December 6, 1940, New York City)", "(2 October 1925, ...)"
    r"\((?=[^)]*(?:born|" + _MONTHS + r"))[^)]*\d{4}[^)]*\)"
    r"|\(\d{4}\s?(?:--|–|—|-)\s?\d{4}\)"
    r"|\b(?:born|died|birth|death)\b[^.;]{0,40}?\b(?:1[89]|20)\d\d\b"
    # the archive's own dating ("oral history given to this archive in 2026") is not activity
    r"|\b(?:this archive|archive research|oral history|founder interview)\b[^.;]*?\b20\d\d\b", re.I)


def activity_years(e):
    """Years of dated events in the entry's sourced facts, with birth and death dates removed.

    A record released in 1969 and a comeback in 2022 put the entry in the 1960s and the
    2020s, not in every decade between.
    """
    text = " ".join(e.get("facts") or [])
    text = _LIFE_DATES.sub(" ", text)
    # a bare year only; "the 1950s" is description, not a dated event
    return {int(y) for y in re.findall(r"(?<![\d-])((?:18[5-9]|19\d|20[0-2])\d)(?![\ds-])", text)}


def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


SLANG = [("201", re.compile(r"\b201\b")), ("Chilltown", re.compile(r"\bChill ?[Tt]own\b"))]


def slang_terms(e):
    """Which of the documented local terms the entry's own facts use."""
    text = " ".join(e.get("facts") or [])
    return [t for t, pat in SLANG if pat.search(text)]


def neighborhood_pages(entries):
    """{neighborhood: [entries]} for neighborhoods with enough entries."""
    groups = {}
    for e in entries:
        for n in e.get("neighborhoods") or []:
            groups.setdefault(n, []).append(e)
    return {n: es for n, es in groups.items() if len(es) >= NEIGHBORHOOD_MIN}


def hub_specs(entries, g):
    """The hubs to build, each with its members. Order here is the sibling-link order."""
    specs = [
        dict(key="rappers", file="rappers-from-jersey-city.html",
             h1="Rappers from Jersey City", kicker="Role",
             title="Rappers from Jersey City: Every Documented MC and Crew",
             members=[e for e in entries if is_rapper(e)]),
        dict(key="born", file="famous-musicians-born-in-jersey-city.html",
             h1="Famous Musicians Born in Jersey City", kicker="Birthplace",
             title="Famous Musicians Born in Jersey City, Sourced",
             members=[e for e in entries if e.get("born_in_jersey_city") and e.get("notability") == "national"]),
        dict(key="famous", file="famous-people-from-jersey-city.html",
             h1="Famous People from Jersey City: Music and Entertainment", kicker="Scope: music and entertainment",
             title="Famous People from Jersey City in Music and Entertainment",
             members=[e for e in entries if e.get("notability") == "national" and not is_place(e)]),
        dict(key="jersey-club", file="jersey-club-and-jersey-city.html",
             h1="Jersey Club and Jersey City", kicker="Genre",
             title="Jersey Club and Jersey City: What the City Added",
             members=[e for e in entries if any("club" in x.lower() for x in (e.get("genres") or []))]),
        dict(key="venues", file="jersey-city-venues-and-record-stores.html",
             h1="Jersey City Music Venues, Record Stores and Studios", kicker="Places",
             title="Jersey City Music Venues, Record Stores and Studios",
             members=[e for e in entries if is_place(e)]),
    ]
    specs.append(dict(key="schools", file="jersey-city-high-schools-music.html",
                      h1="Jersey City High Schools and the Music That Came Through Them", kicker="Schools",
                      title="Jersey City High Schools in the Music Record",
                      members=[e for e in entries if is_place(e) and e.get("place_type") == "school"],
                      connections_list=True))
    specs.append(dict(key="slang", file="jersey-city-slang-in-music.html",
                      h1="Jersey City Slang in Music: 201 and Chilltown", kicker="Language",
                      title="Jersey City Slang in Music: 201 and Chilltown",
                      members=[e for e in entries if slang_terms(e)]))
    for key, label, test in ERAS:
        members = [e for e in entries if any(test(d) for d in decades_of(e, g))]
        specs.append(dict(key=f"era-{key}", file=f"history-{key}.html",
                          h1=f"Jersey City Music {('Before 1960' if key == 'pre-1960s' else 'in ' + label)}",
                          kicker="Era", era=key,
                          title=f"Jersey City Music {('Before 1960' if key == 'pre-1960s' else 'in ' + label)}: Every Documented Artist",
                          members=members))
    for n, members in sorted(neighborhood_pages(entries).items()):
        specs.append(dict(key=f"neighborhood-{slugify(n)}", file=f"neighborhood-{slugify(n)}.html",
                          h1=f"Music from {n}, Jersey City", kicker="Neighborhood", neighborhood=n,
                          title=f"Music from {n}, Jersey City: the Documented Record",
                          members=members))
    return specs


def entry_hub_links(e, g, specs_by_key):
    """(label, href) hubs an entry belongs to, for the record card's 'In the archive' row."""
    links = []
    if is_rapper(e) and "rappers" in specs_by_key:
        links.append(("Rappers from Jersey City", specs_by_key["rappers"]["file"]))
    if is_dj(e):
        links.append(("Jersey City DJs", "jersey-city-djs.html"))
    if is_place(e) and "venues" in specs_by_key:
        links.append(("Venues and record stores", specs_by_key["venues"]["file"]))
    if e.get("born_in_jersey_city") and e.get("notability") == "national" and "born" in specs_by_key:
        links.append(("Born in Jersey City", specs_by_key["born"]["file"]))
    for key, label, test in ERAS:
        if f"era-{key}" in specs_by_key and any(test(d) for d in decades_of(e, g)):
            links.append((("Before 1960" if key == "pre-1960s" else label.replace("the ", "The ")),
                          specs_by_key[f"era-{key}"]["file"]))
    for n in e.get("neighborhoods") or []:
        k = f"neighborhood-{slugify(n)}"
        if k in specs_by_key:
            links.append((n, specs_by_key[k]["file"]))
    return links


# ---------------------------------------------------------------- rendering

def one_line(e, g, limit=150):
    """One sentence for a card: the lead's first sentence, trimmed at a clause if long."""
    facts = e.get("facts") or []
    text = g.first_sentence(re.sub(r"\s+", " ", facts[0]).strip()) if facts else ""
    if len(text) > limit:
        window = text[:limit]
        cut = max(window.rfind(b) for b in ("; ", ", ", " and ", " who ", " which "))
        text = (window[:cut] if cut >= 60 else window.rsplit(" ", 1)[0]).rstrip(",;: ") + "."
    return text


def sort_key(e, g):
    d = decades_of(e, g)
    return (min(d) if d else 9999, e["name"].lower())


def card(e, g):
    decs = sorted(decades_of(e, g))
    chips = "".join(f'<span class="chip">{d}s</span>' for d in decs[:3])
    chips_html = f'\n        <div class="chips">{chips}</div>' if chips else ""
    role = " · ".join(e.get("roles") or [])
    return f"""      <article class="entry-card">
        <span class="entry-card__no">Entry №. {e['entry_no']}</span>
        <h3><a href="entry-{e['slug']}.html">{g.esc(e['name'])}</a></h3>
        <p class="entry-card__role">{g.esc(role)}</p>
        <p class="entry-card__line">{g.esc(one_line(e, g))}</p>{chips_html}
      </article>"""


def para(text, g, name_links, self_slug=""):
    """Escape, resolve [[slug|Label]] and [[page.html|Label]] links, then auto-link first
    mentions of entry names in the remaining text. Explicit links are stashed first so the
    auto-linker never nests an anchor inside them."""
    stash = []

    def keep(html_):
        stash.append(html_)
        return f"\x01{len(stash) - 1}\x01"

    out = g.esc(text)
    out = re.sub(r"\[\[([a-z0-9-]+\.html)\|([^\]]+)\]\]", lambda m: keep(f'<a href="{m.group(1)}">{m.group(2)}</a>'), out)
    out = re.sub(r"\[\[([a-z0-9-]+)\|([^\]]+)\]\]", lambda m: keep(f'<a href="entry-{m.group(1)}.html">{m.group(2)}</a>'), out)
    out = g.linkify(out, name_links, self_slug)
    for i, html_ in enumerate(stash):
        out = out.replace(f"\x01{i}\x01", html_)
    return out


def group_members(spec, members, g):
    """Group cards: eras and neighborhoods by role family; role hubs by era."""
    if spec["key"] == "slang":
        buckets = {}
        for e in members:
            for t in slang_terms(e):
                buckets.setdefault(f"Uses of {t}", []).append(e)
        return sorted(buckets.items())
    if spec["key"] == "venues":
        buckets = {}
        labels = {"venue": "Venues and record stores", "record store": "Venues and record stores",
                  "club": "Venues and record stores", "school": "Schools", "housing": "Public housing",
                  "skating rink": "Skating rinks", "park": "Parks", "street": "Streets", "studio": "Studios"}
        for e in members:
            k = e.get("place_type") or "venue"
            buckets.setdefault(labels.get(k, k.capitalize() + "s"), []).append(e)
        return sorted(buckets.items())
    if spec["key"].startswith(("era-", "neighborhood-")) or spec["key"] in ("born", "famous"):
        buckets = {}
        for e in members:
            fam = ("DJs" if is_dj(e) else "Rappers, MCs and crews" if is_rapper(e)
                   else "Places" if is_place(e) else "Groups" if g.entry_type(e) == "group"
                   else "Labels and companies" if g.entry_type(e) == "label" else "Musicians and singers")
            buckets.setdefault(fam, []).append(e)
        order = ["Musicians and singers", "Groups", "Rappers, MCs and crews", "DJs", "Labels and companies", "Places"]
        return [(k, buckets[k]) for k in order if k in buckets]
    buckets = {}
    for e in members:
        d = decades_of(e, g)
        label = f"{min(d)}s" if d else "Era not yet documented"
        buckets.setdefault(label, []).append(e)
    keys = sorted(buckets, key=lambda k: (k == "Era not yet documented", k))
    return [(k, buckets[k]) for k in keys]


def write_hub(spec, copy, specs, g, name_links):
    members = sorted(spec["members"], key=lambda e: sort_key(e, g))
    canonical = f"{g.SITE}/{spec['file']}"
    intro = copy.get("intro") or []
    lead = intro[0] if intro else ""
    rest = intro[1:]
    faq = copy.get("faq") or []
    sources = copy.get("sources") or []
    research = copy.get("research") or []
    desc = copy.get("description") or g.first_sentence(lead)
    if len(desc) > 155:
        cut = max(desc[:152].rfind(b) for b in ("; ", ", ", ": ", " and ", " with "))
        desc = (desc[:cut] if cut >= 80 else desc[:152].rsplit(" ", 1)[0]).rstrip(",;: ") + "."

    groups = group_members(spec, members, g)
    groups_html = "\n".join(
        f"""    <h3 class="caps caps--wide" style="margin-top:2rem;">{g.esc(label)} <span class="archive-count">({len(es)})</span></h3>
    <div class="related__grid">
{chr(10).join(card(e, g) for e in es)}
    </div>""" for label, es in groups)
    if not members:
        groups_html = "    <p>No entry qualifies yet. The archive adds entries as evidence arrives.</p>"
    if spec.get("connections_list"):
        all_by_slug = {e["slug"]: e for e in g.HANDCRAFTED}
        for e in g.ALL_ENTRIES:
            all_by_slug[e["slug"]] = e
        parts = []
        for e in members:
            conns = e.get("music_connections") or []
            lis = "\n".join(
                f'      <li><a href="entry-{c["slug"]}.html">{g.esc(all_by_slug.get(c["slug"], {}).get("name", c["slug"]))}</a>'
                + (f' <span class="conn-note">{g.esc(c["note"])}</span>' if c.get("note") else "") + "</li>" for c in conns)
            parts.append(f'    <h3><a href="entry-{e["slug"]}.html">{g.esc(e["name"])}</a></h3>\n    <ul class="connections">\n{lis}\n    </ul>')
        groups_html += ('\n    <h2 id="who">Who came through each school<a class="anchor" href="#who" aria-label="Link to this section">§</a></h2>\n'
                        + "\n".join(parts))

    faq_html = "\n".join(f"    <h3>{g.esc(q['q'])}</h3>\n    <p>{para(q['a'], g, name_links)}</p>" for q in faq)
    siblings = [s for s in specs if s["file"] != spec["file"]]
    sib_html = " · ".join(f'<a href="{s["file"]}">{g.esc(s["h1"])}</a>' for s in siblings[:12])
    fixed = ('<a href="archive.html">Musicians from Jersey City: the complete archive</a> · '
             '<a href="jersey-city-djs.html">Jersey City DJs and the mixtape era</a> · '
             '<a href="history.html">Jersey City music history: the timeline</a> · '
             '<a href="chilltown.html">Chilltown</a> · <a href="charts.html">On the Charts</a>')
    src_html = "\n".join(
        f'      <li id="src-{i}">{g.esc(s["label"])}' + (f' — <a href="{g.esc(s["url"])}" rel="nofollow">link</a>' if s.get("url") else "") + "</li>"
        for i, s in enumerate(sources, 1))
    research_html = "".join(f"\n<!-- RESEARCH NEEDED: {r.replace('--', '- -')} -->" for r in research)
    modified = g.lastmod_for(spec["file"], g.hashlib.sha256(
        json.dumps([copy, [e["slug"] for e in members]], sort_keys=True).encode("utf-8")).hexdigest())

    items = ",\n".join(
        f'        {{"@type": "ListItem", "position": {i}, "name": {json.dumps(e["name"])}, "item": "{g.SITE}/entry-{e["slug"]}.html"}}'
        for i, e in enumerate(members, 1))
    faq_ld = ",\n".join(
        f'        {{"@type": "Question", "name": {json.dumps(q["q"])}, "acceptedAnswer": {{"@type": "Answer", "text": {json.dumps(re.sub(r"\[\[[^|\]]+\|([^\]]+)\]\]", r"\1", q["a"]))}}}}}'
        for q in faq)
    ld = f"""{{
  "@context": "https://schema.org",
  "@graph": [
    {{
      "@type": "CollectionPage",
      "@id": "{canonical}#webpage",
      "url": "{canonical}",
      "name": {json.dumps(spec['h1'])},
      "description": {json.dumps(desc)},
      "isPartOf": {{"@id": "{g.SITE}/#website"}},
      "inLanguage": "en-US",
      "datePublished": "{g.iso_dt(modified)}",
      "dateModified": "{g.iso_dt(modified)}",
      "publisher": {{"@id": "{g.SITE}/#org"}},
      "mainEntity": {{"@id": "{canonical}#list"}},
      "breadcrumb": {{"@id": "{canonical}#breadcrumb"}}
    }},
    {{
      "@type": "ItemList",
      "@id": "{canonical}#list",
      "name": {json.dumps(spec['h1'])},
      "numberOfItems": {len(members)},
      "itemListOrder": "https://schema.org/ItemListUnordered",
      "itemListElement": [
{items}
      ]
    }},
    {{
      "@type": "BreadcrumbList",
      "@id": "{canonical}#breadcrumb",
      "itemListElement": [
        {{"@type": "ListItem", "position": 1, "name": "Home", "item": "{g.SITE}/"}},
        {{"@type": "ListItem", "position": 2, "name": "The Archive", "item": "{g.SITE}/archive.html"}},
        {{"@type": "ListItem", "position": 3, "name": {json.dumps(spec['h1'])}}}
      ]
    }}{(',' + chr(10) + '    {' + chr(10) + '      "@type": "FAQPage",' + chr(10) + f'      "@id": "{canonical}#faq",' + chr(10) + '      "mainEntity": [' + chr(10) + faq_ld + chr(10) + '      ]' + chr(10) + '    }') if faq else ''}
  ]
}}"""
    head_extra = f'<script type="application/ld+json">\n{ld}\n</script>\n'

    body = f"""<main class="wrap">{research_html}
  <nav class="breadcrumb" aria-label="Breadcrumb">
    <a href="index.html">Home</a><span class="sep">&#8594;</span><a href="archive.html">The Archive</a><span class="sep">&#8594;</span><span aria-current="page">{g.esc(spec['h1'])}</span>
  </nav>
  <header class="entry-header" style="text-align:center;">
    <span class="entry-no reveal reveal--1">The Archive · {g.esc(spec['kicker'])}</span>
    <h1 class="reveal reveal--2" style="font-size:clamp(2.1rem,4.5vw,3.3rem);">{g.esc(spec['h1'])}</h1>
    <p class="descriptor reveal reveal--3" style="margin-inline:auto;">{len(members)} documented {'entry' if len(members) == 1 else 'entries'}, every one cited. Listed in order of era, then name. Never ranked.</p>
  </header>

  <article class="entry-body reveal reveal--4" style="margin-inline:auto;">
    <p class="lead">{para(lead, g, name_links)}</p>
{chr(10).join('    <p>' + para(p, g, name_links) + '</p>' for p in rest)}

    <h2 id="entries">In the archive<a class="anchor" href="#entries" aria-label="Link to this section">§</a></h2>
{groups_html}

    <h2 id="faq">Questions, answered<a class="anchor" href="#faq" aria-label="Link to this section">§</a></h2>
{faq_html}

    <h2 id="more">Also in the archive<a class="anchor" href="#more" aria-label="Link to this section">§</a></h2>
    <p>{fixed}</p>
    <p>{sib_html}</p>

    <h2 id="sources">Sources<a class="anchor" href="#sources" aria-label="Link to this section">§</a></h2>
    <p>Every fact above is carried by the linked entries, each with its own numbered sources.{' Additional sources for this page:' if sources else ''}</p>
{('    <ol class="sources">' + chr(10) + src_html + chr(10) + '    </ol>') if sources else ''}
    <p class="record-card__since" style="margin-top:2rem;">Archive page by Robert Van Liew · Last updated {modified}</p>
  </article>
</main>"""
    html = g._shell(spec["title"], desc, canonical, body, current="archive", head_extra=head_extra)
    (g.OUT / spec["file"]).write_text(html, encoding="utf-8")
    return modified


def load_copy():
    try:
        return json.loads(COPY_FILE.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {}


def write_hubs(entries, g, name_links):
    """Build every hub. Returns (specs, {file: lastmod}) for the sitemap and entry links."""
    copy_all = load_copy()
    specs = hub_specs(entries, g)
    dates = {}
    for spec in specs:
        copy = copy_all.get(spec["key"]) or {}
        if not copy and spec["key"].startswith("era-"):
            copy = copy_all.get("era-default", {}).copy()
            era_label = spec["h1"].replace("Jersey City Music ", "")
            copy = {k: ([p.replace("{era}", era_label) for p in v] if k == "intro"
                        else [{"q": q["q"].replace("{era}", era_label), "a": q["a"].replace("{era}", era_label)} for q in v] if k == "faq"
                        else v) for k, v in copy.items()}
        if not copy and spec["key"].startswith("neighborhood-"):
            copy = copy_all.get("neighborhood-default", {}).copy()
            n = spec["neighborhood"]
            copy = {k: ([p.replace("{neighborhood}", n) for p in v] if k == "intro"
                        else [{"q": q["q"].replace("{neighborhood}", n), "a": q["a"].replace("{neighborhood}", n)} for q in v] if k == "faq"
                        else v) for k, v in copy.items()}
        dates[spec["file"]] = write_hub(spec, copy, specs, g, name_links)
    return specs, dates


def upgrade_archive_page(page_html, g, name_links):
    """Turn archive.html into the pillar: H1 in the search phrasing, intro, hub links and
    FAQ above the A to Z index, plus FAQPage JSON-LD. The index itself is untouched."""
    copy = load_copy().get("archive") or {}
    intro = copy.get("intro") or []
    faq = copy.get("faq") or []
    if not intro:
        return page_html
    block = "\n".join(
        [f'  <article class="entry-body reveal reveal--4" style="margin-inline:auto;">',
         f'    <p class="lead">{para(intro[0], g, name_links)}</p>']
        + [f'    <p>{para(p, g, name_links)}</p>' for p in intro[1:]]
        + ['    <h2 id="faq">Questions, answered<a class="anchor" href="#faq" aria-label="Link to this section">§</a></h2>']
        + [f'    <h3>{g.esc(q["q"])}</h3>\n    <p>{para(q["a"], g, name_links)}</p>' for q in faq]
        + ['    <h2 id="az-index">A to Z index<a class="anchor" href="#az-index" aria-label="Link to this section">§</a></h2>',
           '    <p>Every entry, searchable and filterable. Catalog numbers mark the order names entered the record.</p>',
           '  </article>\n'])
    faq_ld = ",\n".join(
        f'        {{"@type": "Question", "name": {json.dumps(q["q"])}, "acceptedAnswer": {{"@type": "Answer", "text": {json.dumps(re.sub(r"\[\[[^|\]]+\|([^\]]+)\]\]", r"\1", q["a"]))}}}}}'
        for q in faq)
    out = page_html
    out = out.replace("<title>The Archive — A–Z Index | The Jersey City Sound</title>",
                      "<title>Musicians from Jersey City: The Complete Archive</title>", 1)
    out = out.replace('<meta property="og:title" content="The Archive — A–Z Index | The Jersey City Sound">',
                      '<meta property="og:title" content="Musicians from Jersey City: The Complete Archive">', 1)
    out = re.sub(r'<meta name="description" content="[^"]*">',
                 f'<meta name="description" content="{g.esc(copy.get("description", ""))}">', out, count=1)
    out = out.replace('"name": "The Archive — A–Z Index",', '"name": "Musicians from Jersey City: The Complete Archive",', 1)
    out = out.replace('''    {
      "@type": "BreadcrumbList",
      "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://jerseycitysound.com/"},
        {"@type": "ListItem", "position": 2, "name": "The Archive"}
      ]
    }''', f'''    {{
      "@type": "BreadcrumbList",
      "itemListElement": [
        {{"@type": "ListItem", "position": 1, "name": "Home", "item": "https://jerseycitysound.com/"}},
        {{"@type": "ListItem", "position": 2, "name": "The Archive"}}
      ]
    }},
    {{
      "@type": "FAQPage",
      "@id": "https://jerseycitysound.com/archive.html#faq",
      "mainEntity": [
{faq_ld}
      ]
    }}''', 1)
    out = out.replace('<h1 class="reveal reveal--2" style="font-size:clamp(2.1rem,4.5vw,3.3rem);">A–Z Index</h1>',
                      '<h1 class="reveal reveal--2" style="font-size:clamp(2.1rem,4.5vw,3.3rem);">Musicians from Jersey City: The Complete Archive</h1>', 1)
    out = out.replace('<p class="descriptor reveal reveal--3" style="margin-inline:auto;">Every entry in the record — searchable, filterable, cited.</p>',
                      '<p class="descriptor reveal reveal--3" style="margin-inline:auto;">Every DJ, rapper, singer, group, label and venue in the record, by era, by role and A to Z. Every entry cited.</p>', 1)
    out = out.replace('  <div class="search-wrap reveal reveal--3" role="search">', block + '  <div class="search-wrap reveal reveal--3" role="search">', 1)
    return out


def refresh_dj_roll(entries, g):
    """Regenerate the hand-built DJs hub's roll call (the <ul class="ledger"> block) and its
    DJ count from the data, so the page never falls behind the archive. Nothing else on
    the page is touched."""
    path = g.OUT / "jersey-city-djs.html"
    if not path.exists():
        return
    s = path.read_text(encoding="utf-8")
    djs = sorted((e for e in entries if is_dj(e)), key=lambda e: re.sub(r"^(dj|deejay)\s+", "", e["name"].lower()))
    def li(e):
        years = (e.get("years_active") or "").strip()
        desc = ", ".join((e.get("genres") or [])[:2]) or " · ".join(e.get("roles") or [])
        if years:
            desc = f"{desc} · {years}" if desc else years
        return (f'      <li><a href="entry-{e["slug"]}.html"><span class="name">{g.esc(e["name"])}</span>'
                f'<span class="desc">{g.esc(desc)}</span></a></li>')
    roll = "\n".join(li(e) for e in djs)
    new = re.sub(r'(<ul class="ledger">)\n.*?\n(    </ul>)', lambda m: f"{m.group(1)}\n{roll}\n{m.group(2)}", s, count=1, flags=re.S)
    new = re.sub(r"<strong>\d+ DJs</strong>", f"<strong>{len(djs)} DJs</strong>", new, count=1)
    if new != s:
        path.write_text(new, encoding="utf-8")


def write_map_page(entries, g, name_links):
    """jersey-city-music-map.html: every place entry with coordinates as a pin, a card per
    pin linking to the entry, a list fallback, and an embed snippet. ?embed=1 hides the
    site chrome so the map can be embedded with a link back."""
    places = [e for e in entries if is_place(e) and e.get("lat") is not None and e.get("lng") is not None]
    places.sort(key=lambda e: e["name"].lower())
    pins = [{"name": e["name"], "href": f"entry-{e['slug']}.html", "lat": e["lat"], "lng": e["lng"],
             "kind": (e.get("place_type") or "place").capitalize(), "line": one_line(e, g, 120),
             "note": e.get("geo_note", "")} for e in places]
    unplaced = [e for e in entries if is_place(e) and (e.get("lat") is None or e.get("lng") is None)]
    canonical = f"{g.SITE}/jersey-city-music-map.html"
    lis = "\n".join(
        f'      <li><a href="entry-{e["slug"]}.html">{g.esc(e["name"])}</a> <span class="conn-note">{g.esc((e.get("place_type") or "place").capitalize())}'
        + (f" · {g.esc(e['address'])}" if e.get("address") else "") + "</span></li>" for e in places)
    un_lis = "\n".join(f'      <li><a href="entry-{e["slug"]}.html">{g.esc(e["name"])}</a> <span class="conn-note">address not yet sourced</span></li>' for e in unplaced)
    embed = (f'&lt;iframe src="{canonical}?embed=1" width="100%" height="480" loading="lazy" '
             f'title="Jersey City music map"&gt;&lt;/iframe&gt;\n&lt;p&gt;Map by &lt;a href="{canonical}"&gt;The Jersey City Sound&lt;/a&gt;&lt;/p&gt;')
    modified = g.lastmod_for("jersey-city-music-map.html", g.hashlib.sha256(json.dumps(pins, sort_keys=True).encode("utf-8")).hexdigest())
    has_part = json.dumps([{"@id": f"{g.SITE}/entry-{e['slug']}.html#main"} for e in places])
    ld = (
        '{\n  "@context": "https://schema.org",\n  "@graph": [\n'
        '    {\n      "@type": "CollectionPage",\n'
        f'      "@id": "{canonical}#webpage",\n      "url": "{canonical}",\n'
        '      "name": "Jersey City Music Map",\n'
        '      "description": "Every documented place in Jersey City\'s music history on one map: schools, housing, rinks, streets and stores, each pin linking to a cited entry.",\n'
        f'      "isPartOf": {{"@id": "{g.SITE}/#website"}},\n      "inLanguage": "en-US",\n'
        f'      "dateModified": "{g.iso_dt(modified)}",\n      "publisher": {{"@id": "{g.SITE}/#org"}},\n'
        f'      "hasPart": {has_part}\n    }},\n'
        '    {\n      "@type": "BreadcrumbList",\n      "itemListElement": [\n'
        f'        {{"@type": "ListItem", "position": 1, "name": "Home", "item": "{g.SITE}/"}},\n'
        f'        {{"@type": "ListItem", "position": 2, "name": "Venues and record stores", "item": "{g.SITE}/jersey-city-venues-and-record-stores.html"}},\n'
        '        {"@type": "ListItem", "position": 3, "name": "Jersey City Music Map"}\n'
        '      ]\n    }\n  ]\n}')
    head_extra = (f'<script type="application/ld+json">\n{ld}\n</script>\n'
                  '<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">\n'
                  '<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" defer></script>\n'
                  f'<script>window.JCS_PINS = {json.dumps(pins, ensure_ascii=False)};</script>\n')
    unplaced_html = ""
    if unplaced:
        unplaced_html = ('    <h2 id="unplaced">Documented, not yet placed<a class="anchor" href="#unplaced" aria-label="Link to this section">§</a></h2>\n'
                         '    <ul class="connections">\n' + un_lis + '\n    </ul>\n')
    script = """<script>
(function () {
  if (location.search.indexOf('embed=1') !== -1) document.body.classList.add('embed');
  function start() {
    if (!window.L) return setTimeout(start, 50);
    var pins = window.JCS_PINS || [];
    var map = L.map('music-map', { scrollWheelZoom: false });
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', { maxZoom: 19, attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors' }).addTo(map);
    var group = L.featureGroup();
    pins.forEach(function (p) {
      var m = L.marker([p.lat, p.lng]).bindPopup('<strong><a href="' + p.href + '" target="_top">' + p.name + '</a></strong><br><small>' + p.kind + (p.note ? ' · ' + p.note : '') + '</small><br>' + p.line);
      group.addLayer(m);
    });
    group.addTo(map);
    if (pins.length) map.fitBounds(group.getBounds().pad(0.2)); else map.setView([40.7178, -74.0431], 13);
  }
  start();
})();
</script>"""
    body = f"""<main class="wrap">
  <header class="entry-header" style="text-align:center;">
    <span class="entry-no reveal reveal--1">The Archive · Map</span>
    <h1 class="reveal reveal--2" style="font-size:clamp(2.1rem,4.5vw,3.3rem);">Jersey City Music Map</h1>
    <p class="descriptor reveal reveal--3" style="margin-inline:auto;">Every documented place in the city's music history, each pin linking to a cited entry. {len(places)} places mapped; {len(unplaced)} documented but not yet placed.</p>
  </header>
  <div id="music-map" class="music-map reveal reveal--4" role="region" aria-label="Map of Jersey City music places"></div>
  <section class="map-list">
    <article class="entry-body" style="margin-inline:auto;">
    <h2 id="places">Places on the map<a class="anchor" href="#places" aria-label="Link to this section">§</a></h2>
    <ul class="connections">
{lis}
    </ul>
{unplaced_html}    <h2 id="embed">Embed this map<a class="anchor" href="#embed" aria-label="Link to this section">§</a></h2>
    <p>Local sites, schools and the library are welcome to embed the map. Keep the link back to the archive; the content is CC BY-SA 4.0.</p>
    <pre class="embed-snippet">{embed}</pre>
    <p>Map tiles by <a href="https://www.openstreetmap.org/copyright" rel="noopener">OpenStreetMap</a> contributors. Pins marked approximate sit on the named street rather than an exact address. See the <a href="jersey-city-venues-and-record-stores.html">venues, record stores and studios</a> page for the full list of place entries.</p>
    <p class="record-card__since" style="margin-top:2rem;">Archive page by Robert Van Liew · Last updated {modified}</p>
    </article>
  </section>
</main>
{script}"""
    html = g._shell("Jersey City Music Map: Every Documented Place, Pinned",
                    "Every documented place in Jersey City's music history on one map: schools, housing, rinks, streets and stores, each pin linking to a cited entry.",
                    canonical, body, current="archive", head_extra=head_extra)
    (g.OUT / "jersey-city-music-map.html").write_text(html, encoding="utf-8")
    return modified
