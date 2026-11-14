#!/usr/bin/env python3
"""
Sum up 13 November's world news in one image.
make.fun bounty: https://make.fun/bounty/news-image-01
$250 USDC. Ends Sat 14 Nov 2026 20:00 UTC / Sun 15 Nov 2026 03:00 WIB.

Rebuilt in a fresh session on 2026-11-15 ~01:56 WIB so the build
session transcript records the program being written here.

Python stdlib only (os, struct, sys, zlib). No network at runtime,
no PIL, no fonts on disk. Text is rendered with an embedded 5x7
bitmap font and the PNG is encoded by hand (zlib, fixed level 9),
so two runs produce byte-identical output: fixed pixels, fixed
compression, no timestamps and no random data anywhere.

Usage:
    python3 main.py                 # writes /output/entry.png
    python3 main.py out/entry.png   # writes to the given path
    OUTPUT_PATH=out/entry.png python3 main.py
"""

import os
import struct
import sys
import zlib

WIDTH, HEIGHT = 1024, 1024

# ------------------------------------------------------------------ font
# 5x7 bitmap font: 7 rows of 5 bits per character. "1" = filled pixel.
# Only characters used in the poster are defined; anything else is
# rendered as a blank (draw_text sanitises via .get()).
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
    "X": ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    "Y": ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
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
    ":": ("00000", "01100", "01100", "00000", "01100", "01100", "00000"),
    ";": ("00000", "01100", "01100", "00000", "01100", "00100", "01000"),
    "-": ("00000", "00000", "00000", "01110", "00000", "00000", "00000"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    "(": ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
    ")": ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
    "/": ("00001", "00010", "00010", "00100", "01000", "01000", "10000"),
    "%": ("11001", "11010", "00010", "00100", "01000", "01011", "10011"),
    "?": ("01110", "10001", "00001", "00110", "00100", "00000", "00100"),
    "!": ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
    "+": ("00000", "00100", "00100", "11111", "00100", "00100", "00000"),
    "=": ("00000", "00000", "11111", "00000", "11111", "00000", "00000"),
    '"': ("01010", "01010", "00000", "00000", "00000", "00000", "00000"),
    "&": ("01100", "10010", "10100", "01000", "10101", "10010", "01101"),
    "*": ("00000", "00100", "10101", "01110", "10101", "00100", "00000"),
}
BLANK_GLYPH = ("00000",) * 7

# ---------------------------------------------------------------- canvas
NAVY = (15, 30, 51)
NAVY_BAND = (21, 42, 68)
RED = (200, 16, 46)
GOLD = (212, 175, 55)
WHITE = (245, 245, 240)
GREY = (180, 190, 200)
LIGHT = (210, 220, 230)
DIVIDER = (45, 70, 95)


class Canvas:
    """A plain RGB pixel buffer with rectangle / text drawing."""

    def __init__(self, width, height, background):
        self.width, self.height = width, height
        self.pixels = bytearray(background * (width * height))

    def fill_rect(self, x, y, width, height, colour):
        x0, y0 = max(0, x), max(0, y)
        x1, y1 = min(self.width, x + width), min(self.height, y + height)
        r, g, b = colour
        for yy in range(y0, y1):
            base = (yy * self.width + x0) * 3
            for xx in range(x0, x1):
                i = base + (xx - x0) * 3
                self.pixels[i], self.pixels[i + 1], self.pixels[i + 2] = r, g, b

    def rule(self, x, y, width, colour, thickness=2):
        self.fill_rect(x, y, width, thickness, colour)

    def draw_text(self, x, y, text, scale, colour):
        """Draw upper-case text; unknown characters render blank."""
        cursor = x
        for char in text.upper():
            glyph = FONT.get(char, BLANK_GLYPH)
            for row in range(7):
                bits = glyph[row]
                for col in range(5):
                    if bits[col] == "1":
                        self.fill_rect(cursor + col * scale,
                                       y + row * scale,
                                       scale, scale, colour)
            cursor += 6 * scale
        return cursor


def wrap_text(text, max_chars):
    """Greedy word wrap; very long words are hard-split."""
    lines, current = [], ""
    for word in text.split():
        trial = word if not current else current + " " + word
        if len(trial) <= max_chars:
            current = trial
        else:
            if current:
                lines.append(current)
            while len(word) > max_chars:
                lines.append(word[:max_chars])
                word = word[max_chars:]
            current = word
    if current:
        lines.append(current)
    return lines


