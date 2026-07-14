# Knock the opaque background out of the wordmark PNGs so the logo sits
# cleanly on any page color. Produces two overlay assets from the source art:
#   jerseycitysound-ink.png    - ink wordmark, transparent bg (light pages)
#   jerseycitysound-cream.png  - cream wordmark, transparent bg (dark/memorial)
#
# The shipped -transparent / -transparent-light / -reversed files carry a baked
# background box; these generated files fix that. Re-run if source art changes.
#
# Usage:  py execution/make_transparent_logos.py

from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "design" / "assets"


def knockout(src_name, out_name, near, thresh=60):
    """Make pixels close to `near` (r,g,b) fully transparent."""
    img = Image.open(ASSETS / src_name).convert("RGBA")
    px = img.load()
    w, h = img.size
    nr, ng, nb = near
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if abs(r - nr) < thresh and abs(g - ng) < thresh and abs(b - nb) < thresh:
                px[x, y] = (r, g, b, 0)
    img.save(ASSETS / out_name)
    print(f"wrote {out_name}")


# primary = ink wordmark on WHITE box -> knock out white -> ink on transparent
knockout("jerseycitysound-primary.png", "jerseycitysound-ink.png", (255, 255, 255))
# reversed = cream wordmark on BLACK box -> knock out black -> cream on transparent
knockout("jerseycitysound-reversed.png", "jerseycitysound-cream.png", (14, 14, 16), thresh=40)
