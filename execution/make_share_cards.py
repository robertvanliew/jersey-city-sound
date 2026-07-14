# Branded 1080x1920 share cards (Instagram-story ratio) for every entry.
# If the entry has a gallery/notable image, it becomes the backdrop (a "capture"),
# darkened with a gradient; otherwise a clean ink-and-gold typographic card.
# All carry the Jersey City Sound mark, the name/role, and jerseycitysound.com.
#
# Run:  py execution/make_share_cards.py
import json, sys, re
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
DESIGN = ROOT / "design"
OUT = DESIGN / "assets" / "cards"
OUT.mkdir(parents=True, exist_ok=True)
W, H = 1080, 1920

INK = (14, 14, 16)
CREAM = (245, 239, 221)
GOLD = (201, 162, 39)
GOLDL = (238, 210, 122)
MUTED = (176, 169, 143)
FONTS = "C:/Windows/Fonts/"


def font(name, size):
    return ImageFont.truetype(FONTS + name, size)


def gold_mark(size, ss=4):
    """Vinyl brand mark in gold on transparent — clean over ink and photos."""
    S = size * ss
    cv = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(cv)
    c, R = S / 2, S / 2 - ss
    d.ellipse([c - R, c - R, c + R, c + R], fill=GOLD + (255,))
    gw = max(2, int(S * 0.022))
    for f in (0.90, 0.775, 0.65, 0.525):
        r = R * f
        d.ellipse([c - r, c - r, c + r, c + r], outline=INK + (255,), width=gw)
    lr = R * 0.40
    d.ellipse([c - lr, c - lr, c + lr, c + lr], fill=INK + (255,))
    dr = R * 0.11
    d.ellipse([c - dr, c - dr, c + dr, c + dr], fill=GOLD + (255,))
    return cv.resize((size, size), Image.LANCZOS)


SERIF = "georgia.ttf"; SERIF_B = "georgiab.ttf"; SERIF_I = "georgiai.ttf"; SANS = "arialbd.ttf"


def spaced(t, n=2):
    return (" " * n).join(list(t))


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_name(draw, name, max_w):
    for size in (128, 112, 96, 82, 70, 60):
        f = font(SERIF_B, size)
        lines = wrap(draw, name, f, max_w)
        if len(lines) <= 2 and all(draw.textlength(l, font=f) <= max_w for l in lines):
            return f, lines
    f = font(SERIF_B, 60)
    return f, wrap(draw, name, f, max_w)[:2]


def center(draw, y, text, fnt, fill):
    w = draw.textlength(text, font=fnt)
    draw.text(((W - w) / 2, y), text, font=fnt, fill=fill)


def load_backdrop(src):
    try:
        im = Image.open(DESIGN / src).convert("RGB")
    except Exception:
        return None
    # cover-fit to WxH
    scale = max(W / im.width, H / im.height)
    im = im.resize((int(im.width * scale), int(im.height * scale)), Image.LANCZOS)
    left = (im.width - W) // 2
    top = (im.height - H) // 3        # bias toward the top (faces)
    im = im.crop((left, top, left + W, top + H))
    # darken: flat dim + stronger gradient toward bottom
    im = Image.blend(im, Image.new("RGB", (W, H), INK), 0.42)
    grad = Image.new("L", (1, H), 0)
    for y in range(H):
        grad.putpixel((0, y), int(235 * (max(0, y - H * 0.42) / (H * 0.58)) ** 1.4))
    grad = grad.resize((W, H))
    im = Image.composite(Image.new("RGB", (W, H), INK), im, grad)
    return im


def make_card(name, roles, no, lead, backdrop_src, out_path):
    photo = load_backdrop(backdrop_src) if backdrop_src else None
    img = photo if photo else Image.new("RGB", (W, H), INK)
    d = ImageDraw.Draw(img)

    # hairline gold frame
    d.rectangle([46, 46, W - 46, H - 46], outline=GOLD, width=2)

    # mark, top-center
    mk = gold_mark(188)
    img.paste(mk, ((W - 188) // 2, 118), mk)
    center(d, 330, spaced("THE JERSEY CITY SOUND"), font(SANS, 30), GOLDL)

    # name block — bottom third for photo cards, centered for typographic
    max_w = W - 200
    fname, lines = fit_name(d, name, max_w)
    role_line = " · ".join(roles)
    lh = fname.size + 12
    block_h = lh * len(lines)
    y = (H - block_h) // 2 - 60 if not photo else H - 470 - block_h

    center(d, y - 64, spaced(f"ENTRY №. {no}", 1), font(SANS, 26), GOLD)
    for ln in lines:
        center(d, y, ln, fname, CREAM)
        y += lh
    if role_line:
        center(d, y + 10, role_line, font(SERIF_I, 40), MUTED)
        y += 62

    # gold rule
    d.line([(W // 2 - 140, y + 40), (W // 2 + 140, y + 40)], fill=GOLD, width=2)

    # lead snippet (typographic cards only — keeps photo cards clean)
    if lead and not photo:
        snip = lead.strip()
        if len(snip) > 150:
            snip = snip[:150].rsplit(" ", 1)[0] + "…"
        yy = y + 90
        for ln in wrap(d, snip, font(SERIF, 38), max_w)[:3]:
            center(d, yy, ln, font(SERIF, 38), (222, 214, 190))
            yy += 52

    # footer
    center(d, H - 246, spaced("jerseycitysound.com", 1), font(SANS, 34), CREAM)
    center(d, H - 190, "Every voice in the city, on the record.", font(SERIF_I, 32), MUTED)

    img.save(out_path)


def first_image(e):
    for g in e.get("galleries", []):
        if g.get("images"):
            return g["images"][0]["src"]
    return None


def main():
    data = json.loads((ROOT / "data" / "entries.json").read_text(encoding="utf-8"))
    entries = list(data["entries"])
    # DJ DX is handcrafted — add it explicitly
    entries.append({"slug": "dj-dx", "name": "DJ DX", "entry_no": "001",
                    "roles": ["DJ", "Producer", "Turntablist"],
                    "facts": ["Robert Van Liew, known professionally as DJ DX, is a Jersey City "
                              "DJ, producer, and recording artist active since the late 1990s."]})
    n = 0
    for e in entries:
        lead = (e.get("facts") or [""])[0]
        make_card(e["name"], e.get("roles") or [], e["entry_no"], lead,
                  first_image(e), OUT / f"{e['slug']}.png")
        n += 1
    print(f"generated {n} share cards -> {OUT}")


if __name__ == "__main__":
    main()
