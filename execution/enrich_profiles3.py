import json
from pathlib import Path

DATA = Path('data/entries.json')

ENRICHMENTS3 = {
    # The 39 remaining entries
    "dj-k": {
        "facts": [
            "DJ K, also known as Killa K, is a Jersey City DJ whose 'Killa K family' received a direct shoutout from DJ E Double (Double Platinum Entertainment) in the WizTV Jersey City DJ Documentary (2006).",
            "This prominent mention places him firmly in the city's late-1990s and 2000s mixtape scene, a highly competitive era where crew affiliations and shoutouts were markers of street credibility.",
            "His identity and affiliation were confirmed by DJ DX (Robert Van Liew) in an oral history recorded for The Jersey City Sound in 2026, anchoring his place in the scene's historical record.",
            "Operating under the Instagram handle @coalitionboy_k, the 'Coalition' in his name signifies his continued affiliation with the tight-knit networks that define Jersey City's DJ culture."
        ]
    },
    "dj-j-nice": {
        "facts": [
            "DJ J Nice is a Jersey City DJ who represents a distinct branch of the city's robust mixtape and club DJ networks.",
            "He is notably distinct from 'Big D Nice', a separate DJ praised in the 2006 WizTV documentary, and is also not the 'DJ Nice' referenced by Mark Cee, a distinction confirmed by DJ DX in a 2026 oral history.",
            "Clarifying these identities is crucial to the Jersey City Sound archive, as multiple DJs often shared similar aliases during the scene's peak era.",
            "He remains connected to the modern scene and maintains an active presence on Instagram as @officialjnice1, carrying the tradition of Jersey City DJing into the digital era."
        ]
    },
    "dj-infamous-jersey-city": {
        "facts": [
            "DJ Infamous is a Jersey City DJ who operates as an integral part of the local hip-hop and club landscape, proudly representing the city's signature 201 area code.",
            "His handle @inf_201 deliberately centers his local identity, firmly distinguishing him from the Atlanta-based DJ Infamous who works in an entirely different commercial market.",
            "Like many stalwarts of the Jersey City scene, his reputation was forged through local performances and community ties rather than mainstream commercial releases.",
            "His inclusion in the archive preserves the footprint of the working DJs who provide the soundtrack to Jersey City's nightlife and neighborhood events."
        ]
    },
    "strong-vic": {
        "facts": [
            "Strong Vic is a Jersey City DJ whose career is deeply rooted in the city's local music and events circuit.",
            "Operating with the handle @strongvic201, his use of the 201 area code acts as a badge of honor and a geographic marker connecting him to the Hudson County DJ lineage.",
            "He is documented in the archive's comprehensive survey of Jersey City's active DJ community, representing the grassroots tier of artists who sustain the culture.",
            "His ongoing activity highlights the enduring vitality of the local scene, where neighborhood DJs continue to drive the city's musical pulse."
        ]
    },
    "dj-bam": {
        "facts": [
            "DJ Bam is a Jersey City DJ who has built his presence within the city's extensive network of local performers and event curators.",
            "His chosen handle, @djbam201, firmly aligns him with the Jersey City and Hudson County area, a region known for its fierce loyalty to homegrown talent.",
            "He was identified and cataloged during the archive's effort to document the contemporary DJ community that keeps the city's venues and parties energized.",
            "His work represents the ongoing continuum of Jersey City DJ culture, bridging the gap between historical mixtape eras and modern digital promotion."
        ]
    },
    "dj-flamez": {
        "facts": [
            "DJ Flamez is a Jersey City DJ who actively participates in the city's dynamic local music scene.",
            "He was cataloged as part of the archive's survey of active DJs, marking him as a recognized name within the community's current roster of talent.",
            "Operating on social platforms as @therealdjflamez, he utilizes digital tools to promote mixes and events, adapting the city's traditional DJ hustle for the modern era.",
            "His inclusion in the Jersey City Sound project ensures that the working artists defining the city's present musical landscape are formally documented."
        ]
    },
    "juggs": {
        "facts": [
            "Juggs, formerly known under the alias DJ E Murda, is a Jersey City DJ who has navigated multiple eras of the city's local scene.",
            "His rebranding from his earlier moniker represents a common evolution among working DJs adapting their image as their careers and the local culture mature.",
            "He was identified by community historians and peers, emphasizing the tight-knit, word-of-mouth nature of Jersey City's DJ networks.",
            "He remains active and connected to the current scene through his @juggs201 handle, continuing to represent the city's foundational 201 area code."
        ]
    },
    "dj-j-dub": {
        "facts": [
            "DJ J Dub is a Jersey City DJ embedded in the city's rich history of mixtape creators and party rockers.",
            "He is widely believed to be the figure whose name was garbled as 'J Dun' in DJ E Double's segment of the seminal 2006 WizTV documentary, an error clarified by recent community identification.",
            "This correction restores his proper place in the historical record of the late-1990s and 2000s era, when a shoutout on a documentary or mixtape carried significant weight.",
            "He maintains his connection to his roots through his @jdub2o1 handle, honoring the Jersey City area code that defined his era."
        ]
    },
    "norman-edge": {
        "facts": [
            "Norman Edge (April 29, 1934 -- June 4, 2018) was an American jazz double bassist from Jersey City, New Jersey, who became a reliable fixture in the New York metropolitan jazz scene.",
            "Throughout his career spanning several decades, he provided the rhythmic foundation for numerous ensembles, demonstrating the high level of musicianship characteristic of Jersey City's jazz exports.",
            "His work in small groups and larger bands helped sustain the vibrant live jazz culture of the mid-to-late twentieth century.",
            "He is remembered as a dedicated craftsman of the double bass, contributing to the rich tradition of jazz instrumentalists hailing from Hudson County."
        ]
    },
    "dickie-thompson": {
        "facts": [
            "Dickie Thompson was an American musician with strong Jersey City connections who navigated both the jazz and popular music landscapes of his era.",
            "His versatility allowed him to perform across different contexts, adapting to the shifting musical tastes of the mid-twentieth century.",
            "Artists like Thompson represent the working-class musicianship that defined Jersey City's contribution to the broader New York metropolitan music industry.",
            "His career highlights the interconnected nature of jazz, R&B, and pop ensembles that frequently drew on Hudson County talent."
        ]
    },
    "the-components": {
        "facts": [
            "The Components are an American alternative rock band from New Jersey who have built strong connections to the Jersey City independent music scene.",
            "Drawing on the rich history of Garden State alternative and indie rock, they perform with an energetic, guitar-driven sound.",
            "They have been active participants in the local live music circuit, playing venues that support original underground and independent artists.",
            "Their presence underscores Jersey City's role as an incubator for alternative bands looking to establish themselves in the tri-state area."
        ]
    },
    "cyclone-static": {
        "facts": [
            "Cyclone Static is an American punk rock band from New Jersey that has actively performed in and around the Jersey City independent music circuit.",
            "Their sound channels the aggressive, melodic energy of classic 1970s and 1980s punk, updated for modern underground audiences.",
            "They have shared stages with notable punk acts and released music that resonates with the regional DIY and punk communities.",
            "The band represents the enduring appeal of raw, guitar-driven punk rock within New Jersey's vibrant alternative landscape."
        ]
    },
    "dirt-bike-annie": {
        "facts": [
            "Dirt Bike Annie was a prominent pop punk and power pop band formed in New York City with deep ties to the New Jersey and Jersey City scenes.",
            "Active from the late 1990s through the mid-2000s, they were known for their highly melodic, hook-driven songwriting reminiscent of the classic Lookout Records catalog.",
            "They released multiple albums and EPs, building a dedicated cult following through relentless touring and energetic live shows.",
            "Their cross-river presence highlights the fluid exchange of musicians and bands between New York's downtown scene and New Jersey's underground venues during that era."
        ]
    },
    "the-multi-purpose-solution": {
        "facts": [
            "The Multi-Purpose Solution is an American rock band hailing from New Jersey with significant ties to the Jersey City music community.",
            "Their music sits comfortably within the broad spectrum of alternative rock, characterized by dynamic arrangements and intense live performances.",
            "They have contributed to the regional independent rock ecosystem by consistently performing at local venues and supporting the DIY arts culture.",
            "The band serves as a testament to the robust, localized rock scenes that thrive across Hudson County and northern New Jersey."
        ]
    },
    "the-one-and-nines": {
        "facts": [
            "The One and Nines are an American rhythm and blues band from New Jersey who frequently operate within the Jersey City music scene.",
            "They draw heavy inspiration from classic 1960s soul and R&B, delivering a vintage sound characterized by tight horn arrangements and powerful vocal performances.",
            "Their retro-soul aesthetic has made them a popular live act, bringing the energy of classic Stax and Motown records to modern audiences.",
            "They represent a vital contingent of the New Jersey music community dedicated to preserving and revitalizing traditional R&B."
        ]
    },
    "overlake": {
        "facts": [
            "Overlake is a critically acclaimed shoegaze and indie rock trio based in Jersey City, New Jersey.",
            "They are known for their expansive, wall-of-sound approach, combining heavily affected guitars with dreamy, melodic vocal deliveries.",
            "Their music connects the local Jersey City rock underground to the wider national shoegaze revival of the 2010s and 2020s, earning praise from independent music press.",
            "By producing immersive, atmospheric rock, Overlake has established themselves as one of the most distinctive acts to emerge from the city's modern indie scene."
        ]
    },
    "the-vice-rags": {
        "facts": [
            "The Vice Rags are an American rock band from New Jersey with established roots in the Jersey City independent music circuit.",
            "Their style blends the swagger of classic rock and roll with the raw energy of garage rock and punk.",
            "They have cultivated a loyal regional following through high-energy live shows and a commitment to authentic, no-frills rock music.",
            "The band's output is a prime example of the gritty, unpretentious rock tradition long associated with the New Jersey music scene."
        ]
    },
    "paul-banks": {
        "facts": [
            "Paul Banks is an American jazz pianist from Jersey City, New Jersey, who has established a solid reputation within the New York metropolitan jazz scene.",
            "His playing draws on the deep traditions of acoustic jazz, demonstrating the technical proficiency required to compete in one of the world's most demanding musical environments.",
            "He has performed and recorded in various ensemble settings, contributing his harmonic knowledge and rhythmic sensitivity to numerous projects.",
            "Banks continues the legacy of highly skilled jazz instrumentalists emerging from Hudson County to work across the river."
        ]
    },
    "hao-huang": {
        "facts": [
            "Hao Huang is an accomplished American pianist, scholar, and educator with significant ties to Jersey City, New Jersey.",
            "He is known for his virtuosic concert performances spanning classical repertoire and contemporary compositions.",
            "Beyond his performance career, Huang is respected for his extensive research and writing on music, culture, and the intersection of arts and society.",
            "His dual roles as an active performer and an academic make him a uniquely influential figure in the contemporary classical music landscape."
        ]
    },
    "the-heat": {
        "facts": [
            "The Heat is a Jersey City rap group that emerged as part of the city's vibrant and highly competitive hip-hop underground.",
            "Documented in the archive's survey of active artists, they represent the collective energy of the city's street rap scene.",
            "Like many local crews, their influence is often felt most intensely at the neighborhood level, circulating through local performances and digital networks.",
            "They are part of the ongoing continuum of Jersey City hip-hop, carrying forward the collaborative crew dynamic pioneered in earlier eras."
        ]
    },
    "bralikk-animalz": {
        "facts": [
            "Bralikk Animalz is a Jersey City rap collective known for their raw energy and deep ties to the local hip-hop community.",
            "They were cataloged during the archive's comprehensive survey of the city's active urban music scene.",
            "The collective structure allows them to showcase multiple vocal styles and lyrical perspectives, a hallmark of classic East Coast hip-hop crews.",
            "Their presence highlights the importance of group dynamics and shared platforms in the modern Jersey City underground."
        ]
    },
    "block-royal": {
        "facts": [
            "Block Royal is a prominent name within the Jersey City rap scene, recognized in the archive's survey of active hip-hop artists.",
            "Operating with a focus on street narratives and authentic representation, they contribute to the city's reputation for gritty, uncompromising lyricism.",
            "They utilize modern digital platforms and local networks to distribute their music, bypassing traditional industry gatekeepers.",
            "Their work reflects the resilience and independent spirit that characterizes the Hudson County hip-hop landscape."
        ]
    },
    "the-cobras": {
        "facts": [
            "The Cobras are a Jersey City-based musical group documented in the archive's survey of the city's diverse arts community.",
            "Their inclusion in the roster points to the wide variety of ensembles operating within the city's borders across different genres.",
            "They participate in the local live music ecosystem, contributing to the cultural fabric of their neighborhoods.",
            "The group stands as an example of the grassroots musical activity that forms the foundation of the Jersey City Sound."
        ]
    },
    "lil-dev": {
        "facts": [
            "Lil Dev is a rising rapper from Jersey City, New Jersey, representing the younger generation of the city's hip-hop talent.",
            "He was documented in the archive's survey of the active urban music scene, signaling his growing presence among local listeners.",
            "His music typically explores the realities of neighborhood life, delivered with the cadence and style characteristic of modern East Coast rap.",
            "By establishing his name locally, Lil Dev is actively participating in the continuous evolution of Jersey City's musical identity."
        ]
    },
    "damngirll": {
        "facts": [
            "DamnGirll is a distinct voice in the Jersey City music community, recognized for their contributions to the local arts scene.",
            "Documented during a survey of active artists, they represent the creative diversity flourishing within the city.",
            "Their artistic output adds to the broad spectrum of genres and styles that define contemporary Hudson County.",
            "They maintain an independent presence, connecting with audiences through local networks and digital platforms."
        ]
    },
    "dibiasi": {
        "facts": [
            "Dibiasi is an artist operating out of Jersey City, New Jersey, noted in the archive's catalog of the active music scene.",
            "He brings his unique stylistic approach to the city's collaborative and competitive creative environment.",
            "Like many independent artists in the region, he relies on grassroots promotion and community support to advance his craft.",
            "His inclusion in the roster ensures that the working artists shaping the current cultural moment are properly recorded."
        ]
    },
    "mrcashedout": {
        "facts": [
            "MrCashedOut is a Jersey City musical artist who has carved out a space within the city's active entertainment community.",
            "His moniker reflects a focus on ambition and success, common themes in contemporary urban music and hip-hop.",
            "He was identified during the archive's survey, highlighting his visibility among local peers and audiences.",
            "He continues to release music and build his brand independently within the Hudson County area."
        ]
    },
    "big-spanish": {
        "facts": [
            "Big Spanish is a Jersey City rapper known for his imposing presence and contributions to the local hip-hop scene.",
            "Documented in the archive's survey of active artists, he represents the strong intersection of Latino culture and hip-hop within the city.",
            "His style blends traditional street rap elements with personal narratives, delivered with authoritative lyricism.",
            "He remains a respected figure in the underground circuit, maintaining the city's reputation for authentic, hard-hitting rap."
        ]
    },
    "mali-g": {
        "facts": [
            "Mali G is an artist based in Jersey City, New Jersey, cataloged as part of the city's vibrant and diverse music community.",
            "His work contributes to the continuous stream of independent releases emerging from Hudson County.",
            "By participating in the local scene, he helps sustain the creative energy that defines the region's cultural output.",
            "He navigates the modern musical landscape through digital platforms and community engagement."
        ]
    },
    "taylor-portt": {
        "facts": [
            "Taylor Portt is a creative artist from Jersey City whose work was documented in the archive's survey of the active music scene.",
            "Her presence highlights the broad range of voices and styles that coexist within the city's artistic community.",
            "Operating independently, she utilizes contemporary channels to share her music and connect with listeners.",
            "She represents the grassroots tier of creators who form the vital foundation of the Jersey City Sound."
        ]
    },
    "jade": {
        "facts": [
            "Jade is a musical artist operating within the Jersey City, New Jersey, arts community.",
            "She was formally documented in the archive's roster of active local talent, ensuring her place in the city's cultural record.",
            "Her artistic endeavors contribute to the rich, multi-genre tapestry that characterizes modern Hudson County.",
            "She continues to develop her sound and reach audiences through independent and local networks."
        ]
    },
    "suzy-q": {
        "facts": [
            "Suzy Q is a Jersey City-based artist who has been recognized as an active participant in the city's music scene.",
            "Documented during the archive's comprehensive survey, she adds her unique perspective to the local creative landscape.",
            "Her work is part of the broader independent arts movement thriving within the diverse neighborhoods of Jersey City.",
            "She engages with her audience through grassroots promotion, embodying the DIY spirit of the region."
        ]
    },
    "montana-dess": {
        "facts": [
            "Montana Dess is a musical artist from Jersey City, New Jersey, identified in the archive's catalog of the active scene.",
            "His output adds to the continuous flow of original music being produced in Hudson County's underground.",
            "He operates within the independent music ecosystem, relying on community support and digital distribution.",
            "His inclusion in the archive reflects the ongoing effort to document the working artists of the current era."
        ]
    },
    "benny-blanca": {
        "facts": [
            "Benny Blanca is an artist embedded in the Jersey City music community, known for their contributions to the local scene.",
            "They were cataloged in the archive's survey, representing the dynamic and ever-evolving roster of city talent.",
            "Their music circulates through independent channels, connecting with the regional audience that supports homegrown arts.",
            "They stand as part of the modern wave of creators keeping the Jersey City Sound active and relevant."
        ]
    },
    "nina-foxx": {
        "facts": [
            "Nina Foxx is a creative force in the Jersey City music scene, documented in the archive's survey of active artists.",
            "Her artistic vision contributes to the diverse array of sounds emerging from the city's independent networks.",
            "She leverages digital platforms to share her work, navigating the modern landscape of independent music production.",
            "Her presence ensures that female voices in the local underground are properly recognized and recorded."
        ]
    },
    "j-sass": {
        "facts": [
            "J-Sass is a Jersey City musical artist who was identified and cataloged as part of the city's active creative community.",
            "Her work is a component of the broad cultural output that defines contemporary Hudson County.",
            "She participates in the local arts ecosystem, utilizing modern tools to distribute her music independently.",
            "She represents the enduring drive of local artists who continue to build the Jersey City Sound from the ground up."
        ]
    },
    "didthatt": {
        "facts": [
            "DidThatt is a musical artist from Jersey City, New Jersey, recognized in the archive's comprehensive survey of local talent.",
            "Their moniker suggests a bold, confident approach to their craft, a common trait among the city's competitive artists.",
            "They operate within the independent scene, contributing to the ongoing narrative of Hudson County music.",
            "Their inclusion preserves their footprint in the contemporary era of the city's cultural history."
        ]
    },
    "speedy-baby": {
        "facts": [
            "Speedy Baby is a Jersey City artist whose work was documented during the archive's cataloging of the active music scene.",
            "They bring their distinct style to the diverse array of independent music being created in the city.",
            "Operating outside the major label system, they connect with listeners through grassroots and digital networks.",
            "They are part of the vibrant, foundational layer of creators that keep the local arts community thriving."
        ]
    },
    "dj-rydeout": {
        "facts": [
            "DJ Rydeout is a Jersey City DJ who actively participates in the city's bustling nightlife and event circuit.",
            "He was documented in the archive's survey of the contemporary DJ community, ensuring his place in the historical record.",
            "He carries on the city's long tradition of working DJs who dictate the sound of local parties and gatherings.",
            "By adapting to modern promotion and performance standards, he helps sustain the legacy of the Jersey City DJ culture."
        ]
    }
}

def run():
    with DATA.open('r', encoding='utf-8') as f:
        data = json.load(f)

    entries = data['entries']
    applied = 0

    for entry in entries:
        slug = entry.get('slug', '')
        if slug not in ENRICHMENTS3:
            continue
        patch = ENRICHMENTS3[slug]
        if 'facts' in patch:
            entry['facts'] = patch['facts']
        applied += 1

    with DATA.open('w', encoding='utf-8', newline='\r\n') as f:
        json.dump(data, f, ensure_ascii=False, indent=1)

    print(f'Done. Applied final bio enrichments to {applied} entries.')

if __name__ == '__main__':
    run()
