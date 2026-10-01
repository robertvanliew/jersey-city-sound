# Seed place entries (type "place") into data/entries.json.
#
# Rule (build brief 4b): a place gets an entry only when the archive already holds two
# or more sourced music connections to it. Every fact below restates a sentence that
# already appears, with its source, in one of the connected entries; nothing is added
# from outside the record. Addresses and coordinates are filled by
# execution/set_place_geo.py from sourced research; left empty here.
#
# Idempotent: an entry whose slug already exists is left alone.
#
# Usage:  py execution/add_place_entries.py

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from entries_io import load_entries, save_entries  # noqa: E402

DOC_2006 = {"label": "WizTV Presents: The Jersey City DJ Documentary Vol. 1 (2006), WizTV upload",
            "url": "https://www.youtube.com/watch?v=uyX2waMUOJQ"}
CHILL_TOWN = {"label": "Chill Town J.C. Hip-Hop Documentary Film, dir. Champagne, YouTube",
              "url": "https://www.youtube.com/watch?v=ppgLMMQHDu8"}
MOPOP_SSS = {"label": "MoPOP Museum, Sweet, Slick and Sly Crew, Jersey City (flyer)",
             "url": "https://mopop.emuseum.com/objects/79166/sweet-slick-and-sly-crew-jersey-city"}
MOPOP_TURNOUT = {"label": "MoPOP Museum, Benmore presents The Turnout: Battle of '82 (flyer)",
                 "url": "https://mopop.emuseum.com/objects/83457/rosieb--benmore-presents-the-turnout-battle-of-82-demon-c"}
LINKED = {"label": "The connected entries linked on this page, each with its own numbered sources"}
WIKI_KOOL = {"label": "Wikipedia, Kool & the Gang", "url": "https://en.wikipedia.org/wiki/Kool_%26_the_Gang"}
WIKI_AKON = {"label": "Wikipedia, Akon", "url": "https://en.wikipedia.org/wiki/Akon"}

