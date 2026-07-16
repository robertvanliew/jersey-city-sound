# Generate archive entry pages (design/entry-<slug>.html) from data/entries.json.
#
# data/entries.json is the source of truth (see JCS-ARCHIVE-ROSTER.md).
# Entry No. 001 (DJ DX) is handcrafted in design/entry-dj-dx.html and is NOT
# generated here. Re-run this script whenever entries.json changes.
#
# Usage:  py execution/generate_entry_pages.py

import json
import html
import re
import urllib.parse
from datetime import date
from pathlib import Path

BUILD_DATE = date.today().isoformat()   # dateModified freshness signal

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "entries.json"
CHART_DATA_FILE = ROOT / "data" / "chart-data.json"
OUT = ROOT / "design"
SITE = "https://jerseycitysound.com"

# The chart-fact ledger (single source of truth for chart badges/medallions).
# Rendered per entry by href; a record only shows if "render" is true, so no
# badge exists without a cited fact in the entry body (handoff §14 rule 1).
try:
    CHART_DATA = json.loads(CHART_DATA_FILE.read_text(encoding="utf-8"))
except FileNotFoundError:
    CHART_DATA = {}

# Sealed records (Record-Seal). {filename-base "entry-slug" -> seal date} scanned
# from the signed credentials, so pages can show a "Sealed in the Record" mark.
SEALS = {}
try:
    SAMEAS = json.loads((ROOT / "data" / "sameas.json").read_text(encoding="utf-8"))
except FileNotFoundError:
    SAMEAS = {}

SEAL_SVG = '<svg class="seal-mark__seal" viewBox="0 0 100 100" role="img" aria-label="Sealed in the record"><g stroke="#C9A227" stroke-width="2.4" fill="none"><circle cx="50" cy="50" r="46.00"/><circle cx="50" cy="50" r="39.75"/><circle cx="50" cy="50" r="33.50"/><circle cx="50" cy="50" r="27.25"/><circle cx="50" cy="50" r="21.00"/></g><circle cx="50" cy="50" r="16" fill="#D7B23E"/><circle cx="50" cy="50" r="2.6" fill="#2a2109"/></svg>'
_cred_dir = OUT / "credentials"
if _cred_dir.exists():
    for _f in _cred_dir.glob("*.vc.json"):
        try:
            _vc = json.loads(_f.read_text(encoding="utf-8"))
            SEALS[_f.name[:-len(".vc.json")]] = (_vc.get("validFrom") or "")[:10]
        except Exception:
            pass

STATUS_LABELS = {
    "web-verified": "Web-verified",
    "doc-verified": "Verified in the 2006 documentary",
    "handle-provided": "Entry opened — awaiting its subject",
    "community-verified": "Community-verified — receipts pending",
}

# Default related entries when none specified: the archive's anchor entries.
ANCHORS = ["001", "004", "013"]
ANCHOR_META = {
    "001": ("DJ DX", "DJ · Producer · Turntablist", "entry-dj-dx.html"),
    "004": ("Wiztv", "DJ · Documentarian", "entry-dj-wizard.html"),
    "013": ("The Jersey City DJ Documentary Vol. 1", "Documentary Film · 2006",
            "entry-jersey-city-dj-documentary-2006.html"),
}


def esc(s):
    return html.escape(s, quote=True) if s else ""


# Aliases that should link to an entry but differ from its canonical name.
EXTRA_ALIASES = {
    "DJ DX": "dj-dx",              # handcrafted entry
    "WizTV": "dj-wizard",
    "Wiztv": "dj-wizard",
    "DJ Wizard": "dj-wizard",
    "Big Time": "dj-bigtime",
    "Stan Krause": "stan-krause",
    "Stanley Krause": "stan-krause",
    "Stan's Square Records": "stans-square-records",
    "Ka-Million": "chameleon-ka-million",
    "Wiley Cat": "dj-walley-katt",
    "Styles 007": "dj-007",
    "Nel E Nel Blends": "dj-nel-e-nel",
    "DJ Nel E Nel": "dj-nel-e-nel",
    "DJ Nel \"E\" Nel": "dj-nel-e-nel",
    "Killa K": "dj-k",
    "Wimpy B": "dj-wimpy-bee",
    "DJ E-Dub DaGeneral": "dj-e-double",
    "E-Dub": "dj-e-double",
    "DJ Thurm": "dj-thurmie-thurm",
    "Stranger Dee": "dj-stranger-dee",
    "Stranger D": "dj-stranger-dee",
    "The Hitman Double J": "double-j",
    "MacArthur Munford": "macarthur-munford",
    "McArthur Munford": "macarthur-munford",
    "Gary Van Liew": "chill-divine",
    "Mary Brown": "mary-brown",
    "Catamount Records": "catamount-records",
    "Square Records": "square-records",
    "DJ Semaj": "dj-semaj",
    "DJ Luchionney": "deejay-luchionney",
    "DJ Walleykatt": "dj-walley-katt",
    "DJ Strong Vic": "strong-vic",
    "DJ E-Double": "dj-e-double",
    "1st Lady EL": "1stlady-el",
    "Kenny Ken": "kenny-kenn",
    "Kamillion": "chameleon-ka-million",
    "All Out": "dj-all-out",
    "DJ Dyce": "dj-dyce",
    # Chill Town documentary — crews, labels, and figures
    "Chill Town J.C. Hip-Hop Documentary": "chill-town-jc-hip-hop-documentary",
    "Sweet Slick and Slide": "sweet-slick-and-slide",
    "Sweet Slick and Sly": "sweet-slick-and-slide",
    "Lord Sun Albee Al": "lord-sun-albee-al",
    "Lord Ali": "lord-sun-albee-al",
    "Lord Sun": "lord-sun-albee-al",
    "Tranquilizing Three": "tranquilizing-three",
    "Tranquilizer 3": "tranquilizing-three",
    "Positively Black": "positively-black",
    "Prince Kyrie": "prince-kyrie",
    "Youth Champagne": "champagne",
    "Miss Champagne": "champagne",
    "Champagne": "champagne",
    "Brutha Basil": "dj-count-basil",
    "Count Basil": "dj-count-basil",
    "Producer Mayor": "producer-mayor",
    "MayoR LLC4": "producer-mayor",
    "Presidential Beats": "presidential-beats",
    "Citoonthebeat": "cito-on-the-beat",
    "Nero CKP": "nero-ckp",
    "Money Train Events": "money-train-entertainment",
    "Money Train Ent.": "money-train-entertainment",
    "Many Men Records": "manymen-records",
    "ManyMen Records": "manymen-records",
    "D-Eastwood": "d-eastwood",
    "D Eastwood": "d-eastwood",
    "J. Fresh": "j-fresh",
    "P.Dot": "p-dot",
    "P Dot": "p-dot",
    "Allout": "dj-all-out",
    "Soul Shades": "soul-shades",
    "DJ Flash Hamilton": "dj-flash-jersey-city",
    "A-Team": "the-a-team",
    "Presidential Crew": "presidential-crew",
    "Presidential Blends": "presidential-crew",
    "Whartonberg": "orlando-wharton",
}


def build_name_links(entries):
    """(display name -> slug) for cross-linking mentions, longest names first."""
    links = {e["name"]: e["slug"] for e in entries}
    links.update(EXTRA_ALIASES)
    return sorted(links.items(), key=lambda kv: -len(kv[0]))


def linkify(escaped_text, name_links, self_slug):
    """Link the first mention of each known name to its entry page.

    Longest names are processed first; inserted links are swapped for
    placeholder tokens so shorter names can never match inside them.
    """
    out = escaped_text
    stash = []
    for name, slug in name_links:
        if slug == self_slug:
            continue
        ename = html.escape(name, quote=True)
        pat = re.escape(ename)

        def repl(m):
            stash.append(f'<a href="entry-{slug}.html">{ename}</a>')
            return f'\x00{len(stash) - 1}\x00'

        out = re.sub(rf'(?<![\w\x00]){pat}(?![\w\x00])', repl, out, count=1)
    for i, link in enumerate(stash):
        out = out.replace(f'\x00{i}\x00', link)
    return out


def cite_sup(text, n_sources):
    """Facts are plain sentences; append nothing. Citations live in Sources."""
    return esc(text)


def _img_dims(src):
    """Intrinsic width/height attrs so the browser reserves space (prevents CLS)."""
    try:
        from PIL import Image
        with Image.open(ROOT / "design" / src) as im:
            return f' width="{im.width}" height="{im.height}"'
    except Exception:
        return ""


def meta_desc(entry):
    facts = entry.get("facts") or []
    base = facts[0] if facts else f"{entry['name']} — Jersey City music archive entry."
    base = re.sub(r"\s+", " ", base).strip()
    if len(base) <= 158:
        return base
    window = base[:158]
    # prefer a clean sentence end, then a clause boundary, then a word boundary
    cut = window.rfind(". ")
    if cut >= 110:
        return window[:cut + 1]
    for sep in ("; ", " — ", ", "):
        c = window.rfind(sep)
        if c >= 110:
            return window[:c] + "…"
    return window.rsplit(" ", 1)[0] + "…"


def cert_badge(kind, mult):
    """Inline SVG RIAA-style gold/platinum record badge (no trademarked art)."""
    if kind == "platinum":
        c1, c2, c3, edge, label_bg, txt = ("#f5f5f7", "#c2c2c8", "#e4e4e8",
                                           "#9a9aa2", "#d2d2d8", "#3a3a40")
        word = "PLATINUM"
    else:
        c1, c2, c3, edge, label_bg, txt = ("#f2dd8a", "#c9a227", "#e6c65f",
                                           "#9c7a14", "#dcb739", "#4a3a08")
        word = "GOLD"
    gid = f"cert-{kind}"
    return f"""<div class="cert">
      <svg viewBox="0 0 100 100" role="img" aria-label="RIAA {word} {mult}">
        <defs><radialGradient id="{gid}" cx="38%" cy="30%" r="80%">
          <stop offset="0%" stop-color="{c1}"/><stop offset="55%" stop-color="{c2}"/>
          <stop offset="100%" stop-color="{c3}"/></radialGradient></defs>
        <circle cx="50" cy="50" r="48" fill="url(#{gid})" stroke="{edge}" stroke-width="1"/>
        <g fill="none" stroke="{edge}" stroke-width="0.5" opacity="0.45">
          <circle cx="50" cy="50" r="44.5"/><circle cx="50" cy="50" r="41.5"/><circle cx="50" cy="50" r="38.5"/>
        </g>
        <circle cx="50" cy="50" r="31" fill="{label_bg}" stroke="{edge}" stroke-width="0.8"/>
        <text x="50" y="43" text-anchor="middle" fill="{txt}" font-family="Archivo, sans-serif"
          font-size="11" font-weight="700" letter-spacing="1.2">RIAA</text>
        <text x="50" y="55" text-anchor="middle" fill="{txt}" font-family="Archivo, sans-serif"
          font-size="8.5" font-weight="600" letter-spacing="0.6">{word}</text>
        <text x="50" y="66" text-anchor="middle" fill="{txt}" font-family="Archivo, sans-serif"
          font-size="8" font-weight="700">{mult}</text>
      </svg>
      <span class="cert__label">{mult} {word.title()}</span>
    </div>"""


def cert_block(entry):
    cert = entry.get("certifications")
    if not cert:
        return ""
    badges = []
    if cert.get("platinum"):
        badges.append(cert_badge("platinum", cert["platinum"]))
    if cert.get("gold"):
        badges.append(cert_badge("gold", cert["gold"]))
    if not badges:
        return ""
    note = cert.get("note", "RIAA-certified credits across her catalog.")
    return ('\n      <div class="certs" aria-label="RIAA certifications">\n        '
            + "\n        ".join(badges)
            + f'\n        <p class="certs__note">{esc(note)}</p>\n      </div>')


def entry_type(entry):
    """'person' | 'film' | 'venue' — explicit `type` field wins."""
    if entry.get("type"):
        return entry["type"]
    if "documentary" in entry["name"].lower():
        return "film"
    return "person"


