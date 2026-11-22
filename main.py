#!/usr/bin/env python3
"""Sum up 21 November 2026's world news in one image.

Pure Python 3.13 standard library only. No network, no randomness,
no clock: every run writes exactly the same bytes to entry.png.

The picture is a newspaper front page for Saturday 21 November 2026.
Six main stories, each cross-checked in that day's reporting:

  1. Iran struck U.S. bases in Bahrain; Tehran sought diplomacy to
     end the war while President Trump called its terms unacceptable.
  2. A Russian ballistic missile hit Kryvyi Rih, Ukraine, killing
     two people and wounding dozens.
  3. Mexican special forces captured FBI most-wanted cartel boss
     Fausto Isidro Meza Flores ("El Chapo Isidro") in Sinaloa;
     violence after the raid left at least 11 dead.
  4. The COP31 climate talks in Antalya, Turkey, ran into overtime
     with nations split over fossil fuels and finance.
  5. An AI and chip sell-off pushed U.S. stocks into a slide, and
     Nvidia's accounting faced an SEC investigation.
  6. An Anthropic researcher claimed Claude had solved maths'
     greatest riddle.

Ticker stories: FBI and U.S. Agriculture Department databases were
breached by hackers; countries opened a path towards a "killer
robots" pact; BepiColombo arrived at Mercury; mosquitoes carrying a
bacterium cut dengue cases among children in Brazil.
"""

import os
import struct
import zlib

WIDTH = 1024
HEIGHT = 1024

# ---------------------------------------------------------------- palette
PAPER = (247, 242, 231)
INK = (20, 33, 61)
RED = (193, 39, 45)
BLUE = (36, 84, 160)
TEAL = (18, 128, 116)
ORANGE = (222, 125, 28)
PURPLE = (98, 62, 168)
GREEN = (46, 125, 50)
CARD = (255, 253, 247)
GREY = (92, 96, 110)
LIGHT = (228, 221, 203)

