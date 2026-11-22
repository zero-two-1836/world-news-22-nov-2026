#!/usr/bin/env python3
"""Render the world-news infographic for Sunday 22 November 2026.

Draws a 1024x1024 newspaper-style front page (hero story + 9 panels)
at 2x supersampling (2048x2048) and downscales to 1024x1024.
Fully deterministic: fixed palette, fixed fonts, no randomness, no
timestamps, no network. Requires Pillow.
"""
import os

from PIL import Image, ImageDraw, ImageFont

S = 2                      # supersample factor
W, H = 1024 * S, 1024 * S  # working canvas
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

# --- palette ---------------------------------------------------------------
PAPER = (247, 243, 234)
INK = (20, 20, 20)
MUTED = (90, 86, 76)
RED = (178, 38, 30)
NAVY = (18, 33, 61)
NAVY2 = (28, 48, 88)
GOLD = (233, 180, 60)
CARD = (255, 255, 255)
LINE = (200, 192, 176)
TEAL = (14, 110, 110)
BLUE = (28, 84, 160)
GREEN = (46, 125, 50)
ORANGE = (196, 90, 10)
PURPLE = (104, 58, 140)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_TITLE = font("DejaVuSans-Bold.ttf", 118)
F_DATE = font("DejaVuSans-Bold.ttf", 54)
F_SUB = font("DejaVuSans.ttf", 40)
F_KICK = font("DejaVuSans-Bold.ttf", 34)
F_HEAD = font("DejaVuSans-Bold.ttf", 46)
F_BODY = font("DejaVuSans.ttf", 33)
F_HERO_HEAD = font("DejaVuSans-Bold.ttf", 72)
F_HERO_BODY = font("DejaVuSans.ttf", 42)
F_FOOT = font("DejaVuSans.ttf", 30)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, x, y, fnt, fill, leading):
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


# --- small pictogram icons (all drawn with primitives) ----------------------

def icon_missile(d, x, y, s, c):
    # diagonal missile with nose cone, fins and a burst
    d.polygon([(x + 0.30 * s, y + 0.62 * s), (x + 0.62 * s, y + 0.30 * s),
               (x + 0.78 * s, y + 0.46 * s), (x + 0.46 * s, y + 0.78 * s)], fill=c)
    d.polygon([(x + 0.62 * s, y + 0.30 * s), (x + 0.80 * s, y + 0.12 * s),
               (x + 0.88 * s, y + 0.20 * s)], fill=c)
    d.polygon([(x + 0.30 * s, y + 0.62 * s), (x + 0.12 * s, y + 0.80 * s),
               (x + 0.20 * s, y + 0.88 * s)], fill=c)
    for dx, dy in ((0.10, 0.10), (0.02, 0.22), (0.22, 0.02)):
        d.ellipse([x + dx * s, y + dy * s, x + (dx + 0.12) * s,
                   y + (dy + 0.12) * s], fill=GOLD)


def icon_fence(d, x, y, s, c):
    for i in range(5):
        bx = x + (0.08 + i * 0.19) * s
        d.rectangle([bx, y + 0.10 * s, bx + 0.07 * s, y + 0.90 * s], fill=c)
    d.rectangle([x, y + 0.30 * s, x + s, y + 0.38 * s], fill=c)
    d.rectangle([x, y + 0.62 * s, x + s, y + 0.70 * s], fill=c)
    d.line([x + 0.05 * s, y + 0.05 * s, x + 0.95 * s, y + 0.95 * s],
           fill=RED, width=int(0.08 * s))
    d.line([x + 0.95 * s, y + 0.05 * s, x + 0.05 * s, y + 0.95 * s],
           fill=RED, width=int(0.08 * s))


