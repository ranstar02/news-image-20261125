#!/usr/bin/env python3
"""Draw the 25 November 2026 world-news front page (1024x1024, Pillow only).

Every pictogram is drawn from basic shapes in this file. No photo, logo or
outside image is used. Run:  python3 draw.py [output-path]
"""
import sys
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (246, 241, 227)
INK = (18, 18, 18)
NAVY = (20, 38, 74)
GOLD = (212, 175, 55)
RED = (178, 34, 34)
TEAL = (14, 110, 110)
SKY = (135, 190, 220)
SEA = (38, 90, 140)

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, text, fnt, color, max_w, leading=None):
    lh = leading or int(fnt.size * 1.22)
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=color)
        y += lh
    return y


def flame(draw, cx, cy, s):
    pts = [(cx, cy - s), (cx + s * 0.55, cy - s * 0.2), (cx + s * 0.4, cy + s * 0.25),
           (cx + s * 0.75, cy + s * 0.1), (cx + s * 0.3, cy + s * 0.8),
           (cx, cy + s * 0.45), (cx - s * 0.3, cy + s * 0.8),
           (cx - s * 0.75, cy + s * 0.1), (cx - s * 0.4, cy + s * 0.25),
           (cx - s * 0.55, cy - s * 0.2)]
    draw.polygon(pts, fill=(235, 90, 20))
    draw.ellipse([cx - s * 0.22, cy - s * 0.1, cx + s * 0.22, cy + s * 0.55],
                 fill=(250, 200, 40))


def draw_awacs(draw, x, y, w, h):
    # sky panel; plane sized to stay inside the w x h box
    draw.rectangle([x, y, x + w, y + h], fill=SKY)
    draw.ellipse([x + 14, y + 10, x + 66, y + 40], fill=(255, 255, 255))
    draw.ellipse([x + 46, y + 22, x + 104, y + 48], fill=(255, 255, 255))
    cx, cy = x + w // 2, y + h // 2 + 12
    # tail fin + fuselage
    draw.polygon([(cx - 108, cy + 4), (cx - 92, cy - 34), (cx - 74, cy - 34),
                  (cx - 66, cy + 2)], fill=(200, 205, 210))
    draw.ellipse([cx - 112, cy - 12, cx + 112, cy + 14], fill=(235, 238, 240))
    draw.ellipse([cx - 112, cy - 12, cx + 112, cy + 14], outline=INK, width=3)
    # radar dome on a stalk
    draw.rectangle([cx - 6, cy - 44, cx + 6, cy - 12], fill=INK)
    draw.ellipse([cx - 42, cy - 66, cx + 42, cy - 36], fill=(250, 250, 250),
                 outline=INK, width=3)
    draw.arc([cx - 58, cy - 78, cx + 58, cy - 24], 200, 340, fill=RED, width=3)
    # windows + wings
    for i in range(4):
        draw.ellipse([cx - 66 + i * 24, cy - 5, cx - 54 + i * 24, cy + 5],
                     fill=NAVY)
    draw.polygon([(cx - 20, cy + 6), (cx + 20, cy + 6), (cx + 52, cy + 40),
                  (cx + 26, cy + 40)], fill=(180, 186, 192), outline=INK)
    draw.polygon([(cx - 28, cy - 4), (cx + 8, cy - 4), (cx + 30, cy - 32),
                  (cx + 8, cy - 32)], fill=(180, 186, 192), outline=INK)
    # ground + missile markers
    draw.rectangle([x, y + h - 20, x + w, y + h], fill=(90, 140, 70))
    for mx in (x + 26, x + w - 52):
        draw.polygon([(mx, y + h - 44), (mx + 6, y + h - 30), (mx + 12, y + h - 44)],
                     fill=RED)
        draw.rectangle([mx + 3, y + h - 30, mx + 9, y + h - 20], fill=RED)


