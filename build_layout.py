#!/usr/bin/env python3
"""Apply the hi-fi layer to the LJ Brows static site (safe to re-run).

Usage:  python build_layout.py <site-dir> [--site-url https://example.com.au]

What it does for every *.html in <site-dir>:
  1. links assets/hifi.css (after style.css) and the favicon
  2. (re)writes the shared header + footer between @hifi markers, so every page
     gets the same markup and the correct "current page" state
  3. fills the image slots (hero orb, treatment cards, shop products, page-hero
     art, service-panel thumbnails) - each rule only matches the original markup,
     so a second run changes nothing
Edit HEADER / FOOTER / SLOT rules below to change the site-wide chrome in one place.
"""
import os
import re
import shutil
import sys

SITE = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else "."
SITE_URL = ""
if "--site-url" in sys.argv:
    SITE_URL = sys.argv[sys.argv.index("--site-url") + 1].rstrip("/")

HERE = os.path.dirname(os.path.abspath(__file__))
FRESHA_BNE = "https://www.fresha.com/a/lj-brows-studio-calamvale-662-compton-road-bs02an0m"
FRESHA_ADL = "https://www.fresha.com/bg/a/lj-brows-studio-greenacres-greenacres-shopping-centre-sy0194iz"
BOOK_URL = "https://www.fresha.com/providers/lj-brows-studio-e60eb3tq?menu=true&allOffer=true"
PH_BNE, PH_ADL = ("0416 713 325", "+61416713325"), ("0410 519 285", "+61410519285")
ICON = lambda n: f'<svg class="i" aria-hidden="true"><use href="#i-{n}"/></svg>'


# ------------------------------------------------------------------ header
def nav_link(href, label, page):
    cur = ' class="on" aria-current="page"' if href == page else ""
    return f'<li><a href="{href}"{cur}>{label}</a></li>'


def header_html(page):
    loc_on = page in ("brisbane.html", "adelaide.html")
    loc_btn_style = ' style="background:var(--olive-d);color:#fff"' if loc_on else ""

    def loc(href, label):
        cur = ' class="on" aria-current="page"' if href == page else ""
        return f'<li><a href="{href}"{cur}>{label}</a></li>'

    nav = (
        '<nav id="nav" aria-label="Main"><ul>'
        + nav_link("index.html", "Home", page) + nav_link("shop.html", "Shop", page)
        + nav_link("about.html", "About", page) + nav_link("services.html", "Services", page)
        + nav_link("gift-cards.html", "Gift Cards", page) + "\n"
        f'<li class="dd"><button class="ddb" type="button" aria-haspopup="true"{loc_btn_style}>Locations {ICON("chev")}</button>'
        f'<ul>{loc("brisbane.html", "Brisbane")}{loc("adelaide.html", "Adelaide")}</ul></li>\n'
        f'<li class="dd bk"><button class="ddb" type="button" aria-haspopup="true">Book Now {ICON("chev")}</button>'
        f'<ul><li><a href="{BOOK_URL}" target="_blank" rel="noopener">All services &amp; slots</a></li>'
        f'<li><a href="{FRESHA_BNE}" target="_blank" rel="noopener">Brisbane</a></li>'
        f'<li><a href="{FRESHA_ADL}" target="_blank" rel="noopener">Adelaide</a></li></ul></li>\n'
        + nav_link("contact.html", "Contact", page) + "</ul></nav>"
    )
    return (
        '<!-- @hifi:header -->'
        '<div class="topbar"><div class="wrap">'
        f'<p><a href="tel:{PH_BNE[1]}">{ICON("phone")}Brisbane {PH_BNE[0]}</a>'
        f'<a href="tel:{PH_ADL[1]}">{ICON("phone")}Adelaide {PH_ADL[0]}</a></p>'
        f'<p class="tb-r">{ICON("clock")}Open late Thursdays until 9pm</p></div></div>\n'
        '<header class="hdr"><div class="in glass">'
        '<a class="logo" href="index.html" aria-label="LJ Brows Studio home">'
        '<img class="lm" src="assets/img/logo-mark.svg" alt="" width="38" height="38">'
        '<span>LJ Brows <small>Studio</small></span></a>\n'
        + nav +
        f'<button class="cb" id="cb" aria-label="Open cart">{ICON("bag")}<b id="cc">0</b></button>'
        f'<button id="burger" aria-label="Menu" aria-expanded="false" aria-controls="nav">{ICON("menu")}</button>'
        '</div></header>'
        '<!-- @hifi:/header -->'
    )