def build_media_index(entries):
    """Ancestry-style reverse index of tagged media.

    Every gallery image may carry a `tags` list of entry slugs for the people
    (or venues/labels) featured in it. This returns {slug -> [image, ...]} so a
    flyer that lives in one person's gallery also surfaces on the profile of
    everyone else tagged in it. The image's owner is credited in the caption,
    which creates a back-link between the two entries.
    """
    appearances = {}
    for owner in entries:
        oslug = owner["slug"]
        oname = owner["name"]
        for g in owner.get("galleries") or []:
            for im in g.get("images") or []:
                tags = im.get("tags") or []
                if not tags:
                    continue
                base_cap = (im.get("caption") or "").strip()
                for tag in tags:
                    if tag == oslug:
                        continue
                    prov = f" From the {oname} archive." if oname else ""
                    appearances.setdefault(tag, []).append({
                        "src": im["src"],
                        "alt": im.get("alt", base_cap),
                        "caption": (base_cap + prov).strip(),
                    })
    return appearances


def render_slideshow(gid, title, intro_html, images, name_links, slug):
    """One captioned <section> slideshow. Progressive enhancement: the markup is
    a native scroll-snap carousel that swipes without JavaScript; assets/gallery.js
    layers on arrows, dots, and keyboard control. Captions are linkified so anyone
    named links to their own entry."""
    n = len(images)
    slides = []
    for si, im in enumerate(images):
        cap = im.get("caption", "")
        cap_html = (f'\n          <figcaption>{linkify(esc(cap), name_links, slug)}</figcaption>'
                    if cap else "")
        slides.append(
            f'        <figure class="slide" role="group" aria-roledescription="slide" '
            f'aria-label="{si + 1} of {n}">\n'
            f'          <img src="{esc(im["src"])}" alt="{esc(im.get("alt", cap))}"'
            f'{_img_dims(im["src"])} loading="lazy" decoding="async">{cap_html}\n'
            f'        </figure>')
    slides_html = "\n".join(slides)
    intro = f'      <p class="gallery__intro">{intro_html}</p>\n' if intro_html else ""
    t = esc(title)
    return f"""      <section class="gallery" aria-label="{t}">
      <h2 id="{gid}">{t}<a class="anchor" href="#{gid}" aria-label="Link to {t} section">§</a></h2>
{intro}      <div class="slideshow" data-slideshow>
        <div class="slideshow__track" tabindex="0" aria-label="{t} — swipe or use arrow keys">
{slides_html}
        </div>
        <button type="button" class="slideshow__nav slideshow__nav--prev" aria-label="Previous image" hidden>&#8249;</button>
        <button type="button" class="slideshow__nav slideshow__nav--next" aria-label="Next image" hidden>&#8250;</button>
        <div class="slideshow__dots" role="tablist" aria-label="Choose image"></div>
        <div class="slideshow__count" aria-hidden="true"></div>
      </div>
      </section>"""


def galleries_html(entry, name_links, slug, appearances):
    """This entry's own curated galleries, plus an auto 'Appearances' slideshow
    of images owned by other entries that tag this person."""
    blocks = []
    for gi, g in enumerate(entry.get("galleries") or []):
        images = g.get("images") or []
        if not images:
            continue
        gid = g.get("id") or f"gallery-{gi + 1}"
        intro_html = linkify(esc(g["intro"]), name_links, slug) if g.get("intro") else ""
        blocks.append(render_slideshow(gid, g.get("title", "Gallery"), intro_html,
                                       images, name_links, slug))
    apps = appearances.get(slug) or []
    if apps:
        intro_html = esc(f"Flyers and photographs from across the archive that feature {entry['name']}.")
        blocks.append(render_slideshow("appearances", "Appearances", intro_html,
                                       apps, name_links, slug))
    if not blocks:
        return "", False
    return "\n\n".join(blocks), True


def _yt_id(url):
    """Extract a YouTube video id from a watch/youtu.be/embed URL (or a bare id)."""
    if not url:
        return ""
    m = re.search(r"(?:v=|youtu\.be/|/embed/)([A-Za-z0-9_-]{11})", url)
    if m:
        return m.group(1)
    return url if re.fullmatch(r"[A-Za-z0-9_-]{11}", url) else ""


def awards_html(entry):
    """Render entry['awards'] as struck metal certification medallions — the
    same RIAA-style discs used on Mary Brown's profile — so every honored
    entry reads with one consistent 'trophy shelf'.

    The facts come from the chart-data.json ledger (keyed by entry href), the
    single source of truth. A record renders only when its "render" flag is set,
    so no medallion appears without a cited fact in the entry body. Each
    medallion: {metal: gold|platinum|broadcast, lines: [l1, l2, l3], caption}
    plus an optional record "note" beside the row."""
    rec = CHART_DATA.get("entry-%s.html" % entry.get("slug", ""))
    if not rec or not rec.get("render"):
        return ""
    aws = rec.get("medallions") or []
    note = rec.get("note", "")
    if not aws:
        return ""
    METALS = {
        "platinum": dict(g0="#f5f5f7", g1="#c2c2c8", g2="#e4e4e8", edge="#9a9aa2", inner="#d2d2d8", ink="#3a3a40"),
        "gold":     dict(g0="#f2dd8a", g1="#c9a227", g2="#e6c65f", edge="#9c7a14", inner="#dcb739", ink="#4a3a08"),
        # Broadcast/non-chart honors (SNL, Tonight Show): a parchment seal, never
        # dressed as a chart metal (handoff §14 rule 6).
        "broadcast": dict(g0="#efe7d1", g1="#e0d5b6", g2="#efe7d1", edge="#9c7a14", inner="#e9e1cb", ink="#4a3a08"),
    }

    def fit(text, base, ls):
        # Shrink a line so it fits within the inner disc, letter-spacing included.
        n = max(1, len(text))
        cap = (52.0 - (n - 1) * ls) / (n * 0.6)
        return round(min(base, max(4.5, cap)), 1)

    ys = {1: [56], 2: [46, 60], 3: [43, 55, 66]}
    bases = [11.0, 8.5, 8.0]
    lss = [1.2, 0.6, 0.0]
    fws = [700, 600, 700]
    cells = []
    for i, a in enumerate(aws):
        metal = a.get("metal", "gold")
        m = METALS.get(metal, METALS["gold"])
        gid = f"cert-{metal}-{i}"
        lines = [esc(x) for x in (a.get("lines") or [])][:3]
        cap = esc(a.get("caption", ""))
        yy = ys[max(1, min(3, len(lines)))]
        txt = "".join(
            f'<text x="50" y="{yy[j]}" text-anchor="middle" fill="{m["ink"]}" '
            f'font-family="Archivo, sans-serif" font-size="{fit(ln, bases[j], lss[j])}" '
            f'font-weight="{fws[j]}" letter-spacing="{lss[j]}">{ln}</text>'
            for j, ln in enumerate(lines))
        svg = (f'<svg viewBox="0 0 100 100" role="img" aria-label="{" ".join(lines)}">'
               f'<defs><radialGradient id="{gid}" cx="38%" cy="30%" r="80%">'
               f'<stop offset="0%" stop-color="{m["g0"]}"/><stop offset="55%" stop-color="{m["g1"]}"/>'
               f'<stop offset="100%" stop-color="{m["g2"]}"/></radialGradient></defs>'
               f'<circle cx="50" cy="50" r="48" fill="url(#{gid})" stroke="{m["edge"]}" stroke-width="1"/>'
               f'<g fill="none" stroke="{m["edge"]}" stroke-width="0.5" opacity="0.45">'
               f'<circle cx="50" cy="50" r="44.5"/><circle cx="50" cy="50" r="41.5"/><circle cx="50" cy="50" r="38.5"/></g>'
               f'<circle cx="50" cy="50" r="31" fill="{m["inner"]}" stroke="{m["edge"]}" stroke-width="0.8"/>'
               f'{txt}</svg>')
        cells.append(f'<div class="cert">{svg}<span class="cert__label">{cap}</span></div>')
    note_html = f'<p class="certs__note">{esc(note)}</p>' if note else ""
    return '\n      <div class="certs" aria-label="Achievements">' + "".join(cells) + note_html + '</div>'


def videos_html(entry, name_links, slug):
    """Render entry['videos'] as responsive, privacy-mode YouTube embeds."""
    vids = entry.get("videos") or []
    frames = []
    for v in vids:
        vid = _yt_id(v.get("id") or v.get("url", ""))
        if not vid:
            continue
        title = v.get("title") or "Video"
        cap = v.get("caption", "")
        cap_html = (f'\n        <figcaption>{linkify(esc(cap), name_links, slug)}</figcaption>'
                    if cap else "")
        frames.append(
            f'      <figure class="video">\n'
            f'        <div class="video__frame">'
            f'<iframe src="https://www.youtube-nocookie.com/embed/{vid}" '
            f'title="{esc(title)}" loading="lazy" referrerpolicy="strict-origin-when-cross-origin" '
            f'allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; '
            f'picture-in-picture; web-share" allowfullscreen></iframe></div>{cap_html}\n'
            f'      </figure>')
    if not frames:
        return "", False
    body = "\n".join(frames)
    return (f'      <h2 id="watch">Watch<a class="anchor" href="#watch" aria-label="Link to Watch section">§</a></h2>\n'
            f'{body}'), True


