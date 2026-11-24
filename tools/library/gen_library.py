"""Hidden holiday rental catalog: /holiday-library/ (noindex, not in sitemap or nav).
python3 gen_library.py preview out.html   -> single file, fonts + images inlined (for review)
python3 gen_library.py site <site_dir>      -> writes <site_dir>/holiday-library/index.html + images
"""
import sys, os, base64, html, shutil, urllib.parse

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

def build(mode):
    E = html.escape
    def font(name):
        p = os.path.join(FONTS, name)
        return b64(p, 'font/woff2') if mode == 'preview' else '/fonts/' + name
    def img(slug):
        p = os.path.join(HERE, 'img', slug + '.webp')
        return b64(p, 'image/webp') if mode == 'preview' else f'/holiday-library/img/{slug}.webp'

    cards = []
    n = 0
    for sname, sdesc, items in SETS:
        rows = []
        for c in items:
            n += 1
            rows.append(f'''
<article class="chart">
  <button class="thumb" data-full="{img(c['slug'])}" aria-label="Score sample: {E(c['title'])}">
    <img src="{img(c['slug'])}" alt="First score page of {E(c['title'])}, watermarked" loading="lazy" width="1100" height="1700">
    <span class="zoom">Score sample ↗</span>
  </button>
  <div class="meta">
    <div class="num">{n:02d}</div>
    <h3>{E(c['title'])}</h3>
    <p class="by">{E(c['by'])} · arr. {E(c.get('arr','Kyle Daniel Gordon'))}</p>
    <dl>
      <div><dt>Duration</dt><dd>{E(c['dur'])}</dd></div>
      <div><dt>Voices</dt><dd>{E(c['vox'])}</dd></div>
      <div class="wide"><dt>Instrumentation</dt><dd>{E(c['inst'])}</dd></div>
    </dl>
    <a class="btn" href="{mailto('Perusal request: ' + c['title'])}">Request perusal score</a>
  </div>
</article>''')
        cards.append(f'''
<section class="set">
  <header class="sethead"><h2>{E(sname)}</h2><p>{E(sdesc)}</p></header>
  {''.join(rows)}
</section>''')

    fees = ''.join(f'<tr><th>{E(t)}</th><td>${a}</td><td>${b}</td></tr>' for t, a, b in FEES)

    return f'''<!DOCTYPE html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow, noarchive">
<title>Holiday Library · Kyle Daniel Gordon</title>
<meta name="description" content="Holiday orchestral arrangements by Kyle Daniel Gordon, available for rental.">
<style>
@font-face{{font-family:'Archivo';font-weight:800;font-stretch:62%;font-display:swap;src:url({font('archivo-62-800.v2.woff2')}) format('woff2')}}
@font-face{{font-family:'DM Mono';font-weight:400;font-display:swap;src:url({font('dm-mono-400.v2.woff2')}) format('woff2')}}
@font-face{{font-family:'Instrument Sans';font-weight:400 700;font-display:swap;src:url({font('instrument-sans.v2.woff2')}) format('woff2')}}
@font-face{{font-family:'Instrument Serif';font-style:italic;font-display:swap;src:url({font('instrument-serif-italic.v2.woff2')}) format('woff2')}}
:root{{--ink:#1b1a17;--mute:#625d55;--cream:#f7f4ec;--paper:#fbf8f2;--or:#e2581a;--ol:#6f7a1c;--line:#1b1a1726}}
*{{box-sizing:border-box}}
html{{-webkit-text-size-adjust:100%}}
body{{margin:0;background:var(--cream);color:var(--ink);font:400 17px/1.55 'Instrument Sans',system-ui,sans-serif}}
a{{color:inherit}}
.mono{{font-family:'DM Mono',ui-monospace,monospace;font-size:12px;letter-spacing:.08em;text-transform:uppercase}}
.wrap{{max-width:1180px;margin:0 auto;padding:0 28px}}
.top{{display:flex;justify-content:space-between;align-items:center;padding:22px 0;border-bottom:1px solid var(--line)}}
.top a{{text-decoration:none}}
.hero{{padding:72px 0 56px;border-bottom:1px solid var(--line)}}
.hero h1{{font-family:'Archivo','Arial Narrow',sans-serif;font-weight:800;font-stretch:62%;text-transform:uppercase;font-size:clamp(64px,11vw,168px);line-height:.86;letter-spacing:-.01em;margin:18px 0 28px}}
.hero h1 em{{font-family:'Instrument Serif',Georgia,serif;font-style:italic;font-weight:400;text-transform:none;font-stretch:100%;color:var(--or);letter-spacing:-.02em}}
.lede{{max-width:640px;font-size:20px;line-height:1.5;margin:0}}
.creds{{display:grid;grid-template-columns:repeat(4,1fr);gap:0;margin-top:12px;border-top:1px solid var(--line)}}
.creds div{{padding:18px 18px 0 0}}
.creds b{{display:block;font-family:'Archivo','Arial Narrow',sans-serif;font-stretch:62%;font-weight:800;text-transform:uppercase;font-size:28px;line-height:1}}
.creds span{{color:var(--mute);font-size:14px}}
.set{{padding:64px 0 8px}}
.sethead{{display:flex;justify-content:space-between;align-items:baseline;gap:24px;border-bottom:2px solid var(--ink);padding-bottom:12px;margin-bottom:8px}}
.sethead h2{{font-family:'Archivo','Arial Narrow',sans-serif;font-stretch:62%;font-weight:800;text-transform:uppercase;font-size:44px;line-height:1;margin:0}}
.sethead p{{color:var(--mute);margin:0;max-width:520px;text-align:right;font-size:15px}}
.chart{{display:grid;grid-template-columns:220px 1fr;gap:36px;padding:32px 0;border-bottom:1px solid var(--line)}}
.thumb{{position:relative;padding:0;border:1px solid var(--line);background:#fff;cursor:zoom-in;display:block;width:100%;aspect-ratio:11/17;overflow:hidden;box-shadow:0 1px 0 var(--line),0 12px 28px -18px #1b1a1766;transition:transform .2s}}
.thumb:hover{{transform:translateY(-3px)}}
.thumb img{{width:100%;height:100%;object-fit:cover;object-position:top;display:block}}
.zoom{{position:absolute;left:0;right:0;bottom:0;background:var(--ink);color:var(--cream);font:500 11px/1 'DM Mono',monospace;letter-spacing:.08em;text-transform:uppercase;padding:9px}}
.num{{font-family:'DM Mono',monospace;font-size:12px;color:var(--or)}}
.meta h3{{font-family:'Archivo','Arial Narrow',sans-serif;font-stretch:62%;font-weight:800;text-transform:uppercase;font-size:clamp(36px,4.4vw,56px);line-height:.95;margin:6px 0 6px}}
.by{{font-family:'Instrument Serif',Georgia,serif;font-style:italic;font-size:21px;color:var(--mute);margin:0 0 18px}}
dl{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px 28px;margin:0 0 22px}}
dl .wide{{grid-column:1/-1}}
dt{{font-family:'DM Mono',monospace;font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:var(--mute);margin-bottom:2px}}
dd{{margin:0;font-size:16px}}
.btn{{display:inline-block;background:var(--ink);color:var(--cream);text-decoration:none;font:500 12px/1 'DM Mono',monospace;letter-spacing:.08em;text-transform:uppercase;padding:14px 18px;border-radius:999px;transition:background .15s}}
.btn:hover{{background:var(--or)}}
.btn.alt{{background:transparent;color:var(--ink);box-shadow:inset 0 0 0 1.5px var(--ink)}}
.btn.alt:hover{{background:var(--ink);color:var(--cream)}}
.fees{{margin:72px 0 0;padding:48px;background:var(--ink);color:var(--cream);border-radius:4px;display:grid;grid-template-columns:1fr 1.25fr;gap:48px}}
.fees h2{{font-family:'Archivo','Arial Narrow',sans-serif;font-stretch:62%;font-weight:800;text-transform:uppercase;font-size:56px;line-height:.92;margin:10px 0 16px}}
.fees p{{color:#d9d3c7;font-size:15px;margin:0 0 10px}}
table{{width:100%;border-collapse:collapse}}
th,td{{text-align:left;padding:14px 0;border-bottom:1px solid #f7f4ec2e;font-size:16px;vertical-align:top}}
td{{text-align:right;font-family:'DM Mono',monospace;font-size:18px;white-space:nowrap;padding-left:16px}}
thead th{{font:500 11px 'DM Mono',monospace;letter-spacing:.08em;text-transform:uppercase;color:#bdb6a8}}
thead th:not(:first-child){{text-align:right}}
.terms{{list-style:none;padding:0;margin:18px 0 0;color:#d9d3c7;font-size:14px}}
.terms li{{padding:4px 0 4px 16px;position:relative}}
.terms li:before{{content:'—';position:absolute;left:0;color:var(--or)}}
.cta{{padding:80px 0 96px;text-align:center}}
.cta h2{{font-family:'Archivo','Arial Narrow',sans-serif;font-stretch:62%;font-weight:800;text-transform:uppercase;font-size:clamp(48px,7vw,96px);line-height:.9;margin:12px 0 22px}}
.cta p{{color:var(--mute);margin:0 0 26px}}
.cta .btns{{display:flex;gap:12px;justify-content:center;flex-wrap:wrap}}
footer{{border-top:1px solid var(--line);padding:24px 0 40px;color:var(--mute);font-size:13px;display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap}}
#lb{{position:fixed;inset:0;background:#1b1a17e6;display:none;align-items:flex-start;justify-content:center;overflow:auto;padding:4vh 16px;z-index:9;cursor:zoom-out}}
#lb.on{{display:flex}}
#lb img{{max-width:min(900px,100%);height:auto;background:#fff;box-shadow:0 20px 60px #0008}}
#lb .x{{position:fixed;top:14px;right:18px;color:var(--cream);font:500 12px 'DM Mono',monospace;letter-spacing:.08em;text-transform:uppercase}}
@media (max-width:760px){{
 .wrap{{padding:0 18px}} .top span{{display:none}}
 .hero{{padding:44px 0 40px}}
 .creds{{grid-template-columns:1fr 1fr}} .creds b{{font-size:22px}}
 .sethead{{display:block}} .sethead p{{text-align:left;margin-top:8px}}
 .chart{{grid-template-columns:110px 1fr;gap:18px}}
 dl{{grid-template-columns:1fr}}
 .fees{{grid-template-columns:1fr;padding:28px 22px;gap:24px}}
 .fees h2{{font-size:44px}}
}}
</style></head>
<body>
<div class="wrap">
  <nav class="top mono"><a href="https://www.kyledanielgordon.com/">Kyle Daniel Gordon</a><span>Holiday Library · Rentals</span></nav>

  <header class="hero">
    <div class="mono" style="color:var(--ol)">KG Music Library · For orchestras</div>
    <h1>Holiday<br><em>arrangements</em><br>for orchestra</h1>
    <p class="lede">Nine holiday charts by Kyle Daniel Gordon, orchestrator on Rosalía’s <i>LUX</i>, recorded with the London Symphony Orchestra, which won Album of the Year at the Latin Grammys and is nominated for Album of the Year at the Grammys. Engraved and ready for the stands, for pops orchestra, choir and rhythm section.</p>
    <div class="mono" style="margin-top:44px;color:var(--mute)">Kyle writes for</div>
    <div class="creds orchs">
      <div><b>London Symphony Orchestra</b></div>
      <div><b>New York Philharmonic</b></div>
      <div><b>San Francisco Symphony</b></div>
      <div><b>BBC Concert Orchestra</b></div>
    </div>
  </header>

  {''.join(cards)}

  <section class="fees" id="fees">
    <div>
      <div class="mono" style="color:var(--or)">Rental fees</div>
      <h2>Per chart, per run</h2>
      <p>One fee covers all performances of a chart within a single run of up to six weeks. Score and parts are delivered as PDFs, or printed and shipped, with shipping billed at cost.</p>
      <ul class="terms">
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

  <section class="cta">
    <div class="mono" style="color:var(--ol)">Book or request perusal</div>
    <h2>Planning your<br>holiday program?</h2>
    <p>Tell us your concert dates and which charts you’re considering. We’ll reply within one business day.</p>
    <div class="btns">
      <a class="btn" href="{mailto('Holiday library: booking inquiry')}">Book a chart</a>
      <a class="btn alt" href="{mailto('Holiday library: perusal request')}">Request perusal scores</a>
    </div>
  </section>

  <footer><span>KG Music Library · KG Music LLC · Los Angeles, California</span><a href="mailto:{EMAIL}">{EMAIL}</a></footer>
</div>
<div id="lb" role="dialog" aria-label="Score sample"><span class="x">Close ×</span><img alt=""></div>
<script>
(function(){{var lb=document.getElementById('lb'),im=lb.querySelector('img');
document.querySelectorAll('.thumb').forEach(function(b){{b.addEventListener('click',function(){{im.src=b.dataset.full;im.alt=b.getAttribute('aria-label');lb.classList.add('on')}})}});
lb.addEventListener('click',function(){{lb.classList.remove('on')}});
document.addEventListener('keydown',function(e){{if(e.key==='Escape')lb.classList.remove('on')}});}})();
</script>
</body></html>'''

if __name__ == '__main__':
    mode, out = sys.argv[1], sys.argv[2]
    page = build(mode)
    if mode == 'preview':
        open(out, 'w').write(page)
    else:
        d = os.path.join(out, 'holiday-library'); os.makedirs(os.path.join(d, 'img'), exist_ok=True)
        open(os.path.join(d, 'index.html'), 'w').write(page)
        for s in SETS:
            for c in s[2]:
                shutil.copy(os.path.join(HERE, 'img', c['slug'] + '.webp'), os.path.join(d, 'img'))
    print('ok', len(page))
