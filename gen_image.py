#!/usr/bin/env python3
"""Draw the Agent 3 front page for news-image-20261122, round 3.

One-day news image: Sunday 22 November 2026. Cream newspaper front page:
masthead, giant date, fresh stat strip, region bar, BY HOURS strip, three
hero stories, ten more panels, a dotted-style world map with numbered pins,
an ALSO list of 25 more stories, a DATE CHECK box and a sources footer.

Renders entry.png (1024x1024) next to this file. Run: python3 gen_image.py
"""
import os
import textwrap
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
CREAM = (247, 240, 220)
PAPER = (255, 253, 246)
INK = (28, 26, 23)
MUTED = (107, 98, 87)
RED = (176, 30, 36)
RED_DK = (140, 22, 28)
GOLD = (200, 160, 40)
NAVY = (31, 78, 121)
TEAL = (18, 90, 86)
BORDER = (216, 205, 180)
SEA = (214, 230, 235)
LAND = (232, 214, 170)
PINK = (250, 232, 228)

FD = "/usr/share/fonts/truetype/dejavu"
FL = "/usr/share/fonts/truetype/liberation"


def font(name, size):
    for base in (FD, FL):
        p = os.path.join(base, name)
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)

img = Image.new("RGB", (W, H), CREAM)
d = ImageDraw.Draw(img)


