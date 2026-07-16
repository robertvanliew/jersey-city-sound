# The Jersey City Sound — Editorial Charter & SEO Handoff

*Adopted 2026-07-16. This is the governing document for what gets published and how the archive earns search visibility. When in doubt, this file wins.*

## Project

The Jersey City Sound (jerseycitysound.com) is a permanent, cited encyclopedia-archive of Jersey City music culture: DJs, artists, producers, groups, venues, labels, mixtapes, and the people who built the scene.

Its purpose is not to be a hype page, open directory, or rankings site. It should become the most trusted public record of Jersey City music.

**Core line:** Every voice in the city, on the record.

## Non-Negotiable Editorial Standard

The archive documents **contribution, not self-description**.

Do not publish someone simply because they submit themselves, call themselves a legend, have followers, or say they were active in the scene. Every published entry needs verifiable evidence:

- A release, credit, flyer, video, venue listing, credible press coverage, chart record, or corroborated named firsthand testimony.
- Community contributions are leads for research, not automatic publication.
- No unsupported "famous," "legendary," or "pioneer" language.
- If the public record is not strong enough yet, hold the name privately until evidence arrives.

Public contribution language (used on the About and Suggest-an-Edit pages):

> We welcome leads, memories, photographs, flyers, recordings, and corrections — but publication requires verifiable evidence. Every entry is researched, cited, and reviewed before it joins the record.

## Quality Gate (pre-publication checklist)

Every new page, before it ships:

1. **Source check** — every claim traces to a listed source; no source, no claim.
2. **Fact check** — sources actually say what the entry says (fetch and read them, don't trust search snippets; name-collision check for common DJ names).
3. **Title / meta check** — unique title, meta description under ~158 characters, no truncated ellipsis, editorial framing correct (`jc_from` flag for non-JC-origin figures).
4. **Internal links** — the entry links to its related entries/hub; the hub or archive index links back.
5. **Seal check** — if article content on a *sealed* entry changed, reseal (`node scripts/seal.mjs reseal entry-<slug>`) and run `verify-all` before push.
6. **The ten-year test** — would we stand by this page, as written, in ten years?

## Hold Queue

Unverified names, rumors, and partial leads live in a **private research queue — not on the live site**.

- **Where it lives:** `data/entries.json` → `discovered_candidates.held_pending_source` (plus the other `discovered_candidates` research keys).
- Each held name records **what proof is missing**, so research is focused.
- A name leaves the queue only by clearing the editorial standard above.
- The queue is also the kind answer to social pressure: "it's in research" is true and publishable-neutral.

## Oral-History Protocol

Much of the mixtape era exists only in memory. Firsthand testimony is a legitimate source when captured properly:

- **Capture:** speaker name, date, the speaker's relationship to the event, the exact claim, and any supporting artifact (tape, flyer, photo).
- **Attribute as oral history, not universal fact** — and the attribution appears **on the public page**, relationship included: *"per DJ DX, a firsthand participant in the mixtape era (2026)."*
- Corroborated testimony from two independent named witnesses upgrades a claim's standing.
- Uncorroborated anonymous claims are leads for the hold queue, never publishable facts.

## Red Lines

- No paid placement.
- No "top/best" rankings.
- No follower-count validation (an account's size is never evidence of contribution).
- No copied bios.
- No uncredited photos.
- No publishing to satisfy friendships, pressure, or local politics.

**The archive's power comes from what it refuses to publish as much as what it preserves.**

---

# SEO

## Goal

When someone searches for Jersey City music, people, scenes, and history, The Jersey City Sound should be the best sourced answer — not because it stuffed keywords, but because it created the strongest page for each real question.

## Keyword Strategy — the Jersey City Music Language Map

Build queries from four components:

- **Place:** Jersey City, Jersey City NJ, Chilltown, 201, Journal Square, Greenville, The Heights, Bergen-Lafayette.
- **Role:** musician, artist, rapper, DJ, producer, R&B singer, band, venue, label.
- **Scene:** hip-hop, R&B, Jersey club, mixtapes, record stores, music history.
- **Intent:** famous, notable, from, born in, history, 1990s, 2000s, documentary, list.

Each keyword cluster has **one clear owner page**. No two pages compete for the same phrase.

## Current owners (starting position)

| Cluster | Owner page | Status |
|---|---|---|
| Jersey City music history / eras | `history.html` | live |
| Charted artists from Jersey City | `charts.html` | live |
| Directory / A–Z intent | `archive.html` | live |
| Memorial / legends | `legends.html` | live |
| **Chilltown** ("what is Chilltown Jersey City") | — | **to build — highest-value gap** |
| **Jersey City DJs** / mixtape DJ history | — | **to build — unfair advantage (2006 doc + 60+ DJ entries)** |
| **Jersey City hip-hop / rappers** | — | to build |
| Jersey City R&B | — | later, when evidence depth justifies it |
| Place/era pages (Journal Square venues, record stores, 1990s…) | — | later |

## Hub-page rules

- Open with a **40–60-word direct answer block** (serves featured snippets *and* AI citation).
- A hub is a verified, cross-genre guide — **never a ranking**.
- **Internal-linking loop:** hub links down to its entries; entries link up to their hub. This is what makes clusters rank.
- Only build a hub when the archive can answer it credibly. A high-demand query without evidence is a research priority, not a page.

## Research inputs (quarterly, lightweight)

One keyword sheet: `docs/keyword-map.md` — `Query | Cluster | Intent | Owner page | Evidence ready? | Priority | Notes`.

Quarterly pass: Google Search Console actual queries → autocomplete / People Also Ask → update the sheet. Trends/Ahrefs only when deciding whether to build a new hub. (Monthly cadence was considered and rejected as unsustainable for a one-person shop.)

Ongoing, as research (not SEO): local newspapers, library collections, venue calendars, flyers, record credits, videos, oral histories — the source of authentic local language.

## Success metrics

- Indexed pages; Search Console impressions and clicks.
- Rankings for the priority clusters above.
- Quality local backlinks (news, libraries, venues, artists).
- Corrections resolved.
- **North star: entries meeting the highest evidence standard** — tracked as the `status` tier distribution over time (`doc-verified` / `web-verified` / `community-verified` / `handle-provided`), and specifically the count of stubs upgraded each quarter. Run `py execution/metrics_report.py` for the snapshot.
- AI-answer citations of jerseycitysound.com (manual monthly check in ChatGPT/Perplexity/AI Overviews).

## The loop

**Real search language → documented research → authoritative page → citations and links → better search visibility → new research leads.**
