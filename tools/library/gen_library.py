"""Hidden holiday rental catalog: /holiday-library/ (noindex, not in sitemap or nav).
python3 gen_library.py preview out.html   -> single file, fonts + images inlined (for review)
python3 gen_library.py site <site_dir>      -> writes <site_dir>/holiday-library/index.html + images
"""
import sys, os, re, base64, html, shutil, urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = '/tmp/site_new/fonts'
EMAIL = 'KyleDanielGordonLibrary@gmail.com'

FEES = [  # (tier, first performance, each additional in the same run)
    ('Major orchestras', 500, 150),
    ('Regional professional orchestras', 350, 100),
    ('Community, youth and school orchestras', 200, 75),
]

SETS = [
  ('Pops with rhythm section', 'Full orchestra with piano, electric bass, drum set and harp. Built for holiday pops programs.', [
    dict(slug='feliz-navidad', title='Feliz Navidad', by='José Feliciano', dur='c. 2:15', vox='Vocalist',
         inst='2. 2. 2. 2 + alto sax — 4. 3. 2 + bass tbn. 1 — perc — piano, electric bass, drum set, harp — strings',
         note='New York Philharmonic, Sounds of the Season 2026'),
    dict(slug='fairytale-of-new-york', title='Fairytale of New York', by='The Pogues (MacGowan / Finer)', dur='c. 3:55', vox='Instrumental',
         inst='2 (2nd dbl. picc). 2. 2. 2 + alto sax — 4. 3. 2 + bass tbn. 1 — timp, perc, drum set — piano, electric bass, harp — strings',
         note='New York Philharmonic, Sounds of the Season 2026'),
    dict(slug='i-saw-three-ships', title='I Saw Three Ships', by='Traditional', dur='c. 2:15', vox='Vocalist',
         inst='2. 2. 2. 2 + alto sax — 4. 3. 2 + bass tbn. 1 — timp, perc, drum set — piano, electric bass, harp — strings',
         note='New York Philharmonic, Sounds of the Season 2026'),
    dict(slug='this-christmas', title='This Christmas', by='Donny Hathaway / Nadine McKinnor', dur='c. 4:10', vox='Lead vocal + choir',
         inst='2. 2. 2. 2 (+ opt. alto sax) — 4. 3. 3. 1 — timp — drum set, piano, electric bass, harp — strings',
         note='BBC Concert Orchestra, 2025 · New York Philharmonic, 2026'),
    dict(slug='do-re-mi', title='Do-Re-Mi', by='Richard Rodgers / Oscar Hammerstein II', dur='c. 2:10', vox='Vocalist',
         inst='3. 1. 1 + bass cl. 1 — 1. 2. 1. 0 — timp, perc, drum set — harp, piano — strings',
         note='San Francisco Symphony, Deck the Hall 2026'),
    dict(slug='hark-sfs', title='Hark! The Herald Angels Sing', by='Mendelssohn / Wesley', dur='c. 4–5 min', vox='Choir',
         inst='2 + picc. 2 + E.H. 2 + bass cl. 2 + cbsn — 4. 3. 2 + bass tbn. 1 — timp, perc — organ, harp — strings',
         note='San Francisco Symphony, Holly Jolly Pops 2026'),
  ]),
  ('Gospel Christmas', 'Gospel carols for orchestra, choir and rhythm section, arranged with The Spirituals. Rent one, or all three as a set.', [
    dict(slug='hark-gospel', title='Hark! The Herald Angels Sing', by='Traditional', dur='c. 3:45', vox='Choir',
         inst='2. 2. 2. 2 — 4. 3. 2 + bass tbn. 1 — timp, 2 perc — piano, electric bass, drum set, harp — strings', note='BBC Concert Orchestra, Gospel Christmas 2025', arr='The Spirituals & Kyle Daniel Gordon'),
    dict(slug='o-come-all-ye-faithful', title='O Come All Ye Faithful', by='Traditional', dur='c. 6:00', vox='Choir',
         inst='2. 2. 2. 2 — 4. 3. 2 + bass tbn. 1 — timp, 2 perc — piano, electric bass, drum set, harp — strings', note='BBC Concert Orchestra, Gospel Christmas 2025', arr='The Spirituals & Kyle Daniel Gordon'),
    dict(slug='joy-to-the-world', title='Joy to the World', by='Traditional', dur='c. 4:05', vox='Choir',
         inst='2. 2. 2. 2 — 4. 3. 2 + bass tbn. 1 — timp, 2 perc — piano, electric bass, drum set, harp — strings', note='BBC Concert Orchestra, Gospel Christmas 2025', arr='The Spirituals & Kyle Daniel Gordon'),
  ]),
]

