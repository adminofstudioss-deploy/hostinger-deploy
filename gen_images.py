#!/usr/bin/env python3
"""Generate the hi-fi SVG illustration set for the LJ Brows Studio site.

Usage:  python gen_images.py <site>/assets/img

Everything is procedural (brow hairs, lashes, objects) and uses the site's own
palette, so re-running is deterministic and the whole set can be re-tinted by
editing PALETTE / DEFS below.
"""
import math
import os
import random
import sys

OUT = sys.argv[1] if len(sys.argv) > 1 else "assets/img"
os.makedirs(OUT, exist_ok=True)

SERIF = "Georgia, 'Times New Roman', serif"
HAIR = ["#4a3224", "#5b4030", "#3a261b", "#6a4a37", "#2f1e15"]

DEFS = """<defs>
<linearGradient id="gBg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#DCE3C3"/><stop offset="1" stop-color="#F4D3DA"/></linearGradient>
<linearGradient id="gBg2" x1="0" y1="1" x2="1" y2="0"><stop offset="0" stop-color="#F4D3DA"/><stop offset="1" stop-color="#DCE3C3"/></linearGradient>
<linearGradient id="gCream" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFFFFF"/><stop offset="1" stop-color="#EBE3D3"/></linearGradient>
<linearGradient id="gCreamBg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FBF8F2"/><stop offset="1" stop-color="#DCE3C3"/></linearGradient>
<radialGradient id="gSkin" cx=".32" cy=".22" r="1"><stop offset="0" stop-color="#FBE3D3"/><stop offset=".55" stop-color="#F2CBB6"/><stop offset="1" stop-color="#E2AB94"/></radialGradient>
<linearGradient id="gGold" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#F6E6BC"/><stop offset=".45" stop-color="#B8975A"/><stop offset="1" stop-color="#8A6B33"/></linearGradient>
<linearGradient id="gOlive" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#A9B676"/><stop offset="1" stop-color="#5A6B33"/></linearGradient>
<linearGradient id="gOliveV" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#B7C382"/><stop offset="1" stop-color="#5A6B33"/></linearGradient>
<linearGradient id="gPink" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FCE9ED"/><stop offset="1" stop-color="#E3A6B5"/></linearGradient>
<linearGradient id="gPinkV" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FCE9ED"/><stop offset="1" stop-color="#E3A6B5"/></linearGradient>
<linearGradient id="gCreamV" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFFFFF"/><stop offset=".6" stop-color="#F1EADB"/><stop offset="1" stop-color="#D8CFB9"/></linearGradient>
<linearGradient id="gMetalV" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f4f6f7"/><stop offset=".35" stop-color="#b4babe"/><stop offset=".6" stop-color="#eceff0"/><stop offset="1" stop-color="#868b8f"/></linearGradient>
<linearGradient id="gHandle" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#E4EACB"/><stop offset=".5" stop-color="#8C9A5B"/><stop offset="1" stop-color="#5A6B33"/></linearGradient>
<linearGradient id="gBrown" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8a6247"/><stop offset="1" stop-color="#2f1e15"/></linearGradient>
<linearGradient id="gHoney" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#F8DC8E"/><stop offset="1" stop-color="#D79A3A"/></linearGradient>
<linearGradient id="gGlass" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".95"/><stop offset="1" stop-color="#fff" stop-opacity=".2"/></linearGradient>
<linearGradient id="gLid" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5a2e22" stop-opacity=".55"/><stop offset=".45" stop-color="#5a2e22" stop-opacity="0"/></linearGradient>
<radialGradient id="gIris" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#e2b574"/><stop offset=".5" stop-color="#97633a"/><stop offset=".85" stop-color="#4a2c19"/><stop offset="1" stop-color="#2a170d"/></radialGradient>
<radialGradient id="gSclera" cx=".5" cy=".4" r=".7"><stop offset="0" stop-color="#fffdfa"/><stop offset="1" stop-color="#eadbd5"/></radialGradient>
<radialGradient id="gSph" cx=".3" cy=".25" r=".9"><stop offset="0" stop-color="#fff"/><stop offset=".25" stop-color="#fbe3e8"/><stop offset=".6" stop-color="#cdd7a4"/><stop offset="1" stop-color="#7d8c4e"/></radialGradient>
<radialGradient id="gDisc" cx=".3" cy=".25" r=".95"><stop offset="0" stop-color="#FFFFFF"/><stop offset=".45" stop-color="#F9E4E8"/><stop offset="1" stop-color="#CBD6A0"/></radialGradient>
<filter id="fBlur" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="16"/></filter>
<filter id="fBlur6" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="4.5"/></filter>
<filter id="fBlur2" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="1.6"/></filter>
</defs>"""


# ----------------------------------------------------------------- helpers
def P(x, y):
    return f"{x:.1f},{y:.1f}"


def bez(p0, p1, p2, p3, t):
    u = 1 - t
    return (u**3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t**3 * p3[0],
            u**3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t**3 * p3[1])


def bezd(p0, p1, p2, p3, t):
    u = 1 - t
    return (3 * u * u * (p1[0] - p0[0]) + 6 * u * t * (p2[0] - p1[0]) + 3 * t * t * (p3[0] - p2[0]),
            3 * u * u * (p1[1] - p0[1]) + 6 * u * t * (p2[1] - p1[1]) + 3 * t * t * (p3[1] - p2[1]))


def qb(p0, p1, p2, t):
    u = 1 - t
    return (u * u * p0[0] + 2 * u * t * p1[0] + t * t * p2[0],
            u * u * p0[1] + 2 * u * t * p1[1] + t * t * p2[1])


def qbd(p0, p1, p2, t):
    return (2 * (1 - t) * (p1[0] - p0[0]) + 2 * t * (p2[0] - p1[0]),
            2 * (1 - t) * (p1[1] - p0[1]) + 2 * t * (p2[1] - p1[1]))