PLACES = [
    {
        "name": "Benmore Skating Rink", "slug": "benmore-skating-rink", "place_type": "skating rink",
        "roles": ["Skating rink", "Battle venue"], "genres": ["Hip-hop", "Old school"], "years_active": "c. 1982",
        "status": "doc-verified", "place_status": "closed",
        "facts": [
            "The Benmore Skating Rink was a roller rink on Communipaw Avenue in Jersey City that hosted the New Jersey versus Bronx DJ showdowns of the early 1980s, the events that put the city's park-jam generation on the same bills as New York's crews.",
            "DJ Stranger Dee and his crew performed at the rink's New Jersey vs. Bronx showdowns, including a January 15, 1982 showdown with the Cold Crush Brothers and the Turnout Battle of 82 on July 2, 1982, both preserved in flyers archived at the Museum of Pop Culture (MoPOP).",
            "A period flyer for The Showdown For All DJs at the Benmore, headlined by Grandmaster Flash imagery, bills Lord Sun Albee Al, Sweet Slick and Slide, Grand Wizard Capone and Killer Force alongside Strang D, Jimmy M, Sir Brown and the era's crews.",
        ],
        "sources": [MOPOP_TURNOUT, MOPOP_SSS, CHILL_TOWN, LINKED],
        "music_connections": [
            {"slug": "dj-stranger-dee", "note": "Performed at the rink's New Jersey vs. Bronx showdowns, including the January 15, 1982 showdown with the Cold Crush Brothers and the Turnout Battle of 82."},
            {"slug": "sweet-slick-and-slide", "note": "Billed at The Showdown For All DJs at the Benmore on a period flyer."},
            {"slug": "lord-sun-albee-al", "note": "Billed as Al Bee at The Showdown For All DJs at the Benmore."},
            {"slug": "grand-wizard-capone", "note": "Billed at The Showdown For All DJs at the Benmore."},
            {"slug": "killer-force", "note": "Named across the bill from Sweet S and Sly on The Showdown For All DJs flyer."},
        ],
        "todo_robert": ["Street address and the rink's years of operation", "Who ran the Benmore and when it closed"],
    },
    {
        "name": "Lincoln High School", "slug": "lincoln-high-school", "place_type": "school",
        "roles": ["Public high school"], "genres": ["Funk", "Soul", "Hip-hop"], "years_active": "1964 to present",
        "status": "web-verified", "place_status": "open",
        "facts": [
            "Lincoln High School is the Jersey City public high school where Kool & the Gang formed in 1964: brothers Robert 'Kool' Bell and Ronald Bell and five neighborhood friends who all attended the school.",
            "Founding members George Brown, Dennis 'Dee Tee' Thomas and Claydes Charles Smith attended Lincoln alongside the Bells; the group that grew from the school's scene went on to Billboard Hot 100 No. 1 singles.",
            "The school also sits in the city's DJ lineage: in the Chill Town J.C. Hip-Hop Documentary, DJ Count Basil is remembered as the DJ who first put DJ Wimpy Bee on at a Lincoln High School party.",
            "Mista Quietman's The 201 High School Anthem, a Jersey City rework of DJ Sliink's High School Anthem, calls out Lincoln along with Ferris, Dickinson and Snyder high schools.",
        ],
        "sources": [WIKI_KOOL, CHILL_TOWN, LINKED],
        "music_connections": [
            {"slug": "kool-and-the-gang", "note": "Formed in 1964 by Lincoln High School students."},
            {"slug": "robert-kool-bell", "note": "Co-founded Kool & the Gang with his brother Ronald Bell and five friends who all attended Lincoln."},
            {"slug": "george-brown", "note": "Founding drummer; attended Lincoln High School."},
            {"slug": "dennis-dee-tee-thomas", "note": "Founding saxophonist; attended Lincoln High School alongside the other founding members."},
            {"slug": "claydes-charles-smith", "note": "Founding guitarist of the group that grew from Lincoln's scene in 1964."},
            {"slug": "dj-count-basil", "note": "Put DJ Wimpy Bee on at a Lincoln High School party, per the Chill Town documentary."},
            {"slug": "dj-wimpy-bee", "note": "Got an early start at a Lincoln High School party, per the Chill Town documentary."},
            {"slug": "mista-quietman", "note": "Calls out Lincoln in The 201 High School Anthem."},
        ],
        "todo_robert": [],
    },
    {
        "name": "Henry Snyder High School", "slug": "snyder-high-school", "place_type": "school",
        "roles": ["Public high school"], "genres": ["Hip-hop", "R&B"], "years_active": "",
        "status": "web-verified", "place_status": "open",
        "facts": [
            "Henry Snyder High School is a Jersey City public high school with a documented line of musicians: Akon spent his high school years in the city at Snyder and Dickinson after the rest of his family moved to Atlanta.",
            "The operatic bass-baritone Peter Sliker, born in Jersey City, graduated from Henry Snyder High School before enlisting in the United States Navy in 1942.",
            "Zigimo is a graduate of the Jersey City Arts Program at Henry Snyder High School, where he trained on tuba and piano.",
            "Mista Quietman's The 201 High School Anthem calls out Snyder along with Lincoln, Ferris and Dickinson high schools.",
        ],
        "sources": [WIKI_AKON, LINKED],
        "music_connections": [
            {"slug": "akon", "note": "Attended Snyder High School (and Dickinson) during his high school years in Jersey City."},
            {"slug": "peter-sliker", "note": "Graduated from Henry Snyder High School."},
            {"slug": "zigimo", "note": "Graduate of the Jersey City Arts Program at Henry Snyder High School."},
            {"slug": "mista-quietman", "note": "Calls out Snyder in The 201 High School Anthem."},
        ],
        "todo_robert": [],
    },
    {
        "name": "Ferris High School", "slug": "ferris-high-school", "place_type": "school",
        "roles": ["Public high school"], "genres": ["Hip-hop", "Mixtapes"], "years_active": "",
        "status": "doc-verified", "place_status": "open",
        "facts": [
            "James J. Ferris High School is the Jersey City public high school that the 2006 WizTV documentary names as a producer of the mixtape scene's legends.",
            "In The Jersey City DJ Documentary Vol. 1 (2006), DJ DX credits Ferris High School as a producer of the scene's legends, and the film lists the school among the institutions of the scene alongside Rendezvous, the Boys Club, Lollipop and Taste.",
            "Mista Quietman's The 201 High School Anthem calls out Ferris along with Lincoln, Dickinson and Snyder high schools.",
        ],
        "sources": [DOC_2006, LINKED],
        "music_connections": [
            {"slug": "jersey-city-dj-documentary-2006", "note": "Names Ferris High School as a producer of scene legends."},
            {"slug": "dj-dx", "note": "Credited Ferris High School as a producer of the scene's legends in the 2006 documentary."},
            {"slug": "mista-quietman", "note": "Calls out Ferris in The 201 High School Anthem."},
        ],
        "todo_robert": ["Which Ferris alumni the documentary has in mind, by name, with timestamps", "DJ Wizard's Ferris connection (open item on his entry)"],
    },
    {
        "name": "Dickinson High School", "slug": "dickinson-high-school", "place_type": "school",
        "roles": ["Public high school"], "genres": ["Hip-hop", "R&B"], "years_active": "",
        "status": "web-verified", "place_status": "open",
        "facts": [
            "William L. Dickinson High School is a Jersey City public high school in the record through Akon, who spent his high school years in the city at Snyder and Dickinson after the rest of his family moved to Atlanta.",
            "Mista Quietman's The 201 High School Anthem calls out Dickinson along with Lincoln, Ferris and Snyder high schools.",
        ],
        "sources": [WIKI_AKON, LINKED],
        "music_connections": [
            {"slug": "akon", "note": "Attended Dickinson High School (and Snyder) during his high school years in Jersey City."},
            {"slug": "mista-quietman", "note": "Calls out Dickinson in The 201 High School Anthem."},
        ],
        "todo_robert": ["Further documented musicians who attended Dickinson"],
    },
    {
        "name": "Duncan Projects", "slug": "duncan-projects", "place_type": "housing",
        "roles": ["Public housing"], "genres": ["Hip-hop", "Old school"], "years_active": "c. 1980s",
        "status": "doc-verified", "place_status": "",
        "facts": [
            "The Duncan Projects, the public housing on Duncan Avenue in Jersey City, were home ground for one of the city's founding hip-hop crews.",
            "The Tranquilizing Three (also Tranquilizer 3) were an early Jersey City hip-hop crew out of the Duncan Projects, formed around 1980 from the earlier group Phase Three; by the account of peers they were one of only two Chilltown crews able to hold their own against New York's.",
            "Grand Wizard Capone names the Duncan Projects as his ground and appears in Duncan Projects reunion photographs with DJ Flash, both in Duncan Projects Jersey City shirts, preserved in this archive.",
        ],
        "sources": [CHILL_TOWN, LINKED],
        "music_connections": [
            {"slug": "tranquilizing-three", "note": "Early Jersey City hip-hop crew out of the Duncan Projects, formed around 1980."},
            {"slug": "grand-wizard-capone", "note": "Names the Duncan Projects as his ground; pictured in Duncan Projects reunion photographs."},
            {"slug": "dj-flash-jersey-city", "note": "Pictured with Grand Wizard Capone in the Duncan Projects reunion photographs."},
        ],
        "todo_robert": ["Official name of the development and whether it still stands", "Neighborhood assignment for the hub pages"],
    },
    {
        "name": "P.S. 11", "slug": "ps-11", "place_type": "school",
        "roles": ["Public school", "Party venue"], "genres": ["Hip-hop", "Old school"], "years_active": "c. 1980s",
        "status": "doc-verified", "place_status": "open",
        "facts": [
            "Public School 11 in Jersey City was one of the rooms where the city's early hip-hop happened: DJ Wimpy Bee's staple venue, and the site of an MC battle preserved in the Chill Town J.C. Hip-Hop Documentary.",
            "In the Chill Town documentary DJ Wimpy Bee recounts spinning nearly every venue in the city, with P.S. 11 School as his staple, alongside St. Patrick's, Sacred Heart, Foxes and the city's churches.",
            "Cool Sir Brown is documented in the same film competing in a landmark MC battle at P.S. 11, backed by a doo-wop harmony section arranged by his sister, the songwriter Mary Brown, who as a teenager wrote and arranged the backing harmonies that helped him win.",
        ],
        "sources": [CHILL_TOWN, LINKED],
        "music_connections": [
            {"slug": "dj-wimpy-bee", "note": "His staple venue, by his own account in the Chill Town documentary."},
            {"slug": "cool-sir-brown", "note": "Won a landmark MC battle at P.S. 11, documented in the Chill Town film."},
            {"slug": "mary-brown", "note": "Wrote and arranged the backing harmonies for her brother's P.S. 11 battle."},
        ],
        "todo_robert": ["Current name and address of P.S. 11", "Date of the MC battle"],
    },
    {
        "name": "Curries Woods", "slug": "curries-woods", "place_type": "housing",
        "roles": ["Public housing"], "genres": ["Hip-hop"], "years_active": "2010s to present",
        "status": "community-verified", "place_status": "open", "neighborhoods": ["Greenville"],
        "facts": [
            "Curries Woods, the public housing complex in the Greenville section of Jersey City, is the home ground named by several of the city's current rappers.",
            "Max YB represents the Curries Woods projects and the Uptop section; De$igner Boyz have roots across Curries Woods, Sal-Laf Courts, Bidwell and Ocean, and Lexington Avenue; PressureOnline, an artist and media figure, also represents Curries Woods.",
        ],
        "sources": [LINKED],
        "music_connections": [
            {"slug": "max-yb", "note": "Represents the Curries Woods projects and the Uptop section."},
            {"slug": "designer-boyz", "note": "Roots across Curries Woods, Sal-Laf Courts, Bidwell and Ocean, and Lexington Avenue."},
            {"slug": "pressureonline", "note": "Represents the Curries Woods projects."},
        ],
        "todo_robert": ["A dated release, flyer or performance for each connected artist", "History of the complex (built, redeveloped) from a city or JCHA source"],
    },
    {
        "name": "Kool & the Gang Way", "slug": "kool-and-the-gang-way", "place_type": "street",
        "roles": ["Street", "Honorary street name"], "genres": ["Funk", "Soul"], "years_active": "2016 to present",
        "status": "web-verified", "place_status": "open",
        "facts": [
            "Kool & the Gang Way is the honorary name given in 2016 to the section of Maple Street in Jersey City where Robert 'Kool' Bell and his bandmates grew up.",
            "The city renamed the block in the group's honor in 2016; the founding members had formed Kool & the Gang in Jersey City in 1964 as Lincoln High School students, and the group's catalog is among the most sampled in music history.",
        ],
        "sources": [WIKI_KOOL, {"label": "Wikipedia, Robert \"Kool\" Bell", "url": "https://en.wikipedia.org/wiki/Robert_%22Kool%22_Bell"}, LINKED],
        "music_connections": [
            {"slug": "kool-and-the-gang", "note": "The block was renamed in the group's honor in 2016."},
            {"slug": "robert-kool-bell", "note": "Grew up on this section of Maple Street with his bandmates."},
            {"slug": "lincoln-high-school", "note": "The school the founding members attended, a short walk from the block."},
        ],
        "todo_robert": ["Cross streets of the renamed block and the date of the ceremony, from city coverage"],
    },
]


def main():
    data = load_entries()
    entries = data["entries"]
    have = {e["slug"] for e in entries}
    next_no = max(int(e["entry_no"]) for e in entries) + 1
    added = []
    for p in PLACES:
        if p["slug"] in have:
            continue
        e = {"entry_no": f"{next_no:03d}", "name": p["name"], "slug": p["slug"], "type": "place",
             "place_type": p["place_type"], "status": p["status"], "roles": p["roles"], "genres": p["genres"],
             "years_active": p["years_active"], "origin": "Jersey City, New Jersey",
             "address": "", "lat": None, "lng": None, "place_status": p["place_status"],
             "facts": p["facts"], "sources": p["sources"], "music_connections": p["music_connections"],
             "todo_robert": p["todo_robert"], "links": {}}
        if p.get("neighborhoods"):
            e["neighborhoods"] = p["neighborhoods"]
        entries.append(e)
        added.append((e["entry_no"], e["name"]))
        next_no += 1
    save_entries(data)
    for no, name in added:
        print(f"added {no} {name}")
    print(f"{len(added)} place entries added")


if __name__ == "__main__":
    main()