def page(entry, by_no, name_links, appearances=None):
    appearances = appearances or {}
    name = entry["name"]
    no = entry["entry_no"]
    slug = entry["slug"]
    roles = entry.get("roles") or []
    genres = entry.get("genres") or []
    years = (entry.get("years_active") or "").replace("–", "–")
    status = STATUS_LABELS.get(entry.get("status", ""), "")
    facts = entry.get("facts") or []
    sources = entry.get("sources") or []
    todos = entry.get("todo_robert") or []
    ig = (entry.get("links") or {}).get("instagram")
    etype = entry_type(entry)
    film = etype == "film"
    venue = etype == "venue"
    group = etype == "group"
    label = etype == "label"

    role_line = " · ".join(roles)
    seo_role = ("Documentary" if film
                else "Venue" if venue
                else "Record Label" if label
                else (roles[0] if roles else "Artist"))
    # jc_from defaults True (native/from Jersey City). Set False for acts who are
    # documented for a Jersey City *connection* but were not born/raised here — so
    # the title/FAQ don't overclaim "Jersey City <role>".
    _jc = entry.get("jc_from", True)
    title = (f"{name} — Jersey City {seo_role} | The Jersey City Sound" if _jc
             else f"{name} — {seo_role} | The Jersey City Sound")
    canonical = f"{SITE}/entry-{slug}.html"
    desc = meta_desc(entry)

    lead = facts[0] if facts else f"{name} is documented in the Jersey City music archive."
    body_facts = facts[1:] if len(facts) > 1 else []

    chips = "".join(
        f'      <a class="chip" href="#">{esc(c)}</a>\n'
        for c in (genres + ([years] if years else []))
        if c
    )

    def fact_p(f):
        text = linkify(esc(f), name_links, slug)
        dot = "" if f.rstrip().endswith((".", ")", "”", "'", '"', "!", "?")) else "."
        return f"      <p>{text}{dot}</p>"

    facts_html = "\n".join(fact_p(f) for f in body_facts) \
        or "      <p>Further documentation is being gathered for this entry.</p>"

    video_body, _has_video = videos_html(entry, name_links, slug)
    video_section = ("\n\n" + video_body) if video_body else ""
    gallery_body, has_gallery = galleries_html(entry, name_links, slug, appearances)
    gallery_section = ("\n\n" + gallery_body) if gallery_body else ""
    awards_block = awards_html(entry)
    _ekey = f"entry-{slug}"
    seal_link = (f'\n<link rel="alternate" type="application/json" href="credentials/{_ekey}.vc.json">'
                 if _ekey in SEALS else "")
    seal_mark = (f'\n      <p class="seal-mark" data-noseal><a href="verify.html?entry={_ekey}">'
                 f'{SEAL_SVG}Sealed in the Record &middot; {SEALS[_ekey]} &middot; verify</a></p>'
                 if _ekey in SEALS else "")
    emblem = entry.get("emblem")
    if emblem:
        _ecap = emblem.get("caption", "")
        _ecaph = (f'\n        <figcaption>{linkify(esc(_ecap), name_links, slug)}</figcaption>'
                  if _ecap else "")
        emblem_block = (f'\n      <figure class="entry-emblem">\n        '
                        f'<img src="{esc(emblem["src"])}" alt="{esc(emblem.get("alt", _ecap))}"'
                        f'{_img_dims(emblem["src"])} loading="lazy" decoding="async">{_ecaph}\n      </figure>')
    else:
        emblem_block = ""
    gallery_script = ('\n<script src="assets/gallery.js" defer></script>'
                      if has_gallery else "")

    # Share block — native share, branded story card, X/Facebook, copy link
    _stitle = f"{name} — The Jersey City Sound"
    _x = ("https://twitter.com/intent/tweet?text=" + urllib.parse.quote(_stitle)
          + "&url=" + urllib.parse.quote(canonical))
    _fb = "https://www.facebook.com/sharer/sharer.php?u=" + urllib.parse.quote(canonical)
    share_block = f"""
      <h2 id="share">Share this entry<a class="anchor" href="#share" aria-label="Link to Share section">§</a></h2>
      <div class="share" data-noseal data-url="{canonical}" data-title="{esc(_stitle)}" data-name="{esc(name)}" data-card="assets/cards/{slug}.png">
        <button type="button" class="share__btn share__btn--gold" data-act="story">Share to Story</button>
        <button type="button" class="share__btn" data-act="native">Share&hellip;</button>
        <a class="share__btn" data-act="x" target="_blank" rel="noopener" href="{_x}">X</a>
        <a class="share__btn" data-act="fb" target="_blank" rel="noopener" href="{_fb}">Facebook</a>
        <button type="button" class="share__btn" data-act="copy">Copy link</button>
      </div>
"""

    def src_li(i, s):
        label = esc(s["label"])
        url = s.get("url")
        if url:
            return f'        <li id="src-{i}">{label} — <a href="{esc(url)}">link</a></li>'
        return f'        <li id="src-{i}">{label}</li>'

    sources_html = "\n".join(src_li(i, s) for i, s in enumerate(sources, 1))

    wanted_html = ""
    if todos:
        items = "".join(f"<li>{esc(t)}</li>" for t in todos)
        wanted_html = f"""
      <h2 id="wanted">Wanted for this Entry<a class="anchor" href="#wanted" aria-label="Link to Wanted section">§</a></h2>
      <p>The archive is looking for the following. If you can supply any of it, use the claim bar below.</p>
      <ul class="sources" style="list-style: disc;">{items}</ul>"""

    # record card rows — each value is pre-rendered, safe HTML
    rows = []
    ig = (entry.get("links") or {}).get("instagram")
    origin = entry.get("origin", "Jersey City, New Jersey")
    if origin:
        rows.append(("Origin", esc(origin)))
    if role_line:
        rows.append(("Format" if film else "What it was" if venue else "Type" if label else "Roles", esc(role_line)))
    if genres:
        rows.append(("Subject" if film else "Known for" if venue else "Catalog" if label else "Style", esc(", ".join(genres))))
    if years:
        rows.append(("Released" if film else "Years open" if venue else "Active" if label else "Years active", esc(years)))
    cert = entry.get("certifications")
    if cert:
        bits = []
        if cert.get("platinum"):
            bits.append(f'{esc(cert["platinum"])} Platinum')
        if cert.get("gold"):
            bits.append(f'{esc(cert["gold"])} Gold')
        if bits:
            rows.append(("Certified", " · ".join(bits)))
    # entry-authored extra rows (values may reference other entries -> auto-linked)
    for extra in entry.get("card", []):
        rows.append((extra["label"], linkify(esc(extra["value"]), name_links, slug)))
    # Links row — every platform on file, not just Instagram
    PLATFORM_LABELS = [("instagram.com", "Instagram"), ("open.spotify.com", "Spotify"),
                       ("spotify.com", "Spotify"), ("bandcamp.com", "Bandcamp"),
                       ("soundcloud.com", "SoundCloud"), ("music.apple.com", "Apple Music"),
                       ("audiomack.com", "Audiomack"), ("youtube.com", "YouTube"),
                       ("discogs.com", "Discogs"), ("facebook.com", "Facebook"),
                       ("djdxmusic.com", "Official site"), ("ted.com", "TED"),
                       ("soulshadesmusic.com", "Official site"),
                       ("tiktok.com", "TikTok"), ("patreon.com", "Patreon"),
                       ("wikipedia.org", "Wikipedia"), ("imdb.com", "IMDb")]
    link_bits, seen_labels = [], set()

    def add_link(url, label):
        if label in seen_labels:
            return
        seen_labels.add(label)
        link_bits.append(f'<a href="{esc(url)}">{esc(label)}</a>')

    if ig:
        handle = "@" + ig.rstrip("/").rsplit("/", 1)[-1]
        seen_labels.add("Instagram")
        link_bits.append(f'<a href="{esc(ig)}">{esc(handle)}</a>')
    for s in entry.get("sources", []):
        u = s.get("url")
        if not u:
            continue
        for host, lbl in PLATFORM_LABELS:
            if host in u:
                add_link(u, lbl)
                break
    if link_bits:
        rows.append(("Links", " · ".join(link_bits)))
    rows_html = "\n".join(
        f'        <div class="row"><dt>{esc(k)}</dt><dd>{v}</dd></div>'
        for k, v in rows
    )

    # related: anchors minus self
    rel = [ANCHOR_META[a] for a in ANCHORS if a != no][:3]
    related_html = "\n".join(f"""      <article class="entry-card">
        <span class="entry-card__no">Entry №. {a_no}</span>
        <h3><a href="{a_href}">{esc(a_name)}</a></h3>
        <p class="entry-card__role">{esc(a_role)}</p>
      </article>""" for a_no, (a_name, a_role, a_href) in
        [(a, ANCHOR_META[a]) for a in ANCHORS if a != no][:3])

    schema_type = ("Movie" if film else "MusicStore" if venue
                   else "MusicGroup" if group else "Organization" if label else "Person")
    genre_json = json.dumps(genres) if genres else "[]"
    crumb_cat = ("Films" if film else "Venues" if venue else "Groups" if group
                 else "Labels" if label else "DJs" if any(r == "DJ" for r in roles) else "Artists")
    # DJ entries link up to their hub page (charter: entries <-> hub internal-linking loop)
    crumb_href = "jersey-city-djs.html" if crumb_cat == "DJs" else "archive.html"

    memorial = bool(entry.get("memorial"))
    body_class = ' class="memorial"' if memorial else ""
    memorial_mark = ('\n    <p class="memorial-mark caps reveal reveal--1">In Memoriam</p>'
                     if memorial else "")

    # sameAs: identity/profile links that tie this entry to the wider web
    IDENTITY_HOSTS = ("wikipedia.org", "wikidata.org", "instagram.com", "spotify.com",
                      "discogs.com", "music.apple.com", "allmusic.com", "bandcamp.com",
                      "facebook.com", "soundcloud.com", "youtube.com/@", "imdb.com")
    same = []
    ig = (entry.get("links") or {}).get("instagram")
    if ig:
        same.append(ig)
    for s in entry.get("sources", []):
        u = s.get("url")
        if u and any(h in u for h in IDENTITY_HOSTS) and u not in same:
            same.append(u)
    _sa = SAMEAS.get(f"entry-{slug}")
    if _sa and _sa.get("confidence") == "confirmed":
        for _k in ("wikipedia", "wikidata", "musicbrainz"):
            _u = _sa.get(_k)
            if _u and _u not in same:
                same.append(_u)
    same_json = f',\n      "sameAs": {json.dumps(same)}' if same else ""
    job_json = (f',\n      "jobTitle": {json.dumps(", ".join(roles))}'
                if roles and schema_type == "Person" else "")

    # --- entity enrichment: description, knowsAbout, alternateName, location, date ---
    desc_json = f',\n      "description": {json.dumps(lead)}'
    knows = [x for x in (roles + genres) if x]
    knows_json = f',\n      "knowsAbout": {json.dumps(knows)}' if knows else ""
    aka = next((c["value"] for c in entry.get("card", []) if c.get("label") == "Also known as"), "")
    alt_json = f',\n      "alternateName": {json.dumps(aka)}' if aka else ""
    origin_val = entry.get("origin", "Jersey City, New Jersey")
    loc_prop = ("homeLocation" if schema_type == "Person"
                else "foundingLocation" if schema_type in ("MusicGroup", "Organization")
                else "location" if venue else "")
    if "jersey city" in origin_val.lower():
        place = ('{"@type": "City", "name": "Jersey City", '
                 '"containedInPlace": {"@type": "State", "name": "New Jersey"}}')
    elif origin_val.strip().lower() == "new jersey":
        place = '{"@type": "State", "name": "New Jersey"}'
    else:
        place = f'{{"@type": "Place", "name": {json.dumps(origin_val)}}}'
    loc_json = (f',\n      "{loc_prop}": {place}' if loc_prop and origin_val else "")
    date_json = ',\n      "datePublished": "2026-07-05"'

    # --- FAQ structured data (AEO/GEO) — answers grounded in on-page facts ---
    who = "Who was" if memorial else "Who is"
    known_ans = (f"{name} is a Jersey City {role_line}" if role_line and _jc
                 else f"{name} is a {role_line} with a documented Jersey City connection" if role_line
                 else f"{name} is documented in The Jersey City Sound")
    if genres:
        known_ans += " working in " + ", ".join(genres)
    if years:
        known_ans += f", active {years}"
    known_ans += ", documented in The Jersey City Sound — the cited archive of the city's music culture."
    jc_ans = (f"Yes. {name} is documented in The Jersey City Sound, the cited encyclopedia-archive of "
              f"Jersey City music culture"
              + (f"; origin: {origin_val}." if origin_val else "."))
    faqs = [(f"{who} {name}?", lead),
            (f"What is {name} known for?", known_ans),
            (f"Is {name} part of the Jersey City music scene?", jc_ans)]
    faq_items = ",\n        ".join(
        f'{{"@type": "Question", "name": {json.dumps(q)}, '
        f'"acceptedAnswer": {{"@type": "Answer", "text": {json.dumps(a)}}}}}'
        for q, a in faqs)

    # --- multi-modal: primary image (galleries) + video (embeds) ---
    first_img = next((g["images"][0]["src"] for g in (entry.get("galleries") or [])
                      if g.get("images")), None)
    img_node = img_ref = primary_img = ""
    if first_img:
        img_url = f"{SITE}/{first_img}"
        img_node = (f',\n    {{"@type": "ImageObject", "@id": "{canonical}#primaryimage", '
                    f'"url": "{img_url}", "contentUrl": "{img_url}"}}')
        img_ref = f',\n      "image": {{"@id": "{canonical}#primaryimage"}}'
        primary_img = f',\n      "primaryImageOfPage": {{"@id": "{canonical}#primaryimage"}}'
    vid_node = ""
    vids = entry.get("videos") or []
    if vids:
        vid_id = _yt_id(vids[0].get("id") or vids[0].get("url", ""))
        if vid_id:
            vt = vids[0].get("title") or name
            vc = vids[0].get("caption") or f"{name} on video."
            vid_node = (f',\n    {{"@type": "VideoObject", "@id": "{canonical}#video", '
                        f'"name": {json.dumps(vt)}, "description": {json.dumps(vc)}, '
                        f'"thumbnailUrl": "https://i.ytimg.com/vi/{vid_id}/hqdefault.jpg", '
                        f'"embedUrl": "https://www.youtube-nocookie.com/embed/{vid_id}"}}')

    ld = f"""{{
  "@context": "https://schema.org",
  "@graph": [
    {{
      "@type": "{schema_type}",
      "@id": "{canonical}#main",
      "name": {json.dumps(name)},
      "genre": {genre_json},
      "url": "{canonical}",
      "mainEntityOfPage": {{"@id": "{canonical}#webpage"}}{job_json}{same_json}{desc_json}{knows_json}{alt_json}{loc_json}{img_ref}{date_json}
    }},
    {{
      "@type": "ProfilePage",
      "@id": "{canonical}#webpage",
      "url": "{canonical}",
      "name": {json.dumps(title)},
      "isPartOf": {{"@id": "{SITE}/#website"}},
      "about": {{"@id": "{canonical}#main"}},
      "mainEntity": {{"@id": "{canonical}#main"}},
      "breadcrumb": {{"@id": "{canonical}#breadcrumb"}},
      "inLanguage": "en-US",
      "datePublished": "2026-07-05",
      "dateModified": "{BUILD_DATE}",
      "publisher": {{"@type": "Organization", "name": "The Jersey City Sound", "url": "{SITE}/"}}{primary_img}
    }},
    {{
      "@type": "BreadcrumbList",
      "@id": "{canonical}#breadcrumb",
      "itemListElement": [
        {{"@type": "ListItem", "position": 1, "name": "Archive", "item": "{SITE}/archive.html"}},
        {{"@type": "ListItem", "position": 2, "name": "{crumb_cat}"}},
        {{"@type": "ListItem", "position": 3, "name": {json.dumps(name)}}}
      ]
    }},
    {{
      "@type": "FAQPage",
      "@id": "{canonical}#faq",
      "mainEntity": [
        {faq_items}
      ]
    }}{img_node}{vid_node}
  ]
}}"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{canonical}">{seal_link}
<meta name="robots" content="index, follow">
<link rel="icon" href="assets/favicon-32.png" sizes="32x32">
<link rel="icon" href="assets/favicon-64.png" sizes="64x64">
<link rel="apple-touch-icon" href="assets/favicon-180.png">
<meta property="og:type" content="{'video.movie' if film else 'website' if venue or label else 'profile'}">
<meta property="og:site_name" content="The Jersey City Sound">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{SITE}/assets/og/{slug}.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{esc(name)} — The Jersey City Sound">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{SITE}/assets/og/{slug}.png">
<link rel="preload" as="font" type="font/woff2" href="assets/fonts/sourceserif-latin-37bedc60.woff2" crossorigin>
<link rel="stylesheet" href="assets/fonts/fonts.css">
<link rel="stylesheet" href="styles.css">
</head>
<body{body_class}>

<header class="masthead wrap">
  <div class="masthead__logo masthead__logo--compact">
    <a href="index.html" aria-label="The Jersey City Sound — home">
      <img src="{'assets/jerseycitysound-cream.png' if memorial else 'assets/jerseycitysound-ink.png'}" alt="Jersey City Sound" width="200" height="81">
    </a>
  </div>
  <nav class="nav" aria-label="Primary">
    <a href="index.html">Home</a>
    <a href="archive.html" aria-current="page">The Archive</a>
    <a href="charts.html">On the Charts</a>
    <a href="legends.html">Legends</a>
    <a href="history.html">History</a>
    <a href="report.html">The Sound Report</a>
    <a href="about.html">About</a>
    <div class="nav-search-wrap">
    <form class="nav-search" role="search" action="archive.html">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.8-3.8"/></svg>
      <input type="search" id="nav-search" name="q" placeholder="Search the archive…" autocomplete="off" aria-label="Search the archive" role="combobox" aria-controls="nav-suggest" aria-expanded="false">
      <ul class="search-suggest" id="nav-suggest" role="listbox" aria-label="Search suggestions"></ul>
    </form>
    </div>
  </nav>
</header>

<main class="wrap">
  <nav class="breadcrumb" aria-label="Breadcrumb">
    <a href="archive.html">Archive</a><span class="sep">→</span><a href="{crumb_href}">{crumb_cat}</a><span class="sep">→</span><span aria-current="page">{esc(name)}</span>
  </nav>

  <header class="entry-header">{memorial_mark}
    <span class="entry-no reveal reveal--1">Entry №. {no}</span>
    <h1 class="reveal reveal--2">{esc(name)}</h1>
    <p class="descriptor reveal reveal--3">{esc(role_line)}{(" · " + esc(years)) if years else ""}</p>
    <div class="chips reveal reveal--3">
{chips}    </div>
  </header>

  <div class="entry-layout">
    <article class="entry-body reveal reveal--4">
      <p class="lead">{linkify(esc(lead), name_links, slug)}{"" if lead.rstrip().endswith((".", ")", "”", '"', "!", "?")) else "."}</p>{cert_block(entry)}{awards_block}{seal_mark}{emblem_block}

      <h2 id="record">In the Record<a class="anchor" href="#record" aria-label="Link to In the Record section">§</a></h2>
{facts_html}{video_section}{gallery_section}

      <h2 id="sources">Sources<a class="anchor" href="#sources" aria-label="Link to Sources section">§</a></h2>
      <ol class="sources">
{sources_html}
      </ol>
{wanted_html}

{share_block}
      <aside class="claim-bar" data-noseal>
        <p>See something to correct, or a receipt, photo, or memory to add?</p>
        <a href="suggest-edit.html">Suggest an edit →</a>
      </aside>
    </article>

    <aside class="record-card reveal reveal--3" aria-label="Record card: {esc(name)}">
      <div class="record-card__label">The Record Card</div>
      <div class="record-card__portrait">
        <div class="placeholder" aria-hidden="true">
          <svg viewBox="0 0 200 200" fill="none">
            <g class="spin-slow">
              <circle cx="100" cy="100" r="96" stroke="#C9A227" stroke-width="1.5"/>
              <circle cx="100" cy="100" r="78" stroke="#9C7A14" stroke-width="1"/>
              <circle cx="100" cy="100" r="62" stroke="#C9A227" stroke-width="1"/>
              <circle cx="100" cy="100" r="46" stroke="#9C7A14" stroke-width="1"/>
              <circle cx="100" cy="100" r="30" fill="#C9A227"/>
              <circle cx="100" cy="100" r="7" fill="#0E0E10"/>
            </g>
          </svg>
        </div>
      </div>
      <p class="record-card__caption">{"Stills pending — duotone treatment on receipt." if film else "Storefront photograph pending — duotone treatment on receipt." if venue else "Label scan pending — duotone treatment on receipt." if label else "Portrait pending — duotone treatment on receipt."}</p>
      <dl>
{rows_html}
        <div class="row"><dt>Status</dt><dd>{esc(status)}</dd></div>
      </dl>
      <div class="record-card__since">In the archive since July 2026 · Last updated {BUILD_DATE}</div>
    </aside>
  </div>

  <section class="related">
    <div class="section__head">
      <h2 class="caps caps--wide">Related Entries</h2>
    </div>
    <div class="related__grid">
{related_html}
    </div>
  </section>
</main>

<footer class="footer wrap">
  <div class="footer__grid">
    <div class="footer__brand">
      <img src="{'assets/jerseycitysound-cream.png' if memorial else 'assets/jerseycitysound-ink.png'}" alt="Jersey City Sound" width="150" height="61">
      <p>Every voice in the city, on the record.</p>
      <p class="footer__social"><a href="https://x.com/jerseycitysound" aria-label="X (Twitter)" title="X"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg></a><a href="https://www.instagram.com/jerseycitysound" aria-label="Instagram" title="Instagram"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2.982c2.937 0 3.285.011 4.445.064 1.072.049 1.655.228 2.042.379.514.2.88.437 1.265.822.385.385.622.751.822 1.265.151.387.33.97.379 2.042.053 1.16.064 1.508.064 4.445 0 2.937-.011 3.285-.064 4.445-.049 1.072-.228 1.655-.379 2.042-.2.514-.437.88-.822 1.265-.385.385-.751.622-1.265.822-.387.151-.97.33-2.042.379-1.16.053-1.508.064-4.445.064-2.937 0-3.285-.011-4.445-.064-1.072-.049-1.655-.228-2.042-.379-.514-.2-.88-.437-1.265-.822-.385-.385-.622-.751-.822-1.265-.151-.387-.33-.97-.379-2.042-.053-1.16-.064-1.508-.064-4.445 0-2.937.011-3.285.064-4.445.049-1.072.228-1.655.379-2.042.2-.514.437-.88.822-1.265.385-.385.751-.622 1.265-.822.387-.151.97-.33 2.042-.379 1.16-.053 1.508-.064 4.445-.064M12 1c-2.987 0-3.362.013-4.535.066-1.171.053-1.97.24-2.67.511-.724.281-1.338.658-1.95 1.27-.612.612-.989 1.226-1.27 1.95-.271.7-.458 1.499-.511 2.67C1.013 8.638 1 9.013 1 12s.013 3.362.066 4.535c.053 1.171.24 1.97.511 2.67.281.724.658 1.338 1.27 1.95.612.612 1.226.989 1.95 1.27.7.271 1.499.458 2.67.511C8.638 22.987 9.013 23 12 23s3.362-.013 4.535-.066c1.171-.053 1.97-.24 2.67-.511.724-.281 1.338-.658 1.95-1.27.612-.612.989-1.226 1.27-1.95.271-.7.458-1.499.511-2.67.053-1.173.066-1.548.066-4.535s-.013-3.362-.066-4.535c-.053-1.171-.24-1.97-.511-2.67-.281-.724-.658-1.338-1.27-1.95-.612-.612-1.226-.989-1.95-1.27-.7-.271-1.499-.458-2.67-.511C15.362 1.013 14.987 1 12 1zm0 5.351A5.649 5.649 0 1 0 12 17.649 5.649 5.649 0 0 0 12 6.351zm0 9.316A3.667 3.667 0 1 1 12 8.333a3.667 3.667 0 0 1 0 7.334zm7.192-9.539a1.32 1.32 0 1 1-2.64 0 1.32 1.32 0 0 1 2.64 0z"/></svg></a><a href="https://www.tiktok.com/@jerseycitysound" aria-label="TikTok" title="TikTok"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M16.6 5.82a4.28 4.28 0 0 1-1.06-2.82h-3.09v12.4a2.59 2.59 0 0 1-2.59 2.5 2.6 2.6 0 0 1-2.6-2.6c0-1.72 1.66-3.01 3.37-2.48V9.66c-3.45-.46-6.47 2.22-6.47 5.64a5.7 5.7 0 0 0 5.69 5.7 5.7 5.7 0 0 0 5.69-5.7V9.01a7.35 7.35 0 0 0 4.3 1.38V7.3s-1.88.09-3.24-1.48z"/></svg></a><a href="https://www.youtube.com/@jerseycitysound" aria-label="YouTube" title="YouTube"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg></a></p>
    </div>
    <nav aria-label="Footer">
      <a href="archive.html">Archive</a>
      <a href="legends.html">Legends</a>
      <a href="history.html">History</a>
      <a href="chilltown.html">Chilltown</a>
      <a href="report.html">Sound Report</a>
      <a href="sources.html">Sources</a>
      <a href="about.html">About</a>
      <a href="suggest-edit.html">Suggest an edit</a>
    </nav>
  </div>
  <div class="footer__legal">
    <span>© 2026 The Jersey City Sound · Content licensed CC BY-SA 4.0</span>
    <nav class="footer__policies" aria-label="Policies">
      <a href="privacy.html">Privacy</a>
      <a href="terms.html">Terms</a>
      <a href="corrections.html">Corrections &amp; Removal</a>
    </nav>
    <span>Conceived 7 · 5 · 2026 — designed by <a href="https://robertvanliew.com">Robert Van Liew</a></span>
  </div>
</footer>

<script type="application/ld+json">
{ld}
</script>{gallery_script}
<script src="assets/share.js" defer></script>

<script src="archive-data.js"></script>
<script src="assets/nav-search.js" defer></script>
<script src="assets/protect.js" defer></script>
</body>
</html>
"""