def write(name, w, h, body, bg=None):
    bgs = ""
    if bg:
        bgs = f'<rect width="{w}" height="{h}" fill="{bg}"/>'
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">'
           f'{DEFS}{bgs}{body}</svg>')
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(svg)


def sparkle(x, y, r, fill="url(#gGold)", op=1.0, rot=0):
    d = (f"M{x},{y - r} Q{x},{y} {x + r},{y} Q{x},{y} {x},{y + r} "
         f"Q{x},{y} {x - r},{y} Q{x},{y} {x},{y - r}Z")
    return f'<path d="{d}" fill="{fill}" opacity="{op}" transform="rotate({rot} {x} {y})"/>'


def droplet(x, y, r, fill="url(#gPink)", op=1.0):
    d = (f"M{x},{y - r} C{x + r * .7},{y - r * .2} {x + r * .95},{y + r * .35} {x},{y + r} "
         f"C{x - r * .95},{y + r * .35} {x - r * .7},{y - r * .2} {x},{y - r}Z")
    hl = (f'<path d="M{x - r * .35},{y + r * .1} Q{x - r * .4},{y + r * .5} {x - r * .1},{y + r * .65}" '
          f'stroke="#fff" stroke-width="{max(1.5, r * .12):.1f}" stroke-linecap="round" fill="none" opacity=".8"/>')
    return f'<path d="{d}" fill="{fill}" opacity="{op}"/>{hl}'


def leaf(x, y, length, rot, fill="url(#gOlive)", op=1.0):
    w = length * 0.34
    d = f"M0,0 C{length * .25},-{w} {length * .75},-{w} {length},0 C{length * .75},{w} {length * .25},{w} 0,0Z"
    vein = f'<path d="M2,0 L{length * .9},0" stroke="#fff" stroke-opacity=".45" stroke-width="1.4" fill="none"/>'
    return f'<g transform="translate({x},{y}) rotate({rot})" opacity="{op}"><path d="{d}" fill="{fill}"/>{vein}</g>'


def bokeh(w, h, seed, n=7, cols=("#fff", "#F4D3DA", "#DCE3C3", "#F6E6BC")):
    rnd = random.Random(seed)
    s = ""
    for _ in range(n):
        s += (f'<circle cx="{rnd.uniform(0, w):.0f}" cy="{rnd.uniform(0, h):.0f}" r="{rnd.uniform(24, 70):.0f}" '
              f'fill="{rnd.choice(cols)}" opacity="{rnd.uniform(.3, .6):.2f}" filter="url(#fBlur)"/>')
    return s


def shadow(x, y, rx, ry=9, op=.28):
    return f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="#2F3523" opacity="{op}" filter="url(#fBlur6)"/>'


# ------------------------------------------------------------ brow + eye
def brow(x0, y0, cx, cy, x1, y1, thick=50, n=320, seed=1, lift=False, tint="#5b4030"):
    rnd = random.Random(seed)
    p0, p1, p2 = (x0, y0), (cx, cy), (x1, y1)

    def prof(t):
        return thick * (1 - t**2.2) * (0.62 + 0.38 * min(1, t * 4))

    top, bot = [], []
    N = 28
    for i in range(N + 1):
        t = i / N
        x, y = qb(p0, p1, p2, t)
        dx, dy = qbd(p0, p1, p2, t)
        m = math.hypot(dx, dy) or 1
        nx, ny = dy / m, -dx / m
        h = prof(t) / 2
        top.append((x + nx * h, y + ny * h))
        bot.append((x - nx * h, y - ny * h))
    body = "M" + " L".join(P(*q) for q in top + bot[::-1]) + "Z"
    s = f'<path d="{body}" fill="{tint}" opacity=".32" filter="url(#fBlur6)"/>'
    hairs = []
    for _ in range(n):
        t = rnd.random() ** 1.05
        x, y = qb(p0, p1, p2, t)
        dx, dy = qbd(p0, p1, p2, t)
        m = math.hypot(dx, dy) or 1
        nx, ny = dy / m, -dx / m
        h = prof(t) / 2
        off = rnd.uniform(-1, 1)
        hx, hy = x + nx * h * off, y + ny * h * off
        tang = math.atan2(dy, dx)
        if lift:
            ang = math.radians(-86 + t * 32 + rnd.uniform(-9, 9))
        else:
            k = min(1, (t / 0.55) ** 0.7)
            ang = tang + math.radians(-52 * (1 - k) + 6 * k + rnd.uniform(-7, 7))
        ln = thick * rnd.uniform(0.36, 0.62) * (1.0 - 0.35 * t)
        ex, ey = hx + math.cos(ang) * ln, hy + math.sin(ang) * ln
        bend = rnd.uniform(-0.18, 0.18) * ln
        mx, my = (hx + ex) / 2 - math.sin(ang) * bend, (hy + ey) / 2 + math.cos(ang) * bend
        w = rnd.uniform(1.3, 2.3)
        hairs.append(f'<path d="M{P(hx, hy)} Q{P(mx, my)} {P(ex, ey)}" stroke="{rnd.choice(HAIR)}" '
                     f'stroke-width="{w:.1f}" opacity="{rnd.uniform(.55, .95):.2f}"/>')
    s += '<g fill="none" stroke-linecap="round">' + "".join(hairs) + "</g>"
    return s


