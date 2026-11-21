"""Render 1200x630 share cards for each page into og/<name>.jpg using Playwright."""
import base64, json, os
from playwright.sync_api import sync_playwright
W='/home/claude/kdg_web'
def b64(k): return 'data:image/jpeg;base64,'+base64.b64encode(open(f'{W}/{k}.jpg','rb').read()).decode()
CARDS = [
 ('home', 'Kyle Daniel Gordon', 'Orchestrator · Arranger · Conductor', 'Rosalía’s LUX · Oppenheimer · BBC Proms', 'conducting-london-symphony-orchestra-for-rosalia-lux-lso', '1/1', '#120d0b 0%, #4a1a12 24%, #b4461a 50%, #e9a36f 76%, #f7f4ec 100%'),
 ('rosalia-lux', 'Rosalía · LUX', 'Lead orchestrator', 'London Symphony Orchestra · 6 Latin Grammys', 'rosalia-lux-album', '1/1', '#0f0e10 0%, #3b3a40 30%, #a7a3a0 60%, #f7f4ec 100%'),
 ('oppenheimer', 'Oppenheimer', 'Orchestration', 'Ludwig Göransson’s Academy Award-winning score', 'oppenheimer-film-poster', '2/3', '#050302 0%, #3a1406 30%, #c2521a 62%, #f7f4ec 100%'),
 ('live', 'Live', 'BBC Proms · San Francisco Symphony', 'Bond and Beyond · Soul Revolution · The Little Bird', None, None, '#2b0f2a 0%, #8e2a5e 32%, #f08a5d 64%, #f7f4ec 100%'),
 ('pop-strings', 'Pop strings', 'String & orchestral arrangements', 'For artists, sessions and live shows', 'mollie-elizabeth-people-pleaser', '1/1', '#0e1a12 0%, #31502c 32%, #a8b85a 64%, #f7f4ec 100%'),
 ('work-with-kyle', 'Work with Kyle', 'Orchestration · Pop strings · Conducting', 'Los Angeles · London · Nashville', 'conducting-london-symphony-orchestra', '4/3', '#120f22 0%, #3b2a6a 32%, #8a76c9 64%, #f7f4ec 100%'),
 ('romani-the-untold-story', 'Romani', 'Arranger · Orchestrator · Conductor', 'Ion Zanca · London Symphony Orchestra · Billboard No. 1', 'romani-the-untold-story-london-symphony-orchestra', '1/1', '#140a0f 0%, #4b1a24 30%, #b0473c 62%, #f7f4ec 100%'),
 ('baby-shark-london-symphony-orchestra', 'Baby Shark × LSO', 'Arranger · Conductor', 'Pinkfong · London Symphony Orchestra · 2025', 'baby-shark-10th-anniversary-london-symphony-orchestra', '1/1', '#06121f 0%, #0d3b63 30%, #2f8fc4 62%, #f7f4ec 100%'),
 ('grace-kelly-with-strings-at-the-movies', 'At The Movies', 'Arranger · Orchestrator · Co-producer', 'Grace Kelly with Strings · 2024', 'grace-kelly-with-strings-at-the-movies', '1/1', '#1a0f08 0%, #5a2a14 30%, #c98a3c 62%, #f7f4ec 100%'),
 ('david-friesen-this-light-has-no-darkness', 'This Light Has No Darkness', 'Arranger · Orchestrator', 'David Friesen · 33-piece chamber orchestra', 'david-friesen-this-light-has-no-darkness', '1/1', '#0c0d14 0%, #23305a 30%, #8a8fc4 62%, #f7f4ec 100%'),
 ('mollie-elizabeth-people-pleaser', 'People Pleaser', 'Arranger · Orchestrator · Conductor', 'Mollie Elizabeth · Capitol Records · 2026', 'mollie-elizabeth-people-pleaser', '1/1', '#160b12 0%, #4e1c3a 30%, #c45a86 62%, #f7f4ec 100%'),
 ('ariza-magia-en-dos', 'Magia en Dos', 'Orchestrator', 'Ariza · 2025', 'ariza-magia-en-dos', '1/1', '#0b1012 0%, #173f45 30%, #3f9a8c 62%, #f7f4ec 100%'),
]
for pt in json.load(open('/home/claude/kdg_scripts/pitches.json')):
    CARDS.append(('for-' + pt['slug'], f"Hi {pt['name'].split()[0]}.", 'A note from Kyle Daniel Gordon', 'Orchestrator · Rosalía’s LUX · Oppenheimer', 'conducting-london-symphony-orchestra-for-rosalia-lux-lso', '1/1', '#120f22 0%, #3b2a6a 30%, #a9c3ff 62%, #f7f4ec 100%'))
TPL = '''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><style>
@font-face{font-family:D;src:url(file:///usr/share/fonts/opentype/inter/InterDisplay-Bold.otf)}
@font-face{font-family:M;src:url(file:///usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf)}
body{margin:0;width:1200px;height:630px;overflow:hidden;background:#f7f4ec;color:#1b1a17;font-family:D}
.band{position:absolute;inset:0 0 auto 0;height:300px;background:linear-gradient(180deg,%(grad)s)}
.grain{position:absolute;inset:0;background:url(file:///home/claude/kdg_tex/grain.png);opacity:.16;mix-blend-mode:multiply}
.txt{position:absolute;left:64px;bottom:60px;right:%(right)spx;display:flex;flex-direction:column;gap:18px}
.k{font-family:M;font-size:20px;letter-spacing:.06em;text-transform:uppercase}
h1{margin:0;font-size:%(size)spx;line-height:.9;letter-spacing:-.045em;text-transform:none}
.s{font-family:M;font-size:19px;letter-spacing:.04em;text-transform:uppercase;color:#625d55}
.top{position:absolute;left:64px;top:48px;font-family:M;font-size:18px;letter-spacing:.08em;text-transform:uppercase;color:#f7f4ec}
.art{position:absolute;right:64px;bottom:60px;height:%(ah)spx;aspect-ratio:%(ar)s;box-shadow:0 30px 50px -20px rgba(27,26,23,.55);background:url(%(img)s) center/cover}
.staff{position:absolute;left:64px;right:64px;bottom:28px;height:9px;background:repeating-linear-gradient(180deg,#1b1a17 0 1px,transparent 1px 2.2px);opacity:.5}
</style></head><body><div class="band"></div><div class="grain"></div>
<div class="top">kyledanielgordon.com</div>
%(artdiv)s<div class="txt"><span class="k">%(kick)s</span><h1>%(title)s</h1><span class="s">%(sub)s</span></div></body></html>'''
with sync_playwright() as p:
    b = p.chromium.launch(executable_path='/usr/bin/google-chrome')
    pg = b.new_page(viewport={'width': 1200, 'height': 630})
    for name, title, kick, sub, key, ar, grad in CARDS:
        ah = {'1/1': 400, '2/3': 470, '4/3': 330}.get(ar, 0)
        aw = {'1/1': 400, '2/3': 313, '4/3': 440}.get(ar, 0)
        html = TPL % dict(grad=grad, right=(aw + 120) if key else 64, size=96 if len(title) < 16 else 80, kick=kick, title=title, sub=sub,
                          ah=ah, ar=ar or '1', img=b64(key) if key else '', artdiv='<div class="art"></div>' if key else '')
        open('/tmp/og.html', 'w', encoding='utf-8').write(html)
        pg.goto('file:///tmp/og.html'); pg.wait_for_timeout(300)
        pg.screenshot(path=f'og/{name}.jpg', type='jpeg', quality=86)
    b.close()
print('ok')