def b64(path, mime):
    return f'data:{mime};base64,' + base64.b64encode(open(path, 'rb').read()).decode()

def mailto(subject):
    return 'mailto:' + EMAIL + '?subject=' + urllib.parse.quote(subject)

GRAD = '#0b1712 0%, #1d4a35 24%, #b8702f 50%, #f2dcc0 76%'
SITE = 'https://www.kyledanielgordon.com'

def shell(src_page):
    """Pull the site's real styles, nav, footer and analytics from a built page so this page matches the site."""
    t = open(src_page).read()
    head = t[:t.index('</head>')]
    styles = ''.join(re.findall(r'<style>.*?</style>', head, re.S))
    preloads = ''.join(re.findall(r'<link as="(?:font|image)"[^>]*>', head))
    nav = re.search(r'<nav aria-label="Primary".*?</nav>', t, re.S).group(0)
    nav = nav.replace(' aria-current="page"', '')
    nav = re.sub(r'(font-size: 12px; color: )#[0-9a-fA-F]{3,6}', r'\g<1>#f6eedd', nav, count=1)
    foot = t[t.index('<footer'):t.index('</footer>') + 9]
    foot = re.sub(r'linear-gradient\(180deg, #f7f4ec 0%, [^)]*\)', 'linear-gradient(180deg, #f7f4ec 0%, #b8702f 30%, #1d4a35 62%, #0b1712 100%)', foot, count=1)
    tail = t[t.index("<script>addEventListener('load',function(){var s=document.createElement('script')"):t.index('</body>')]
    # Clarity: tag visits that came through a personal /r/ link (#c=code) so sessions can be matched to the email that was sent
    tail = tail.replace("if(location.pathname.indexOf('/for/')===0)",
        "var m=/[#&]c=([a-z0-9]{3})/.exec(location.hash);if(m){clarity('set','lib',m[1]);try{history.replaceState(null,'',location.pathname)}catch(e){}}\nif(location.pathname.indexOf('/for/')===0)")
    return styles, preloads, nav, foot, tail

def band(h=300):
    fade = 'linear-gradient(180deg, #000 0%, #000 42%, rgba(0,0,0,.55) 70%, rgba(0,0,0,.18) 86%, transparent 100%)'
    return (f'<div aria-hidden="true" style="position: absolute; left: 0; right: 0; top: 0; height: {h + 160}px; '
            f'background: linear-gradient(180deg, {GRAD}); overflow: hidden; -webkit-mask-image: {fade}; mask-image: {fade}">'
            f'<span class="grain" style="opacity: 0.38"></span></div>')