def eye(cx, cy, w=300, h=100, uid="e", lash_n=30, lash_len=40, sweep=38, lift=0, seed=3,
        thick=3.2, layers=1, shadow_tint="#E3A6B5"):
    L = (cx - w / 2, cy + h * 0.08)
    R = (cx + w / 2, cy - h * 0.06)
    c1 = (cx - w * 0.2, cy - h * 1.05)
    c2 = (cx + w * 0.18, cy - h * 1.1)
    d1 = (cx + w * 0.22, cy + h * 0.75)
    d2 = (cx - w * 0.22, cy + h * 0.78)
    path = f"M{P(*L)} C{P(*c1)} {P(*c2)} {P(*R)} C{P(*d1)} {P(*d2)} {P(*L)}Z"
    upper = f"M{P(*L)} C{P(*c1)} {P(*c2)} {P(*R)}"
    ir = h * 0.66
    ix, iy = cx + w * 0.03, cy - h * 0.14
    s = f'<clipPath id="{uid}c"><path d="{path}"/></clipPath>'
    # soft lid colour above the lash line
    s += (f'<ellipse cx="{cx}" cy="{cy - h * 0.95}" rx="{w * .58}" ry="{h * .62}" fill="{shadow_tint}" '
          f'opacity=".34" filter="url(#fBlur)"/>')
    s += f'<path d="{path}" fill="url(#gSclera)"/>'
    g = f'<g clip-path="url(#{uid}c)">'
    g += f'<circle cx="{ix}" cy="{iy}" r="{ir}" fill="url(#gIris)"/>'
    rnd = random.Random(seed + 40)
    for i in range(36):
        a = i / 36 * math.tau
        r0, r1 = ir * 0.42, ir * rnd.uniform(.72, .95)
        g += (f'<path d="M{P(ix + math.cos(a) * r0, iy + math.sin(a) * r0)} L{P(ix + math.cos(a) * r1, iy + math.sin(a) * r1)}" '
              f'stroke="#f2c892" stroke-opacity="{rnd.uniform(.12, .32):.2f}" stroke-width="1.3"/>')
    g += f'<circle cx="{ix}" cy="{iy}" r="{ir * 0.4}" fill="#150b06"/>'
    g += f'<circle cx="{ix}" cy="{iy}" r="{ir}" fill="none" stroke="#1d0f08" stroke-opacity=".55" stroke-width="{ir * .09:.1f}"/>'
    g += f'<circle cx="{ix - ir * .34}" cy="{iy - ir * .38}" r="{ir * .2}" fill="#fff" opacity=".92"/>'
    g += f'<circle cx="{ix + ir * .3}" cy="{iy + ir * .32}" r="{ir * .08}" fill="#fff" opacity=".6"/>'
    g += f'<rect x="{cx - w / 2}" y="{cy - h * 1.1}" width="{w}" height="{h * 1.0}" fill="url(#gLid)"/>'
    g += f'<ellipse cx="{L[0] + 12}" cy="{L[1] - 2}" rx="13" ry="9" fill="#E08E86" opacity=".7"/>'
    g += "</g>"
    s += g
    # lower lid + crease + lash line
    s += (f'<path d="M{P(*R)} C{P(*d1)} {P(*d2)} {P(*L)}" stroke="#b9806c" stroke-opacity=".7" '
          f'stroke-width="2" fill="none" stroke-linecap="round"/>')
    cr = (f"M{P(L[0] + w * .05, L[1] - h * .5)} C{P(c1[0] + w * .02, c1[1] - h * .5)} "
          f"{P(c2[0], c2[1] - h * .48)} {P(R[0] - w * .03, R[1] - h * .42)}")
    s += f'<path d="{cr}" stroke="#b27663" stroke-opacity=".55" stroke-width="2.6" fill="none" stroke-linecap="round"/>'
    s += (f'<path d="{upper}" stroke="#241410" stroke-width="{thick + 1.6}" fill="none" '
          f'stroke-linecap="round"/>')
    # lashes
    rnd = random.Random(seed)
    out = []
    for layer in range(layers):
        for i in range(lash_n):
            t = 0.05 + 0.93 * (i + rnd.uniform(-.3, .3)) / (lash_n - 1)
            t = min(max(t, 0.02), 0.99)
            px, py = bez(L, c1, c2, R, t)
            dx, dy = bezd(L, c1, c2, R, t)
            m = math.hypot(dx, dy) or 1
            tx, ty = dx / m, dy / m
            nx, ny = ty, -tx
            ang = math.atan2(ny, nx) + math.radians(sweep * t**1.2 - lift * (0.4 + t) - 14 * (1 - t)
                                                    + rnd.uniform(-3, 3) + layer * 4)
            ln = lash_len * (0.42 + 0.78 * t**1.1) * (0.82 + 0.36 * rnd.random()) * (1 - 0.18 * layer)
            cxp, cyp = px + math.cos(ang) * ln * 0.58, py + math.sin(ang) * ln * 0.58
            tip_a = ang - math.radians(22 + lift * 0.4)
            tx_, ty_ = px + math.cos(tip_a) * ln, py + math.sin(tip_a) * ln
            bx, by = -math.sin(ang) * thick * .5, math.cos(ang) * thick * .5
            out.append(f'<path d="M{P(px - bx, py - by)} Q{P(cxp - bx * .5, cyp - by * .5)} {P(tx_, ty_)} '
                       f'Q{P(cxp + bx * .5, cyp + by * .5)} {P(px + bx, py + by)}Z"/>')
    s += '<g fill="#1e120c" opacity=".93">' + "".join(out) + "</g>"
    return s


# ---------------------------------------------------------------- objects
def spoolie(x, y, rot=0, s=1, seed=4):
    rnd = random.Random(seed)
    br = ""
    for i in range(3, 88, 3):
        a = rnd.uniform(-2, 2)
        br += (f'<path d="M{i},-8 l{a:.1f},-{rnd.uniform(7, 11):.1f} M{i},8 l{a:.1f},{rnd.uniform(7, 11):.1f}"/>')
    return (f'<g transform="translate({x},{y}) rotate({rot}) scale({s})">'
            '<path d="M-176,-5 Q-176,-8 -170,-8 L-26,-7 L-26,7 L-170,8 Q-176,8 -176,5Z" fill="url(#gHandle)"/>'
            '<path d="M-170,-4.5 L-32,-4.5" stroke="#fff" stroke-opacity=".55" stroke-width="2" stroke-linecap="round"/>'
            '<rect x="-26" y="-8.5" width="30" height="17" rx="3" fill="url(#gMetalV)"/>'
            '<rect x="0" y="-8" width="90" height="16" rx="8" fill="#3a2b22"/>'
            f'<g stroke="#2b1d16" stroke-width="1.7" stroke-linecap="round">{br}</g></g>')


