# LJ Brows Studio website

Static website for **LJ Brows Studio** - brows, lashes, waxing, threading and facials in **Brisbane** and **Adelaide**.
Plain HTML, CSS and JavaScript: no build step, no dependencies.

## Pages

| Page | File |
|---|---|
| Home (with online booking + Fresha QR) | `index.html` |
| Shop | `shop.html` |
| About | `about.html` |
| Services & prices | `services.html` |
| Gift cards | `gift-cards.html` |
| Contact | `contact.html` |
| Brisbane studio | `brisbane.html` |
| Adelaide studio | `adelaide.html` |

## Folder structure

```
.
├── index.html, shop.html, about.html, services.html,
│   gift-cards.html, contact.html, brisbane.html, adelaide.html
├── assets/
│   ├── style.css        design system
│   ├── hifi.css         hi-fi layer (header, footer, images, booking panel)
│   ├── main.js          cart, menu, animations, contact form
│   └── img/             illustrations, logo mark, Fresha QR, social cover
├── data/
│   └── studios.json     studio details, hours, booking links (reference)
├── docs/
│   └── brand-guide.md   palette, fonts, image inventory
├── tools/
│   └── lj-brows-hifi-site/   scripts that generate the images and shared header/footer
├── robots.txt
├── .nojekyll            tells GitHub Pages to serve files as-is
└── .gitignore
```

## Run locally

Open `index.html` in a browser, or serve the folder:

```bash
python3 -m http.server 8000   # then visit http://localhost:8000
```

## Publish on GitHub Pages

1. Upload everything in this folder to the root of your repository (branch `main`).
2. Repository **Settings -> Pages -> Build and deployment**: Source = *Deploy from a branch*, Branch = `main`, Folder = `/ (root)`.
3. After a minute the site is live at `https://<username>.github.io/<repository>/`.

All links are relative, so the site works from a sub-path as well as from a custom domain.

## Online booking

Bookings are handled on Fresha. The home page has a booking panel (`#book`) with the Fresha QR code and the
"Make a booking at LJ Brows Studio" button. To change them, edit `BOOK_URL` in
`tools/lj-brows-hifi-site/scripts/build_layout.py`, replace `assets/img/fresha-qr.jpeg`, and re-run the build below.

## Regenerating images / header / footer (optional)

The header, footer and illustrations are generated, so site-wide changes happen in one place:

```bash
python3 tools/lj-brows-hifi-site/scripts/gen_images.py assets/img      # illustrations
python3 tools/lj-brows-hifi-site/scripts/build_layout.py .             # header, footer, image slots, booking panel
```

Re-running is safe: it leaves unchanged pages unchanged. See `tools/lj-brows-hifi-site/SKILL.md` for details.
`tools/lj-brows-hifi-site/assets/hifi.css` is the source copy of `assets/hifi.css`.

## Contact details

Kept in `data/studios.json` for reference; the live values are in the HTML pages.