def draw_tanker(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(255, 214, 150))
    draw.ellipse([x + 20, y + 16, x + 70, y + 44], fill=(255, 240, 200))
    # sea
    draw.rectangle([x, y + h - 40, x + w, y + h], fill=SEA)
    draw.arc([x + 10, y + h - 34, x + 90, y + h - 10], 0, 180, fill=(255, 255, 255), width=3)
    draw.arc([x + w - 100, y + h - 34, x + w - 20, y + h - 10], 0, 180,
             fill=(255, 255, 255), width=3)
    # hull + containers
    hx, hy = x + 30, y + h - 72
    draw.polygon([(hx, hy), (hx + w - 60, hy), (hx + w - 84, hy + 34),
                  (hx + 24, hy + 34)], fill=(150, 40, 40), outline=INK, width=3)
    for i, c in enumerate([(40, 90, 160), (220, 160, 40), (40, 140, 90)]):
        draw.rectangle([hx + 22 + i * 62, hy - 26, hx + 76 + i * 62, hy - 2],
                       fill=c, outline=INK, width=2)
    draw.rectangle([hx + w - 92, hy - 38, hx + w - 62, hy - 2], fill=(240, 240, 240),
                   outline=INK, width=2)
    # spiky mine + flame above the deck
    mx, my = x + w - 52, y + 36
    for a in range(0, 360, 45):
        import math
        dx, dy = math.cos(math.radians(a)), math.sin(math.radians(a))
        draw.line([mx + dx * 14, my + dy * 14, mx + dx * 26, my + dy * 26],
                  fill=INK, width=4)
    draw.ellipse([mx - 15, my - 15, mx + 15, my + 15], fill=INK)
    flame(draw, x + 62, y + h - 48, 16)


def draw_laptop_lock(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(220, 228, 235))
    # laptop
    draw.rectangle([x + 28, y + 34, x + w - 28, y + h - 52], fill=NAVY, outline=INK, width=3)
    draw.rectangle([x + 38, y + 44, x + w - 38, y + h - 62], fill=(170, 210, 235))
    draw.polygon([(x + 16, y + h - 52), (x + w - 16, y + h - 52), (x + w - 4, y + h - 34),
                  (x + 4, y + h - 34)], fill=(120, 130, 140), outline=INK, width=2)
    # padlock on the screen
    cx, cy = x + w // 2, y + h // 2 - 6
    draw.arc([cx - 22, cy - 34, cx + 22, cy + 2], 180, 360, fill=RED, width=7)
    draw.rounded_rectangle([cx - 30, cy - 6, cx + 30, cy + 34], 6, fill=RED, outline=INK, width=2)
    draw.ellipse([cx - 6, cy + 6, cx + 6, cy + 18], fill=(255, 255, 255))
    draw.rectangle([cx - 2, cy + 14, cx + 2, cy + 26], fill=(255, 255, 255))


def draw_gavel(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(232, 222, 200))
    # phone body
    draw.rounded_rectangle([x + 18, y + 22, x + 78, y + h - 22], 8, fill=(30, 30, 30))
    draw.rectangle([x + 26, y + 34, x + 70, y + h - 44], fill=(90, 170, 220))
    draw.ellipse([x + 42, y + h - 36, x + 54, y + h - 24], fill=(200, 200, 200))
    # gavel head + handle, diagonal, kept inside the box
    draw.polygon([(x + 96, y + 28), (x + 156, y + 62), (x + 144, y + 80),
                  (x + 84, y + 46)], fill=(120, 72, 20), outline=INK, width=2)
    draw.polygon([(x + 104, y + 58), (x + 142, y + 82), (x + 132, y + 94),
                  (x + 94, y + 70)], fill=(90, 52, 14), outline=INK, width=2)
    draw.line([x + 112, y + 76, x + 152, y + 104], fill=(120, 72, 20), width=8)
    # sound block
    draw.rectangle([x + 96, y + h - 22, x + 176, y + h - 10], fill=(150, 110, 60),
                   outline=INK, width=2)