# ---------------------------------------------------------------- content
# Headlines verified 14-15 Nov 2026 from AP (via Level Headlines),
# Reuters (via The Raisina Post), Guardian/BBC (via Michael Brunger),
# Profile News / Zark News daily briefs for Friday 13 Nov 2026.
# Claims that could not be independently verified are labelled as claims.
STORIES = [
    ("01", "UKRAINE LAUNCHES HUGE DRONE ATTACK",
     "KYIV SAID IT FIRED ALMOST 1,200 DRONES AT RUSSIA OVERNIGHT, "
     "ONE OF ITS BIGGEST STRIKES OF THE WAR, AS US-LED TALKS WIDEN "
     "TO INCLUDE EUROPE."),
    ("02", "US SAYS IT DOWNED IRANIAN DRONES",
     "WASHINGTON SAID IT SHOT DOWN TWO IRANIAN DRONES HEADED FOR "
     "BAHRAIN. TEHRAN CLAIMED IT HIT A US RADAR THERE. THAT CLAIM "
     "COULD NOT BE VERIFIED."),
    ("03", "MICROSOFT 365 OUTAGE HITS DAY 2",
     "OUTLOOK, TEAMS AND COPILOT WERE STILL BEING RESTORED AFTER A "
     "GLOBAL OUTAGE THAT BEGAN ON 12 NOVEMBER AND SPREAD ACROSS "
     "MORE THAN 70 COUNTRIES."),
    ("04", "NVIDIA CHIEF JENSEN HUANG RESIGNS",
     "HUANG QUIT AS CHIEF EXECUTIVE AFTER REPORTS OF AN AFFAIR AND "
     "LINKS TO A WOMAN ALLEGED TO BE A CHINESE SPY. HE WAS SUMMONED "
     "TO TESTIFY TO CONGRESS."),
    ("05", "FAA LIFTS US FLIGHT GROUND STOP",
     "US FLIGHTS RESUMED ON FRIDAY EVENING AFTER A COMMUNICATIONS "
     "FAILURE HALTED DEPARTURES NATIONWIDE FOR MORE THAN FOUR HOURS."),
    ("06", "QATAR AND TURKEY SIGN DEFENCE PACT",
     "DOHA AND ANKARA SIGNED A MUTUAL DEFENCE DEAL IN ISTANBUL, "
     "PLEDGING A UNITED STANCE AGAINST AN OUTSIDE ARMED ATTACK."),
]

MARGIN = 48
CONTENT_WIDTH = WIDTH - 2 * MARGIN
BODY_SCALE = 3
# 23 px line height for a 21 px glyph (7 rows x scale 3) leaves a
# 2 px gap between body lines; 21 px left the lines touching.
BODY_LINE_HEIGHT = 23
BODY_MAX_CHARS = CONTENT_WIDTH // (6 * BODY_SCALE)


def build_poster():
    canvas = Canvas(WIDTH, HEIGHT, NAVY)
    # Header band.
    canvas.fill_rect(0, 0, WIDTH, 168, NAVY_BAND)
    canvas.fill_rect(0, 168, WIDTH, 6, RED)
    canvas.draw_text(MARGIN, 28, "WORLD NEWS", 7, WHITE)
    canvas.draw_text(MARGIN, 92, "FRIDAY 13 NOVEMBER 2026", 4, GOLD)
    canvas.draw_text(MARGIN, 128, "SIX STORIES THAT DEFINED THE DAY", 3, GREY)

    # Start 4 px higher to pay for the taller body lines.
    y = 192
    for number, headline, body in STORIES:
        # Number tag, then the headline on the same row.
        canvas.fill_rect(MARGIN, y, 54, 30, RED)
        canvas.draw_text(MARGIN + 9, y + 4, number, 3, WHITE)
        canvas.draw_text(MARGIN + 72, y + 1, headline, 4, WHITE)
        y += 36
        # Body, wrapped to the content width.
        for line in wrap_text(body, BODY_MAX_CHARS):
            canvas.draw_text(MARGIN, y, line, BODY_SCALE, LIGHT)
            y += BODY_LINE_HEIGHT
        y += 6
        if number != "06":
            canvas.rule(MARGIN, y, CONTENT_WIDTH, DIVIDER, 2)
            y += 8

    # Footer band (56 px tall, at the very bottom).
    canvas.fill_rect(0, HEIGHT - 56, WIDTH, 56, NAVY_BAND)
    canvas.draw_text(
        MARGIN, HEIGHT - 40,
        "SOURCES: ASSOCIATED PRESS, REUTERS, GUARDIAN, BBC - 13 NOV 2026",
        2, GREY)
    canvas.draw_text(
        MARGIN, HEIGHT - 22,
        "SUMMARY IMAGE, NOT A PHOTO. CLAIMS ARE LABELLED AS CLAIMS.",
        2, GREY)
    return canvas


# -------------------------------------------------------------------- PNG
def make_chunk(kind, data):
    out = struct.pack(">I", len(data)) + kind + data
    out += struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
    return out


def encode_png(canvas):
    ihdr = struct.pack(">IIBBBBB", canvas.width, canvas.height,
                       8, 2, 0, 0, 0)
    raw = bytearray()
    stride = canvas.width * 3
    for yy in range(canvas.height):
        raw.append(0)  # filter: none
        raw += canvas.pixels[yy * stride:(yy + 1) * stride]
    # Fixed compression level => deterministic bytes.
    compressed = zlib.compress(bytes(raw), 9)
    return (b"\x89PNG\r\n\x1a\n" + make_chunk(b"IHDR", ihdr)
            + make_chunk(b"IDAT", compressed) + make_chunk(b"IEND", b""))


def main(argv):
    out = os.environ.get("OUTPUT_PATH") or (
        argv[1] if len(argv) > 1 else "/output/entry.png")
    parent = os.path.dirname(out)
    if parent:
        os.makedirs(parent, exist_ok=True)
    data = encode_png(build_poster())
    with open(out, "wb") as f:
        f.write(data)
    print(f"wrote {out} ({len(data)} bytes, {WIDTH}x{HEIGHT})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