# ---------------------------------------------------------------- 5x7 font
# Each glyph is 7 rows of 5 pixels, written as strings of "0"/"1".
FONT = {
    "A": ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    "B": ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    "C": ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    "D": ("11100", "10010", "10001", "10001", "10001", "10010", "11100"),
    "E": ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    "F": ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    "G": ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
    "H": ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    "I": ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    "J": ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    "K": ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    "L": ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    "M": ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    "N": ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    "O": ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    "P": ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    "Q": ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    "R": ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    "S": ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    "T": ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    "U": ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    "V": ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    "W": ("10001", "10001", "10001", "10101", "10101", "10101", "01010"),
    "X": ("10001", "01010", "00100", "00100", "01010", "10001", "10001"),
    "Y": ("10001", "01010", "00100", "00100", "00100", "00100", "00100"),
    "Z": ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    "0": ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    "1": ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    "2": ("01110", "10001", "00001", "00110", "01000", "10000", "11111"),
    "3": ("11111", "00010", "00100", "00010", "00001", "10001", "01110"),
    "4": ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    "5": ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    "6": ("00110", "01000", "10000", "11110", "10001", "10001", "01110"),
    "7": ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    "8": ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    "9": ("01110", "10001", "10001", "01111", "00001", "00010", "01100"),
    " ": ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
    ".": ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
    ",": ("00000", "00000", "00000", "00000", "01100", "00100", "01000"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    "-": ("00000", "00000", "00000", "01110", "00000", "00000", "00000"),
    "&": ("01100", "10010", "10100", "01000", "10101", "10010", "01101"),
    ":": ("00000", "01100", "01100", "00000", "01100", "01100", "00000"),
    "/": ("00001", "00010", "00010", "00100", "01000", "01000", "10000"),
    "(": ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
    ")": ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
    "!": ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
    "?": ("01110", "10001", "00001", "00110", "00100", "00000", "00100"),
    "%": ("11001", "11010", "00010", "00100", "01000", "01011", "10011"),
    "$": ("00100", "01111", "10100", "01110", "00101", "11110", "00100"),
    "+": ("00000", "00100", "00100", "01110", "00100", "00100", "00000"),
    "*": ("00000", "10101", "01110", "10101", "00000", "00000", "00000"),
}


class Canvas:
    """A tiny RGB raster canvas drawn with plain Python."""

    def __init__(self, width, height, colour):
        self.width = width
        self.height = height
        self.pixels = bytearray(colour * (width * height))

    def set_pixel(self, x, y, colour):
        if 0 <= x < self.width and 0 <= y < self.height:
            i = (y * self.width + x) * 3
            self.pixels[i:i + 3] = bytes(colour)

    def rect(self, x, y, w, h, colour):
        x0 = max(0, x)
        y0 = max(0, y)
        x1 = min(self.width, x + w)
        y1 = min(self.height, y + h)
        row = bytes(colour) * (x1 - x0)
        for yy in range(y0, y1):
            i = (yy * self.width + x0) * 3
            self.pixels[i:i + len(row)] = row

    def outline(self, x, y, w, h, colour, thick=3):
        self.rect(x, y, w, thick, colour)
        self.rect(x, y + h - thick, w, thick, colour)
        self.rect(x, y, thick, h, colour)
        self.rect(x + w - thick, y, thick, h, colour)

    def circle(self, cx, cy, r, colour):
        for yy in range(cy - r, cy + r + 1):
            for xx in range(cx - r, cx + r + 1):
                if (xx - cx) ** 2 + (yy - cy) ** 2 <= r * r:
                    self.set_pixel(xx, yy, colour)

    def ring(self, cx, cy, r, colour, thick=5):
        for yy in range(cy - r, cy + r + 1):
            for xx in range(cx - r, cx + r + 1):
                d2 = (xx - cx) ** 2 + (yy - cy) ** 2
                if (r - thick) ** 2 < d2 <= r * r:
                    self.set_pixel(xx, yy, colour)

    def line(self, x0, y0, x1, y1, colour, thick=4):
        steps = max(abs(x1 - x0), abs(y1 - y0), 1)
        for i in range(steps + 1):
            x = x0 + (x1 - x0) * i // steps
            y = y0 + (y1 - y0) * i // steps
            self.rect(x - thick // 2, y - thick // 2, thick, thick, colour)

    def triangle(self, x0, y0, x1, y1, x2, y2, colour):
        min_x = max(0, min(x0, x1, x2))
        max_x = min(self.width - 1, max(x0, x1, x2))
        min_y = max(0, min(y0, y1, y2))
        max_y = min(self.height - 1, max(y0, y1, y2))

        def edge(ax, ay, bx, by, px, py):
            return (px - ax) * (by - ay) - (py - ay) * (bx - ax)

        for yy in range(min_y, max_y + 1):
            for xx in range(min_x, max_x + 1):
                d0 = edge(x0, y0, x1, y1, xx, yy)
                d1 = edge(x1, y1, x2, y2, xx, yy)
                d2 = edge(x2, y2, x0, y0, xx, yy)
                if (d0 >= 0 and d1 >= 0 and d2 >= 0) or (
                        d0 <= 0 and d1 <= 0 and d2 <= 0):
                    self.set_pixel(xx, yy, colour)


def text_width(text, scale):
    return len(text) * 6 * scale - scale


def draw_text(canvas, x, y, text, scale, colour):
    cx = x
    for ch in text.upper():
        glyph = FONT.get(ch, FONT[" "])
        for row_i, row in enumerate(glyph):
            for col_i, bit in enumerate(row):
                if bit == "1":
                    canvas.rect(cx + col_i * scale, y + row_i * scale,
                                scale, scale, colour)
        cx += 6 * scale
    return cx - scale


def draw_text_centred(canvas, y, text, scale, colour, centre=WIDTH // 2):
    x = centre - text_width(text, scale) // 2
    draw_text(canvas, x, y, text, scale, colour)


def wrap_text(text, max_chars):
    words = text.split()
    lines = []
    current = ""
    for word in words:
        trial = word if not current else current + " " + word
        if len(trial) <= max_chars:
            current = trial
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


# ---------------------------------------------------------------- icons
def icon_missile(canvas, cx, cy, colour):
    canvas.line(cx - 34, cy + 34, cx + 18, cy - 18, colour, 13)
    canvas.triangle(cx + 14, cy - 34, cx + 38, cy - 10, cx + 10, cy - 6, colour)
    canvas.line(cx - 40, cy + 10, cx - 22, cy + 28, colour, 7)
    canvas.line(cx - 12, cy + 40, cx + 6, cy + 22, colour, 7)
    for dx, dy in ((-40, 44), (-26, 52), (-42, 26)):
        canvas.circle(cx + dx, cy + dy, 5, ORANGE)


def icon_building(canvas, cx, cy, colour):
    canvas.rect(cx - 36, cy - 6, 30, 46, colour)
    canvas.rect(cx - 2, cy - 22, 34, 62, colour)
    for wx in (cx - 30, cx - 18):
        for wy in (cy + 2, cy + 16):
            canvas.rect(wx, wy, 7, 8, CARD)
    for wx in (cx + 6, cx + 19):
        for wy in (cy - 12, cy + 4, cy + 20):
            canvas.rect(wx, wy, 7, 8, CARD)
    canvas.circle(cx + 34, cy - 32, 11, ORANGE)
    canvas.circle(cx + 34, cy - 32, 6, RED)
    canvas.line(cx + 34, cy - 20, cx + 24, cy - 4, RED, 5)


def icon_handcuffs(canvas, cx, cy, colour):
    canvas.ring(cx - 20, cy + 8, 19, colour, 6)
    canvas.ring(cx + 22, cy + 8, 19, colour, 6)
    canvas.line(cx - 8, cy - 14, cx + 10, cy - 14, colour, 6)
    canvas.rect(cx - 24, cy - 30, 8, 20, colour)
    canvas.rect(cx + 18, cy - 30, 8, 20, colour)


def icon_globe(canvas, cx, cy, colour):
    canvas.ring(cx, cy, 34, colour, 5)
    canvas.line(cx - 34, cy, cx + 34, cy, colour, 4)
    canvas.line(cx, cy - 34, cx, cy + 34, colour, 4)
    canvas.line(cx - 24, cy - 24, cx - 24, cy + 24, colour, 3)
    canvas.line(cx + 24, cy - 24, cx + 24, cy + 24, colour, 3)
    canvas.circle(cx + 38, cy - 38, 8, RED)
    canvas.rect(cx + 35, cy - 34, 6, 13, RED)


def icon_chart(canvas, cx, cy, colour):
    canvas.line(cx - 44, cy + 36, cx + 46, cy + 36, GREY, 4)
    canvas.line(cx - 44, cy + 36, cx - 44, cy - 38, GREY, 4)
    points = ((-38, -22), (-16, -8), (2, -26), (22, 4), (42, 26))
    for (ax, ay), (bx, by) in zip(points, points[1:]):
        canvas.line(cx + ax, cy + ay, cx + bx, cy + by, RED, 7)
    canvas.triangle(cx + 30, cy + 30, cx + 52, cy + 32, cx + 40, cy + 14, RED)


def icon_pi(canvas, cx, cy, colour):
    canvas.rect(cx - 34, cy - 26, 68, 11, colour)
    canvas.rect(cx - 26, cy - 26, 11, 52, colour)
    canvas.rect(cx + 15, cy - 26, 11, 40, colour)
    canvas.circle(cx + 36, cy - 34, 9, ORANGE)
    draw_text(canvas, cx + 29, cy - 43, "?", 3, ORANGE)


ICON_DRAWERS = {
    "missile": icon_missile,
    "building": icon_building,
    "handcuffs": icon_handcuffs,
    "globe": icon_globe,
    "chart": icon_chart,
    "pi": icon_pi,
}

STORIES = [
    {
        "tag": "MIDDLE EAST - BAHRAIN",
        "colour": RED,
        "icon": "missile",
        "headline": "IRAN STRIKES U.S. BASES IN BAHRAIN",
        "detail": "TEHRAN SEEKS TALKS. TRUMP: TERMS UNACCEPTABLE",
    },
    {
        "tag": "UKRAINE WAR",
        "colour": BLUE,
        "icon": "building",
        "headline": "RUSSIAN MISSILE HITS KRYVYI RIH",
        "detail": "2 KILLED, DOZENS WOUNDED IN CITY CENTRE HIT",
    },
    {
        "tag": "MEXICO - SINALOA",
        "colour": TEAL,
        "icon": "handcuffs",
        "headline": "CARTEL BOSS EL CHAPO ISIDRO CAPTURED",
        "detail": "FBI MOST-WANTED SEIZED. AFTERMATH: 11 DEAD",
    },
    {
        "tag": "CLIMATE - ANTALYA, TURKEY",
        "colour": GREEN,
        "icon": "globe",
        "headline": "COP31 TALKS RUN INTO OVERTIME",
        "detail": "NO DEAL YET. SPLIT OVER FOSSIL FUELS, FINANCE",
    },
    {
        "tag": "MARKETS - NEW YORK",
        "colour": ORANGE,
        "icon": "chart",
        "headline": "AI SELL-OFF SLIDES U.S. STOCKS",
        "detail": "CHIP SHARES PLUNGE. NVIDIA FACES SEC PROBE",
    },
    {
        "tag": "SCIENCE - AI",
        "colour": PURPLE,
        "icon": "pi",
        "headline": "AI 'SOLVES GREATEST MATH RIDDLE'",
        "detail": "ANTHROPIC RESEARCHER CLAIMS CLAUDE DID IT",
    },
]

TICKER_LINES = [
    "ALSO TODAY: FBI + FARM DEPT DATABASES BREACHED",
    "KILLER ROBOTS PACT TALKS OPEN * BEPICOLOMBO AT MERCURY",
    "BRAZIL: BACTERIA MOSQUITOES CUT CHILD DENGUE",
]


def draw_panel(canvas, x, y, w, h, story):
    canvas.rect(x, y, w, h, CARD)
    canvas.outline(x, y, w, h, INK, 3)
    canvas.rect(x, y, w, 34, story["colour"])
    draw_text(canvas, x + 14, y + 8, story["tag"], 3, CARD)
    icon_cx = x + 52
    icon_cy = y + 108
    ICON_DRAWERS[story["icon"]](canvas, icon_cx, icon_cy, story["colour"])
    text_x = x + 104
    headline_lines = wrap_text(story["headline"], 15)
    hy = y + 48
    for line_text in headline_lines[:3]:
        draw_text(canvas, text_x, hy, line_text, 4, INK)
        hy += 34
    detail_lines = wrap_text(story["detail"], 25)
    dy = y + h - 56
    for line_text in detail_lines[:2]:
        draw_text(canvas, x + 14, dy, line_text, 3, GREY)
        dy += 24


def build_image():
    canvas = Canvas(WIDTH, HEIGHT, PAPER)

    # Header ------------------------------------------------------------
    canvas.rect(0, 0, WIDTH, 168, INK)
    canvas.rect(0, 168, WIDTH, 8, RED)
    draw_text_centred(canvas, 16, "THE WORLD IN ONE PICTURE", 4, LIGHT)
    draw_text_centred(canvas, 56, "SATURDAY 21 NOVEMBER 2026", 6, CARD)
    draw_text_centred(canvas, 122, "WORLD NEWS OF THE DAY", 3, LIGHT)

    # Story grid: 2 columns x 3 rows ------------------------------------
    margin = 24
    gap = 16
    panel_w = (WIDTH - margin * 2 - gap) // 2
    panel_h = 218
    top = 196
    for index, story in enumerate(STORIES):
        col = index % 2
        row = index // 2
        x = margin + col * (panel_w + gap)
        y = top + row * (panel_h + gap)
        draw_panel(canvas, x, y, panel_w, panel_h, story)

    # Ticker --------------------------------------------------------------
    ticker_y = top + 3 * panel_h + 2 * gap + 14
    canvas.rect(margin, ticker_y, WIDTH - margin * 2, 92, INK)
    ty = ticker_y + 14
    for line_text in TICKER_LINES:
        draw_text_centred(canvas, ty, line_text, 3, CARD)
        ty += 24

    return canvas


def encode_png(canvas):
    raw = bytearray()
    stride = canvas.width * 3
    for yy in range(canvas.height):
        raw.append(0)
        start = yy * stride
        raw.extend(canvas.pixels[start:start + stride])

    def chunk(kind, data):
        return (
            struct.pack(">I", len(data))
            + kind
            + data
            + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
        )

    header = struct.pack(
        ">IIBBBBB", canvas.width, canvas.height, 8, 2, 0, 0, 0
    )
    return (
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", header)
        + chunk(b"IDAT", zlib.compress(bytes(raw), 9))
        + chunk(b"IEND", b"")
    )


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    try:
        os.makedirs(out_dir, exist_ok=True)
    except OSError:
        out_dir = "output"
        os.makedirs(out_dir, exist_ok=True)
    data = encode_png(build_image())
    with open(os.path.join(out_dir, "entry.png"), "wb") as fh:
        fh.write(data)


if __name__ == "__main__":
    main()