# Entry No. 001 is handcrafted — include it in the archive index and search.
HANDCRAFTED = [{
    "entry_no": "001", "name": "DJ DX", "slug": "dj-dx",
    "roles": ["DJ", "Producer", "Turntablist"], "years_active": "c. 1998 - present",
    "type": "person", "status": "doc-verified",
}]


def write_archive_data(entries):
    """design/archive-data.js — the client-side search/browse index."""
    items = []
    for e in sorted(entries, key=lambda x: x["name"].lower()):
        items.append({
            "no": e["entry_no"],
            "name": e["name"],
            "href": f"entry-{e['slug']}.html",
            "role": " · ".join(e.get("roles") or []),
            "type": entry_type(e),
            "years": e.get("years_active") or "",
        })
    js = "window.JCS_ENTRIES = " + json.dumps(items, ensure_ascii=False, indent=1) + ";\n"
    (OUT / "archive-data.js").write_text(js, encoding="utf-8")


def build_az_static(entries):
    """Static, crawlable A–Z index HTML (AI bots don't run JS) + the count text.
    Mirrors the client-side render() so JS enhancement overwrites identical markup."""
    items = sorted(
        ({"no": e["entry_no"], "name": e["name"], "href": f"entry-{e['slug']}.html",
          "role": " · ".join(e.get("roles") or []), "years": e.get("years_active") or ""}
         for e in entries), key=lambda x: x["name"].lower())

    def letter_of(name):
        n = re.sub(r"^(The|DJ|A)\s+", "", name, flags=re.I)
        c = n[:1].upper()
        return c if (c.isalpha() and c.isascii()) else "#"

    groups = {}
    for it in items:
        groups.setdefault(letter_of(it["name"]), []).append(it)
    sections = []
    for L in sorted(groups):
        lis = "".join(
            f'<li><a href="{esc(it["href"])}"><span class="no">№. {esc(it["no"])}</span>'
            f'<span class="name">{esc(it["name"])}</span>'
            f'<span class="desc">{esc(it["role"])}'
            f'{(" · " + esc(it["years"])) if it["years"] else ""}</span></a></li>'
            for it in groups[L])
        sections.append(f'<section class="az-group"><h2>{esc(L)}</h2><ul class="ledger">{lis}</ul></section>')
    return "\n".join(sections), f"{len(items)} of {len(items)} entries"