def build(mode, src_page):
    E = html.escape
    styles, preloads, nav, foot, tail = shell(src_page)
    def img(slug):
        p = os.path.join(HERE, 'img', slug + '.webp')
        return b64(p, 'image/webp') if mode == 'preview' else f'/holiday-library/img/{slug}.webp'

    cards = []
    n = 0
    for sname, sdesc, items in SETS:
        rows = []
        for c in items:
            n += 1
            rows.append(f"""
<article class="chart">
  <button class="thumb" data-full="{img(c['slug'])}" aria-label="Score sample: {E(c['title'])}">
    <img src="{img(c['slug'])}" alt="First score page of {E(c['title'])}, watermarked" loading="lazy" width="1100" height="1700">
    <span class="zoom"><span class="zl">Score sample ↗</span><span class="zs">Score ↗</span></span>
  </button>
  <div class="head">
    <div class="num">{n:02d}</div>
    <h3>{E(c['title'])}</h3>
    <p class="by">{E(c['by'])} · arr. {E(c.get('arr','Kyle Daniel Gordon'))}</p>
  </div>
  <div class="body">
    <dl>
      <div><dt>Duration</dt><dd>{E(c['dur'])}</dd></div>
      <div><dt>Voices</dt><dd>{E(c['vox'])}</dd></div>
      <div class="wide"><dt>Instrumentation</dt><dd>{E(c['inst'])}</dd></div>
    </dl>
    <a class="btn solid" href="{mailto('Perusal request: ' + c['title'])}">Request perusal score</a>
  </div>
</article>""")
        cards.append(f"""
<section class="set">
  <header class="sethead"><h2>{E(sname)}</h2><p>{E(sdesc)}</p></header>
  {''.join(rows)}
</section>""")
    fees = ''.join(f'<tr><th>{E(t)}</th><td data-l="First performance">${a}</td><td data-l="Each additional">${b}</td></tr>' for t, a, b in FEES)

    css = """
.lib{max-width:1392px;margin:0 auto;padding:0 24px;box-sizing:border-box}
.lib *{box-sizing:border-box}
.lib .lede{max-width:46ch;font-size:20px;line-height:1.45;margin:0}
.lib .orch{display:grid;grid-template-columns:repeat(4,1fr);border-top:1px solid #1b1a1726;margin-top:12px}
.lib .orch div{padding:16px 16px 0 0;font-family:'Archivo','Arial Narrow',sans-serif;font-stretch:62%;font-weight:800;text-transform:uppercase;font-size:28px;line-height:1}
.lib .set{padding:72px 0 8px}
.lib .sethead{display:flex;justify-content:space-between;align-items:baseline;gap:24px;border-bottom:2px solid #1b1a17;padding-bottom:12px;margin-bottom:8px}
.lib .sethead h2{font-family:'Archivo','Arial Narrow',sans-serif;font-stretch:62%;font-weight:800;text-transform:uppercase;font-size:44px;line-height:1;margin:0}
.lib .sethead p{color:#625d55;margin:0;max-width:520px;text-align:right;font-size:15px}
.lib .chart{display:grid;grid-template-columns:220px 1fr;grid-template-areas:'thumb head' 'thumb body';grid-template-rows:auto 1fr;gap:0 36px;padding:32px 0;border-bottom:1px solid #1b1a1726}
.lib .chart .thumb{grid-area:thumb;align-self:start}.lib .chart .head{grid-area:head}.lib .chart .body{grid-area:body}
.lib .zs{display:none}
.lib .thumb{position:relative;padding:0;border:1px solid #1b1a1726;background:#fff;cursor:zoom-in;display:block;width:100%;aspect-ratio:11/17;overflow:hidden;box-shadow:0 12px 28px -18px #1b1a1766;transition:transform .2s}
.lib .thumb:hover{transform:translateY(-3px)}
.lib .thumb img{width:100%;height:100%;object-fit:cover;object-position:top;display:block}
.lib .zoom{position:absolute;left:0;right:0;bottom:0;background:#1b1a17;color:#f7f4ec;font:500 11px/1 'DM Mono',monospace;letter-spacing:.06em;text-transform:uppercase;padding:9px}
.lib .num{font-family:'DM Mono',monospace;font-size:12px;color:#e2581a}
.lib h3{font-family:'Archivo','Arial Narrow',sans-serif;font-stretch:62%;font-weight:800;text-transform:uppercase;font-size:clamp(36px,4.4vw,56px);line-height:.95;margin:6px 0}
.lib .by{font-family:'Instrument Serif',Georgia,serif;font-style:italic;font-size:21px;color:#625d55;margin:0 0 18px}
.lib dl{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px 28px;margin:0 0 22px}
.lib dl .wide{grid-column:1/-1}
.lib dt{font-family:'DM Mono',monospace;font-size:11px;letter-spacing:.06em;text-transform:uppercase;color:#625d55;margin-bottom:2px}
.lib dd{margin:0;font-size:16px}
.lib .fees{margin:88px 0 0;padding:48px;background:#1b1a17;color:#f7f4ec;display:grid;grid-template-columns:1fr 1.25fr;gap:48px;position:relative;overflow:hidden}
.lib .fees h2{font-family:'Archivo','Arial Narrow',sans-serif;font-stretch:62%;font-weight:800;text-transform:uppercase;font-size:56px;line-height:.92;margin:10px 0 16px}
.lib .fees p{color:#d9d3c7;font-size:15px;margin:0 0 10px}
.lib table{width:100%;border-collapse:collapse}
.lib th,.lib td{text-align:left;padding:14px 0;border-bottom:1px solid #f7f4ec2e;font-size:16px;vertical-align:top}
.lib td{text-align:right;font-family:'DM Mono',monospace;font-size:18px;white-space:nowrap;padding-left:16px}
.lib thead th{font:500 11px 'DM Mono',monospace;letter-spacing:.06em;text-transform:uppercase;color:#bdb6a8}
.lib thead th:not(:first-child){text-align:right}
.lib .terms{list-style:none;padding:0;margin:18px 0 0;color:#d9d3c7;font-size:14px}
.lib .terms li{padding:4px 0 4px 16px;position:relative}
.lib .terms li:before{content:'—';position:absolute;left:0;color:#e2581a}
.lib .cta{padding:96px 0 0;text-align:center}
.lib .cta h2{font-family:'Archivo','Arial Narrow',sans-serif;font-stretch:62%;font-weight:800;text-transform:uppercase;font-size:clamp(48px,7vw,96px);line-height:.9;margin:12px 0 22px}
.lib .cta p{color:#625d55;margin:0 0 26px}
.lib .cta .btns{display:flex;gap:10px;justify-content:center;flex-wrap:wrap}
.mono{font-family:'DM Mono',ui-monospace,monospace;text-transform:uppercase;letter-spacing:.04em;font-size:12px}
.lib .comm{position:relative;overflow:hidden;margin:88px 0 0;padding:56px 48px;color:#fbf8f2;background:linear-gradient(120deg,#0b1712 0%,#1d4a35 45%,#b8702f 100%);display:grid;grid-template-columns:1fr 1fr;gap:40px 64px;align-items:end}
.lib .comm-in{position:relative}
.lib .comm h2{font-family:'Archivo','Arial Narrow',sans-serif;font-stretch:62%;font-weight:800;text-transform:uppercase;font-size:clamp(44px,5.6vw,80px);line-height:.9;margin:12px 0 0}
.lib .comm h2 em{font-family:'Instrument Serif',Georgia,serif;font-style:italic;font-weight:400;text-transform:none;font-stretch:100%;color:#f2dcc0;letter-spacing:-.02em}
.lib .comm p{font-size:18px;line-height:1.5;margin:0 0 22px;max-width:44ch;color:#f6eedd}
.lib .comm .btn.line:hover{background:#fbf8f2;color:#1b1a17;border-color:#fbf8f2}
#lb{position:fixed;inset:0;background:#1b1a17e6;display:none;align-items:flex-start;justify-content:center;overflow:auto;padding:4vh 16px;z-index:99;cursor:zoom-out}
#lb.on{display:flex}
#lb img{max-width:min(900px,100%);height:auto;background:#fff;box-shadow:0 20px 60px #0008}
#lb .x{position:fixed;top:14px;right:18px;color:#f7f4ec;font:500 12px 'DM Mono',monospace;letter-spacing:.06em;text-transform:uppercase}
@media (max-width:760px){
 .lib.hero{padding-top:120px !important}
 .lib h1 em{font-size:.8em}
 .lib .lede{font-size:18px}
 .lib .orch{grid-template-columns:1fr 1fr}.lib .orch div{font-size:22px}
 .lib .set{padding-top:56px}
 .lib .sethead{display:block}.lib .sethead h2{font-size:38px}.lib .sethead p{text-align:left;margin-top:8px}
 .lib .chart{grid-template-columns:92px 1fr;grid-template-areas:'thumb head' 'body body';grid-template-rows:auto auto;gap:18px 16px;padding:28px 0}
 .lib .chart .head{align-self:center}
 .lib h3{font-size:32px;margin:4px 0}
 .lib .by{font-size:17px;margin:0;line-height:1.3}
 .lib .zoom{font-size:9px;padding:7px 4px;letter-spacing:.04em}.lib .zl{display:none}.lib .zs{display:inline}
 .lib dl{grid-template-columns:1fr 1fr;gap:12px 16px;margin:0 0 18px}
 .lib .chart .btn{width:100%;justify-content:center}
 .lib .comm{grid-template-columns:1fr;padding:36px 22px;gap:20px}
 .lib .fees{grid-template-columns:1fr;padding:30px 22px;gap:20px}.lib .fees h2{font-size:44px}
 .lib table thead{display:none}
 .lib table tr{display:grid;grid-template-columns:1fr 1fr;gap:4px 16px;padding:16px 0;border-bottom:1px solid #f7f4ec2e}
 .lib table th{grid-column:1/-1;border:0;padding:0 0 4px;font-size:17px}
 .lib table td{border:0;padding:0;text-align:left;font-size:22px}
 .lib table td:before{content:attr(data-l);display:block;font:500 10px 'DM Mono',monospace;letter-spacing:.06em;text-transform:uppercase;color:#bdb6a8;margin-bottom:2px}
 .lib .cta{padding-top:72px}
 .lib .cta .btns .btn{width:100%;justify-content:center;max-width:340px}
}"""

    body = f"""<div style="position: relative; background: #f7f4ec; color: #1b1a17; font-family: 'Instrument Sans', system-ui, sans-serif; font-size: 16px; line-height: 1.55; overflow-x: clip">
<span class="grainm"></span>
<header style="position: relative">
{band(300)}
{nav}
<div class="lib hero" style="position: relative; padding-top: 230px">
  <div class="rise" style="display: flex; flex-direction: column; gap: 24px">
    <span class="mono" style="color: #1d4a35">KG Music Library · Holiday rentals</span>
    <h1 style="margin: 0; font-family: 'Archivo', 'Arial Narrow', sans-serif; font-stretch: 62%; font-weight: 800; text-transform: uppercase; font-size: clamp(76px, 12vw, 190px); line-height: 0.84; color: #1d4a35">Holiday<br><em style="font-family: 'Instrument Serif', Georgia, serif; font-style: italic; font-weight: 400; text-transform: none; font-stretch: 100%; color: #e2581a; letter-spacing: -0.02em">arrangements</em><br>for orchestra</h1>
    <p class="lede">Nine holiday charts by Kyle Daniel Gordon, orchestrator on Rosalía’s <i>LUX</i>, recorded with the London Symphony Orchestra, which won Album of the Year at the Latin Grammys and is nominated for Album of the Year at the Grammys. Engraved and ready for the stands, for pops orchestra, choir and rhythm section.</p>
    <div style="display: flex; flex-wrap: wrap; gap: 10px"><a class="btn solid" href="#charts">See the charts</a><a class="btn line" href="#fees">Rental fees</a></div>
  </div>
  <div class="mono" style="margin-top: 64px; color: #625d55">Kyle writes for</div>
  <div class="orch"><div>London Symphony Orchestra</div><div>New York Philharmonic</div><div>San Francisco Symphony</div><div>BBC Concert Orchestra</div></div>
</div>
</header>
<main class="lib" id="charts">
{''.join(cards)}
  <section class="fees" id="fees">
    <div>
      <div class="mono" style="color:#e2581a">Rental fees</div>
      <h2>Per chart, per run</h2>
      <p>One fee covers all performances of a chart within a single run of up to six weeks. Score and parts are delivered as PDFs, or printed and shipped, with shipping billed at cost.</p>
      <ul class="terms">
        <li>Custom instrumentation or a new key for your soloist: quoted per chart</li>
        <li>Rush delivery (within 3 weeks of first rehearsal): +$100</li>
        <li>Performance licensing for the underlying songs is handled through your usual ASCAP/BMI licenses</li>
        <li>Recording, broadcast and streaming by arrangement</li>
      </ul>
    </div>
    <table>
      <thead><tr><th>Orchestra</th><th>First performance</th><th>Each additional</th></tr></thead>
      <tbody>{fees}</tbody>
    </table>
  </section>
  <section class="comm" aria-labelledby="comm-h">
    <span aria-hidden="true" class="grain" style="opacity: 0.34"></span>
    <div class="comm-in">
      <div class="mono" style="color:#f2dcc0">Commissions</div>
      <h2 id="comm-h">Need something<br><em>written for you?</em></h2>
    </div>
    <div class="comm-in comm-r">
      <p>Kyle also writes new arrangements on commission: a holiday song your audience is asking for, a feature for your guest artist, or a full program built around your orchestra’s forces and your hall.</p>
      <a class="btn line" style="color:#fbf8f2" href="{mailto('Commission inquiry')}">Ask about a commission</a>
    </div>
  </section>
  <section class="cta">
    <div class="mono" style="color:#1d4a35">Book or request perusal</div>
    <h2>Planning your<br>holiday program?</h2>
    <p>Tell us your concert dates and which charts you’re considering. We’ll reply within one business day.<br><a class="cl" href="mailto:{EMAIL}">{EMAIL}</a></p>
    <div class="btns">
      <a class="btn solid" href="{mailto('Holiday library: booking inquiry')}">Book a chart</a>
      <a class="btn line" href="{mailto('Holiday library: perusal request')}">Request perusal scores</a>
    </div>
  </section>
</main>
{foot}
</div>
<div id="lb" role="dialog" aria-label="Score sample"><span class="x">Close ×</span><img alt=""></div>
<script>
(function(){{var lb=document.getElementById('lb'),im=lb.querySelector('img');
document.querySelectorAll('.thumb').forEach(function(b){{b.addEventListener('click',function(){{im.src=b.dataset.full;im.alt=b.getAttribute('aria-label');lb.classList.add('on')}})}});
lb.addEventListener('click',function(){{lb.classList.remove('on')}});
document.addEventListener('keydown',function(e){{if(e.key==='Escape')lb.classList.remove('on')}});}})();
</script>
{tail}"""

    page = f"""<!DOCTYPE html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow, noarchive">
{preloads}
{styles}
<style>{css}</style>
<title>Holiday Library · Kyle Daniel Gordon</title>
<meta name="description" content="Holiday orchestral arrangements by Kyle Daniel Gordon, available for rental.">
<meta property="og:type" content="website"><meta property="og:site_name" content="Kyle Daniel Gordon">
<meta property="og:title" content="Holiday Library · Kyle Daniel Gordon">
<meta property="og:description" content="Holiday arrangements for orchestra, available to rent. Orchestrator on Rosalía’s LUX.">
<meta property="og:url" content="https://www.kyledanielgordon.com/holiday-library/">
<meta property="og:image" content="https://www.kyledanielgordon.com/holiday-library/share.jpg?v=1"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="Holiday Library · Kyle Daniel Gordon">
<meta name="twitter:description" content="Holiday arrangements for orchestra, available to rent. Orchestrator on Rosalía’s LUX.">
<meta name="twitter:image" content="https://www.kyledanielgordon.com/holiday-library/share.jpg?v=1">
<meta content="#f7f4ec" name="theme-color">
<link href="/favicon.svg?v=2" rel="icon" type="image/svg+xml"><link href="/apple-touch-icon.png?v=2" rel="apple-touch-icon">
</head>
<body>
{body}
</body></html>"""
    if mode == 'preview':
        for f in os.listdir(FONTS):
            page = page.replace('/fonts/' + f, b64(os.path.join(FONTS, f), 'font/woff2'))
        page = page.replace('url(/img/', f'url({SITE}/img/').replace('href="/', f'href="{SITE}/')
        page = page.replace(tail, '')  # no analytics in the private preview
    return page

if __name__ == '__main__':
    mode, out = sys.argv[1], sys.argv[2]
    src = os.path.join(out if mode == 'site' else '/tmp/site_new', 'work-with-kyle', 'index.html')
    page = build(mode, src)
    if mode == 'preview':
        open(out, 'w').write(page)
    else:
        d = os.path.join(out, 'holiday-library'); os.makedirs(os.path.join(d, 'img'), exist_ok=True)
        open(os.path.join(d, 'index.html'), 'w').write(page)
        shutil.copy(os.path.join(HERE, 'og-holiday-library.jpg'), os.path.join(d, 'share.jpg'))
        for s in SETS:
            for c in s[2]:
                shutil.copy(os.path.join(HERE, 'img', c['slug'] + '.webp'), os.path.join(d, 'img'))
    print('ok', len(page))
