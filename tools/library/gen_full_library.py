"""Hidden full rental library: /library/ (noindex, not in sitemap or nav). Holiday charts are included and link to /holiday-library/.
python3 gen_full_library.py preview out.html   -> single file for review (fonts inlined)
python3 gen_full_library.py site <site_dir>      -> writes <site_dir>/library/index.html
Chart data comes from the scores themselves (instrumentation pages) and the mockup audio lengths (durations).
Rules: never say who a chart was written for; co-arrangers credited as on the score; no LUX; no artist shows.
"""
import sys, os, re, json, html, urllib.parse
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gen_library as H   # shell(), FEES, EMAIL, holiday SETS

GRAD = '#120d14 0%, #3d1838 24%, #c2577a 50%, #f3d9cf 76%'
E = html.escape
KDG = 'Kyle Daniel Gordon'

SOUL_INST = '2 fl · ob · 2 cl · bsn — alto, tenor, bari sax — 4 hn · 4 tpt · 3 tbn · b tbn · tuba — timp · 2 perc — piano · e-guitar · e-bass · drum set · harp — strings'
GOSPEL_INST = '2.2.2.2 — 4 hn · 3 tpt · 2 tbn · b tbn · tuba — timp · 2 perc — piano · e-bass · drum set · harp — strings'
WNO_INST = '2 + picc · 2 + E.H. · 2 + b cl · 2 + cbsn — 4 hn · 2 tpt · 2 tbn · b tbn · tuba — timp · perc — piano · e-guitar · bass · drum set · harp — strings'
BOND_INST = '3 (picc) · 2 · 2 + b cl · 2 — 4 hn · 3 tpt · 2 tbn · b tbn · tuba — timp · perc — piano/organ · e-guitar · e-bass · drum set · harp — strings'
MG_INST = '2.2.2.2 + alto & tenor sax — 4 hn · 3 tpt · 2 tbn · b tbn · tuba — timp · 2 perc — 2 guitars · piano · e-bass · drum set · harp — strings'
POPS1 = '1.1.1.1 — 1.1.1.1 — timp · perc — piano · harp · bass guitar · drum set — strings'