def icon_globe(d, x, y, s, c):
    d.ellipse([x + 0.08 * s, y + 0.08 * s, x + 0.92 * s, y + 0.92 * s],
              outline=c, width=int(0.07 * s))
    d.ellipse([x + 0.30 * s, y + 0.08 * s, x + 0.70 * s, y + 0.92 * s],
              outline=c, width=int(0.05 * s))
    d.line([x + 0.08 * s, y + 0.50 * s, x + 0.92 * s, y + 0.50 * s],
           fill=c, width=int(0.05 * s))
    d.arc([x + 0.08 * s, y + 0.28 * s, x + 0.92 * s, y + 0.72 * s],
          0, 180, fill=c, width=int(0.05 * s))


def icon_quake(d, x, y, s, c):
    d.polygon([(x + 0.05 * s, y + 0.85 * s), (x + 0.25 * s, y + 0.35 * s),
               (x + 0.45 * s, y + 0.85 * s), (x + 0.65 * s, y + 0.25 * s),
               (x + 0.95 * s, y + 0.85 * s)], fill=c)
    pts = [(x + 0.02 * s, y + 0.55 * s), (x + 0.20 * s, y + 0.55 * s),
           (x + 0.30 * s, y + 0.30 * s), (x + 0.42 * s, y + 0.72 * s),
           (x + 0.55 * s, y + 0.40 * s), (x + 0.68 * s, y + 0.62 * s),
           (x + 0.80 * s, y + 0.45 * s), (x + 0.98 * s, y + 0.55 * s)]
    d.line(pts, fill=RED, width=int(0.07 * s), joint="curve")


def icon_storm(d, x, y, s, c):
    d.ellipse([x + 0.08 * s, y + 0.30 * s, x + 0.48 * s, y + 0.68 * s], fill=c)
    d.ellipse([x + 0.34 * s, y + 0.16 * s, x + 0.78 * s, y + 0.62 * s], fill=c)
    d.ellipse([x + 0.58 * s, y + 0.34 * s, x + 0.94 * s, y + 0.70 * s], fill=c)
    d.rectangle([x + 0.10 * s, y + 0.55 * s, x + 0.90 * s, y + 0.70 * s], fill=c)
    d.polygon([(x + 0.52 * s, y + 0.66 * s), (x + 0.36 * s, y + 0.98 * s),
               (x + 0.50 * s, y + 0.98 * s), (x + 0.42 * s, y + 1.22 * s),
               (x + 0.68 * s, y + 0.82 * s), (x + 0.54 * s, y + 0.82 * s)],
              fill=GOLD)


def icon_boat(d, x, y, s, c):
    d.polygon([(x + 0.10 * s, y + 0.55 * s), (x + 0.90 * s, y + 0.55 * s),
               (x + 0.78 * s, y + 0.82 * s), (x + 0.22 * s, y + 0.82 * s)],
              fill=c)
    d.rectangle([x + 0.47 * s, y + 0.12 * s, x + 0.53 * s, y + 0.55 * s], fill=c)
    d.polygon([(x + 0.53 * s, y + 0.14 * s), (x + 0.53 * s, y + 0.48 * s),
               (x + 0.86 * s, y + 0.48 * s)], fill=RED)
    for wy in (0.88, 0.97):
        d.arc([x, y + wy * s, x + 0.45 * s, y + (wy + 0.10) * s],
              0, 180, fill=BLUE, width=int(0.05 * s))
        d.arc([x + 0.55 * s, y + wy * s, x + s, y + (wy + 0.10) * s],
              0, 180, fill=BLUE, width=int(0.05 * s))


def icon_crowd(d, x, y, s, c):
    for i, px in enumerate((0.12, 0.40, 0.68)):
        d.rectangle([x + px * s, y + 0.30 * s, x + (px + 0.22) * s,
                     y + 0.62 * s], fill=c)
        d.rectangle([x + (px + 0.09) * s, y + 0.62 * s,
                     x + (px + 0.13) * s, y + 0.98 * s], fill=c)
        d.ellipse([x + (px + 0.04) * s, y + 0.10 * s,
                   x + (px + 0.18) * s, y + 0.28 * s], fill=c)


