# The Jersey City Sound

A permanent, static HTML encyclopedia-archive of Jersey City, New Jersey music
culture — the DJs, artists, producers, venues, crews, and labels that built the
scene. Every claim is cited (cite-or-cut); the memorial "Legends" wing honors
the elders and the departed.

**Live site:** https://jerseycitysound.com

## How it works

Pure static HTML — no framework, no bundler, no server, no database. It runs on
any static host.

- **`data/entries.json`** — the source of truth: every entry, its facts,
  sources, cross-links, galleries, and media.
- **`execution/generate_entry_pages.py`** — the generator. Reads the data and
  writes every `entry-*.html` page plus the archive index, Legends wing,
  Sources page, sitemap, robots.txt, and llms.txt.
- **`design/`** — the built site that gets deployed (HTML, `styles.css`,
  `assets/`, media, and the client-side search index `archive-data.js`).
  `design/entry-dj-dx.html` is hand-authored; all other entry pages are
  generated.

## Regenerate the site

```
py execution/generate_entry_pages.py
```

This rewrites the generated pages from `data/entries.json` and removes orphaned
pages for entries that were deleted or renamed. The handcrafted DJ DX page is
left untouched.

## Deployment

The site is hosted on Vercel, which deploys the **`design/`** folder on every
push to `main` (settings in `design/vercel.json`). The apex domain serves the
site directly; `www` 308-redirects to it.

After each push, `.github/workflows/indexnow.yml` runs
`execution/indexnow_submit.py`, which tells IndexNow (Bing, Yandex, Naver,
Seznam, Yep) exactly which pages changed. The key is the public key file at the
site root. Google does not use IndexNow: resubmit `sitemap.xml` in Search
Console after a build that touches many pages, and request indexing by hand for
pages that matter.

Before pushing, `py execution/audit_links.py` lists any page with fewer than
three inbound internal links; the target is none.

## Contributing

Spotted an error or have a receipt to add? Use the **Suggest an edit** form on
any entry page, or email **contact@jerseycitysound.com**. Contributions are held
to the same cite-or-cut standard before publishing.

## License

Content is licensed **CC BY-SA 4.0**.