ARCHIVE_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>The Archive — A–Z Index | The Jersey City Sound</title>
<meta name="description" content="The A-Z index of the Jersey City (&quot;Chilltown&quot;) music archive: DJs, mixtape legends, rappers, producers, groups, venues, films, and record labels - every entry cited.">
<meta name="keywords" content="Jersey City music, Chilltown, Jersey City DJs, Jersey City hip-hop, mixtape DJs, Jersey City rappers, producers, groups, venues, record labels, A-Z index">
<link rel="canonical" href="https://jerseycitysound.com/archive.html">
<link rel="icon" href="assets/favicon-32.png" sizes="32x32">
<link rel="icon" href="assets/favicon-64.png" sizes="64x64">
<link rel="apple-touch-icon" href="assets/favicon-180.png">
<meta property="og:type" content="website">
<meta property="og:site_name" content="The Jersey City Sound">
<meta property="og:title" content="The Archive — A–Z Index | The Jersey City Sound">
<meta property="og:description" content="The A-Z index of the Jersey City music archive: DJs, producers, venues, films, and crews - every entry cited.">
<meta property="og:url" content="https://jerseycitysound.com/archive.html">
<meta property="og:image" content="https://jerseycitysound.com/assets/og-card.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="robots" content="index, follow">
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "CollectionPage",
      "@id": "https://jerseycitysound.com/archive.html#webpage",
      "url": "https://jerseycitysound.com/archive.html",
      "name": "The Archive — A–Z Index",
      "isPartOf": {"@id": "https://jerseycitysound.com/#website"},
      "about": {"@id": "https://jerseycitysound.com/#org"},
      "description": "The A–Z index of the Jersey City (Chilltown) music archive: DJs, mixtape legends, rappers, producers, groups, venues, films, and record labels — every entry cited.",
      "inLanguage": "en-US",
      "publisher": {"@type": "Organization", "name": "The Jersey City Sound", "url": "https://jerseycitysound.com/"}
    },
    {
      "@type": "BreadcrumbList",
      "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://jerseycitysound.com/"},
        {"@type": "ListItem", "position": 2, "name": "The Archive"}
      ]
    }
  ]
}
</script>
<link rel="preload" as="font" type="font/woff2" href="assets/fonts/sourceserif-latin-37bedc60.woff2" crossorigin>
<link rel="stylesheet" href="assets/fonts/fonts.css">
<link rel="stylesheet" href="styles.css">
</head>
<body>

<header class="masthead wrap">
  <div class="masthead__logo masthead__logo--compact">
    <a href="index.html" aria-label="The Jersey City Sound — home">
      <img src="assets/jerseycitysound-ink.png" alt="Jersey City Sound" width="200" height="81">
    </a>
  </div>
  <nav class="nav" aria-label="Primary">
    <a href="index.html">Home</a>
    <a href="archive.html" aria-current="page">The Archive</a>
    <a href="charts.html">On the Charts</a>
    <a href="legends.html">Legends</a>
    <a href="history.html">History</a>
    <a href="report.html">The Sound Report</a>
    <a href="about.html">About</a>
    <div class="nav-search-wrap">
    <form class="nav-search" role="search" action="archive.html">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.8-3.8"/></svg>
      <input type="search" id="nav-search" name="q" placeholder="Search the archive…" autocomplete="off" aria-label="Search the archive" role="combobox" aria-controls="nav-suggest" aria-expanded="false">
      <ul class="search-suggest" id="nav-suggest" role="listbox" aria-label="Search suggestions"></ul>
    </form>
    </div>
  </nav>
</header>

<main class="wrap">
  <header class="entry-header" style="text-align:center;">
    <span class="entry-no reveal reveal--1">The Archive</span>
    <h1 class="reveal reveal--2" style="font-size:clamp(2.1rem,4.5vw,3.3rem);">A–Z Index</h1>
    <p class="descriptor reveal reveal--3" style="margin-inline:auto;">Every entry in the record — searchable, filterable, cited.</p>
  </header>

  <div class="search-wrap reveal reveal--3" role="search">
    <div class="search">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true">
        <circle cx="11" cy="11" r="7"/><path d="m20 20-3.8-3.8"/>
      </svg>
      <input type="search" id="archive-search" placeholder="Filter the archive…" aria-label="Filter the archive">
    </div>
  </div>

  <div class="filters reveal reveal--4" id="filters" role="group" aria-label="Filter by type">
    <button class="chip" data-f="all" aria-pressed="true">All</button>
    <button class="chip" data-f="person" aria-pressed="false">People</button>
    <button class="chip" data-f="group" aria-pressed="false">Groups</button>
    <button class="chip" data-f="venue" aria-pressed="false">Venues</button>
    <button class="chip" data-f="film" aria-pressed="false">Films</button>
  </div>
  <p class="caps archive-count" id="count"></p>

  <div id="az"></div>
  <p class="az-empty" id="empty" hidden>Nothing in the record yet under that filter — the archive grows weekly.</p>
</main>

<footer class="footer wrap">
  <div class="footer__grid">
    <div class="footer__brand">
      <img src="assets/jerseycitysound-ink.png" alt="Jersey City Sound" width="150" height="61">
      <p>Every voice in the city, on the record.</p>
      <p class="footer__social"><a href="https://x.com/jerseycitysound" aria-label="X (Twitter)" title="X"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg></a><a href="https://www.instagram.com/jerseycitysound" aria-label="Instagram" title="Instagram"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2.982c2.937 0 3.285.011 4.445.064 1.072.049 1.655.228 2.042.379.514.2.88.437 1.265.822.385.385.622.751.822 1.265.151.387.33.97.379 2.042.053 1.16.064 1.508.064 4.445 0 2.937-.011 3.285-.064 4.445-.049 1.072-.228 1.655-.379 2.042-.2.514-.437.88-.822 1.265-.385.385-.751.622-1.265.822-.387.151-.97.33-2.042.379-1.16.053-1.508.064-4.445.064-2.937 0-3.285-.011-4.445-.064-1.072-.049-1.655-.228-2.042-.379-.514-.2-.88-.437-1.265-.822-.385-.385-.622-.751-.822-1.265-.151-.387-.33-.97-.379-2.042-.053-1.16-.064-1.508-.064-4.445 0-2.937.011-3.285.064-4.445.049-1.072.228-1.655.379-2.042.2-.514.437-.88.822-1.265.385-.385.751-.622 1.265-.822.387-.151.97-.33 2.042-.379 1.16-.053 1.508-.064 4.445-.064M12 1c-2.987 0-3.362.013-4.535.066-1.171.053-1.97.24-2.67.511-.724.281-1.338.658-1.95 1.27-.612.612-.989 1.226-1.27 1.95-.271.7-.458 1.499-.511 2.67C1.013 8.638 1 9.013 1 12s.013 3.362.066 4.535c.053 1.171.24 1.97.511 2.67.281.724.658 1.338 1.27 1.95.612.612 1.226.989 1.95 1.27.7.271 1.499.458 2.67.511C8.638 22.987 9.013 23 12 23s3.362-.013 4.535-.066c1.171-.053 1.97-.24 2.67-.511.724-.281 1.338-.658 1.95-1.27.612-.612.989-1.226 1.27-1.95.271-.7.458-1.499.511-2.67.053-1.173.066-1.548.066-4.535s-.013-3.362-.066-4.535c-.053-1.171-.24-1.97-.511-2.67-.281-.724-.658-1.338-1.27-1.95-.612-.612-1.226-.989-1.95-1.27-.7-.271-1.499-.458-2.67-.511C15.362 1.013 14.987 1 12 1zm0 5.351A5.649 5.649 0 1 0 12 17.649 5.649 5.649 0 0 0 12 6.351zm0 9.316A3.667 3.667 0 1 1 12 8.333a3.667 3.667 0 0 1 0 7.334zm7.192-9.539a1.32 1.32 0 1 1-2.64 0 1.32 1.32 0 0 1 2.64 0z"/></svg></a><a href="https://www.tiktok.com/@jerseycitysound" aria-label="TikTok" title="TikTok"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M16.6 5.82a4.28 4.28 0 0 1-1.06-2.82h-3.09v12.4a2.59 2.59 0 0 1-2.59 2.5 2.6 2.6 0 0 1-2.6-2.6c0-1.72 1.66-3.01 3.37-2.48V9.66c-3.45-.46-6.47 2.22-6.47 5.64a5.7 5.7 0 0 0 5.69 5.7 5.7 5.7 0 0 0 5.69-5.7V9.01a7.35 7.35 0 0 0 4.3 1.38V7.3s-1.88.09-3.24-1.48z"/></svg></a><a href="https://www.youtube.com/@jerseycitysound" aria-label="YouTube" title="YouTube"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg></a></p>
    </div>
    <nav aria-label="Footer">
      <a href="archive.html">Archive</a>
      <a href="legends.html">Legends</a>
      <a href="history.html">History</a>
      <a href="chilltown.html">Chilltown</a>
      <a href="report.html">Sound Report</a>
      <a href="sources.html">Sources</a>
      <a href="about.html">About</a>
      <a href="suggest-edit.html">Suggest an edit</a>
    </nav>
  </div>
  <div class="footer__legal">
    <span>© 2026 The Jersey City Sound · Content licensed CC BY-SA 4.0</span>
    <nav class="footer__policies" aria-label="Policies">
      <a href="privacy.html">Privacy</a>
      <a href="terms.html">Terms</a>
      <a href="corrections.html">Corrections &amp; Removal</a>
    </nav>
    <span>Conceived 7 · 5 · 2026 — designed by <a href="https://robertvanliew.com">Robert Van Liew</a></span>
  </div>
</footer>

<script src="archive-data.js"></script>
<script>
(function () {
  var q = document.getElementById('archive-search');
  var az = document.getElementById('az');
  var empty = document.getElementById('empty');
  var count = document.getElementById('count');
  var filter = 'all';

  var params = new URLSearchParams(location.search);
  if (params.get('q')) q.value = params.get('q');

  function letterOf(name) {
    var n = name.replace(/^(The|DJ|A)\\s+/i, '');
    var c = n.charAt(0).toUpperCase();
    return /[A-Z]/.test(c) ? c : '#';
  }

  function render() {
    var term = q.value.trim().toLowerCase();
    var list = window.JCS_ENTRIES.filter(function (e) {
      if (filter !== 'all' && e.type !== filter) return false;
      if (!term) return true;
      return (e.name + ' ' + e.role + ' ' + e.no).toLowerCase().indexOf(term) !== -1;
    });
    count.textContent = list.length + ' of ' + window.JCS_ENTRIES.length + ' entries';
    var groups = {};
    list.forEach(function (e) {
      var L = letterOf(e.name);
      (groups[L] = groups[L] || []).push(e);
    });
    var letters = Object.keys(groups).sort();
    az.innerHTML = letters.map(function (L) {
      return '<section class="az-group"><h2>' + L + '</h2><ul class="ledger">' +
        groups[L].map(function (e) {
          return '<li><a href="' + e.href + '"><span class="no">№. ' + e.no +
            '</span><span class="name">' + e.name + '</span><span class="desc">' +
            e.role + (e.years ? ' · ' + e.years : '') + '</span></a></li>';
        }).join('') + '</ul></section>';
    }).join('');
    empty.hidden = list.length > 0;
  }

  q.addEventListener('input', render);
  document.getElementById('filters').addEventListener('click', function (ev) {
    var b = ev.target.closest('button[data-f]');
    if (!b) return;
    filter = b.dataset.f;
    this.querySelectorAll('button').forEach(function (x) {
      x.setAttribute('aria-pressed', String(x === b));
    });
    render();
  });
  render();
})();
</script>

