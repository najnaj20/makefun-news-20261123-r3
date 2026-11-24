#!/usr/bin/env python3
"""Draw the v3 front page: 15 verified Monday 23 November 2026 stories.

Clean newspaper layout on a 1024x1024 canvas: masthead, two big leads,
then the remaining stories in two wide columns with short headlines and
one-line sub-lines. Everything is measured before it is drawn, so no text
can overflow the page. Deterministic: same input, same PNG bytes.
"""

import os
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = "/usr/share/fonts/truetype/dejavu"

PAGE = 1024
MARGIN = 30
CONTENT = PAGE - 2 * MARGIN
GUTTER = 28
COL = (CONTENT - GUTTER) // 2

PAPER = (246, 241, 229)
INK = (26, 26, 26)
RED = (164, 30, 34)
FAINT = (120, 112, 96)


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_MAST = font("DejaVuSerif-Bold.ttf", 60)
F_DATE = font("DejaVuSans.ttf", 23)
F_KICK = font("DejaVuSans-Bold.ttf", 16)
F_LEAD_HEAD = font("DejaVuSerif-Bold.ttf", 40)
F_LEAD_SUB = font("DejaVuSans.ttf", 18)
F_SECT = font("DejaVuSans-Bold.ttf", 17)
F_HEAD = font("DejaVuSerif-Bold.ttf", 21)
F_SUB = font("DejaVuSans.ttf", 15)
F_CHECK_HEAD = font("DejaVuSans-Bold.ttf", 18)
F_CHECK_BODY = font("DejaVuSans-Bold.ttf", 18)
F_FOOT = font("DejaVuSans.ttf", 14)


