import os, sys
OUT = sys.argv[1] if len(sys.argv) > 1 else '.'
GRAIN = '/_blob/80095bbcfe99eac870fb89454132fd08'
FONTS = ('https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..900'
         '&amp;family=Bagel+Fat+One&amp;family=DM+Mono:wght@400;500'
         '&amp;family=Instrument+Sans:wght@400;500;600&amp;display=swap')

COND = "font-family: 'Archivo', 'Arial Narrow', sans-serif; font-stretch: 62%; font-weight: 800; text-transform: uppercase"
WIDE = "font-family: 'Archivo', 'Arial', sans-serif; font-stretch: 125%; font-weight: 800; text-transform: uppercase"
MONO = "font-family: 'DM Mono', ui-monospace, monospace; text-transform: uppercase; letter-spacing: 0.04em"

C = dict(olive='#6f7a1c', peri='#a9c3ff', tang='#e2581a', mag='#cf1f84', sky='#3a97f2', celery='#dfe8b0',
         ink='#262422', paper='#fbf8f2', butter='#f2eddc')

G = [
 'linear-gradient(180deg, #f0e3a4 0%, #e07a2c 48%, #3b170b 100%)',
 'linear-gradient(180deg, #1b1a3f 0%, #3a3fd6 52%, #f2b56b 100%)',
 'radial-gradient(90% 70% at 50% 40%, #f6c1d8 0%, #cf1f84 48%, #2b0a1f 100%)',
 'linear-gradient(180deg, #c9d7ff 0%, #8a9be6 45%, #f0a07a 100%)',
 'linear-gradient(165deg, #0e0e0e 0%, #2a4a2a 50%, #c9e07a 100%)',
 'linear-gradient(180deg, #f7efe0 0%, #b9c9f6 50%, #3a97f2 100%)',
 'radial-gradient(80% 70% at 32% 30%, #ffe6a8 0%, #e2581a 46%, #2a0f08 100%)',
 'linear-gradient(180deg, #2b1022 0%, #8e2a5e 38%, #f08a5d 72%, #f6e2b0 100%)',
 'linear-gradient(180deg, #e9e4d6 0%, #9aa36a 55%, #3c4214 100%)',
 'radial-gradient(70% 60% at 60% 70%, #b6e0ff 0%, #3a97f2 45%, #0b1838 100%)',
]
TITLE_COLS = [C['olive'], C['peri'], C['tang'], C['mag'], C['sky']]

OM = 'Orchestration & music dept.'
FILM = [('Oppenheimer', 'Orchestrator'), ('Frozen II', OM), ('Babylon', OM), ('Black Panther: Wakanda Forever', OM),
        ('Star Wars: The Last Jedi', OM), ('Haunted Mansion', OM), ('Chevalier', OM), ('Cocaine Bear', OM),
        ('Blue Beetle', OM), ('White Noise', OM)]
TV = [('Bridgerton', OM), ('The Mandalorian', OM), ('Star Trek: Strange New Worlds', OM), ('The Simpsons', OM),
      ('Bluey', OM), ('Outer Banks', OM), ('The Serpent Queen', OM), ('Frozen Planet II', OM)]
REC = [('LUX', 'Lead orchestrator', 'Rosalía · London Symphony Orchestra'),
       ('Romani: The Untold Story', 'Arranger, orchestrator, conductor', 'London Symphony Orchestra · Dallas String Quartet'),
       ('Baby Shark 10th Anniversary', 'Arranger, orchestrator, conductor', 'London Symphony Orchestra'),
       ('Soul Revolution', 'Lead orchestrator', 'BBC Proms · BBC Concert Orchestra'),
       ('Grace Kelly with Strings', 'Arranger, orchestrator, co-producer', 'Grace Kelly'),
       ('This Light Has No Darkness', 'Arranger, orchestrator, co-producer', 'David Friesen'),
       ('Magia en Dos', 'Orchestrator', 'Ariza')]

BIO = ("Kyle Daniel Gordon is a Los Angeles orchestrator, arranger and conductor working across film, television and "
       "contemporary music. He was lead orchestrator on Rosalía's LUX with the London Symphony Orchestra, BBC Proms: "
       "Soul Revolution with the BBC Concert Orchestra, and the Baby Shark 10th Anniversary symphonic album.")
BIO2 = ("He leads orchestration teams in Los Angeles for composers including John Williams, Ludwig Göransson, Kris Bowers, "
        "Walter Murphy and Justin Hurwitz, and has conducted sessions and concerts in Los Angeles, Nashville and London.")
BIO3 = ("In 2024 he received a Billboard Award for the #1 Classical Album, for orchestrating and conducting Romani: The Untold "
        "Story with the LSO and Dallas String Quartet. Master's in music, University of North Texas. Carnegie Hall debut "
        "as a bassist, 2018.")


