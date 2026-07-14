# Promote the community-documented Jersey City hip-hop names (the Hardwood
# Classics artist/female/legends editions, staged in
# discovered_candidates.community_documentation_review) into full entries.
#
# Already-built names (Kenny Kenn, Rigga Mortis, Revenue Wrong, Apache, Akon,
# Double X Posse, Heather B. Gardner) are skipped.
#
# Usage:  py execution/add_community_entries.py

import json
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data" / "entries.json"
RESEARCH = {"label": "Archive research: The Jersey City Sound, 2026"}

# (name, slug, type, roles, genres, [facts], optional extra source url)
NEW = [
    # ---- groups ----
    ("De$igner Boyz", "designer-boyz", "group", ["Hip-hop group"], ["Hip-hop"], [
        "De$igner Boyz are a Jersey City hip-hop group with roots across Curries Woods, Sal-Laf Courts, Bidwell & Ocean, and Lexington Avenue",
        "Their catalog, produced largely by Uncle YG and Herogawd, includes “Mama Rich,” “Fine$$er,” and “Do or Die 2 & 3”",
    ], None),
    ("Manymen Records", "manymen-records", "group", ["Record label", "Collective"], ["Hip-hop"], [
        "Manymen Records (MMR) is a Jersey City hip-hop label and collective that anchored a controlled club and party scene in the city",
        "Its roster and affiliates included Dibiasi, Kamillion, Allout, Illanoise, P Dot, and D Eastwood, with production led by DJ Kamillion and Illanoise",
    ], None),
    ("The Heat", "the-heat", "group", ["Hip-hop group"], ["Hip-hop"], [
        "The Heat are a Jersey City hip-hop group out of the Montgomery Projects",
        "Members documented in the community record include Crisis, Panic, and Monroe",
    ], None),
    ("Bralikk Animalz", "bralikk-animalz", "group", ["Hip-hop group"], ["Hip-hop"], [
        "Bralikk Animalz are a Jersey City hip-hop crew associated with the L.E.X. and C Dub areas",
        "Documented members include Sam Black, Frank Money, Ock, Streets, Rico, and Chizzy",
    ], None),
    ("Block Royal", "block-royal", "group", ["Hip-hop group"], ["Hip-hop"], [
        "Block Royal are a Jersey City hip-hop group out of The Heights, led by Roberto “Tito” Montanez",
        "Community documentation associates the group with figures including Akon, Joell Ortiz, and Fury",
    ], None),
    ("The Cobras", "the-cobras", "group", ["Hip-hop group"], ["Hip-hop"], [
        "The Cobras are a Jersey City hip-hop group repping Downtown Jersey City, Communipaw, and Lafayette",
        "The group is documented as Mafi, 4DaBread, and Jefe",
    ], None),
    # ---- individuals ----
    ("KS (Mr Xtortion)", "ks-mr-xtortion", "person", ["Rapper"], ["Hip-hop"], [
        "KS, also known as Mr Xtortion, is a Jersey City rapper affiliated with the Black Congress team",
        "He is documented as a 106 & Park Freestyle Friday champion, known for aggression, bully bars, and freestyles",
    ], None),
    ("Ruga", "ruga", "person", ["Rapper"], ["Hip-hop"], [
        "Ruga is a Jersey City rapper affiliated with the Team Fetti and Section 8 crews",
        "He is documented as a BET 106 & Park Freestyle Friday champion and as undefeated in the JC Hunger Games battle league, known for metaphors and punchlines",
    ], None),
    ("Lil Dev", "lil-dev", "person", ["Rapper"], ["Hip-hop"], [
        "Lil Dev is a Jersey City rapper affiliated with the Greazy Gang",
        "The community record documents him for lyrics, wordplay, aggression, and energy, with millions of streams on Apple Music",
    ], None),
    ("Max YB", "max-yb", "person", ["Rapper"], ["Hip-hop"], [
        "Max YB is a Jersey City rapper representing the Curries Woods projects and the Uptop section",
        "He appears alongside DJ Swill B in the city's recent hip-hop catalog and is documented for versatility, energy, hunger, and passion",
    ], None),
    ("DamnGirll", "damngirll", "person", ["Rapper"], ["Hip-hop"], [
        "DamnGirll is a Jersey City rapper documented for bars, charisma, attitude, and style",
        "Documented songs include “Honestly,” “Baddie,” and “Who Run It”",
    ], None),
    ("Dibiasi", "dibiasi", "person", ["Rapper"], ["Hip-hop"], [
        "Dibiasi is a Jersey City rapper representing Stegman Avenue and affiliated with Manymen Records (MMR)",
        "The community record documents him for cockiness, charisma, bars, and work ethic",
    ], None),
    ("MrCashedOut", "mrcashedout", "person", ["Rapper"], ["Hip-hop"], [
        "MrCashedOut is a Jersey City rapper affiliated with the MBF crew",
        "He is documented for hunger, pain, substance, and determination",
    ], None),
    ("PressureOnline", "pressureonline", "person", ["Artist", "Media"], ["Hip-hop"], [
        "PressureOnline is a Jersey City artist and media figure representing the Curries Woods projects",
        "He is documented for lyrical ability, aggression, work output, and punchlines, and operates the outlet pressureonline.com",
    ], "https://pressureonline.com"),
    ("Big Spanish", "big-spanish", "person", ["Rapper"], ["Hip-hop"], [
        "Big Spanish is a Jersey City rapper representing the Nu Houses",
        "He is documented for hunger, aggression, work ethic, and determination",
    ], None),
    ("Mali G", "mali-g", "person", ["Rapper"], ["Hip-hop"], [
        "Mali G is a Jersey City rapper representing the Nu Houses",
        "He is documented for flow, wittiness, hunger, and grind",
    ], None),
    ("1stLady EL", "1stlady-el", "person", ["Party promoter"], ["Hip-hop"], [
        "1stLady EL is a Jersey City party promoter documented as a queen of the city's party scene",
        "Affiliated with the Murda Mamis, she is credited with over a decade of events, connections, and culture — from small rooms to sold-out nights — supporting female artists",
    ], None),
    ("Taylor Portt", "taylor-portt", "person", ["Rapper"], ["Hip-hop"], [
        "Taylor Portt is a Jersey City rapper whose past teams include Manymen Records (MMR) and ZoneOutMusic",
        "She is documented for elite bars, aggression, and freestyles",
    ], None),
    ("Jade", "jade", "person", ["Vocalist"], ["R&B", "Hip-hop"], [
        "Jade is a Jersey City vocalist affiliated with Manymen Records (MMR), remembered as a signature voice of the city's mixtape era",
        "Her documented work includes the acappella “Over You”",
    ], None),
    ("Suzy Q", "suzy-q", "person", ["Vocalist"], ["R&B"], [
        "Suzy Q is a Jersey City singer documented for longevity, vocal gift, and passion",
        "The community record describes her as a voice with a timeless sound that continues to inspire",
    ], None),
    ("Montana Dess", "montana-dess", "person", ["Rapper"], ["Hip-hop"], [
        "Montana Dess is a Jersey City rapper documented for flow, aggressive lyrics, and appeal",
        "The community record describes her wordplay, delivery, and stage presence",
    ], None),
    ("Benny Blanca", "benny-blanca", "person", ["Artist"], ["Hip-hop"], [
        "Benny Blanca is a Jersey City artist affiliated with Fairmount Music",
        "Her documented work includes the song “Locked In,” with the community record citing appeal, bars, and work ethic",
    ], None),
    ("Nina Foxx", "nina-foxx", "person", ["Vocalist"], ["R&B", "Hip-hop"], [
        "Nina Foxx is a Jersey City artist affiliated with the Grindhouse (HBIC)",
        "She is documented as having toured with Fantasia, known for confidence and command on stage",
    ], None),
    ("J-Sass", "j-sass", "person", ["Rapper"], ["Hip-hop"], [
        "J-Sass is a Jersey City rapper affiliated with the TRMz crew",
        "She is documented for clever, aggressive lyrics and work ethic",
    ], None),
    ("Mariah Lynn", "mariah-lynn", "person", ["Artist"], ["Hip-hop"], [
        "Mariah Lynn is a Jersey City independent artist",
        "Her documented work includes the song “Once Upon a Time,” with the community record citing work ethic, confidence, and energy",
    ], None),
    ("DidThatt", "didthatt", "person", ["Rapper"], ["Hip-hop"], [
        "DidThatt is a Jersey City independent rapper working in a pain-music lane",
        "She is documented for aggression, energy, and work ethic",
    ], None),
]


def main():
    d = json.loads(DATA.read_text(encoding="utf-8"))
    existing = {e["slug"] for e in d["entries"]}
    names = {e["name"].lower() for e in d["entries"]}
    next_no = max(int(e["entry_no"]) for e in d["entries"]) + 1

    added = 0
    for name, slug, etype, roles, genres, facts, url in NEW:
        if slug in existing or name.lower() in names:
            continue
        sources = [RESEARCH]
        if url:
            sources.insert(0, {"label": f"{name} — official site", "url": url})
        entry = {
            "entry_no": f"{next_no:03d}",
            "name": name,
            "slug": slug,
            "status": "community-verified",
            "roles": roles,
            "genres": genres,
            "years_active": "",
            "facts": facts,
            "sources": sources,
            "todo_robert": ["Instagram handle and receipts (streams, releases, video)",
                            "Era, key songs, and crew detail from memory", "Photo permission"],
            "links": {},
        }
        if etype == "group":
            entry["type"] = "group"
        d["entries"].append(entry)
        next_no += 1
        added += 1

    json.dump(d, open(DATA, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(f"added {added} community entries; archive now {len(d['entries'])} entries")


if __name__ == "__main__":
    main()
