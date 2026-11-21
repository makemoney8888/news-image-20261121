#!/usr/bin/env python3
"""Render the world-news infographic for Saturday, 21 November 2026.

Draws a single 1024x1024 PNG summarising the day's most consequential
stories, as reported on 21 November 2026. Pure Pillow, no network.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 24
GAP = 14

FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

NAVY = (15, 42, 74)
ORANGE = (232, 122, 26)
WHITE = (255, 255, 255)
INK = (24, 30, 38)
GREY = (88, 98, 110)
PANEL_BG = (246, 248, 250)
HERO_BG = (255, 241, 240)


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_width):
    """Greedy word wrap; returns a list of lines that fit max_width."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_tag(draw, x, y, label, color):
    """Small coloured category chip; returns its width."""
    f = font(FONT_BOLD, 15)
    tw = draw.textlength(label, font=f)
    pad_x, pad_y = 10, 5
    draw.rounded_rectangle([x, y, x + tw + 2 * pad_x, y + 24],
                           radius=6, fill=color)
    draw.text((x + pad_x, y + pad_y - 1), label, font=f, fill=WHITE)
    return tw + 2 * pad_x


def draw_panel(draw, box, tag, tag_color, headline, summary,
               headline_size=23, summary_size=18, bg=PANEL_BG):
    x0, y0, x1, y1 = box
    draw.rounded_rectangle(box, radius=10, fill=bg)
    draw.rectangle([x0, y0 + 10, x0 + 6, y1 - 10], fill=tag_color)
    px = x0 + 20
    py = y0 + 14
    draw_tag(draw, px, py, tag, tag_color)
    py += 24 + 10
    hf = font(FONT_BOLD, headline_size)
    lines = wrap(draw, headline, hf, x1 - px - 16)
    for line in lines:
        draw.text((px, py), line, font=hf, fill=INK)
        py += headline_size + 5
    py += 2
    sf = font(FONT_REG, summary_size)
    for line in wrap(draw, summary, sf, x1 - px - 16):
        draw.text((px, py), line, font=sf, fill=(52, 62, 74))
        py += summary_size + 5


def main():
    img = Image.new("RGB", (W, H), WHITE)
    draw = ImageDraw.Draw(img)

    # ---- Header band ----
    draw.rectangle([0, 0, W, 118], fill=NAVY)
    draw.rectangle([0, 118, W, 122], fill=ORANGE)
    draw.text((MARGIN, 18), "THE WORLD IN ONE DAY",
              font=font(FONT_BOLD, 42), fill=WHITE)
    draw.text((MARGIN, 70), "Saturday, 21 November 2026",
              font=font(FONT_BOLD, 30), fill=(255, 176, 92))

    # ---- Hero story: Russia's attack on Ukraine, missiles in Poland ----
    hero = (MARGIN, 136, W - MARGIN, 136 + 148)
    draw_panel(
        draw, hero, "CONFLICT  ·  UKRAINE & POLAND", (178, 34, 34),
        "Russia's biggest air attack in weeks hits Kyiv; missiles land in Poland",
        "400+ drones and 110 missiles hit Ukraine overnight, killing at least "
        "eight people in Kyiv. Two missiles and a suspected drone landed in "
        "Poland; PM Tusk called it a deliberate provocation.",
        headline_size=26, summary_size=19, bg=HERO_BG)

    # ---- Grid: six more stories, 2 columns x 3 rows ----
    col_w = (W - 2 * MARGIN - GAP) // 2
    row_h = 200
    gx, gy = MARGIN, 298
    stories = [
        ("JUSTICE  ·  THE HAGUE", (27, 94, 143),
         "UN court finds Myanmar guilty of genocide against the Rohingya",
         "The International Court of Justice ruled Myanmar committed genocide "
         "in 2017 \u2014 the first time it has held a state responsible. "
         "It ordered returns and reparations."),
        ("MARKETS  ·  NEW YORK", (140, 82, 8),
         "AI sell-off drags US stocks into correction",
         "The S&P 500 fell 3.7% and the Nasdaq 5.3% as AI and chip shares "
         "slumped. Nvidia dropped 13.8% amid reports of an SEC accounting "
         "inquiry."),
        ("POLITICS  ·  SHENZHEN", (90, 60, 140),
         "Trump defends ties to Putin and Xi after three-way summit",
         "After the first US\u2013China\u2013Russia leaders' meeting in "
         "Shenzhen, Trump gave a 90-minute press conference and called his "
         "talks with Putin \u201cvery good\u201d."),
        ("CLIMATE  ·  ANTALYA", (18, 122, 90),
         "COP31 talks run into overtime with no deal",
         "The climate summit missed its deadline after a draft deal dropped "
         "all mention of moving away from fossil fuels. Delegates kept "
         "negotiating into Saturday."),
        ("DISASTER  ·  PERU", (176, 96, 20),
         "Magnitude 6.7 earthquake shakes central Peru",
         "The quake struck near Jun\u00edn and was felt across Lima, sending "
         "residents into the streets. Early reports listed no deaths or "
         "major damage."),
        ("CULTURE  ·  GAMES", (150, 40, 120),
         "GTA VI takes a record $3.79 billion on its first day",
         "Rockstar said the game sold 32.5 million copies before launch \u2014 "
         "the biggest entertainment launch ever, nearly five times GTA V's "
         "first day."),
    ]
    for i, (tag, color, headline, summary) in enumerate(stories):
        col, row = i % 2, i // 2
        x0 = gx + col * (col_w + GAP)
        y0 = gy + row * (row_h + GAP)
        draw_panel(draw, (x0, y0, x0 + col_w, y0 + row_h),
                   tag, color, headline, summary)

    # ---- Footer: sources ----
    footer = ("Sources: Reuters, AP, BBC, AFP, The Daily Star  ·  "
              "Events reported on Saturday, 21 November 2026")
    ff = font(FONT_REG, 15)
    fw = draw.textlength(footer, font=ff)
    draw.text(((W - fw) / 2, 952), footer, font=ff, fill=GREY)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