def page(title, body, css, bg, w=1440, h=4000):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{title}</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
<link rel="stylesheet" href="{FONTS}">
<style>
body{{margin:0;background:{bg}}}
a{{color:inherit}}a:hover{{color:inherit}}
.grain{{position:absolute;inset:0;pointer-events:none;background-image:url({GRAIN});background-size:240px 240px;mix-blend-mode:overlay;opacity:.32}}
.grainm{{position:absolute;inset:0;pointer-events:none;background-image:url({GRAIN});background-size:240px 240px;mix-blend-mode:multiply;opacity:.07}}
a:focus-visible,button:focus-visible{{outline:2px solid currentColor;outline-offset:4px}}
{css}
@media (prefers-reduced-motion: reduce){{*{{transition:none !important;animation:none !important}}}}
</style>
</helmet>
{body}
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{{"$preview":{{"width":{w},"height":{h}}}}}'>
class Component extends DCLogic {{
  renderVals() {{ return {{}}; }}
}}
</script>
</body>
</html>
'''


def art(g, ratio, extra=''):
    return (f'<span class="art" aria-hidden="true" style="position: relative; display: block; width: 100%; aspect-ratio: {ratio}; '
            f'background: {g}; overflow: hidden{extra}"><span class="grain"></span></span>')


# ------------------------------------------------------------------ A · AFTERGLOW
def build_a():
    css = '''.tile{display:flex;flex-direction:column;align-items:center;gap:14px;text-decoration:none}
.tile .art{transition:transform .5s cubic-bezier(.2,.8,.2,1)}
.tile:hover .art{transform:translateY(-8px) rotate(-1.2deg)}
.tile .t{color:var(--c);text-decoration:underline;text-decoration-thickness:1.5px;text-underline-offset:6px}
.tile:hover .t{text-decoration-thickness:4px}
.scatter{display:grid;grid-template-columns:repeat(12,minmax(0,1fr));column-gap:24px}
.cl{text-decoration:underline;text-underline-offset:5px;text-decoration-thickness:1px}
.cl:hover{text-decoration-thickness:3px}
@media (max-width: 760px){.scatter>*{grid-column:1/-1 !important;margin-top:56px !important}.split>*{grid-column:1/-1 !important}}'''
    items = [
        ('Oppenheimer', 'Film · Orchestrator', '2 / span 3', 0, '2 / 3', G[6]),
        ('LUX', 'Rosalía · LSO · Lead orchestrator', '8 / span 3', 180, '1 / 1', G[2]),
        ('Bridgerton', 'Television', '4 / span 3', 60, '2 / 3', G[3]),
        ('Romani: The Untold Story', 'LSO · Billboard #1 Classical', '9 / span 3', 0, '1 / 1', G[0]),
        ('The Mandalorian', 'Television', '1 / span 3', 40, '2 / 3', G[1]),
        ('Babylon', 'Film', '6 / span 3', 200, '2 / 3', G[7]),
        ('Soul Revolution', 'BBC Proms · Lead orchestrator', '10 / span 3', 30, '1 / 1', G[9]),
        ('Frozen II', 'Film', '3 / span 3', 80, '2 / 3', G[5]),
        ('Baby Shark 10th Anniversary', 'LSO · Arranger, conductor', '8 / span 3', 160, '1 / 1', G[8]),
        ('Black Panther: Wakanda Forever', 'Film', '5 / span 3', 70, '2 / 3', G[4]),
    ]
    tiles = ''
    for i, (t, m, col, mt, ratio, g) in enumerate(items):
        tiles += (f'<a href="#work" class="tile" style="grid-column: {col}; margin-top: {mt}px; --c: {TITLE_COLS[i % 5]}">'
                  + art(g, ratio) +
                  f'<span class="t" style="{COND}; font-size: 26px; line-height: 1.05; text-align: center">{t}</span>'
                  f'<span style="{MONO}; font-size: 11px; color: #6b665e; text-align: center">{m}</span></a>\n')
    body = f'''<div style="position: relative; background: {C['paper']}; color: {C['ink']}; font-family: 'DM Mono', ui-monospace, monospace; font-size: 15px; line-height: 1.6; overflow-x: clip">

<header style="position: relative; height: 800px; overflow: hidden; background: linear-gradient(180deg, #efe6ad 0%, #e6b062 17%, #c4501c 33%, #5a1f0c 45%, #120c09 56%, #0c0a08 84%, #1c2f9c 91.5%, #f04d86 96%, #f7d6c6 98.2%, #fbf8f2 100%)">
<span class="grain" style="opacity: 0.4"></span>
<nav aria-label="Primary" style="position: absolute; left: 32px; right: 32px; top: 26px; display: flex; justify-content: space-between; gap: 24px; {MONO}; font-size: 13px; color: {C['tang']}">
<a class="cl" href="#contact" style="padding: 10px 0">kylegordonmusic@gmail.com</a>
<a class="cl" href="#contact" style="padding: 10px 0">Work with Kyle</a>
</nav>
<h1 style="position: absolute; left: 28px; right: 28px; bottom: 124px; margin: 0; font-family: 'Bagel Fat One', 'Arial Rounded MT Bold', sans-serif; font-weight: 400; font-size: clamp(64px, 10.6vw, 156px); line-height: 0.86; letter-spacing: -0.01em; color: {C['celery']}">Kyle Daniel<br>Gordon</h1>
<p style="position: absolute; right: 32px; bottom: 132px; margin: 0; max-width: 260px; {MONO}; font-size: 12px; line-height: 1.6; color: {C['celery']}; text-align: right">Arranger<br>Orchestrator<br>Conductor<br>Los Angeles</p>
</header>