def tweezers(x, y, rot=0, s=1):
    return (f'<g transform="translate({x},{y}) rotate({rot}) scale({s})">'
            '<path d="M0,-6 C40,-18 110,-16 168,-3 L173,1 L166,3 C108,-9 40,-9 0,-1Z" fill="url(#gMetalV)"/>'
            '<path d="M0,6 C40,18 110,16 168,3 L173,-1 L166,-3 C108,9 40,9 0,1Z" fill="url(#gMetalV)"/>'
            '<path d="M6,-6 C42,-15 108,-13 158,-4" stroke="#fff" stroke-opacity=".75" stroke-width="1.6" fill="none" stroke-linecap="round"/>'
            '<rect x="-16" y="-7.5" width="20" height="15" rx="5" fill="url(#gGold)"/></g>')


def pen(x, y, rot=0, s=1):
    return (f'<g transform="translate({x},{y}) rotate({rot}) scale({s})">'
            '<rect x="-72" y="-10" width="84" height="20" rx="10" fill="url(#gOliveV)"/>'
            '<rect x="14" y="-9" width="152" height="18" rx="4" fill="url(#gCreamV)"/>'
            '<rect x="104" y="-9.5" width="11" height="19" fill="url(#gGold)"/>'
            '<path d="M166,-9 L208,-2.6 Q212,0 208,2.6 L166,9Z" fill="url(#gBrown)"/>'
            '<path d="M22,-5.5 L158,-5.5" stroke="#fff" stroke-opacity=".85" stroke-width="2" stroke-linecap="round"/>'
            f'<text x="60" y="4" text-anchor="middle" font-family="{SERIF}" font-style="italic" font-size="10" fill="#5A6B33">LJ Brows</text></g>')


def bottle(x, y, s=1, liquid="#8C9A5B", glass="#E4EACB"):
    return (f'<g transform="translate({x},{y}) scale({s})">'
            f'{shadow(0, 2, 42, 7)}'
            '<rect x="-12" y="-100" width="24" height="28" rx="5" fill="url(#gGold)"/>'
            '<rect x="-9" y="-134" width="18" height="40" rx="9" fill="#2F3523"/>'
            f'<rect x="-28" y="-78" width="56" height="78" rx="14" fill="{glass}" fill-opacity=".6" stroke="#fff" stroke-opacity=".9" stroke-width="1.5"/>'
            f'<rect x="-24" y="-42" width="48" height="38" rx="10" fill="{liquid}" opacity=".85"/>'
            '<rect x="-20" y="-62" width="40" height="40" rx="6" fill="#fff" opacity=".93"/>'
            f'<text x="0" y="-36" text-anchor="middle" font-family="{SERIF}" font-style="italic" font-size="14" fill="#5A6B33">LJ</text>'
            '<path d="M-22,-72 Q-25,-40 -22,-12" stroke="#fff" stroke-width="3" stroke-linecap="round" opacity=".75" fill="none"/></g>')


def tube(x, y, s=1):
    return (f'<g transform="translate({x},{y}) scale({s})">{shadow(0, 2, 36, 7)}'
            '<rect x="-24" y="-112" width="48" height="112" rx="12" fill="url(#gBrown)"/>'
            '<rect x="-26" y="-134" width="52" height="30" rx="8" fill="url(#gGold)"/>'
            '<rect x="-24" y="-80" width="48" height="40" fill="#FBF8F2"/>'
            f'<text x="0" y="-60" text-anchor="middle" font-family="{SERIF}" font-style="italic" font-size="13" fill="#2F3523">Brow</text>'
            f'<text x="0" y="-46" text-anchor="middle" font-family="{SERIF}" font-size="8.5" letter-spacing="1.5" fill="#5A6B33">GEL</text>'
            '<path d="M-17,-100 Q-19,-60 -17,-14" stroke="#fff" stroke-width="3" stroke-linecap="round" opacity=".35" fill="none"/></g>')


def jar(x, y, s=1, label="WAX"):
    return (f'<g transform="translate({x},{y}) scale({s})">{shadow(0, 4, 62, 9)}'
            '<path d="M-50,-58 L50,-58 L52,-6 Q52,8 38,8 L-38,8 Q-52,8 -52,-6Z" fill="url(#gHoney)"/>'
            '<path d="M-42,-52 Q-46,-20 -42,0" stroke="#fff" stroke-opacity=".6" stroke-width="4" stroke-linecap="round" fill="none"/>'
            '<rect x="-56" y="-84" width="112" height="30" rx="8" fill="url(#gGold)"/>'
            '<rect x="-32" y="-46" width="64" height="30" rx="5" fill="#FBF8F2" opacity=".95"/>'
            f'<text x="0" y="-26" text-anchor="middle" font-family="{SERIF}" font-style="italic" font-size="14" fill="#5A6B33">{label}</text></g>')


def spool(x, y, s=1, thread="#E3A6B5"):
    lines = "".join(f'<path d="M-30,{yy} Q0,{yy + 5} 30,{yy}" stroke="#fff" stroke-opacity=".3" stroke-width="1.4" fill="none"/>'
                    for yy in range(-30, 32, 6))
    return (f'<g transform="translate({x},{y}) scale({s})">{shadow(0, 46, 40, 7)}'
            '<ellipse cx="0" cy="42" rx="38" ry="9" fill="url(#gGold)"/>'
            f'<rect x="-32" y="-38" width="64" height="80" fill="{thread}"/>{lines}'
            '<ellipse cx="0" cy="-38" rx="32" ry="8" fill="#f6c9d3"/>'
            '<ellipse cx="0" cy="-48" rx="38" ry="9" fill="url(#gGold)"/>'
            '<ellipse cx="0" cy="-52" rx="38" ry="9" fill="#F6E6BC"/>'
            f'<path d="M20,-40 C60,-20 70,20 40,44" stroke="{thread}" stroke-width="3" fill="none" stroke-linecap="round"/></g>')