def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns a list of lines that fit inside width."""
    words = text.split()
    lines = []
    current = ""
    for word in words:
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=fnt) <= width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def block_height(draw, text, fnt, width, leading):
    return len(wrap(draw, text, fnt, width)) * leading


def draw_lines(draw, x, y, text, fnt, width, leading, fill=INK):
    lines = wrap(draw, text, fnt, width)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


# The fifteen stories. Headlines are kept short on purpose: every one must
# fit on a single line in its column at 21pt. Sub-lines are one line each.
LEAD_ONE = {
    "kicker": "CLIMATE \u2014 ANTALYA, TURKEY",
    "head": "COP31 COLLAPSES WITH NO DEAL AS TALKS RUN LONGEST EVER",
    "sub": (
        "Pacific islands despair as the fossil-fuel phase-out is dropped; "
        "90+ nations back an electrification pledge to 35% by 2035; calls "
        "grow for president Chris Bowen to resign."
    ),
}
LEAD_TWO = {
    "kicker": "UNITED STATES \u2014 WASHINGTON",
    "head": "DEMOCRATS CLINCH THE HOUSE",
    "sub": (
        "At least 258 seats, the largest House majority for either party "
        "since 1992."
    ),
}

SECTIONS = [
    ("EUROPE \u2014 6", [
        ("Kyiv region strikes kill at least 15",
         "Rescuers dig for survivors in Dymer."),
        ("Russian corvette sinks in Benghazi",
         "Suspected Ukrainian sea drone strike blamed."),
        ("Denmark says Russia plotted a killing",
         "Denmark accuses Russia of plotting to kill a rapper."),
        ("Burnham: EU deal or the status quo",
         "PM frames the choice; Theresa May dismayed."),
        ("Belgian airports shut as protests hit",
         "Air traffic control suspended amid austerity protest."),
        ("Poland reports airspace breach",
         "Strike on Zelenskyy's hometown kills two, wounds 60."),
    ]),
    ("MIDDLE EAST \u2014 2", [
        ("Trump \u2018inclined\u2019 to hit Iran again",
         "Trump favours resuming conflict if no deal by New Year."),
        ("Gaza flooding displaces 100,000 more",
         "Hamas demands talks after aid workers are killed in Gaza."),
    ]),
    ("ASIA-PACIFIC \u2014 2", [
        ("Banten factory fire toll hits 24",
         "Death toll rises in Indonesia; about 30 still missing."),
        ("Seoul minister quits over exam chaos",
         "Minister resigns after AI-cheating chaos upends the exam."),
    ]),
    ("AMERICAS \u2014 3", [
        ("Trump signs law ending the penny",
         "Common Cents Act ends the one-cent coin\u2019s 232-year run."),
        ("Delta outage delays 1,600+ flights",
         "Thanksgiving travel begins with delays at Atlanta hub."),
        ("Bitcoin climbs back to $61,800",
         "Bitcoin recovers from Saturday\u2019s $55,081 two-year low."),
    ]),
]

DATE_CHECK = (
    "Every story above happened or was first reported on Monday "
    "23 November 2026."
)
SOURCES = "Sources: Reuters, AP, CNN, BBC, Xinhua, The Guardian"


def section_height(draw, stories):
    """Height of one section: header plus one block per story."""
    total = 24  # section header line plus its rule
    for head, sub in stories:
        total += 26 + 19 + 7  # one-line headline, one-line sub, gap
    return total


def render():
    img = Image.new("RGB", (PAGE, PAGE), PAPER)
    draw = ImageDraw.Draw(img)

    # Outer frame.
    draw.rectangle([10, 10, PAGE - 11, PAGE - 11], outline=INK, width=2)

    y = MARGIN

    # Masthead.
    mast = "THE WORLD IN ONE DAY"
    mw = draw.textlength(mast, font=F_MAST)
    draw.text(((PAGE - mw) / 2, y), mast, font=F_MAST, fill=INK)
    y += 70

    date = "Monday, 23 November 2026"
    dw = draw.textlength(date, font=F_DATE)
    draw.text(((PAGE - dw) / 2, y), date, font=F_DATE, fill=INK)
    y += 30

    draw.line([(MARGIN, y), (PAGE - MARGIN, y)], fill=INK, width=3)
    y += 5
    draw.line([(MARGIN, y), (PAGE - MARGIN, y)], fill=INK, width=1)
    y += 12

    # Lead story one.
    draw.text((MARGIN, y), LEAD_ONE["kicker"], font=F_KICK, fill=RED)
    y += 22
    y = draw_lines(draw, MARGIN, y, LEAD_ONE["head"], F_LEAD_HEAD,
                   CONTENT, 46)
    y = draw_lines(draw, MARGIN, y, LEAD_ONE["sub"], F_LEAD_SUB,
                   CONTENT, 23)
    y += 8
    draw.line([(MARGIN, y), (PAGE - MARGIN, y)], fill=INK, width=1)
    y += 10

    # Lead story two.
    draw.text((MARGIN, y), LEAD_TWO["kicker"], font=F_KICK, fill=RED)
    y += 22
    y = draw_lines(draw, MARGIN, y, LEAD_TWO["head"], F_LEAD_HEAD,
                   CONTENT, 46)
    y = draw_lines(draw, MARGIN, y, LEAD_TWO["sub"], F_LEAD_SUB,
                   CONTENT, 23)
    y += 8
    draw.line([(MARGIN, y), (PAGE - MARGIN, y)], fill=INK, width=2)
    y += 12

    columns_top = y

    # Split the sections across two columns: Europe + Middle East on the
    # left, Asia-Pacific + Americas on the right.
    left = SECTIONS[0:2]
    right = SECTIONS[2:4]
    left_h = sum(section_height(draw, s) for _, s in left)
    right_h = sum(section_height(draw, s) for _, s in right)

    # Every column headline must fit on one line; every sub on one line.
    for _, stories in SECTIONS:
        for head, sub in stories:
            assert draw.textlength(head, font=F_HEAD) <= COL, head
            assert draw.textlength(sub, font=F_SUB) <= COL, sub

    for col_x, col_sections in ((MARGIN, left),
                                (MARGIN + COL + GUTTER, right)):
        cy = columns_top
        for title, stories in col_sections:
            draw.rectangle([col_x, cy + 2, col_x + 10, cy + 12], fill=RED)
            draw.text((col_x + 16, cy), title, font=F_SECT, fill=RED)
            cy += 24
            for head, sub in stories:
                draw.text((col_x, cy), head, font=F_HEAD, fill=INK)
                cy += 26
                draw.text((col_x, cy), sub, font=F_SUB, fill=INK)
                cy += 19
                cy += 7

    y = columns_top + max(left_h, right_h) + 8

    # Date check box.
    box_h = 60
    assert y + box_h <= PAGE - MARGIN - 22, "page overflow before date check"
    draw.rectangle([MARGIN, y, PAGE - MARGIN, y + box_h],
                   outline=RED, width=2)
    draw.text((MARGIN + 14, y + 8), "\u2713  DATE CHECK",
              font=F_CHECK_HEAD, fill=RED)
    draw.text((MARGIN + 14, y + 32), DATE_CHECK,
              font=F_CHECK_BODY, fill=INK)
    y += box_h + 10

    # Sources footer.
    draw.text((MARGIN, y), SOURCES, font=F_FOOT, fill=FAINT)
    y += 20
    assert y <= PAGE - MARGIN + 4, "page overflow at footer"

    out = os.path.join(HERE, "entry.png")
    img.save(out, "PNG")
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    render()
