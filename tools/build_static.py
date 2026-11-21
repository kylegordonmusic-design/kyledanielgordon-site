"""Build the live static site for kyledanielgordon.com from the design pages.

Usage: python3 build_static.py <design project dir> <images dir> <out dir>
"""
import os, re, sys, json, shutil
from PIL import Image

SRC, IMGDIR, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
SITE = 'https://www.kyledanielgordon.com'
A = json.load(open('/home/claude/kdg_scripts/assets.json'))
GRAIN_BLOB = '/_blob/80095bbcfe99eac870fb89454132fd08'

if os.path.exists(OUT):
    shutil.rmtree(OUT)
os.makedirs(os.path.join(OUT, 'img'))

# ---- images: SEO file names
blob2path = {GRAIN_BLOB: '/img/grain.png'}
shutil.copy('/home/claude/kdg_tex/grain.png', os.path.join(OUT, 'img', 'grain.png'))
for key, blob in A.items():
    name = f'{key}-kyle-daniel-gordon-orchestrator.jpg'
    shutil.copy(os.path.join(IMGDIR, key + '.jpg'), os.path.join(OUT, 'img', name))
    blob2path[blob] = '/img/' + name

# ---- social share image 1200x630
im = Image.open(os.path.join(IMGDIR, 'conducting-london-symphony-orchestra.jpg')).convert('RGB')
w, h = im.size
tw = int(h * 1200 / 630)
if tw <= w:
    im = im.crop(((w - tw) // 2, 0, (w - tw) // 2 + tw, h))
im.resize((1200, 630), Image.LANCZOS).save(os.path.join(OUT, 'img', 'kyle-daniel-gordon-orchestrator-share.jpg'), quality=84)
OG = SITE + '/img/kyle-daniel-gordon-orchestrator-share.jpg'
OGDIR = '/home/claude/kdg_scripts/og'
for f in os.listdir(OGDIR):
    shutil.copy(os.path.join(OGDIR, f), os.path.join(OUT, 'img', f'share-{f[:-4]}-kyle-daniel-gordon.jpg'))
def ogi(n): return f'{SITE}/img/share-{n}-kyle-daniel-gordon.jpg'
OG = ogi('home')

LINKS = [('Home.dc.html#', '/#'), ('Home.dc.html', '/'), ('ProjectES.dc.html', '/es/rosalia-lux/'), ('Project.dc.html', '/work/rosalia-lux/'), ('WorkWith.dc.html', '/work-with-kyle/'), ('Oppenheimer.dc.html', '/work/oppenheimer/'), ('Live.dc.html', '/live/'), ('PopStrings.dc.html', '/pop-strings/'), ('Press.dc.html', '/press/'), ('Privacy.dc.html', '/privacy/'), ('LA.dc.html', '/orchestrator-los-angeles/'), ('Orchestrator.dc.html', '/what-does-an-orchestrator-do/'), ('Contact.dc.html', '/contact/'), ('Rec-romani.dc.html', '/work/romani-the-untold-story/'), ('Rec-babyshark.dc.html', '/work/baby-shark-london-symphony-orchestra/'), ('Rec-gracekelly.dc.html', '/work/grace-kelly-with-strings-at-the-movies/'), ('Rec-friesen.dc.html', '/work/david-friesen-this-light-has-no-darkness/'), ('Rec-mollie.dc.html', '/work/mollie-elizabeth-people-pleaser/'), ('Rec-ariza.dc.html', '/work/ariza-magia-en-dos/')]

PERSON = {
    "@type": "Person", "@id": SITE + "/#kyle", "name": "Kyle Daniel Gordon", "alternateName": "Kyle Gordon",
    "disambiguatingDescription": "Los Angeles orchestrator, arranger and conductor (Rosalía's LUX, Oppenheimer, BBC Proms). Not the comedian Kyle Gordon.",
    "jobTitle": ["Orchestrator", "Arranger", "Conductor"],
    "hasOccupation": [{"@type": "Occupation", "name": n, "occupationLocation": {"@type": "City", "name": "Los Angeles"}} for n in ["Orchestrator", "Music arranger", "Conductor"]],
    "knowsAbout": ["Orchestration", "String arrangements", "Pop strings", "Film scoring", "Conducting", "Score production", "Big band arranging"],
    "worksFor": {"@type": "Organization", "name": "KG Music LLC", "url": SITE + "/"},
    "url": SITE + "/", "image": [{"@type": "ImageObject", "url": SITE + blob2path[A['kyle-daniel-gordon-orchestrator-portrait']], "caption": "Kyle Daniel Gordon, orchestrator"}, {"@type": "ImageObject", "url": SITE + blob2path[A['conducting-london-symphony-orchestra-for-rosalia-lux-lso']], "caption": "Kyle Daniel Gordon conducting"}], "email": "mailto:kylegordonmusic@gmail.com", "contactPoint": {"@type": "ContactPoint", "contactType": "bookings", "email": "kylegordonmusic@gmail.com", "telephone": "+1-818-518-3441", "url": SITE + "/contact/"},
    "homeLocation": {"@type": "Place", "name": "Los Angeles, California"},
    "alumniOf": {"@type": "CollegeOrUniversity", "name": "University of North Texas"},
    "award": "Billboard Award, #1 Classical Album (Romani: The Untold Story), 2024",
    "subjectOf": [{"@type": "NewsArticle", "headline": "'Art for Art's Sake': Rosalía's Collaborators Reflect on 'Lux'",
                   "publisher": {"@type": "Organization", "name": "Rolling Stone"},
                   "url": "https://www.rollingstone.com/music/music-features/rosalia-lux-collaborators-making-of-1235470741/"},
                  {"@type": "NewsArticle", "headline": "Baby Shark Teams Up with the London Symphony Orchestra for a 10-Year Celebration",
                   "publisher": {"@type": "Organization", "name": "The Pinkfong Company"}, "url": "https://www.thepinkfongcompany.com/en/news/pr/121"}],
    "sameAs": ["https://www.imdb.com/name/nm8773349/", "https://www.instagram.com/kylegordonmusic/", "https://musicbrainz.org/artist/d642a287-31a5-409d-aaf6-33e91929405c", "https://www.discogs.com/artist/13136118-Kyle-Gordon-7", "https://www.allmusic.com/artist/kyle-daniel-gordon-mn0005019152", "https://www.wikidata.org/wiki/Q136366079", "https://www.youtube.com/@kylegordonmusic", "https://www.linkedin.com/in/kyle-daniel-gordon-5274ab451/", "https://genius.com/artists/Kyle-daniel-gordon"]}
ALBUM = {
    "@type": "MusicAlbum", "@id": SITE + "/work/rosalia-lux/#album", "name": "LUX",
    "byArtist": {"@type": "MusicGroup", "name": "Rosalía"}, "datePublished": "2025-11-07",
    "publisher": {"@type": "Organization", "name": "Columbia Records"},
    "contributor": {"@id": SITE + "/#kyle"}, "award": "Latin Grammy Award for Album of the Year (2026)",
    "image": SITE + blob2path[A['rosalia-lux-album']],
    "sameAs": "https://open.spotify.com/album/3SUEJULSGgBDG1j4GQhfYY"}
RAH = {"@type": "Place", "name": "Royal Albert Hall", "address": "Kensington Gore, London SW7 2AP, United Kingdom"}
BBCCO = {"@type": "MusicGroup", "name": "BBC Concert Orchestra"}
EVENTS = [
    {"@type": "MusicEvent", "name": "BBC Proms: Bond and Beyond", "startDate": "2026-08-25T19:00+01:00", "location": RAH,
     "performer": [BBCCO, {"@id": SITE + "/#kyle"}], "eventStatus": "https://schema.org/EventScheduled"},
    {"@type": "MusicEvent", "name": "BBC Proms: Marvin Gaye, Prince of Soul", "startDate": "2026-08-14T19:00+01:00", "location": RAH,
     "performer": [BBCCO], "contributor": {"@id": SITE + "/#kyle"}},
    {"@type": "MusicEvent", "name": "BBC Proms: Soul Revolution", "startDate": "2025-08-03T19:30+01:00", "location": RAH,
     "performer": [BBCCO], "contributor": {"@id": SITE + "/#kyle"}}]
import datetime
TODAY = datetime.date.today().isoformat()
PROFILE = {"@type": "ProfilePage", "@id": SITE + "/#profile", "url": SITE + "/", "name": "Kyle Daniel Gordon, orchestrator",
           "mainEntity": {"@id": SITE + "/#kyle"}, "dateModified": TODAY, "inLanguage": "en"}
INDEXNOW_KEY = "8f3c2a7d5e9b41c6a0d4f7e2b9c13a58"
WEBSITE = {"@type": "WebSite", "@id": SITE + "/#site", "url": SITE + "/", "name": "Kyle Daniel Gordon", "publisher": {"@id": SITE + "/#kyle"}}

# ---- every credit as structured data: Kyle's role on each work
TYPE = {'Film': 'Movie', 'Television': 'TVSeries', 'Record': 'MusicAlbum', 'Stage': 'MusicEvent', 'Game': 'VideoGame'}
CREDITS = json.load(open('/home/claude/kdg_scripts/credits.json', encoding='utf-8'))
WORKS = {"@type": "ItemList", "@id": SITE + "/#credits", "name": "Credits of Kyle Daniel Gordon", "numberOfItems": len(CREDITS),
         "itemListElement": [{"@type": "ListItem", "position": i + 1, "item": dict(
             {"@type": TYPE.get(c['cat'], 'CreativeWork'), "name": c['title'],
              "contributor": {"@type": "Role", "roleName": c['role'], "contributor": {"@id": SITE + "/#kyle"}}},
             **({"description": c['with_']} if c['with_'] else {}))} for i, c in enumerate(CREDITS) if c['cat'] != 'Stage']}

FAQS = json.load(open('/home/claude/kdg_scripts/faq.json', encoding='utf-8'))
def FAQ(k):
    strip = lambda t: re.sub(r'<[^>]+>', '', t)
    return {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": strip(a)}} for q, a in FAQS[k]]}

PAGES = [
    dict(src='Home.dc.html', out='index.html', path='/',
         title='Kyle Daniel Gordon, Orchestrator for Rosalía’s LUX',
         desc='Orchestrator, arranger and conductor in Los Angeles. Pop string arrangements and orchestrations for Rosalía’s LUX, Oppenheimer and Bridgerton.',
         graph=[WEBSITE, PROFILE, PERSON, ALBUM, WORKS] + EVENTS),
    dict(src='Project.dc.html', out='work/rosalia-lux/index.html', path='/work/rosalia-lux/',
         title='Rosalía LUX Orchestrations, Kyle Daniel Gordon',
         desc='Kyle Daniel Gordon orchestrated Rosalía’s LUX, recorded with the London Symphony Orchestra at AIR Studios. Six Latin Grammys; Grammy Album of the Year nominee.',
         graph=[PERSON, ALBUM, {"@type": "BreadcrumbList", "itemListElement": [
             {"@type": "ListItem", "position": 1, "name": "Work", "item": SITE + "/#work"},
             {"@type": "ListItem", "position": 2, "name": "Rosalía, LUX", "item": SITE + "/work/rosalia-lux/"}]}],
         og=ogi('rosalia-lux'), alternates={'en': '/work/rosalia-lux/', 'es': '/es/rosalia-lux/'}),
    dict(src='ProjectES.dc.html', out='es/rosalia-lux/index.html', path='/es/rosalia-lux/', lang='es',
         alternates={'en': '/work/rosalia-lux/', 'es': '/es/rosalia-lux/'},
         title='Rosalía, LUX: orquestaciones de Kyle Daniel Gordon',
         desc='Kyle Daniel Gordon fue el orquestador principal de LUX de Rosalía, grabado con la Orquesta Sinfónica de Londres. Seis Latin Grammy; nominado al Grammy a Álbum del Año.',
         graph=[PERSON, ALBUM], og=ogi('rosalia-lux')),
    dict(src='WorkWith.dc.html', out='work-with-kyle/index.html', path='/work-with-kyle/',
         title='Hire an Orchestrator: Kyle Daniel Gordon',
         desc='Orchestration, pop string arrangements and conducting for composers, artists and labels. Orchestrator on Rosalía’s LUX, Oppenheimer and the BBC Proms.',
         graph=[PERSON, {"@type": "Service", "serviceType": "Orchestration and string arrangements", "provider": {"@id": SITE + "/#kyle"},
                         "areaServed": "Worldwide", "description": "Orchestration, pop string arrangements and conducting for film, television, records and live shows."}], og=ogi('work-with-kyle')),
    dict(src='Oppenheimer.dc.html', out='work/oppenheimer/index.html', path='/work/oppenheimer/',
         title='Oppenheimer Orchestration, Kyle Daniel Gordon',
         desc='Kyle Daniel Gordon, one of the orchestrators on Ludwig Göransson’s Academy Award-winning score for Christopher Nolan’s Oppenheimer (2023).',
         graph=[PERSON, {"@type": "Movie", "name": "Oppenheimer", "dateCreated": "2023", "director": {"@type": "Person", "name": "Christopher Nolan"},
                         "musicBy": {"@type": "Person", "name": "Ludwig Göransson"}, "contributor": {"@id": SITE + "/#kyle"},
                         "image": SITE + blob2path[A['oppenheimer-film-poster']], "sameAs": "https://www.imdb.com/title/tt15398776/"},
                {"@type": "BreadcrumbList", "itemListElement": [
             {"@type": "ListItem", "position": 1, "name": "Work", "item": SITE + "/#work"},
             {"@type": "ListItem", "position": 2, "name": "Oppenheimer", "item": SITE + "/work/oppenheimer/"}]}],
         og=ogi('oppenheimer')),
    dict(src='Live.dc.html', out='live/index.html', path='/live/',
         title='BBC Proms Arranger and Organist, Kyle Daniel Gordon',
         desc='Arranger and organist at the BBC Proms: Bond and Beyond (Radiohead’s “Spectre”), Soul Revolution, Marvin Gaye. The Little Bird premiered by the San Francisco Symphony.',
         graph=[PERSON] + EVENTS, og=ogi('live')),
    dict(src='PopStrings.dc.html', out='pop-strings/index.html', path='/pop-strings/',
         title='Pop String Arrangements, Kyle Daniel Gordon',
         desc='String and orchestral arrangements for pop artists, from Rosalía’s LUX with the London Symphony Orchestra to records, sessions and live shows.',
         graph=[PERSON, {"@type": "Service", "serviceType": "Pop string arrangements", "provider": {"@id": SITE + "/#kyle"}, "areaServed": "Worldwide",
                         "description": "String and orchestral arrangements for pop and alternative artists: records, recording sessions and live shows."}], og=ogi('pop-strings')),
    dict(src='Privacy.dc.html', out='privacy/index.html', path='/privacy/', title='Privacy, Kyle Daniel Gordon',
         desc='How kyledanielgordon.com measures visits: Cloudflare Web Analytics and Microsoft Clarity. No advertising, no personal data unless you email.',
         graph=[PERSON]),
    dict(src='LA.dc.html', out='orchestrator-los-angeles/index.html', path='/orchestrator-los-angeles/',
         title='Orchestrator in Los Angeles: Kyle Daniel Gordon',
         desc='Los Angeles orchestrator, arranger and conductor for film, TV and records: Rosalía’s LUX, Oppenheimer, Frozen II, Star Wars. Orchestration, strings, score prep.',
         graph=[PERSON, {"@type": "ProfessionalService", "name": "Kyle Daniel Gordon, orchestrator", "url": SITE + "/orchestrator-los-angeles/",
                         "legalName": "KG Music LLC", "founder": {"@id": SITE + "/#kyle"}, "email": "kylegordonmusic@gmail.com", "telephone": "+1-818-518-3441",
                         "address": {"@type": "PostalAddress", "addressLocality": "Los Angeles", "addressRegion": "CA", "addressCountry": "US"},
                         "areaServed": [{"@type": "City", "name": "Los Angeles"}, "Worldwide"],
                         "serviceType": ["Orchestration", "String arrangements", "Score preparation", "Conducting"]}, FAQ('la')]),
    dict(src='Orchestrator.dc.html', out='what-does-an-orchestrator-do/index.html', path='/what-does-an-orchestrator-do/',
         title='What Does an Orchestrator Do? A Guide by Kyle Daniel Gordon',
         desc='What an orchestrator does on a film score and a pop record, how it differs from arranging and composing, and how to hire one. By orchestrator Kyle Daniel Gordon.',
         graph=[PERSON, {"@type": "Article", "headline": "What does an orchestrator do?", "author": {"@id": SITE + "/#kyle"},
                         "datePublished": TODAY, "dateModified": TODAY, "mainEntityOfPage": SITE + "/what-does-an-orchestrator-do/",
                         "about": ["Orchestration", "Film scoring", "String arrangements"], "image": OG}]),
    dict(src='Contact.dc.html', out='contact/index.html', path='/contact/',
         title='Contact Kyle Daniel Gordon, Orchestrator',
         desc='Contact Los Angeles orchestrator Kyle Daniel Gordon for orchestration, string arrangements and conducting: kylegordonmusic@gmail.com, (818) 518-3441.',
         graph=[PERSON, {"@type": "ContactPage", "url": SITE + "/contact/", "mainEntity": {"@id": SITE + "/#kyle"}}, FAQ('contact')]),
    dict(src='Press.dc.html', out='press/index.html', path='/press/',
         title='Press Room: Kyle Daniel Gordon, Orchestrator of LUX',
         desc='Interviews, biographies, photos, credit wording and a press sheet for Kyle Daniel Gordon, orchestrator of Rosalía’s LUX and Oppenheimer.',
         graph=[PERSON]),
]
# ---- record pages (one per project)
RECP = [
 ('Rec-romani.dc.html', '/work/romani-the-untold-story/', 'romani-the-untold-story-london-symphony-orchestra', 'Romani: The Untold Story',
  'Romani: The Untold Story, Ion Zanca & LSO: Kyle Daniel Gordon',
  'Kyle Daniel Gordon arranged, orchestrated and conducted Romani: The Untold Story, Ion Zanca’s No. 1 Billboard Classical album with the Dallas String Quartet and the London Symphony Orchestra.',
  {"@type": "MusicGroup", "name": "Ion Zanca, Dallas String Quartet, London Symphony Orchestra"}, '2024-08-23', 'Dallas String Quartet', 'https://open.spotify.com/track/31eojlHu2jxOHQr5NW74PL'),
 ('Rec-babyshark.dc.html', '/work/baby-shark-london-symphony-orchestra/', 'baby-shark-10th-anniversary-london-symphony-orchestra', 'Baby Shark (London Symphony Orchestra Version)',
  'Baby Shark × London Symphony Orchestra: Arranger & Conductor Kyle Daniel Gordon',
  'Kyle Daniel Gordon arranged and conducted the London Symphony Orchestra version of Baby Shark for its 10th anniversary, recorded at LSO St Luke’s, plus the Bebefinn Medley.',
  {"@type": "MusicGroup", "name": "Pinkfong, London Symphony Orchestra"}, '2025-09-19', 'The Pinkfong Company', 'https://open.spotify.com/album/6myoH7UjcukBliJGvWorpG'),
 ('Rec-gracekelly.dc.html', '/work/grace-kelly-with-strings-at-the-movies/', 'grace-kelly-with-strings-at-the-movies', 'Grace Kelly with Strings: At The Movies',
  'Grace Kelly with Strings: At The Movies, Arranger Kyle Daniel Gordon',
  'Kyle Daniel Gordon was arranger, orchestrator and co-producer on saxophonist Grace Kelly’s film-music album with strings (2024): Morricone, E.T., James Bond, Disney.',
  {"@type": "Person", "name": "Grace Kelly"}, '2024-03-01', 'PAZZ Productions', 'https://open.spotify.com/album/2buBjbRAHUe3QMiWbRuHM0'),
 ('Rec-friesen.dc.html', '/work/david-friesen-this-light-has-no-darkness/', 'david-friesen-this-light-has-no-darkness', 'This Light Has No Darkness, Volume 1',
  'David Friesen, This Light Has No Darkness: Orchestrated by Kyle Daniel Gordon',
  'Bassist David Friesen’s 12-part suite, arranged and orchestrated by Kyle Daniel Gordon for 33-piece chamber orchestra. Origin Records, 2024.',
  {"@type": "Person", "name": "David Friesen"}, '2024-02-16', 'Origin Records', None),
 ('Rec-mollie.dc.html', '/work/mollie-elizabeth-people-pleaser/', 'mollie-elizabeth-people-pleaser', 'People Pleaser',
  'Mollie Elizabeth, People Pleaser: Arranger & Conductor Kyle Daniel Gordon',
  'Kyle Daniel Gordon arranged, orchestrated, score-produced and conducted Mollie Elizabeth’s People Pleaser EP (Capitol Records, 2026), and plays upright bass and music box.',
  {"@type": "Person", "name": "Mollie Elizabeth"}, '2026-10-30', 'Capitol Records', 'https://open.spotify.com/album/6vYVu3wSl9OedjOU8n8pVX'),
 ('Rec-ariza.dc.html', '/work/ariza-magia-en-dos/', 'ariza-magia-en-dos', 'Magia en Dos',
  'Ariza, Magia en Dos: Orchestrator Kyle Daniel Gordon',
  'Kyle Daniel Gordon orchestrated Ariza’s 2025 album Magia en Dos, with Morat, Juliana, nic and ROBI. Orquestador: Kyle Daniel Gordon.',
  {"@type": "Person", "name": "Ariza"}, '2025-05-23', 'Ariza', 'https://open.spotify.com/album/4KTrbaxpyksYA5qWOpPE9l'),
]
for src, path, key, name, title, desc, by, date, label, spot in RECP:
    alb = {"@type": "MusicAlbum", "@id": SITE + path + "#album", "name": name, "byArtist": by, "datePublished": date,
           "publisher": {"@type": "Organization", "name": label}, "contributor": {"@id": SITE + "/#kyle"}, "image": SITE + blob2path[A[key]]}
    if spot: alb["sameAs"] = spot
    PAGES.append(dict(src=src, out=path.strip('/') + '/index.html', path=path, title=title, desc=desc,
                      graph=[PERSON, alb, {"@type": "BreadcrumbList", "itemListElement": [
                          {"@type": "ListItem", "position": 1, "name": "Credits", "item": SITE + "/#credits"},
                          {"@type": "ListItem", "position": 2, "name": name, "item": SITE + path}]}],
                      og=ogi(path.strip('/').split('/')[-1])))


# ---- pitch pages (/for/<slug>/), hidden from search
for pt in json.load(open('/home/claude/kdg_scripts/pitches.json')):
    PAGES.append(dict(src=f'Pitch-{pt["slug"]}.dc.html', out=f'for/{pt["slug"]}/index.html', path=f'/for/{pt["slug"]}/',
                      title=f'For {pt["name"]}, Kyle Daniel Gordon', desc='A note from Kyle Daniel Gordon, orchestrator.', graph=[PERSON], noindex=True, og=ogi('for-' + pt['slug'])))

FAVICON = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" fill="#1b1a17"/><g stroke="#f7f4ec" stroke-width="2.2"><path d="M10 20h44M10 27h44M10 34h44M10 41h44M10 48h44"/></g><ellipse cx="34" cy="37.5" rx="8" ry="5.5" fill="#e2581a" transform="rotate(-22 34 37.5)"/><path d="M41.2 35V13" stroke="#e2581a" stroke-width="2.6"/></svg>'''
open(os.path.join(OUT, 'favicon.svg'), 'w').write(FAVICON)
import shutil as _sh
for _f in os.listdir('/home/claude/kdg_scripts/icons'): _sh.copy(os.path.join('/home/claude/kdg_scripts/icons', _f), os.path.join(OUT, _f))
open(os.path.join(OUT, 'site.webmanifest'), 'w').write(json.dumps({"name": "Kyle Daniel Gordon", "short_name": "Kyle D. Gordon", "start_url": "/", "display": "browser", "background_color": "#f7f4ec", "theme_color": "#f7f4ec", "icons": [{"src": "/icon-192.png", "sizes": "192x192", "type": "image/png"}, {"src": "/icon-512.png", "sizes": "512x512", "type": "image/png"}]}))


def fix(s):
    for a, b in blob2path.items():
        s = s.replace(a, b)
    for a, b in LINKS:
        s = s.replace(f'href="{a}', f'href="{b}')
    s = re.sub(r'<a href="(https?://[^"]+)"', r'<a href="\1" target="_blank" rel="noopener"', s)
    # performance: one slim font request, lazy images
    s = re.sub(r'https://fonts\.googleapis\.com/css2\?[^"]+',
               'https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62,800&amp;family=DM+Mono:wght@400;500&amp;family=Instrument+Sans:wght@400;500;600&amp;family=Instrument+Serif:ital@0;1&amp;display=swap', s)
    s = re.sub(r'<img (?![^>]*loading=)', '<img loading="lazy" ', s)
    s = re.sub(r'<img (?![^>]*decoding=)', '<img decoding="async" ', s)
    s = re.sub(r'<a ([^>]*?)href="(https?://[^"]+)"', lambda m: m.group(0) if 'target=' in m.group(0) else f'<a {m.group(1)}href="{m.group(2)}" target="_blank" rel="noopener"', s)
    return s


def head(p):
    canon = SITE + p['path']
    og = p.get('og', OG)
    ld = json.dumps({"@context": "https://schema.org", "@graph": p['graph']}, ensure_ascii=False, indent=1)
    return f'''<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{p['title']}</title>
<meta name="description" content="{p['desc']}">
{'<meta name="robots" content="noindex, nofollow">' if p.get('noindex') else ''}
<link rel="canonical" href="{canon}">{''.join(f'<link rel="alternate" hreflang="{l}" href="{SITE}{u}">' for l, u in p.get('alternates', {}).items())}{('<link rel="alternate" hreflang="x-default" href="' + SITE + p['alternates']['en'] + '">') if p.get('alternates') else ''}
<meta name="author" content="Kyle Daniel Gordon">
<meta name="msvalidate.01" content="D4D450FFF230A7CE8C4381C45F062F39">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Kyle Daniel Gordon">
<meta property="og:title" content="{p['title']}">
<meta property="og:description" content="{p['desc']}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{og}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{p['title']}">
<meta name="twitter:description" content="{p['desc']}">
<meta name="twitter:image" content="{og}">
<meta name="theme-color" content="#f7f4ec">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon-48.png" sizes="48x48" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<script type="application/ld+json">
{ld}
</script>'''


for p in PAGES:
    s = open(os.path.join(SRC, p['src']), encoding='utf-8').read()
    helmet = re.search(r'<helmet>(.*?)</helmet>', s, re.S).group(1)
    body = re.search(r'</helmet>(.*?)</x-dc>', s, re.S).group(1)
    html = f'''<!doctype html>
<html lang="{p.get('lang', 'en')}">
<head>
{head(p)}
{fix(helmet).strip()}
</head>
<body>
{fix(body).strip()}
</body>
</html>
'''
    dst = os.path.join(OUT, p['out'])
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    open(dst, 'w', encoding='utf-8').write(html)

# ---- 404
home = open(os.path.join(OUT, 'index.html'), encoding='utf-8').read()
h404 = re.sub(r'<body>.*</body>', '''<body><main style="min-height: 100vh; display: flex; flex-direction: column; justify-content: center; gap: 24px; padding: 24px; max-width: 900px; margin: 0 auto; font-family: 'Instrument Sans', system-ui, sans-serif; color: #1b1a17; background: #f7f4ec">
<span style="font-family: 'DM Mono', monospace; font-size: 12px; text-transform: uppercase; letter-spacing: .04em; color: #625d55">Tacet · 404</span>
<h1 style="margin: 0; font-weight: 600; font-size: clamp(48px, 9vw, 110px); line-height: .9; letter-spacing: -.05em">This bar is empty.</h1>
<p style="margin: 0; font-size: 18px">The page you were looking for isn’t here. <a href="/" style="color: #b5410b; display: inline-block; padding: 10px 0">Back to the score</a>.</p>
</main></body>''', home, flags=re.S)
h404 = h404.replace('<link rel="canonical"', '<meta name="robots" content="noindex">\n<link rel="canonical"')
open(os.path.join(OUT, '404.html'), 'w', encoding='utf-8').write(h404)

open(os.path.join(OUT, 'googleb7fd6123e4efb445.html'), 'w').write('google-site-verification: googleb7fd6123e4efb445.html')

# ---- sitemap, robots, netlify config, readme
PHOTOS = {'/work/mollie-elizabeth-people-pleaser/': [SITE + blob2path[A['mollie-elizabeth-people-pleaser']], SITE + blob2path[A['kyle-daniel-gordon-recording-session']]], '/pop-strings/': [SITE + blob2path[A['kyle-daniel-gordon-recording-session']]], '/': [SITE + blob2path[A['kyle-daniel-gordon-orchestrator-portrait']], SITE + blob2path[A['conducting-london-symphony-orchestra']], SITE + blob2path[A['conducting-london-symphony-orchestra-for-rosalia-lux-lso']], SITE + blob2path[A['rosalia-lux-album']]],
          '/work/rosalia-lux/': [SITE + blob2path[A['rosalia-lux-album']], SITE + blob2path[A['kyle-daniel-gordon-rosalia-lux-london-symphony-orchestra-session']], SITE + blob2path[A['conducting-london-symphony-orchestra-for-rosalia-lux-lso']]],
          '/work/oppenheimer/': [SITE + blob2path[A['oppenheimer-film-poster']]],
          '/press/': [SITE + blob2path[A['kyle-daniel-gordon-orchestrator-portrait']], SITE + blob2path[A['kyle-daniel-gordon-recording-session']], SITE + blob2path[A['conducting-london-symphony-orchestra']], SITE + blob2path[A['conducting-london-symphony-orchestra-for-rosalia-lux-lso']]]}
urls = ''.join(f'<url><loc>{SITE}{p["path"]}</loc><lastmod>{TODAY}</lastmod><changefreq>monthly</changefreq><priority>{"1.0" if p["path"] == "/" else "0.8"}</priority>'
               + ''.join(f'<image:image><image:loc>{i}</image:loc></image:image>' for i in PHOTOS.get(p['path'], [p.get('og', OG)]))
               + '</url>' for p in PAGES if not p.get('noindex'))
open(os.path.join(OUT, 'sitemap.xml'), 'w').write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">{urls}</urlset>\n')
open(os.path.join(OUT, 'robots.txt'), 'w').write(f'User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n')
open(os.path.join(OUT, INDEXNOW_KEY + '.txt'), 'w').write(INDEXNOW_KEY)
os.makedirs(os.path.join(OUT, 'press'), exist_ok=True); shutil.copy('/home/claude/kdg_scripts/press/kyle-daniel-gordon-press-sheet.pdf', os.path.join(OUT, 'press', 'kyle-daniel-gordon-press-sheet.pdf'))
open(os.path.join(OUT, 'llms.txt'), 'w', encoding='utf-8').write(open('/home/claude/kdg_scripts/llms.txt', encoding='utf-8').read())
open(os.path.join(OUT, 'netlify.toml'), 'w').write('''[build]
  publish = "."

[[redirects]]
  from = "https://kyledanielgordon.com/*"
  to = "https://www.kyledanielgordon.com/:splat"
  status = 301
  force = true

[[headers]]
  for = "/img/*"
  [headers.values]
    Cache-Control = "public, max-age=31536000, immutable"

[[headers]]
  for = "/*"
  [headers.values]
    X-Content-Type-Options = "nosniff"
    Referrer-Policy = "strict-origin-when-cross-origin"
''')
open(os.path.join(OUT, 'README.md'), 'w').write('''# kyledanielgordon.com

Static site for Kyle Daniel Gordon, orchestrator, arranger and conductor.
Hosted on Netlify; every push to `main` deploys automatically.

- `index.html` home
- `work/rosalia-lux/` LUX project page
- `work-with-kyle/` services
- `img/` images (file names carry project + name for search)
''')
print('built', sorted(os.path.relpath(os.path.join(d, f), OUT) for d, _, fs in os.walk(OUT) for f in fs if not f.endswith('.jpg')))

# ---- speed pass: responsive WebP, self-hosted fonts, instant navigation, service worker
sys.path.insert(0, '/home/claude/kdg_scripts')
import speed
speed.optimize(OUT)