<script src="archive-data.js"></script>
<script src="assets/nav-search.js" defer></script>
<script src="assets/protect.js" defer></script>
</body>
</html>
"""


def _shell(title, desc, canonical, body, memorial=False, current="", head_extra=""):
    logo = "jerseycitysound-cream.png" if memorial else "jerseycitysound-ink.png"
    def cur(name):
        return ' aria-current="page"' if name == current else ""
    body_attr = ' class="memorial"' if memorial else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{canonical}">
<meta name="robots" content="index, follow">
<link rel="icon" href="assets/favicon-32.png" sizes="32x32">
<link rel="icon" href="assets/favicon-64.png" sizes="64x64">
<link rel="apple-touch-icon" href="assets/favicon-180.png">
<meta property="og:type" content="website">
<meta property="og:site_name" content="The Jersey City Sound">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{SITE}/assets/og-card.png">
<meta name="twitter:card" content="summary_large_image">
{head_extra}<link rel="preload" as="font" type="font/woff2" href="assets/fonts/sourceserif-latin-37bedc60.woff2" crossorigin>
<link rel="stylesheet" href="assets/fonts/fonts.css">
<link rel="stylesheet" href="styles.css">
</head>
<body{body_attr}>

<header class="masthead wrap">
  <div class="masthead__logo masthead__logo--compact">
    <a href="index.html" aria-label="The Jersey City Sound — home">
      <img src="assets/{logo}" alt="Jersey City Sound" width="200" height="81">
    </a>
  </div>
  <nav class="nav" aria-label="Primary">
    <a href="index.html"{cur('home')}>Home</a>
    <a href="archive.html"{cur('archive')}>The Archive</a>
    <a href="charts.html"{cur('charts')}>On the Charts</a>
    <a href="legends.html"{cur('legends')}>Legends</a>
    <a href="history.html"{cur('history')}>History</a>
    <a href="report.html"{cur('report')}>The Sound Report</a>
    <a href="about.html"{cur('about')}>About</a>
    <div class="nav-search-wrap">
    <form class="nav-search" role="search" action="archive.html">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.8-3.8"/></svg>
      <input type="search" id="nav-search" name="q" placeholder="Search the archive…" autocomplete="off" aria-label="Search the archive" role="combobox" aria-controls="nav-suggest" aria-expanded="false">
      <ul class="search-suggest" id="nav-suggest" role="listbox" aria-label="Search suggestions"></ul>
    </form>
    </div>
  </nav>
</header>

{body}

<footer class="footer wrap">
  <div class="footer__grid">
    <div class="footer__brand">
      <img src="assets/{logo}" alt="Jersey City Sound" width="150" height="61">
      <p>Every voice in the city, on the record.</p>
      <p class="footer__social"><a href="https://x.com/jerseycitysound" aria-label="X (Twitter)" title="X"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg></a><a href="https://www.instagram.com/jerseycitysound" aria-label="Instagram" title="Instagram"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2.982c2.937 0 3.285.011 4.445.064 1.072.049 1.655.228 2.042.379.514.2.88.437 1.265.822.385.385.622.751.822 1.265.151.387.33.97.379 2.042.053 1.16.064 1.508.064 4.445 0 2.937-.011 3.285-.064 4.445-.049 1.072-.228 1.655-.379 2.042-.2.514-.437.88-.822 1.265-.385.385-.751.622-1.265.822-.387.151-.97.33-2.042.379-1.16.053-1.508.064-4.445.064-2.937 0-3.285-.011-4.445-.064-1.072-.049-1.655-.228-2.042-.379-.514-.2-.88-.437-1.265-.822-.385-.385-.622-.751-.822-1.265-.151-.387-.33-.97-.379-2.042-.053-1.16-.064-1.508-.064-4.445 0-2.937.011-3.285.064-4.445.049-1.072.228-1.655.379-2.042.2-.514.437-.88.822-1.265.385-.385.751-.622 1.265-.822.387-.151.97-.33 2.042-.379 1.16-.053 1.508-.064 4.445-.064M12 1c-2.987 0-3.362.013-4.535.066-1.171.053-1.97.24-2.67.511-.724.281-1.338.658-1.95 1.27-.612.612-.989 1.226-1.27 1.95-.271.7-.458 1.499-.511 2.67C1.013 8.638 1 9.013 1 12s.013 3.362.066 4.535c.053 1.171.24 1.97.511 2.67.281.724.658 1.338 1.27 1.95.612.612 1.226.989 1.95 1.27.7.271 1.499.458 2.67.511C8.638 22.987 9.013 23 12 23s3.362-.013 4.535-.066c1.171-.053 1.97-.24 2.67-.511.724-.281 1.338-.658 1.95-1.27.612-.612.989-1.226 1.27-1.95.271-.7.458-1.499.511-2.67.053-1.173.066-1.548.066-4.535s-.013-3.362-.066-4.535c-.053-1.171-.24-1.97-.511-2.67-.281-.724-.658-1.338-1.27-1.95-.612-.612-1.226-.989-1.95-1.27-.7-.271-1.499-.458-2.67-.511C15.362 1.013 14.987 1 12 1zm0 5.351A5.649 5.649 0 1 0 12 17.649 5.649 5.649 0 0 0 12 6.351zm0 9.316A3.667 3.667 0 1 1 12 8.333a3.667 3.667 0 0 1 0 7.334zm7.192-9.539a1.32 1.32 0 1 1-2.64 0 1.32 1.32 0 0 1 2.64 0z"/></svg></a><a href="https://www.tiktok.com/@jerseycitysound" aria-label="TikTok" title="TikTok"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M16.6 5.82a4.28 4.28 0 0 1-1.06-2.82h-3.09v12.4a2.59 2.59 0 0 1-2.59 2.5 2.6 2.6 0 0 1-2.6-2.6c0-1.72 1.66-3.01 3.37-2.48V9.66c-3.45-.46-6.47 2.22-6.47 5.64a5.7 5.7 0 0 0 5.69 5.7 5.7 5.7 0 0 0 5.69-5.7V9.01a7.35 7.35 0 0 0 4.3 1.38V7.3s-1.88.09-3.24-1.48z"/></svg></a><a href="https://www.youtube.com/@jerseycitysound" aria-label="YouTube" title="YouTube"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg></a></p>
    </div>
    <nav aria-label="Footer">
      <a href="archive.html">Archive</a>
      <a href="legends.html">Legends</a>
      <a href="history.html">History</a>
      <a href="chilltown.html">Chilltown</a>
      <a href="report.html">Sound Report</a>
      <a href="sources.html">Sources</a>
      <a href="about.html">About</a>
      <a href="suggest-edit.html">Suggest an edit</a>
    </nav>
  </div>
  <div class="footer__legal">
    <span>© 2026 The Jersey City Sound · Content licensed CC BY-SA 4.0</span>
    <nav class="footer__policies" aria-label="Policies">
      <a href="privacy.html">Privacy</a>
      <a href="terms.html">Terms</a>
      <a href="corrections.html">Corrections &amp; Removal</a>
    </nav>
    <span>Conceived 7 · 5 · 2026 — designed by <a href="https://robertvanliew.com">Robert Van Liew</a></span>
  </div>
</footer>

<script src="archive-data.js"></script>
<script src="assets/nav-search.js" defer></script>
<script src="assets/protect.js" defer></script>
</body>
</html>
"""


# Artists commonly misattributed to Jersey City (handoff §5). Each line is one
# machine-extractable correction: name, the denial, the correct place.
CHARTS_DISAMBIG = [
    ("Frank Sinatra", "is from Hoboken, not Jersey City. His daughter Nancy Sinatra and son Frank Sinatra Jr. were born in Jersey City."),
    ("Queen Latifah", "was born in Newark and raised in East Orange, not Jersey City, despite widespread online claims to the contrary."),
    ("Lauryn Hill", "is from South Orange, not Jersey City, despite widespread online claims to the contrary."),
    ("Shaquille O'Neal", "is from Newark, not Jersey City, by his own account."),
    ("Whitney Houston", "is from Newark, not Jersey City."),
    ("Sarah Vaughan", "is from Newark, not Jersey City."),
    ("Gloria Gaynor", "is from Newark, not Jersey City."),
    ("Dionne Warwick", "is from East Orange, not Jersey City."),
    ("Zakk Wylde", "was born in Bayonne, not Jersey City."),
    ("The Ad Libs", "(“The Boy from New York City”) formed in Bayonne, not Jersey City."),
    ("070 Shake", "is from North Bergen, not Jersey City."),
    ("Erick Morillo", "was raised in Union City, not Jersey City."),
    ("Ray Toro", "of My Chemical Romance is from Kearny, not Jersey City."),
    ("Fetty Wap", "is from Paterson, not Jersey City."),
    ("The Shirelles", "are from Passaic, not Jersey City."),
    ("Felipe Rose", "of the Village People lived only briefly in Jersey City; he is from Brooklyn and later settled in Asbury Park."),
]


def write_charts_hub(entries, data):
    """On the Charts (handoff §10): the roster of Jersey City artists with
    verified national chart history, rendered from the chart-data.json ledger,
    plus the misattribution corrections (§5). The hub asserts; the entries
    prove. Only render:true (cited) records appear."""
    by_href = {"entry-%s.html" % e["slug"]: e for e in entries}
    order = [("no1", "The Number Ones"),
             ("top40", "Top 40 and Gold"),
             ("genre", "Genre Charts and Broadcast")]
    groups = {k: [] for k, _ in order}
    for href, rec in CHART_DATA.items():
        if not rec.get("render") or not rec.get("hub_tier"):
            continue
        e = by_href.get(href)
        if not e:
            continue
        groups[rec["hub_tier"]].append((e["name"], href, rec.get("note", "")))

    sections, item_li, pos = "", [], 0
    for key, title in order:
        rows = groups[key]
        if not rows:
            continue
        lis = ""
        for name, href, note in rows:
            pos += 1
            item_li.append('        {"@type": "ListItem", "position": %d, "name": %s, "item": "%s/%s"}'
                            % (pos, json.dumps(name), SITE, href))
            lis += (f'\n        <li><a href="{href}"><span class="cr-name">{esc(name)}</span></a>'
                    f'<span class="cr-note">{esc(note)}</span></li>')
        sections += (f'\n  <section class="section wrap">\n'
                     f'    <div class="section__head"><h2 class="caps caps--wide">{title}</h2></div>\n'
                     f'    <ul class="charts-roster">{lis}\n    </ul>\n  </section>')

    dis_li = "".join(f'\n        <li><strong>{esc(n)}</strong> {esc(t)}</li>' for n, t in CHARTS_DISAMBIG)

    num_ones = ", ".join(n for n, _, _ in groups["no1"])
    faqs = [
        ("What famous musicians are from Jersey City?",
         "Jersey City's charted artists include " + num_ones +
         ", among many others documented in this archive."),
        ("Has a Jersey City artist ever had a number 1 on the Billboard Hot 100?",
         "Yes. Kool & the Gang, P.M. Dawn, The Manhattans, Nancy Sinatra, Marilyn McCoo, and Akon all reached No. 1 on the Billboard Hot 100, and Jersey City natives Frank Infante and members played on four Hot 100 number ones with Blondie."),
        ("Is Frank Sinatra from Jersey City?",
         "No. Frank Sinatra is from Hoboken. His daughter Nancy Sinatra and son Frank Sinatra Jr. were both born in Jersey City."),
        ("Is Queen Latifah from Jersey City?",
         "No. Queen Latifah was born in Newark and raised in East Orange, not Jersey City."),
        ("Is Lauryn Hill from Jersey City?",
         "No. Lauryn Hill is from South Orange, not Jersey City."),
    ]
    faq_visible = "".join(
        f'\n      <div class="faq-item"><h3>{esc(q)}</h3><p>{esc(a)}</p></div>' for q, a in faqs)
    faq_json = ",\n        ".join(
        '{"@type": "Question", "name": %s, "acceptedAnswer": {"@type": "Answer", "text": %s}}'
        % (json.dumps(q), json.dumps(a)) for q, a in faqs)

    canonical = f"{SITE}/charts.html"
    head_extra = f'''<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@graph": [
    {{
      "@type": "CollectionPage",
      "@id": "{canonical}#webpage",
      "url": "{canonical}",
      "name": "On the Charts — Jersey City's Charted Artists",
      "isPartOf": {{"@id": "{SITE}/#website"}},
      "about": {{"@id": "{SITE}/#org"}},
      "inLanguage": "en-US"
    }},
    {{
      "@type": "Dataset",
      "@id": "{canonical}#dataset",
      "name": "Jersey City Billboard chart history",
      "description": "Verified national chart records for artists with a documented Jersey City connection — Billboard Hot 100 number ones, chart peaks, and honors, each cited to a primary source.",
      "url": "{canonical}",
      "creator": {{"@id": "{SITE}/#org"}},
      "license": "https://creativecommons.org/licenses/by-sa/4.0/",
      "isAccessibleForFree": true,
      "keywords": ["Jersey City", "Billboard", "Hot 100", "chart history", "R&B", "soul", "hip-hop", "Chilltown"]
    }},
    {{
      "@type": "BreadcrumbList",
      "itemListElement": [
        {{"@type": "ListItem", "position": 1, "name": "Home", "item": "{SITE}/"}},
        {{"@type": "ListItem", "position": 2, "name": "On the Charts"}}
      ]
    }},
    {{
      "@type": "ItemList",
      "name": "Jersey City artists with national chart history",
      "itemListElement": [
{",\n".join(item_li)}
      ]
    }},
    {{
      "@type": "FAQPage",
      "mainEntity": [
        {faq_json}
      ]
    }}
  ]
}}
</script>
'''

    body = f'''<main>
  <header class="hero wrap" style="padding-bottom:1.5rem;">
    <span class="caps caps--gold">The Charts Wing</span>
    <h1 class="reveal reveal--2">Jersey City on the Billboard charts.</h1>
    <p class="lede reveal reveal--3">Every artist here has a verified national chart record and a documented Jersey City connection, stated plainly and cited on each entry. From the first No. 1 of the SoundScan era to a street-corner R&amp;B giant, these are the receipts.</p>
  </header>
{sections}

  <section class="section wrap" id="not-from">
    <div class="section__head"><h2 class="caps caps--wide">Commonly Misattributed</h2></div>
    <p style="max-width:62ch;color:#4a4636;">Widely syndicated lists, including real-estate and tourism blogs, credit several artists to Jersey City who are from elsewhere in the region. The record, corrected below, and the full story in <a href="report-001-not-from-jersey-city.html">The Sound Report</a>:</p>
    <ul class="disambig-list">{dis_li}
    </ul>
  </section>

  <section class="section wrap">
    <div class="section__head"><h2 class="caps caps--wide">Common Questions</h2></div>
    <div class="faq">{faq_visible}
    </div>
  </section>

  <section class="claim-strip wrap">
    <h2>Know a charted act we are missing?</h2>
    <p>The archive grows by receipts. If a Jersey City artist charted and is not here, or a fact needs a stronger source, tell us.</p>
    <a class="btn-ink" href="suggest-edit.html">Suggest an edit</a>
  </section>
</main>'''

    html = _shell("On the Charts — Jersey City's Charted Artists | The Jersey City Sound",
                  "Jersey City artists with verified Billboard chart history: the Hot 100 number ones, the top 40 and gold, the genre-chart and broadcast names, plus corrections of who is not from Jersey City.",
                  canonical, body, current="charts", head_extra=head_extra)
    (OUT / "charts.html").write_text(html, encoding="utf-8")
    print(f"Wrote charts.html ({pos} charted acts across {sum(1 for k,_ in order if groups[k])} tiers)")