def logo_mark(x, y, s=1):
    """Brow arch + eye + lashes monogram on an olive disc (64x64 design space)."""
    return (f'<g transform="translate({x},{y}) scale({s})">'
            '<circle cx="32" cy="32" r="30" fill="url(#gOlive)"/>'
            '<circle cx="32" cy="32" r="27" fill="none" stroke="url(#gGold)" stroke-width="1.6"/>'
            '<path d="M13,26 Q30,12 51,23 Q31,18 13,26Z" fill="#FBF8F2"/>'
            '<path d="M15,38 Q32,27 49,38 Q32,48 15,38Z" fill="none" stroke="#FBF8F2" stroke-width="2.3" stroke-linejoin="round"/>'
            '<circle cx="32" cy="37.5" r="4.4" fill="url(#gGold)"/>'
            '<g stroke="#FBF8F2" stroke-width="1.8" stroke-linecap="round" fill="none">'
            '<path d="M21,34 Q18,31 17,28"/><path d="M26,31.2 Q24,27 23.5,24"/><path d="M32,29.8 L32,25.5"/>'
            '<path d="M38,31.2 Q40,27 40.5,24"/><path d="M43,34 Q46,31 47,28"/></g></g>')


# -------------------------------------------------------------- scene bits
def hero_inner():
    """Brow + eye composition in a 600x600 space (reused in the hero and the About mirror)."""
    s = f'<ellipse cx="300" cy="300" rx="190" ry="60" fill="#E3A6B5" opacity=".34" filter="url(#fBlur)"/>'
    s += f'<ellipse cx="320" cy="262" rx="150" ry="22" fill="#fff" opacity=".28" filter="url(#fBlur6)"/>'
    s += brow(88, 214, 270, 90, 512, 204, thick=60, n=460, seed=11)
    s += eye(300, 380, w=390, h=130, uid="hi", lash_n=40, lash_len=58, sweep=40, seed=5, layers=2)
    return s


def disc(cx, cy, r):
    return (f'{shadow(cx, cy + r + 8, r * .62, 12, .3)}'
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#gDisc)"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r + 14}" fill="none" stroke="#B8975A" stroke-opacity=".7" stroke-width="2" stroke-dasharray="3 9" stroke-linecap="round"/>'
            f'<ellipse cx="{cx - r * .34}" cy="{cy - r * .5}" rx="{r * .42}" ry="{r * .2}" fill="#fff" opacity=".6" filter="url(#fBlur6)" transform="rotate(-28 {cx - r * .34} {cy - r * .5})"/>')


# ================================================================== SCENES
def scene_hero():
    b = f'<rect width="600" height="600" fill="url(#gSkin)"/>'
    b += '<ellipse cx="190" cy="140" rx="250" ry="150" fill="#fff" opacity=".4" filter="url(#fBlur)"/>'
    b += '<ellipse cx="500" cy="540" rx="220" ry="120" fill="#E3A6B5" opacity=".4" filter="url(#fBlur)"/>'
    b += hero_inner()
    b += sparkle(105, 118, 26) + sparkle(505, 100, 18, op=.9) + sparkle(520, 470, 22) + sparkle(78, 480, 14, op=.85)
    write("hero-eye.svg", 600, 600, b)


def treat_bg(seed, skin=True):
    b = f'<rect width="480" height="300" fill="url(#gSkin)"/>' if skin else '<rect width="480" height="300" fill="url(#gBg)"/>'
    b += bokeh(480, 300, seed, 6)
    return b


