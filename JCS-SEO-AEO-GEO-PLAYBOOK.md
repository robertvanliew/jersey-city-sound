# THE JERSEY CITY SOUND — SEO / AEO / GEO Playbook

Companion to `JERSEY-CITY-SOUND-DESIGN-SPEC.md`. Goal: when anyone — human or AI — asks about Jersey City music, this site is the answer. Traditional SEO gets ranked; AEO gets **cited**; GEO covers both generative engines and geographic relevance. We build all three into every page, not as an afterthought.

---

## 1. Target Query Map

| Intent | Queries | Owning Page |
|---|---|---|
| Scene (head) | jersey city djs, jersey city music scene, jersey city hip hop | /archive/ pillar + /history/ |
| Names | "{name}" dj, who is {name} jersey city | /archive/{slug}/ |
| History | history of jersey city hip hop, jersey city music history, 90s jersey city djs | /history/{era}/ |
| Lists | best djs in jersey city, top jersey city artists | /archive/ pillar (curated, methodology-free framing: "documented, not ranked") |
| Booking | book a dj jersey city, dj for wedding jersey city | future matcher tool page |
| Local color | chilltown music, journal square music venues, jersey city record stores | /history/ + venue entries |
| Zero-volume gold | every profile name = a query with almost no competition. 100 entries = 100 near-guaranteed #1s that compound authority for the head terms |

Rule: **one query family per page**, H1 and title match the query phrasing, no cannibalizing.

---

## 2. Traditional SEO Foundation

**Technical (locked in the spec, restated as law):** static Astro HTML — content visible without JS; correct self-canonicals on every page; XML sitemap auto-generated + submitted; clean 200s, no soft-404s; Core Web Vitals green (static + no frameworks = free pass); descriptive alt text on every archival photo.

**On-page pattern per entry:** title `{Name} — Jersey City {Role} | The Jersey City Sound`; H1 = name; lead paragraph contains name + "Jersey City" + role + era in the first 40 words; "Last updated" date visible; author line ("Archive entry by Robert Van Liew").

**Internal linking (hub-and-spoke):** /archive/ pillar links every entry; every entry links its era page + 3 related entries + relevant venues. Era pages link back to the pillar. No orphan pages, ever.

**Backlinks (local authority beats generic):** targets — Hoboken Girl, Jersey City Times, NJ.com, TapInto JC, JC cultural affairs / city pages, NJCU + Saint Peter's (radio/music depts), local venue sites, r/jerseycity. Pitch angle: "the first archive of JC music history" is a *story*, not a link request. Every documented person linking their own entry from their bios = dozens of natural links (the claim flywheel is also a link engine).

---

## 3. AEO — Getting Cited by AI (ChatGPT, Perplexity, AI Overviews, Claude, Gemini)

AI extracts **passages, not pages**. Princeton GEO research (KDD 2024): citing sources +40% visibility, statistics +37%, quotations +30%, keyword stuffing −10%. The archive format is naturally aligned — enforce it:

1. **Lead = extractable definition block.** Every entry opens with a 40–60 word self-contained summary that answers "who is X" with zero surrounding context needed. This is the sentence AI will quote.
2. **Receipts as statistics.** "1.47M Spotify streams," "25 years active," "resident at X from 1998–2004" — specific numbers with sources. Never "legendary," always countable.
3. **Quotations.** One sourced quote per entry where possible (from the subject or press) with name + title attribution.
4. **Numbered sources section** on every entry — the +40% factor, and the thing that separates an encyclopedia from a blog.
5. **FAQ blocks** on pillar and history pages ("Who were the first Jersey City DJs?", "Where did JC hip-hop start?") with `FAQPage` schema — natural-language H3s matching how people ask.
6. **Freshness:** visible "Last updated," update pillar pages quarterly minimum.
7. **robots.txt allows:** GPTBot, ChatGPT-User, PerplexityBot, ClaudeBot, anthropic-ai, Google-Extended, Bingbot. (Optionally block CCBot only.)
8. **/llms.txt** at root: one-paragraph site description + links to pillar, history, about, and the 25 flagship entries.
9. **Schema (per spec §3):** Person/MusicGroup + BreadcrumbList per entry; Organization + WebSite sitewide; FAQPage on pillars; `Article` with author/date on history + report pages. Schema-marked content shows 30–40% higher AI visibility.
10. **Third-party presence** — brands are 6.5x more likely to be cited via third parties: Wikidata items (site + notable figures), r/jerseycity participation with receipts, local press features. A Wikipedia mention outweighs ten blog posts.

---

## 4. GEO — Geographic Entity Dominance

Make the site the strongest *entity* attached to "Jersey City" + music:

- **Entity saturation, naturally:** entries name real neighborhoods (Greenville, The Heights, Journal Square, Bergen-Lafayette, Downtown, McGinley Square), venues, streets, and years. AI models map entity co-occurrence; every accurate local detail strengthens the site's claim to the geography.
- **Organization schema:** `areaServed: Jersey City, NJ`, `foundingDate: 2026-07-05`, founder → Robert Van Liew (link his Wikidata Q17579958 via sameAs).
- **Wikidata spine:** item for The Jersey City Sound (instance of: digital archive / online database; subject: music of Jersey City) linked both ways with entries. This survives even the domain and feeds every model's knowledge graph.
- **Venue + place entries** get `Place`/`MusicVenue` schema with geo coordinates — the only structured local music data that will exist for JC.
- **The annual report:** "State of the Jersey City Sound {year}" — original data (entry counts, era analysis, streams aggregates). Original research earns ~12% of all AI citations and is the #1 backlink magnet. Publish yearly, same URL pattern.

---

## 5. Priority Build Order (content that ranks first)

1. `/archive/` pillar — "Jersey City DJs & Artists: The Complete Archive" (head-term owner)
2. Entries №1–10 (names = instant rankings, immediate claim-flywheel fuel)
3. `/history/` + first era page — "The History of Jersey City Hip-Hop & DJ Culture" (definitive-guide format, ~15% of AI citations)
4. FAQ blocks on both pillars
5. Entries №11–25 + first venue entries
6. State of the Scene report #1

## 6. Monitoring (monthly, 30 minutes)

- Google Search Console: impressions/clicks for the query map; fix anything indexed wrong.
- AI answer log: run the top 20 queries through ChatGPT, Perplexity, and Google AI Overviews; record cited-or-not and who is; track month over month in one sheet.
- Validate schema after any template change (Rich Results Test).

## 7. 90-Day Targets

- Day 30: indexed, all schema valid, 10 entries live, GSC baseline logged.
- Day 60: 25 entries, history pillar live, 5+ local backlinks, first AI citation observed for a name query.
- Day 90: ranking page 1 for ≥3 name queries + "jersey city djs" in top 20; cited by at least one AI platform for a scene query; first claimed profiles linking back.

*Structure makes it extractable. Receipts make it citable. Presence makes it inevitable.*
