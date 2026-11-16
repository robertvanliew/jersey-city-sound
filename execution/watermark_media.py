"""Watermark every archive photo with a clean, single-line "THE JERSEY CITY SOUND"
wordmark — gold caps with a crisp dark outline (legible on any background, no boxy
plate) — auto-placed in each photo's emptiest region.

Sources from the clean originals in ./Media Originals/ and writes to
design/assets/media/, so it never stacks watermarks and is fully idempotent.

Output is web-sized: the long edge is capped at MAX_EDGE, PNG photos are written as
WebP (the .png is removed from design/ but the clean .png stays in Media Originals/),
and JPEGs are re-encoded at web quality. After a PNG converts, point its gallery
"src" in data/entries.json at the .webp and regenerate.

  py execution/watermark_media.py
"""
import shutil
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
MEDIA = ROOT / "design" / "assets" / "media"
BACKUP = ROOT / "Media Originals"
EXTS = {".png", ".jpg", ".jpeg", ".webp"}
SKIP_NAMES = {"catamount-logo.png"}
MAX_EDGE = 1600      # px, long edge; slideshows display far smaller
WEBP_Q = 78
JPEG_Q = 82
FONT_PATH = "C:/Windows/Fonts/arialbd.ttf"
TEXT = "THE JERSEY CITY SOUND"
GOLD = (233, 199, 74, 255)
DARK = (12, 11, 8, 255)


def build_wordmark(cap_px=120):
    """Crisp gold caps with a dark stroke outline and letter-spacing. High-res; downscale per photo."""
    S = 4
    fs = cap_px * S
    font = ImageFont.truetype(FONT_PATH, fs)
    track = fs * 0.16                       # letter-spacing
    stroke = max(1, round(fs * 0.055))
    asc, desc = font.getmetrics()
    total = sum(font.getlength(c) for c in TEXT) + track * (len(TEXT) - 1)
    W = int(total + stroke * 2 + fs)
    H = int(asc + desc + stroke * 2)
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    x = stroke + fs * 0.15
    for c in TEXT:
        if c != " ":
            d.text((x, stroke), c, font=font, fill=GOLD, stroke_width=stroke, stroke_fill=DARK)
        x += font.getlength(c) + track
    img = img.crop(img.split()[3].getbbox())
    w2 = max(1, img.width // S)
    return img.resize((w2, max(1, round(img.height * w2 / img.width))), Image.LANCZOS)


MARK = build_wordmark()


def emptiest_spot(gray, mw, mh, W, H, margin):
    xs = {"l": margin, "c": (W - mw) // 2, "r": W - mw - margin}
    ys = {"t": margin, "b": H - mh - margin}
    best, bx, by = None, W - mw - margin, H - mh - margin
    for yk, y in ys.items():
        for x in xs.values():
            if x < 0 or y < 0 or x + mw > W or y + mh > H:
                continue
            region = np.asarray(gray.crop((x, y, x + mw, y + mh)), dtype=np.float32)
            score = region.std() + (6.0 if yk == "t" else 0.0)
            if best is None or score < best:
                best, bx, by = score, x, y
    return bx, by


def watermark(src, dst):
    im = Image.open(src).convert("RGBA")
    if max(im.size) > MAX_EDGE:
        im.thumbnail((MAX_EDGE, MAX_EDGE), Image.LANCZOS)
    W, H = im.size
    mw = max(150, min(int(W * 0.26), 360))          # single line ≈ 26% of width
    mark = MARK.resize((mw, max(1, round(MARK.height * mw / MARK.width))), Image.LANCZOS)
    mkw, mkh = mark.size
    a = mark.split()[3].point(lambda p: int(p * 0.82))
    mark.putalpha(a)
    margin = max(12, int(min(W, H) * 0.035))
    x, y = emptiest_spot(im.convert("L"), mkw, mkh, W, H, margin)
    im.alpha_composite(mark, (x, y))
    ext = dst.suffix.lower()
    if ext in (".jpg", ".jpeg"):
        im.convert("RGB").save(dst, "JPEG", quality=JPEG_Q, optimize=True, progressive=True)
    elif ext == ".webp":
        if im.getextrema()[3][0] == 255:        # fully opaque: drop the alpha channel
            im = im.convert("RGB")
        im.save(dst, "WEBP", quality=WEBP_Q, method=6)
    else:
        im.save(dst, "PNG", optimize=True)


def clean_source(p):
    """The clean original for a design/ media file. A .webp may come from a .png original."""
    rel = p.relative_to(MEDIA)
    for cand in [BACKUP / rel] + [BACKUP / rel.with_suffix(x) for x in (".png", ".jpg", ".jpeg")]:
        if cand.exists():
            return cand
    return None


def main():
    done, converted = 0, []
    for p in sorted(MEDIA.rglob("*")):
        if p.suffix.lower() not in EXTS or p.name in SKIP_NAMES or p.name.startswith("."):
            continue
        clean = clean_source(p)
        if clean is None:
            clean = BACKUP / p.relative_to(MEDIA)
            clean.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, clean)
        dst = p.with_suffix(".webp") if p.suffix.lower() == ".png" else p
        watermark(clean, dst)
        if dst != p:
            p.unlink()
            converted.append((p, dst))
        done += 1
    print(f"watermarked {done} images (clean single-line wordmark, from {BACKUP.name}/)")
    for old, new in converted:
        print(f"  converted {old.relative_to(MEDIA.parent.parent).as_posix()} -> {new.suffix}")


if __name__ == "__main__":
    main()
