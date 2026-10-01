# Entry 013, The Jersey City DJ Documentary Vol. 1 (2006): embed the director's own
# public upload, and add the on-camera segments list from the archive roster with
# [TIMESTAMP] placeholders for the editor to fill (format h:mm:ss or mm:ss). Once a
# timestamp is filled the generator links the row to the embed at that time.
#
# Both uploads were checked with YouTube's oEmbed endpoint on 2026-10-01 and are public.
# Idempotent. Usage:  py execution/update_documentary_entry.py

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from entries_io import load_entries, save_entries  # noqa: E402

SLUG = "jersey-city-dj-documentary-2006"

VIDEO = {
    "id": "uyX2waMUOJQ",
    "title": "Wiztv Presents The Jersey City DJ Documentary Vol. 1 (2006)",
    "caption": "The full documentary, from the director's WizTV channel. A second preserved upload is on The Real Mista Quietman channel.",
    "upload_date": "2006",
    "duration": "PT2H57M58S",
}

# Interviewed on camera, per JCS-ARCHIVE-ROSTER.md; slug where the archive has an entry
SEGMENTS = [
    ("DJ Flash", "dj-flash-jersey-city"), ("Mista Quietman", "mista-quietman"), ("Mark Cee (Mark C)", "mark-cee"),
    ("Styles 007 (DJ 007)", "dj-007"), ("DJ Mad Money (Man Money)", "dj-mad-money"),
    ("DJ E Double (Double Platinum Entertainment)", "dj-e-double"), ("DJ BigTime (Big Time)", "dj-bigtime"),
    ("DJ Dolo", "dj-dolo"), ("DJ DX", "dj-dx"), ("X5", "x5"), ("Chameleon (Ka-Million)", "chameleon-ka-million"),
    ("DJ Semaj (transcribed as DJ Simmons)", "dj-semaj"), ("DJ Madden", "dj-madden"), ("Benito", "benito"),
    ("Joe Bananas", "joe-bananas"), ("Blaze (Blaze-In-Arts), cover designer", "blaze-in-arts"),
    ("Sean, organizer of the 2000 Winterblaze battle", ""), ("House B aka Bob Charlie (outro)", ""),
    ("DJ Savage (battle footage)", ""),
]


def main():
    data = load_entries()
    e = next(x for x in data["entries"] if x["slug"] == SLUG)
    if not any(v.get("id") == VIDEO["id"] for v in e.get("videos", [])):
        e["videos"] = [VIDEO]
    if not e.get("segments"):
        e["segments"] = [{"name": n, "slug": s, "timestamp": "[TIMESTAMP]"} for n, s in SEGMENTS]
    save_entries(data)
    print("updated", SLUG, "videos:", len(e["videos"]), "segments:", len(e["segments"]))


if __name__ == "__main__":
    main()
