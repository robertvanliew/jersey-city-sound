# THE JERSEY CITY SOUND — Design & Build Spec

**Project:** The definitive encyclopedia-archive of Jersey City DJs, artists, and music culture.
**Positioning:** Wikipedia's structure, Britannica's gravity, liner-note soul. A monument, not a media site.
**Mission line:** "Every voice in the city, on the record."
**Founding date numerology:** Conceived 7/5/2026 → 7+5+2+0+2+6 = 22, the Master Builder.
**Owner:** Frankpella LLC. **Domain:** jerseycitysound.com (register 10 yrs, auto-renew, LLC-owned). Defensive: chilltownsound.com, jerseycityrecords.com, chilltownlegends.com → 301 redirect.

---

## 1. Brand System

### 1.1 Logos (Jersey City Sound wordmark only — all other marks reserved for separate projects)
| File | Use |
|---|---|
| `jerseycitysound-primary` | Light backgrounds, print, default |
| `jerseycitysound-reversed` | Dark backgrounds |
| `jerseycitysound-transparent` / `-transparent-light` | Overlays (ink / cream) |

Favicon/avatar: crop the record O from the wordmark at square sizes (512/180/64) until a dedicated mark is chosen.

Rules: never stretch, never recolor outside the palette, never place the cream-accent versions on light backgrounds (use mono). Clear space = height of the record O on all sides.

### 1.2 Color Tokens
```css
--ink:        #0B0B0C;  /* primary text, JCS logo ink */
--paper:      #F7F4EC;  /* page background (archival paper, slightly warm) */
--cream:      #F5F2EA;  /* reversed text, accents on dark */
--night:      #0E0E10;  /* Legends section background */
--gold:       #C9A227;  /* primary gold */
--gold-light: #EED27A;  /* gradient top */
--gold-deep:  #9C7A14;  /* gradient bottom */
--gold-ink:   #7A5E0E;  /* gold that reads on light backgrounds */
--gold-mid:   #B89221;  /* universal gold accents */
--rule:       #D9D2C2;  /* hairlines on paper */
```
Gold gradient (vertical): `#EED27A → #C9A227 (55%) → #9C7A14`.

### 1.3 Typography
- **Entry titles / headlines:** serious serif with authority — Freight Text, Tiempos, or free: *Source Serif 4 / Playfair Display (sparingly)*.
- **Body:** highly readable serif or humanist sans — *Source Serif 4* body, or *Inter* if sans.
- **Meta / labels / small caps:** letterspaced caps (tracking +80 to +140), echoing the JERSEY CITY line of the wordmark. Free: *Archivo* or *Inter* in all-caps.
- Scale: 1.25 modular. Body 17–18px, line-height 1.65. Measure ~68ch max.
- Numbers styled like pressings: "ENTRY №. 001" in letterspaced caps + gold.

### 1.4 Design Principles (Premium Encyclopedia)
1. Typography does the luxury. Whitespace is the second designer.
2. Hairline rules, never boxes. Gold used like gilding — 5% of any page, max.
3. Paper light-mode by default; **the Legends memorial wing inverts to night + gold** (JCS reversed logo there, not a separate brand).
4. Museum-label tone: factual, warm, zero hype, zero beef. Receipts over adjectives.
5. Every page looks typeset, not templated. No stock icons, no drop shadows, no gradients except brand gold.
6. Photography: duotone or B&W treatment for era consistency; color allowed in galleries.

---

## 2. Site Architecture

```
jerseycitysound.com/
├── /                       Homepage: search-first, featured entries, latest additions
├── /archive/               A–Z index; filters: role (DJ/artist/producer/venue/crew), era, genre
│   └── /archive/[slug]/    ENTRY PAGES — the core unit (e.g. /archive/dj-dx/)
├── /legends/               Legends — memorial wing (night/gold theme)
│   └── /legends/[slug]/
├── /history/               Scene timeline by era (/history/1980s/ etc.)
├── /report/                The Sound Report — short editorial + newsletter archive
├── /about/                 Founding story, methodology, permanence commitment, CC BY-SA notice
├── /claim/                 Claim-your-profile flow (the flywheel)
└── /sources/               Master bibliography
```