def draw_tower(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(250, 210, 140))
    draw.ellipse([x + 16, y + 14, x + 66, y + 44], fill=(255, 240, 190))
    # skyscraper
    tx = x + w // 2 - 42
    draw.rectangle([tx, y + 26, tx + 84, y + h - 14], fill=(70, 90, 120), outline=INK, width=3)
    draw.polygon([(tx, y + 26), (tx + 42, y + 6), (tx + 84, y + 26)], fill=(50, 68, 92))
    for r in range(4):
        for c in range(3):
            draw.rectangle([tx + 10 + c * 26, y + 42 + r * 17, tx + 26 + c * 26,
                            y + 54 + r * 17], fill=(255, 220, 90))
    # blast + drone
    flame(draw, tx + 96, y + 52, 22)
    dx, dy = x + 34, y + 44
    draw.ellipse([dx - 12, dy - 7, dx + 12, dy + 7], fill=INK)
    for ox, oy in ((-20, -12), (20, -12), (-20, 12), (20, 12)):
        draw.line([dx + ox * 0.5, dy + oy * 0.5, dx + ox, dy + oy], fill=INK, width=2)
        draw.ellipse([dx + ox - 9, dy + oy - 3, dx + ox + 9, dy + oy + 3],
                     fill=(200, 200, 200), outline=INK, width=1)


def draw_ballot(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(215, 235, 215))
    # two flags shaking hands: simplified as two joined banners + ballot box
    draw.polygon([(x + 30, y + 8), (x + 96, y + 8), (x + 96, y + 36),
                  (x + 30, y + 36)], fill=(255, 140, 40), outline=INK, width=2)
    draw.polygon([(x + 108, y + 8), (x + 174, y + 8), (x + 174, y + 36),
                  (x + 108, y + 36)], fill=(40, 120, 200), outline=INK, width=2)
    draw.line([x + 96, y + 22, x + 108, y + 22], fill=INK, width=4)
    draw.ellipse([x + 94, y + 14, x + 110, y + 30], fill=GOLD, outline=INK, width=2)
    # ballot box
    bx, by = x + w // 2 - 52, y + h - 58
    draw.rectangle([bx, by, bx + 104, by + 52], fill=(240, 240, 240), outline=INK, width=3)
    draw.rectangle([bx - 8, by - 12, bx + 112, by + 2], fill=NAVY)
    draw.rectangle([bx + 38, by - 8, bx + 66, by - 2], fill=(255, 255, 255))
    f = font(BOLD, 30)
    draw.text((bx + 34, by + 12), "117", font=f, fill=NAVY)


