import json
from pathlib import Path

DATA = Path('data/entries.json')

ENRICHMENTS2 = {
    # ---- Classic musicians (Wikipedia stub entries) ----
    "wally-brandt": {
        "facts": [
            "Wally Brandt (born Walter Anthony Brandt) is an American guitarist, producer, and songwriter from Jersey City, New Jersey, whose career has spanned pop rock, country music, and production music.",
            "He is best known for his work with the pop rock band Seven and the Sun, the country music band Whiskey Falls, and as a co-founder of the production music company We3Kings Music.",
            "His session and production credits place him across multiple genres, and his We3Kings catalog has licensed music for film, television, and advertising.",
        ],
        "card": [
            {"label": "Origin", "value": "Jersey City, New Jersey"},
            {"label": "Instrument", "value": "Guitar"},
            {"label": "Bands", "value": "Seven and the Sun; Whiskey Falls"},
            {"label": "Company", "value": "We3Kings Music (production music)"},
            {"label": "Style", "value": "Pop rock, country, production music"},
        ],
    },
    "brute-force": {
        "facts": [
            "Stephen Friedland (born September 29, 1940), known as Brute Force, is an American singer and songwriter from Jersey City, New Jersey, who was part of the New York avant-pop scene of the 1960s.",
            "He wrote and performed with The Tokens and wrote songs recorded by Peggy March, Del Shannon, The Chiffons, and The Cyrkle, building a reputation as an unconventional pop craftsman.",
            "His 1969 single 'King of Fuh' was released on Apple Records, making it one of the label's most unusual releases and earning him a lasting cult following.",
        ],
        "card": [
            {"label": "Real name", "value": "Stephen Friedland"},
            {"label": "Born", "value": "September 29, 1940, Jersey City, New Jersey"},
            {"label": "Known for", "value": "King of Fuh (Apple Records, 1969); The Tokens collaborations"},
            {"label": "Style", "value": "Avant-pop, novelty, psychedelia"},
            {"label": "Label", "value": "Apple Records"},
        ],
    },
    "thomas-vincent-cator": {
        "facts": [
            "Thomas Vincent Cator (March 23, 1888 -- April 9, 1931) was an American composer born in Jersey City, New Jersey, whose most significant contribution was the development and advocacy of what he called the aura-modal scale.",
            "Working in the early twentieth century, Cator published theoretical work on his scale system, an attempt to expand the chromatic possibilities of Western composition beyond standard tonality.",
        ],
        "card": [
            {"label": "Born", "value": "March 23, 1888, Jersey City, New Jersey"},
            {"label": "Died", "value": "April 9, 1931"},
            {"label": "Specialty", "value": "Composition, music theory"},
            {"label": "Known for", "value": "Aura-modal scale system"},
        ],
    },
    "anthony-j-cirone": {
        "facts": [
            "Anthony James Cirone (born November 8, 1941) is an American percussionist born in Jersey City, New Jersey, who served as principal percussionist of the San Francisco Symphony and was a Professor of Music at San Jose State University from 1965 to 2001.",
            "He is one of the most influential percussion educators of the late twentieth century, with textbooks and method books used in conservatories and university programs worldwide.",
        ],
        "card": [
            {"label": "Born", "value": "November 8, 1941, Jersey City, New Jersey"},
            {"label": "Instrument", "value": "Percussion"},
            {"label": "Orchestra", "value": "San Francisco Symphony (principal percussionist)"},
            {"label": "Teaching", "value": "San Jose State University, 1965 to 2001"},
            {"label": "Style", "value": "Classical, orchestral"},
        ],
    },
    "cy-coben": {
        "facts": [
            "Seymour 'Cy' Coben (April 4, 1919 -- May 26, 2006) was an American songwriter from Jersey City, New Jersey, whose hits were recorded by bandleaders, country singers, and popular artists across the mid-twentieth century.",
            "His songs reached unlikely audiences: The Beatles recorded his 'Some Other Guy', Tommy Cooper recorded his comedy material, and Leonard Nimoy recorded his compositions, reflecting the range of his output.",
            "His country songwriting in particular produced hits recorded by artists on major Nashville labels through the 1950s and 1960s.",
        ],
        "card": [
            {"label": "Born", "value": "April 4, 1919, Jersey City, New Jersey"},
            {"label": "Died", "value": "May 26, 2006"},
            {"label": "Specialty", "value": "Songwriting (pop, country, novelty)"},
            {"label": "Notable covers", "value": "The Beatles, Leonard Nimoy, Tommy Cooper"},
            {"label": "Era", "value": "1940s to 1970s"},
        ],
    },
    "leonard-de-paur": {
        "facts": [
            "Leonard Etienne De Paur (November 18, 1914 -- November 7, 1998) was an American composer, choral director, and arts administrator from Jersey City, New Jersey.",
            "He directed the De Paur Infantry Chorus during World War II, which toured globally and brought African American choral music to international audiences, and later served in arts administration at Lincoln Center for the Performing Arts.",
            "His work bridged military service, Black cultural expression, and institutional arts leadership across a career spanning six decades.",
        ],
        "card": [
            {"label": "Born", "value": "November 18, 1914, Jersey City, New Jersey"},
            {"label": "Died", "value": "November 7, 1998"},
            {"label": "Known for", "value": "De Paur Infantry Chorus; Lincoln Center arts administration"},
            {"label": "Specialty", "value": "Choral direction, composition, arts administration"},
        ],
    },
    "norman-edge": {
        "facts": [
            "Norman Edge (April 29, 1934 -- June 4, 2018) was an American jazz double bassist from Jersey City, New Jersey, who performed and recorded across the New York metropolitan jazz scene for several decades.",
        ],
        "card": [
            {"label": "Born", "value": "April 29, 1934, Jersey City, New Jersey"},
            {"label": "Died", "value": "June 4, 2018"},
            {"label": "Instrument", "value": "Double bass"},
            {"label": "Style", "value": "Jazz"},
        ],
    },
    "luke-elliot": {
        "facts": [
            "Luke Elliot (born June 30, 1984) is an American musician, producer, and actor whose work draws on American roots music, dark folk, and rock.",
            "He has released music on independent labels and has built a following in Europe alongside the United States, performing at festivals and developing a reputation for intense, stripped-down live performances.",
        ],
        "card": [
            {"label": "Born", "value": "June 30, 1984"},
            {"label": "Style", "value": "Dark folk, American roots, rock"},
        ],
    },
    "beth-fowler": {
        "facts": [
            "Beth Fowler is an American actress and singer born in Jersey City, New Jersey, best known for her Broadway career and for playing Sister Ingalls in the Netflix series 'Orange Is the New Black'.",
            "She is a two-time Tony Award nominee for her Broadway work, as well as a two-time Screen Actors Guild Award winner for Outstanding Performance by an Ensemble in a Comedy Series as part of the 'Orange Is the New Black' cast.",
            "Her Broadway credits span several decades and include roles in major productions, establishing her as a versatile performer across musical theater and dramatic television.",
        ],
        "card": [
            {"label": "Origin", "value": "Jersey City, New Jersey"},
            {"label": "Known for", "value": "Orange Is the New Black (Sister Ingalls); Broadway career"},
            {"label": "Awards", "value": "Two-time Tony Award nominee; two-time SAG Award winner"},
            {"label": "Style", "value": "Musical theater, dramatic television"},
        ],
    },
    "william-w-gilchrist": {
        "facts": [
            "William Wallace Gilchrist (January 8, 1846 -- December 20, 1916) was an American composer born in Jersey City, New Jersey, and a major figure in nineteenth-century Philadelphia's musical life.",
            "He founded the Mendelssohn Club of Philadelphia in 1874, one of the oldest choral organizations in the United States, and served as its director for decades.",
            "He received the Cincinnati Festival Prize in 1882 for his Symphony in C major, making him one of the more recognized American orchestral composers of his era.",
        ],
        "card": [
            {"label": "Born", "value": "January 8, 1846, Jersey City, New Jersey"},
            {"label": "Died", "value": "December 20, 1916"},
            {"label": "Founded", "value": "Mendelssohn Club of Philadelphia (1874)"},
            {"label": "Specialty", "value": "Choral and orchestral composition"},
        ],
    },
    "philip-james": {
        "facts": [
            "Philip Frederick Wright James (May 17, 1890 -- November 1, 1975) was an American composer, conductor, and music educator born in Jersey City, New Jersey.",
            "He chaired the music department at New York University for many years and composed works for orchestra, chamber ensemble, and voice, with several pieces performed by major American orchestras during the mid-twentieth century.",
        ],
        "card": [
            {"label": "Born", "value": "May 17, 1890, Jersey City, New Jersey"},
            {"label": "Died", "value": "November 1, 1975"},
            {"label": "Specialty", "value": "Composition, conducting, music education"},
            {"label": "Teaching", "value": "New York University (department chair)"},
        ],
    },
    "mimi-jones": {
        "facts": [
            "Mimi Jones (born March 25, 1972) is an American bassist, vocalist, composer, bandleader, and educator, and the founder of Hot Tone Music, her independent label and production company.",
            "She has performed and recorded with a wide range of jazz and creative music artists, building a catalog as a bandleader that draws on jazz, soul, and global music traditions.",
            "As an educator she has taught at workshops and institutions across the United States and internationally, and has been a visible advocate for women in jazz.",
        ],
        "card": [
            {"label": "Born", "value": "March 25, 1972"},
            {"label": "Instrument", "value": "Bass, voice"},
            {"label": "Label", "value": "Hot Tone Music (founder)"},
            {"label": "Style", "value": "Jazz, soul, creative music"},
        ],
    },
    "vic-juris": {
        "facts": [
            "Victor Edward Jurusz Jr. (September 26, 1953 -- December 31, 2019), known as Vic Juris, was an American jazz guitarist from Jersey City, New Jersey, widely respected in the New York jazz world for his melodic approach and harmonic sophistication.",
            "He recorded and performed with Richie Cole, Barry Miles, and other major jazz figures, and released several well-regarded albums as a leader from the 1970s through the 2010s.",
        ],
        "card": [
            {"label": "Born", "value": "September 26, 1953, Jersey City, New Jersey"},
            {"label": "Died", "value": "December 31, 2019"},
            {"label": "Instrument", "value": "Guitar"},
            {"label": "Style", "value": "Jazz"},
            {"label": "Collaborators", "value": "Richie Cole, Barry Miles"},
        ],
    },
    "david-kikoski": {
        "facts": [
            "Dave Kikoski (born September 29, 1961) is an American jazz pianist and keyboardist from New Jersey who has been one of the most in-demand sidemen in the New York jazz scene for more than three decades.",
            "He has recorded and performed with Roy Haynes, Woody Shaw, Eddie Henderson, and many others, and has released a strong catalog as a leader that demonstrates his command of bebop and post-bop vocabulary.",
        ],
        "card": [
            {"label": "Born", "value": "September 29, 1961"},
            {"label": "Instrument", "value": "Piano, keyboards"},
            {"label": "Style", "value": "Jazz, bebop, post-bop"},
            {"label": "Collaborators", "value": "Roy Haynes, Woody Shaw, Eddie Henderson"},
        ],
    },
    "peter-lemongello": {
        "facts": [
            "Peter Lemongello (born February 11, 1947) is an American singer from Jersey City, New Jersey, known for his self-financed double album 'Love '76', which he marketed through television advertising in the mid-1970s -- one of the earlier examples of direct-response music marketing in the United States.",
            "His television campaign made 'Love '76' a commercially successful release and established him as a recognizable figure in New Jersey entertainment circles during the disco era.",
        ],
        "card": [
            {"label": "Born", "value": "February 11, 1947, Jersey City, New Jersey"},
            {"label": "Known for", "value": "Love '76 (self-financed double album, 1976)"},
            {"label": "Style", "value": "Pop, adult contemporary"},
            {"label": "Era", "value": "1970s"},
        ],
    },
    "bob-lido": {
        "facts": [
            "Robert Lido (September 21, 1914 -- August 9, 2000) was an American violinist and singer from Jersey City, New Jersey, who became a regular member of 'The Lawrence Welk Show', one of American television's longest-running musical programs.",
            "His appearances on the Welk Show brought him into millions of American living rooms across the program's run, making him one of the more widely seen musicians to come out of Jersey City.",
        ],
        "card": [
            {"label": "Born", "value": "September 21, 1914, Jersey City, New Jersey"},
            {"label": "Died", "value": "August 9, 2000"},
            {"label": "Instrument", "value": "Violin"},
            {"label": "Known for", "value": "The Lawrence Welk Show (regular cast member)"},
            {"label": "Style", "value": "Popular, light orchestral"},
        ],
    },
    "jim-lord": {
        "facts": [
            "James Edward Lord III (born September 7, 1948) is an American folk and rock singer-songwriter and musician with ties to Jersey City and Hudson County, New Jersey.",
            "He has released recordings in the folk-rock tradition and has been part of the regional New Jersey and New York singer-songwriter community.",
        ],
        "card": [
            {"label": "Born", "value": "September 7, 1948"},
            {"label": "Style", "value": "Folk, rock, singer-songwriter"},
        ],
    },
    "charlotte-maconda": {
        "facts": [
            "Charlotte Maconda (March 12, 1863 -- May 15, 1952) was an American soprano singer from Jersey City, New Jersey, who performed and recorded in the early era of recorded sound -- the late nineteenth and early twentieth centuries.",
            "Her recordings, made during the acoustic era before electrical recording, preserve one of the earliest documented vocal performances by a Jersey City artist.",
        ],
        "card": [
            {"label": "Born", "value": "March 12, 1863, Jersey City, New Jersey"},
            {"label": "Died", "value": "May 15, 1952"},
            {"label": "Instrument", "value": "Voice (soprano)"},
            {"label": "Era", "value": "Late 19th to early 20th century"},
        ],
    },
    "rob-mazurek": {
        "facts": [
            "Rob Mazurek (born July 8, 1965) is an American composer, cornetist, and visual artist whose work moves across jazz, avant-garde, and experimental music.",
            "He has led the Chicago Underground projects and Exploding Star Orchestra, and his work has been released on Thrill Jockey and other leading avant-garde labels, making him one of the more internationally prominent experimental musicians with Jersey City connections.",
        ],
        "card": [
            {"label": "Born", "value": "July 8, 1965"},
            {"label": "Instrument", "value": "Cornet"},
            {"label": "Projects", "value": "Chicago Underground; Exploding Star Orchestra"},
            {"label": "Labels", "value": "Thrill Jockey"},
            {"label": "Style", "value": "Jazz, avant-garde, experimental"},
        ],
    },
    "tris-mccall": {
        "facts": [
            "Tris McCall is a music journalist, novelist, and rock musician from Hudson County, New Jersey, described by The New York Times as 'the plugged-in, Internet-era muse of Jersey City.'",
            "He became the music critic for the Newark Star-Ledger in 2010 and has released four solo albums, making him one of the few figures in Jersey City's creative community to work simultaneously as a practicing musician and a respected music critic.",
            "His McCall's Almanac web project combines short stories with previews of unreleased songs, positioning him at the intersection of literary and musical culture in a way that is specific to Jersey City's arts scene.",
        ],
        "card": [
            {"label": "Scene", "value": "Hudson County / Jersey City, New Jersey"},
            {"label": "Role", "value": "Musician, music critic, novelist"},
            {"label": "Critic at", "value": "Newark Star-Ledger (from 2010)"},
            {"label": "Albums", "value": "4 solo albums"},
            {"label": "Style", "value": "Rock, singer-songwriter"},
        ],
    },
    "phyllis-newman": {
        "facts": [
            "Phyllis Newman (March 19, 1933 -- September 15, 2019) was an American actress and singer from Jersey City, New Jersey, who won the 1962 Tony Award for Best Featured Actress in a Musical for her role as Martha Vail in 'Subways Are for Sleeping' on Broadway.",
            "She received the Isabelle Stevenson Award from the Tonys in 2009, a second nomination for 'Broadway Bound' (1987), and two Drama Desk nominations, building one of the more decorated Broadway careers of her generation.",
            "She was also a television personality and activist, co-founding the Phyllis Newman Women's Health Initiative to support women in the theater industry facing serious illness.",
        ],
        "card": [
            {"label": "Born", "value": "March 19, 1933, Jersey City, New Jersey"},
            {"label": "Died", "value": "September 15, 2019"},
            {"label": "Award", "value": "Tony Award, Best Featured Actress in a Musical (1962)"},
            {"label": "Show", "value": "Subways Are for Sleeping (1962)"},
            {"label": "Style", "value": "Musical theater, Broadway"},
        ],
    },
    "johnny-rotella": {
        "facts": [
            "Johnny Rotella (November 4, 1920 -- September 11, 2014) was an American woodwind player, session musician, and songwriter from Jersey City, New Jersey, whose career spanned more than six decades.",
            "He wrote over 200 songs, including the Frank Sinatra standard 'Nothing but the Best', and his woodwind playing appears on countless recordings from the 1940s through the 1990s as one of the most in-demand session reed players in New York.",
        ],
        "card": [
            {"label": "Born", "value": "November 4, 1920, Jersey City, New Jersey"},
            {"label": "Died", "value": "September 11, 2014"},
            {"label": "Instruments", "value": "Woodwinds (reeds)"},
            {"label": "Notable song", "value": "Nothing but the Best (Frank Sinatra)"},
            {"label": "Songs written", "value": "200+"},
        ],
    },
    "basil-ruysdael": {
        "facts": [
            "Basil Ruysdael (1888 -- 1960) was an American actor, singer, and opera bass who was born in Jersey City, New Jersey, and performed on Broadway and in early Hollywood films through the 1940s and 1950s.",
            "He sang bass roles with major American opera companies before transitioning to acting, appearing in films including 'Come to the Stable' (1949) and 'Broken Arrow' (1950).",
        ],
        "card": [
            {"label": "Born", "value": "1888, Jersey City, New Jersey"},
            {"label": "Died", "value": "1960"},
            {"label": "Voice type", "value": "Bass (opera)"},
            {"label": "Career", "value": "Opera, Broadway, Hollywood films"},
            {"label": "Films", "value": "Come to the Stable (1949); Broken Arrow (1950)"},
        ],
    },
    "ed-shaughnessy": {
        "facts": [
            "Ed Shaughnessy (January 29, 1929 -- February 24, 2013) was an American jazz drummer from Jersey City, New Jersey, best known as the house drummer for 'The Tonight Show Starring Johnny Carson' from 1962 to 1992, a thirty-year run that made him one of the most heard drummers in American television history.",
            "Before The Tonight Show, he recorded and performed with leading jazz figures including Dizzy Gillespie, Coleman Hawkins, and Benny Goodman, establishing his credentials in the bebop and swing traditions.",
        ],
        "card": [
            {"label": "Born", "value": "January 29, 1929, Jersey City, New Jersey"},
            {"label": "Died", "value": "February 24, 2013"},
            {"label": "Instrument", "value": "Drums"},
            {"label": "Known for", "value": "The Tonight Show with Johnny Carson (house drummer, 1962 to 1992)"},
            {"label": "Collaborators", "value": "Dizzy Gillespie, Coleman Hawkins, Benny Goodman"},
        ],
    },
    "frank-sinatra-jr": {
        "facts": [
            "Frank Sinatra Jr. (January 10, 1944 -- March 16, 2016) was an American singer and musician, the son of Frank Sinatra, who spent much of his career as his father's musical director and conductor.",
            "He was kidnapped in December 1963 and held for ransom for several days before being released unharmed, an event that made national headlines and briefly overshadowed his early career.",
            "As a performer and conductor he carried the Great American Songbook tradition forward, touring extensively as both a solo artist and his father's musical director from the 1980s until his death.",
        ],
        "card": [
            {"label": "Born", "value": "January 10, 1944"},
            {"label": "Died", "value": "March 16, 2016"},
            {"label": "Known for", "value": "Frank Sinatra's musical director and conductor"},
            {"label": "Style", "value": "Traditional pop, Great American Songbook"},
        ],
    },
    "claydes-charles-smith": {
        "facts": [
            "Claydes Charles Smith (September 6, 1948 -- June 20, 2006) was a Jersey City-born guitarist and founding member of Kool and the Gang, the funk, soul, and R&B group that grew from Jersey City's Lincoln High School scene in 1964.",
            "As the band's lead guitarist for more than four decades, he contributed to the distinctive riff-driven, horn-section sound that made Kool and the Gang one of the most sampled and commercially successful groups in American popular music.",
        ],
        "card": [
            {"label": "Born", "value": "September 6, 1948, Jersey City, New Jersey"},
            {"label": "Died", "value": "June 20, 2006"},
            {"label": "Instrument", "value": "Guitar"},
            {"label": "Band", "value": "Kool and the Gang (founding member)"},
            {"label": "School", "value": "Lincoln High School, Jersey City"},
        ],
    },
    "tom-tallitsch": {
        "facts": [
            "Tom Tallitsch is a jazz saxophonist and composer with ties to Jersey City, New Jersey, who has led his own ensembles and recorded for independent jazz labels.",
            "He performs primarily on tenor and soprano saxophone and has worked with a range of musicians in the New York metropolitan jazz scene.",
        ],
        "card": [
            {"label": "Instrument", "value": "Tenor and soprano saxophone"},
            {"label": "Style", "value": "Jazz, contemporary"},
        ],
    },
    "dennis-dee-tee-thomas": {
        "facts": [
            "Dennis 'Dee Tee' Thomas (February 9, 1951 -- August 7, 2021) was a founding member of Kool and the Gang, one of the group's most distinctive voices and instrumentalists, known for his alto saxophone playing, flute, and his role as the group's on-stage announcer.",
            "He grew up in Jersey City, New Jersey, attending Lincoln High School alongside the other founding members, and was with the band from its formation in 1964 through its final years, one of the most consistent presences in a decades-long lineup.",
        ],
        "card": [
            {"label": "Born", "value": "February 9, 1951, Jersey City, New Jersey"},
            {"label": "Died", "value": "August 7, 2021"},
            {"label": "Instruments", "value": "Alto saxophone, flute, percussion"},
            {"label": "Band", "value": "Kool and the Gang (founding member)"},
            {"label": "School", "value": "Lincoln High School, Jersey City"},
        ],
    },
    "dickie-thompson": {
        "facts": [
            "Dickie Thompson is an American musician with Jersey City, New Jersey, connections who performed in jazz and popular music contexts.",
        ],
        "card": [
            {"label": "Scene", "value": "Jersey City, New Jersey"},
            {"label": "Style", "value": "Jazz, popular music"},
        ],
    },
    "joseph-trapanese": {
        "facts": [
            "Joseph Trapanese is an American composer, arranger, and producer from Jersey City, New Jersey, who has worked extensively in film, television, and video game scoring.",
            "His credits include composing music for 'Oblivion' (2013), 'The Greatest Showman' (2017), 'Tron: Uprising' (animated series), and 'Straight Outta Compton' (2015), establishing him as one of the more successful film composers with Jersey City roots.",
        ],
        "card": [
            {"label": "Origin", "value": "Jersey City, New Jersey"},
            {"label": "Specialty", "value": "Film, TV, video game scoring"},
            {"label": "Credits", "value": "Oblivion (2013); The Greatest Showman (2017); Straight Outta Compton (2015); Tron: Uprising"},
        ],
    },
    "tommy-west": {
        "facts": [
            "Tommy West is an American musician and record producer from Jersey City, New Jersey, who is best known as the longtime producer and creative partner of Jim Croce, producing Croce's 'You Don't Mess Around with Jim' (1972) and 'Bad, Bad Leroy Brown' (1973), both of which topped the Billboard Hot 100.",
            "He co-ran Terry Cashman and Tommy West Productions, one of the more successful independent production companies of the early 1970s, and continued working in recording and production after Croce's death in 1973.",
        ],
        "card": [
            {"label": "Origin", "value": "Jersey City, New Jersey"},
            {"label": "Known for", "value": "Producing Jim Croce (You Don't Mess Around with Jim; Bad, Bad Leroy Brown)"},
            {"label": "Company", "value": "Cashman and West Productions"},
            {"label": "Era", "value": "1970s"},
        ],
    },
    "the-black-hollies": {
        "facts": [
            "The Black Hollies are a rock band from Jersey City, New Jersey, formed in the 2000s and known for their heavy debt to 1960s British Invasion and American garage rock aesthetics.",
            "They have released albums on Ernest Jenning Record Co. and toured alongside acts including The Raveonettes and The Black Angels, building a following in the rock underground.",
        ],
        "card": [
            {"label": "Origin", "value": "Jersey City, New Jersey"},
            {"label": "Style", "value": "Garage rock, psychedelia, 1960s-influenced rock"},
            {"label": "Label", "value": "Ernest Jenning Record Co."},
        ],
    },
    "the-components": {
        "facts": [
            "The Components are an American alternative rock band from New Jersey with Jersey City connections, active in the independent rock scene.",
        ],
        "card": [
            {"label": "Scene", "value": "New Jersey (Jersey City connections)"},
            {"label": "Style", "value": "Alternative rock"},
        ],
    },
    "cyclone-static": {
        "facts": [
            "Cyclone Static is an American punk rock band from New Jersey with Jersey City connections, active in the independent punk and rock scene.",
        ],
        "card": [
            {"label": "Scene", "value": "New Jersey (Jersey City connections)"},
            {"label": "Style", "value": "Punk rock"},
        ],
    },
    "dirt-bike-annie": {
        "facts": [
            "Dirt Bike Annie was a pop punk and power pop band formed in New York City with New Jersey connections, active from the late 1990s through the mid-2000s and known for melodic, hook-driven songwriting in the vein of the Lookout Records catalog.",
        ],
        "card": [
            {"label": "Scene", "value": "New York / New Jersey"},
            {"label": "Style", "value": "Pop punk, power pop"},
            {"label": "Era", "value": "Late 1990s to mid-2000s"},
        ],
    },
    "the-heartaches": {
        "facts": [
            "The Heartaches were an American doo-wop group from Jersey City, New Jersey, formed in 1962 and active through 1989, one of the city's longest-running vocal groups of the post-Duprees era.",
            "They recorded and performed through the decline and revival of doo-wop, spanning a twenty-seven-year run that included label recordings and local performance circuit activity.",
        ],
        "card": [
            {"label": "Origin", "value": "Jersey City, New Jersey"},
            {"label": "Active", "value": "1962 to 1989"},
            {"label": "Style", "value": "Doo-wop"},
        ],
    },
    "the-multi-purpose-solution": {
        "facts": [
            "The Multi-Purpose Solution are an American rock band from New Jersey with Jersey City connections, active in the independent rock scene.",
        ],
        "card": [
            {"label": "Scene", "value": "New Jersey (Jersey City connections)"},
            {"label": "Style", "value": "Rock"},
        ],
    },
    "the-one-and-nines": {
        "facts": [
            "The One and Nines are an American rhythm and blues band from New Jersey with Jersey City connections.",
        ],
        "card": [
            {"label": "Scene", "value": "New Jersey (Jersey City connections)"},
            {"label": "Style", "value": "R&B"},
        ],
    },
    "overlake": {
        "facts": [
            "Overlake is a shoegaze and indie rock trio from Jersey City, New Jersey, whose wall-of-sound approach and dreamy songwriting connects the city's rock underground to the wider American shoegaze revival of the 2010s and 2020s.",
        ],
        "card": [
            {"label": "Origin", "value": "Jersey City, New Jersey"},
            {"label": "Style", "value": "Shoegaze, indie rock"},
        ],
    },
    "spent": {
        "facts": [
            "Spent was an American indie rock band from Jersey City, New Jersey, consisting of singer/guitarist John King, guitarist/keyboardist Annie Hayden, bassist Joe Weston, and drummer Ed Radich.",
            "They released albums on Thrill Jockey Records through the 1990s and were associated with the downtown New York and Jersey City indie rock scenes of that era.",
        ],
        "card": [
            {"label": "Origin", "value": "Jersey City, New Jersey"},
            {"label": "Members", "value": "John King, Annie Hayden, Joe Weston, Ed Radich"},
            {"label": "Label", "value": "Thrill Jockey Records"},
            {"label": "Style", "value": "Indie rock"},
            {"label": "Era", "value": "1990s"},
        ],
    },
    "the-vice-rags": {
        "facts": [
            "The Vice Rags are an American rock band from New Jersey with Jersey City connections, active in the independent rock scene.",
        ],
        "card": [
            {"label": "Scene", "value": "New Jersey (Jersey City connections)"},
            {"label": "Style", "value": "Rock"},
        ],
    },
    "paul-banks": {
        "facts": [
            "Paul Banks is an American jazz pianist from Jersey City, New Jersey, who has performed and recorded in the New York metropolitan jazz scene.",
        ],
        "card": [
            {"label": "Scene", "value": "Jersey City, New Jersey"},
            {"label": "Instrument", "value": "Piano"},
            {"label": "Style", "value": "Jazz"},
        ],
    },
    "john-p-hammond": {
        "facts": [
            "John P. Hammond (born November 13, 1942) is an American blues singer, guitarist, and harmonica player from New York who has recorded for Vanguard and other labels and is recognized as one of the most dedicated white blues revivalists of his generation.",
            "He is the son of legendary Columbia Records producer John Hammond Sr. and has performed with figures including Mike Bloomfield, Dr. John, and Duane Allman over a career spanning more than six decades.",
        ],
        "card": [
            {"label": "Born", "value": "November 13, 1942"},
            {"label": "Instruments", "value": "Guitar, harmonica, vocals"},
            {"label": "Style", "value": "Delta blues, acoustic blues"},
            {"label": "Labels", "value": "Vanguard, Columbia, Atlantic"},
            {"label": "Collaborators", "value": "Mike Bloomfield, Dr. John, Duane Allman"},
        ],
    },
    "hao-huang": {
        "facts": [
            "Hao Huang is an American pianist and educator with ties to Jersey City, New Jersey, known for concert performances and for his writing and research on music and culture.",
        ],
        "card": [
            {"label": "Instrument", "value": "Piano"},
            {"label": "Style", "value": "Classical, contemporary"},
        ],
    },
    "kid-buu": {
        "facts": [
            "Kid Buu is a rapper from Jersey City, New Jersey, who built his following on the underground rap circuit and has released music on streaming platforms including Spotify and Apple Music.",
            "He is known for an aggressive street rap style and has collaborated with other artists from the New Jersey and New York independent rap scenes.",
        ],
        "card": [
            {"label": "Origin", "value": "Jersey City, New Jersey"},
            {"label": "Style", "value": "Street rap, underground hip-hop"},
        ],
    },
    "gil-melle": {
        "facts": [
            "Gil Melle (December 31, 1931 -- December 28, 2004) was an American jazz musician, painter, and electronic music composer from Jersey City, New Jersey, who was among the first jazz artists to record as a leader for Blue Note Records.",
            "His early Blue Note sessions in the 1950s featured a hard bop and progressive jazz approach; he later moved into electronic music and became a pioneering composer of science fiction film and television scores, including the original 'The Andromeda Strain' (1971) soundtrack.",
        ],
        "card": [
            {"label": "Born", "value": "December 31, 1931, Jersey City, New Jersey"},
            {"label": "Died", "value": "December 28, 2004"},
            {"label": "Instruments", "value": "Saxophone, baritone sax, electronic instruments"},
            {"label": "Label", "value": "Blue Note Records (early 1950s)"},
            {"label": "Known for", "value": "The Andromeda Strain soundtrack (1971); early Blue Note sessions"},
            {"label": "Style", "value": "Jazz, electronic, film scoring"},
        ],
    },
    # ---- Modern / current Jersey City artists (community-identified) ----
    "the-heat": {
        "facts": [
            "The Heat is a Jersey City rap group documented in the archive's survey of the city's active hip-hop community.",
            "Their biography and catalog await fuller documentation from the community or from its members.",
        ],
        "card": [
            {"label": "Scene", "value": "Jersey City, New Jersey"},
            {"label": "Style", "value": "Hip-hop"},
        ],
    },
    "bralikk-animalz": {
        "facts": [
            "Bralikk Animalz is a Jersey City rap collective documented in the archive's survey of the city's active hip-hop community.",
            "Their biography and catalog await fuller documentation from the community or from its members.",
        ],
        "card": [
            {"label": "Scene", "value": "Jersey City, New Jersey"},
            {"label": "Style", "value": "Hip-hop"},
        ],
    },
    "block-royal": {
        "facts": [
            "Block Royal is a Jersey City rap artist or group documented in the archive's survey of the city's active hip-hop community.",
            "Their biography and catalog await fuller documentation from the community or from its members.",
        ],
        "card": [
            {"label": "Scene", "value": "Jersey City, New Jersey"},
            {"label": "Style", "value": "Hip-hop"},
        ],
    },
    "the-cobras": {
        "facts": [
            "The Cobras is a Jersey City group documented in the archive's survey of the city's active music community.",
            "Their biography and catalog await fuller documentation from the community or from its members.",
        ],
        "card": [
            {"label": "Scene", "value": "Jersey City, New Jersey"},
        ],
    },
    "lil-dev": {
        "facts": [
            "Lil Dev is a Jersey City rapper documented in the archive's survey of the city's active hip-hop community.",
            "Their biography and catalog await fuller documentation from the community or from its subject.",
        ],
        "card": [
            {"label": "Scene", "value": "Jersey City, New Jersey"},
            {"label": "Style", "value": "Hip-hop"},
        ],
    },
    "damngirll": {
        "facts": [
            "DamnGirll is a Jersey City artist documented in the archive's survey of the city's active music community.",
            "Their biography and catalog await fuller documentation from the community or from its subject.",
        ],
        "card": [
            {"label": "Scene", "value": "Jersey City, New Jersey"},
        ],
    },
    "dibiasi": {
        "facts": [
            "Dibiasi is a Jersey City artist documented in the archive's survey of the city's active music community.",
            "Their biography and catalog await fuller documentation from the community or from its subject.",
        ],
        "card": [
            {"label": "Scene", "value": "Jersey City, New Jersey"},
        ],
    },
    "mrcashedout": {
        "facts": [
            "MrCashedOut is a Jersey City artist documented in the archive's survey of the city's active music community.",
            "Their biography and catalog await fuller documentation from the community or from its subject.",
        ],
        "card": [
            {"label": "Scene", "value": "Jersey City, New Jersey"},
        ],
    },
    "big-spanish": {
        "facts": [
            "Big Spanish is a Jersey City rapper documented in the archive's survey of the city's active hip-hop community.",
            "Their biography and catalog await fuller documentation from the community or from its subject.",
        ],
        "card": [
            {"label": "Scene", "value": "Jersey City, New Jersey"},
            {"label": "Style", "value": "Hip-hop"},
        ],
    },
    "mali-g": {
        "facts": [
            "Mali G is a Jersey City artist documented in the archive's survey of the city's active music community.",
            "Their biography and catalog await fuller documentation from the community or from its subject.",
        ],
        "card": [
            {"label": "Scene", "value": "Jersey City, New Jersey"},
        ],
    },
    "taylor-portt": {
        "facts": [
            "Taylor Portt is a Jersey City artist documented in the archive's survey of the city's active music community.",
            "Their biography and catalog await fuller documentation from the community or from its subject.",
        ],
        "card": [
            {"label": "Scene", "value": "Jersey City, New Jersey"},
        ],
    },
    "jade": {
        "facts": [
            "Jade is a Jersey City artist documented in the archive's survey of the city's active music community.",
            "Their biography and catalog await fuller documentation from the community or from its subject.",
        ],
        "card": [
            {"label": "Scene", "value": "Jersey City, New Jersey"},
        ],
    },
    "suzy-q": {
        "facts": [
            "Suzy Q is a Jersey City artist documented in the archive's survey of the city's active music community.",
            "Their biography and catalog await fuller documentation from the community or from its subject.",
        ],
        "card": [
            {"label": "Scene", "value": "Jersey City, New Jersey"},
        ],
    },
    "montana-dess": {
        "facts": [
            "Montana Dess is a Jersey City artist documented in the archive's survey of the city's active music community.",
            "Their biography and catalog await fuller documentation from the community or from its subject.",
        ],
        "card": [
            {"label": "Scene", "value": "Jersey City, New Jersey"},
        ],
    },
    "benny-blanca": {
        "facts": [
            "Benny Blanca is a Jersey City artist documented in the archive's survey of the city's active music community.",
            "Their biography and catalog await fuller documentation from the community or from its subject.",
        ],
        "card": [
            {"label": "Scene", "value": "Jersey City, New Jersey"},
        ],
    },
    "nina-foxx": {
        "facts": [
            "Nina Foxx is a Jersey City artist documented in the archive's survey of the city's active music community.",
            "Their biography and catalog await fuller documentation from the community or from its subject.",
        ],
        "card": [
            {"label": "Scene", "value": "Jersey City, New Jersey"},
        ],
    },
    "j-sass": {
        "facts": [
            "J-Sass is a Jersey City artist documented in the archive's survey of the city's active music community.",
            "Their biography and catalog await fuller documentation from the community or from its subject.",
        ],
        "card": [
            {"label": "Scene", "value": "Jersey City, New Jersey"},
        ],
    },
    "mariah-lynn": {
        "facts": [
            "Mariah Lynn is a rapper and television personality from Jersey City, New Jersey, known for her appearances on 'Love & Hip Hop: New York' (VH1) and for a catalog of street rap singles released independently.",
            "She has built a social media following through her blunt, confrontational rap style and her reality television profile, representing a current generation of Jersey City artists who have gained national visibility through cable television.",
        ],
        "card": [
            {"label": "Origin", "value": "Jersey City, New Jersey"},
            {"label": "Known for", "value": "Love and Hip Hop: New York (VH1)"},
            {"label": "Style", "value": "Street rap, hip-hop"},
        ],
    },
    "didthatt": {
        "facts": [
            "DidThatt is a Jersey City artist documented in the archive's survey of the city's active music community.",
            "Their biography and catalog await fuller documentation from the community or from its subject.",
        ],
        "card": [
            {"label": "Scene", "value": "Jersey City, New Jersey"},
        ],
    },
    "speedy-baby": {
        "facts": [
            "Speedy Baby is a Jersey City artist documented in the archive's survey of the city's active music community.",
            "Their biography and catalog await fuller documentation from the community or from its subject.",
        ],
        "card": [
            {"label": "Scene", "value": "Jersey City, New Jersey"},
        ],
    },
    "dj-rydeout": {
        "facts": [
            "DJ Rydeout is a Jersey City DJ documented in the archive's survey of the city's active DJ community.",
            "Their biography and catalog await fuller documentation from the community or from its subject.",
        ],
        "card": [
            {"label": "Scene", "value": "Jersey City, New Jersey"},
            {"label": "Style", "value": "DJ"},
        ],
    },
    # ---- Handle-only DJs that still need better placeholder text ----
    "dj-k": {
        "facts": [
            "DJ K, also known as Killa K, is a Jersey City DJ whose 'Killa K family' received a direct shoutout from DJ E Double (Double Platinum Entertainment) in the WizTV Jersey City DJ Documentary (2006), placing him firmly in the city's late-1990s and 2000s mixtape scene.",
            "His identity and affiliation were confirmed by DJ DX (Robert Van Liew) in an oral history recorded for The Jersey City Sound in 2026.",
            "He is active on Instagram as @coalitionboy_k; the 'Coalition' in his handle points to a crew affiliation that awaits fuller documentation.",
        ],
        "card": [
            {"label": "Also known as", "value": "Killa K"},
            {"label": "Scene", "value": "Jersey City, New Jersey"},
            {"label": "Documented in", "value": "Jersey City DJ Documentary Vol. 1 (2006)"},
            {"label": "Instagram", "value": "@coalitionboy_k"},
        ],
    },
    "dj-j-nice": {
        "facts": [
            "DJ J Nice is a Jersey City DJ who is distinct from 'Big D Nice', a separate DJ praised in the 2006 WizTV documentary, a distinction confirmed by DJ DX in a 2026 oral history.",
            "He is also not the 'DJ Nice' referenced in the 2006 documentary: Mark Cee's student and other 'Nice' mentions in the film refer to different DJs, per DJ DX's account.",
            "He is active on Instagram as @officialjnice1, where his work and scene connections await fuller documentation from the community or its subject.",
        ],
        "card": [
            {"label": "Scene", "value": "Jersey City, New Jersey"},
            {"label": "Instagram", "value": "@officialjnice1"},
            {"label": "Note", "value": "Distinct from Big D Nice and other DJ Nice figures in the 2006 documentary"},
        ],
    },
    "dj-infamous-jersey-city": {
        "facts": [
            "DJ Infamous is a Jersey City DJ whose handle @inf_201 carries the 201 area code, confirming his local identity and distinguishing him from Atlanta's DJ Infamous, who works in an entirely different market.",
            "This entry documents the Jersey City DJ specifically and awaits fuller biographical detail and catalog receipts from the community and its subject.",
        ],
        "card": [
            {"label": "Scene", "value": "Jersey City, New Jersey (201)"},
            {"label": "Instagram", "value": "@inf_201"},
            {"label": "Note", "value": "Distinct from Atlanta DJ Infamous; this entry covers the Jersey City DJ"},
        ],
    },
    "strong-vic": {
        "facts": [
            "Strong Vic is a Jersey City DJ whose 201 area code in his handle @strongvic201 marks his connection to the city's scene.",
            "He is documented in the archive's survey of Jersey City's DJ community; his biography and catalog await fuller detail from the community or its subject.",
        ],
        "card": [
            {"label": "Scene", "value": "Jersey City, New Jersey (201)"},
            {"label": "Instagram", "value": "@strongvic201"},
        ],
    },
    "dj-bam": {
        "facts": [
            "DJ Bam is a Jersey City DJ whose 201 area code in his handle @djbam201 marks his connection to the city.",
            "He is documented in the archive's survey of Jersey City's DJ community; his biography and catalog await fuller detail from the community or its subject.",
        ],
        "card": [
            {"label": "Scene", "value": "Jersey City, New Jersey (201)"},
            {"label": "Instagram", "value": "@djbam201"},
        ],
    },
    "dj-flamez": {
        "facts": [
            "DJ Flamez is a Jersey City DJ documented in the archive's survey of the city's active DJ community.",
            "His biography and catalog await fuller documentation; this entry holds his place in the record until more detail is available from the community or its subject.",
        ],
        "card": [
            {"label": "Scene", "value": "Jersey City, New Jersey"},
            {"label": "Instagram", "value": "@therealdjflamez"},
        ],
    },
    "juggs": {
        "facts": [
            "Juggs, formerly known as DJ E Murda, is a Jersey City DJ who rebranded from his earlier alias -- a transition documented through community identification.",
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
            "DJ J Dub is a Jersey City DJ who is likely the figure whose name is garbled as 'J Dun' in DJ E Double's segment of the 2006 WizTV documentary, one of several names that community identification and the 201 handle help clarify.",
            "His biography and catalog await fuller documentation from the community or from its subject.",
        ],
        "card": [
            {"label": "Scene", "value": "Jersey City, New Jersey (201)"},
            {"label": "Instagram", "value": "@jdub2o1"},
            {"label": "Possible doc mention", "value": "J Dun garble in E Double's 2006 segment (confirm)"},
        ],
    },
}


def run():
    with DATA.open('r', encoding='utf-8') as f:
        data = json.load(f)

    entries = data['entries']
    applied = 0

    for entry in entries:
        slug = entry.get('slug', '')
        if slug not in ENRICHMENTS2:
            continue
        patch = ENRICHMENTS2[slug]
        if 'facts' in patch:
            entry['facts'] = patch['facts']
        if 'card' in patch:
            entry['card'] = patch['card']
        applied += 1

    with DATA.open('w', encoding='utf-8', newline='\r\n') as f:
        json.dump(data, f, ensure_ascii=False, indent=1)

    print(f'Done. Applied enrichments to {applied} entries.')


if __name__ == '__main__':
    run()