URL rules: lowercase, hyphenated, human names as slugs, no dates in slugs, no trailing querystrings. Every page self-canonical (this killed djdxmusic.com — never again).

---

## 3. Entry Page Anatomy (the core template)

Order, top to bottom:
1. **Breadcrumb** (Archive → DJs → Name) — with BreadcrumbList schema.
2. **Entry header:** "ENTRY №. 001" · Name in serif display · one-line descriptor · era chips.
3. **Record Card (infobox, right rail on desktop / top on mobile):** portrait (duotone), years active, roles, genres, notable works with numbers, affiliations, official links, "In the archive since" date. Gold hairline frame.
4. **Lead paragraph** — 2–3 sentence neutral summary (this is what AI models quote).
5. **Sections:** Career · Notable Works · Credits & Receipts · In the Community · Gallery.
6. **Sources** — numbered citations, real links.
7. **Claim bar:** "Is this you? Claim and complete this entry." → /claim/
8. **Related entries** (3, by era/role overlap).

### JSON-LD (non-negotiable, every entry)
- `Person` (or `MusicGroup`/`Place`): name, alternateName, jobTitle, genre, url, image, sameAs → [official site, Spotify, Instagram, Wikidata].
- `BreadcrumbList`.
- Site-wide: `Organization` ("The Jersey City Sound", logo, founder, foundingDate 2026-07-05) + `WebSite` with SearchAction.

---

## 4. SEO / AEO Requirements
- **Static HTML, prerendered. Astro.** No client-side-rendered content, ever.
- Title pattern: `{Name} — Jersey City {Role} | The Jersey City Sound`
- Meta description ≤ 155 chars, written per entry, factual.
- XML sitemap + auto-submit; robots.txt open; RSS for /report/.
- Wikidata: create item for the site (Organization); link entries to existing items (DJ DX = Q17579958); add items for notable undocumented figures over time.
- Internal linking: every entry links ≥3 related entries + its era page.
- Target queries: "jersey city djs", "jersey city music scene", "jersey city hip hop history", "{name} dj jersey city", "book a dj jersey city" (→ future matcher tool).

---

## 5. Tech & Permanence Spine
- **Stack:** Astro + plain CSS (tokens above) → static output. No database. Content as Markdown/JSON per entry in the repo.
- **Repo:** public GitHub, MIT for code, **CC BY-SA 4.0 for content** (stated in footer + /about/).
- **Hosting:** Cloudflare Pages (free, fast). 
- **Permanence checklist:**
  - [ ] Domain: 10-year registration, auto-renew, 2 payment methods, owned by Frankpella LLC
  - [ ] Public repo = anyone can mirror in 5 minutes
  - [ ] Wayback Machine submission on every deploy (simple API ping)
  - [ ] Arweave snapshot at launch + yearly
  - [ ] Succession doc: credentials location, deploy steps, steward = Julie; GitHub successor set
  - [ ] Wikidata entries (survive even the domain)

---

## 6. Content Rules
- **Never mention competitors or lists. Ever.** Generosity is the positioning.
- Everyone from the scene gets documented accurately — including people who snubbed you. That's the power move.
- Verifiable claims only; cite or cut. Neutral encyclopedic voice; let numbers talk (streams, credits, years).
- Robert Van Liew / DJ DX = Entry №. 001, written by the same rules as everyone. Julie Schatz = Entry №. 002.
- First 25 entries: pull from JCIT's covered names + the omitted (Nel El Blends, Wiz TV, DJ Madden, etc.) + elders for /legends/.

## 7. Launch Sequence
1. Register domains (today).
2. Build homepage + Entry №. 001 template → review → lock design.
3. Write/build first 10 entries → soft launch → submit sitemap, Wayback, schema validation.
4. Outreach: personally invite each documented person to claim their entry (the flywheel).
5. Entries 11–25 + first /history/ era page + Sound Report #1.
6. Arweave snapshot. Announce.

*Built different. Sealed on a Master Builder day. — The Jersey City Sound*