def icon_chart(d, x, y, s, c):
    d.line([x + 0.10 * s, y + 0.90 * s, x + 0.90 * s, y + 0.90 * s],
           fill=c, width=int(0.06 * s))
    d.line([x + 0.10 * s, y + 0.90 * s, x + 0.10 * s, y + 0.10 * s],
           fill=c, width=int(0.06 * s))
    pts = [(x + 0.14 * s, y + 0.30 * s), (x + 0.32 * s, y + 0.42 * s),
           (x + 0.50 * s, y + 0.38 * s), (x + 0.68 * s, y + 0.62 * s),
           (x + 0.86 * s, y + 0.78 * s)]
    d.line(pts, fill=RED, width=int(0.08 * s), joint="curve")
    d.polygon([(x + 0.86 * s, y + 0.78 * s), (x + 0.86 * s, y + 0.62 * s),
               (x + 0.98 * s, y + 0.80 * s)], fill=RED)


def icon_chip(d, x, y, s, c):
    d.rectangle([x + 0.22 * s, y + 0.22 * s, x + 0.78 * s, y + 0.78 * s],
                outline=c, width=int(0.07 * s))
    d.rectangle([x + 0.38 * s, y + 0.38 * s, x + 0.62 * s, y + 0.62 * s], fill=c)
    for i in range(3):
        px = x + (0.34 + i * 0.16) * s
        d.line([px, y + 0.08 * s, px, y + 0.22 * s], fill=c, width=int(0.05 * s))
        d.line([px, y + 0.78 * s, px, y + 0.92 * s], fill=c, width=int(0.05 * s))
        py = y + (0.34 + i * 0.16) * s
        d.line([x + 0.08 * s, py, x + 0.22 * s, py], fill=c, width=int(0.05 * s))
        d.line([x + 0.78 * s, py, x + 0.92 * s, py], fill=c, width=int(0.05 * s))


def icon_cuffs(d, x, y, s, c):
    d.ellipse([x + 0.05 * s, y + 0.30 * s, x + 0.45 * s, y + 0.70 * s],
              outline=c, width=int(0.09 * s))
    d.ellipse([x + 0.55 * s, y + 0.30 * s, x + 0.95 * s, y + 0.70 * s],
              outline=c, width=int(0.09 * s))
    d.line([x + 0.45 * s, y + 0.50 * s, x + 0.55 * s, y + 0.50 * s],
           fill=c, width=int(0.07 * s))


# --- the day's stories (researched 22 Nov 2026; Reuters, AP, AFP, CNN, USGS) -
HERO = {
    "kicker": "MEXICO  ·  TOP STORY",
    "headline": "FBI's most-wanted cartel boss 'El Chapo Isidro' captured",
    "body": "Mexican troops seize Fausto Isidro Meza Flores in Sinaloa. "
            "Eleven killed as gunmen burn trucks and block roads.",
}

PANELS = [
    ("POLAND", "Russian missiles land on NATO soil",
     "Two cruise missiles and a drone crash in Poland. NATO vows to defend "
     "\u201cevery inch\u201d of allied land.", icon_missile, BLUE),
    ("ESTONIA", "Estonia shuts its Russia border",
     "All road crossings close from 1 Dec after a GRU-linked sabotage "
     "attack on a defence firm.", icon_fence, TEAL),
    ("CLIMATE · COP31", "Climate talks in overtime, fossil fuels cut",
     "Draft deal in Antalya drops all mention of fossil fuels. No "
     "agreement yet.", icon_globe, GREEN),
    ("PERU", "Magnitude 6.9 quake shakes the Andes",
     "Strong tremor felt in Lima. No damage or casualties reported.",
     icon_quake, ORANGE),
    ("BRAZIL", "Supercell storm flattens a town",
     "Three dead and 5,000 homes damaged in Tupanciret\u00e3, southern "
     "Brazil.", icon_storm, PURPLE),
    ("NIGERIA", "Boat sinks carrying mourners",
     "At least 24 dead after a funeral boat capsizes in Bayelsa state.",
     icon_boat, BLUE),
    ("FRANCE", "Sixth weekend of street protests",
     "82,500 march across France over living costs and public services.",
     icon_crowd, RED),
    ("MARKETS", "Tech stocks plunge on Wall Street",
     "Sell-off deepens in the US and spreads across Asia and Europe.",
     icon_chart, RED),
    ("UNITED STATES", "Trump warns over AI data centres abroad",
     "US firms building them overseas face a \u201ctremendous tax\u201d, "
     "Trump says.", icon_chip, NAVY2),
]


