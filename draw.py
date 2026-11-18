#!/usr/bin/env python3
"""Render the front page for Wednesday 18 November 2026.

Draws a newspaper front page with six real stories first reported on
18 November 2026, using Pillow. All artwork is simple geometric shapes.
Output: entry.png, 1024x1024, well under 1 MiB.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
PAPER = (248, 243, 230)
INK = (26, 26, 26)
RED = (176, 42, 42)
BLUE = (31, 78, 121)
TEAL = (14, 110, 110)
GOLD = (176, 132, 24)
GREEN = (34, 120, 60)
GREY = (90, 88, 80)
PANEL = (255, 253, 246)
LINE = (60, 58, 50)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Wrap text into lines that fit max_w pixels."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, fnt, max_w, fill=INK, leading=None):
    lines = wrap(draw, text, fnt, max_w)
    lh = leading or int(fnt.size * 1.25)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


# ---------------- pictograms (geometric shapes only) ----------------

def pic_globe(d, x, y, s):
    """Globe with four Quad dots around it."""
    cx, cy, r = x + s // 2, y + s // 2, s // 2 - 4
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=BLUE, width=4)
    d.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r], outline=BLUE, width=3)
    d.line([cx - r, cy, cx + r, cy], fill=BLUE, width=3)
    d.arc([cx - r, cy - r // 2, cx + r, cy + r // 2], 0, 180, fill=BLUE, width=3)
    d.arc([cx - r, cy - r // 2, cx + r, cy + r // 2], 180, 360, fill=BLUE, width=3)
    for dx, dy, col in [(-r - 14, -r - 6, RED), (r + 8, -r - 6, GOLD),
                        (-r - 14, r - 4, GREEN), (r + 8, r - 4, TEAL)]:
        d.ellipse([cx + dx, cy + dy, cx + dx + 16, cy + dy + 16], fill=col)


def pic_bridge(d, x, y, s):
    """Bridge deck with a burst at the break, waves below."""
    w = s
    d.rectangle([x, y + s // 2, x + w, y + s // 2 + 12], fill=INK)
    for px in (x + 8, x + w // 2 - 6, x + w - 20):
        d.rectangle([px, y + s // 2 + 12, px + 12, y + s - 26], fill=INK)
    d.arc([x + 6, y + 4, x + w - 6, y + s // 2 + 10], 180, 360, fill=RED, width=4)
    cx, cy = x + w // 2, y + s // 2
    for ang in range(0, 360, 45):
        import math
        x2 = cx + int(26 * math.cos(math.radians(ang)))
        y2 = cy + int(26 * math.sin(math.radians(ang)))
        d.line([cx, cy, x2, y2], fill=RED, width=4)
    d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=RED)
    for wy in (y + s - 18, y + s - 8):
        for wx in range(x, x + w - 24, 48):
            d.arc([wx, wy, wx + 28, wy + 12], 180, 360, fill=BLUE, width=3)


def pic_cyclone(d, x, y, s):
    """Spiral storm with rain lines."""
    cx, cy = x + s // 2, y + s // 2
    for k, r in enumerate((14, 26, 38, 50)):
        d.arc([cx - r, cy - r, cx + r, cy + r], k * 40, k * 40 + 270,
              fill=TEAL if k % 2 == 0 else BLUE, width=5)
    d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=RED)
    for rx in (x + 6, x + s // 3, x + 2 * s // 3, x + s - 12):
        d.line([rx, y + s - 22, rx - 6, y + s - 6], fill=BLUE, width=3)


def pic_parliament(d, x, y, s):
    """Classical parliament building: pediment, columns, steps."""
    w = s
    d.polygon([(x + 8, y + 34), (x + w // 2, y + 6), (x + w - 8, y + 34)],
              fill=BLUE)
    d.rectangle([x + 8, y + 34, x + w - 8, y + 44], fill=BLUE)
    for i in range(4):
        cx0 = x + 22 + i * (w - 44) // 3
        d.rectangle([cx0, y + 48, cx0 + 12, y + s - 26], fill=INK)
    d.rectangle([x + 4, y + s - 26, x + w - 4, y + s - 18], fill=INK)
    d.rectangle([x, y + s - 16, x + w, y + s - 8], fill=INK)


def pic_chip(d, x, y, s):
    """Microchip with a rising arrow."""
    d.rectangle([x + 18, y + 18, x + s - 18, y + s - 18],
                outline=INK, width=5)
    d.rectangle([x + s // 2 - 16, y + s // 2 - 16, x + s // 2 + 16,
                 y + s // 2 + 16], fill=GREEN)
    for i in range(4):
        px = x + 30 + i * (s - 60) // 3
        py = y + 30 + i * (s - 60) // 3
        d.line([px, y + 6, px, y + 18], fill=INK, width=4)
        d.line([px, y + s - 18, px, y + s - 6], fill=INK, width=4)
        d.line([x + 6, py, x + 18, py], fill=INK, width=4)
        d.line([x + s - 18, py, x + s - 6, py], fill=INK, width=4)
    d.line([x + 16, y + s - 30, x + s // 2, y + 26], fill=RED, width=6)
    d.line([x + s // 2, y + 26, x + s - 16, y + 40], fill=RED, width=6)
    d.polygon([(x + s // 2 - 12, y + 22), (x + s // 2 + 12, y + 22),
               (x + s // 2, y + 6)], fill=RED)


def pic_cricket(d, x, y, s):
    """Cricket bat, ball and stumps."""
    d.line([x + s // 2 - 26, y + 14, x + s // 2 + 26, y + s - 34],
           fill=(150, 110, 60), width=16)
    d.line([x + s // 2 + 26, y + s - 34, x + s // 2 + 44, y + s - 12],
           fill=(150, 110, 60), width=10)
    d.ellipse([x + 12, y + s - 40, x + 40, y + s - 12], fill=RED)
    for i in range(3):
        sx = x + s - 34 - i * 14
        d.line([sx, y + 12, sx, y + 46], fill=GOLD, width=5)
    d.line([x + s - 62, y + 10, x + s - 20, y + 10], fill=GOLD, width=4)


PICS = {"globe": pic_globe, "bridge": pic_bridge, "cyclone": pic_cyclone,
        "parliament": pic_parliament, "chip": pic_chip,
        "cricket": pic_cricket}


# ---------------- page ----------------

def panel(d, x, y, w, h, kicker, headline, summary, pic, pic_side=True,
          head_size=30, sum_size=20):
    d.rectangle([x, y, x + w, y + h], fill=PANEL, outline=LINE, width=2)
    if pic_side:
        pw = int(w * 0.30)
        tx, tw = x + 16, w - pw - 32
        PICS[pic](d, x + w - pw + 4, y + 18, 96)
    else:
        tx, tw = x + 16, w - 32
        PICS[pic](d, x + (w - 84) // 2, y + 12, 84)
        y += 104
        h -= 104
    cy = y + 14
    d.text((tx, cy), kicker, font=font(SANS_B, 16), fill=RED)
    cy += 26
    cy = draw_wrapped(d, tx, cy, headline, font(SERIF_B, head_size), tw,
                      leading=int(head_size * 1.12))
    cy += 8
    draw_wrapped(d, tx, cy, summary, font(SANS, sum_size), tw,
                 leading=int(sum_size * 1.3))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([6, 6, W - 7, H - 7], outline=INK, width=3)

    # Masthead
    d.line([24, 18, W - 24, 18], fill=RED, width=4)
    d.text((W // 2, 30), "THE WORLD TODAY", font=font(SERIF_B, 62),
           fill=INK, anchor="ma")
    d.line([24, 112, W - 24, 112], fill=RED, width=4)
    d.text((W // 2, 122), "WEDNESDAY  18  NOVEMBER  2026",
           font=font(SANS_B, 30), fill=RED, anchor="ma")
    d.text((W // 2, 158), "ONE DAY  •  SIX STORIES  •  FROM AROUND THE WORLD",
           font=font(SANS, 17), fill=GREY, anchor="ma")

    # Lead story: Trump in Manila
    d.rectangle([24, 196, W - 24, 428], fill=PANEL, outline=LINE, width=2)
    d.text((48, 212), "ASIA-PACIFIC  •  DIPLOMACY", font=font(SANS_B, 18),
           fill=RED)
    end_y = draw_wrapped(d, 48, 240, "TRUMP IN MANILA FOR QUAD TALKS",
                         font(SERIF_B, 40), 600, leading=46)
    draw_wrapped(d, 48, end_y + 12,
                 "The US president opens his Asia trip with Quad allies, "
                 "ahead of a visit to China.",
                 font(SANS, 24), 600, leading=31)
    pic_globe(d, 710, 216, 200)

    # Row 2: Ukraine bridge, Cyclone Akvan
    panel(d, 24, 444, 476, 236, "EUROPE  •  WAR",
          "UKRAINE HITS CRIMEA BRIDGE AGAIN",
          "Kyiv strikes the bridge for a second day as Russia pounds "
          "bridges in Kyiv.", "bridge", head_size=27, sum_size=19)
    panel(d, 524, 444, 476, 236, "WEATHER  •  SOUTH ASIA",
          "CYCLONE AKVAN STRENGTHENS",
          "Storm over the Bay of Bengal set to turn severe; flights "
          "cancelled.", "cyclone", head_size=27,
          sum_size=19)

    # Row 3: Israel speaker, Nvidia, Dhoni
    panel(d, 24, 696, 317, 288, "MIDDLE EAST  •  POLITICS",
          "ISRAEL ELECTS NEW SPEAKER",
          "Knesset picks Matan Kahana, an ally of Eisenkot, in a blow to "
          "Netanyahu.", "parliament", pic_side=False, head_size=27,
          sum_size=19)
    panel(d, 353, 696, 317, 288, "BUSINESS  •  TECH",
          "NVIDIA BEATS FORECASTS",
          "Chip giant tops expectations and its shares climb.",
          "chip", pic_side=False, head_size=27, sum_size=19)
    panel(d, 683, 696, 317, 288, "SPORT  •  CRICKET",
          "DHONI ENDS IPL CAREER",
          "MS Dhoni retires from playing; Chennai name him team mentor.",
          "cricket", pic_side=False, head_size=27, sum_size=19)

    d.text((W // 2, 992),
           "All six stories first reported on 18 November 2026.",
           font=font(SANS, 15), fill=GREY, anchor="ma")

    img.save(OUT, "PNG", optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