# ------------------------------------------------------------------ footer
def footer_html():
    def studio(name, addr, phone, fresha, page):
        return (f'<div><h3>{name}</h3><address>{addr}<br>'
                f'<a href="tel:{phone[1]}">{ICON("phone")}{phone[0]}</a><br>'
                f'<a href="{page}">{ICON("pin")}Studio details</a></address>'
                f'<div class="row-b" style="margin-top:14px"><a class="btn sm" href="{fresha}" target="_blank" rel="noopener">Book {name}</a></div></div>')

    return (
        '<!-- @hifi:footer -->'
        '<footer class="ft">'
        '<div class="ft-cta"><div class="wrap"><div class="cta glass rv">'
        '<div><h2 class="serif">Ready for your glow?</h2>'
        '<p>Book brows, lashes, waxing or a facial at the studio nearest you.</p></div>'
        f'<div class="row-b"><a class="btn" href="{FRESHA_BNE}" target="_blank" rel="noopener">Book Brisbane</a>'
        f'<a class="btn pk" href="{FRESHA_ADL}" target="_blank" rel="noopener">Book Adelaide</a></div>'
        '</div></div></div>\n'
        '<div class="ft-body"><img class="ft-art" src="assets/img/footer-art.svg" alt="" width="420" height="290" loading="lazy">'
        '<div class="wrap"><div class="fg">'
        '<div class="fb"><a class="logo" href="index.html" aria-label="LJ Brows Studio home">'
        '<img class="lm" src="assets/img/logo-mark.svg" alt="" width="38" height="38" loading="lazy">'
        '<span>LJ Brows <small>Studio</small></span></a>'
        '<p class="serif tag">Empowering Your Beauty, Every Day,</p>\n'
        '<div class="soc"><a href="https://www.facebook.com/lj.brows.studio/" target="_blank" rel="noopener" aria-label="Facebook">'
        f'{ICON("fb")}</a><a href="https://www.instagram.com/ljbrowsstudio/" target="_blank" rel="noopener" aria-label="Instagram">'
        f'{ICON("ig")}</a></div></div>\n'
        '<div><h3>Explore</h3><ul><li><a href="index.html">Home</a></li><li><a href="shop.html">Shop</a></li>'
        '<li><a href="about.html">About</a></li><li><a href="services.html">Services</a></li>'
        '<li><a href="gift-cards.html">Gift Cards</a></li><li><a href="contact.html">Contact</a></li></ul></div>\n'
        + studio("Brisbane", "41/662 Compton Rd,<br>Calamvale QLD 4116", PH_BNE, FRESHA_BNE, "brisbane.html")
        + studio("Adelaide", "Greenacres Shopping Centre,<br>Muller Rd, Greenacres SA 5086", PH_ADL, FRESHA_ADL, "adelaide.html")
        + '\n<div><h3>Legal</h3><ul><li><a href="#">Privacy Policy</a></li><li><a href="#">Terms and Conditions</a></li>'
        '<li><a href="#">Return Policy</a></li></ul></div></div>\n'
        '<p class="cr"><span>Design and Build by Total Business Group</span></p></div></div></footer>'
        '<!-- @hifi:/footer -->'
    )