def draw_header(d):
    d.rectangle([0, 0, W, H], fill=PAPER)
    d.rectangle([48, 44, W - 48, 50], fill=RED)
    title = "WORLD NEWS"
    tw = d.textlength(title, font=F_TITLE)
    d.text(((W - tw) / 2, 62), title, font=F_TITLE, fill=INK)
    date = "SUNDAY  22  NOVEMBER  2026"
    dw = d.textlength(date, font=F_DATE)
    d.text(((W - dw) / 2, 196), date, font=F_DATE, fill=RED)
    d.rectangle([48, 268, W - 48, 274], fill=INK)
    sub = "The day in one image  ·  Ten stories from around the world"
    sw = d.textlength(sub, font=F_SUB)
    d.text(((W - sw) / 2, 288), sub, font=F_SUB, fill=MUTED)


def draw_hero(d):
    x0, y0, x1, y1 = 48, 344, W - 48, 812
    d.rounded_rectangle([x0, y0, x1, y1], radius=28, fill=NAVY)
    d.rounded_rectangle([x0, y0, x1, y1], radius=28, outline=GOLD, width=4)
    # left: pictogram in a gold-ringed disc
    cx, cy, r = x0 + 190, y0 + 234, 150
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=GOLD, width=6)
    icon_cuffs(d, cx - 120, cy - 120, 240, (255, 255, 255))
    tx = x0 + 400
    d.text((tx, y0 + 48), HERO["kicker"], font=F_KICK, fill=GOLD)
    y = y0 + 112
    y = draw_lines(d, wrap(d, HERO["headline"], F_HERO_HEAD, x1 - tx - 60),
                   tx, y, F_HERO_HEAD, (255, 255, 255), 84)
    y += 18
    draw_lines(d, wrap(d, HERO["body"], F_HERO_BODY, x1 - tx - 60),
               tx, y, F_HERO_BODY, (214, 222, 235), 50)


def draw_grid(d):
    gx, gy = 48, 844
    gw = (W - 96 - 2 * 28) // 3
    gh = 352
    gap = 28
    for i, (kicker, head, body, icon, color) in enumerate(PANELS):
        col, row = i % 3, i // 3
        x0 = gx + col * (gw + gap)
        y0 = gy + row * (gh + gap)
        x1, y1 = x0 + gw, y0 + gh
        d.rounded_rectangle([x0, y0, x1, y1], radius=22, fill=CARD,
                            outline=LINE, width=3)
        d.rectangle([x0 + 24, y0 + 24, x0 + 34, y0 + 74], fill=color)
        d.text((x0 + 52, y0 + 22), kicker, font=F_KICK, fill=color)
        icon(d, x1 - 100, y0 + 12, 76, color)
        y = y0 + 92
        y = draw_lines(d, wrap(d, head, F_HEAD, gw - 48),
                       x0 + 24, y, F_HEAD, INK, 50)
        y += 8
        draw_lines(d, wrap(d, body, F_BODY, gw - 48),
                   x0 + 24, y, F_BODY, MUTED, 42)


def draw_footer(d):
    foot = ("Sources: Reuters  ·  Associated Press  ·  AFP  ·  CNN  ·  USGS"
            "     —     Sunday 22 November 2026")
    fw = d.textlength(foot, font=F_FOOT)
    d.text(((W - fw) / 2, H - 62), foot, font=F_FOOT, fill=MUTED)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    draw_header(d)
    draw_hero(d)
    draw_grid(d)
    draw_footer(d)
    img = img.resize((1024, 1024), Image.LANCZOS)
    img.save(OUT, format="PNG", optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