<section style="padding: 130px 24px 120px; display: flex; flex-direction: column; align-items: center; gap: 56px; text-align: center">
<h2 style="margin: 0; max-width: 1100px; {COND}; font-size: clamp(44px, 6.6vw, 96px); line-height: 0.92; color: {C['peri']}; text-wrap: balance">Music for film, television and the concert stage.</h2>
<div style="width: 300px; max-width: 80%; aspect-ratio: 3 / 4; background: #d9d4c9; display: flex; align-items: center; justify-content: center; padding: 20px; box-sizing: border-box; {MONO}; font-size: 11px; color: #6b665e">[Photo: conducting the LSO]</div>
<p style="margin: 0; max-width: 520px; font-size: 15px; line-height: 1.6; text-align: justify; text-align-last: center; letter-spacing: 0.02em">Orchestrator, arranger and conductor. Lead orchestrator on Rosalía's LUX with the London Symphony Orchestra. Part of the orchestration teams behind Oppenheimer, Bridgerton and The Mandalorian.</p>
</section>

<section class="scatter split" style="padding: 40px 24px 40px; max-width: 1440px; margin: 0 auto; box-sizing: border-box; align-items: start">
<h2 style="grid-column: 2 / span 8; margin: 0; {COND}; font-size: clamp(48px, 7vw, 104px); line-height: 0.92; color: {C['mag']}">Orchestration.<br>Arranging.<br>Conducting.</h2>
<div style="grid-column: 11 / span 2; position: relative; aspect-ratio: 1 / 2.3; background: linear-gradient(180deg, #1e1226 0%, #3a2a56 34%, #2a3fe0 50%, #f2b56b 86%, #e2581a 100%); overflow: hidden"><span class="grain"></span></div>
</section>

<section id="work" aria-label="Selected work" class="scatter" style="padding: 120px 24px 80px; max-width: 1440px; margin: 0 auto; box-sizing: border-box; row-gap: 40px; align-items: start">
{tiles}</section>

<section class="scatter split" style="padding: 120px 24px 160px; max-width: 1440px; margin: 0 auto; box-sizing: border-box; align-items: end">
<div style="grid-column: 2 / span 5; position: relative; aspect-ratio: 16 / 7; background: linear-gradient(180deg, #2a1240 0%, #7b2f7a 30%, #e2581a 70%, #f6c06a 100%); overflow: hidden"><span class="grain"></span></div>
<p style="grid-column: 8 / span 3; margin: 0; {MONO}; font-size: 13px; line-height: 1.5; color: {C['sky']}; text-align: justify">Billboard Award, 2024: #1 Classical Album. Romani: The Untold Story, orchestrated and conducted with the London Symphony Orchestra and Dallas String Quartet.</p>
</section>

<footer id="contact" style="position: relative; overflow: hidden; background: linear-gradient(180deg, #2b2a31 0%, #8c99cc 20%, #b8c6f0 34%, #d6a98c 58%, #b8456e 82%, #5e1129 100%); color: #f7f2ea; padding: 150px 24px 40px">
<span class="grain" style="opacity: 0.38"></span>
<div style="position: relative; max-width: 900px; margin: 0 auto; display: flex; flex-direction: column; align-items: center; gap: 30px; text-align: center">
<h2 style="margin: 0; {COND}; font-size: clamp(40px, 5.6vw, 80px); line-height: 0.95; color: {C['celery']}; text-wrap: balance">Teams for John Williams, Ludwig Göransson & Justin Hurwitz.</h2>
<span style="{MONO}; font-size: 12px; color: #5b1a49">Orchestration · Arranging · Conducting</span>
<p style="margin: 0; max-width: 640px; font-size: 15px">{BIO}</p>
<p style="margin: 0; max-width: 640px; font-size: 15px">{BIO3}</p>
</div>
<div style="position: relative; margin-top: 150px; display: flex; flex-wrap: wrap; gap: 16px 32px; justify-content: space-between; align-items: baseline; {MONO}; font-size: 13px; color: {C['celery']}">
<a class="cl" href="mailto:kylegordonmusic@gmail.com" style="padding: 10px 0">kylegordonmusic@gmail.com</a>
<span style="{COND}; font-size: 22px; color: #f7f2ea">Written for the room.</span>
<span style="display: flex; gap: 28px"><a class="cl" href="https://www.instagram.com/kylegordonmusic/" style="padding: 10px 0">Instagram</a><a class="cl" href="https://www.imdb.com/name/nm8773349/" style="padding: 10px 0">IMDb</a></span>
</div>
</footer>
</div>'''
    return page('Direction A, Afterglow', body, css, C['paper'], h=4700)


# ------------------------------------------------------------------ B · END CREDITS
def build_b():
    css = '''.cr{position:relative;display:flex;flex-direction:column;align-items:center;gap:2px;padding:14px 0;text-decoration:none}
