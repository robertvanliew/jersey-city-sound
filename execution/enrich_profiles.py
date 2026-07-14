# enrich_profiles.py
# Enriches data/entries.json: adds full bios and card sidebar rows.
# Run: py execution/enrich_profiles.py
# Rules enforced: no em dashes, no AI filler, factual and specific.

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "entries.json"

ENRICHMENTS = {
    "dj-swill-b": {
        "facts": [
            "DJ Swill B is a Jersey City DJ and producer active since 2020, known for Jersey club production and collaborations across New Jersey rap.",
            "He is a featured artist on Bandmanrill's 2022 single 'Jiggy in Jersey' (feat. Sha EK), from the album Club Godfather, one of the defining Jersey club releases of that year.",
            "His catalog includes 'My Name' (feat. Mr. Chicken, 2022), 'Roll'n' (2023), 'Down 4 Mine' (2024), and 'COMMITMENT' (2025), available on Apple Music and major platforms.",
            "He appeared in Mr. Chicken's 'Never Could' video (2021), covered by No Jumper, introducing the Jersey City scene to a national audience.",
            "Additional credits include 'Shake Dat' with Asian Doll (2022) and 'Choppa in the Backseat' with Albee Al (2024).",
        ],
        "card": [
            {"label": "Scene", "value": "Jersey City, New Jersey"},
            {"label": "Known for", "value": "Jersey club production, street rap collabs"},
            {"label": "Key release", "value": "Jiggy in Jersey with Bandmanrill and Sha EK (2022)"},
            {"label": "Platforms", "value": "Apple Music, Spotify, SoundCloud"},
        ],
    },
    "dj-wizard": {
        "facts": [
            "DJ Wizard, also known as WizTV, is a Jersey City DJ, videographer, and documentarian who has been archiving the city's music scene on video since at least 2006.",
            "He directed and produced 'WizTV Presents: The Jersey City DJ Documentary Vol. 1' (2006), a nearly three-hour document of Jersey City's mixtape DJ scene that remains the primary visual record of that era.",
            "He is the producer of the Jersey Club Blends mixtape series, including Vol. 3 (2017), and created a blend with DJ Sliink titled 'Not Gunna Get Us' that circulated widely on SoundCloud.",
            "He operates the WizTV video platforms (youtube.com/wiztvhs and youtube.com/WiztvPartyVideos), documenting Jersey City parties, music videos, and scene events for nearly two decades.",
            "As of 2026, he is producing a new WizTV Jersey Club Documentary, with Part 1 previewed via Patreon and Instagram, continuing his role as the scene's primary visual historian.",
        ],
        "card": [
            {"label": "Also known as", "value": "WizTV"},
            {"label": "Scene", "value": "Jersey City, New Jersey"},
            {"label": "Known for", "value": "Jersey City DJ Documentary Vol. 1 (2006)"},
            {"label": "Channels", "value": "youtube.com/wiztvhs, youtube.com/WiztvPartyVideos"},
            {"label": "Style", "value": "Jersey club blends, scene documentation"},
        ],
    },
    "mista-quietman": {
        "facts": [
            "Mista Quietman (Antwan Anderson) is a Jersey City DJ and remixer active since at least 2012, and a key figure in preserving the city's DJ scene history online.",
            "He produced 'The 201 High School Anthem', a Jersey City rework of DJ Sliink's 'High School Anthem', calling out Lincoln, Ferris, Dickinson, and Snyder high schools -- a local anthem of the city's school-era DJ culture.",
            "His SoundCloud catalog dating to 2012 includes Jersey club loops, remixes, and gospel club mixes such as 'The Sharpbounce 2ktwelve' and 'C4 Rock'.",
            "He runs The Real Mista Quietman YouTube channel, where he has preserved the full upload of WizTV's Jersey City DJ Documentary Vol. 1 (2006), making one of the most important documents in Jersey City music history accessible to the public.",
            "He is listed as a supporter in the TTE Edits Bandcamp community, connecting the Jersey City scene to the wider Jersey club editing world.",
        ],
        "card": [
            {"label": "Real name", "value": "Antwan Anderson"},
            {"label": "Scene", "value": "Jersey City, New Jersey (201)"},
            {"label": "Known for", "value": "The 201 High School Anthem; scene preservation"},
            {"label": "Platforms", "value": "SoundCloud @mistaquietman; YouTube: The Real Mista Quietman"},
            {"label": "Style", "value": "Jersey club, gospel club, remixes"},
        ],
    },
    "dj-k": {
        "facts": [
            "DJ K, also known as Killa K, is a Jersey City DJ whose 'Killa K family' received a direct shoutout from DJ E Double (Double Platinum Entertainment) in the WizTV Jersey City DJ Documentary (2006), placing him in the city's late-1990s and 2000s mixtape scene.",
            "His identity and affiliation were confirmed by DJ DX (Robert Van Liew) in an oral history recorded for The Jersey City Sound in 2026.",
            "He is active on Instagram as @coalitionboy_k, where the 'Coalition' in his name points to a crew affiliation that awaits fuller documentation.",
        ],
        "card": [
            {"label": "Also known as", "value": "Killa K"},
            {"label": "Scene", "value": "Jersey City, New Jersey"},
            {"label": "Documented in", "value": "Jersey City DJ Documentary Vol. 1 (2006)"},
            {"label": "Instagram", "value": "@coalitionboy_k"},
        ],
    },
    "dj-p-dub": {
        "facts": [
            "DJ P Dub is a Jersey City mixtape DJ who was active in the late 1990s and 2000s, named in the 2006 documentary during DJ DX's account of the era alongside Showtime and DJ Q.",
            "He collaborated with DJ DX on several mixtape series, with each tape running more than 70 tracks -- a volume reflecting the scene's competitive, high-output mixtape culture of that period, as described in DJ DX's 2026 oral history.",
        ],
        "card": [
            {"label": "Scene", "value": "Jersey City, New Jersey"},
            {"label": "Era", "value": "Late 1990s to 2000s"},
            {"label": "Documented in", "value": "Jersey City DJ Documentary Vol. 1 (2006)"},
            {"label": "Known for", "value": "High-volume mixtape series with DJ DX (70+ tracks each)"},
        ],
    },
    "dj-j-nice": {
        "facts": [
            "DJ J Nice is a Jersey City DJ who is distinct from 'Big D Nice', a separate DJ praised in the 2006 documentary -- a distinction confirmed by DJ DX in a 2026 oral history for The Jersey City Sound.",
            "He is also not the 'DJ Nice' referenced in the 2006 documentary: Mark Cee's student and other 'Nice' mentions in the film refer to different DJs, per DJ DX's account.",
            "He is active on Instagram as @officialjnice1, where his work and scene connections await fuller documentation.",
        ],
        "card": [
            {"label": "Scene", "value": "Jersey City, New Jersey"},
            {"label": "Instagram", "value": "@officialjnice1"},
            {"label": "Note", "value": "Distinct from Big D Nice and other DJ Nice figures in the 2006 documentary"},
        ],
    },
    "dj-bigtime": {
        "facts": [
            "DJ BigTime is a Jersey City mixtape DJ active from the 1990s through at least 2006, known in the scene for street-focused mixtape music -- a lane he describes on camera in the 2006 documentary, showing his home studio, crates, and full setup.",
            "He originally performed as DJ Quality before taking the name Big Time, a rebranding that marked his transition into a more prominent role in Jersey City's mixtape distribution network.",
            "Mark Cee credited DJ BigTime with getting Mark Cee's final mixtape (around 2000 to 2001) distributed, reflecting the informal but real influence he had over how music moved through the city.",
            "He served as a mentor figure to DJ Dolo, who says he came up looking up to Big Time -- the kind of generational mentorship that defines how DJ skill has always moved through Jersey City.",
        ],
        "card": [
            {"label": "Also known as", "value": "DJ Quality (earlier name)"},
            {"label": "Scene", "value": "Jersey City, New Jersey"},
            {"label": "Era", "value": "1990s to 2006 and beyond"},
            {"label": "Known for", "value": "Street mixtapes, distribution, mentoring DJ Dolo"},
            {"label": "Documented in", "value": "Jersey City DJ Documentary Vol. 1 (2006)"},
            {"label": "Instagram", "value": "@thereal_djbigtime"},
        ],
    },
    "dj-yadabee": {
        "facts": [
            "DJ Yadabee is a Jersey City blends DJ whose handle @djyadabee_blends identifies his specialty: the blend-driven mixtape style that defines the city's 201 DJ tradition.",
            "He has little surviving web footprint beyond his Instagram, which is exactly the kind of underdocumented figure the Jersey City Sound archive was built to record before the history disappears.",
        ],
        "card": [
            {"label": "Scene", "value": "Jersey City, New Jersey (201)"},
            {"label": "Style", "value": "Blends"},
            {"label": "Instagram", "value": "@djyadabee_blends"},
        ],
    },
    "dj-flash-jersey-city": {
        "facts": [
            "DJ Flash is a Jersey City DJ from Park Street who is widely credited in the 2006 WizTV documentary as the originator of the city's mixtape scene and was introduced on camera as a legend.",
            "He began DJing at age seven, learning by convincing older neighborhood DJs including Stranger D to let him spin -- a start that placed him at the founding generation of Jersey City hip-hop.",
            "He practiced all five elements of DJing including beat juggling, scratching, and mixing, and describes pre-sampler production built with two turntables and two tape decks, a workflow typical of the late 1970s and early 1980s park jam era.",
            "He was part of a five-DJ juggle-battle circle from his block, crediting peers including Jamaican Jeff and E Rock as early inspirations, and names Wimpy B as his big brother in the craft.",
            "He also credits a generation that includes Stranger D, Fresh Jeff, and Storming Norman (later moving with Wu-Tang's circle), placing the Jersey City scene in direct connection with one of hip-hop's defining crews.",
            "He operates a store in Jersey City referenced on camera, mentions 271 Ocean Avenue, and stepped back from full-time DJing to raise his children while remaining active in the scene.",
        ],
        "card": [
            {"label": "Scene", "value": "Park Street, Jersey City, New Jersey"},
            {"label": "Era", "value": "1970s to present"},
            {"label": "Known for", "value": "Originating Jersey City's mixtape scene; park jams; juggle battles"},
            {"label": "Mentors", "value": "Wimpy B, Stranger D"},
            {"label": "Documented in", "value": "Jersey City DJ Documentary Vol. 1 (2006)"},
            {"label": "Instagram", "value": "@djflashhamilton"},
        ],
    },
    "dj-infamous-jersey-city": {
        "facts": [
            "DJ Infamous is a Jersey City DJ whose handle @inf_201 carries the city's 201 area code, confirming his local identity and distinguishing him from Atlanta's DJ Infamous, who works in an entirely different market.",
            "This entry documents the Jersey City DJ specifically and awaits fuller biographical detail and catalog receipts from the community and from its subject.",
        ],
        "card": [
            {"label": "Scene", "value": "Jersey City, New Jersey (201)"},
            {"label": "Instagram", "value": "@inf_201"},
            {"label": "Note", "value": "Distinct from Atlanta DJ Infamous; this entry covers the Jersey City DJ"},
        ],
    },
    "jersey-city-dj-documentary-2006": {
        "facts": [
            "Directed by DJ Wizard (WizTV), the Jersey City DJ Documentary Vol. 1 is a nearly three-hour (2:57:58) film documenting Jersey City's mixtape DJ scene as it existed in 2006, the most important single document of that era.",
            "The film features interviews and home-studio performances from DJ Flash, Mista Quietman, Mark Cee, Styles 007, Man Money, DJ E Double (Double Platinum Entertainment), DJ BigTime, DJ Dolo, DJ DX, X5, Chameleon (Ka-Million), Semaj da DJ, DJ Madden, Benito, Joe Bananas, cover designer Blaze, and others.",
            "Bonus footage includes the Winterblaze mixtape battle held at the Boys Club (2000), with battle organizer Sean interviewed and DJ Savage among the competitors -- a rare visual record of the city's battle culture.",
            "The film preserves oral history documenting turntable battles at Audubon Park in the late 1970s and early 1980s where the winner took the loser's equipment, and names scene venues including Rendezvous (formerly Ruthie's), the Boys Club, Lollipop, Taste, and Ferris High School.",
            "The documentary names and defines Jersey City style markers including blend-driven mixtapes, the 201 style of doubled drums, and stacked-acapella blends, making it the source record for these terms.",
        ],
        "card": [
            {"label": "Director", "value": "DJ Wizard (WizTV)"},
            {"label": "Year", "value": "2006"},
            {"label": "Runtime", "value": "2 hours 57 minutes 58 seconds"},
            {"label": "Subject", "value": "Jersey City mixtape DJ scene"},
            {"label": "Watch", "value": "YouTube (WizTV upload and The Real Mista Quietman upload)"},
        ],
    },
    "mark-cee": {
        "facts": [
            "Mark Cee, also known as Nemo, is a Jersey City DJ and ghost producer who is one of the most influential behind-the-scenes figures in the city's mixtape scene, as documented in the 2006 WizTV documentary.",
            "He is credited with schooling a generation of Jersey City DJs on the MPC, including DJ DX, making him a key link in the chain of music technology knowledge that passed through the scene.",
            "He performed as half of the brother duo Double D alongside his brother Shannon, and his final mixtape (around 2000 to 2001) was distributed with the help of DJ BigTime.",
        ],
        "card": [
            {"label": "Also known as", "value": "Nemo"},
            {"label": "Scene", "value": "Jersey City, New Jersey"},
            {"label": "Era", "value": "1990s to 2000s"},
            {"label": "Known for", "value": "MPC mentorship, ghost production, Double D crew"},
            {"label": "Documented in", "value": "Jersey City DJ Documentary Vol. 1 (2006)"},
        ],
    },
    "dj-007": {
        "facts": [
            "DJ 007, also known as Styles 007 and Mr. Shut Em Down, and formerly as DJ Worm, is a single Jersey City DJ who operated under all of these aliases across a career of roughly 15 years documented in the 2006 WizTV documentary.",
            "In the film he announced plans to retire in 2007, making his interview one of the few on-camera retirements in the scene's documented history.",
            "He sold mixtapes through Stan's Square Records alongside the city's top DJs, placing him in the commercial heart of Jersey City's mixtape distribution network.",
        ],
        "card": [
            {"label": "Also known as", "value": "Styles 007, Mr. Shut Em Down, DJ Worm (earlier name)"},
            {"label": "Scene", "value": "Jersey City, New Jersey"},
            {"label": "Era", "value": "c. 1991 to 2007"},
            {"label": "Distribution", "value": "Stan's Square Records"},
            {"label": "Documented in", "value": "Jersey City DJ Documentary Vol. 1 (2006)"},
            {"label": "Instagram", "value": "@007_style201"},
        ],
    },
    "man-money": {
        "facts": [
            "Man Money, also billed as Mad Money, is a Jersey City mixtape DJ who has been active since approximately 1989, making him one of the longest-running figures in the scene's documented history.",
            "He is the producer of the Street Blends series, including Phase 20 and Phase 21 -- tape series spanning decades that reflect the sustained output of a career DJ.",
            "In the 2006 WizTV documentary he recalls the era when a Jersey City mixtape could earn a DJ $2,000 or more, and names Devil Seven as a peer from that period, placing the city's tape economy in historical context.",
        ],
        "card": [
            {"label": "Also known as", "value": "Mad Money"},
            {"label": "Scene", "value": "Jersey City, New Jersey"},
            {"label": "Active since", "value": "c. 1989"},
            {"label": "Known for", "value": "Street Blends series (Phase 20, Phase 21)"},
            {"label": "Documented in", "value": "Jersey City DJ Documentary Vol. 1 (2006)"},
        ],
    },
    "dj-e-double": {
        "facts": [
            "DJ E Double, born Eric Pinkney and also known as DJ E-Dub DaGeneral and E Platinum, is a Jersey City DJ celebrated as the Prince of Jersey -- one of the city's most prominent mixtape and club DJs of the late 1990s and early 2000s.",
            "In 1995 he founded his entertainment brand DpEnt. (Double Platinum Entertainment), which became the foundation for his promotions, party hosting, and mixtape distribution across the East Coast.",
            "Through the early 2000s he built a reputation for signature blends, club mixes, and custom tracks defining North Jersey's urban nightlife, with residencies at Rendezvous (formerly Ruthie's), Lollipop, Taste, Brenda's, and Bills.",
            "He is interviewed in the 2006 WizTV documentary, where he gives a shoutout to the Killa K family, documenting the social fabric of the scene.",
            "His daughter performs as DJ She Dog, making him part of a family lineage in the city's DJ tradition.",
        ],
        "card": [
            {"label": "Real name", "value": "Eric Pinkney"},
            {"label": "Also known as", "value": "DJ E-Dub DaGeneral, E Platinum, da General"},
            {"label": "Scene", "value": "Jersey City, New Jersey (201)"},
            {"label": "Era", "value": "1995 to present"},
            {"label": "Brand", "value": "Double Platinum Entertainment (DpEnt.)"},
            {"label": "Residencies", "value": "Rendezvous, Lollipop, Taste, Brenda's, Bills"},
            {"label": "Documented in", "value": "Jersey City DJ Documentary Vol. 1 (2006)"},
            {"label": "Instagram", "value": "@djedubdageneral"},
        ],
    },
    "dj-dolo": {
        "facts": [
            "DJ Dolo is a Jersey City DJ of the Dangerous Minds crew who performed earlier as Dollar Mike before settling on the Dolo name, a transition documented in the 2006 WizTV documentary.",
            "He credits DJ BigTime as a mentor who shaped his approach to the craft, reflecting the mentorship networks that passed DJ skills across generations in the Jersey City scene.",
        ],
        "card": [
            {"label": "Also known as", "value": "Dollar Mike (earlier name)"},
            {"label": "Crew", "value": "Dangerous Minds"},
            {"label": "Scene", "value": "Jersey City, New Jersey"},
            {"label": "Partner", "value": "E Square"},
            {"label": "Mentor", "value": "DJ BigTime"},
            {"label": "Documented in", "value": "Jersey City DJ Documentary Vol. 1 (2006)"},
        ],
    },
    "x5": {
        "facts": [
            "X5 is a Jersey City DJ who named himself after the BMW X5, a self-description captured in the 2006 WizTV documentary where he is interviewed alongside his partner Wiley Cat (Walley Katt).",
            "He is part of the HuF fam alongside Monster A and Gooch, a crew affiliation placing him in Jersey City's broader hip-hop social network of the early 2000s.",
            "He sold mixtapes through Stan's Square Records with his partner Walley Katt, distributing through the store that served as the commercial hub for the city's entire mixtape scene.",
        ],
        "card": [
            {"label": "Scene", "value": "Jersey City, New Jersey"},
            {"label": "Partner", "value": "DJ Walley Katt (Wiley Cat)"},
            {"label": "Crew", "value": "HuF fam (with Monster A and Gooch)"},
            {"label": "Distribution", "value": "Stan's Square Records"},
            {"label": "Documented in", "value": "Jersey City DJ Documentary Vol. 1 (2006)"},
        ],
    },
    "chameleon-ka-million": {
        "facts": [
            "Chameleon, now billed as Ka-Million, is a Jersey City DJ and producer who performed earlier as DJ Solid before adopting his current alias, a progression documented in the 2006 WizTV documentary.",
            "He operates Paid In Full Studios and Ful Real Entertainment, a company named in memory of a friend known as Ful -- a tribute that reflects the loyalty running through the Jersey City scene.",
            "He is active on Instagram as @mixedbykamillion and remains part of the city's active DJ community as of 2026.",
        ],
        "card": [
            {"label": "Also known as", "value": "Chameleon, DJ Solid (earlier name)"},
            {"label": "Scene", "value": "Jersey City, New Jersey"},
            {"label": "Studio", "value": "Paid In Full Studios"},
            {"label": "Label", "value": "Ful Real Entertainment"},
            {"label": "Partner", "value": "All Out"},
            {"label": "Documented in", "value": "Jersey City DJ Documentary Vol. 1 (2006)"},
            {"label": "Instagram", "value": "@mixedbykamillion"},
        ],
    },
    "dj-semaj": {
        "facts": [
            "Semaj da DJ is a Jersey City DJ whose name is James spelled backward -- a wordplay identity confirmed when the 2006 documentary's transcript rendered his name as 'DJ Simmons', a mishearing corrected by DJ DX in 2026.",
            "He founded Two-One Digital Productions with a crew that includes DJ Evil, E Baby, Yoshi, and Shady, and operated record stores in West New York and Union City in addition to his Jersey City scene work.",
            "He has been active since approximately 1998 and sold mixtapes through Stan's Square Records alongside the city's top DJs.",
        ],
        "card": [
            {"label": "Scene", "value": "Jersey City, New Jersey"},
            {"label": "Active since", "value": "c. 1998"},
            {"label": "Label/imprint", "value": "Two-One Digital Productions"},
            {"label": "Crew", "value": "DJ Evil, E Baby, Yoshi, Shady"},
            {"label": "Stores", "value": "West New York and Union City, NJ"},
            {"label": "Distribution", "value": "Stan's Square Records"},
            {"label": "Documented in", "value": "Jersey City DJ Documentary Vol. 1 (2006)"},
            {"label": "Instagram", "value": "@semajdadj"},
        ],
    },
    "dj-madden": {
        "facts": [
            "DJ Madden is a Jersey City DJ, turntablist, and producer who was put on by DJ Wizard and mentored by Mark Cee, placing him in the direct lineage of the city's most influential scene-builders.",
            "He collaborated with DJ DX on a trilogy of studio albums: 'This Is Hip-Hop', 'The Unfortunate Child', and 'Made From Scratch' (2015, Apple Music), marking a formal recording output that sets him apart from many mixtape-only peers.",
            "He sold mixtapes through Stan's Square Records alongside the city's top DJs and is active on Instagram as @officialdjmadden.",
        ],
        "card": [
            {"label": "Scene", "value": "Jersey City, New Jersey"},
            {"label": "Mentors", "value": "Mark Cee, DJ Wizard"},
            {"label": "Collaborator", "value": "DJ DX"},
            {"label": "Albums", "value": "This Is Hip-Hop; The Unfortunate Child; Made From Scratch (2015)"},
            {"label": "Distribution", "value": "Stan's Square Records"},
            {"label": "Documented in", "value": "Jersey City DJ Documentary Vol. 1 (2006)"},
            {"label": "Instagram", "value": "@officialdjmadden"},
        ],
    },
    "benito": {
        "facts": [
            "Benito is a Jersey City producer-DJ who was roughly 11 years into his career at the time of the 2006 WizTV documentary, placing his start around 1995.",
            "He is a practitioner of the 201 style of doubled drums -- the production signature that the documentary names as specific to Jersey City -- making him one of the clearest documented examples of that sound.",
            "He worked alongside Double O, and his interview is one of the most technically specific accounts of Jersey City's production culture in the entire film.",
        ],
        "card": [
            {"label": "Scene", "value": "Jersey City, New Jersey (201)"},
            {"label": "Era", "value": "c. 1995 to 2006 and beyond"},
            {"label": "Known for", "value": "201 style doubled drums; the Jersey City production signature"},
            {"label": "Collaborator", "value": "Double O"},
            {"label": "Documented in", "value": "Jersey City DJ Documentary Vol. 1 (2006)"},
        ],
    },
    "joe-bananas": {
        "facts": [
            "Joe Bananas is a Jersey City DJ of Bananas Entertainment and Chemical Records who is interviewed in the 2006 WizTV documentary and noted for working in the chopped and screwed style -- a Southern technique he adapted to the Jersey City mixtape format.",
            "His segment in the documentary is dedicated in memory of Jay Vito (RIP), making it one of the film's most personal moments and reflecting the losses the scene had already absorbed by 2006.",
        ],
        "card": [
            {"label": "Scene", "value": "Jersey City, New Jersey"},
            {"label": "Label", "value": "Bananas Entertainment, Chemical Records"},
            {"label": "Style", "value": "Chopped and screwed"},
            {"label": "Documented in", "value": "Jersey City DJ Documentary Vol. 1 (2006)"},
        ],
    },
    "blaze-in-arts": {
        "facts": [
            "Blaze, working under the brand Blaze-In-Arts, is the graphic designer behind the visual identity of Jersey City's mixtape era, called the scene's cover designer in the 2006 WizTV documentary.",
            "He has designed roughly 1,000 mixtape covers since 2003, each marked by his signature crown logo, making him one of the most prolific visual artists in the city's music history.",
        ],
        "card": [
            {"label": "Scene", "value": "Jersey City, New Jersey"},
            {"label": "Specialty", "value": "Mixtape cover art"},
            {"label": "Active since", "value": "c. 2003"},
            {"label": "Volume", "value": "~1,000 covers designed"},
            {"label": "Signature mark", "value": "Crown logo"},
            {"label": "Documented in", "value": "Jersey City DJ Documentary Vol. 1 (2006)"},
        ],
    },
    "dj-nel-e-nel": {
        "facts": [
            "DJ NEL E NEL, also known as Mandela and billed as Nel El Blends, is a Jersey City blends mixtape legend, DJ, and producer with credits extending from the local scene to nationally known artists.",
            "His production and blends credits include work with Joe Budden, Ransom, PnB Rock, and N.O.R.E., and per the archive's founding oral history, his resume also includes credits with Kodak Black and the duo Hitchcock and Ransom.",
            "He is said by the scene's oral tradition to have put out a Notorious B.I.G. album ahead of its official release, a claim that awaits a second source but reflects his standing as a first-tier figure in Jersey City's mixtape culture.",
            "By community account he won the Winter Blaze 2000 DJ battle held at the Jersey City Boys and Girls Club, the city's premier battle competition of that era.",
            "He sold mixtapes through Stan's Square Records alongside the city's top DJs and remains active on Bandcamp and Instagram as @nelenelblends.",
        ],
        "card": [
            {"label": "Also known as", "value": "Mandela, Nel El Blends"},
            {"label": "Scene", "value": "Jersey City, New Jersey (201)"},
            {"label": "Known for", "value": "Blends; production with Joe Budden, Ransom, PnB Rock, N.O.R.E."},
            {"label": "Battle credential", "value": "Winter Blaze 2000 (community account)"},
            {"label": "Distribution", "value": "Stan's Square Records"},
            {"label": "Platforms", "value": "Bandcamp: djnelenel.bandcamp.com"},
            {"label": "Instagram", "value": "@nelenelblends"},
        ],
    },
    "dj-dyce": {
        "facts": [
            "DJ Dyce is a Jersey City DJ who is likely the figure shouted out as 'Dice' in the 2006 WizTV documentary, one of several names called out by peers during the film's interview segments.",
            "He sold mixtapes through Stan's Square Records alongside the city's top DJs and is active on Instagram as @djdyce201, where the 201 area code confirms his Jersey City identity.",
        ],
        "card": [
            {"label": "Scene", "value": "Jersey City, New Jersey (201)"},
            {"label": "Distribution", "value": "Stan's Square Records"},
            {"label": "Instagram", "value": "@djdyce201"},
            {"label": "Possible doc mention", "value": "Shouted out as Dice in the 2006 documentary (confirm)"},
        ],
    },
    "dj-q": {
        "facts": [
            "DJ Q is a Jersey City mixtape DJ of the late 1990s and 2000s era who is named in both DJ DX's and DJ 007's segments of the 2006 WizTV documentary, reflecting his standing across multiple crew networks.",
            "His identity was confirmed by DJ DX (Robert Van Liew) in a 2026 oral history for The Jersey City Sound, which places him as an era peer of DJ DX, DJ P Dub, and Showtime.",
        ],
        "card": [
            {"label": "Scene", "value": "Jersey City, New Jersey"},
            {"label": "Era", "value": "Late 1990s to 2000s"},
            {"label": "Documented in", "value": "Jersey City DJ Documentary Vol. 1 (2006)"},
            {"label": "Instagram", "value": "@da_topic_81"},
        ],
    },
    "dj-walley-katt": {
        "facts": [
            "DJ Walley Katt, referenced in the 2006 WizTV documentary as Wiley Cat, is a Jersey City DJ and the partner of X5, forming one of the documentary's on-camera partnerships.",
            "He sold mixtapes through Stan's Square Records alongside X5 and remains active on Instagram as @djwalleykatt as of 2026.",
        ],
        "card": [
            {"label": "Also known as", "value": "Wiley Cat (in 2006 documentary)"},
            {"label": "Scene", "value": "Jersey City, New Jersey"},
            {"label": "Partner", "value": "X5"},
            {"label": "Distribution", "value": "Stan's Square Records"},
            {"label": "Documented in", "value": "Jersey City DJ Documentary Vol. 1 (2006)"},
            {"label": "Instagram", "value": "@djwalleykatt"},
        ],
    },
    "strong-vic": {
        "facts": [
            "Strong Vic is a Jersey City DJ whose 201 area code in his handle @strongvic201 marks his connection to the city's scene.",
            "His biography and catalog await fuller documentation from the community or from its subject.",
        ],
        "card": [
            {"label": "Scene", "value": "Jersey City, New Jersey (201)"},
            {"label": "Instagram", "value": "@strongvic201"},
        ],
    },
    "dj-bam": {
        "facts": [
            "DJ Bam is a Jersey City DJ whose 201 area code in his handle @djbam201 marks his connection to the city.",
            "His biography and catalog await fuller documentation from the community or from its subject.",
        ],
        "card": [
            {"label": "Scene", "value": "Jersey City, New Jersey (201)"},
            {"label": "Instagram", "value": "@djbam201"},
        ],
    },
    "dj-flamez": {
        "facts": [
            "DJ Flamez is a Jersey City DJ documented in the archive's survey of the city's active DJ community.",
            "His biography and catalog await fuller documentation; this entry holds his place in the record until more detail is available.",
        ],
        "card": [
            {"label": "Scene", "value": "Jersey City, New Jersey"},
            {"label": "Instagram", "value": "@therealdjflamez"},
        ],
    },
    "juggs": {
        "facts": [
            "Juggs, formerly known as DJ E Murda, is a Jersey City DJ who rebranded from his earlier alias, a transition documented through community identification.",
            "His biography and catalog await fuller documentation from the community or its subject.",
        ],
        "card": [
            {"label": "Also known as", "value": "DJ E Murda (earlier name)"},
            {"label": "Scene", "value": "Jersey City, New Jersey (201)"},
            {"label": "Instagram", "value": "@juggs201"},
        ],
    },
    "dj-j-dub": {
        "facts": [
            "DJ J Dub is a Jersey City DJ who is likely the figure whose name is garbled as 'J Dun' in DJ E Double's segment of the 2006 WizTV documentary.",
        ],
        "card": [
            {"label": "Scene", "value": "Jersey City, New Jersey (201)"},
            {"label": "Instagram", "value": "@jdub2o1"},
            {"label": "Possible doc mention", "value": "J Dun garble in E Double's 2006 segment (confirm)"},
        ],
    },
    "midnite-the-dj": {
        "facts": [
            "Midnite The DJ is a Jersey City-area open-format DJ who works weddings, festivals, clubs, corporate events, and cruises across New Jersey and New York, with travel dates beyond the region.",
            "He bills as an award-winning DJ and performs under the motto 'If it ain't Nite, it ain't right'.",
            "He is connected to the city's broader DJ community, with peers including DJ Madden and WizTV among his Instagram followers.",
        ],
        "card": [
            {"label": "Scene", "value": "Jersey City area, New Jersey"},
            {"label": "Format", "value": "Open format"},
            {"label": "Events", "value": "Weddings, festivals, clubs, corporate, cruises"},
            {"label": "Instagram", "value": "@midnitethedj"},
            {"label": "Website", "value": "midnitethedj.com"},
        ],
    },
    "joe-budden": {
        "facts": [
            "Joe Budden is a rapper and media personality raised in Jersey City from age 13, who moved from the city's mixtape circuit to a national profile and is one of the most commercially successful artists the city has produced.",
            "His single 'Pump It Up' (2003) reached No. 38 on the Billboard Hot 100 and earned a Grammy nomination for Best Male Rap Solo Performance.",
            "He is a founding member of the rap supergroup Slaughterhouse (with Royce da 5'9, Joell Ortiz, and Crooked I), signed to Eminem's Shady Records.",
            "He has hosted The Joe Budden Podcast since 2015, surpassing 900 episodes and becoming one of hip-hop's most successful independent podcast platforms.",
        ],
        "card": [
            {"label": "Origin", "value": "Raised in Jersey City, New Jersey from age 13"},
            {"label": "Active since", "value": "c. 2001"},
            {"label": "Group", "value": "Slaughterhouse (Shady Records)"},
            {"label": "Key single", "value": "Pump It Up (2003) -- No. 38 Billboard Hot 100; Grammy nominated"},
            {"label": "Media", "value": "The Joe Budden Podcast (2015 to present; 900+ episodes)"},
        ],
    },
    "albee-al": {
        "facts": [
            "Albee Al is a Jersey City rapper from the Marion Projects whose music draws on lived experience, with millions of streams across Apple Music and YouTube.",
            "He is affiliated with Flatline and Splashlyfe and is credited on DJ Swill B's 'Choppa in the Backseat' (2024).",
            "Community voices count him among the city's current legends, recognizing his street credibility and sustained output.",
        ],
        "card": [
            {"label": "Origin", "value": "Marion Projects, Jersey City, New Jersey"},
            {"label": "Affiliations", "value": "Flatline, Splashlyfe"},
            {"label": "Known for", "value": "Millions of streams; raw street rap"},
            {"label": "Collab", "value": "Choppa in the Backseat with DJ Swill B (2024)"},
        ],
    },
    "ransom": {
        "facts": [
            "Ransom (Randy Nicholls) is a Jersey City rapper who moved to the city around age eight and built his reputation as one of the most technically precise MCs on the New Jersey mixtape circuit.",
            "He is one half of the A-Team alongside Hitchcock, a duo affiliated with DJ Clue's Desert Storm alongside Fabolous and Stack Bundles.",
            "The A-Team released the Hardhood Classics mixtape trilogy, earning a reputation for punishing punchlines and grimy street verses that defined the era's bar-for-bar standard.",
            "After a Def Jam deal did not materialize the A-Team split around 2006; Ransom has continued a prolific solo career.",
        ],
        "card": [
            {"label": "Real name", "value": "Randy Nicholls"},
            {"label": "Origin", "value": "Jersey City, New Jersey (moved age 8)"},
            {"label": "Duo", "value": "The A-Team (with Hitchcock)"},
            {"label": "Affiliation", "value": "DJ Clue's Desert Storm"},
            {"label": "Mixtapes", "value": "Hardhood Classics trilogy"},
            {"label": "Era", "value": "Late 1990s to present"},
        ],
    },
    "hitchcock": {
        "facts": [
            "Hitchcock is a Jersey City rapper, one half of the A-Team alongside Ransom, whose partnership placed them among the sharpest punchline duos on the New Jersey mixtape circuit of the early 2000s.",
            "The A-Team were affiliates of DJ Clue's Desert Storm and released the Hardhood Classics mixtape trilogy before splitting around 2006.",
        ],
        "card": [
            {"label": "Scene", "value": "Jersey City, New Jersey"},
            {"label": "Duo", "value": "The A-Team (with Ransom)"},
            {"label": "Affiliation", "value": "DJ Clue's Desert Storm"},
            {"label": "Mixtapes", "value": "Hardhood Classics trilogy"},
            {"label": "Era", "value": "Late 1990s to 2006 and beyond"},
        ],
    },
    "kenny-kenn": {
        "facts": [
            "Kenny Kenn was a Jersey City videographer and platform builder who gave the city's unsigned artists a stage long before social media existed to fill that role.",
            "He created DJ Kenny Kenn's Unsigned Hype DVD, which documented and promoted unsigned Jersey City talent during the DVD era -- a format that preceded YouTube as the primary way local artists reached audiences.",
            "He produced the Promise Me Tomorrow documentary series and is remembered by peers as a staple of Jersey City culture who 'gave us all a shot to be on the tube way before social media.'",
        ],
        "card": [
            {"label": "Scene", "value": "Jersey City, New Jersey"},
            {"label": "Known for", "value": "Unsigned Hype DVD; Promise Me Tomorrow documentary"},
            {"label": "Legacy", "value": "Platform builder for unsigned Jersey City artists"},
        ],
    },
    "rigga-mortis": {
        "facts": [
            "Rigga Mortis is a Jersey City rapper remembered by peers as a freestyle master whose cleverness and lyricism set a high bar in the city's hip-hop underground.",
            "He is credited by community voices with sharpening a generation of MCs: 'the man that made me perfect my punchlines,' as one tribute put it.",
        ],
        "card": [
            {"label": "Scene", "value": "Jersey City, New Jersey"},
            {"label": "Known for", "value": "Freestyle mastery, punchlines, lyricism"},
        ],
    },
    "revenue-wrong": {
        "facts": [
            "Revenue Wrong, also known as Wrong, is a Jersey City rapper from Arlington Park affiliated with the Blockstar and Frontline teams.",
            "He is remembered as a 'legend before the internet' -- a figure whose reputation was built entirely through in-person performance and word of mouth before digital platforms could have carried it.",
        ],
        "card": [
            {"label": "Also known as", "value": "Wrong"},
            {"label": "Scene", "value": "Arlington Park, Jersey City, New Jersey"},
            {"label": "Affiliations", "value": "Blockstar, Frontline"},
        ],
    },
    "harold-adamson": {
        "facts": [
            "Harold Campbell Adamson (December 10, 1906 -- August 17, 1980) was an American lyricist born in Greenville, New Jersey, who became one of the most prolific popular songwriters of the mid-twentieth century.",
            "He collaborated with composers including Jimmy McHugh, Burton Lane, and Hoagy Carmichael, writing lyrics for films, Broadway productions, and recordings across more than three decades.",
            "His songs include 'Around the World', 'Everything I Have Is Yours', and 'Time on My Hands', featured in Hollywood productions from the 1930s through the 1960s.",
        ],
        "card": [
            {"label": "Born", "value": "December 10, 1906, Greenville, New Jersey"},
            {"label": "Died", "value": "August 17, 1980"},
            {"label": "Specialty", "value": "Popular song lyrics, film and Broadway"},
            {"label": "Era", "value": "1930s to 1960s"},
        ],
    },
    "robert-kool-bell": {
        "facts": [
            "Robert Earl 'Kool' Bell (born October 8, 1950), also known as Muhammad Bayyan, is an American musician, singer, and songwriter who grew up in Jersey City, New Jersey.",
            "He co-founded Kool and the Gang in Jersey City in 1964 alongside his brother Ronald Bell and five neighborhood friends, all of whom attended Lincoln High School in the city.",
            "As the band's bassist and a driving creative force, he helped build one of the most sampled catalogs in music history, spanning funk, soul, R&B, and pop across six decades.",
            "The section of Maple Street in Jersey City where Bell and his bandmates grew up was officially renamed 'Kool and the Gang Way' in 2016 in their honor.",
        ],
        "card": [
            {"label": "Also known as", "value": "Muhammad Bayyan"},
            {"label": "Origin", "value": "Jersey City, New Jersey"},
            {"label": "School", "value": "Lincoln High School, Jersey City"},
            {"label": "Band", "value": "Kool and the Gang (co-founder, 1964)"},
            {"label": "Instrument", "value": "Bass"},
            {"label": "Street named", "value": "Kool and the Gang Way, Maple Street, Jersey City (2016)"},
        ],
    },
    "george-brown": {
        "facts": [
            "George 'Funky' Brown (January 15, 1949 -- November 17, 2023) was an American drummer born in Jersey City, New Jersey, and a founding member of Kool and the Gang.",
            "He co-founded the group in the mid-1960s alongside Robert 'Kool' Bell and other Jersey City neighbors, all of whom attended Lincoln High School, and served as the rhythmic anchor of the band for more than five decades.",
            "As the group's primary drummer, he helped craft a sound blending jazz roots with hard funk and later crossover R&B, producing a catalog that is among the most sampled in music history.",
        ],
        "card": [
            {"label": "Also known as", "value": "George Funky Brown"},
            {"label": "Born", "value": "January 15, 1949, Jersey City, New Jersey"},
            {"label": "Died", "value": "November 17, 2023"},
            {"label": "School", "value": "Lincoln High School, Jersey City"},
            {"label": "Band", "value": "Kool and the Gang (co-founder)"},
            {"label": "Instrument", "value": "Drums"},
        ],
    },
    "kool-and-the-gang": {
        "facts": [
            "Kool and the Gang formed in Jersey City, New Jersey, in 1964, founded by brothers Robert 'Kool' Bell and Ronald Bell along with five neighborhood friends who all attended Lincoln High School in the city.",
            "Before settling on their name the group went through earlier identities including the Jazziacs, the Soul Town Band, the New Dimensions, and Kool and the Flames.",
            "They honed their sound in Jersey City basements, at St. John's Church, and at the Boys and Girls Club on Ash Street before achieving national and international success across funk, soul, R&B, and pop.",
            "Their catalog is among the most sampled in music history, and Jersey City honored them in 2016 by officially renaming a section of Maple Street 'Kool and the Gang Way'.",
        ],
        "card": [
            {"label": "Origin", "value": "Jersey City, New Jersey (founded 1964)"},
            {"label": "School", "value": "Lincoln High School, Jersey City"},
            {"label": "Rehearsal spaces", "value": "St. John's Church; Boys and Girls Club on Ash Street, Jersey City"},
            {"label": "Street named", "value": "Kool and the Gang Way, Maple Street, Jersey City (2016)"},
            {"label": "Style", "value": "Funk, soul, R&B, pop, jazz"},
        ],
    },
    "charlie-dixon": {
        "facts": [
            "Charles Edward Dixon (December 31, 1898, Jersey City, New Jersey -- December 6, 1940, New York City) was an American jazz banjoist, one of the earliest recorded jazz instrumentalists from Jersey City.",
            "Between 1921 and 1923 he was a member of Johnny Dunn's Original Jazz Hounds, recording for Columbia Records in New York -- among the earliest commercial jazz recordings produced in the country.",
            "He played in local ensembles before joining Sam Wooding's orchestra in 1922, a band that toured internationally and introduced jazz to European audiences.",
        ],
        "card": [
            {"label": "Born", "value": "December 31, 1898, Jersey City, New Jersey"},
            {"label": "Died", "value": "December 6, 1940, New York City"},
            {"label": "Instrument", "value": "Banjo (jazz)"},
            {"label": "Bands", "value": "Johnny Dunn's Original Jazz Hounds; Sam Wooding's orchestra"},
            {"label": "Label", "value": "Columbia Records"},
            {"label": "Era", "value": "1920s to 1930s"},
        ],
    },
    "the-duprees": {
        "facts": [
            "The Duprees are a Jersey City doo-wop group who had a run of top-ten Billboard hits in the early 1960s, among the most successful vocal groups the city has produced.",
            "Their highest-charting single, 'You Belong to Me', reached No. 7 on the Billboard Hot 100 in 1962, bringing the soft close-harmony doo-wop sound of Jersey City's street corners to a national audience.",
        ],
        "card": [
            {"label": "Origin", "value": "Jersey City, New Jersey"},
            {"label": "Style", "value": "Doo-wop"},
            {"label": "Peak single", "value": "You Belong to Me -- No. 7 Billboard Hot 100 (1962)"},
            {"label": "Era", "value": "Early 1960s"},
        ],
    },
    "al-caiola": {
        "facts": [
            "Alexander Emil Caiola (September 7, 1920 -- November 9, 2016) was an American guitarist, composer, and arranger born in Jersey City, New Jersey, who became one of the most in-demand session guitarists of the twentieth century.",
            "He recorded over fifty albums and worked with Elvis Presley, Ray Conniff, Frank Sinatra, Percy Faith, Buddy Holly, Mitch Miller, Tony Bennett, and Astor Piazzolla, among many others.",
            "His work spanned jazz, country, rock, and pop, and his guitar playing is embedded in some of the most commercially successful recordings of the 1950s and 1960s.",
        ],
        "card": [
            {"label": "Born", "value": "September 7, 1920, Jersey City, New Jersey"},
            {"label": "Died", "value": "November 9, 2016"},
            {"label": "Instrument", "value": "Guitar"},
            {"label": "Style", "value": "Jazz, pop, country, rock (session guitar)"},
            {"label": "Collaborators", "value": "Elvis Presley, Frank Sinatra, Tony Bennett, Buddy Holly, Mitch Miller"},
            {"label": "Albums", "value": "50+"},
        ],
    },
    "dino-danelli": {
        "facts": [
            "Dino Danelli (born Robert Daniel, July 23, 1944 -- December 15, 2022) was an American drummer and an original member of the Young Rascals, the rock group whose sound defined a moment of 1960s blue-eyed soul.",
            "He has been called 'one of the great unappreciated rock drummers in history', a reputation built on his technical command and his ability to hold the Rascals' hybrid of soul, gospel, and rock together.",
        ],
        "card": [
            {"label": "Born", "value": "July 23, 1944"},
            {"label": "Died", "value": "December 15, 2022"},
            {"label": "Instrument", "value": "Drums"},
            {"label": "Band", "value": "The Young Rascals"},
            {"label": "Style", "value": "Rock, blue-eyed soul"},
        ],
    },
    "richie-havens": {
        "facts": [
            "Richard Pierce Havens (January 21, 1941 -- April 22, 2013) was an American singer-songwriter and guitarist known for his distinctive open-tuning guitar style and a voice that bridged folk, soul, and rhythm and blues.",
            "He is best remembered for his opening performance at Woodstock in 1969, where his improvised extended set -- including the a cappella spiritual 'Freedom' -- became one of the defining moments of the festival.",
            "His catalog spans more than twenty albums from the mid-1960s through the 2000s, and his covers of Bob Dylan and The Beatles became near-definitive readings for a generation of listeners.",
        ],
        "card": [
            {"label": "Born", "value": "January 21, 1941"},
            {"label": "Died", "value": "April 22, 2013"},
            {"label": "Instrument", "value": "Guitar (open tunings), voice"},
            {"label": "Style", "value": "Folk, soul, R&B"},
            {"label": "Known for", "value": "Opening Woodstock 1969; Freedom"},
        ],
    },
    "jerry-herman": {
        "facts": [
            "Gerald Sheldon Herman (July 10, 1931 -- December 26, 2019) was an American composer and lyricist born in Jersey City, New Jersey, whose Broadway musicals made him one of the most commercially successful theater songwriters of the twentieth century.",
            "His shows include Hello, Dolly! (1964), which ran for 2,844 performances and at one time was the longest-running Broadway musical in history; Mame (1966), a vehicle for Angela Lansbury; and La Cage aux Folles (1983), the first hit Broadway musical about a gay couple.",
            "The title song from Hello, Dolly! became a hit for Louis Armstrong (1964) and reached No. 1 on the Billboard Hot 100, extending Herman's reach from the theater to popular radio.",
        ],
        "card": [
            {"label": "Born", "value": "July 10, 1931, Jersey City, New Jersey"},
            {"label": "Died", "value": "December 26, 2019"},
            {"label": "Specialty", "value": "Broadway musical composition and lyrics"},
            {"label": "Shows", "value": "Hello, Dolly! (1964); Mame (1966); La Cage aux Folles (1983)"},
            {"label": "Chart hit", "value": "Hello, Dolly! by Louis Armstrong -- No. 1 Billboard Hot 100 (1964)"},
        ],
    },
    "heather-b-gardner": {
        "facts": [
            "Heather B. Gardner (born November 13, 1970), known professionally as Heather B., is a rapper from Jersey City who first gained national visibility as a cast member of 'The Real World: New York' (MTV, 1992), the inaugural season of reality television's most influential franchise.",
            "Before her television debut she had already been affiliated with Boogie Down Productions, KRS-One's influential hip-hop group and one of the defining acts of socially conscious rap.",
            "She later returned to hip-hop as a recording artist and has worked as a radio personality, building a career spanning music, television, and broadcasting.",
        ],
        "card": [
            {"label": "Origin", "value": "Jersey City, New Jersey"},
            {"label": "Born", "value": "November 13, 1970"},
            {"label": "Known for", "value": "The Real World: New York (MTV, 1992); Boogie Down Productions"},
            {"label": "Style", "value": "Hip-hop, conscious rap"},
        ],
    },
    "marilyn-mccoo": {
        "facts": [
            "Marilyn McCoo (born September 30, 1943) is an American singer, actress, and television host from Jersey City who became one of the signature voices of the 5th Dimension, the group behind 'Aquarius/Let the Sunshine In' and 'Up, Up and Away'.",
            "As the group's lead female vocalist, she co-wrote and sang 'You Don't Have to Be a Star (To Be in My Show)', a duet with her husband Billy Davis Jr. that reached No. 1 on the Billboard Hot 100 in 1977.",
            "She hosted the syndicated music television program Solid Gold (1980 to 1983), giving her a second national platform and making her one of the most familiar faces in 1980s pop television.",
        ],
        "card": [
            {"label": "Origin", "value": "Jersey City, New Jersey"},
            {"label": "Born", "value": "September 30, 1943"},
            {"label": "Group", "value": "The 5th Dimension"},
            {"label": "No. 1 hit", "value": "You Don't Have to Be a Star with Billy Davis Jr. (1977)"},
            {"label": "Television", "value": "Solid Gold host (1980 to 1983)"},
        ],
    },
    "tia-fuller": {
        "facts": [
            "Tia Fuller (born March 27, 1976) is an American saxophonist, composer, and educator who has been a member of Beyonce's all-female touring band, bringing her to stages in front of millions worldwide.",
            "She is a faculty member in the ensembles department at Berklee College of Music and has released multiple albums as a leader in the jazz tradition.",
            "She was a featured jazz musician in Pixar's animated film 'Soul' (2020), bringing her improvisational approach into one of the most widely seen films of that year.",
        ],
        "card": [
            {"label": "Born", "value": "March 27, 1976"},
            {"label": "Instrument", "value": "Saxophone"},
            {"label": "Known for", "value": "Beyonce touring band; Pixar's Soul (2020)"},
            {"label": "Teaching", "value": "Berklee College of Music, ensembles faculty"},
            {"label": "Style", "value": "Jazz, contemporary"},
        ],
    },
    "christina-milian": {
        "facts": [
            "Christina Milian (born Christine Flores, September 26, 1981) is an American singer, songwriter, and actress from Jersey City, New Jersey, who debuted on the national stage with a feature on Ja Rule's 'Between Me and You' (2000), which peaked at No. 11 on the Billboard Hot 100.",
            "Her debut single 'AM to PM' (2001, Island Records) reached the top 40 of the Billboard Hot 100 and crossed over to UK charts, establishing her as an international pop presence.",
            "She has built a parallel acting career alongside her music, with television and film credits across network productions.",
        ],
        "card": [
            {"label": "Born", "value": "September 26, 1981, Jersey City, New Jersey"},
            {"label": "Style", "value": "Pop, R&B, hip-hop"},
            {"label": "Label", "value": "Island Records"},
            {"label": "Debut", "value": "Feature on Ja Rule's Between Me and You (2000) -- No. 11 Billboard Hot 100"},
            {"label": "Hit single", "value": "AM to PM (2001)"},
        ],
    },
    "chill-rob-g": {
        "facts": [
            "Chill Rob G (born Robert Frazier) is a rapper from Jersey City, New Jersey, and a founding member of DJ Mark the 45 King's legendary Flavor Unit collective -- one of the defining hip-hop crews of the Golden Era.",
            "His 1989 debut album 'Ride the Rhythm' (Wild Pitch Records), produced by The 45 King, is widely cited as a classic of the era, featuring 'Court Is Now in Session' and 'Dope Rhymes'.",
            "His song 'Let the Words Flow' was sampled without permission by German dance group Snap! for their global hit 'The Power' (1990), one of the most commercially successful acts of unauthorized sampling in early 1990s pop.",
            "He returned with 'Empires Crumble' (2022, SpitSLAM/Chuck D's label), a boom bap comeback featuring a Flavor Unit reunion with The 45 King, Lakim Shabazz, and others, followed by 'Survival of the Better' (2026), executive produced by Chuck D and produced entirely by C-Doc.",
        ],
        "card": [
            {"label": "Real name", "value": "Robert Frazier"},
            {"label": "Origin", "value": "Jersey City, New Jersey"},
            {"label": "Collective", "value": "Flavor Unit (DJ Mark the 45 King)"},
            {"label": "Debut album", "value": "Ride the Rhythm (1989, Wild Pitch Records)"},
            {"label": "Known for", "value": "Let the Words Flow -- sampled by Snap! for The Power"},
            {"label": "Return album", "value": "Empires Crumble (2022, SpitSLAM); Survival of the Better (2026)"},
            {"label": "Style", "value": "Hip-hop, boom bap, Golden Era"},
        ],
    },
    "double-j": {
        "facts": [
            "Double J (Gerald 'J' Jones), known as The Hitman Double J, is a Jersey City rapper and a founding member of Queen Latifah's original Flavor Unit collective, one of the defining hip-hop crews of the late 1980s and early 1990s.",
            "Growing up in Jersey City he hosted block parties alongside future stars including Apache; in 1988 he joined DJ Mark the 45 King's Flavor Unit after an introduction through Apache and the crew.",
            "He appears on the 1990 posse cut 'Flavor Unit Assassination Squad' (4th and Broadway/Island Records) and released the 12-inch 'Cannibal Town / Def Style' and solo album 'The Hitman', best known for the track 'Double J'z Tantrum'.",
            "He later resurfaced as half of the Maniac Mob, reuniting with DJ Mark the 45 King for production on several independent releases including a track on the 1995 compilation 'The D&D Project'.",
            "He received his Island Records deal after Fab Five Freddy saw a homemade video of the Flavor Unit crew and passed it up the chain -- a chain of events that shows how the early 1990s rap industry actually worked.",
        ],
        "card": [
            {"label": "Real name", "value": "Gerald J. Jones"},
            {"label": "Origin", "value": "Jersey City, New Jersey"},
            {"label": "Collective", "value": "Flavor Unit (DJ Mark the 45 King)"},
            {"label": "Key track", "value": "Flavor Unit Assassination Squad (1990)"},
            {"label": "Album", "value": "The Hitman (4th and Broadway / Island Records)"},
            {"label": "Later group", "value": "Maniac Mob"},
            {"label": "Style", "value": "Hip-hop, boom bap, East Coast rap"},
        ],
    },
    "dj-stranger-dee": {
        "facts": [
            "DJ Stranger Dee is a legendary figure in the Jersey City hip-hop and DJ scene who gained local fame in the early 1980s as a foundational DJ and pioneer for the Sweet, Slick and Sly Crew -- one of the most celebrated acts in early New Jersey hip-hop.",
            "Along with his crew, Stranger Dee performed at seminal events including New Jersey vs. Bronx showdowns at the Benmore Skating Rink in Jersey City; key documented dates include a January 15, 1982 showdown with the Cold Crush Brothers and the Turnout Battle of 82 on July 2 of that year, both preserved in flyers archived at the Museum of Pop Culture (MoPOP).",
            "He is credited by DJ Flash -- who names Stranger D as an influence who let him spin as a child -- with being a founding presence in the park-jam scene that built Jersey City's DJ tradition from the ground up.",
            "He made contributions on a national scale, working as a DJ on major hip-hop tours alongside groups including Public Enemy in the late 1980s, taking the Jersey City sound to a national touring circuit.",
            "He is regarded by older generations and hip-hop historians as a founding father of the Chilltown (Jersey City) music movement.",
        ],
        "card": [
            {"label": "Crew", "value": "Sweet, Slick and Sly Crew"},
            {"label": "Scene", "value": "Jersey City (Chilltown), New Jersey"},
            {"label": "Era", "value": "Early 1980s to late 1980s and beyond"},
            {"label": "Key venues", "value": "Benmore Skating Rink, Jersey City"},
            {"label": "Tour work", "value": "Public Enemy tour (late 1980s)"},
            {"label": "Legacy", "value": "Credited by DJ Flash as a founding influence"},
        ],
    },
    "cool-sir-brown": {
        "facts": [
            "Cool Sir Brown is an independent hip-hop artist from Jersey City, New Jersey, known for classic and modern rap tracks across a catalog available on Spotify, Apple Music, Audiomack, Amazon Music, and Deezer.",
            "His single and album 'Sir Brown Lives' is the centerpiece of his catalog, a project rooted in vintage Jersey City hip-hop tradition.",
            "He has collaborated with the late hip-hop legend Biz Markie and maintains an active release schedule into 2025.",
        ],
        "card": [
            {"label": "Origin", "value": "Jersey City, New Jersey"},
            {"label": "Style", "value": "Hip-hop, boom bap, classic rap"},
            {"label": "Key project", "value": "Sir Brown Lives"},
            {"label": "Platforms", "value": "Spotify, Apple Music, Audiomack, Amazon Music, Deezer"},
            {"label": "Notable collab", "value": "Biz Markie"},
        ],
    },
    "dj-thurmie-thurm": {
        "facts": [
            "DJ Thurmie Thurm, also known as DJ Thurm, is a battle DJ and pioneer of the original Jersey City, New Jersey hip-hop and house scene, best known for his work in the late 1970s and early 1980s as a founding member of the Jersey City Chiba Crew.",
            "He came up in the Chilltown scene -- Jersey City's nickname -- playing park jams, community centers, and local spots alongside legends including Grand Wizard Capone, Nicky Barnes, and the Sweet, Slick and Sly Crew.",
            "He is featured in the documentary 'Chill Town J.C.', directed by A. Champagne Lloyd, which documents the hip-hop artists who developed their talents in the streets of Jersey City and places him alongside Chill Rob G, Lakim Shabazz, Master Cee, and DJ Wimpy Bee as a city pioneer.",
            "Decades on, he remains a respected figure in Chilltown history, celebrated across East Coast music history circles and documented in community groups and online archives dedicated to Jersey City's founding era.",
        ],
        "card": [
            {"label": "Also known as", "value": "DJ Thurm"},
            {"label": "Scene", "value": "Chilltown (Jersey City), New Jersey"},
            {"label": "Era", "value": "Late 1970s to 1980s"},
            {"label": "Crew", "value": "Jersey City Chiba Crew"},
            {"label": "Documented in", "value": "Chill Town J.C. documentary"},
            {"label": "Contemporaries", "value": "Grand Wizard Capone, Sweet, Slick and Sly, DJ Wimpy Bee"},
            {"label": "Instagram", "value": "@originaldjthurm"},
        ],
    },
    "dj-wimpy-bee": {
        "facts": [
            "DJ Wimpy Bee (Edmund Bryant) was a Jersey City DJ legend celebrated as a founding figure of the Chilltown hip-hop scene and one of the most respected DJs in the city's history, known for technical mastery including super-fast scratches and deep command of the turntables.",
            "He was named by DJ Flash as his 'big brother' in the craft -- the most direct form of mentorship credit in the scene -- placing Wimpy Bee at the top of the generational chain that built Jersey City's DJ tradition.",
            "He was featured in documentaries chronicling the city's unsung hip-hop pioneers, including the Chill Town Jersey City documentary, and his influence spanned decades from early block parties and school events through club sets and recorded mixtapes.",
            "Edmund Bryant passed away in October 2025. His death was met with an outpouring of respect from the Jersey City community, where he was remembered not only as a master of the turntables but as a 'special gentleman' deeply embedded in the city's cultural fabric.",
        ],
        "card": [
            {"label": "Real name", "value": "Edmund Bryant"},
            {"label": "Scene", "value": "Chilltown (Jersey City), New Jersey"},
            {"label": "Era", "value": "Late 1970s to 2025"},
            {"label": "Passed", "value": "October 2025"},
            {"label": "Known for", "value": "Super-fast scratches; founding the city's DJ tradition"},
            {"label": "Mentor to", "value": "DJ Flash (named Wimpy Bee as big brother in the craft)"},
            {"label": "Documented in", "value": "Chill Town J.C. documentary"},
        ],
    },
    "pm-dawn": {
        "facts": [
            "PM Dawn is a hip-hop duo from Jersey City, New Jersey, consisting of brothers Attrell Cordes (Prince Be) and Jarrett Cordes (DJ Minutemix), who blended hip-hop, soul, psychedelia, and new age into a style entirely their own.",
            "Their debut single 'Set Adrift on Memory Bliss' (1991, Gee Street/Island Records) sampled Spandau Ballet's 'True' and reached No. 1 in the United Kingdom and No. 1 on the Billboard Hot 100 in the United States, giving Jersey City one of its most commercially successful chart-toppers.",
            "Their debut album 'Of the Heart, of the Soul and of the Cross: The Utopian Experience' (1991) established them as a critical darling of the alternative hip-hop and new jack swing era.",
        ],
        "card": [
            {"label": "Origin", "value": "Jersey City, New Jersey"},
            {"label": "Members", "value": "Prince Be (Attrell Cordes), DJ Minutemix (Jarrett Cordes)"},
            {"label": "Style", "value": "Hip-hop, soul, psychedelia, new age"},
            {"label": "No. 1 hit", "value": "Set Adrift on Memory Bliss (1991) -- No. 1 US and UK"},
            {"label": "Debut album", "value": "Of the Heart, of the Soul and of the Cross (1991, Gee Street/Island)"},
        ],
    },
    "attrell-cordes": {
        "facts": [
            "Attrell Cordes (born May 19, 1970), known as Prince Be, is the primary vocalist of Jersey City hip-hop duo PM Dawn and one of the most distinctive voices of the early 1990s alternative hip-hop era.",
            "He co-wrote and performed 'Set Adrift on Memory Bliss' (1991), which reached No. 1 on the Billboard Hot 100 and brought PM Dawn -- and Jersey City -- to the top of the American pop chart.",
            "His lyrical style blended introspection, spirituality, and surreal imagery in a way that set PM Dawn apart from every other act in early 1990s hip-hop.",
        ],
        "card": [
            {"label": "Known as", "value": "Prince Be"},
            {"label": "Group", "value": "PM Dawn"},
            {"label": "Origin", "value": "Jersey City, New Jersey"},
            {"label": "Born", "value": "May 19, 1970"},
            {"label": "Style", "value": "Hip-hop, soul, new age, conscious rap"},
            {"label": "Key hit", "value": "Set Adrift on Memory Bliss (1991) -- No. 1 Billboard Hot 100"},
        ],
    },
}


def run():
    with DATA.open("r", encoding="utf-8") as f:
        data = json.load(f)

    entries = data["entries"]
    applied = 0
    skipped = 0

    for entry in entries:
        slug = entry.get("slug", "")
        if slug not in ENRICHMENTS:
            skipped += 1
            continue

        patch = ENRICHMENTS[slug]

        if "facts" in patch:
            entry["facts"] = patch["facts"]

        if "card" in patch:
            entry["card"] = patch["card"]

        applied += 1

    with DATA.open("w", encoding="utf-8", newline="\r\n") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)

    print(f"Done. Applied enrichments to {applied} entries. Skipped {skipped} entries (no patch).")


if __name__ == "__main__":
    run()