def wrap(text, fnt, width):
    """Greedy wrap on words to the given pixel width."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text(x, y, s, fnt, fill=INK, anchor="la"):
    d.text((x, y), s, font=fnt, fill=fill, anchor=anchor)


def centre(x, y, s, fnt, fill=INK):
    d.text((x, y), s, font=fnt, fill=fill, anchor="ma")


def badge(cx, cy, num, r=11):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED, outline=(255, 255, 255), width=2)
    centre(cx, cy - 8, str(num), SANS_B(13), (255, 255, 255))


def flames(cx, base_y, scale=1.0):
    """A cluster of orange/yellow flame triangles."""
    cols = [(255, 140, 0), (255, 190, 40), (230, 80, 10)]
    for i, (dx, wdt, hgt) in enumerate([(-16, 14, 26), (0, 20, 38), (16, 14, 26)]):
        c = cols[i % 3]
        x0 = cx + dx * scale
        d.polygon([(x0 - wdt * scale / 2, base_y), (x0, base_y - hgt * scale),
                   (x0 + wdt * scale / 2, base_y)], fill=c)


def smoke(cx, cy, n=4, top=None):
    """Grey smoke puffs rising from a fire, never drawn above `top`.

    The default ceiling keeps every puff inside the art box that called it,
    so no puff can spill into the strip or panel above it.
    """
    if top is None:
        top = cy - 8
    for i in range(n):
        r = 7 - i
        px = cx + i * 6
        py = max(cy - i * 4, top + r)
        d.ellipse([px - r, py - r, px + r, py + r], fill=(120, 120, 120))


# ---------------------------------------------------------------- masthead
d.rectangle([8, 8, 1016, 44], fill=RED)
text(20, 15, "THE WORLD IN ONE DAY", SANS_B(20), (255, 255, 255))
text(1004, 19, "BY HOURS + NUMBERS", SANS_B(13), (255, 255, 255), anchor="ra")

# ---------------------------------------------------------------- title
centre(512, 50, "Sunday 22 November 2026", SERIF_B(44))
centre(512, 100, "COP31 nears a deal in Antalya  ·  Iran strikes US bases in Bahrain  ·  "
                  "Russian ship still burning in the Baltic", SANS(14), MUTED)

# ---------------------------------------------------------------- stat strip
STATS = [
    ("03:00 GMT", "COP31 OBJECTIONS CLOSE"),
    ("16", "SPARTA II CREW SAVED"),
    ("2", "US BASES HIT IN BAHRAIN"),
    ("856", "HONG KONG CANDIDATES"),
    ("35%", "COP31 CLEAN POWER 2035"),
    ("24", "BAYELSA DEAD"),
]
sx, sy, sw, sh, gap = 8, 118, 163, 42, 6
for i, (num, lab) in enumerate(STATS):
    x0 = sx + i * (sw + gap)
    d.rectangle([x0, sy, x0 + sw, sy + sh], fill=PAPER, outline=BORDER, width=1)
    centre(x0 + sw // 2, sy + 3, num, SANS_B(20), RED)
    centre(x0 + sw // 2, sy + 28, lab, SANS_B(8), MUTED)

# ---------------------------------------------------------------- region bar
REGIONS = [("EUROPE", 9, (176, 30, 36)), ("MIDDLE EAST", 8, (214, 110, 30)),
           ("ASIA", 9, (31, 78, 121)), ("AMERICAS", 5, (46, 125, 70)),
           ("AFRICA", 2, (110, 80, 140)), ("OCEANIA", 2, (18, 120, 120)),
           ("GLOBAL", 3, (110, 110, 110))]
rx, ry, rw = 8, 166, 1008
x = rx
for name, n, col in REGIONS:
    seg = rw * n // 38
    d.rectangle([x, ry, x + seg, ry + 12], fill=col)
    x += seg
centre(512, ry + 15, "EUROPE 9  ·  MIDDLE EAST 8  ·  ASIA 9  ·  AMERICAS 5  ·  "
                      "AFRICA 2  ·  OCEANIA 2  ·  GLOBAL 3  —  38 STORIES",
       SANS_B(11))

# ---------------------------------------------------------------- BY HOURS strip
d.rectangle([8, 198, 1016, 234], fill=(238, 228, 202), outline=BORDER, width=1)
d.rectangle([8, 198, 138, 234], fill=RED)
text(16, 210, "THE DAY", SANS_B(12), (255, 255, 255))
text(16, 222, "BY HOURS", SANS_B(12), (255, 255, 255))
HOURS = [
    ("01:58 UTC", "Bitcoin $60,020"),
    ("03:00 GMT", "COP31 objections close"),
    ("04:00 UTC", "F1 finish, Las Vegas"),
    ("06:00 GMT", "COP31 approval opens"),
    ("13:00 WIB", "HK turnout 89.81%"),
    ("16:30 GMT", "Liverpool v Man Utd"),
    ("17:00 GMT", "ATP final"),
]
hx = 146
for t, lab in HOURS:
    text(hx, 203, t, SANS_B(11), RED)
    for j, ln in enumerate(wrap(lab, SANS(10), 118)):
        text(hx, 218 + j * 11, ln, SANS(10))
    hx += 126

# ---------------------------------------------------------------- hero art
def hero_cop31(x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(16, 52, 66))
    d.rectangle([x0 + 70, y0 + 8, x0 + w - 70, y0 + 42], fill=(24, 84, 96))
    centre(x0 + w // 2, y0 + 12, "COP31", SANS_B(22), (255, 255, 255))
    d.ellipse([x0 + w // 2 - 76, y0 + 16, x0 + w // 2 - 58, y0 + 34], fill=(120, 200, 90))
    d.ellipse([x0 + w // 2 + 58, y0 + 16, x0 + w // 2 + 76, y0 + 34], fill=(120, 200, 90))
    for r in range(3):
        y = y0 + 52 + r * 16
        for c in range(7):
            cx = x0 + 22 + c * 42
            d.rectangle([cx - 15, y + 6, cx + 15, y + 12], fill=(120, 90, 50))
            d.ellipse([cx - 5, y - 4, cx + 5, y + 6], fill=(235, 205, 170))
            d.rectangle([cx - 12, y + 2, cx - 4, y + 6], fill=[(200, 40, 40), (40, 90, 180),
                        (240, 200, 60), (40, 140, 80), (255, 255, 255)][(r + c) % 5])


def hero_sparta(x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(12, 22, 48))
    for sx_, sy_ in [(30, 14), (90, 26), (180, 10), (260, 22), (300, 12)]:
        d.ellipse([x0 + sx_, y0 + sy_, x0 + sx_ + 3, y0 + sy_ + 3], fill=(255, 255, 255))
    d.ellipse([x0 + w - 52, y0 + 10, x0 + w - 22, y0 + 40], fill=(240, 238, 220))
    d.rectangle([x0, y0 + 62, x0 + w, y0 + h], fill=(20, 44, 74))
    d.rectangle([x0 + 30, y0 + 46, x0 + w - 30, y0 + 74], fill=(90, 40, 34))
    for i, col in enumerate([(200, 90, 40), (60, 120, 160), (190, 160, 60)]):
        d.rectangle([x0 + 48 + i * 62, y0 + 28, x0 + 96 + i * 62, y0 + 46], fill=col)
    flames(x0 + 90, y0 + 30, 0.9)
    flames(x0 + 250, y0 + 30, 0.7)
    smoke(x0 + 90, y0 + 8)
    for i in range(6):
        d.line([x0 + 40 + i * 44, y0 + 82, x0 + 70 + i * 44, y0 + 82], fill=(255, 170, 60), width=2)


def hero_bahrain(x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(14, 18, 40))
    for bx, bw, bh in [(0, 34, 46), (40, 26, 62), (72, 40, 38), (118, 30, 58),
                       (154, 36, 44), (196, 28, 66), (230, 34, 40), (268, 30, 54)]:
        d.rectangle([x0 + bx, y0 + h - bh, x0 + bx + bw, y0 + h], fill=(30, 34, 58))
        for wy in range(y0 + h - bh + 6, y0 + h - 4, 10):
            for wx in range(x0 + bx + 5, x0 + bx + bw - 4, 10):
                d.rectangle([wx, wy, wx + 3, wy + 4], fill=(255, 210, 110))
    d.polygon([(x0 + 120, y0 + 8), (x0 + 140, y0 + h), (x0 + 130, y0 + h)], fill=(255, 220, 120))
    d.polygon([(x0 + 200, y0 + 8), (x0 + 190, y0 + h), (x0 + 206, y0 + h)], fill=(200, 220, 255))
    flames(x0 + 60, y0 + 46, 0.8)
    flames(x0 + 250, y0 + 40, 0.9)
    smoke(x0 + 250, y0 + 16)
    d.line([x0 + 90, y0 + 12, x0 + 130, y0 + 34], fill=(255, 255, 255), width=2)
    d.line([x0 + 220, y0 + 10, x0 + 190, y0 + 30], fill=(255, 255, 255), width=2)


HEROES = [
    (1, "ANTALYA, TÜRKIYE · CLIMATE", "COP31 nears a deal as approval session opens",
     "Final text tabled early Sunday, no fossil-fuel mention; clean power 35% by 2035. "
     "Objections closed 03:00 GMT; approval 06:00 GMT — quorum fear remains.", hero_cop31),
    (2, "GULF OF FINLAND · WAR", "Russian ship still burning in Finnish waters",
     "Sparta II hit by two drones Saturday; fire still burning Sunday; 16 crew evacuated. "
     "Finland leads the rescue. Helsinki: Ukraine likely behind it.", hero_sparta),
    (3, "BAHRAIN · IRAN WAR", "Iran strikes US bases in Bahrain",
     "Strikes hit two Patriot radar sites at al-Riffa and Awali on Saturday night; Bahrain says "
     "most were intercepted, one industrial site burned, no casualties.", hero_bahrain),
]
hy, hh, hw = 240, 182, 328
for i, (num, kick, head, body, art) in enumerate(HEROES):
    x0 = 8 + i * (hw + 8)
    d.rectangle([x0, hy, x0 + hw, hy + hh], fill=PAPER, outline=BORDER, width=1)
    art(x0 + 1, hy + 1, hw - 2, 96)
    badge(x0 + 16, hy + 16, num, 12)
    text(x0 + 10, hy + 104, kick, SANS_B(9), RED)
    y = hy + 118
    for ln in wrap(head, SANS_B(17), hw - 20):
        text(x0 + 10, y, ln, SANS_B(17))
        y += 19
    y += 2
    for ln in wrap(body, SANS(11), hw - 20):
        text(x0 + 10, y, ln, SANS(11))
        y += 13

# ---------------------------------------------------------------- panel art
def p_ukraine(x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(16, 20, 44))
    for dx, dy in [(30, 12), (70, 20), (120, 10), (160, 24)]:
        d.ellipse([x0 + dx, y0 + dy, x0 + dx + 3, y0 + dy + 3], fill=(255, 255, 255))
    flames(x0 + w // 2, y0 + h - 14, 1.0)
    smoke(x0 + w // 2, y0 + 10)
    for bx, bw, bh in [(6, 26, 22), (40, 20, 30), (150, 28, 24)]:
        d.rectangle([x0 + bx, y0 + h - bh, x0 + bx + bw, y0 + h], fill=(40, 42, 60))


def p_hk(x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(196, 40, 44))
    d.rectangle([x0 + 70, y0 + 22, x0 + w - 70, y0 + h], fill=(150, 25, 30))
    d.rectangle([x0 + 78, y0 + 14, x0 + w - 78, y0 + 26], fill=(40, 40, 40))
    d.rectangle([x0 + 82, y0 + 4, x0 + 114, y0 + 26], fill=(255, 255, 255))
    d.line([x0 + 86, y0 + 16, x0 + 94, y0 + 23, x0 + 110, y0 + 7], fill=RED, width=3)


def p_hormuz(x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(14, 90, 96))
    d.rectangle([x0, y0 + 26, x0 + w, y0 + h], fill=(24, 120, 128))
    d.rectangle([x0 + 18, y0 + 18, x0 + w - 18, y0 + 38], fill=(70, 50, 44))
    d.rectangle([x0 + 130, y0 + 6, x0 + 150, y0 + 18], fill=(200, 200, 200))
    flames(x0 + 40, y0 + 22, 0.5)
    for i in range(4):
        d.line([x0 + 16 + i * 44, y0 + 44, x0 + 40 + i * 44, y0 + 44], fill=(160, 220, 225), width=2)


def p_cricket(x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(58, 140, 70))
    d.ellipse([x0 + 8, y0 + 8, x0 + w - 8, y0 + h + 30], fill=(120, 190, 110))
    d.rectangle([x0 + 84, y0 + 6, x0 + 96, y0 + 34], fill=(220, 190, 130))
    d.line([x0 + 84, y0 + 6, x0 + 96, y0 + 34], fill=(120, 90, 40), width=2)
    d.ellipse([x0 + 130, y0 + 30, x0 + 142, y0 + 42], fill=(200, 40, 40))
    for sx in (30, 150):
        for k in range(3):
            d.rectangle([x0 + sx + k * 5, y0 + h - 22, x0 + sx + k * 5 + 3, y0 + h - 8],
                        fill=(240, 220, 160))


def p_f1(x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(24, 24, 34))
    for cx in range(x0 + 4, x0 + w, 16):
        d.rectangle([cx, y0 + 6, cx + 8, y0 + 14], fill=(255, 255, 255) if (cx // 16) % 2 else (20, 20, 20))
        d.rectangle([cx + 8, y0 + 6, cx + 16, y0 + 14], fill=(20, 20, 20) if (cx // 16) % 2 else (255, 255, 255))
    d.polygon([(x0 + 50, y0 + 40), (x0 + 150, y0 + 32), (x0 + 168, y0 + 42), (x0 + 60, y0 + 46)],
              fill=(200, 30, 30))
    d.polygon([(x0 + 150, y0 + 32), (x0 + 168, y0 + 26), (x0 + 176, y0 + 36), (x0 + 168, y0 + 42)],
              fill=(160, 20, 20))
    for wx in (62, 150):
        d.ellipse([x0 + wx, y0 + 38, x0 + wx + 16, y0 + 54], fill=(10, 10, 10))
        d.ellipse([x0 + wx + 4, y0 + 42, x0 + wx + 12, y0 + 50], fill=(180, 180, 180))
    text(x0 + w - 22, y0 + 26, "1", SANS_B(16), (255, 255, 255))


def p_gaza(x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(222, 208, 180))
    d.rectangle([x0 + 40, y0 + 16, x0 + 150, y0 + 40], fill=(240, 240, 240))
    d.rectangle([x0 + 150, y0 + 22, x0 + 172, y0 + 40], fill=(200, 200, 200))
    d.rectangle([x0 + 60, y0 + 22, x0 + 76, y0 + 34], fill=RED)
    d.rectangle([x0 + 72, y0 + 20, x0 + 76, y0 + 36], fill=RED)
    for wx in (56, 148):
        d.ellipse([x0 + wx, y0 + 38, x0 + wx + 14, y0 + 52], fill=(30, 30, 30))
    d.line([x0 + 8, y0 + h - 2, x0 + w - 8, y0 + h - 2], fill=(120, 110, 95), width=2)


def p_sudan(x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(238, 210, 150))
    d.ellipse([x0 + w - 46, y0 + 6, x0 + w - 16, y0 + 36], fill=(255, 200, 90))
    d.polygon([(x0, y0 + h), (x0 + 70, y0 + 22), (x0 + 150, y0 + h)], fill=(214, 170, 100))
    d.polygon([(x0 + 90, y0 + h), (x0 + 150, y0 + 30), (x0 + w, y0 + h)], fill=(200, 155, 88))
    for tx in (30, 70, 120):
        d.polygon([(x0 + tx, y0 + 40), (x0 + tx + 12, y0 + 28), (x0 + tx + 24, y0 + 40)],
                  fill=(250, 245, 230))


def p_basra(x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(52, 52, 60))
    for tx, tw in [(30, 26), (70, 30), (120, 26)]:
        d.polygon([(x0 + tx, y0 + h), (x0 + tx + 5, y0 + 14), (x0 + tx + tw - 5, y0 + 14),
                   (x0 + tx + tw, y0 + h)], fill=(150, 150, 155))
        d.ellipse([x0 + tx + 3, y0 + 10, x0 + tx + tw - 3, y0 + 18], fill=(120, 120, 125))
    flames(x0 + 85, y0 + 20, 0.8)
    smoke(x0 + 85, y0 + 14)


def p_bayelsa(x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(30, 110, 150))
    for i in range(3):
        d.arc([x0 + 10 + i * 55, y0 + 34, x0 + 60 + i * 55, y0 + 54], 0, 180, fill=(200, 235, 245), width=2)
    d.polygon([(x0 + 40, y0 + 22), (x0 + 155, y0 + 22), (x0 + 140, y0 + 34), (x0 + 55, y0 + 34)],
              fill=(120, 80, 50))
    d.polygon([(x0 + 90, y0 + 22), (x0 + 95, y0 + 8), (x0 + 100, y0 + 22)], fill=(240, 240, 230))


def p_bepi(x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(8, 10, 26))
    for sx_, sy_ in [(20, 10), (60, 24), (150, 12), (180, 30), (110, 8)]:
        d.ellipse([x0 + sx_, y0 + sy_, x0 + sx_ + 2, y0 + sy_ + 2], fill=(255, 255, 255))
    d.ellipse([x0 + 118, y0 + 6, x0 + 178, y0 + 52], fill=(160, 158, 150))
    for cx, cy, cr in [(140, 20, 5), (160, 32, 4), (132, 38, 3), (166, 16, 3)]:
        d.ellipse([x0 + cx - cr, y0 + cy - cr, x0 + cx + cr, y0 + cy + cr], fill=(120, 118, 110))
    d.rectangle([x0 + 30, y0 + 22, x0 + 78, y0 + 34], fill=(40, 90, 180))
    d.rectangle([x0 + 44, y0 + 16, x0 + 64, y0 + 40], fill=(200, 200, 200))
    d.line([x0 + 78, y0 + 28, x0 + 118, y0 + 28], fill=(255, 255, 255), width=2)


PANELS = [
    (4, "KYIV · WAR", "Ukraine hit by 148 drones overnight",
     "148 drones + 3 missiles + 12 glide bombs; Kryvyi Rih 2 dead, 60 hurt; 161 drones shot down.", p_ukraine),
    (5, "HONG KONG · POLITICS", "Hong Kong votes for its Election Committee",
     "856 candidates chase 723 seats; turnout 89.81% by 13:00.", p_hk),
    (6, "HORMUZ · IRAN WAR", "Two tankers hit leaving Hormuz",
     "One struck in the stern, one in the engine room; no casualties.", p_hormuz),
    (7, "WELLINGTON · CRICKET", "Pant 128 as India declare 720/9, lead 352",
     "Pant 128 off 153 balls; Jurel 78. NZ 105/2, trailing by 247.", p_cricket),
    (8, "LAS VEGAS · FORMULA ONE", "Verstappen wins the Las Vegas GP",
     "Third win in four years. Norris 2nd (+0.639), Piastri 3rd.", p_f1),
    (9, "GAZA · CEASEFIRE", "Four killed as Gaza ceasefire frays",
     "4 Palestinians dead, 14 hurt; food-aid vehicle hit, 3 killed.", p_gaza),
    (10, "SUDAN · WAR", "5,000 still missing in El-Fasher",
     "MSF: 5,000 unaccounted for after the city's fall.", p_sudan),
    (11, "BASRA, IRAQ · DISASTER", "Power plant fire kills four in Basra",
     "Blaze at the Hartha plant; 4 dead, 35 injured.", p_basra),
    (12, "BAYELSA, NIGERIA · DISASTER", "Boat carrying mourners capsizes, 24 dead",
     "Passengers heading to a funeral; toll rose to 24.", p_bayelsa),
    (13, "WORLD · SPACE", "BepiColombo enters orbit around Mercury",
     "ESA craft sends first photos from Mercury orbit.", p_bepi),
]
pw, ph = 196, 124
for row in range(2):
    y0 = 428 + row * 130
    for col in range(5):
        num, kick, head, body, art = PANELS[row * 5 + col]
        x0 = 8 + col * (pw + 7)
        d.rectangle([x0, y0, x0 + pw, y0 + ph], fill=PAPER, outline=BORDER, width=1)
        art(x0 + 1, y0 + 1, pw - 2, 52)
        badge(x0 + 14, y0 + 14, num, 10)
        text(x0 + 8, y0 + 57, kick, SANS_B(8), RED)
        yy = y0 + 68
        for ln in wrap(head, SANS_B(12), pw - 16):
            text(x0 + 8, yy, ln, SANS_B(12))
            yy += 13
        yy += 1
        for ln in wrap(body, SANS(10), pw - 16):
            text(x0 + 8, yy, ln, SANS(10))
            yy += 11

# ---------------------------------------------------------------- map
text(8, 692, "WHERE IT HAPPENED", SANS_B(11), RED)
text(1016, 692, "Numbered pins mark panels 1–13", SANS(10), MUTED, anchor="ra")
MX0, MX1, MY0, MY1 = 8, 1016, 706, 786
d.rectangle([MX0, MY0, MX1, MY1], fill=SEA, outline=BORDER, width=1)


def ll(lon, lat):
    return (MX0 + (lon + 170) / 360.0 * (MX1 - MX0),
            MY0 + (78 - lat) / 136.0 * (MY1 - MY0))


def poly(points, fill=LAND):
    d.polygon([ll(lo, la) for lo, la in points], fill=fill)


poly([(-168, 66), (-140, 70), (-120, 71), (-95, 80), (-80, 73), (-75, 62), (-65, 60),
      (-55, 47), (-70, 42), (-75, 35), (-80, 32), (-85, 30), (-90, 21), (-95, 16),
      (-83, 9), (-79, 9), (-90, 14), (-100, 16), (-105, 20), (-110, 23), (-115, 30),
      (-125, 40), (-125, 49), (-140, 60), (-155, 58), (-165, 60)])
poly([(-79, 9), (-75, 11), (-70, 12), (-62, 10), (-55, 6), (-50, 0), (-44, -3),
      (-35, -8), (-40, -20), (-48, -28), (-55, -35), (-65, -41), (-70, -50),
      (-73, -53), (-70, -40), (-72, -20), (-77, -12), (-80, -4), (-80, 1)])
poly([(-17, 15), (-10, 30), (0, 36), (10, 37), (20, 32), (32, 31), (35, 28),
      (43, 12), (48, 11), (51, 12), (44, 0), (40, -10), (35, -18), (32, -26),
      (26, -34), (19, -35), (15, -27), (12, -18), (9, -1), (9, 4), (-8, 5),
      (-13, 8), (-17, 12)])
poly([(-10, 36), (-9, 43), (-2, 48), (0, 50), (5, 53), (8, 57), (18, 56), (21, 55),
      (24, 58), (30, 60), (30, 65), (40, 68), (55, 68), (70, 72), (90, 75),
      (110, 76), (130, 72), (150, 70), (170, 66), (178, 65), (170, 60), (162, 56),
      (158, 52), (142, 50), (140, 40), (130, 42), (127, 35), (122, 30), (120, 25),
      (110, 20), (105, 10), (100, 8), (98, 12), (92, 16), (88, 22), (80, 15),
      (75, 10), (72, 20), (66, 25), (58, 25), (55, 26), (52, 28), (48, 30),
      (44, 29), (40, 36), (36, 36), (30, 36), (27, 37), (23, 36), (18, 40),
      (12, 44), (8, 44), (3, 43), (-2, 37), (-9, 37)])
poly([(114, -22), (114, -32), (120, -34), (130, -32), (138, -35), (146, -39),
      (150, -37), (153, -27), (146, -19), (142, -11), (136, -12), (132, -12),
      (126, -14), (122, -17), (114, -22)])
poly([(-45, 60), (-40, 65), (-30, 68), (-22, 70), (-25, 76), (-40, 80), (-55, 76),
      (-58, 70), (-52, 64)])
poly([(44, -16), (47, -15), (50, -16), (49, -20), (45, -25), (43, -21)])
poly([(-5, 50), (-3, 53), (-5, 56), (-2, 58), (0, 53), (1, 51)])
poly([(130, 31), (132, 33), (135, 34), (138, 35), (140, 38), (141, 42), (143, 44),
      (141, 45), (139, 40), (137, 36), (133, 33)])
poly([(167, -35), (169, -37), (172, -40), (174, -41), (176, -38), (174, -35), (170, -34)])

PINS = [  # num, lon, lat, dx, dy (pixel nudge so crowded pins do not overlap)
    (1, 30.7, 36.9, -14, -10), (2, 24.9, 60.2, 14, -8), (3, 50.6, 26.2, 16, 10),
    (4, 33.4, 47.9, 12, -12), (5, 114.2, 22.3, 0, -10), (6, 56.3, 27.2, 18, -10),
    (7, 174.8, -41.3, -12, -8), (8, -115.1, 36.2, 0, -10), (9, 34.5, 31.5, -16, 10),
    (10, 25.3, 13.6, -14, 10), (11, 47.8, 30.5, 14, 12), (12, 6.3, 4.9, 0, -10),
    (13, 8.65, 49.87, -16, -6),
]
for num, lon, lat, dx, dy in PINS:
    px, py = ll(lon, lat)
    cx, cy = px + dx, py + dy
    if dx or dy:
        d.line([px, py, cx, cy], fill=INK, width=1)
        d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=INK)
    badge(cx, cy, num, 8)

# ---------------------------------------------------------------- ALSO list
ALSO = [
    ("MEXICO", "El Chapo Isidro held; 11 killed in violence"),
    ("JERUSALEM", "Eisenkot invites Likud to coalition talks"),
    ("TEHRAN", "Power rationed 2 hrs a day as gas lags"),
    ("SAN ANTONIO", "Wembanyama 50 pts, 19 boards, Spurs record"),
    ("WASHINGTON", "Nvidia faces SEC probe; shares -14%"),
    ("BRASÍLIA", "Bolsonaro in ICU, stable"),
    ("TALLINN", "Estonia shuts Russia border 1 Dec"),
    ("SEOUL", "Education minister quits over exam leak"),
    ("BEIJING", "China bans US phones, calls them “malicious”"),
    ("TOKYO", "Japan holds first live-fire drill with India"),
    ("NEW DELHI", "Nepal PM arrives on first visit"),
    ("CANBERRA", "Marles rejects US report on AUKUS"),
    ("JAKARTA", "EU–Indonesia trade deal; 98.5% tariffs cut"),
    ("BRUSSELS", "Air-traffic strike cancels Monday flights"),
    ("PARIS", "France seeks UN action on Myanmar"),
    ("MANILA", "Chinese bomber turns back 170 km out"),
    ("LIVERPOOL", "Liverpool v Man Utd 16:30 GMT"),
    ("TURIN", "Zverev v Alcaraz, ATP final 17:00 GMT"),
    ("RIYADH", "Saudi coalition downs 3 Houthi missiles"),
    ("GAZA AID", "Four nations press Israel on aid"),
    ("MELBOURNE", "Australia chase 188 to beat England in T20"),
    ("KYIV", "Drone hits 5-storey block in Kyiv Oblast"),
    ("MARKETS", "Bitcoin rebounds above $60,000 (+1.85%)"),
    ("VATICAN", "Pope Leo lunches with 1,300 poor guests"),
    ("THE HAGUE", "World court: Myanmar committed genocide on Rohingya"),
]
text(8, 792, "ALSO ON SUNDAY 22 NOVEMBER", SANS_B(11), RED)
d.line([8, 806, 1016, 806], fill=RED, width=1)
ay = 810
for i, (city, s) in enumerate(ALSO):
    col = 0 if i < 13 else 1
    xx = 8 if col == 0 else 516
    yy = ay + (i % 13) * 10
    text(xx, yy, f"{14 + i}. {city} — {s}", SANS(9), INK)

# ---------------------------------------------------------------- DATE CHECK
d.rectangle([8, 944, 1016, 998], fill=PINK, outline=RED, width=1)
dc = ("DATE CHECK — Every story here happened, or was first reported, on Sunday 22 November 2026 "
      "in at least one time zone. Tonight’s barrage was 148 drones — not Friday’s 400. Left out as "
      "earlier news: Peru quake (Fri 20 Nov) · missiles landing in Poland (19 Nov) · Kerch Bridge "
      "strikes (earlier this week) · Shenzhen summit (19 Nov) · Voyager 1 (18 Nov) · GTA VI launch "
      "(19 Nov) · Anthropic IPO (19 Nov). Not yet happened when drawn: final COP31 approval "
      "(06:00 GMT session) · ATP final (17:00 GMT) · Liverpool v Man Utd (16:30 GMT).")
yy = 948
for ln in wrap(dc, SANS(9), 984):
    text(16, yy, ln, SANS(9))
    yy += 11

# ---------------------------------------------------------------- footer
text(8, 1002, "Sources: Reuters · AP · AFP · SCMP · Al Jazeera · Kyiv Independent · UKMTO · ESA · "
              "Vatican News · ABC · Guardian · Straits Times · NBA · ATP · F1", SANS(9), MUTED)
text(8, 1013, "HOW WE CHECKED: every story is dated to 22 November 2026 in at least one time zone; "
              "developing stories are labelled as reported, and what had not happened yet is listed "
              "in the DATE CHECK above.", SANS(9), MUTED)

img.save(OUT, optimize=True)
print("wrote", OUT, os.path.getsize(OUT), "bytes")