# ------------------------------------------------------------------ booking
def booking_html():
    steps = [("01", "Scan or tap", "Point your phone camera at the code, or use the button."),
             ("02", "Pick your treatment", "Brows, lashes, waxing, threading or facials, in Brisbane or Adelaide."),
             ("03", "Choose a time", "Select a slot that suits you and confirm your booking.")]
    stats = [("2", "Studios", "Brisbane &amp; Adelaide"), ("7", "Days a week", "Open every day"), ("9pm", "Thursdays", "Late-night appointments")]
    st = "".join(f'<li><span class="n">{n}</span><div><h3>{t}</h3><p>{d}</p></div></li>' for n, t, d in steps)
    sx = "".join(f'<li><b>{a}</b><span>{b}</span><small>{c}</small></li>' for a, b, c in stats)
    return (
        '<!-- @hifi:booking -->'
        '<section class="bk" id="book" aria-labelledby="bk-h"><div class="wrap"><div class="bk-panel rv">'
        '<div class="bk-main"><p class="bk-eyebrow">Online booking</p>'
        '<h2 id="bk-h" class="serif">Reserve your slot in a few taps</h2>'
        '<p class="bk-sub">Choose your studio, treatment and time on Fresha, where every LJ Brows Studio appointment is booked.</p>'
        f'<ol class="bk-steps">{st}</ol>'
        f'<div class="row-b"><a class="btn gold" href="{BOOK_URL}" target="_blank" rel="noopener">{ICON("spark")}Make a booking at LJ Brows Studio</a></div>'
        f'<ul class="bk-stats">{sx}</ul></div>'
        '<aside class="bk-qr" aria-label="Scan to book"><div class="qr-card"><div class="qr-frame">'
        '<img src="assets/img/fresha-qr.jpeg" alt="QR code to book at LJ Brows Studio on Fresha" width="240" height="240" loading="lazy">'
        '</div><p class="qr-t serif">Scan to book</p><p class="qr-s">Open your camera and point it at the code</p></div></aside>'
        '</div></div></section>'
        '<!-- @hifi:/booking -->'
    )

# -------------------------------------------------------------- slot rules
IMG = 'src="assets/img/{n}" alt="" width="{w}" height="{h}" decoding="async"'
TREAT = {
    "Brow Lamination": "treat-brow-lamination.svg",
    "Eyelash Lift": "treat-eyelash-lift.svg",
    "Classic Lash Extensions": "treat-lash-extensions.svg",
    "Facial (20 min)": "treat-facial.svg",
}
PRODUCT = {"spark": "prod-kit.svg", "eye": "prod-pen.svg", "thread": "prod-tweezers.svg", "drop": "prod-gel.svg"}
PAGE_ART = {"about.html": "about", "services.html": "services", "shop.html": "shop", "gift-cards.html": "gift",
            "contact.html": "contact", "brisbane.html": "brisbane", "adelaide.html": "adelaide"}
PANEL_THUMB = {"Waxing": "thumb-waxing.svg", "Threading": "thumb-threading.svg", "Eyebrow &amp; Lash": "treat-brow-lamination.svg",
               "Eyebrow & Lash": "treat-brow-lamination.svg", "Combos": "thumb-combos.svg", "Facial": "treat-facial.svg",
               "Lash Extensions": "treat-lash-extensions.svg"}


