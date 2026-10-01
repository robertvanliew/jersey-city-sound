# Fill address, coordinates, status and the sourced history of the place entries.
#
# Every value below comes from a fetched source named next to it (research pass of
# 2026-10-01; Nominatim/OpenStreetMap for coordinates). Places with no findable
# source keep empty fields. Re-runnable: it sets the listed fields and appends a
# fact or source only if that text is not already present.
#
# Usage:  py execution/set_place_geo.py

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from entries_io import load_entries, save_entries  # noqa: E402

GEO = {
    "lincoln-high-school": {
        "address": "60 Crescent Avenue, Jersey City, NJ 07304", "lat": 40.717363, "lng": -74.070515,
        "place_status": "open",
        "sources": [{"label": "Wikipedia, Lincoln High School (New Jersey)", "url": "https://en.wikipedia.org/wiki/Lincoln_High_School_(New_Jersey)"}],
    },
    "snyder-high-school": {
        "address": "239 Bergen Avenue, Jersey City, NJ 07305", "lat": 40.710444, "lng": -74.083847,
        "place_status": "open",
        "sources": [{"label": "Wikipedia, Henry Snyder High School", "url": "https://en.wikipedia.org/wiki/Henry_Snyder_High_School"}],
    },
    "ferris-high-school": {
        "address": "35 Colgate Street, Jersey City, NJ 07302", "lat": 40.720845, "lng": -74.053948,
        "place_status": "open",
        "sources": [{"label": "Wikipedia, James J. Ferris High School", "url": "https://en.wikipedia.org/wiki/James_J._Ferris_High_School"},
                    {"label": "James J. Ferris High School, contact page (Jersey City Public Schools)", "url": "https://jfhs.jcboe.org/apps/contact/"}],
    },
    "dickinson-high-school": {
        "address": "2 Palisade Avenue, Jersey City, NJ 07306", "lat": 40.73000, "lng": -74.05389,
        "place_status": "open",
        "facts": ["The school opened in 1906."],
        "sources": [{"label": "Wikipedia, William L. Dickinson High School", "url": "https://en.wikipedia.org/wiki/William_L._Dickinson_High_School"}],
    },
    "ps-11": {
        "address": "886 Bergen Avenue, Jersey City, NJ 07306", "lat": 40.7291875, "lng": -74.0649984,
        "place_status": "open",
        "facts": ["Today the school is Martin Luther King, Jr. School, PS #11, a pre-kindergarten to grade 8 school of the Jersey City Public Schools at 886 Bergen Avenue."],
        "card": [{"label": "Also known as", "value": "Martin Luther King, Jr. School, PS #11"}],
        "sources": [{"label": "Martin Luther King, Jr. School, PS #11 (Jersey City Public Schools)", "url": "https://ps11.jcboe.org/apps/pages/index.jsp?uREC_ID=1535306&type=d&pREC_ID=1666252"}],
    },
    "curries-woods": {
        "address": "3 New Heckman Drive, Jersey City, NJ 07305", "lat": 40.689030, "lng": -74.095570,
        "place_status": "open",
        "facts": ["Built by the Jersey City Housing Authority in 1959 in the southern end of Greenville, bordering Bayonne, the complex was rebuilt under the federal HOPE VI program: six of the original towers were demolished and the development completed in 2005 consists of 204 two-story townhouses and one rehabilitated original 13-story building."],
        "sources": [{"label": "Wikipedia, Curries Woods", "url": "https://en.wikipedia.org/wiki/Curries_Woods"},
                    {"label": "Urban Omnibus, Hard Units: a drive through Jersey City with Brian Loughlin (2014)", "url": "https://urbanomnibus.net/2014/06/hard-units-a-drive-through-jersey-city-with-brian-loughlin/"},
                    {"label": "ProPublica HUD property record, Curries Woods (Housing Authority City of Jersey City)", "url": "https://projects.propublica.org/hud/properties/NJ009000008"}],
    },
    "duncan-projects": {
        "address": "330 Duncan Avenue, Jersey City, NJ 07306 (site of the former towers)", "lat": 40.7295791, "lng": -74.0829099,
        "place_status": "demolished",
        "facts": ["Officially the A. Harry Moore Houses, the development was a seven-tower, 664-unit public housing project built in 1954 and known locally as Duncan Towers. The Jersey City Housing Authority adopted a HOPE VI plan in 2005; the towers were demolished and replaced by the Gloria Robinson Court Homes, whose four phases were complete by 2016."],
        "card": [{"label": "Also known as", "value": "A. Harry Moore Houses; Duncan Towers"}],
        "sources": [{"label": "Pennrose, Gloria Robinson Court Homes III and IV (project history)", "url": "https://www.pennrose.com/portfolio/gloria-robinson-court-homes-iii-iv-1/"},
                    {"label": "HUD, HOPE VI demolition grant for A. Harry Moore Houses (June 4, 2004)", "url": "https://archives.hud.gov/local/nj/news/pr2004-06-04.cfm"},
                    {"label": "Urban Omnibus, Hard Units: a drive through Jersey City with Brian Loughlin (2014)", "url": "https://urbanomnibus.net/2014/06/hard-units-a-drive-through-jersey-city-with-brian-loughlin/"}],
    },
    "kool-and-the-gang-way": {
        # Maple Street centerline point (OpenStreetMap); the street is about 300 m long and the
        # named block lies on it, so the pin is within the block, marked approximate on the page
        "address": "Maple Street between Pacific Avenue and Whiton Street, Jersey City, NJ 07304", "lat": 40.7129, "lng": -74.0599,
        "geo_note": "approximate (street centerline)",
        "place_status": "open",
        "facts": ["The renamed block is Maple Street between Pacific Avenue and Whiton Street, near the apartment above a dry cleaner where the band members once lived. The sign went up at a ceremony on April 29, 2016 at the corner of Pacific Avenue and Maple Street, with Robert 'Kool' Bell, Ronald Bell, Dennis Thomas and George Brown present alongside Mayor Steven Fulop and members of the city council."],
        "sources": [{"label": "NJArts, Jersey City street to be renamed Kool & the Gang Way (April 28, 2016)", "url": "https://www.njarts.net/jersey-city-street-to-be-renamed-kool-the-gang-way/"},
                    {"label": "Hudson County View, Jersey City street gets named after Kool & the Gang (April 29, 2016)", "url": "https://hudsoncountyview.com/not-too-kool-for-jersey-city-street-gets-named-after-kool-the-gang/"},
                    {"label": "Hoboken Girl, Kool & the Gang: the Jersey City band's history", "url": "https://www.hobokengirl.com/kool-and-the-gang-jersey-city-band-history/"}],
    },
    "benmore-skating-rink": {
        # no address or status found in any source; the flyers place it on Communipaw Avenue
        "address": "", "lat": None, "lng": None, "place_status": "",
    },
}


def main():
    data = load_entries()
    by = {e["slug"]: e for e in data["entries"]}
    for slug, g in GEO.items():
        e = by.get(slug)
        if not e:
            print("missing entry:", slug)
            continue
        for k in ("address", "lat", "lng", "place_status", "geo_note"):
            if k in g:
                e[k] = g[k]
        for f in g.get("facts", []):
            if f not in e["facts"]:
                e["facts"].append(f)
        for c in g.get("card", []):
            e.setdefault("card", [])
            if not any(x["label"] == c["label"] for x in e["card"]):
                e["card"].append(c)
        have = {s.get("url") for s in e["sources"]}
        for s in g.get("sources", []):
            if s["url"] not in have:
                # keep the "linked entries" note last
                tail = [x for x in e["sources"] if not x.get("url")]
                e["sources"] = [x for x in e["sources"] if x.get("url")] + [s] + tail
        print("set", slug)
    save_entries(data)


if __name__ == "__main__":
    main()
