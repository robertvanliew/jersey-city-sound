# Brand favicon set — the vinyl mark (the "O" from the SOUND wordmark / the
# Instagram avatar), redrawn cleanly on a cream disc so it reads on light and
# dark browser tabs. Writes design/assets/favicon-{512,180,64,32,16}.png.
# The gold mark-jcs-*.png stay as the share-card mark (different context).
#
# Run:  py execution/make_favicons.py
import sys
from pathlib import Path
from PIL import Image, ImageDraw
sys.stdout.reconfigure(encoding="utf-8")

OUT = Path(__file__).resolve().parent.parent / "design" / "assets"
CREAM = (245, 239, 221, 255)
INK = (14, 14, 16, 255)


def vinyl(size, ss=4):
    S = size * ss
    cv = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(cv)
    d.ellipse([0, 0, S - 1, S - 1], fill=CREAM)                 # avatar disc
    c, R = S / 2, S * 0.455
    d.ellipse([c - R, c - R, c + R, c + R], fill=INK)           # black record
    gw = max(2, int(S * 0.020))
    for f in (0.90, 0.775, 0.65, 0.525):                        # cream grooves
        r = R * f
        d.ellipse([c - r, c - r, c + r, c + r], outline=CREAM, width=gw)
    lr = R * 0.40
    d.ellipse([c - lr, c - lr, c + lr, c + lr], fill=INK)       # center label
    dr = R * 0.11
    d.ellipse([c - dr, c - dr, c + dr, c + dr], fill=CREAM)     # spindle dot
    return cv.resize((size, size), Image.LANCZOS)


def main():
    for s in (512, 180, 64, 32, 16):
        vinyl(s).save(OUT / f"favicon-{s}.png")
    print("wrote favicon-{512,180,64,32,16}.png ->", OUT)


if __name__ == "__main__":
    main()