# (id, title, by, arr, cat, voices, duration, instrumentation, tags)
C = [
 # Soul & gospel
 ('ball-of-confusion', 'Ball of Confusion', 'The Temptations', KDG, 'soul', 'Lead vocal + choir', '3:45', SOUL_INST, 'soul motown protest civil rights black history month juneteenth funk upbeat energetic'),
 ('hard-times', 'Hard Times', '', KDG, 'soul', 'Lead vocal', '3:33', SOUL_INST, 'soul funk protest black history month groove'),
 ('how-i-got-over', 'How I Got Over', 'Clara Ward', KDG + ' & LJ Singers', 'gospel', 'Lead vocal + choir', '2:53', SOUL_INST, 'gospel choir church aretha black history month juneteenth uplifting celebration'),
 ('i-wish-i-knew', 'I Wish I Knew How It Would Feel to Be Free', 'Billy Taylor', KDG, 'soul', 'Lead vocal + choir', '4:34', SOUL_INST, 'nina simone civil rights freedom mlk black history month juneteenth anthem uplifting'),
 ('oh-happy-day', 'Oh Happy Day', 'Edwin Hawkins', KDG + ' & LJ Singers', 'gospel', 'Lead vocal + choir', '3:51', SOUL_INST, 'gospel choir church joyful celebration closer finale encore black history month juneteenth easter'),
 ('precious-lord', 'Precious Lord, Take My Hand', 'Thomas A. Dorsey', KDG + ' & LJ Singers', 'gospel', 'Lead vocal + choir', '4:29', SOUL_INST, 'gospel choir church ballad mlk memorial black history month reflective'),
 ('save-me-lord', 'Save Me Lord', '', KDG, 'gospel', 'Lead vocal', '2:05', SOUL_INST, 'spiritual gospel ballad nina simone reflective black history month'),
 ('say-it-loud', 'Say It Loud', 'James Brown', KDG, 'soul', 'Lead vocal + choir', '3:05', SOUL_INST, 'funk soul james brown protest black history month juneteenth energetic upbeat'),
 ('revolution', 'The Revolution Will Not Be Televised', 'Gil Scott-Heron', KDG, 'soul', 'Lead vocal (spoken)', '3:14', SOUL_INST, 'spoken word protest civil rights black history month jazz funk'),
 ('think', 'Think', 'Aretha Franklin', KDG, 'soul', 'Lead vocal + choir', '2:23', SOUL_INST, 'aretha soul women empowerment upbeat energetic black history month womens history month short'),
 ('young-gifted-black', 'To Be Young, Gifted and Black', 'Nina Simone', KDG, 'soul', 'Lead vocal + choir', '2:56', SOUL_INST, 'nina simone civil rights youth black history month juneteenth uplifting anthem'),
 ('war', 'War', 'Edwin Starr', KDG, 'soul', 'Lead vocal + choir', '3:36', SOUL_INST, 'motown protest funk powerful black history month veterans energetic'),
 ('we-shall-not-be-moved', 'We Shall Not Be Moved', 'Traditional', KDG, 'gospel', 'Lead vocal + choir', '4:34', SOUL_INST, 'spiritual civil rights freedom song mavis staples mlk black history month juneteenth anthem'),
 ('after-the-dance', 'After the Dance', 'Marvin Gaye', KDG, 'soul', 'Female & male vocals + choir', '4:47', MG_INST, 'marvin gaye soul r&b smooth romantic valentines love duet black history month'),
 ('here-my-dear', 'Here, My Dear', 'Marvin Gaye', KDG, 'soul', 'Male vocal + choir', '3:22', MG_INST, 'marvin gaye soul r&b smooth black history month'),
 ('my-mistake', 'My Mistake (Was to Love You)', 'Marvin Gaye', KDG, 'soul', 'Female & male vocals', '3:08', MG_INST, 'marvin gaye diana ross duet soul r&b love valentines black history month'),
 ('give-me-jesus', 'Give Me Jesus', 'Spiritual', KDG, 'gospel', 'Vocalist + choir', '4:06', WNO_INST, 'spiritual gospel choir ballad church reflective black history month opera singer'),
 ('my-soul-anchored', 'My Soul’s Been Anchored in the Lord', 'Spiritual', KDG, 'gospel', 'Vocalist + choir', '1:44', WNO_INST, 'spiritual gospel choir upbeat short opera singer black history month'),
 ('oh-happy-day-symphonic', 'Oh Happy Day (symphonic version)', 'Edwin Hawkins', KDG, 'gospel', 'Vocalist + choir', '3:50', WNO_INST, 'gospel choir joyful celebration finale encore full orchestra'),
 ('soul-bossa-nova', 'Soul Bossa Nova', 'Quincy Jones', KDG, 'soul', 'Vocalist + choir', '2:39', WNO_INST, 'quincy jones jazz latin bossa groove fun upbeat austin powers'),
 ('abide-with-me', 'Abide With Me', 'Traditional', 'The Spirituals & ' + KDG, 'gospel', 'Lead vocals + choir', '4:04', GOSPEL_INST, 'hymn gospel choir church memorial reflective'),
 ('bless-the-lord', 'Bless the Lord', 'Traditional', 'Volney Morgan & New-Ye & ' + KDG, 'gospel', 'Lead vocal + choir', '3:50', GOSPEL_INST, 'gospel choir church praise uplifting'),
 ('amazing-god', 'Amazing God', 'Traditional', 'Volney Morgan & New-Ye & ' + KDG, 'gospel', 'Lead vocal + choir', '3:06', GOSPEL_INST, 'gospel choir church praise uplifting'),
 ('great-i-am', 'Great I Am', 'Volney Morgan', 'Volney Morgan & New-Ye & ' + KDG, 'gospel', 'Lead vocal + choir', '5:54', GOSPEL_INST, 'gospel choir church praise big finale'),
 # Film & TV themes
 ('avengers', 'The Avengers Suite', 'Laurie Johnson', KDG, 'film', 'Instrumental', '3:11', BOND_INST, 'spy tv theme british 60s film movie opener instrumental fun family pops'),
 ('casino-royale', 'Casino Royale', 'Burt Bacharach', KDG, 'film', 'Instrumental', '2:37', BOND_INST, 'bond spy 60s herb alpert film movie instrumental fun pops short'),
 ('ohmss', 'On Her Majesty’s Secret Service', 'John Barry', KDG, 'film', 'Instrumental', '2:32', BOND_INST, 'bond spy john barry film movie instrumental pops opener short'),
 ('spectre', 'Spectre', 'Radiohead', KDG, 'film', 'Male vocal', '3:12', BOND_INST, 'bond spy radiohead film movie ballad vocal pops'),
 ('uncle', 'The Man from U.N.C.L.E.', 'Jerry Goldsmith', KDG, 'film', 'Instrumental', '2:40', BOND_INST, 'spy tv theme 60s film instrumental fun family pops short'),
 # Concert, pops & originals
 ('little-bird', 'The Little Bird', 'Kyle Daniel Gordon (original work)', '', 'concert', 'Instrumental', '5:21', '2 + picc · 2 + E.H. · 2 + b cl · 2 + cbsn — 4 hn · 3 tpt · 2 tbn · b tbn · tuba — timp · 3 perc — piano · harp — strings', 'original new music premiere spring nature birds family subscription classical contemporary'),
 ('golden-age-overture', 'Golden Age Overture', 'Kyle Daniel Gordon (original work)', '', 'concert', 'Instrumental', '1:38', '1 (+ picc) · 1 · 1 · 1 (+ cbsn) — 1.1.1.1 — timp · 2 perc — piano · upright bass · drum set · harp — strings', 'original overture opener hollywood golden age film pops short fanfare instrumental'),
 ('l-is-for-love', 'L Is for Love', 'Kyle Daniel Gordon (original work)', '', 'concert', 'Instrumental', '4:11', '1.1.1.1 — 1.1.1.1 — timp · 2 perc — piano · harp — strings', 'original love valentines romantic lyrical instrumental'),
 ('fashion', 'Fashion', 'Lady Gaga', KDG, 'concert', 'Instrumental or vocal feature', '2:54', POPS1 + ' (+ soloist)', 'lady gaga pop pride fun young audiences dance upbeat instrumental vocal'),
 ('la-vie-en-rose', 'La Vie en Rose / Non, je ne regrette rien', 'Édith Piaf', KDG, 'concert', 'Instrumental or vocal feature', '5:31', '1.1.1.1 — 1.1.1.1 — timp · perc — harp · piano · upright bass · drum set (+ opt. melodica) — strings (+ soloist)', 'piaf french paris cabaret love valentines romantic medley instrumental vocal bastille day'),
 ('orage', 'Orage (from Platée)', 'Jean-Philippe Rameau', KDG + ' (transcription)', 'concert', 'Instrumental', '2:02', 'oboe · bassoon · piano — strings', 'baroque french storm chamber small orchestra short classical instrumental'),
 ('whatd-i-say', 'What’d I Say', 'Ray Charles', KDG, 'concert', 'Vocalist (+ backing vocal)', '4:31', '2.1.2.1 + alto, 2 tenor, bari sax — 4 hn · 3 tpt · 2 tbn · b tbn · tuba — perc — piano · organ · guitar · upright bass · drums · harp — strings', 'ray charles big band jazz rhythm and blues soul swing finale encore upbeat'),
 ('ode-to-hope', 'Ode to Hope', 'Beethoven, reimagined', KDG, 'concert', 'Instrumental', 'On request', '1.1.1.1 — 1.1.1.1 — timp · perc — piano · harp — strings (+ optional flex band for side-by-side)', 'beethoven ode to joy peace unity side by side youth community education un day memorial instrumental'),
 ('ode-to-peace', 'Ode to Peace', 'Beethoven, reimagined', KDG, 'concert', 'Instrumental', 'On request', '2.2.2.2 — 4 hn · 3 tpt · 3 tbn · b tbn · tuba — timp · 3 perc — piano · harp — strings', 'beethoven ode to joy peace unity memorial anthem instrumental'),
]