def fill_slots(html, page):
    n_changes = 0

    # hero orb -> illustration
    new = html.replace('<div class="orb"></div>',
                       '<div class="orb"><img ' + IMG.format(n="hero-eye.svg", w=600, h=600) + ' fetchpriority="high"></div>')
    n_changes += new != html
    html = new

    # treatment cards
    for title, f in TREAT.items():
        pat = re.compile(r'<div class="ico">.*?</div>(<h3) style="margin-top:16px">' + re.escape(title) + "</h3>", re.S)
        new = pat.sub(lambda m: f'<figure class="tim"><img {IMG.format(n=f, w=480, h=300)} loading="lazy"></figure>'
                                f"{m.group(1)}>{title}</h3>", html)
        n_changes += new != html
        html = new

    # shop products
    for icon, f in PRODUCT.items():
        pat = re.compile(r'<div class="art"><svg class="i" style="width:1em;height:1em" aria-hidden="true"><use href="#i-' + icon + r'"/></svg></div>')
        new = pat.sub(f'<div class="art"><img {IMG.format(n=f, w=320, h=200)} loading="lazy"></div>', html)
        n_changes += new != html
        html = new

    # page-hero art replaces the blob
    key = PAGE_ART.get(page)
    if key:
        new = html.replace('<span class="blob" data-d=".12" aria-hidden="true"></span>',
                           f'<img class="phart" data-d=".08" {IMG.format(n="ph-" + key + ".svg", w=400, h=400)}>')
        n_changes += new != html
        html = new

    # service panel thumbs
    for title, f in PANEL_THUMB.items():
        old = f"<header><h2>{title}</h2>"
        if old in html:
            html = html.replace(old, f'<header><img class="pimg" {IMG.format(n=f, w=68, h=68)} loading="lazy"><h2>{title}</h2>')
            n_changes += 1
    return html, n_changes


# ------------------------------------------------------------------ driver
def replace_region(html, name, new_html, legacy):
    marked = re.compile(rf"<!-- @hifi:{name} -->.*?<!-- @hifi:/{name} -->", re.S)
    if marked.search(html):
        return marked.sub(lambda m: new_html, html, count=1)
    if legacy.search(html):
        return legacy.sub(lambda m: new_html, html, count=1)
    raise SystemExit(f"could not find {name} region")


def process(path):
    page = os.path.basename(path)
    html = open(path, encoding="utf-8").read()

    if "assets/hifi.css" not in html:
        html = html.replace('<link rel="stylesheet" href="assets/style.css">',
                            '<link rel="stylesheet" href="assets/style.css"><link rel="stylesheet" href="assets/hifi.css">'
                            '<link rel="icon" type="image/svg+xml" href="assets/img/logo-mark.svg">', 1)
    if SITE_URL and "og:image" not in html:
        html = html.replace('<meta property="og:type"', f'<meta property="og:image" content="{SITE_URL}/assets/img/og-cover.png">'
                            '<meta property="og:type"', 1)

    html = replace_region(html, "header", header_html(page), re.compile(r'<header class="hdr">.*?</header>', re.S))
    html = replace_region(html, "footer", footer_html(), re.compile(r"<footer>.*?</footer>", re.S))
    html, n = fill_slots(html, page)
    if page == "index.html":
        marked = re.compile(r"<!-- @hifi:booking -->.*?<!-- @hifi:/booking -->", re.S)
        if marked.search(html):
            html = marked.sub(lambda m: booking_html(), html, count=1)
        else:
            html = re.sub(r'(<main id="main"><section class="hero">.*?</section>)', lambda m: m.group(1) + "\n" + booking_html(),
                          html, count=1, flags=re.S)
        if 'href="#book"' not in html:
            html = html.replace('>Adelaide</a></div></div>\n<div class="scene"',
                                f'>Adelaide</a><a class="btn gold" href="#book">{ICON("spark")}Scan &amp; Book</a></div></div>\n<div class="scene"', 1)
    open(path, "w", encoding="utf-8").write(html)
    return n


if __name__ == "__main__":
    os.makedirs(os.path.join(SITE, "assets"), exist_ok=True)
    shutil.copy(os.path.join(HERE, "..", "assets", "hifi.css"), os.path.join(SITE, "assets", "hifi.css"))
    os.makedirs(os.path.join(SITE, "assets", "img"), exist_ok=True)
    shutil.copy(os.path.join(HERE, "..", "assets", "fresha-qr.jpeg"), os.path.join(SITE, "assets", "img", "fresha-qr.jpeg"))
    for f in sorted(os.listdir(SITE)):
        if f.endswith(".html"):
            print(f"{f}: {process(os.path.join(SITE, f))} slot(s) filled")