def card(draw, x, y, w, h, tag, title, sub, pict):
    draw.rectangle([x, y, x + w, y + h], fill=(255, 255, 255), outline=INK, width=3)
    draw.rectangle([x, y, x + w, y + 30], fill=NAVY)
    draw.text((x + 10, y + 4), tag, font=font(BOLD, 19), fill=(255, 255, 255))
    px, py, pw, ph = x + 12, y + 42, 196, h - 54
    pict(draw, px, py, pw, ph)
    draw.rectangle([px, py, px + pw, py + ph], outline=INK, width=2)
    tx = x + 220
    text_block(draw, tx, y + 44, title, font(BOLD, 23), INK, w - 234, leading=28)
    lines = wrap(draw, sub, font(REG, 16), w - 234)[:3]
    yy = y + 104
    for line in lines:
        draw.text((tx, yy), line, font=font(REG, 16), fill=(60, 60, 60))
        yy += 20


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([4, 4, W - 5, H - 5], outline=INK, width=5)

    # ---- masthead ----
    d.rectangle([12, 12, W - 13, 158], fill=NAVY)
    d.text((512, 22), "THE WORLD TODAY", font=font(BOLD, 74),
           fill=(255, 255, 255), anchor="ma")
    d.text((512, 104), "Wednesday, 25 November 2026", font=font(BOLD, 38),
           fill=GOLD, anchor="ma")

    # ---- lead stories ----
    ly, lh = 172, 300
    # NATO / AWACS (left, big)
    d.rectangle([16, ly, 616, ly + lh], fill=(255, 255, 255), outline=INK, width=3)
    d.rectangle([16, ly, 616, ly + 34], fill=RED)
    d.text((28, ly + 5), "LEAD  •  EUROPE", font=font(BOLD, 20), fill=(255, 255, 255))
    draw_awacs(d, 28, ly + 46, 250, 150)
    d.rectangle([28, ly + 46, 278, ly + 196], outline=INK, width=2)
    text_block(d, 292, ly + 46, "NATO SENDS AWACS TO POLAND",
               font(BOLD, 33), INK, 312, leading=38)
    text_block(d, 292, ly + 168,
               "After three Russian missiles landed in Poland, the alliance steps up radar watch on its eastern flank.",
               font(REG, 19), (60, 60, 60), 312, leading=24)
    d.text((28, ly + 268), "Missiles fell on 20 Nov; NATO approved the deployment on 23 Nov.",
           font=font(REG, 15), fill=(90, 90, 90))
    # Hormuz (right)
    d.rectangle([632, ly, 1008, ly + lh], fill=(255, 255, 255), outline=INK, width=3)
    d.rectangle([632, ly, 1008, ly + 34], fill=TEAL)
    d.text((644, ly + 5), "MIDDLE EAST", font=font(BOLD, 20), fill=(255, 255, 255))
    draw_tanker(d, 644, ly + 46, 352, 118)
    d.rectangle([644, ly + 46, 996, ly + 164], outline=INK, width=2)
    text_block(d, 644, ly + 178, "IRAN CLAIMS 3 TANKERS HIT MINES",
               font(BOLD, 26), INK, 352, leading=30)
    text_block(d, 644, ly + 246,
               "IRGC says 3 ships caught fire in the Strait of Hormuz; claim unverified.",
               font(REG, 17), (60, 60, 60), 352, leading=21)

    # ---- four-card grid ----
    gy, gh, gap = 488, 164, 12
    cw = (1008 - 16 - gap) // 2
    card(d, 16, gy, cw, gh, "USA  •  CYBER",
         "CIA AND ODNI HIT BY HACK",
         "Unclassified open-source network breached; officials say no classified data was hit.",
         draw_laptop_lock)
    card(d, 16 + cw + gap, gy, cw, gh, "USA  •  COURTS",
         "HUAWEI GUILTY ON 10 COUNTS",
         "Brooklyn jury convicts the Chinese tech giant over Iran business and trade secrets.",
         draw_gavel)
    card(d, 16, gy + gh + gap, cw, gh, "MIDDLE EAST",
         "HOUTHI DRONE HITS RIYADH",
         "Second strike in a week on the PIF tower wounds 11 people, Saudi officials say.",
         draw_tower)
    card(d, 16 + cw + gap, gy + gh + gap, cw, gh, "INDIA  •  POLITICS",
         "BJP AND AKALI DAL REUNITE",
         "Old allies join forces for the 2027 Punjab polls; Akali Dal named senior partner.",
         draw_ballot)

    # ---- footer: also today ----
    fy = 828
    d.rectangle([16, fy, 1008, 1008], fill=NAVY)
    d.text((28, fy + 10), "ALSO TODAY", font=font(BOLD, 24), fill=GOLD)
    items = [
        ("UKRAINE", "Zelensky confirms Kyiv hit the Russian cargo ship Sparta II in the Gulf of Finland."),
        ("USA", "Trump awards the Medal of Freedom to former New York mayor Rudy Giuliani."),
        ("SPORT", "England crush Australia by 8 wickets in the 2nd T20I; Donald hits 85, series 1-1."),
        ("AFRICA", "WHO evacuates Ebola staff from a hospital in DR Congo after days of fighting."),
    ]
    f_tag, f_txt = font(BOLD, 17), font(REG, 17)
    for i, (tag, txt) in enumerate(items):
        x = 28 + (i % 2) * 496
        y = fy + 48 + (i // 2) * 52
        d.text((x, y), tag + " — ", font=f_tag, fill=GOLD)
        tw = d.textlength(tag + " — ", font=f_tag)
        for line in wrap(d, txt, f_txt, 480 - tw)[:2]:
            d.text((x + tw, y), line, font=f_txt, fill=(255, 255, 255))
            y += 21
    d.line([16, 984, 1008, 984], fill=(120, 130, 150), width=1)
    d.text((512, 990), "Sources: Reuters, AP, CNN, The New York Times  •  All stories reported 24–25 November 2026",
           font=font(REG, 14), fill=(180, 185, 195), anchor="ma")

    img.save(out, "PNG", optimize=True)
    print(f"wrote {out} ({img.size[0]}x{img.size[1]})")


if __name__ == "__main__":
    main()