CATS = [('soul', 'Soul & Motown', 'Soul, Motown, funk and freedom songs for vocalists and orchestra with rhythm section. Built to program as a full evening or drop into any pops concert.'),
        ('gospel', 'Gospel & spirituals', 'Choir-forward gospel, hymns and spirituals with orchestra and band, from quiet reflection to the big finale.'),
        ('film', 'Film & TV themes', 'Spy-era classics and modern Bond, arranged for full orchestra with rhythm section. Big, tight and fun.'),
        ('concert', 'Concert, pops & originals', 'Features, crowd-pleasers and Kyle’s own concert works, from chamber forces to full orchestra.'),
        ('holiday', 'Holiday', 'Nine holiday charts: pops with rhythm section, vocal features and gospel carols.')]

PROGRAMS = [
 ('Soul Revolution', 'A full evening of soul, Motown and freedom songs: Say It Loud, Think, War, I Wish I Knew How It Would Feel to Be Free, Oh Happy Day and more.', '13 charts · about 45 min', 'soul'),
 ('Bond & Beyond', 'A spy-themed set: The Avengers, Casino Royale, On Her Majesty’s Secret Service, The Man from U.N.C.L.E. and Spectre.', '5 charts · about 14 min', 'film'),
 ('Gospel Celebration', 'Choir-forward gospel with orchestra and band: Great I Am, Bless the Lord, Amazing God, Abide With Me, Precious Lord and Oh Happy Day.', '6+ charts · 20–25 min', 'gospel'),
 ('A Holiday Pops Half', 'Feliz Navidad, Fairytale of New York, This Christmas, Do-Re-Mi and the gospel carols. Program the half, we’ll do the rest.', '9 charts · about 35 min', 'holiday'),
]

def holiday_entries():
    out = []
    for sname, sdesc, items in H.SETS:
        for c in items:
            out.append((c['slug'], c['title'], c['by'], c.get('arr', KDG), 'holiday', c['vox'], c['dur'].replace('c. ', ''), c['inst'],
                        'holiday christmas december pops festive family ' + ('gospel choir' if 'Gospel' in sname else '') + ' ' + c['title'].lower()))
    return out

def mailto(subject, body=''):
    q = 'subject=' + urllib.parse.quote(subject) + (('&body=' + urllib.parse.quote(body)) if body else '')
    return 'mailto:' + H.EMAIL + '?' + q