def scene_brow_lamination():
    b = treat_bg(21)
    b += brow(52, 205, 230, 78, 432, 172, thick=64, n=420, seed=21, lift=True)
    b += spoolie(330, 214, -150, 1.05, seed=6)
    for (x, y) in ((120, 90), (230, 52), (340, 76)):
        b += (f'<path d="M{x - 8},{y + 8} L{x},{y - 4} L{x + 8},{y + 8}" stroke="#B8975A" stroke-width="3" '
              f'fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
    b += sparkle(420, 62, 20) + sparkle(60, 80, 13, op=.9)
    write("treat-brow-lamination.svg", 480, 300, b)


def scene_eyelash_lift():
    b = treat_bg(33)
    b += brow(78, 96, 240, 30, 402, 84, thick=40, n=240, seed=33)
    b += eye(240, 214, w=290, h=90, uid="lf", lash_n=34, lash_len=44, sweep=30, lift=24, seed=9, layers=1)
    b += sparkle(432, 190, 18) + sparkle(54, 230, 12, op=.9)
    write("treat-eyelash-lift.svg", 480, 300, b)


def scene_lash_ext():
    b = treat_bg(45)
    b += eye(215, 205, w=310, h=96, uid="lx", lash_n=46, lash_len=70, sweep=44, seed=8, layers=3, thick=3.8)
    b += shadow(330, 150, 70, 8, .2)
    b += tweezers(446, 40, 150, 1.0)
    b += sparkle(60, 70, 18) + sparkle(430, 250, 14, op=.9)
    write("treat-lash-extensions.svg", 480, 300, b)


def scene_facial():
    b = '<rect width="480" height="300" fill="url(#gBg)"/>' + bokeh(480, 300, 57, 6)
    b += leaf(60, 250, 90, -35) + leaf(48, 270, 70, -60, op=.9) + leaf(420, 252, 90, 215) + leaf(432, 272, 66, 240, op=.9)
    b += shadow(240, 280, 80, 9)
    b += '<ellipse cx="240" cy="156" rx="86" ry="114" fill="url(#gSkin)"/>'
    b += '<ellipse cx="240" cy="156" rx="86" ry="114" fill="none" stroke="#fff" stroke-opacity=".6" stroke-width="2"/>'
    b += '<path d="M150,132 C146,30 334,30 330,132 C300,98 180,98 150,132Z" fill="url(#gOlive)"/>'
    b += '<path d="M168,110 Q240,70 312,110" stroke="#fff" stroke-opacity=".5" stroke-width="3" fill="none" stroke-linecap="round"/>'
    b += '<circle cx="240" cy="62" r="7" fill="url(#gGold)"/>'
    b += '<ellipse cx="190" cy="190" rx="22" ry="13" fill="#E3A6B5" opacity=".55" filter="url(#fBlur6)"/>'
    b += '<ellipse cx="290" cy="190" rx="22" ry="13" fill="#E3A6B5" opacity=".55" filter="url(#fBlur6)"/>'
    for sx in (-1, 1):
        ex = 240 + sx * 38
        b += f'<path d="M{ex - 18},150 Q{ex},164 {ex + 18},150" stroke="#2f1e15" stroke-width="3.4" fill="none" stroke-linecap="round"/>'
        for k in range(-2, 3):
            b += f'<path d="M{ex + k * 6.5},{153 + (2 - abs(k)) * .5} l{k * 1.6},6" stroke="#2f1e15" stroke-width="1.8" stroke-linecap="round"/>'
        b += f'<path d="M{ex - 20},131 Q{ex},121 {ex + 20},131" stroke="#5b4030" stroke-width="4.5" fill="none" stroke-linecap="round"/>'
    b += '<path d="M240,160 Q236,182 244,186" stroke="#c98d79" stroke-width="2.4" fill="none" stroke-linecap="round"/>'
    b += '<path d="M224,208 Q240,220 256,208 Q240,214 224,208Z" fill="#d88a9b" stroke="#d88a9b" stroke-width="3" stroke-linejoin="round"/>'
    b += droplet(120, 90, 15) + droplet(366, 72, 12) + droplet(396, 168, 9, op=.9) + droplet(92, 170, 10, op=.9)
    b += sparkle(420, 40, 18) + sparkle(64, 38, 12)
    write("treat-facial.svg", 480, 300, b)


# ---- shop products (320x200)
def prod_bg(seed):
    return '<rect width="320" height="200" fill="url(#gCreamBg)"/>' + bokeh(320, 200, seed, 5)


def scene_prod_kit():
    b = prod_bg(61) + shadow(150, 172, 112, 10)
    b += '<rect x="64" y="72" width="152" height="98" rx="12" fill="url(#gCreamV)" stroke="#e1d8c3"/>'
    b += '<rect x="64" y="72" width="152" height="24" rx="12" fill="url(#gOlive)"/>'
    b += '<rect x="132" y="72" width="16" height="98" fill="url(#gGold)" opacity=".9"/>'
    b += f'<text x="98" y="140" text-anchor="middle" font-family="{SERIF}" font-style="italic" font-size="15" fill="#5A6B33">LJ Brows</text>'
    b += f'<text x="98" y="156" text-anchor="middle" font-family="{SERIF}" font-size="7.5" letter-spacing="1.8" fill="#8C9A5B">AFTERCARE</text>'
    b += bottle(250, 172, .78)
    b += spoolie(110, 182, -12, .5, seed=8)
    b += sparkle(292, 40, 14) + sparkle(36, 60, 10, op=.9)
    write("prod-kit.svg", 320, 200, b)


def scene_prod_pen():
    b = prod_bg(63) + shadow(165, 168, 110, 8)
    b += pen(78, 112, -24, 1.0)
    for i, (dx, dy, ln) in enumerate(((0, 0, 30), (6, 3, 27), (12, 6, 24), (18, 9, 22))):
        b += (f'<path d="M{250 + dx},{170 + dy} l{ln * .8:.0f},-{ln * .45:.0f}" stroke="{HAIR[i]}" '
              f'stroke-width="2.2" stroke-linecap="round" opacity=".9"/>')
    b += sparkle(272, 46, 14) + sparkle(46, 164, 9, op=.9)
    write("prod-pen.svg", 320, 200, b)


def scene_prod_tweezers():
    b = prod_bg(65) + shadow(165, 150, 112, 8, .22)
    b += tweezers(48, 142, -20, 1.45)
    for i in range(5):
        b += (f'<path d="M{262 + i * 5},{58 + i * 2} q4,-14 14,-18" stroke="{HAIR[i % 5]}" stroke-width="2.2" fill="none" stroke-linecap="round"/>')
    b += sparkle(270, 150, 13) + sparkle(46, 52, 10, op=.9)
    write("prod-tweezers.svg", 320, 200, b)


def scene_prod_gel():
    b = prod_bg(67) + shadow(170, 176, 80, 8)
    b += tube(176, 176, 1.0)
    b += spoolie(60, 182, -14, .55, seed=10)
    for i in range(4):
        b += (f'<path d="M{250 + i * 7},{108 + i * 3} q3,-16 14,-22" stroke="{HAIR[i]}" stroke-width="2.4" fill="none" stroke-linecap="round" opacity=".9"/>')
    b += sparkle(268, 42, 13) + sparkle(40, 56, 10, op=.9)
    write("prod-gel.svg", 320, 200, b)


# ---- page heroes (400x400)
def ph_about():
    b = disc(200, 200, 168)
    b += leaf(70, 322, 90, -52) + leaf(84, 338, 70, -78, op=.9) + leaf(332, 322, 90, 232) + leaf(318, 338, 70, 258, op=.9)
    b += '<rect x="184" y="296" width="32" height="82" rx="16" fill="url(#gGold)"/>'
    b += '<circle cx="200" cy="378" r="7" fill="#FBF8F2" opacity=".8"/>'
    b += '<ellipse cx="200" cy="176" rx="96" ry="124" fill="url(#gGold)"/>'
    b += '<clipPath id="mir"><ellipse cx="200" cy="176" rx="82" ry="110"/></clipPath>'
    b += ('<g clip-path="url(#mir)"><rect x="100" y="50" width="200" height="250" fill="url(#gSkin)"/>'
          '<g transform="translate(200,172) scale(.44) translate(-300,-330)">' + hero_inner() + '</g>'
          '<path d="M122,98 Q150,60 196,52" stroke="#fff" stroke-opacity=".75" stroke-width="7" fill="none" stroke-linecap="round"/></g>')
    b += '<ellipse cx="200" cy="176" rx="82" ry="110" fill="none" stroke="#fff" stroke-opacity=".6" stroke-width="2"/>'
    b += sparkle(330, 70, 20) + sparkle(64, 110, 13)
    write("ph-about.svg", 400, 400, b)


def ph_services():
    b = disc(200, 200, 168)
    b += spool(300, 150, .9)
    b += jar(120, 290, 1.0)
    b += spoolie(215, 178, -38, .8, seed=3)
    b += tweezers(150, 340, -18, 1.1)
    b += sparkle(330, 300, 16) + sparkle(70, 100, 12)
    write("ph-services.svg", 400, 400, b)


def ph_shop():
    b = disc(200, 200, 168)
    b += bottle(292, 270, 1.05) + tube(112, 262, .9)
    b += shadow(200, 352, 96, 11)
    b += '<path d="M150,168 C150,100 250,100 250,168" stroke="url(#gGold)" stroke-width="9" fill="none" stroke-linecap="round"/>'
    b += '<path d="M104,168 L296,168 L314,342 Q314,352 304,352 L96,352 Q86,352 86,342Z" fill="url(#gPink)"/>'
    b += '<path d="M104,168 L296,168 L300,200 L100,200Z" fill="#fff" opacity=".35"/>'
    b += logo_mark(168, 224, 1.0)
    b += f'<text x="200" y="326" text-anchor="middle" font-family="{SERIF}" font-style="italic" font-size="17" fill="#5A6B33">LJ Brows Studio</text>'
    b += sparkle(338, 98, 18) + sparkle(62, 128, 12)
    write("ph-shop.svg", 400, 400, b)


def ph_gift():
    b = disc(200, 200, 168) + shadow(200, 346, 104, 11)
    b += '<rect x="112" y="214" width="176" height="128" rx="10" fill="url(#gOlive)"/>'
    b += '<rect x="100" y="172" width="200" height="52" rx="10" fill="url(#gOlive)"/>'
    b += '<rect x="100" y="172" width="200" height="14" rx="7" fill="#fff" opacity=".25"/>'
    b += '<rect x="186" y="172" width="28" height="170" fill="url(#gPink)"/>'
    b += '<path d="M200,174 C168,98 100,126 148,170 C164,182 184,178 200,174Z" fill="url(#gPink)" stroke="#d68ea1" stroke-width="2"/>'
    b += '<path d="M200,174 C232,98 300,126 252,170 C236,182 216,178 200,174Z" fill="url(#gPink)" stroke="#d68ea1" stroke-width="2"/>'
    b += '<path d="M196,180 L168,226 L186,222Z M204,180 L232,226 L214,222Z" fill="#E3A6B5"/>'
    b += '<ellipse cx="200" cy="176" rx="15" ry="13" fill="url(#gPink)" stroke="#d68ea1" stroke-width="2"/>'
    b += sparkle(322, 100, 22) + sparkle(76, 138, 14) + sparkle(306, 308, 12, op=.9)
    write("ph-gift.svg", 400, 400, b)


def ph_contact():
    b = disc(200, 200, 168) + shadow(200, 340, 100, 10)
    b += '<rect x="122" y="108" width="156" height="120" rx="8" fill="#fff"/>'
    b += '<path d="M146,138 H254 M146,160 H254 M146,182 H214" stroke="#DCE3C3" stroke-width="6" stroke-linecap="round"/>'
    b += '<rect x="86" y="170" width="228" height="162" rx="16" fill="url(#gCreamV)" stroke="#e1d8c3"/>'
    b += '<path d="M86,186 L200,268 L314,186 L314,174 Q314,170 308,170 L92,170 Q86,170 86,176Z" fill="url(#gPinkV)"/>'
    b += '<path d="M90,326 L176,246 M310,326 L224,246" stroke="#e1d8c3" stroke-width="2.4" fill="none"/>'
    b += '<circle cx="200" cy="262" r="19" fill="url(#gGold)"/>'
    b += '<path d="M200,272 C186,262 186,252 194,252 C198,252 200,255 200,257 C200,255 202,252 206,252 C214,252 214,262 200,272Z" fill="#FBF8F2"/>'
    b += sparkle(328, 112, 20) + sparkle(70, 150, 13)
    write("ph-contact.svg", 400, 400, b)


def pin(fill, hole_fill="#FBF8F2"):
    return (f'<path d="M200,338 C150,266 112,226 112,170 A88,88 0 0 1 288,170 C288,226 250,266 200,338Z" fill="{fill}"/>'
            '<path d="M130,150 A70,70 0 0 1 190,96" stroke="#fff" stroke-opacity=".55" stroke-width="8" fill="none" stroke-linecap="round"/>'
            f'<circle cx="200" cy="170" r="40" fill="{hole_fill}"/>')


def ph_brisbane():
    b = disc(200, 200, 168) + shadow(200, 346, 70, 9)
    b += '<circle cx="312" cy="96" r="30" fill="url(#gGold)"/><circle cx="312" cy="96" r="42" fill="none" stroke="#B8975A" stroke-opacity=".5" stroke-dasharray="2 8" stroke-linecap="round"/>'
    for a in (-140, -110, -80, -50, -20):
        b += leaf(92, 342, 86, a, op=.95)
    b += pin("url(#gOlive)")
    b += sparkle(200, 170, 22) + sparkle(76, 120, 12)
    write("ph-brisbane.svg", 400, 400, b)


def ph_adelaide():
    b = disc(200, 200, 168) + shadow(200, 346, 70, 9)
    b += '<clipPath id="hc"><circle cx="200" cy="200" r="168"/></clipPath><g clip-path="url(#hc)">'
    b += '<path d="M20,310 Q110,230 190,300 Q270,232 380,306 L380,380 L20,380Z" fill="url(#gOlive)" opacity=".55"/>'
    b += '<path d="M20,334 Q120,276 200,328 Q280,278 380,330 L380,380 L20,380Z" fill="url(#gOlive)" opacity=".8"/></g>'
    b += pin("url(#gPink)")
    b += sparkle(200, 170, 22) + sparkle(318, 92, 20) + sparkle(76, 120, 12) + sparkle(332, 250, 11, op=.9)
    write("ph-adelaide.svg", 400, 400, b)


# ---- services thumbs (240x240)
def thumb_bg(seed):
    return '<rect width="240" height="240" fill="url(#gBg2)"/>' + bokeh(240, 240, seed, 4)


def thumb_waxing():
    b = thumb_bg(71) + jar(110, 172, 1.25)
    b += '<g transform="translate(170,70) rotate(24)"><rect x="-6" y="0" width="12" height="104" rx="5" fill="#E7C98E"/><rect x="-6" y="0" width="12" height="10" rx="5" fill="#C9A15C"/></g>'
    b += droplet(52, 62, 12, "url(#gHoney)") + sparkle(196, 38, 14) + sparkle(36, 150, 9, op=.9)
    write("thumb-waxing.svg", 240, 240, b)


def thumb_threading():
    b = thumb_bg(73) + spool(120, 130, 1.45)
    b += '<path d="M40,196 C80,150 120,230 210,176" stroke="#E3A6B5" stroke-width="3" fill="none" stroke-linecap="round"/>'
    b += '<path d="M40,206 C80,160 120,240 210,186" stroke="#B8975A" stroke-width="2" fill="none" stroke-linecap="round" opacity=".8"/>'
    b += sparkle(196, 42, 14) + sparkle(40, 60, 10, op=.9)
    write("thumb-threading.svg", 240, 240, b)


def thumb_combos():
    b = '<rect width="240" height="240" fill="url(#gSkin)"/>' + bokeh(240, 240, 75, 4)
    b += brow(30, 96, 110, 38, 210, 84, thick=34, n=200, seed=75)
    b += eye(120, 160, w=170, h=58, uid="cb", lash_n=24, lash_len=28, sweep=36, seed=12, layers=1, thick=2.6)
    b += sparkle(208, 40, 13) + sparkle(30, 206, 10, op=.9)
    write("thumb-combos.svg", 240, 240, b)


# ---- decor
def gift_pattern():
    b = ('<g fill="none" stroke="#fff" stroke-opacity=".28" stroke-width="2.2" stroke-linecap="round">'
         '<circle cx="410" cy="60" r="80"/><circle cx="410" cy="60" r="120" stroke-dasharray="3 10"/>'
         '<circle cx="410" cy="60" r="170" stroke-opacity=".16"/>'
         '<path d="M250,252 Q350,180 460,236"/><path d="M262,268 Q360,208 470,258" stroke-opacity=".18"/></g>')
    b += sparkle(330, 66, 16, "#fff", .55) + sparkle(448, 150, 11, "#fff", .45) + sparkle(36, 262, 10, "#fff", .4)
    b += '<g opacity=".3" transform="translate(226,114) scale(.42)">' + eye(150, 100, w=300, h=96, uid="gp", lash_n=22, lash_len=36, sweep=34, seed=2, thick=3) + '</g>'
    write("gift-pattern.svg", 480, 300, b)


def footer_art():
    b = '<g transform="translate(40,40)" opacity=".26">' + eye(180, 140, w=300, h=96, uid="fa", lash_n=28, lash_len=44, sweep=36, seed=4, shadow_tint="#8C9A5B") + "</g>"
    b += leaf(30, 250, 120, -40, "#5A6B33", .35) + leaf(48, 262, 90, -70, "#5A6B33", .3)
    b += sparkle(360, 56, 22, "#B8975A", .6) + sparkle(396, 140, 12, "#B8975A", .5)
    write("footer-art.svg", 420, 290, b)


def logo_files():
    write("logo-mark.svg", 64, 64, logo_mark(0, 0, 1))


def og_cover():
    b = '<rect width="1200" height="630" fill="url(#gBg)"/>' + bokeh(1200, 630, 99, 9)
    b += '<g transform="translate(640,40) scale(.9)"><clipPath id="oc"><circle cx="300" cy="300" r="290"/></clipPath><g clip-path="url(#oc)"><rect width="600" height="600" fill="url(#gSkin)"/>' + hero_inner() + '</g><circle cx="300" cy="300" r="296" fill="none" stroke="#B8975A" stroke-width="3" stroke-dasharray="3 12" stroke-linecap="round"/></g>'
    b += logo_mark(90, 120, 1.5)
    b += f'<text x="90" y="300" font-family="{SERIF}" font-size="84" fill="#2F3523">LJ Brows Studio</text>'
    b += f'<text x="94" y="352" font-family="{SERIF}" font-size="30" fill="#5A6B33" letter-spacing="3">BROWS · LASHES · WAXING · FACIALS</text>'
    b += f'<text x="94" y="420" font-family="{SERIF}" font-style="italic" font-size="34" fill="#5d6548">Brisbane &amp; Adelaide</text>'
    b += sparkle(560, 100, 26) + sparkle(1130, 540, 22)
    write("og-cover.svg", 1200, 630, b)


if __name__ == "__main__":
    scene_hero()
    scene_brow_lamination(); scene_eyelash_lift(); scene_lash_ext(); scene_facial()
    scene_prod_kit(); scene_prod_pen(); scene_prod_tweezers(); scene_prod_gel()
    ph_about(); ph_services(); ph_shop(); ph_gift(); ph_contact(); ph_brisbane(); ph_adelaide()
    thumb_waxing(); thumb_threading(); thumb_combos()
    gift_pattern(); footer_art(); logo_files(); og_cover()
    print("wrote", len(os.listdir(OUT)), "files to", OUT)