.cr .ttl{color:var(--c);transition:color .25s ease,letter-spacing .4s cubic-bezier(.2,.8,.2,1)}
.cr:hover .ttl{color:#fffaf0;letter-spacing:0.01em}
.cr .peek{position:absolute;right:0;top:50%;width:108px;opacity:0;transform:translateY(-50%) rotate(4deg) scale(.92);transition:opacity .3s ease,transform .45s cubic-bezier(.2,.8,.2,1);pointer-events:none}
.cr:nth-child(even) .peek{right:auto;left:0;transform:translateY(-50%) rotate(-4deg) scale(.92)}
.cr:hover .peek{opacity:1;transform:translateY(-50%) rotate(4deg) scale(1)}
.cr:nth-child(even):hover .peek{transform:translateY(-50%) rotate(-4deg) scale(1)}
.cl{text-decoration:underline;text-underline-offset:5px;text-decoration-thickness:1px}
@media (max-width: 760px){.cr .peek{display:none}}'''
    cols = [C['celery'], C['peri'], '#f08a4b', '#f06bb0', '#6fb6ff']

    def group(name, rows, ratio):
        h = (f'<div style="{MONO}; font-size: 12px; letter-spacing: 0.32em; color: #8f8678; padding: 70px 0 18px; text-align: center">— {name} —</div>\n'
             f'<div style="display: flex; flex-direction: column">\n')
        for i, r in enumerate(rows):
            t, role = r[0], r[1]
            g = G[(i * 3 + len(name)) % len(G)]
            h += (f'<a href="#credits" class="cr" style="--c: {cols[(i + len(name)) % 5]}">'
                  f'<span style="{MONO}; font-size: 11px; color: #8f8678">{role}</span>'
                  f'<span class="ttl" style="{COND}; font-size: clamp(34px, 4.6vw, 64px); line-height: 0.98; text-align: center">{t}</span>'
                  f'<span class="peek">{art(g, ratio)}</span></a>\n')
        return h + '</div>\n'

    credits = group('Film', FILM[:8], '2 / 3') + group('Television', TV, '2 / 3') + group('Records & stage', REC[:6], '1 / 1')
    aura = ('<div aria-hidden="true" style="position: absolute; inset: -10%; filter: blur(70px); background: '
            'radial-gradient(34% 40% at 28% 42%, rgba(226,88,26,0.85), rgba(226,88,26,0) 70%), '
            'radial-gradient(30% 38% at 72% 52%, rgba(58,63,214,0.8), rgba(58,63,214,0) 70%), '
            'radial-gradient(30% 30% at 52% 82%, rgba(240,77,134,0.7), rgba(240,77,134,0) 70%), '
            'radial-gradient(26% 30% at 60% 18%, rgba(223,232,176,0.45), rgba(223,232,176,0) 70%)"></div>')
    body = f'''<div style="position: relative; background: #0d0c0b; color: #efe9dc; font-family: 'DM Mono', ui-monospace, monospace; font-size: 15px; line-height: 1.6; overflow-x: clip">

<header style="position: relative; height: 820px; overflow: hidden">
{aura}
<span class="grain" style="opacity: 0.45"></span>
<nav aria-label="Primary" style="position: absolute; left: 32px; right: 32px; top: 26px; display: flex; flex-wrap: wrap; justify-content: space-between; gap: 16px; {MONO}; font-size: 13px">
<span style="padding: 10px 0">Kyle Daniel Gordon</span>
<span style="display: flex; gap: 28px"><a class="cl" href="#credits" style="padding: 10px 0">Credits</a><a class="cl" href="#about" style="padding: 10px 0">About</a><a class="cl" href="#contact" style="padding: 10px 0">Contact</a></span>
</nav>
<div style="position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 30px; padding: 0 24px; text-align: center">
<span style="{MONO}; font-size: 12px; letter-spacing: 0.32em; color: #e9dfc9">Music by the orchestra of</span>
<h1 style="margin: 0; {COND}; font-weight: 900; font-size: clamp(80px, 13.6vw, 210px); line-height: 0.8; color: #f6efdc">Kyle<br>Daniel<br>Gordon</h1>
<span style="{MONO}; font-size: 13px; letter-spacing: 0.2em">Orchestrator · Arranger · Conductor</span>
</div>
</header>

<section id="credits" aria-label="Credits" style="max-width: 980px; margin: 0 auto; padding: 60px 24px 40px; box-sizing: border-box">
{credits}
<div style="padding: 60px 0 0; text-align: center"><a class="cl" href="#credits" style="{MONO}; font-size: 13px; color: {C['celery']}; padding: 12px 0; display: inline-block">And 24 more credits</a></div>
</section>

<section id="about" style="max-width: 1100px; margin: 0 auto; padding: 150px 24px 80px; box-sizing: border-box; display: flex; flex-direction: column; align-items: center; gap: 28px; text-align: center">
<span style="{MONO}; font-size: 12px; letter-spacing: 0.32em; color: #8f8678">In the room with</span>
<p style="margin: 0; {COND}; font-size: clamp(30px, 3.6vw, 50px); line-height: 1.1; color: {C['peri']}; text-wrap: balance">John Williams · Ludwig Göransson · Kris Bowers · Walter Murphy · Justin Hurwitz</p>
<span style="{MONO}; font-size: 12px; letter-spacing: 0.32em; color: #8f8678; padding-top: 30px">Performed by</span>
<p style="margin: 0; max-width: 760px; {MONO}; font-size: 14px; line-height: 1.9">London Symphony Orchestra / BBC Concert Orchestra / San Francisco Symphony / Seattle Symphony / National Arts Centre Orchestra</p>
<p style="margin: 40px 0 0; max-width: 620px; font-size: 15px; color: #cfc6b6; text-transform: none">{BIO3}</p>
</section>

<footer id="contact" style="position: relative; overflow: hidden; padding: 140px 24px 40px">
{aura}
<span class="grain" style="opacity: 0.45"></span>
<div style="position: relative; display: flex; flex-direction: column; align-items: center; gap: 18px; text-align: center">
<span style="{MONO}; font-size: 12px; letter-spacing: 0.32em">For bookings and sessions</span>
<a href="mailto:kylegordonmusic@gmail.com" style="{COND}; font-weight: 900; font-size: clamp(36px, 7vw, 110px); line-height: 0.95; text-decoration: none; color: #f6efdc; overflow-wrap: anywhere">kylegordonmusic@gmail.com</a>
</div>
<div style="position: relative; margin-top: 130px; display: flex; flex-wrap: wrap; justify-content: space-between; gap: 16px; {MONO}; font-size: 12px">
<span>Los Angeles</span>
<span style="display: flex; gap: 28px"><a class="cl" href="https://www.instagram.com/kylegordonmusic/" style="padding: 10px 0">Instagram</a><a class="cl" href="https://www.imdb.com/name/nm8773349/" style="padding: 10px 0">IMDb</a></span>
</div>
</footer>
</div>'''
    return page('Direction B, End credits', body, css, '#0d0c0b', h=5200)


# ------------------------------------------------------------------ C · INDEX
def build_c():
    css = '''.row{position:relative;display:grid;grid-template-columns:64px minmax(0,1fr) 170px 260px;gap:16px;align-items:center;padding:14px 12px;border-top:1px solid #1d1b18;text-decoration:none;transition:background-color .2s ease}
.row:hover{background-color:var(--tint)}
.row .ttl{transition:transform .35s cubic-bezier(.2,.8,.2,1)}
.row:hover .ttl{transform:translateX(10px)}
.row .peek{position:absolute;right:300px;top:50%;width:96px;opacity:0;transform:translateY(-50%) rotate(-5deg) scale(.9);transition:opacity .25s ease,transform .4s cubic-bezier(.2,.8,.2,1);pointer-events:none;z-index:2}
.row:hover .peek{opacity:1;transform:translateY(-50%) rotate(-5deg) scale(1)}
.chip{transition:background-color .2s ease,color .2s ease}
.chip:hover{background-color:#1d1b18;color:#f2eddc}
.cl{text-decoration:underline;text-underline-offset:5px;text-decoration-thickness:1px}
@media (max-width: 860px){.row{grid-template-columns:44px minmax(0,1fr)}.row .hide{display:none}.row .peek{display:none}}'''
    rows = []
    for t, r in FILM[:5]:
        rows.append((t, 'Film', r))
    for t, r in TV[:4]:
        rows.append((t, 'Television', r))
    for t, r, w in REC[:4]:
        rows.append((t, 'Records', r))
    order = [0, 9, 5, 1, 10, 6, 2, 11, 7, 3, 12, 8, 4]
    tints = ['#e4e9c7', '#dde6ff', '#f6d8c3', '#f6cfe2', '#d3e7fb']
    dots = [C['olive'], C['peri'], C['tang'], C['mag'], C['sky']]
    html = ''
    for n, k in enumerate(order):
        t, cat, role = rows[k]
        ratio = '1 / 1' if cat == 'Records' else '2 / 3'
        html += (f'<a href="#index" class="row" style="--tint: {tints[n % 5]}">'
                 f'<span style="{MONO}; font-size: 13px; font-variant-numeric: tabular-nums">{n + 1:02d}</span>'
                 f'<span class="ttl" style="display: flex; align-items: center; gap: 14px; {COND}; font-size: clamp(28px, 3.2vw, 44px); line-height: 1">'
                 f'<span aria-hidden="true" style="flex: 0 0 auto; width: 12px; height: 12px; border-radius: 50%; background: {dots[n % 5]}"></span>{t}</span>'
                 f'<span class="hide" style="{MONO}; font-size: 12px">{cat}</span>'
                 f'<span class="hide" style="{MONO}; font-size: 12px">{role}</span>'
                 f'<span class="peek">{art(G[(n * 3) % len(G)], ratio)}</span></a>\n')
    seg = lambda g, label, n, flex: (f'<div style="position: relative; flex: {flex} 1 0; min-width: 0; background: {g}; overflow: hidden">'
                                     f'<span class="grain" style="opacity: 0.4"></span>'
                                     f'<span style="position: absolute; left: 14px; bottom: 12px; {MONO}; font-size: 12px; color: #fbf8f2">{label} — {n}</span></div>')
    body = f'''<div style="position: relative; background: {C['butter']}; color: #1d1b18; font-family: 'DM Mono', ui-monospace, monospace; font-size: 14px; line-height: 1.6; overflow-x: clip">
<span class="grainm"></span>

<header style="position: relative; max-width: 1440px; margin: 0 auto; padding: 26px 24px 0; box-sizing: border-box">
<nav aria-label="Primary" style="display: flex; flex-wrap: wrap; justify-content: space-between; gap: 16px; {MONO}; font-size: 13px">
<span style="padding: 10px 0">Los Angeles · Est. 2016</span>
<span style="display: flex; gap: 28px"><a class="cl" href="#index" style="padding: 10px 0">Index</a><a class="cl" href="#about" style="padding: 10px 0">About</a><a class="cl" href="#contact" style="padding: 10px 0">Contact</a></span>
</nav>
<h1 style="margin: 70px 0 0 -0.03em; {WIDE}; font-weight: 900; font-size: clamp(40px, 6.2vw, 90px); line-height: 0.9; letter-spacing: -0.03em">Kyle Daniel Gordon</h1>
<p style="margin: 18px 0 0; {MONO}; font-size: 13px">Orchestrator · Arranger · Conductor</p>
</header>

<div aria-label="43 projects: 9 records and stage, 13 film, 21 television" role="img" style="position: relative; margin-top: 56px; height: 170px; display: flex">
{seg('linear-gradient(180deg, #f0e3a4, #e07a2c 55%, #8a2a0e)', 'Records &amp; stage', 9, 9)}
{seg('linear-gradient(180deg, #1b1a3f, #3a3fd6 55%, #f2b56b)', 'Film', 13, 13)}
{seg('linear-gradient(180deg, #f6c1d8, #cf1f84 55%, #2b0a1f)', 'Television', 21, 21)}
</div>

<section id="index" style="position: relative; max-width: 1440px; margin: 0 auto; padding: 72px 24px 40px; box-sizing: border-box">
<div style="display: flex; flex-wrap: wrap; gap: 24px 56px; align-items: flex-end; justify-content: space-between; padding-bottom: 36px">
<p style="margin: 0; max-width: 480px; font-size: 14px; text-transform: none">Forty-three projects across film, television and the concert stage. Hover a title to see the cover; open one for the full credit.</p>
<div role="group" aria-label="Filter" style="display: flex; flex-wrap: wrap; gap: 8px">
<button type="button" class="chip" aria-pressed="true" style="min-height: 40px; padding: 0 16px; border: 1px solid #1d1b18; border-radius: 999px; background-color: #1d1b18; color: #f2eddc; {MONO}; font-size: 12px; cursor: pointer">All 43</button>
<button type="button" class="chip" aria-pressed="false" style="min-height: 40px; padding: 0 16px; border: 1px solid #1d1b18; border-radius: 999px; background-color: transparent; color: #1d1b18; {MONO}; font-size: 12px; cursor: pointer">Film 13</button>
<button type="button" class="chip" aria-pressed="false" style="min-height: 40px; padding: 0 16px; border: 1px solid #1d1b18; border-radius: 999px; background-color: transparent; color: #1d1b18; {MONO}; font-size: 12px; cursor: pointer">Television 21</button>
<button type="button" class="chip" aria-pressed="false" style="min-height: 40px; padding: 0 16px; border: 1px solid #1d1b18; border-radius: 999px; background-color: transparent; color: #1d1b18; {MONO}; font-size: 12px; cursor: pointer">Records 9</button>
</div>
</div>
<div style="display: grid; grid-template-columns: 64px minmax(0, 1fr) 170px 260px; gap: 16px; padding: 0 12px 10px; {MONO}; font-size: 11px; color: #6b665e" aria-hidden="true"><span>No.</span><span>Title</span><span>Category</span><span>Role</span></div>
{html}<div style="border-top: 1px solid #1d1b18; padding: 18px 12px; {MONO}; font-size: 12px"><a class="cl" href="#index" style="padding: 10px 0">Show all 43</a></div>
</section>

<section id="about" style="position: relative; max-width: 1440px; margin: 0 auto; padding: 120px 24px 40px; box-sizing: border-box; display: grid; grid-template-columns: repeat(auto-fit, minmax(min(380px, 100%), 1fr)); gap: 48px 72px; align-items: start">
<div style="position: relative; aspect-ratio: 4 / 5; background: linear-gradient(180deg, #2b2a31 0%, #8c99cc 30%, #d6a98c 70%, #b8456e 100%); overflow: hidden; display: flex; align-items: flex-end; padding: 18px; box-sizing: border-box"><span class="grain" style="opacity: 0.4"></span><span style="position: relative; {MONO}; font-size: 11px; color: #fbf8f2">[Photo: conducting the LSO]</span></div>
<div style="display: flex; flex-direction: column; gap: 22px">
<h2 style="margin: 0; {COND}; font-size: clamp(44px, 5.6vw, 80px); line-height: 0.92">Lead orchestrator, LUX. Billboard #1, Romani.</h2>
<p style="margin: 0; font-size: 14px; text-transform: none; max-width: 60ch">{BIO}</p>
<p style="margin: 0; font-size: 14px; text-transform: none; max-width: 60ch">{BIO2}</p>
<p style="margin: 0; font-size: 14px; text-transform: none; max-width: 60ch">{BIO3}</p>
</div>
</section>

<footer id="contact" style="position: relative; max-width: 1440px; margin: 0 auto; padding: 140px 24px 40px; box-sizing: border-box">
<a href="mailto:kylegordonmusic@gmail.com" style="display: block; {WIDE}; font-weight: 900; font-size: clamp(26px, 4.6vw, 66px); line-height: 1; letter-spacing: -0.03em; text-decoration: none; overflow-wrap: anywhere; border-top: 1px solid #1d1b18; padding-top: 28px">kylegordonmusic@gmail.com</a>
<div style="margin-top: 60px; display: flex; flex-wrap: wrap; justify-content: space-between; gap: 16px; {MONO}; font-size: 12px">
<span style="display: flex; gap: 28px"><a class="cl" href="https://www.instagram.com/kylegordonmusic/" style="padding: 10px 0">Instagram</a><a class="cl" href="https://www.imdb.com/name/nm8773349/" style="padding: 10px 0">IMDb</a></span>
</div>
</footer>
</div>'''
    return page('Direction C, Index', body, css, C['butter'], h=3700)


# ------------------------------------------------------------------ D · SCORE IN COLOUR
def build_d():
    css = '''.note{position:absolute;top:0;width:64px;height:280px;text-decoration:none;color:#fbf8f2}
.note .lab{position:absolute;left:36px;top:100px;line-height:30px;white-space:nowrap;transform-origin:0 100%;transform:rotate(-38deg);transition:color .2s ease,transform .3s cubic-bezier(.2,.8,.2,1)}
.note:hover .lab{color:#dfe8b0;transform:rotate(-38deg) translateX(6px)}
.note .head{position:absolute;left:21px;width:22px;height:15px;box-sizing:border-box;border-radius:50%;transform:rotate(-22deg);transition:transform .3s cubic-bezier(.2,.8,.2,1),background-color .2s ease,border-color .2s ease}
.note .full{background:#fbf8f2}
.note .open{border:3px solid #fbf8f2;border-top-width:2px;border-bottom-width:2px}
.note:hover .head{transform:rotate(-22deg) scale(1.3)}
.note:hover .full{background:#dfe8b0}
.note:hover .open{border-color:#dfe8b0}
.note .stem{position:absolute;width:2px;height:50px;background:currentColor}
.cl{text-decoration:underline;text-underline-offset:5px;text-decoration-thickness:1px}
.sc{scrollbar-width:thin;scrollbar-color:rgba(255,255,255,.4) transparent}'''
    staves = [
        ('A', 'Records & stage', [(t, True) for t, r, w in REC]),
        ('B', 'Film', [(t, i == 0) for i, (t, r) in enumerate(FILM)]),
        ('C', 'Television', [(t, False) for t, r in TV]),
    ]
    contours = [[6, 4, 5, 2, 3, 5, 7, 4, 2, 3], [3, 5, 4, 6, 7, 5, 2, 3, 1, 4], [5, 7, 6, 4, 2, 3, 5, 6, 4, 1]]
    short = {'Black Panther: Wakanda Forever': 'Wakanda Forever', 'Star Wars: The Last Jedi': 'The Last Jedi',
             'Star Trek: Strange New Worlds': 'Strange New Worlds', 'Romani: The Untold Story': 'Romani',
             'Baby Shark 10th Anniversary': 'Baby Shark 10th', 'This Light Has No Darkness': 'This Light Has No Darkness'}
    X0, DX, TOP = 44, 92, 160
    html = ''
    for si, (mark, name, notes) in enumerate(staves):
        w = X0 + (len(notes) - 1) * DX + 280
        ns = ''
        for i, (t, lead) in enumerate(notes):
            pos = contours[si][i % 10]
            cy = TOP + pos * 8
            up = pos >= 4
            ns += (f'<a href="#now" class="note" aria-label="{t}" style="left: {X0 + i * DX}px">'
                   f'<span class="lab" style="{COND}; font-size: 22px">{short.get(t, t)}</span>'
                   f'<span class="stem" aria-hidden="true" style="left: {41 if up else 21}px; top: {cy - 50 if up else cy}px"></span>'
                   f'<span class="head {"open" if lead else "full"}" aria-hidden="true" style="top: {cy - 7.5}px"></span></a>\n')
        bars = ''.join(f'<span aria-hidden="true" style="position: absolute; left: {X0 + k * DX - 10}px; top: {TOP}px; width: 1.5px; height: 65.5px; background: rgba(251,248,242,0.85)"></span>'
                       for k in range(4, len(notes), 4))
        html += f'''<section aria-label="{name}" style="display: flex; flex-wrap: wrap; align-items: flex-start">
<div style="flex: 0 0 160px; box-sizing: border-box; padding: 160px 12px 0 20px; display: flex; flex-direction: column; align-items: flex-start; gap: 8px">
<span aria-hidden="true" style="width: 28px; height: 28px; box-sizing: border-box; border: 1.5px solid #fbf8f2; display: flex; align-items: center; justify-content: center; {MONO}; font-size: 13px">{mark}</span>
<h2 style="margin: 0; {COND}; font-size: 26px; line-height: 1">{name}</h2>
<span style="{MONO}; font-size: 11px; opacity: 0.8">{len(notes)} shown</span>
</div>
<div class="sc" style="flex: 1 1 300px; min-width: 0; overflow-x: auto; overflow-y: hidden">
<div style="position: relative; height: 270px; width: {w}px; min-width: 100%">
<span aria-hidden="true" style="position: absolute; left: 0; right: 0; top: {TOP}px; height: 66px; background: repeating-linear-gradient(180deg, rgba(251,248,242,0.85) 0px, rgba(251,248,242,0.85) 1.5px, rgba(0,0,0,0) 1.5px, rgba(0,0,0,0) 16px)"></span>
{bars}
{ns}</div>
</div>
</section>
'''
    body = f'''<div style="position: relative; background: linear-gradient(180deg, #17163a 0%, #2f3488 16%, #8d9ee6 34%, #c9c4e6 44%, #f2c3a0 58%, #e46c7c 76%, #8e2148 90%, #3e0c1f 100%); color: #fbf8f2; font-family: 'DM Mono', ui-monospace, monospace; font-size: 15px; line-height: 1.6; overflow-x: clip">
<span class="grain" style="opacity: 0.42; z-index: 5"></span>

<header style="position: relative; max-width: 1440px; margin: 0 auto; padding: 26px 24px 0; box-sizing: border-box">
<nav aria-label="Primary" style="display: flex; flex-wrap: wrap; justify-content: space-between; gap: 16px; {MONO}; font-size: 13px">
<span style="padding: 10px 0">Los Angeles</span>
<span style="display: flex; gap: 28px"><a class="cl" href="#score" style="padding: 10px 0">Score</a><a class="cl" href="#about" style="padding: 10px 0">About</a><a class="cl" href="#contact" style="padding: 10px 0">Contact</a></span>
</nav>
<div style="padding: 70px 0 60px; display: flex; flex-wrap: wrap; gap: 28px 72px; align-items: flex-end; justify-content: space-between">
<h1 style="margin: 0 0 0 -0.04em; font-family: 'Instrument Sans', system-ui, sans-serif; font-weight: 600; font-size: clamp(60px, 9.4vw, 136px); line-height: 0.88; letter-spacing: -0.05em">Kyle Daniel<br>Gordon</h1>
<div style="flex: 0 1 360px; display: flex; flex-direction: column; gap: 16px; margin-bottom: 8px">
<span style="{MONO}; font-size: 13px; color: {C['celery']}">Arr. · Orch. · Cond.</span>
<p style="margin: 0; font-family: 'Instrument Sans', system-ui, sans-serif; font-size: 19px; line-height: 1.4">Forty-three projects for film, television and the concert stage, written out as a score.</p>
</div>
</div>
</header>

<div id="score" style="position: relative; max-width: 1440px; margin: 0 auto; padding: 0 24px; box-sizing: border-box">
<div style="border-left: 4px solid #fbf8f2; padding-left: 6px"><div style="border-left: 1.5px solid #fbf8f2; display: flex; flex-direction: column; gap: 10px">
{html}</div></div>

<div id="now" style="position: relative; margin-top: 48px; display: flex; flex-wrap: wrap; gap: 24px 48px; align-items: center; padding: 22px 26px; background: rgba(23,22,58,0.32); border: 1px solid rgba(251,248,242,0.35); backdrop-filter: blur(14px); -webkit-backdrop-filter: blur(14px)">
<div style="flex: 0 0 auto; position: relative; width: 74px; aspect-ratio: 2 / 3; background: {G[6]}; overflow: hidden"><span class="grain"></span></div>
<div style="flex: 1 1 280px; display: flex; flex-direction: column; gap: 2px">
<span style="{MONO}; font-size: 11px; color: {C['celery']}">Film · Selected</span>
<span style="font-family: 'Instrument Sans', system-ui, sans-serif; font-weight: 600; font-size: 34px; line-height: 1.05; letter-spacing: -0.04em">Oppenheimer</span>
</div>
<span style="flex: 1 1 220px; {MONO}; font-size: 13px">Orchestrator</span>
<div style="display: flex; gap: 10px"><button type="button" style="min-height: 44px; padding: 0 18px; border: 1px solid #fbf8f2; border-radius: 999px; background: transparent; color: #fbf8f2; {MONO}; font-size: 12px; cursor: pointer">Previous</button><button type="button" style="min-height: 44px; padding: 0 18px; border: 1px solid #fbf8f2; border-radius: 999px; background: #fbf8f2; color: #2a1340; {MONO}; font-size: 12px; cursor: pointer">Next</button></div>
</div>
</div>

<section id="about" style="position: relative; max-width: 1440px; margin: 0 auto; padding: 150px 24px 0; box-sizing: border-box; display: grid; grid-template-columns: repeat(auto-fit, minmax(min(380px, 100%), 1fr)); gap: 40px 80px; align-items: start">
<h2 style="margin: 0 0 0 -0.04em; font-family: 'Instrument Sans', system-ui, sans-serif; font-weight: 600; font-size: clamp(48px, 6.4vw, 92px); line-height: 0.9; letter-spacing: -0.05em">About</h2>
<div style="display: flex; flex-direction: column; gap: 18px; font-family: 'Instrument Sans', system-ui, sans-serif; font-size: 18px; line-height: 1.5; max-width: 62ch">
<p style="margin: 0">{BIO}</p>
<p style="margin: 0">{BIO2}</p>
</div>
</section>

<footer id="contact" style="position: relative; max-width: 1440px; margin: 0 auto; padding: 150px 24px 40px; box-sizing: border-box">
<span aria-hidden="true" style="display: block; height: 66px; background: repeating-linear-gradient(180deg, rgba(251,248,242,0.85) 0px, rgba(251,248,242,0.85) 1.5px, rgba(0,0,0,0) 1.5px, rgba(0,0,0,0) 16px); border-right: 5px solid #fbf8f2"></span>
<div style="padding-top: 36px; display: flex; flex-wrap: wrap; gap: 24px 72px; align-items: flex-end; justify-content: space-between">
<div style="display: flex; flex-direction: column; gap: 6px">
<span style="{MONO}; font-size: 12px; color: {C['celery']}">Write to me</span>
<a href="mailto:kylegordonmusic@gmail.com" style="font-family: 'Instrument Sans', system-ui, sans-serif; font-weight: 600; font-size: clamp(28px, 5vw, 72px); line-height: 0.95; letter-spacing: -0.045em; text-decoration: none; overflow-wrap: anywhere">kylegordonmusic@gmail.com</a>
</div>
<span style="display: flex; gap: 28px; {MONO}; font-size: 12px"><a class="cl" href="https://www.instagram.com/kylegordonmusic/" style="padding: 10px 0">Instagram</a><a class="cl" href="https://www.imdb.com/name/nm8773349/" style="padding: 10px 0">IMDb</a></span>
</div>
</footer>
</div>'''
    return page('Direction D, Score in colour', body, css, '#17163a', h=2900)


if __name__ == '__main__':
    for fn, fnc in [('MuckA.dc.html', build_a), ('MuckB.dc.html', build_b), ('MuckC.dc.html', build_c), ('MuckD.dc.html', build_d)]:
        open(os.path.join(OUT, fn), 'w', encoding='utf-8').write(fnc())
    print('written')
