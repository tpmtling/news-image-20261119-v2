"""Newspaper front page for Thursday 19 November 2026.

One 1024x1024 image that sums up the day's world news, styled as a
classic broadsheet front page. Deterministic: fixed layout and fonts,
no timestamps, no randomness.
"""
from PIL import Image, ImageDraw, ImageFont

W = 1024
H = 1024

PAPER = (247, 242, 231)
INK = (26, 23, 16)
SOFT = (84, 78, 64)
FAINT = (150, 142, 122)
RED = (179, 32, 42)
RULE = (26, 23, 16)

SANS = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/noto/NotoSerif-Regular.ttf"
SERIF_B = "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf"
SERIF_K = "/usr/share/fonts/truetype/noto/NotoSerif-Black.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines = []
    cur = ""
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


def draw_wrapped(draw, xy, text, fnt, fill, max_w, leading):
    x, y = xy
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def centered(draw, y, text, fnt, fill):
    w = draw.textlength(text, font=fnt)
    draw.text(((W - w) / 2, y), text, font=fnt, fill=fill)
    return y + fnt.size + 8


LEAD_HEAD = "Trump, Xi and Putin sit down together for the first time"
LEAD_BODY = (
    "SHENZHEN - The leaders of the United States, China and Russia held "
    "their first-ever three-way summit on Thursday, on the sidelines of "
    "the APEC gathering in Shenzhen. Nuclear arms control, the wars in "
    "Ukraine and Iran and energy stability were on the table. Officials "
    "played down any breakthrough, but the handshake alone drew "
    "comparisons with Yalta."
)

LEFT = [
    {
        "kicker": "STRAIT OF HORMUZ",
        "title": "Three oil tankers catch fire after hitting mines",
        "body": (
            "Iran said three tankers caught fire after striking mines "
            "east of Hormuz, a day after US strikes on Qeshm Island "
            "and drone attacks across the Gulf."
        ),
    },
    {
        "kicker": "GAZA",
        "title": "Israel launches rare ground operation in central Gaza",
        "body": (
            "Israeli tanks advanced beyond the Yellow Line into "
            "central Gaza as dozens of families fled, while four "
            "nations urged Israel to let aid reach the enclave."
        ),
    },
]

RIGHT = [
    {
        "kicker": "ART MARKET",
        "title": "Van Gogh sells for a record $190.4 million",
        "body": (
            "A Van Gogh sold for $190.4 million, a record for the "
            "artist, after a public dispute over its Nazi-era "
            "history was resolved."
        ),
    },
    {
        "kicker": "CULTURE & GAMES",
        "title": "GTA VI launches worldwide to near-perfect reviews",
        "body": (
            "Gamers finally entered the new Vice City as Grand Theft "
            "Auto VI began its global rollout to near-perfect "
            "review scores."
        ),
    },
]

BRIEFS = [
    "World Court to rule on Myanmar's alleged Rohingya genocide",
    "Governments warn an AI-found Java flaw leaves systems open to hackers",
    "EU proposes a 45 billion euro Ukraine loan, repaid from reparations",
    "Anthropic poised for a stock market debut valuing it above $1.4 trillion",
]


def story(draw, x, y, col_w, item):
    draw.text((x, y), item["kicker"], font=font(SANS_B, 15), fill=RED)
    y += 22
    y = draw_wrapped(draw, (x, y), item["title"], font(SERIF_B, 24), INK, col_w, 30)
    y += 3
    y = draw_wrapped(draw, (x, y), item["body"], font(SERIF, 17), SOFT, col_w, 24)
    return y


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    margin = 54

    # masthead
    centered(d, 28, "THE WORLD TODAY", font(SERIF_K, 64), INK)
    d.line([(margin, 110), (W - margin, 110)], fill=RULE, width=5)
    d.line([(margin, 119), (W - margin, 119)], fill=RULE, width=1)
    dateline = "Thursday, November 19, 2026  -  World Edition  -  One image, the whole day"
    centered(d, 128, dateline, font(SANS, 17), SOFT)
    d.line([(margin, 162), (W - margin, 162)], fill=RULE, width=1)

    # lead story
    y = 176
    d.text((margin, y), "APEC SUMMIT  -  SHENZHEN", font=font(SANS_B, 17), fill=RED)
    y += 27
    y = draw_wrapped(d, (margin, y), LEAD_HEAD, font(SERIF_K, 46), INK, W - 2 * margin, 55)
    y += 6
    y = draw_wrapped(d, (margin, y), LEAD_BODY, font(SERIF, 19), SOFT, W - 2 * margin, 27)
    y += 14
    d.line([(margin, y), (W - margin, y)], fill=RED, width=3)
    y += 20

    # two columns
    gap = 36
    col_w = (W - 2 * margin - gap) // 2
    left_x = margin
    right_x = margin + col_w + gap
    top = y
    ly = top
    for i, item in enumerate(LEFT):
        ly = story(d, left_x, ly, col_w, item)
        ly += 12
        if i == 0:
            d.line([(left_x, ly), (left_x + col_w, ly)], fill=FAINT, width=1)
            ly += 14
    ry = top
    for i, item in enumerate(RIGHT):
        ry = story(d, right_x, ry, col_w, item)
        ry += 12
        if i == 0:
            d.line([(right_x, ry), (right_x + col_w, ry)], fill=FAINT, width=1)
            ry += 14
    # vertical divider between the columns
    div_x = margin + col_w + gap // 2
    d.line([(div_x, top), (div_x, max(ly, ry))], fill=FAINT, width=1)
    y = max(ly, ry) + 2

    # briefs strip
    d.line([(margin, y), (W - margin, y)], fill=RULE, width=3)
    y += 10
    d.text((margin, y), "IN BRIEF", font=font(SANS_B, 17), fill=RED)
    y += 24
    for brief in BRIEFS:
        d.rectangle([margin + 4, y + 7, margin + 12, y + 15], fill=RED)
        y = draw_wrapped(d, (margin + 30, y), brief, font(SERIF, 18), INK, W - 2 * margin - 30, 24)
        y += 2

    # footer
    d.line([(margin, H - 46), (W - margin, H - 46)], fill=RULE, width=1)
    centered(d, H - 36, "THE WORLD TODAY  -  Thursday, November 19, 2026", font(SANS, 15), SOFT)

    img.save("news_image.png", format="PNG", optimize=False)
    print("saved news_image.png", img.size)


if __name__ == "__main__":
    main()
