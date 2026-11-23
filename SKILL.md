---
name: lj-brows-hifi-site
description: Adds hi-fi SVG illustrations (hero eye/brow art, treatment cards, shop products, page-hero art, service thumbnails, logo mark, favicon, OG cover) plus a shared hi-fi header (top bar, logo, Book Now CTA) and footer (CTA band, studio columns) to the LJ Brows Studio static HTML site. Use whenever the user wants to add, refresh, re-tint or extend images, headers or footers on lj-brows-studio.zip or its pages (index, shop, about, services, gift-cards, contact, brisbane, adelaide), or add a new page that must match the same header/footer.
---

# LJ Brows hi-fi site layer

The site is plain static HTML + `assets/style.css` + `assets/main.js` (olive / pink / gold glass UI, no build tooling).
This skill layers images and shared chrome on top without touching `style.css` or `main.js`.

## Workflow

1. Unzip the site to a working folder (`SITE`).
2. `python scripts/gen_images.py SITE/assets/img` - writes ~23 SVGs (deterministic, palette-matched).
3. `python scripts/build_layout.py SITE` - copies `assets/hifi.css`, links it in every page, rewrites the
   header/footer between `<!-- @hifi:header -->` / `<!-- @hifi:footer -->` markers, and fills the image slots.
   Safe to re-run: slot rules only match the original markup, header/footer are replaced by marker.
   Add `--site-url https://example.com.au` to also emit an absolute `og:image` meta tag.
4. Optional: `python scripts/render_og.py SITE/assets/img` for `og-cover.png` (needs playwright/chromium).
5. Screenshot at 1280 and 390 px (playwright, with `.rv{opacity:1!important}` injected so reveal-on-scroll
   content shows) and check header, hero, treatment cards, shop cards, footer before delivering.

## Home-page online booking (Fresha)

`build_layout.py` also inserts a luxury booking panel (`#book`, markers `@hifi:booking`) right after the home hero:
steps, stats, a gold "Make a booking at LJ Brows Studio" button (`BOOK_URL`) and the Fresha QR (`assets/fresha-qr.jpeg`,
decodes to the Fresha book-now link). The hero gets a "Scan & Book" button to `#book` and the Book Now menu gets an
"All services & slots" item. To change the link or QR edit `BOOK_URL` and replace `assets/fresha-qr.jpeg`.

## Where things live

- `scripts/gen_images.py` - all artwork. Primitives: `brow()` (procedural hairs), `eye()` (iris, lid, tapered
  lashes), `spoolie/tweezers/pen/bottle/tube/jar/spool`, `logo_mark()`. Palette gradients are in `DEFS`.
- `scripts/build_layout.py` - `header_html()`, `footer_html()` and the slot tables (`TREAT`, `PRODUCT`,
  `PAGE_ART`, `PANEL_THUMB`). Phone numbers and Fresha URLs are constants at the top.
- `assets/hifi.css` - all styling for the new chrome and slots (`.topbar`, `.dd.bk`, `.ft*`, `.tim`, `.art img`,
  `.phart`, `.pimg`, gift-card pattern).

## Conventions and gotchas

- Images are decorative (`alt=""`); the card text carries the meaning. Keep it that way unless a photo is
  informational.
- SVGs used through `<img>` cannot load web fonts, so text inside art uses Georgia/serif fallbacks.
- `main.js` depends on ids `#burger #nav #cb #cc .hdr` and `.rv`, `.tilt`, `[data-d]` - the header partial keeps them.
- Page-hero art uses `data-d` so the existing parallax in `main.js` still moves it.
- To add a page: copy any page, keep the `@hifi` markers, add it to `PAGE_ART` and the nav lists, re-run step 3.
- To swap in real photos later: keep the file name (e.g. `assets/img/hero-eye.svg` -> point the `<img>` at a `.jpg`
  with the same width/height) or edit the slot tables; add `loading="lazy"` for anything below the fold.
- The "Fresha" menu label was renamed "Book Now" (same two links). Footer tagline text is kept verbatim,
  including its trailing comma - flag to the owner rather than silently editing copy.