def write_report_issue(entries):
    """The Sound Report, Issue No. 1 (handoff §17): the Jersey City
    misattribution correction piece. Its own indexable URL, Article + two
    ClaimReview blocks mirroring the visible corrections. Section 8 voice:
    connection-first, plain chart numbers, no dashes, receipts not fights."""
    canonical = f"{SITE}/report-001-not-from-jersey-city.html"
    jsonld = ('{\n'
        '  "@context": "https://schema.org",\n'
        '  "@graph": [\n'
        '    {\n'
        '      "@type": "Article",\n'
        '      "@id": "__CANON__#article",\n'
        '      "headline": "Is Queen Latifah From Jersey City? No, and the Truth Is Better",\n'
        '      "description": "The famous musicians actually from Jersey City, and the two names the internet keeps getting wrong.",\n'
        '      "mainEntityOfPage": "__CANON__",\n'
        '      "author": {"@type": "Organization", "name": "The Jersey City Sound", "url": "__SITE__/"},\n'
        '      "publisher": {"@id": "__SITE__/#org"},\n'
        '      "datePublished": "2026-07-12",\n'
        '      "dateModified": "__DATE__",\n'
        '      "inLanguage": "en-US"\n'
        '    },\n'
        '    {\n'
        '      "@type": "BreadcrumbList",\n'
        '      "itemListElement": [\n'
        '        {"@type": "ListItem", "position": 1, "name": "Home", "item": "__SITE__/"},\n'
        '        {"@type": "ListItem", "position": 2, "name": "The Sound Report", "item": "__SITE__/report.html"},\n'
        '        {"@type": "ListItem", "position": 3, "name": "Issue No. 1"}\n'
        '      ]\n'
        '    },\n'
        '    {\n'
        '      "@type": "ClaimReview",\n'
        '      "url": "__CANON__#latifah",\n'
        '      "claimReviewed": "Queen Latifah is from Jersey City.",\n'
        '      "author": {"@type": "Organization", "name": "The Jersey City Sound", "url": "__SITE__/"},\n'
        '      "datePublished": "2026-07-12",\n'
        '      "reviewRating": {"@type": "Rating", "ratingValue": 1, "bestRating": 5, "worstRating": 1, "alternateName": "False"},\n'
        '      "itemReviewed": {"@type": "Claim", "appearance": {"@type": "CreativeWork", "name": "Widely syndicated online lists of Jersey City musicians"}}\n'
        '    },\n'
        '    {\n'
        '      "@type": "ClaimReview",\n'
        '      "url": "__CANON__#hill",\n'
        '      "claimReviewed": "Lauryn Hill is from Jersey City.",\n'
        '      "author": {"@type": "Organization", "name": "The Jersey City Sound", "url": "__SITE__/"},\n'
        '      "datePublished": "2026-07-12",\n'
        '      "reviewRating": {"@type": "Rating", "ratingValue": 1, "bestRating": 5, "worstRating": 1, "alternateName": "False"},\n'
        '      "itemReviewed": {"@type": "Claim", "appearance": {"@type": "CreativeWork", "name": "Widely syndicated online lists of Jersey City musicians"}}\n'
        '    }\n'
        '  ]\n'
        '}').replace("__CANON__", canonical).replace("__SITE__", SITE).replace("__DATE__", BUILD_DATE)
    head_extra = f'<script type="application/ld+json">\n{jsonld}\n</script>\n'

    body = '''<main class="wrap" style="max-width:64rem;">
  <nav class="breadcrumb" aria-label="Breadcrumb">
    <a href="report.html">The Sound Report</a><span class="sep">&#8594;</span><span aria-current="page">Issue No. 1</span>
  </nav>
  <header class="entry-header">
    <span class="entry-no reveal reveal--1">The Sound Report &middot; Issue No. 1</span>
    <h1 class="reveal reveal--2">Is Queen Latifah From Jersey City? No, and the Truth Is Better</h1>
    <p class="descriptor reveal reveal--3">The famous musicians actually from Jersey City, and the two names the internet keeps getting wrong.</p>
  </header>
  <article class="entry-body reveal reveal--4" style="margin-inline:auto;">
    <p class="lead">Search "famous musicians from Jersey City" and two of the most famous answers do not hold up. Widely syndicated lists, including real estate and tourism blogs, credit Queen Latifah and Lauryn Hill to Jersey City. Both claims are false. Here is the record, corrected, and then the part that matters more: the truth is better than the myth.</p>

    <h2 id="corrections">The two corrections</h2>
    <p><strong>Is Queen Latifah from Jersey City? No.</strong> She was born in Newark and raised in East Orange. But Jersey City is genuinely in her story. The original Flavor Unit she came up with ran straight through this city: <a href="entry-apache.html">Apache</a>, <a href="entry-chill-rob-g.html">Chill Rob G</a>, and Latee were Jersey City rappers, and Apache ghostwrote on her album Black Reign. She is North Jersey royalty, and the map only gets more interesting when it is drawn accurately.</p>
    <p><strong>Is Lauryn Hill from Jersey City? No.</strong> She is from South Orange, the same Garden State soil, the maker of one of the greatest albums ever recorded, simply a different town's daughter.</p>
    <p>We are not naming the pages that got it wrong. The pattern is what matters: a list repeats a claim, an answer engine ingests it, and the error becomes the internet's default. The fix is not a fight. It is receipts.</p>

    <h2 id="the-truth">So who is actually from Jersey City?</h2>
    <p>The number ones first, because Billboard is Billboard.</p>
    <ul class="report-roster">
      <li><a href="entry-kool-and-the-gang.html">Kool &amp; the Gang</a> formed here in 1964. "Celebration" hit No. 1 on the Billboard Hot 100 in 1981, and the group entered the Rock and Roll Hall of Fame in 2024.</li>
      <li><a href="entry-pm-dawn.html">P.M. Dawn</a> formed here in 1988. "Set Adrift on Memory Bliss" was the first No. 1 of the Billboard SoundScan era, in 1991.</li>
      <li><a href="entry-the-manhattans.html">The Manhattans</a> formed here in 1962. "Kiss and Say Goodbye" reached No. 1 in 1976, among the first singles the RIAA ever certified platinum.</li>
      <li><a href="entry-nancy-sinatra.html">Nancy Sinatra</a> was born here in 1940. "These Boots Are Made for Walkin'" went to No. 1 in 1966.</li>
      <li><a href="entry-marilyn-mccoo.html">Marilyn McCoo</a> was born here in 1943, the lead voice of The 5th Dimension on multiple Hot 100 number ones.</li>
      <li><a href="entry-akon.html">Akon</a> spent his high school years here. He reached No. 1 twice, in 2006 and 2007.</li>
      <li><a href="entry-frank-infante.html">Frank Infante</a> was born here in 1951. As a member of Blondie he played on four Hot 100 number ones.</li>
    </ul>
    <p>Then the buried giant. <a href="entry-roy-hamilton.html">Roy Hamilton</a> was raised in Jersey City from his early teens. "You'll Never Walk Alone" spent eight weeks at No. 1 on the Billboard R&amp;B chart in 1954, and he was a documented influence on Elvis Presley. His is the single most under-told story on this list.</p>
    <p>And the line runs to the present. <a href="entry-joe-budden.html">Joe Budden</a> moved here at 13 and has repped the city throughout his career, from a Grammy-nominated Hot 100 single to one of the most influential podcast operations in music. The <a href="charts.html">full record lives on the charts hub</a>.</p>

    <h2 id="the-twist">The lists even got the athlete wrong</h2>
    <p>The same lists that misattributed the musicians also claim Shaquille O'Neal for Jersey City. He is from Newark, by his own repeated account. And here is the part that stings: Shaq is also a platinum rapper, "Shaq Diesel" and a Hot 100 hit in 1993, which is one more thing Newark gets to keep.</p>

    <h2 id="share">Share this story</h2>
    <div class="share" data-url="__CANON__" data-title="Is Queen Latifah From Jersey City? No, and the Truth Is Better">
      <button type="button" class="share__btn" data-act="native">Share&hellip;</button>
      <a class="share__btn" data-act="x" target="_blank" rel="noopener" href="https://twitter.com/intent/tweet?text=__XT__&amp;url=__CANONE__">X</a>
      <a class="share__btn" data-act="fb" target="_blank" rel="noopener" href="https://www.facebook.com/sharer/sharer.php?u=__CANONE__">Facebook</a>
      <button type="button" class="share__btn" data-act="copy">Copy link</button>
    </div>

    <aside class="claim-bar">
      <p>The archive is built to be corrected. If we got something wrong, tell us. That is the whole point.</p>
      <a href="suggest-edit.html">Suggest an edit &#8594;</a>
    </aside>
  </article>
</main>
<script src="assets/share.js" defer></script>'''
    body = (body.replace("__CANON__", canonical)
                .replace("__CANONE__", urllib.parse.quote(canonical))
                .replace("__XT__", urllib.parse.quote("Is Queen Latifah From Jersey City? No, and the Truth Is Better")))

    html = _shell("Is Queen Latifah From Jersey City? No, and the Truth Is Better | The Jersey City Sound",
                  "The famous musicians actually from Jersey City, and the two names the internet keeps getting wrong. Queen Latifah is from Newark and East Orange; Lauryn Hill is from South Orange. Here is who actually charted.",
                  canonical, body, current="report", head_extra=head_extra)
    (OUT / "report-001-not-from-jersey-city.html").write_text(html, encoding="utf-8")
    print("Wrote report-001-not-from-jersey-city.html")


