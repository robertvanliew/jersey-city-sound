# Branded 1200x630 Open Graph cards (link-preview ratio) for every entry.
# These are what WhatsApp / Messenger / Facebook / X / iMessage render when an
# entry URL is shared. Same branding as the 1080x1920 story cards: a darkened
# "capture" of the person's photo when one exists, else a clean ink-and-gold
# typographic card. Written to design/assets/og/{slug}.png.
#
# Run:  py execution/make_og_cards.py
import json, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
DESIGN = ROOT / "design"
OUT = DESIGN / "assets" / "og"
OUT.mkdir(parents=True, exist_ok=True)
W, H = 1200, 630

INK = (14, 14, 16)
CREAM = (245, 239, 221)
GOLD = (201, 162, 39)
GOLDL = (238, 210, 122)
MUTED = (176, 169, 143)
FONTS = "C:/Windows/Fonts/"
SERIF = "georgia.ttf"; SERIF_B = "georgiab.ttf"; SERIF_I = "georgiai.ttf"; SANS = "arialbd.ttf"


def font(name, size):
    return ImageFont.truetype(FONTS + name, size)


def gold_mark(size, ss=4):
    """The vinyl brand mark in gold on transparent — composites cleanly over
    both the ink typographic cards and the photo backdrops (no dark box)."""
    S = size * ss
    cv = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(cv)
    c, R = S / 2, S / 2 - ss
    d.ellipse([c - R, c - R, c + R, c + R], fill=GOLD + (255,))       # gold record
    gw = max(2, int(S * 0.022))
    for f in (0.90, 0.775, 0.65, 0.525):                             # ink grooves
        r = R * f
        d.ellipse([c - r, c - r, c + r, c + r], outline=INK + (255,), width=gw)
    lr = R * 0.40
    d.ellipse([c - lr, c - lr, c + lr, c + lr], fill=INK + (255,))   # center label
    dr = R * 0.11
    d.ellipse([c - dr, c - dr, c + dr, c + dr], fill=GOLD + (255,))  # spindle dot
    return cv.resize((size, size), Image.LANCZOS)


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
    for size in (88, 76, 64, 54, 46, 40):
        f = font(SERIF_B, size)
        lines = wrap(draw, name, f, max_w)
        if len(lines) <= 2 and all(draw.textlength(l, font=f) <= max_w for l in lines):
            return f, lines
    f = font(SERIF_B, 40)
    return f, wrap(draw, name, f, max_w)[:2]


def center(draw, y, text, fnt, fill):
    w = draw.textlength(text, font=fnt)
    draw.text(((W - w) / 2, y), text, font=fnt, fill=fill)


def load_backdrop(src):
    try:
        im = Image.open(DESIGN / src).convert("RGB")
    except Exception:
        return None
    scale = max(W / im.width, H / im.height)
    im = im.resize((int(im.width * scale), int(im.height * scale)), Image.LANCZOS)
    left = (im.width - W) // 2
    top = (im.height - H) // 4          # bias toward the top (faces)
    im = im.crop((left, top, left + W, top + H))
    im = Image.blend(im, Image.new("RGB", (W, H), INK), 0.52)
    grad = Image.new("L", (1, H), 0)
    for y in range(H):
        grad.putpixel((0, y), int(246 * (max(0, y - H * 0.26) / (H * 0.74)) ** 1.15))
    grad = grad.resize((W, H))
    im = Image.composite(Image.new("RGB", (W, H), INK), im, grad)
    return im


def make_card(name, roles, no, lead, backdrop_src, out_path):
    photo = load_backdrop(backdrop_src) if backdrop_src else None
    img = photo if photo else Image.new("RGB", (W, H), INK)
    d = ImageDraw.Draw(img)

    d.rectangle([28, 28, W - 28, H - 28], outline=GOLD, width=2)

    mk = gold_mark(104)
    img.paste(mk, ((W - 104) // 2, 58), mk)
    center(d, 176, spaced("THE JERSEY CITY SOUND"), font(SANS, 22), GOLDL)

    max_w = W - 200
    fname, lines = fit_name(d, name, max_w)
    role_line = " · ".join(roles)
    lh = fname.size + 8
    block_h = lh * len(lines)
    y = (H - block_h) // 2 - 4 if not photo else H - 214 - block_h

    center(d, y - 44, spaced(f"ENTRY №. {no}", 1), font(SANS, 20), GOLD)
    for ln in lines:
        center(d, y, ln, fname, CREAM)
        y += lh
    if role_line:
        center(d, y + 6, role_line, font(SERIF_I, 28), MUTED)
        y += 46

    d.line([(W // 2 - 120, y + 26), (W // 2 + 120, y + 26)], fill=GOLD, width=2)

    if lead and not photo:
        snip = lead.strip()
        if len(snip) > 140:
            snip = snip[:140].rsplit(" ", 1)[0] + "…"
        yy = y + 58
        for ln in wrap(d, snip, font(SERIF, 26), max_w)[:2]:
            center(d, yy, ln, font(SERIF, 26), (222, 214, 190))
            yy += 36

    center(d, H - 92, spaced("jerseycitysound.com", 1), font(SANS, 24), CREAM)

    img.save(out_path)


def first_image(e):
    for g in e.get("galleries", []):
        if g.get("images"):
            return g["images"][0]["src"]
    return None


def main():
    data = json.loads((ROOT / "data" / "entries.json").read_text(encoding="utf-8"))
    entries = list(data["entries"])
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
    print(f"generated {n} OG cards -> {OUT}")


if __name__ == "__main__":
    main()