def build(mode, src_page):
    styles, preloads, nav, foot, tail = H.shell(src_page)
    foot = re.sub(r'linear-gradient\(180deg, #f7f4ec 0%, [^)]*\)', 'linear-gradient(180deg, #f7f4ec 0%, #c2577a 30%, #3d1838 62%, #120d14 100%)', foot, count=1)
    allc = C + holiday_entries()
    data = [dict(id=i, t=t, by=b, arr=a, cat=c, v=v, d=d, inst=ins, tags=tg) for i, t, b, a, c, v, d, ins, tg in allc]

    def row(x):
        hol = x['cat'] == 'holiday'
        by = (E(x['by']) + ' · ' if x['by'] else '') + (('arr. ' + E(x['arr'])) if x['arr'] else '')
        cta = (f'<a class="btn line sm" href="/holiday-library/">Score sample ↗</a>' if hol else '') + \
              f'<a class="btn solid sm" href="{mailto("Perusal request: " + x["t"])}">Request perusal</a>'
        return f'''<article class="ch" id="c-{x['id']}" data-cat="{x['cat']}">
  <div class="ch-main">
    <h3>{E(x['t'])}</h3>
    <p class="by">{by}</p>
  </div>
  <div class="ch-facts"><span class="pill v">{E(x['v'])}</span><span class="pill d">{E(x['d'])}</span></div>
  <details class="ch-inst"><summary>Instrumentation</summary><p>{E(x['inst'])}</p></details>
  <div class="ch-cta">{cta}</div>
</article>'''

    secs = []
    for key, name, desc in CATS:
        rows = ''.join(row(x) for x in data if x['cat'] == key)
        n = sum(1 for x in data if x['cat'] == key)
        extra = '<p class="sec-note">Watermarked score samples for every holiday chart are on the <a class="cl" href="/holiday-library/">Holiday Library</a> page.</p>' if key == 'holiday' else ''
        secs.append(f'''<section class="sec" id="{key}" data-sec="{key}">
  <header class="sec-h"><div><span class="mono count">{n} charts</span><h2>{E(name)}</h2></div><p>{E(desc)}</p></header>
  {extra}
  <div class="rows">{rows}</div>
</section>''')

    progs = ''.join(f'''<article class="prog" data-go="{k}"><span class="mono">{E(meta)}</span><h3>{E(t)}</h3><p>{E(d)}</p>
<a class="btn line sm" style="color:#fbf8f2" href="{mailto('Program inquiry: ' + t)}">Ask about this program</a></article>''' for t, d, meta, k in PROGRAMS)
    fees = ''.join(f'<tr><th>{E(t)}</th><td data-l="First performance">${a}</td><td data-l="Each additional">${b}</td></tr>' for t, a, b in H.FEES)
    total = len(data)

    css = """
.lib{max-width:1392px;margin:0 auto;padding:0 24px;box-sizing:border-box}
.lib *{box-sizing:border-box}
.mono{font-family:'DM Mono',ui-monospace,monospace;text-transform:uppercase;letter-spacing:.04em;font-size:12px}
.lib .lede{max-width:48ch;font-size:20px;line-height:1.45;margin:0}
.lib .orch{display:grid;grid-template-columns:repeat(4,1fr);border-top:1px solid #1b1a1726;margin-top:12px}
.lib .orch div{padding:16px 16px 0 0;font-family:'Archivo','Arial Narrow',sans-serif;font-stretch:62%;font-weight:800;text-transform:uppercase;font-size:28px;line-height:1}
.ask{margin:64px 0 0;background:#1b1a17;color:#f7f4ec;padding:40px;position:relative;overflow:hidden}
.ask h2{font-family:'Archivo','Arial Narrow',sans-serif;font-stretch:62%;font-weight:800;text-transform:uppercase;font-size:clamp(40px,5vw,72px);line-height:.92;margin:8px 0 18px}
.ask h2 em{font-family:'Instrument Serif',Georgia,serif;font-style:italic;font-weight:400;text-transform:none;font-stretch:100%;color:#f3b9a6}
.ask form{display:flex;gap:10px;flex-wrap:wrap}
.ask input{flex:1 1 420px;min-height:56px;border-radius:999px;border:1px solid #f7f4ec55;background:#f7f4ec12;color:#fbf8f2;font:400 18px 'Instrument Sans',system-ui,sans-serif;padding:0 22px;outline:none}
.ask input::placeholder{color:#f7f4ec99}
.ask input:focus{border-color:#f3b9a6;background:#f7f4ec1c}
.ask .btn.solid{background:#f7f4ec;color:#1b1a17;border-color:#f7f4ec;min-height:56px}
.ask .btn.solid:hover{background:#e2581a;border-color:#e2581a;color:#fbf8f2}
.ask .eg{margin:14px 0 0;display:flex;flex-wrap:wrap;gap:8px}
.ask .eg button{font:500 12px 'DM Mono',monospace;letter-spacing:.03em;color:#f7f4ecd0;background:transparent;border:1px solid #f7f4ec40;border-radius:999px;padding:8px 12px;cursor:pointer}
.ask .eg button:hover{border-color:#f7f4ec;color:#fff}
.ask .out{margin-top:26px;display:none}
.ask .out.on{display:block}
.ask .out h4{font:500 12px 'DM Mono',monospace;letter-spacing:.06em;text-transform:uppercase;color:#f3b9a6;margin:0 0 12px}
.ask .sug{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:10px}
.ask .sug a{display:block;text-decoration:none;color:#fbf8f2;border:1px solid #f7f4ec33;padding:14px 16px;transition:border-color .15s,background .15s}
.ask .sug a:hover{border-color:#f3b9a6;background:#f7f4ec0d}
.ask .sug b{display:block;font:700 17px 'Instrument Sans',sans-serif}
.ask .sug span{font:400 12px 'DM Mono',monospace;color:#f7f4ecb0;letter-spacing:.02em}
.ask .more{margin-top:16px;font-size:15px;color:#d9d3c7}
.ask .more a{color:#fbf8f2}
.chips{position:sticky;top:0;z-index:5;background:#f7f4ecf2;backdrop-filter:blur(6px);-webkit-backdrop-filter:blur(6px);display:flex;gap:8px;flex-wrap:wrap;padding:14px 0;margin-top:48px;border-bottom:1px solid #1b1a1726}
.chips button{font:500 12px 'DM Mono',monospace;letter-spacing:.04em;text-transform:uppercase;border:1px solid #1b1a17;background:transparent;color:#1b1a17;border-radius:999px;padding:10px 14px;cursor:pointer}
.chips button[aria-pressed=true]{background:#1b1a17;color:#f7f4ec}
.chips .tot{margin-left:auto;align-self:center;color:#625d55}
.progs{margin-top:56px}
.progs .grid{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-top:14px}
.prog{position:relative;overflow:hidden;color:#fbf8f2;padding:22px;display:flex;flex-direction:column;gap:10px;background:linear-gradient(150deg,#120d14 0%,#3d1838 55%,#c2577a 130%)}
.prog:nth-child(2){background:linear-gradient(150deg,#0b0f1a 0%,#1d2f55 55%,#6f8fd0 130%)}
.prog:nth-child(3){background:linear-gradient(150deg,#140c06 0%,#4a2a12 55%,#d08a3a 130%)}
.prog:nth-child(4){background:linear-gradient(150deg,#0b1712 0%,#1d4a35 55%,#b8702f 130%)}
.prog .mono{color:#f7f4ecc0;font-size:11px}
.prog h3{font-family:'Archivo','Arial Narrow',sans-serif;font-stretch:62%;font-weight:800;text-transform:uppercase;font-size:34px;line-height:.95;margin:0}
.prog p{margin:0;font-size:15px;line-height:1.45;color:#f6eedd;flex:1}
.prog .btn{align-self:flex-start}
.sec{padding:72px 0 0;scroll-margin-top:70px}
.sec-h{display:flex;justify-content:space-between;align-items:flex-end;gap:24px;border-bottom:2px solid #1b1a17;padding-bottom:12px}
.sec-h h2{font-family:'Archivo','Arial Narrow',sans-serif;font-stretch:62%;font-weight:800;text-transform:uppercase;font-size:clamp(40px,5vw,64px);line-height:.92;margin:4px 0 0}
.sec-h .count{color:#c2577a}
.sec-h p{color:#625d55;margin:0;max-width:520px;text-align:right;font-size:15px}
.sec-note{font-size:15px;color:#625d55;margin:14px 0 0}
.ch{display:grid;grid-template-columns:minmax(0,1.6fr) 250px 150px 170px;gap:10px 24px;align-items:center;padding:18px 0;border-bottom:1px solid #1b1a1726;scroll-margin-top:80px}
.ch.hit{background:linear-gradient(90deg,#f3d9cf 0%,transparent 70%)}
.ch h3{font-family:'Archivo','Arial Narrow',sans-serif;font-stretch:62%;font-weight:800;text-transform:uppercase;font-size:28px;line-height:1;margin:0}
.ch .by{font-family:'Instrument Serif',Georgia,serif;font-style:italic;font-size:18px;color:#625d55;margin:4px 0 0}
.ch-facts{display:flex;gap:6px;flex-wrap:wrap;align-content:center}
.pill{font:500 11px 'DM Mono',monospace;letter-spacing:.03em;text-transform:uppercase;border:1px solid #1b1a1740;border-radius:999px;padding:6px 10px;white-space:nowrap}
.pill.d{background:#1b1a170d}
.ch-inst summary{cursor:pointer;font:500 11px 'DM Mono',monospace;letter-spacing:.05em;text-transform:uppercase;color:#625d55;list-style:none}
.ch-inst summary::-webkit-details-marker{display:none}
.ch-inst summary:before{content:'+ '}
.ch-inst[open] summary:before{content:'– '}
.ch-inst p{margin:6px 0 0;font-size:14px;line-height:1.45}
.ch-cta{display:flex;gap:8px;justify-content:flex-end}
.btn.sm{min-height:38px;padding:0 14px;font-size:11px}
.lib .fees{margin:96px 0 0;padding:48px;background:#1b1a17;color:#f7f4ec;display:grid;grid-template-columns:1fr 1.25fr;gap:48px}
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
.faq{margin-top:88px;display:grid;grid-template-columns:1fr 2fr;gap:24px 64px}
.faq h2{font-family:'Archivo','Arial Narrow',sans-serif;font-stretch:62%;font-weight:800;text-transform:uppercase;font-size:56px;line-height:.92;margin:0}
.faq details{border-bottom:1px solid #1b1a1726;padding:16px 0}
.faq summary{cursor:pointer;font:600 18px 'Instrument Sans',sans-serif;list-style:none}
.faq summary::-webkit-details-marker{display:none}
.faq p{margin:10px 0 0;color:#3a362f;font-size:16px;line-height:1.55;max-width:64ch}
.comm{position:relative;overflow:hidden;margin:88px 0 0;padding:56px 48px;color:#fbf8f2;background:linear-gradient(120deg,#120d14 0%,#3d1838 45%,#c2577a 100%);display:grid;grid-template-columns:1fr 1fr;gap:40px 64px;align-items:end}
.comm h2{font-family:'Archivo','Arial Narrow',sans-serif;font-stretch:62%;font-weight:800;text-transform:uppercase;font-size:clamp(44px,5.6vw,80px);line-height:.9;margin:12px 0 0}
.comm h2 em{font-family:'Instrument Serif',Georgia,serif;font-style:italic;font-weight:400;text-transform:none;font-stretch:100%;color:#f3d9cf}
.comm p{font-size:18px;line-height:1.5;margin:0 0 22px;max-width:44ch;color:#f6eedd}
.comm .btn.line:hover{background:#fbf8f2;color:#1b1a17;border-color:#fbf8f2}
.soon{margin-top:16px;font-size:15px;color:#625d55}
.cta{padding:96px 0 0;text-align:center}
.cta h2{font-family:'Archivo','Arial Narrow',sans-serif;font-stretch:62%;font-weight:800;text-transform:uppercase;font-size:clamp(48px,7vw,96px);line-height:.9;margin:12px 0 22px}
.cta p{color:#625d55;margin:0 0 26px}
.cta .btns{display:flex;gap:10px;justify-content:center;flex-wrap:wrap}
@media (max-width:1100px){.progs .grid{grid-template-columns:1fr 1fr}.ch{grid-template-columns:minmax(0,1fr) auto;}.ch-inst{grid-column:1/-1}.ch-cta{grid-column:1/-1;justify-content:flex-start}}
@media (max-width:760px){
 .lib.hero{padding-top:120px !important}
 .lib .lede{font-size:18px}
 .lib .orch{grid-template-columns:1fr 1fr}.lib .orch div{font-size:22px}
 .ask{padding:28px 20px;margin-top:48px}.ask input{flex-basis:100%;font-size:16px}.ask .btn.solid{width:100%;justify-content:center}
 .chips{gap:6px;padding:10px 24px;margin-left:-24px;margin-right:-24px;flex-wrap:nowrap;overflow-x:auto;scrollbar-width:none}.chips::-webkit-scrollbar{display:none}.chips button{padding:8px 12px;font-size:11px;white-space:nowrap;flex:0 0 auto}.chips .tot{display:none}
 .progs .grid{grid-template-columns:1fr}
 .sec-h{display:block}.sec-h p{text-align:left;margin-top:8px}
 .ch{grid-template-columns:minmax(0,1fr) auto;gap:8px 12px;padding:18px 0}.ch-main{grid-column:1/-1}.ch h3{font-size:26px}.ch-facts{grid-column:1/-1}.ch-inst{grid-column:1/2;align-self:center}.ch-cta{grid-column:2/3;grid-row:3;justify-content:flex-end}.ch-cta .btn.solid{background:transparent;color:#1b1a17;border-color:#1b1a17}
 .lib .fees{grid-template-columns:1fr;padding:30px 22px;gap:20px}.lib .fees h2{font-size:44px}
 .lib table thead{display:none}
 .lib table tr{display:grid;grid-template-columns:1fr 1fr;gap:4px 16px;padding:16px 0;border-bottom:1px solid #f7f4ec2e}
 .lib table th{grid-column:1/-1;border:0;padding:0 0 4px;font-size:17px}
 .lib table td{border:0;padding:0;text-align:left;font-size:22px}
 .lib table td:before{content:attr(data-l);display:block;font:500 10px 'DM Mono',monospace;letter-spacing:.06em;text-transform:uppercase;color:#bdb6a8;margin-bottom:2px}
 .faq{grid-template-columns:1fr}.faq h2{font-size:44px}
 .comm{grid-template-columns:1fr;padding:36px 22px;gap:20px}
 .cta{padding-top:72px}.cta .btns .btn{width:100%;justify-content:center;max-width:340px}
}"""

    js = """
(function(){
var D=__DATA__;
var SYN={'bhm':'black history month','mlk':'mlk civil rights','xmas':'christmas holiday','christmas':'holiday christmas','july':'patriotic','4th':'patriotic','fourth':'patriotic','independence':'patriotic','memorial':'memorial reflective','veterans':'veterans patriotic','valentine':'love valentines romantic','valentines':'love valentines romantic','romance':'love romantic','kids':'family young audiences','children':'family young audiences','family':'family','movie':'film movie','movies':'film movie','film':'film movie','spy':'spy bond','007':'bond spy','james':'bond','church':'gospel church','gospel':'gospel choir','choir':'choir','soul':'soul','motown':'motown soul','funk':'funk','jazz':'jazz big band','swing':'swing jazz','opener':'opener overture','overture':'overture opener','closer':'finale encore closer','finale':'finale closer encore','encore':'encore finale','french':'french paris','paris':'paris french','pride':'pride','women':'womens history month women','juneteenth':'juneteenth black history month','easter':'easter gospel','peace':'peace unity','unity':'unity peace','new':'original new music','premiere':'original premiere','short':'short','instrumental':'instrumental','vocalist':'vocal','singer':'vocal','duet':'duet'};
function words(s){return (s||'').toLowerCase().replace(/[^a-z0-9&' ]+/g,' ').split(/\\s+/).filter(Boolean)}
function expand(q){var w=words(q),o=w.slice();w.forEach(function(x){if(SYN[x])o=o.concat(words(SYN[x]))});for(var i=0;i<w.length-1;i++){var b=w[i]+' '+w[i+1];if(b=='black history')o=o.concat(['black','history','month']);if(b=='no vocalist'||b=='no singer'||b=='no vocals'||b=='without vocalist'||b=='no choir')o.push('__noVoc')}return o}
function mins(d){var m=/^(\\d+):(\\d+)/.exec(d);return m?(+m[1]+ +m[2]/60):null}
function score(c,ws,q){var hay=(c.tags+' '+c.t+' '+c.by+' '+c.v+' '+c.cat).toLowerCase(),s=0;
 ws.forEach(function(w){if(w.length<3&&w!='r&b')return;if(hay.indexOf(w)>=0)s+= (c.t.toLowerCase().indexOf(w)>=0?3:1)});
 var noV=ws.indexOf('__noVoc')>=0||/no (vocal|singer|choir)|without (a )?(vocal|singer)|instrumental only/.test(q);
 if(noV){if(/instrumental/i.test(c.v))s+=2;else s-=99}
 if(/choir/.test(q)&&/choir/i.test(c.v))s+=1;
 if(/short|under 3/.test(q)){var m=mins(c.d);if(m&&m<3)s+=1}
 return s}
var form=document.getElementById('askf'),inp=document.getElementById('askq'),out=document.getElementById('asko'),sug=document.getElementById('asks'),more=document.getElementById('askm');
function run(q){q=(q||'').trim();if(!q)return;var lq=q.toLowerCase(),ws=expand(lq);
 var r=D.map(function(c){return [score(c,ws,lq),c]}).filter(function(x){return x[0]>0}).sort(function(a,b){return b[0]-a[0]}).slice(0,8);
 document.querySelectorAll('.ch.hit').forEach(function(e){e.classList.remove('hit')});
 sug.innerHTML=r.length?r.map(function(x){var c=x[1];return '<a href="#c-'+c.id+'" data-id="'+c.id+'"><b>'+c.t+'</b><span>'+(c.by?c.by+' · ':'')+c.v+' · '+c.d+'</span></a>'}).join(''):'<p style="margin:0;color:#d9d3c7">Nothing in the library matches that exactly yet, but Kyle writes new arrangements on commission.</p>';
 var pat=/patriot|july|4th|fourth|independence|veteran|memorial day|americana/.test(lq)?'<p style="margin:0 0 10px;color:#f3b9a6">Patriotic and Americana charts are being added to the library. Ask us and we’ll send the list.</p>':'';
 out.querySelector('h4').textContent=r.length?'Suggested for “'+q+'”':'For “'+q+'”';
 more.innerHTML=pat+'Want a hand building the program? <a href="mailto:__EMAIL__?subject='+encodeURIComponent('Program help: '+q)+'&body='+encodeURIComponent('Hi Alex,\\n\\nWe are planning: '+q+'\\n\\nConcert date(s):\\nOrchestra size:\\nVocalists / choir:\\n\\nThanks!')+'">Send this to the library</a> and we’ll put together a list within one business day.';
 out.classList.add('on');
 r.forEach(function(x){var e=document.getElementById('c-'+x[1].id);if(e)e.classList.add('hit')});
 try{if(window.clarity)clarity('event','library_ask')}catch(e){}
}
form.addEventListener('submit',function(e){e.preventDefault();run(inp.value)});
document.querySelectorAll('.eg button').forEach(function(b){b.addEventListener('click',function(){inp.value=b.textContent;run(b.textContent)})});
sug.addEventListener('click',function(e){var a=e.target.closest('a[data-id]');if(!a)return;e.preventDefault();show('all');var el=document.getElementById('c-'+a.dataset.id);el.scrollIntoView({behavior:'smooth',block:'center'});var d=el.querySelector('details');if(d)d.open=true});
function show(cat){document.querySelectorAll('.chips button[data-f]').forEach(function(b){b.setAttribute('aria-pressed',b.dataset.f==cat)});
 document.querySelectorAll('.sec').forEach(function(s){s.style.display=(cat=='all'||s.dataset.sec==cat)?'':'none'})}
document.querySelectorAll('.chips button[data-f]').forEach(function(b){b.addEventListener('click',function(){show(b.dataset.f);var t=document.getElementById(b.dataset.f=='all'?'soul':b.dataset.f);if(t)t.scrollIntoView({behavior:'smooth'})})});
document.querySelectorAll('.prog').forEach(function(p){p.addEventListener('click',function(e){if(e.target.closest('a'))return;show(p.dataset.go);document.getElementById(p.dataset.go).scrollIntoView({behavior:'smooth'})})});
})();"""
    js = js.replace('__DATA__', json.dumps([{k: x[k] for k in ('id', 't', 'by', 'v', 'd', 'cat', 'tags')} for x in data], ensure_ascii=False)).replace('__EMAIL__', H.EMAIL)

    examples = ['Black History Month, gospel choir', 'Family concert, no vocalist', 'Spy and film night', 'Valentine’s pops', 'A big finale with choir', 'Short opener']
    body = f"""<div style="position: relative; background: #f7f4ec; color: #1b1a17; font-family: 'Instrument Sans', system-ui, sans-serif; font-size: 16px; line-height: 1.55; overflow-x: clip">
<span class="grainm"></span>
<header style="position: relative">
<div aria-hidden="true" style="position: absolute; left: 0; right: 0; top: 0; height: 460px; background: linear-gradient(180deg, {GRAD}); overflow: hidden; -webkit-mask-image: linear-gradient(180deg, #000 0%, #000 42%, rgba(0,0,0,.55) 70%, rgba(0,0,0,.18) 86%, transparent 100%); mask-image: linear-gradient(180deg, #000 0%, #000 42%, rgba(0,0,0,.55) 70%, rgba(0,0,0,.18) 86%, transparent 100%)"><span class="grain" style="opacity: 0.38"></span></div>
{nav}
<div class="lib hero" style="position: relative; padding-top: 230px">
  <div class="rise" style="display: flex; flex-direction: column; gap: 24px">
    <span class="mono" style="color: #3d1838">KG Music Library · Orchestra rentals</span>
    <h1 style="margin: 0; font-family: 'Archivo', 'Arial Narrow', sans-serif; font-stretch: 62%; font-weight: 800; text-transform: uppercase; font-size: clamp(76px, 12vw, 190px); line-height: 0.84; color: #3d1838">The<br><em style="font-family: 'Instrument Serif', Georgia, serif; font-style: italic; font-weight: 400; text-transform: none; font-stretch: 100%; color: #c2577a; letter-spacing: -0.02em">arrangements</em><br>library</h1>
    <p class="lede">{total} concert-ready charts by Kyle Daniel Gordon, orchestrator on Rosalía’s <i>LUX</i>, recorded with the London Symphony Orchestra, which won Album of the Year at the Latin Grammys and is nominated for Album of the Year at the Grammys. Soul and gospel, film themes, pops features, original works and holiday, all engraved and ready for the stands.</p>
    <div style="display: flex; flex-wrap: wrap; gap: 10px"><a class="btn solid" href="#ask">Find charts for your concert</a><a class="btn line" href="#fees">Rental fees</a></div>
  </div>
  <div class="mono" style="margin-top: 64px; color: #625d55">Kyle writes for</div>
  <div class="orch"><div>London Symphony Orchestra</div><div>New York Philharmonic</div><div>San Francisco Symphony</div><div>BBC Concert Orchestra</div></div>
</div>
</header>
<main class="lib">
  <section class="ask" id="ask" aria-labelledby="ask-h">
    <span aria-hidden="true" class="grain" style="opacity: 0.25"></span>
    <div style="position:relative">
      <span class="mono" style="color:#f3b9a6">Program finder</span>
      <h2 id="ask-h">What are you <em>planning?</em></h2>
      <form id="askf" role="search"><label for="askq" class="mono" style="position:absolute;left:-9999px">Describe your concert</label>
        <input id="askq" type="text" autocomplete="off" placeholder="e.g. Black History Month concert with a gospel choir, about 20 minutes">
        <button class="btn solid" type="submit">Suggest charts</button></form>
      <div class="eg">{''.join(f'<button type="button">{E(x)}</button>' for x in examples)}</div>
      <div class="out" id="asko" aria-live="polite"><h4></h4><div class="sug" id="asks"></div><p class="more" id="askm"></p></div>
    </div>
  </section>
  <section class="progs" aria-labelledby="pg-h">
    <span class="mono" style="color:#c2577a">Ready-made programs</span>
    <h2 id="pg-h" style="font-family:'Archivo','Arial Narrow',sans-serif;font-stretch:62%;font-weight:800;text-transform:uppercase;font-size:clamp(40px,5vw,64px);line-height:.92;margin:6px 0 0">Program a whole half</h2>
    <div class="grid">{progs}</div>
  </section>
  <nav class="chips" aria-label="Filter the library"><button data-f="all" aria-pressed="true">All</button>{''.join(f'<button data-f="{k}" aria-pressed="false">{E(n)}</button>' for k, n, _ in CATS)}<span class="mono tot">{total} charts</span></nav>
  {''.join(secs)}
  <p class="soon mono">Coming soon: patriotic &amp; Americana. <a class="cl" href="{mailto('Patriotic charts')}">Ask for the list</a></p>
  <section class="fees" id="fees">
    <div>
      <div class="mono" style="color:#e2581a">Rental fees</div>
      <h2>Per chart, per run</h2>
      <p>One fee covers all performances of a chart within a single run of up to six weeks. Score and parts are delivered as PDFs, or printed and shipped, with shipping billed at cost.</p>
      <ul class="terms">
        <li>Renting a full program? Ask about program pricing</li>
        <li>Rush delivery (within 3 weeks of first rehearsal): +$100</li>
        <li>Performance licensing for the underlying songs is handled through your usual ASCAP/BMI licenses</li>
        <li>Recording, broadcast and streaming by arrangement</li>
      </ul>
    </div>
    <table><thead><tr><th>Orchestra</th><th>First performance</th><th>Each additional</th></tr></thead><tbody>{fees}</tbody></table>
  </section>
  <section class="faq" aria-labelledby="faq-h">
    <h2 id="faq-h">Good to know</h2>
    <div>
      <details><summary>Can I see the score before booking?</summary><p>Yes. Request a perusal score for any chart and we’ll send a watermarked PDF, usually within one business day.</p></details>
      <details><summary>What if my vocalist needs a different key?</summary><p>Ask us. Many charts can be adapted for your soloist; we’ll tell you what’s possible and what it costs before anything is booked.</p></details>
      <details><summary>Do we need extra licensing?</summary><p>The rental covers the arrangement. Performance rights for the underlying songs go through your orchestra’s usual ASCAP/BMI licenses. Recording, broadcast and streaming are arranged separately.</p></details>
      <details><summary>How are parts delivered?</summary><p>As print-ready PDFs (score and parts), or printed and shipped to you, with shipping billed at cost.</p></details>
      <details><summary>Our orchestra is smaller than the listed instrumentation.</summary><p>Tell us your forces. Several charts work with reduced winds or brass, and we’ll say which ones honestly.</p></details>
    </div>
  </section>
  <section class="comm" aria-labelledby="comm-h">
    <span aria-hidden="true" class="grain" style="opacity: 0.34"></span>
    <div style="position:relative"><div class="mono" style="color:#f3d9cf">Commissions</div><h2 id="comm-h">Need something<br><em>written for you?</em></h2></div>
    <div style="position:relative"><p>Kyle also writes new arrangements on commission: a song your audience is asking for, a feature for your guest artist, or a full program built around your orchestra’s forces and your hall.</p>
    <a class="btn line" style="color:#fbf8f2" href="{mailto('Commission inquiry')}">Ask about a commission</a></div>
  </section>
  <section class="cta">
    <div class="mono" style="color:#3d1838">Book or request perusal</div>
    <h2>Let’s build<br>your program</h2>
    <p>Tell us your dates, your forces and what you’re considering. We’ll reply within one business day.<br><a class="cl" href="mailto:{H.EMAIL}">{H.EMAIL}</a></p>
    <div class="btns"><a class="btn solid" href="{mailto('Library: booking inquiry')}">Book charts</a><a class="btn line" href="{mailto('Library: perusal request')}">Request perusal scores</a></div>
  </section>
</main>
{foot}
</div>
<script>{js}</script>
{tail}"""

    og = '''<meta property="og:type" content="website"><meta property="og:site_name" content="Kyle Daniel Gordon">
<meta property="og:title" content="The Arrangements Library · Kyle Daniel Gordon">
<meta property="og:description" content="Concert-ready orchestral arrangements to rent: soul and gospel, film themes, pops features and holiday.">
<meta property="og:image" content="https://www.kyledanielgordon.com/library/share.jpg?v=1"><meta name="twitter:card" content="summary_large_image">'''
    page = f"""<!DOCTYPE html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow, noarchive">
{preloads}
{styles}
<style>{css}</style>
<title>The Arrangements Library · Kyle Daniel Gordon</title>
<meta name="description" content="Concert-ready orchestral arrangements by Kyle Daniel Gordon, available to rent.">
{og}
<meta content="#f7f4ec" name="theme-color">
<link href="/favicon.svg?v=2" rel="icon" type="image/svg+xml"><link href="/apple-touch-icon.png?v=2" rel="apple-touch-icon">
</head>
<body>
{body}
</body></html>"""
    if mode == 'preview':
        for f in os.listdir(H.FONTS):
            page = page.replace('/fonts/' + f, H.b64(os.path.join(H.FONTS, f), 'font/woff2'))
        page = page.replace('url(/img/', f'url({H.SITE}/img/').replace('href="/', f'href="{H.SITE}/')
        page = page.replace(tail, '')
    return page

if __name__ == '__main__':
    mode, out = sys.argv[1], sys.argv[2]
    src = os.path.join(out if mode == 'site' else '/tmp/site_new', 'work-with-kyle', 'index.html')
    page = build(mode, src)
    if mode == 'preview':
        open(out, 'w').write(page)
    else:
        d = os.path.join(out, 'library'); os.makedirs(d, exist_ok=True)
        open(os.path.join(d, 'index.html'), 'w').write(page)
        og = os.path.join(HERE, 'og-library.jpg')
        if os.path.exists(og):
            import shutil; shutil.copy(og, os.path.join(d, 'share.jpg'))
    print('ok', len(page))