def write_legends(entries, data):
    memorial = [e for e in entries if e.get("memorial")]
    memorial.sort(key=lambda e: e["name"].lower())
    cards = "\n".join(f"""      <article class="entry-card">
        <span class="entry-card__no">Entry №. {e['entry_no']}</span>
        <h3><a href="entry-{e['slug']}.html">{esc(e['name'])}</a></h3>
        <p class="entry-card__role">{esc(' · '.join(e.get('roles') or []))}</p>
      </article>""" for e in memorial)

    dc = data.get("discovered_candidates", {})
    named = dc.get("named_legends_for_legends_wing", [])
    named_names = [n.split(" (")[0] for n in named]
    in_mem = dc.get("in_memoriam", [])
    named_html = " · ".join(esc(n) for n in named_names)
    in_mem_html = " · ".join(esc(n) for n in in_mem)

    # Living legends — linked to their entries where one exists
    resolver = {e["name"].lower(): e["slug"] for e in entries}
    resolver.update({k.lower(): v for k, v in EXTRA_ALIASES.items()})

    def _ll(n):
        slug = resolver.get(n.lower())
        return f'<a href="entry-{slug}.html">{esc(n)}</a>' if slug else esc(n)

    living = dc.get("living_legends_for_legends_wing", [])
    living_html = " · ".join(_ll(n) for n in living)

    body = f"""<main class="wrap">
  <header class="entry-header" style="text-align:center;">
    <p class="memorial-mark caps reveal reveal--1">The Memorial Wing</p>
    <h1 class="reveal reveal--2" style="font-size:clamp(2.1rem,4.5vw,3.3rem);">Legends of the Jersey City Sound</h1>
    <p class="descriptor reveal reveal--3" style="margin-inline:auto;">The elders and the departed who built the Jersey City music scene — honored in full, in night and gold. Other departed artists born in the city are documented throughout the archive; this wing is for the scene's own. Every voice in the city, on the record.</p>
  </header>

  <section class="related" style="padding-top:2.5rem;">
    <div class="section__head"><h2 class="caps caps--wide">In Memoriam</h2></div>
    <div class="related__grid">
{cards}
    </div>
  </section>

  <section class="section" style="padding-top:3rem;">
    <div class="section__head"><h2 class="caps caps--wide">Living Legends of the Scene</h2></div>
    <p style="max-width:62ch;color:#b9b4a6;">The elders still with us — documented in the archive and honored here.</p>
    <p class="legends-list" style="font-size:var(--t-md);line-height:2;color:var(--cream);">{living_html}</p>
  </section>

  <section class="section" style="padding-top:2.5rem;">
    <div class="section__head"><h2 class="caps caps--wide">Also Documented by Name</h2></div>
    <p style="max-width:60ch;color:#b9b4a6;">Named in the record and honored here — full entries in progress.</p>
    <p style="font-size:var(--t-md);line-height:2;color:var(--cream);">{named_html}</p>
  </section>

  <section class="section" style="padding-top:2.5rem;padding-bottom:2rem;">
    <div class="section__head"><h2 class="caps caps--wide">Held in Memory</h2></div>
    <p style="font-size:var(--t-md);font-style:italic;color:var(--gold-light);">{in_mem_html}</p>
  </section>
</main>"""
    html = _shell("Legends — The Memorial Wing | The Jersey City Sound",
                  "The memorial wing of The Jersey City Sound: the elders and the departed who built the city's music scene, honored in night and gold.",
                  f"{SITE}/legends.html", body, memorial=True, current="legends")
    (OUT / "legends.html").write_text(html, encoding="utf-8")


def write_sources(entries):
    seen = {}
    for e in entries:
        for s in e.get("sources", []):
            url = s.get("url")
            label = s.get("label", "")
            if not url:
                continue
            seen.setdefault(url, {"label": label, "count": 0})
            seen[url]["count"] += 1
    items = sorted(seen.items(), key=lambda kv: kv[1]["label"].lower())
    rows = "\n".join(
        f'        <li><a href="{esc(url)}">{esc(v["label"])}</a>'
        f' <span class="caps" style="color:#8a8474;">· cited in {v["count"]} entr{"y" if v["count"]==1 else "ies"}</span></li>'
        for url, v in items)
    body = f"""<main class="wrap">
  <header class="entry-header" style="text-align:center;">
    <span class="entry-no reveal reveal--1">The Archive</span>
    <h1 class="reveal reveal--2" style="font-size:clamp(2.1rem,4.5vw,3.3rem);">Master Bibliography</h1>
    <p class="descriptor reveal reveal--3" style="margin-inline:auto;">Every externally-linked source cited across the archive. Oral history and internal research are cited on the entries themselves.</p>
  </header>
  <section class="section" style="padding-top:2rem;padding-bottom:2rem;">
    <ol class="sources" style="max-width:70ch;margin-inline:auto;font-size:var(--t-base);">
{rows}
    </ol>
  </section>
</main>"""
    html = _shell("Sources — Master Bibliography | The Jersey City Sound",
                  "The master bibliography of The Jersey City Sound — every externally-linked source cited across the archive.",
                  f"{SITE}/sources.html", body, current="")
    (OUT / "sources.html").write_text(html, encoding="utf-8")


def write_sitemap(entries):
    # Flat .html URLs — matching the actual filenames and canonicals (handoff Task 2).
    # report.html is now indexable (Issue №1 shipped) and included.
    hubs = ["", "archive.html", "legends.html", "history.html", "chilltown.html", "jersey-city-djs.html",
            "report.html", "about.html", "sources.html", "verify.html", "privacy.html", "terms.html",
            "corrections.html"]
    from datetime import date
    today = date.today().isoformat()

    def u(loc, prio):
        return (f"  <url><loc>{loc}</loc><lastmod>{today}</lastmod>"
                f"<changefreq>monthly</changefreq><priority>{prio}</priority></url>")

    rows = [u(f"{SITE}/", "1.0")]                       # homepage
    rows.append(u(f"{SITE}/charts.html", "0.9"))        # the charts hub — elevated (§11.8)
    rows.append(u(f"{SITE}/report-001-not-from-jersey-city.html", "0.8"))  # Sound Report Issue №1
    rows += [u(f"{SITE}/{h}", "0.6") for h in hubs[1:]]  # hub pages
    rows.append(u(f"{SITE}/entry-dj-dx.html", "0.8"))
    rows += [u(f"{SITE}/entry-{e['slug']}.html", "0.8") for e in entries]
    body = "\n".join(rows)
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
           f"{body}\n</urlset>\n")
    (OUT / "sitemap.xml").write_text(xml, encoding="utf-8")


def write_root_files(entries=None):
    ai_bots = ["Googlebot", "Google-Extended", "Bingbot", "GPTBot", "OAI-SearchBot",
               "ChatGPT-User", "PerplexityBot", "Perplexity-User", "ClaudeBot",
               "Claude-SearchBot", "Claude-User", "anthropic-ai", "Applebot",
               "Meta-ExternalAgent", "DuckAssistBot"]
    robots = (
        "# The Jersey City Sound — open to indexing and to AI answer engines.\n"
        "User-agent: *\nAllow: /\n\n"
        + "".join(f"User-agent: {b}\nAllow: /\n" for b in ai_bots)
        + f"\nSitemap: {SITE}/sitemap.xml\n"
    )
    (OUT / "robots.txt").write_text(robots, encoding="utf-8")

    # llms-full.txt — the entire archive as one markdown file (one-fetch for LLMs)
    if entries is not None:
        parts = [
            "# The Jersey City Sound — Full Archive\n",
            "> Every entry in the cited encyclopedia-archive of Jersey City (\"Chilltown\") music "
            "culture. Licensed CC BY-SA 4.0; free to quote with attribution.\n",
        ]
        for e in sorted(entries, key=lambda x: x["name"].lower()):
            roles = " · ".join(e.get("roles") or [])
            head = f"## {e['name']}"
            meta = " — ".join(x for x in (roles, e.get("years_active") or "") if x)
            parts.append(f"{head}\n{meta}\n" if meta else f"{head}\n")
            for f in e.get("facts", []):
                parts.append(f"- {f}")
            srcs = [s.get("label", "") for s in e.get("sources", []) if s.get("label")]
            if srcs:
                parts.append("Sources: " + "; ".join(srcs))
            parts.append(f"URL: {SITE}/entry-{e['slug']}.html\n")
        (OUT / "llms-full.txt").write_text("\n".join(parts), encoding="utf-8")
    llms = (
        "# The Jersey City Sound\n\n"
        "> The definitive encyclopedia-archive of Jersey City, New Jersey (\"Chilltown\") music "
        "culture — its DJs, rappers, producers, singers, groups, venues, crews, and record labels, "
        "documented with cited, neutral, encyclopedic entries across six decades. Every voice in the "
        "city, on the record.\n\n"
        "The archive covers Jersey City hip-hop, mixtape and blends DJs, rap, soul, and R&B — and the "
        "labels and venues behind them — from 1960s Catamount Records soul, through the 1980s park-jam "
        "era and the 1990s–2000s mixtape scene, to the present day. Content is licensed CC BY-SA 4.0 "
        "and free to quote with attribution to The Jersey City Sound.\n\n"
        "## What it documents\n"
        "- Jersey City DJs and mixtape legends — blends, battles, and the Stan's Square Records circuit\n"
        "- Rappers and groups — e.g. Ransom, Chill Rob G, Joe Budden, The A-Team, Sweet Slick and Slide\n"
        "- Producers, singers, and hitmakers — e.g. Grammy-nominated Mary Brown, and Kool & the Gang\n"
        "- Charted artists — Jersey City's Billboard Hot 100 number ones include Kool & the Gang, "
        "P.M. Dawn (the first No. 1 of the SoundScan era), The Manhattans, Nancy Sinatra, Marilyn McCoo, and Akon\n"
        "- Venues, record labels, crews, and the documentaries that recorded the scene\n\n"
        "## Key pages\n"
        f"- [On the Charts — Jersey City's Billboard chart history]({SITE}/charts.html)\n"
        f"- [The Archive (A–Z index)]({SITE}/archive.html)\n"
        f"- [History — the scene by era]({SITE}/history.html)\n"
        f"- [Why is Jersey City called Chilltown? — the documented history of the nickname]({SITE}/chilltown.html)\n"
        f"- [Jersey City DJs — the documented record of the city's DJ culture]({SITE}/jersey-city-djs.html)\n"
        f"- [Legends — the memorial wing]({SITE}/legends.html)\n"
        f"- [Sources — master bibliography]({SITE}/sources.html)\n"
        f"- [About & methodology]({SITE}/about.html)\n\n"
        "## Follow\n"
        "- X/Twitter: https://x.com/jerseycitysound\n"
        "- Instagram: https://www.instagram.com/jerseycitysound\n"
        "- TikTok: https://www.tiktok.com/@jerseycitysound\n"
        "- YouTube: https://www.youtube.com/@jerseycitysound\n\n"
        "## Founding\n"
        "Founded July 5, 2026. Founder: Robert Van Liew (DJ DX). Contact via the site's suggest-an-edit form.\n"
    )
    (OUT / "llms.txt").write_text(llms, encoding="utf-8")


def main():
    data = json.loads(DATA.read_text(encoding="utf-8"))
    entries = data["entries"]
    by_no = {e["entry_no"]: e for e in entries}
    name_links = build_name_links(entries)
    appearances = build_media_index(entries)
    written = set()
    for e in entries:
        out = OUT / f"entry-{e['slug']}.html"
        out.write_text(page(e, by_no, name_links, appearances), encoding="utf-8")
        written.add(out.name)

    # remove orphan pages for entries deleted/renamed in the data
    # (entry-dj-dx.html is handcrafted and lives outside this generator)
    keep = written | {"entry-dj-dx.html"}
    removed = []
    for f in OUT.glob("entry-*.html"):
        if f.name not in keep:
            f.unlink()
            removed.append(f.name)

    write_archive_data(HANDCRAFTED + entries)
    az_html, az_count = build_az_static(HANDCRAFTED + entries)
    archive_page = ARCHIVE_PAGE.replace(
        '<div id="az"></div>', f'<div id="az">\n{az_html}\n  </div>')
    archive_page = archive_page.replace(
        '<p class="caps archive-count" id="count"></p>',
        f'<p class="caps archive-count" id="count">{az_count}</p>')
    (OUT / "archive.html").write_text(archive_page, encoding="utf-8")
    write_legends(entries, data)
    write_charts_hub(entries, data)
    write_report_issue(entries)
    write_sources(entries)
    write_sitemap(entries)
    write_root_files(entries)
    # chart-data.json served copy for the client-side verifier (/data/chart-data.json)
    (OUT / "data").mkdir(exist_ok=True)
    (OUT / "data" / "chart-data.json").write_text(CHART_DATA_FILE.read_text(encoding="utf-8"), encoding="utf-8")
    note = f"; removed {len(removed)} orphan(s)" if removed else ""
    print(f"Wrote {len(written)} entry pages + archive/legends/sources/sitemap/robots/llms{note}")


if __name__ == "__main__":
    main()
