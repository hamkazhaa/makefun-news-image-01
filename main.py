#!/usr/bin/env python3
"""
Sum up 13 November's world news in one image.
make.fun bounty: https://make.fun/bounty/news-image-01
$250 USDC, ends Sat 14 Nov 2026 20:00 UTC / Sun 15 Nov 2026 03:00 WIB.

Stdlib only (Python 3.13 target; also runs on 3.12). No network at
runtime. No PIL, no fonts on disk: text is rendered with an embedded
5x7 bitmap font, and the PNG is encoded with zlib/struct only.
Two runs produce byte-identical output: fixed pixels, fixed zlib
level, no timestamps or random data anywhere.

Usage:
    python3 main.py                 # writes /output/entry.png
    python3 main.py out/entry.png   # writes to the given path (local test)
    OUTPUT_PATH=out/entry.png python3 main.py
"""

import os
import struct
import sys
import zlib

W, H = 1024, 1024

# ---------------------------------------------------------------- font
# 5x7 bitmap font, one entry per character: 7 rows, 5 columns each.
# "1" = filled pixel. Only the characters used in the image are defined;
# anything else renders as a blank (sanitised in draw_text).
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
BLANK = ("00000",) * 7

# ---------------------------------------------------------------- canvas
NAVY = (15, 30, 51)
NAVY2 = (21, 42, 68)
RED = (200, 16, 46)
GOLD = (212, 175, 55)
WHITE = (245, 245, 240)
GREY = (180, 190, 200)
LIGHT = (210, 220, 230)


class Canvas:
    def __init__(self, w, h, bg):
        self.w, self.h = w, h
        self.px = bytearray(bg * (w * h))

    def rect(self, x, y, w, h, colour):
        x0, y0 = max(0, x), max(0, y)
        x1, y1 = min(self.w, x + w), min(self.h, y + h)
        r, g, b = colour
        for yy in range(y0, y1):
            base = (yy * self.w + x0) * 3
            for xx in range(x0, x1):
                i = base + (xx - x0) * 3
                self.px[i], self.px[i + 1], self.px[i + 2] = r, g, b

    def hline(self, x, y, w, colour, thick=2):
        self.rect(x, y, w, thick, colour)

    def text(self, x, y, s, scale, colour):
        """Draw uppercase text; unknown chars render blank."""
        cx = x
        for ch in s.upper():
            glyph = FONT.get(ch, BLANK)
            for row in range(7):
                bits = glyph[row]
                for col in range(5):
                    if bits[col] == "1":
                        self.rect(cx + col * scale, y + row * scale,
                                  scale, scale, colour)
            cx += 6 * scale
        return cx

    def text_width(self, s, scale):
        return len(s) * 6 * scale - scale


def wrap(text, max_chars):
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if len(trial) <= max_chars:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            # very long word: hard-split it
            while len(word) > max_chars:
                lines.append(word[:max_chars])
                word = word[max_chars:]
            cur = word
    if cur:
        lines.append(cur)
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
CONTENT_W = W - 2 * MARGIN


def build():
    c = Canvas(W, H, NAVY)
    # header band
    c.rect(0, 0, W, 168, NAVY2)
    c.rect(0, 168, W, 6, RED)
    c.text(MARGIN, 28, "WORLD NEWS", 7, WHITE)
    c.text(MARGIN, 92, "FRIDAY 13 NOVEMBER 2026", 4, GOLD)
    c.text(MARGIN, 128, "SIX STORIES THAT DEFINED THE DAY", 3, GREY)

    y = 192
    for num, headline, body in STORIES:
        # number tag
        c.rect(MARGIN, y, 54, 30, RED)
        c.text(MARGIN + 9, y + 4, num, 3, WHITE)
        # headline, one line at scale 4 (all headlines fit in 40 chars)
        c.text(MARGIN + 72, y + 1, headline, 4, WHITE)
        y += 38
        # body, scale 3, wrapped to content width
        max_chars = CONTENT_W // (6 * 3)
        for line in wrap(body, max_chars):
            c.text(MARGIN, y, line, 3, LIGHT)
            y += 22
        y += 10
        if num != "06":
            c.hline(MARGIN, y, CONTENT_W, (45, 70, 95), 2)
            y += 12

    # footer
    c.rect(0, H - 56, W, 56, NAVY2)
    c.text(MARGIN, H - 40,
           "SOURCES: ASSOCIATED PRESS, REUTERS, GUARDIAN, BBC - 13 NOV 2026",
           2, GREY)
    c.text(MARGIN, H - 22,
           "SUMMARY IMAGE, NOT A PHOTO. CLAIMS ARE LABELLED AS CLAIMS.",
           2, GREY)
    return c


# ---------------------------------------------------------------- PNG
def chunk(kind, data):
    out = struct.pack(">I", len(data)) + kind + data
    out += struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
    return out


def encode_png(canvas):
    ihdr = struct.pack(">IIBBBBB", canvas.w, canvas.h, 8, 2, 0, 0, 0)
    raw = bytearray()
    stride = canvas.w * 3
    for yy in range(canvas.h):
        raw.append(0)  # filter: none
        raw += canvas.px[yy * stride:(yy + 1) * stride]
    # Fixed compression level => deterministic bytes.
    comp = zlib.compress(bytes(raw), 9)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr)
            + chunk(b"IDAT", comp) + chunk(b"IEND", b""))


def main(argv):
    out = os.environ.get("OUTPUT_PATH") or (argv[1] if len(argv) > 1
                                            else "/output/entry.png")
    parent = os.path.dirname(out)
    if parent:
        os.makedirs(parent, exist_ok=True)
    data = encode_png(build())
    with open(out, "wb") as f:
        f.write(data)
    print(f"wrote {out} ({len(data)} bytes, {W}x{H})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
