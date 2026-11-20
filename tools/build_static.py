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

LINKS = [('Home.dc.html#', '/#'), ('Home.dc.html', '/'), ('Project.dc.html', '/work/rosalia-lux/'), ('WorkWith.dc.html', '/work-with-kyle/')]

PERSON = {
    "@type": "Person", "@id": SITE + "/#kyle", "name": "Kyle Daniel Gordon", "alternateName": "Kyle Gordon",
    "disambiguatingDescription": "Los Angeles orchestrator, arranger and conductor (Rosalía's LUX, Oppenheimer, BBC Proms). Not the comedian Kyle Gordon.",
    "jobTitle": ["Orchestrator", "Arranger", "Conductor"],
    "knowsAbout": ["Orchestration", "String arrangements", "Pop strings", "Film scoring", "Conducting"],
    "url": SITE + "/", "image": OG, "email": "mailto:kylegordonmusic@gmail.com",
    "homeLocation": {"@type": "Place", "name": "Los Angeles, California"},
    "alumniOf": {"@type": "CollegeOrUniversity", "name": "University of North Texas"},
    "award": "Billboard Award, #1 Classical Album (Romani: The Untold Story), 2024",
    "subjectOf": [{"@type": "NewsArticle", "headline": "'Art for Art's Sake': Rosalía's Collaborators Reflect on 'Lux'",
                   "publisher": {"@type": "Organization", "name": "Rolling Stone"},
                   "url": "https://www.rollingstone.com/music/music-features/rosalia-lux-collaborators-making-of-1235470741/"}],
    "sameAs": ["https://www.imdb.com/name/nm8773349/", "https://www.instagram.com/kylegordonmusic/"]}
ALBUM = {
    "@type": "MusicAlbum", "@id": SITE + "/work/rosalia-lux/#album", "name": "LUX",
    "byArtist": {"@type": "MusicGroup", "name": "Rosalía"}, "datePublished": "2025-11-07",
    "recordLabel": {"@type": "Organization", "name": "Columbia Records"},
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
WEBSITE = {"@type": "WebSite", "@id": SITE + "/#site", "url": SITE + "/", "name": "Kyle Daniel Gordon", "publisher": {"@id": SITE + "/#kyle"}}

PAGES = [
    dict(src='Home.dc.html', out='index.html', path='/',
         title='Kyle Daniel Gordon, Orchestrator for Rosalía’s LUX',
         desc='Orchestrator, arranger and conductor in Los Angeles. Pop string arrangements and orchestrations for Rosalía’s LUX, Oppenheimer and Bridgerton.',
         graph=[WEBSITE, PERSON, ALBUM] + EVENTS),
    dict(src='Project.dc.html', out='work/rosalia-lux/index.html', path='/work/rosalia-lux/',
         title='Rosalía LUX Orchestrations, Kyle Daniel Gordon',
         desc='Kyle Daniel Gordon orchestrated Rosalía’s LUX, recorded with the London Symphony Orchestra at AIR Studios. Six Latin Grammys, ten Grammy nominations.',
         graph=[PERSON, ALBUM, {"@type": "BreadcrumbList", "itemListElement": [
             {"@type": "ListItem", "position": 1, "name": "Work", "item": SITE + "/#work"},
             {"@type": "ListItem", "position": 2, "name": "Rosalía, LUX", "item": SITE + "/work/rosalia-lux/"}]}],
         og=SITE + blob2path[A['rosalia-lux-album']]),
    dict(src='WorkWith.dc.html', out='work-with-kyle/index.html', path='/work-with-kyle/',
         title='Hire an Orchestrator: Kyle Daniel Gordon',
         desc='Orchestration, pop string arrangements and conducting for composers, artists and labels. Orchestrator on Rosalía’s LUX, Oppenheimer and the BBC Proms.',
         graph=[PERSON, {"@type": "Service", "serviceType": "Orchestration and string arrangements", "provider": {"@id": SITE + "/#kyle"},
                         "areaServed": "Worldwide", "description": "Orchestration, pop string arrangements and conducting for film, television, records and live shows."}]),
]

FAVICON = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" fill="#1b1a17"/><g stroke="#f7f4ec" stroke-width="2.2"><path d="M10 20h44M10 27h44M10 34h44M10 41h44M10 48h44"/></g><ellipse cx="34" cy="37.5" rx="8" ry="5.5" fill="#e2581a" transform="rotate(-22 34 37.5)"/><path d="M41.2 35V13" stroke="#e2581a" stroke-width="2.6"/></svg>'''
open(os.path.join(OUT, 'favicon.svg'), 'w').write(FAVICON)


def fix(s):
    for a, b in blob2path.items():
        s = s.replace(a, b)
    for a, b in LINKS:
        s = s.replace(f'href="{a}', f'href="{b}')
    s = re.sub(r'<a href="(https?://[^"]+)"', r'<a href="\1" target="_blank" rel="noopener"', s)
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
<link rel="canonical" href="{canon}">
<meta name="author" content="Kyle Daniel Gordon">
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
<html lang="en">
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
<p style="margin: 0; font-size: 18px">The page you were looking for isn’t here. <a href="/" style="color: #e2581a">Back to the score</a>.</p>
</main></body>''', home, flags=re.S)
h404 = h404.replace('<link rel="canonical"', '<meta name="robots" content="noindex">\n<link rel="canonical"')
open(os.path.join(OUT, '404.html'), 'w', encoding='utf-8').write(h404)

# ---- sitemap, robots, netlify config, readme
urls = ''.join(f'<url><loc>{SITE}{p["path"]}</loc><changefreq>monthly</changefreq><priority>{"1.0" if p["path"] == "/" else "0.8"}</priority></url>' for p in PAGES)
open(os.path.join(OUT, 'sitemap.xml'), 'w').write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
open(os.path.join(OUT, 'robots.txt'), 'w').write(f'User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n')
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
