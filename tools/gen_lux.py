import os, sys, json
from urllib.parse import quote
sys.path.insert(0, '/home/claude/kdg_scripts')
from gen_muck import page, COND, MONO, C, G

OUT = sys.argv[1]
A = json.load(open('/home/claude/kdg_scripts/assets.json'))
SANS = "font-family: 'Instrument Sans', system-ui, sans-serif; font-weight: 600"
INK, PAPER, MUTE, RULE = '#1b1a17', '#f7f4ec', '#625d55', 'rgba(27,26,23,0.22)'
OM = 'Orchestration & music department'
WRAP = 'position: relative; max-width: 1392px; margin: 0 auto; padding-left: 24px; padding-right: 24px; box-sizing: border-box'
CATCOL = {'Record': C['olive'], 'Stage': C['olive'], 'Film': C['tang'], 'Television': C['mag'], 'Game': C['sky']}
TINT = {'Record': '#e6eac9', 'Stage': '#e6eac9', 'Film': '#f6dcc8', 'Television': '#f4d3e3', 'Game': '#d8e8fb'}


def sp_search(q):
    return 'https://open.spotify.com/search/' + quote(q)


# title, category, role, with, image key, spotify
P = [
 ('LUX', 'Record', 'Supervising orchestrator', 'Rosalía · London Symphony Orchestra', 'rosalia-lux-album', 'https://open.spotify.com/album/3SUEJULSGgBDG1j4GQhfYY'),
 ('Romani: The Untold Story', 'Record', 'Arranger, orchestrator, conductor', 'Ion Zanca · Dallas String Quartet · LSO', 'romani-the-untold-story-london-symphony-orchestra', 'https://open.spotify.com/track/31eojlHu2jxOHQr5NW74PL'),
 ('Baby Shark 10th Anniversary', 'Record', 'Arranger, orchestrator, conductor', 'Pinkfong · London Symphony Orchestra', 'baby-shark-10th-anniversary-london-symphony-orchestra', 'https://open.spotify.com/album/6myoH7UjcukBliJGvWorpG'),
 ('BBC Proms: Bond and Beyond', 'Stage', 'Arranger · organ on Radiohead’s “Spectre”', 'BBC Concert Orchestra · 2026', None, 'https://www.instagram.com/kylegordonmusic/reel/Dejq7epTaDR/'),
 ('BBC Proms: Marvin Gaye, Prince of Soul', 'Stage', 'Arrangements', 'BBC Concert Orchestra · 2026', None, None),
 ('BBC Proms: Soul Revolution', 'Stage', 'Arranger, composer (finale), organ', 'BBC Concert Orchestra · 2025', None, 'https://www.instagram.com/kylegordonmusic/reel/DM7t0RKo_Ne/'),
 ('The Little Bird', 'Stage', 'Composer · world premiere', 'San Francisco Symphony · 2026', None, None),
 ('People Pleaser', 'Record', 'Arranger', 'Mollie Elizabeth · 2026', 'mollie-elizabeth-people-pleaser', 'https://open.spotify.com/album/6vYVu3wSl9OedjOU8n8pVX'),
 ('Grace Kelly with Strings: At The Movies', 'Record', 'Arranger, orchestrator, co-producer', 'Grace Kelly', 'grace-kelly-with-strings-at-the-movies', 'https://open.spotify.com/album/2buBjbRAHUe3QMiWbRuHM0'),
 ('This Light Has No Darkness', 'Record', 'Arranger, orchestrator, co-producer', 'David Friesen', 'david-friesen-this-light-has-no-darkness', sp_search('David Friesen This Light Has No Darkness')),
 ('Magia en Dos', 'Record', 'Orchestrator', 'Ariza', 'ariza-magia-en-dos', sp_search('Ariza Magia en Dos')),
 ('Hawthorne Heights', 'Stage', 'Arranger', 'Touring orchestral show', None, sp_search('Hawthorne Heights')),
 ('Escape the Fate', 'Stage', 'Arranger', 'Touring orchestral show', None, sp_search('Escape the Fate')),
 ('Oppenheimer', 'Film', 'Orchestrator', 'Ludwig Göransson', 'oppenheimer-film-poster', 'https://open.spotify.com/album/0rwbMKjNkp4ehQTwf9V2Jk'),
 ('Frozen II', 'Film', OM, '', 'frozen-ii', sp_search('Frozen II soundtrack')),
 ('Star Wars: The Last Jedi', 'Film', OM, 'John Williams', 'star-wars-the-last-jedi', sp_search('Star Wars The Last Jedi soundtrack')),
 ('Star Wars: The Rise of Skywalker', 'Film', 'Music department', 'John Williams', 'star-wars-the-rise-of-skywalker', sp_search('Star Wars The Rise of Skywalker soundtrack')),
 ('Black Panther: Wakanda Forever', 'Film', OM, 'Ludwig Göransson', 'black-panther-wakanda-forever', sp_search('Black Panther Wakanda Forever score')),
 ('Babylon', 'Film', OM, 'Justin Hurwitz', 'babylon', sp_search('Babylon soundtrack Justin Hurwitz')),
 ('Blue Beetle', 'Film', OM, '', 'blue-beetle', sp_search('Blue Beetle soundtrack')),
 ('White Noise', 'Film', OM, '', 'white-noise', sp_search('White Noise soundtrack')),
 ('Cocaine Bear', 'Film', OM, '', 'cocaine-bear', sp_search('Cocaine Bear soundtrack')),
 ('Chevalier', 'Film', OM, 'Kris Bowers', 'chevalier', sp_search('Chevalier soundtrack Kris Bowers')),
 ('Jerry & Marge Go Large', 'Film', OM, '', 'jerry-and-marge-go-large', sp_search('Jerry and Marge Go Large soundtrack')),
 ('Haunted Mansion', 'Film', OM, 'Kris Bowers', 'haunted-mansion', sp_search('Haunted Mansion 2023 soundtrack')),
 ('Mink!', 'Film', OM, 'Documentary', 'mink-documentary', sp_search('Mink documentary soundtrack')),
 ('Bridgerton', 'Television', OM, 'Kris Bowers', 'bridgerton', sp_search('Bridgerton Kris Bowers')),
 ('The Gilded Age', 'Television', OM, 'Harry & Rupert Gregson-Williams', 'the-gilded-age', sp_search('The Gilded Age soundtrack Gregson-Williams')),
 ('The Mandalorian', 'Television', OM, 'Ludwig Göransson', 'the-mandalorian', sp_search('The Mandalorian original score')),
 ('The Book of Boba Fett', 'Television', OM, '', 'the-book-of-boba-fett', sp_search('The Book of Boba Fett soundtrack')),
 ('Star Trek: Strange New Worlds', 'Television', OM, '', 'star-trek-strange-new-worlds', sp_search('Star Trek Strange New Worlds soundtrack')),
 ('Star Trek: Discovery', 'Television', OM, '', 'star-trek-discovery', sp_search('Star Trek Discovery soundtrack')),
 ('Star Trek: Picard', 'Television', OM, '', 'star-trek-picard', sp_search('Star Trek Picard soundtrack')),
 ('Stargirl', 'Television', OM, '', 'dc-stargirl', sp_search('Stargirl soundtrack')),
 ('The Serpent Queen', 'Television', OM, '', 'the-serpent-queen', sp_search('The Serpent Queen soundtrack')),
 ('Outer Banks', 'Television', OM, '', 'outer-banks', sp_search('Outer Banks soundtrack')),
 ('The Santa Clauses', 'Television', OM, '', 'the-santa-clauses', sp_search('The Santa Clauses soundtrack')),
 ('Frozen Planet II', 'Television', OM, '', 'frozen-planet-ii', sp_search('Frozen Planet II soundtrack')),
 ('Prehistoric Planet 2', 'Television', OM, '', 'prehistoric-planet-2', sp_search('Prehistoric Planet soundtrack')),
 ('The Simpsons', 'Television', OM, '', 'the-simpsons', sp_search('The Simpsons music')),
 ('Bluey', 'Television', OM, '', 'bluey', sp_search('Bluey soundtrack')),
 ('The Wonderful World of Mickey Mouse', 'Television', OM, '', 'the-wonderful-world-of-mickey-mouse', sp_search('The Wonderful World of Mickey Mouse soundtrack')),
 ('American Dad', 'Television', OM, '', 'american-dad', sp_search('American Dad soundtrack')),
 ('Fraggle Rock: Back to the Rock', 'Television', OM, '', 'fraggle-rock-back-to-the-rock', sp_search('Fraggle Rock Back to the Rock')),
 ('T.O.T.S.', 'Television', OM, 'Tiny Ones Transport Service', 'tots-tiny-ones-transport-service', sp_search('T.O.T.S. Disney Junior')),
 ('Mira, Royal Detective', 'Television', OM, '', 'mira-royal-detective', sp_search('Mira Royal Detective soundtrack')),
 ('Cars on the Road', 'Television', OM, '', 'cars-on-the-road', sp_search('Cars on the Road soundtrack')),
 ('Genshin Impact', 'Game', OM, '', 'genshin-impact', sp_search('Genshin Impact soundtrack')),
]
BY = {p[0]: p for p in P}
PHOTO_WIDE = A['conducting-london-symphony-orchestra']
POPULAR = ['Frozen II', 'Star Wars: The Last Jedi', 'Star Wars: The Rise of Skywalker', 'Black Panther: Wakanda Forever', 'The Gilded Age', 'The Book of Boba Fett',
           'Haunted Mansion', 'Star Trek: Strange New Worlds', 'Outer Banks', 'Bluey', 'Star Trek: Discovery', 'Star Trek: Picard',
           'Frozen Planet II', 'The Serpent Queen', 'Cocaine Bear', 'Blue Beetle', 'White Noise', 'Chevalier', 'The Santa Clauses',
           'Prehistoric Planet 2', 'Genshin Impact', 'The Simpsons', 'American Dad', 'Stargirl', 'The Wonderful World of Mickey Mouse',
           'Cars on the Road', 'Fraggle Rock: Back to the Rock', 'Mira, Royal Detective', 'T.O.T.S.', 'Jerry & Marge Go Large', 'Mink!']
GOLD = 'linear-gradient(165deg, #120d07 0%, #4a3315 38%, #b8893c 72%, #f1d9a0 100%)'
RS_URL = 'https://www.rollingstone.com/music/music-features/rosalia-lux-collaborators-making-of-1235470741/'
PRESS = [('Rolling Stone', '‘Art for Art’s Sake’: Rosalía’s Collaborators Reflect on ‘Lux’', 'Gordon on how the LUX orchestrations came about, alongside Daníel Bjarnason, Carminho and Yahritza.', RS_URL),
         ('Dazed', 'Inside Rosalía’s Lux, with its key collaborators', 'Conductor Daníel Bjarnason on the AIR Studios sessions and the orchestrator who prepared them.', 'https://www.dazeddigital.com/music/article/69044/1/lux-rosalia-new-album-2025-noah-dillon-carminho-daniel-bjaranason-yahritza'),
         ('BroadwayWorld', 'Review: BBC Proms, Bond and Beyond', 'Arrangements credited to Kyle Gordon, Barry Forgie, Guy Barker and Nic Raine; Radiohead’s “Spectre” singled out.', 'https://www.broadwayworld.com/article/Review-BBC-PROMS-BOND-AND-BEYOND-Royal-Albert-Hall-20260826'),
         ('Rolling Stone Brasil', '‘Arte pela Arte’: colaboradores de Rosalía refletem sobre ‘Lux’', 'Portuguese edition of the Rolling Stone feature.', 'https://rollingstone.com.br/musica/arte-pela-arte-colaboradores-de-rosalia-refletem-sobre-lux/')]
PROMS = [('2026', 'Bond and Beyond', 'Arranger · organ on Radiohead’s “Spectre”', 'BBC Concert Orchestra · Daniel Bartholomew-Poyser, conductor · 25 August 2026',
          'linear-gradient(160deg, #0b0b0c 0%, #3a3330 45%, #c9a24a 100%)', ('Watch “Spectre” from the organ', 'https://www.instagram.com/kylegordonmusic/reel/Dejq7epTaDR/'), 'BBC Proms · Royal Albert Hall'),
         ('2026', 'The Little Bird', 'Composer · world premiere', 'San Francisco Symphony · Davies Symphony Hall · May 2026',
          'linear-gradient(160deg, #06281f 0%, #1f6b52 48%, #e9d27a 100%)', None, 'San Francisco Symphony'),
         ('2026', 'Marvin Gaye: Prince of Soul', 'Arrangements', 'BBC Concert Orchestra · Edwin Outwater, conductor · 14 August 2026',
          'linear-gradient(160deg, #0f1a3a 0%, #2a4fb8 50%, #f2c36b 100%)', None, 'BBC Proms · Royal Albert Hall'),
         ('2025', 'Soul Revolution', 'Arranger · composer of the finale · organ', 'BBC Concert Orchestra · Daniel Bartholomew-Poyser, conductor · presented by Trevor Nelson · 3 August 2025',
          'linear-gradient(160deg, #2b0f2a 0%, #8e2a5e 45%, #f08a5d 100%)', ('Watch the finale', 'https://www.instagram.com/kylegordonmusic/reel/DM7t0RKo_Ne/'), 'BBC Proms · Royal Albert Hall')]
PHOTO_LUX = A['conducting-london-symphony-orchestra-for-rosalia-lux-lso']

PLAY = '<svg aria-hidden="true" width="12" height="13" viewBox="0 0 12 13"><path d="M1.5 1v11l9.5-5.5z" fill="currentColor"></path></svg>'
ARROW = '<svg aria-hidden="true" width="11" height="11" viewBox="0 0 11 11" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M2 9 9 2M3.5 2H9v5.5"></path></svg>'

CSS = '''.cl{text-decoration:underline;text-underline-offset:5px;text-decoration-thickness:1px}
.cl:hover{text-decoration-thickness:3px}
.cov{position:relative;display:block;overflow:hidden;background:#1b1a17;text-decoration:none}
.cov img{display:block;width:100%;height:100%;object-fit:cover;filter:saturate(1.02) contrast(1.01);transition:filter .45s ease,transform .7s cubic-bezier(.2,.8,.2,1)}
.cov:hover img,.cov:focus-visible img{filter:saturate(1.3) contrast(1.05) brightness(1.03);transform:scale(1.035)}
.cov .play{position:absolute;left:12px;bottom:12px;display:inline-flex;align-items:center;gap:8px;padding:8px 12px 8px 10px;border-radius:999px;background:rgba(247,244,236,.94);color:#1b1a17;opacity:0;transform:translateY(8px);transition:opacity .3s ease,transform .4s cubic-bezier(.2,.8,.2,1);font-family:'DM Mono',ui-monospace,monospace;font-size:11px;text-transform:uppercase;letter-spacing:.04em}
.cov:hover .play,.cov:focus-visible .play{opacity:1;transform:none}
.tile{display:flex;flex-direction:column;gap:12px}
.tile .cov{transition:transform .5s cubic-bezier(.2,.8,.2,1),box-shadow .5s ease}
.tile:hover .cov{transform:translateY(-6px);box-shadow:0 24px 34px -20px rgba(27,26,23,.6)}
.wall{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(118px,30%),1fr));gap:10px}
.wall .cov{aspect-ratio:2/3;overflow:visible;background:none;transform-origin:50% 50%;transition:transform .45s cubic-bezier(.2,.8,.2,1),box-shadow .45s ease,z-index 0s .45s}
.wall .cov img{border-radius:2px}
.wall .cov:hover,.wall .cov:focus-visible{transform:scale(1.22);z-index:3;box-shadow:0 26px 40px -18px rgba(27,26,23,.6);transition:transform .45s cubic-bezier(.2,.8,.2,1),box-shadow .45s ease,z-index 0s}
.wall .cov:hover img,.wall .cov:focus-visible img{transform:none}
.prom{position:relative;display:flex;flex-direction:column;overflow:hidden;background:#1b1a17;color:#fbf8f2}
.prom .face{transition:transform .6s cubic-bezier(.2,.8,.2,1)}
.prom:hover .face{transform:scale(1.04)}
.press{display:flex;flex-direction:column;gap:10px;padding:20px 0;border-top:1px solid rgba(27,26,23,.22);text-decoration:none;color:#1b1a17}
.press .h{transition:color .2s ease}
.press:hover .h{color:#e2581a}
.wall .cov .play{left:8px;bottom:8px;padding:6px 9px 6px 8px;font-size:10px}
.row{position:relative;display:grid;grid-template-columns:48px minmax(0,1.5fr) 120px minmax(0,1.2fr) minmax(0,1fr) 92px;gap:16px;align-items:center;padding:12px 10px;border-top:1px solid rgba(27,26,23,.22);text-decoration:none;color:#1b1a17;transition:background-color .2s ease}
.row:hover{background-color:var(--tint)}
.row .peek{position:absolute;right:120px;top:50%;width:72px;opacity:0;transform:translateY(-50%) rotate(-4deg) scale(.9);transition:opacity .25s ease,transform .4s cubic-bezier(.2,.8,.2,1);pointer-events:none;z-index:2;box-shadow:0 16px 24px -14px rgba(27,26,23,.6)}
.row:hover .peek{opacity:1;transform:translateY(-50%) rotate(-4deg) scale(1)}
.row .go{justify-self:end;display:inline-flex;align-items:center;gap:6px;opacity:1;transition:opacity .2s ease}
.row:hover .go{opacity:1}
.btn{display:inline-flex;align-items:center;gap:10px;min-height:46px;padding:0 20px;border-radius:999px;text-decoration:none;font-family:'DM Mono',ui-monospace,monospace;font-size:12px;text-transform:uppercase;letter-spacing:.04em;transition:background-color .2s ease,color .2s ease,border-color .2s ease}
.btn.solid{background:#1b1a17;color:#f7f4ec;border:1px solid #1b1a17}
.btn.solid:hover{background:#e2581a;border-color:#e2581a}
.btn.line{background:transparent;color:inherit;border:1px solid currentColor}
.btn.line:hover{background:#1b1a17;color:#f7f4ec;border-color:#1b1a17}
@keyframes rise{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:none}}
.rise{animation:rise .9s cubic-bezier(.2,.8,.2,1) both}
@media (max-width: 600px){.luxcard{grid-template-columns:1fr !important}.luxcard>.cov{max-width:280px}}
@media (max-width: 860px){.row{grid-template-columns:36px minmax(0,1fr) 40px}.row .hide{display:none}.row .peek{display:none}}'''


def grain(op=0.38):
    return f'<span class="grain" style="opacity: {op}"></span>'


def band(grad, h=300):
    fade = 'linear-gradient(180deg, #000 0%, #000 42%, rgba(0,0,0,.55) 70%, rgba(0,0,0,.18) 86%, transparent 100%)'
    return (f'<div aria-hidden="true" style="position: absolute; left: 0; right: 0; top: 0; height: {h + 160}px; '
            f'background: linear-gradient(180deg, {grad}); overflow: hidden; '
            f'-webkit-mask-image: {fade}; mask-image: {fade}">{grain()}</div>')


def nav(color, current=''):
    links = [('Work', 'Home.dc.html#work'), ('LUX', 'Project.dc.html'), ('Live', 'Live.dc.html'), ('Credits', 'Home.dc.html#credits'),
             ('About', 'Home.dc.html#about'), ('Work with Kyle', 'WorkWith.dc.html')]
    ls = ''.join(f'<a class="cl" href="{h}" style="padding: 10px 0"{" aria-current=\"page\"" if n == current else ""}>{n}</a>' for n, h in links)
    return (f'<nav aria-label="Primary" style="{WRAP}; padding-top: 22px; display: flex; flex-wrap: wrap; justify-content: space-between; '
            f'gap: 12px 28px; {MONO}; font-size: 12px; color: {color}">'
            f'<a href="Home.dc.html" style="padding: 10px 0; text-decoration: none">Kyle Daniel Gordon</a>'
            f'<span style="display: flex; flex-wrap: wrap; gap: 6px 26px">{ls}</span></nav>')


def cov(title, key, ratio, href, label='Play on Spotify', extra='', grad=None):
    alt = f'{title} poster' if ratio == '2 / 3' else (f'{title} album cover' if ratio == '1 / 1' else f'{title} artwork')
    img = f'<img src="{A[key]}" alt="{alt}" loading="lazy">' if key else ''
    inner = img if key else (f'<span aria-hidden="true" style="position: absolute; inset: 0; background: {grad or G[7]}">{grain(0.42)}</span>'
                             f'<span style="position: absolute; left: 10px; top: 9px; {MONO}; font-size: 9px; color: rgba(251,248,242,.8)">HBO</span>'
                             f'<span style="position: absolute; left: 10px; right: 10px; bottom: 12px; {COND}; font-size: 22px; line-height: .95; color: #fbf8f2">{title}</span>')
    tag = 'a' if href else 'span'
    attrs = f' href="{href}" aria-label="Play {title} on Spotify"' if href else ''
    play = f'<span class="play">{PLAY}{label}</span>' if href else ''
    return f'<{tag} class="cov"{attrs} style="aspect-ratio: {ratio}{extra}">{inner}{play}</{tag}>'


def staff_head(mark, title, meta, sid=''):
    return f'''<div{f' id="{sid}"' if sid else ''} style="display: flex; flex-direction: column; gap: 14px">
<div style="display: flex; flex-wrap: wrap; align-items: center; gap: 10px 16px">
<span aria-hidden="true" style="width: 30px; height: 30px; box-sizing: border-box; border: 1.5px solid {INK}; display: flex; align-items: center; justify-content: center; {MONO}; font-size: 13px; font-weight: 500">{mark}</span>
<h2 style="margin: 0; {SANS}; font-size: clamp(28px, 3vw, 40px); line-height: 1; letter-spacing: -0.04em">{title}</h2>
<span style="margin-left: auto; {MONO}; font-size: 12px; color: {MUTE}">{meta}</span>
</div>
<span aria-hidden="true" style="display: block; height: 33px; background: repeating-linear-gradient(180deg, {INK} 0px, {INK} 1px, rgba(0,0,0,0) 1px, rgba(0,0,0,0) 8px); border-left: 1.5px solid {INK}; border-right: 4px solid {INK}; opacity: 0.85"></span>
</div>'''


def footer(grad):
    return f'''<footer id="contact" style="position: relative; overflow: hidden; margin-top: 150px; padding: 180px 24px 36px; color: #fbf8f2">
<div aria-hidden="true" style="position: absolute; inset: 0; background: linear-gradient(180deg, {PAPER} 0%, {grad}); -webkit-mask-image: linear-gradient(180deg, transparent 0%, rgba(0,0,0,.25) 12%, #000 34%); mask-image: linear-gradient(180deg, transparent 0%, rgba(0,0,0,.25) 12%, #000 34%)">{grain(0.4)}</div>
<div style="position: relative; max-width: 1392px; margin: 0 auto; display: flex; flex-direction: column; gap: 72px">
<div style="display: flex; flex-wrap: wrap; gap: 28px 64px; align-items: flex-end; justify-content: space-between">
<div style="display: flex; flex-direction: column; gap: 10px">
<span style="{MONO}; font-size: 12px; color: {C['celery']}">Contact</span>
<a href="mailto:kylegordonmusic@gmail.com" style="{SANS}; font-size: clamp(30px, 5.4vw, 78px); line-height: 0.95; letter-spacing: -0.045em; text-decoration: none; color: #fbf8f2; overflow-wrap: anywhere">kylegordonmusic@gmail.com</a>
<span style="{MONO}; font-size: 13px">(818) 518-3441 · Los Angeles</span>
</div>
<a class="btn line" href="mailto:kylegordonmusic@gmail.com" style="color: #fbf8f2">Start a project</a>
</div>
<div style="display: flex; flex-wrap: wrap; justify-content: space-between; gap: 12px 28px; {MONO}; font-size: 11px; border-top: 1px solid rgba(251,248,242,0.4); padding-top: 18px">
<span>Kyle Daniel Gordon · Orchestrator, arranger, conductor · Los Angeles</span>
<span style="display: flex; gap: 26px"><a class="cl" href="https://www.instagram.com/kylegordonmusic/" style="padding: 10px 0">Instagram</a><a class="cl" href="https://www.imdb.com/name/nm8773349/" style="padding: 10px 0">IMDb</a><a class="cl" href="https://www.youtube.com/@kylegordonmusic" style="padding: 10px 0">YouTube</a><a class="cl" href="Press.dc.html" style="padding: 10px 0">Press kit</a><a class="cl" href="Privacy.dc.html" style="padding: 10px 0">Privacy</a></span>
</div>
</div>
</footer>'''


def root(inner):
    return (f'<div style="position: relative; background: {PAPER}; color: {INK}; font-family: \'Instrument Sans\', system-ui, sans-serif; '
            f'font-size: 16px; line-height: 1.55; overflow-x: clip">\n<span class="grainm"></span>\n{inner}\n</div>')


def tile(title, sub, ratio, href_title=None):
    t, cat, role, w, key, spot = BY[title]
    name = (f'<a href="{href_title}" class="cl" style="color: {CATCOL[cat]}; text-decoration-color: {CATCOL[cat]}">{title}</a>' if href_title
            else f'<span style="color: {CATCOL[cat]}">{title}</span>')
    return (f'<div class="tile">{cov(t, key, ratio, spot)}'
            f'<div style="display: flex; flex-direction: column; gap: 3px"><h3 style="margin: 0; {COND}; font-size: 26px; line-height: 1.02">{name}</h3>'
            f'<span style="{MONO}; font-size: 11px; color: {MUTE}">{sub}</span></div></div>')


def prom_cards():
    return ''.join(f'''<article class="prom" aria-label="{ven} {y}: {t}">
<div class="face" style="position: relative; aspect-ratio: 4 / 3; background: {g}; overflow: hidden">{grain(0.42)}
<span style="position: absolute; left: 18px; top: 16px; z-index: 1; max-width: 46%; {MONO}; font-size: 11px; line-height: 1.5">{ven}</span>
<span style="position: absolute; right: 16px; top: 4px; {SANS}; font-size: 120px; line-height: 1; letter-spacing: -0.06em; opacity: 0.9">{y[2:]}</span>
<h3 style="position: absolute; left: 18px; right: 18px; bottom: 16px; margin: 0; {COND}; font-size: 38px; line-height: 0.95">{t}</h3>
</div>
<div style="display: flex; flex-direction: column; gap: 8px; padding: 16px 18px 20px">
<span style="font-size: 16px; font-weight: 600">{r}</span>
<span style="{MONO}; font-size: 11px; line-height: 1.5; color: #cfc6b6">{d}</span>
{f'<a href="{v[1]}" style="{MONO}; font-size: 11px; color: {C["celery"]}; padding: 8px 0 0; text-transform: uppercase; letter-spacing: .04em; display: inline-flex; align-items: center; gap: 8px">{PLAY} {v[0]}</a>' if v else ''}
</div></article>''' for y, t, r, d, g, v, ven in PROMS)


AWARDS = [('6', 'Latin Grammys', 'Including Album of the Year, 2026'), ('10', 'Grammy nominations', 'Including Album of the Year, 2027')]


# ------------------------------------------------------------------ HOME
def home():
    posters = ''.join(tile(t, f'{BY[t][1]} · {s}', '2 / 3', 'Oppenheimer.dc.html' if t == 'Oppenheimer' else None) for t, s in
                      [('Oppenheimer', 'Orchestrator'), ('Bridgerton', 'Orchestration'), ('The Mandalorian', 'Orchestration'), ('Babylon', 'Orchestration')])
    recs = ''.join(tile(t, s, '1 / 1') for t, s in
                   [('Romani: The Untold Story', 'Billboard #1 Classical Album, 2024'), ('Baby Shark 10th Anniversary', 'London Symphony Orchestra'),
                    ('Grace Kelly with Strings: At The Movies', 'Arranger, orchestrator, co-producer'), ('People Pleaser', 'Mollie Elizabeth · arranger, 2026')])
    wall = ''.join(cov(t, BY[t][4], '2 / 3', BY[t][5], 'Play', grad=GOLD) for t in POPULAR)
    proms = prom_cards()
    press = ''.join(f'''<a class="press" href="{u}"><span style="{MONO}; font-size: 11px; color: {MUTE}">{o}</span>
<span class="h" style="{SANS}; font-size: 22px; line-height: 1.2; letter-spacing: -0.02em">{h} {ARROW}</span>
<span style="font-size: 15px; line-height: 1.45; color: #3a362f">{dsc}</span></a>''' for o, h, dsc, u in PRESS)
    rows = ''
    for n, (t, cat, role, w, key, spot) in enumerate(P):
        peek = f'<span class="peek" aria-hidden="true"><img src="{A[key]}" alt="" style="display: block; width: 100%"></span>' if key else ''
        go = f'<span class="go" style="{MONO}; font-size: 11px">{PLAY}{"Watch" if "instagram" in spot else "Listen"}</span>' if spot else f'<span class="go" style="{MONO}; font-size: 11px; color: {MUTE}">Broadcast</span>'
        tag, attr = ('a', f' href="{spot}"') if spot else ('div', '')
        rows += (f'<{tag}{attr} class="row" style="--tint: {TINT[cat]}">'
                 f'<span style="{MONO}; font-size: 11px; font-variant-numeric: tabular-nums; color: {MUTE}">{n + 1:02d}</span>'
                 f'<span style="{COND}; font-size: clamp(22px, 2.2vw, 30px); line-height: 1">{t}</span>'
                 f'<span class="hide" style="{MONO}; font-size: 11px; color: {CATCOL[cat]}">{cat}</span>'
                 f'<span class="hide" style="{MONO}; font-size: 11px">{role}</span>'
                 f'<span class="hide" style="{MONO}; font-size: 11px; color: {MUTE}">{w}</span>{go}{peek}</{tag}>\n')
    aw = ''.join(f'''<div style="display: flex; align-items: baseline; gap: 14px; padding: 14px 0; border-top: 1px solid {RULE}">
<span style="{SANS}; font-size: 44px; line-height: 0.9; letter-spacing: -0.05em; font-variant-numeric: tabular-nums">{a}</span>
<span style="display: flex; flex-direction: column"><span style="font-size: 16px; font-weight: 600">{b}</span><span style="{MONO}; font-size: 11px; color: {MUTE}">{c}</span></span></div>''' for a, b, c in AWARDS)
    inner = f'''<header style="position: relative">
{band('#120d0b 0%, #4a1a12 22%, #b4461a 46%, #e9a36f 70%', 320)}
{nav('#f3e7cf')}
<div style="{WRAP}; padding-top: 240px; display: grid; grid-template-columns: repeat(auto-fit, minmax(min(440px, 100%), 1fr)); gap: 56px 72px; align-items: end">
<div class="rise" style="display: flex; flex-direction: column; gap: 22px">
<h1 style="margin: 0 0 0 -0.045em; {SANS}; font-size: clamp(64px, 10.4vw, 150px); line-height: 0.86; letter-spacing: -0.055em">Kyle Daniel<br>Gordon</h1>
<p style="margin: 0; font-size: clamp(18px, 1.6vw, 21px); line-height: 1.4; max-width: 38ch; color: #2f2c27">Orchestrator, arranger and conductor. Orchestral and string arrangements for pop artists, film and television, from Rosalía’s <em>LUX</em> to <em>Oppenheimer</em>. Based in Los Angeles.</p>
</div>
<article aria-labelledby="lux-h" class="rise luxcard" style="animation-delay: .15s; display: grid; grid-template-columns: minmax(0, 200px) minmax(0, 1fr); gap: 22px; align-items: start">
{cov('LUX', 'rosalia-lux-album', '1 / 1', BY['LUX'][5])}
<div style="display: flex; flex-direction: column; gap: 10px">
<span style="{MONO}; font-size: 11px; color: #b5410b">Supervising orchestrator · Rosalía · 2025</span>
<h2 id="lux-h" style="margin: 0; {COND}; font-size: 46px; line-height: 0.92">Rosalía — LUX</h2>
<p style="margin: 0; font-size: 15px; line-height: 1.45; color: #2f2c27">Supervising orchestrator on Rosalía's fourth album, recorded with the London Symphony Orchestra at AIR Studios, London.</p>
<div style="display: flex; flex-direction: column">{aw}</div>
<div style="display: flex; flex-wrap: wrap; gap: 10px; padding-top: 6px"><a class="btn solid" href="{BY['LUX'][5]}">{PLAY}Listen</a><a class="btn line" href="Project.dc.html">About the record</a></div>
</div>
</article>
</div>
</header>

<section aria-label="Orchestras and composers" style="{WRAP}; margin-top: 110px">
<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(min(420px, 100%), 1fr)); gap: 28px 72px; padding: 24px 0; border-top: 1px solid {INK}; border-bottom: 1px solid {INK}">
<div style="display: flex; flex-direction: column; gap: 8px"><span style="{MONO}; font-size: 11px; color: {MUTE}">Orchestras</span><p style="margin: 0; {COND}; font-size: 24px; line-height: 1.15; color: #1d6fc4">London Symphony Orchestra · New York Philharmonic · San Francisco Symphony · BBC Concert Orchestra · Seattle Symphony · National Arts Centre Orchestra</p></div>
<div style="display: flex; flex-direction: column; gap: 8px"><span style="{MONO}; font-size: 11px; color: {MUTE}">Orchestration teams for</span><p style="margin: 0; {COND}; font-size: 24px; line-height: 1.15; color: {C['mag']}">John Williams · Ludwig Göransson · Kris Bowers · Walter Murphy · Justin Hurwitz</p></div>
</div>
</section>

<figure style="position: relative; margin: 110px 0 0; padding: 0">
<img src="{PHOTO_WIDE}" alt="Kyle Daniel Gordon conducting the London Symphony Orchestra in the recording studio" style="display: block; width: 100%; height: clamp(320px, 50vw, 700px); object-fit: cover; filter: saturate(.9) sepia(.06)">
<figcaption style="{WRAP}; padding-top: 12px; display: flex; flex-wrap: wrap; justify-content: space-between; gap: 8px; {MONO}; font-size: 11px; color: {MUTE}"><span>With the London Symphony Orchestra</span><span>Fig. 1</span></figcaption>
</figure>

<section id="work" aria-label="Selected work" style="{WRAP}; margin-top: 140px; display: flex; flex-direction: column; gap: 44px">
{staff_head('A', 'Film &amp; television', 'Selected')}
<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(min(240px, 100%), 1fr)); gap: 44px 28px">
{posters}</div>
{staff_head('B', 'Records', 'Selected')}
<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(min(240px, 100%), 1fr)); gap: 44px 28px">
{recs}</div>
</section>

<section id="live" aria-label="Live" style="{WRAP}; margin-top: 140px; display: flex; flex-direction: column; gap: 36px">
{staff_head('C', 'Live', '<a class="cl" href="Live.dc.html" style="padding: 10px 0">BBC Proms · San Francisco Symphony →</a>')}
<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(min(300px, 100%), 1fr)); gap: 24px">
{proms}</div>
</section>

<section id="press" aria-label="Press" style="{WRAP}; margin-top: 140px; display: grid; grid-template-columns: repeat(auto-fit, minmax(min(440px, 100%), 1fr)); gap: 40px 80px; align-items: start">
<a href="{RS_URL}" style="display: flex; flex-direction: column; gap: 22px; text-decoration: none; color: {INK}">
<span style="{MONO}; font-size: 12px; color: #b5410b">In Rolling Stone</span>
<span style="{SANS}; font-size: clamp(36px, 4.4vw, 64px); line-height: 1; letter-spacing: -0.045em">“Known for the <em style="font-family: 'Instrument Serif', Georgia, serif; font-weight: 400">Oppenheimer</em> and <em style="font-family: 'Instrument Serif', Georgia, serif; font-weight: 400">Bridgerton</em> soundtracks.”</span>
<span style="font-size: 17px; line-height: 1.45; color: #3a362f; max-width: 46ch">Rolling Stone’s feature on the making of <em>LUX</em> names Kyle Daniel Gordon as the album’s orchestrator. In it he describes getting the call from the London Symphony Orchestra.</span>
<span class="btn line" style="align-self: flex-start">Read the feature {ARROW}</span>
</a>
<div style="display: flex; flex-direction: column">
<span style="{MONO}; font-size: 12px; color: {MUTE}; padding-bottom: 12px">Press</span>
{press}<span style="border-top: 1px solid {RULE}"></span>
</div>
</section>

<section aria-label="More film and television" style="{WRAP}; margin-top: 140px; display: flex; flex-direction: column; gap: 32px">
{staff_head('D', 'Also on screen', 'Most watched first · hover to play')}
<div class="wall">
{wall}</div>
</section>

<section id="credits" aria-label="Full credits" style="{WRAP}; margin-top: 140px; display: flex; flex-direction: column; gap: 28px">
{staff_head('E', 'Credits', f'{len(P)} projects')}
<div>
<div aria-hidden="true" class="row" style="border-top: 0; padding-top: 0; padding-bottom: 10px; {MONO}; font-size: 10px; color: {MUTE}"><span>No.</span><span>Title</span><span class="hide">Category</span><span class="hide">Role</span><span class="hide">With</span><span></span></div>
{rows}</div>
</section>

<section id="about" aria-label="About" style="{WRAP}; margin-top: 150px; display: flex; flex-direction: column; gap: 44px">
{staff_head('F', 'About', 'Los Angeles')}
<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(min(420px, 100%), 1fr)); gap: 44px 80px; align-items: start">
<figure style="margin: 0; display: flex; flex-direction: column; gap: 10px"><img src="{PHOTO_LUX}" alt="Kyle Daniel Gordon with the London Symphony Orchestra during the LUX sessions" loading="lazy" style="display: block; width: 100%; aspect-ratio: 4 / 5; object-fit: cover; object-position: 50% 40%"><figcaption style="{MONO}; font-size: 11px; color: {MUTE}">LUX sessions, London Symphony Orchestra</figcaption></figure>
<div style="display: flex; flex-direction: column; gap: 18px; font-size: 18px; line-height: 1.55; max-width: 62ch">
<p style="margin: 0">Kyle Daniel Gordon is an orchestrator, arranger and conductor based in Los Angeles. He was supervising orchestrator on Rosalía's <em>LUX</em>, recorded with the London Symphony Orchestra, which won six Latin Grammys including Album of the Year and received ten Grammy nominations.</p>
<p style="margin: 0; color: #3a362f">In film and television he orchestrated <em>Oppenheimer</em> and <em>Bridgerton</em>, and has worked in the music departments of <em>The Mandalorian</em>, <em>Black Panther: Wakanda Forever</em> and <em>Star Wars: The Rise of Skywalker</em>. He leads orchestration teams in Los Angeles for composers including John Williams, Ludwig Göransson, Kris Bowers, Walter Murphy and Justin Hurwitz.</p>
<p style="margin: 0; color: #3a362f">At the BBC Proms he was lead orchestrator on <em>Soul Revolution</em> (2025) with the BBC Concert Orchestra, writing its finale and playing the Royal Albert Hall organ. In 2026 he arranged the <em>Bond and Beyond</em> Prom, performing his arrangement of Radiohead’s “Spectre” on the organ, and wrote arrangements for <em>Marvin Gaye: Prince of Soul</em>. His piece <em>The Little Bird</em> was premiered by the San Francisco Symphony in 2026. He arranged, orchestrated and conducted the <em>Baby Shark 10th Anniversary</em> symphonic album with the LSO. <em>Romani: The Untold Story</em>, which he orchestrated and conducted with the LSO and Dallas String Quartet, received the 2024 Billboard Award for #1 Classical Album. He has conducted sessions and concerts in Los Angeles, Nashville and London, and arranged touring orchestral shows for Hawthorne Heights and Escape the Fate.</p>
<p style="margin: 0; color: #3a362f">Trained in jazz and classical music, he holds a master's in music from the University of North Texas, and made his Carnegie Hall debut as a bassist in 2018. He is also credited as Kyle Gordon.</p>

</div>
</div>
</section>

{footer('#d6a98c 30%, #b8456e 62%, #3e0c1f 100%')}'''
    return page('Kyle Daniel Gordon, orchestrator of Rosalía LUX and Oppenheimer, pop strings', root(inner), CSS, PAPER, h=9600)


# ------------------------------------------------------------------ LUX PROJECT
def lux():
    tracks = ['Sexo, Violencia y Llantas', 'Reliquia', 'Divinize', 'Porcelana', 'Mio Cristo Piange Diamanti', 'Berghain', 'La Perla',
              'Mundo Nuevo', 'De Madrugá', 'Dios Es Un Stalker', 'La Yugular', 'Sauvignon Blanc', 'La Rumba Del Perdón', 'Memória', 'Magnolias']
    tl = ''.join(f'<li style="display: grid; grid-template-columns: 34px minmax(0, 1fr); gap: 10px; padding: 9px 0; border-top: 1px solid {RULE}">'
                 f'<span style="{MONO}; font-size: 11px; color: {MUTE}; font-variant-numeric: tabular-nums">{i + 1:02d}</span><span>{t}</span></li>' for i, t in enumerate(tracks))
    spec = [('Artist', 'Rosalía'), ('Album', 'LUX (2025) · LUX (Complete Works)'), ('Supervising orchestrator', 'Kyle Daniel Gordon'),
            ('Orchestra', 'London Symphony Orchestra'), ('Conductor', 'Daníel Bjarnason'), ('Recorded', 'AIR Studios, London'),
            ('Label', 'Columbia Records')]
    sp = ''.join(f'<dt style="padding: 11px 18px 11px 0; color: {MUTE}; border-top: 1px solid {RULE}">{a}</dt><dd style="margin: 0; padding: 11px 0; border-top: 1px solid {RULE}">{b}</dd>' for a, b in spec)
    big = ''.join(f'''<div style="display: flex; flex-direction: column; gap: 6px; padding-top: 16px; border-top: 1.5px solid {INK}">
<span style="{SANS}; font-size: clamp(80px, 11vw, 150px); line-height: 0.82; letter-spacing: -0.06em; font-variant-numeric: tabular-nums">{a}</span>
<span style="font-size: 20px; font-weight: 600; letter-spacing: -0.02em">{b}</span><span style="{MONO}; font-size: 12px; color: {MUTE}">{c}</span></div>''' for a, b, c in
                  [('6', 'Latin Grammys', 'Album of the Year, Song of the Year (“La Perla”), Best Alternative Music Album and more · 27th Latin Grammy Awards, 2026'),
                   ('10', 'Grammy nominations', 'Including Album of the Year · 69th Grammy Awards, 2027')])
    inner = f'''<header style="position: relative">
{band('#0f0e10 0%, #3b3a40 22%, #a7a3a0 48%, #e9e4da 74%', 320)}
{nav('#f2efe8', 'LUX')}
<div style="{WRAP}; padding-top: 230px; display: grid; grid-template-columns: repeat(auto-fit, minmax(min(460px, 100%), 1fr)); gap: 48px 80px; align-items: start">
<div class="rise" style="display: flex; flex-direction: column; gap: 22px">
<span style="{MONO}; font-size: 12px; color: {MUTE}"><a class="cl" href="Home.dc.html#work" style="padding: 10px 0">Work</a> / Records / Rosalía <span aria-hidden="true">·</span> <a class="cl" href="ProjectES.dc.html" hreflang="es" lang="es" style="padding: 10px 0">Español</a></span>
<h1 style="margin: 0; display: flex; flex-direction: column; gap: 6px"><span style="{MONO}; font-size: 14px; font-weight: 400">Rosalía</span><span style="{COND}; font-size: clamp(96px, 15vw, 220px); line-height: 0.8; color: {INK}">LUX</span></h1>
<p style="margin: 0; {MONO}; font-size: 15px; line-height: 1.45; max-width: 40ch">Orchestrations for an album sung in thirteen languages, with the London Symphony Orchestra on every track.</p>
<p style="margin: 0; font-size: 17px; max-width: 58ch">LUX is Rosalía's fourth studio album, released in November 2025. Kyle Daniel Gordon was the album’s supervising orchestrator. The album was recorded with the London Symphony Orchestra at AIR Studios in London, conducted by Daníel Bjarnason.</p>
<p style="margin: 0; font-size: 17px; max-width: 58ch; color: #3a362f">LUX won six Latin Grammys at the 27th Latin Grammy Awards, including Album of the Year, and received ten nominations at the 69th Grammy Awards, including Album of the Year.</p>
<a href="{RS_URL}" class="press" style="margin-top: 8px; border-top: 2px solid {C['tang']}"><span style="{MONO}; font-size: 11px; color: #b5410b">Rolling Stone</span>
<span class="h" style="{SANS}; font-size: 22px; line-height: 1.25; letter-spacing: -0.02em">‘Art for Art’s Sake’: Rosalía’s Collaborators Reflect on ‘Lux’ {ARROW}</span>
<span style="font-size: 15px; color: #3a362f">Gordon tells the story of the call from the London Symphony Orchestra that brought him onto the album.</span></a>
</div>
<div class="rise" style="animation-delay: .15s; display: flex; flex-direction: column; gap: 22px">
{cov('LUX', 'rosalia-lux-album', '1 / 1', BY['LUX'][5])}
<div style="display: flex; flex-wrap: wrap; gap: 10px"><a class="btn solid" href="{BY['LUX'][5]}">{PLAY}Listen on Spotify</a></div>
<dl style="margin: 0; display: grid; grid-template-columns: max-content minmax(0, 1fr); {MONO}; font-size: 12px; border-bottom: 1px solid {RULE}">{sp}</dl>
</div>
</div>
</header>

<section aria-label="Recognition" style="{WRAP}; margin-top: 130px; display: flex; flex-direction: column; gap: 40px">
{staff_head('A', 'Recognition', 'LUX')}
<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(min(380px, 100%), 1fr)); gap: 40px 56px">{big}</div>
</section>

<figure style="position: relative; margin: 130px 0 0; padding: 0">
<img src="{PHOTO_LUX}" alt="Kyle Daniel Gordon with the London Symphony Orchestra during the recording of Rosalía's LUX" loading="lazy" style="display: block; width: 100%; height: clamp(360px, 56vw, 760px); object-fit: cover; object-position: 50% 35%">
<figcaption style="{WRAP}; padding-top: 12px; display: flex; flex-wrap: wrap; justify-content: space-between; gap: 8px; {MONO}; font-size: 11px; color: {MUTE}"><span>LUX sessions with the London Symphony Orchestra</span><span>Fig. 2</span></figcaption>
</figure>

<section aria-label="Tracklist" style="{WRAP}; margin-top: 130px; display: grid; grid-template-columns: repeat(auto-fit, minmax(min(420px, 100%), 1fr)); gap: 40px 80px; align-items: start">
<div style="display: flex; flex-direction: column; gap: 18px">
{staff_head('B', 'Tracklist', 'LUX · 15 tracks')}
<p style="margin: 0; font-size: 16px; color: #3a362f; max-width: 44ch">The London Symphony Orchestra plays on every song. LUX (Complete Works) adds three more.</p>
<a class="btn line" href="{BY['LUX'][5]}" style="align-self: flex-start">{PLAY}Play the album</a>
</div>
<ol style="margin: 0; padding: 0; list-style: none; font-size: 17px; border-bottom: 1px solid {RULE}">{tl}</ol>
</section>

<section aria-label="Next project" style="{WRAP}; margin-top: 140px">
<div style="display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 18px 40px; border-top: 1px solid {INK}; padding-top: 22px">
<span style="{MONO}; font-size: 12px; color: {MUTE}">Next — Film</span>
<span style="display: flex; align-items: center; gap: 24px">{cov('Oppenheimer', 'oppenheimer-film-poster', '2 / 3', BY['Oppenheimer'][5], 'Play', '; width: 84px')}<a href="Home.dc.html#work" class="cl" style="{COND}; font-size: clamp(48px, 7vw, 100px); line-height: 0.9; color: {C['tang']}; text-decoration-color: {C['tang']}">Oppenheimer →</a></span>
</div>
</section>

{footer('#a7a3a0 30%, #3b3a40 62%, #0f0e10 100%')}'''
    return page('Rosalía LUX orchestrations, Kyle Daniel Gordon', root(inner), CSS, PAPER, h=4700)


# ------------------------------------------------------------------ WORK WITH
def workwith():
    caps = [('Orchestration', ['Full orchestration from mockups, sketches and lead sheets', 'Lead orchestrator and orchestration team lead',
                               'Score preparation and parts', 'Film, television, games and records']),
            ('Pop strings', ['String and orchestral arrangements for pop artists', 'Symphonic albums and reimaginings',
                             'Orchestral shows: BBC Proms, touring bands', 'Co-production']),
            ('Conducting', ['Recording sessions', 'Live concerts', 'Los Angeles, Nashville and London', 'Trained in jazz and classical'])]
    cap = ''.join(f'''<div style="display: flex; flex-direction: column; gap: 16px; padding-top: 18px; border-top: 1.5px solid {INK}">
<span style="{MONO}; font-size: 12px; color: {MUTE}">0{i + 1}</span>
<h3 style="margin: 0; {COND}; font-size: clamp(40px, 4.4vw, 60px); line-height: 0.92; color: {['#2271c3', C['mag'], C['tang']][i]}">{f'<a href="PopStrings.dc.html" class="cl">{h}</a>' if h == 'Pop strings' else h}</h3>
<ul style="margin: 0; padding: 0; list-style: none; {MONO}; font-size: 12px">{''.join(f'<li style="padding: 9px 0; border-top: 1px solid {RULE}">{x}</li>' for x in items)}</ul>
</div>''' for i, (h, items) in enumerate(caps))
    steps = [('Sketch to score', 'A mockup, sketch or demo becomes a full score written for the players in the room, in the composer’s voice.'),
             ('Score to stand', 'Scores and parts are proofed and delivered before the session, so studio time goes to the music.'),
             ('Stand to session', 'On the podium or in the booth, keeping the session on schedule and the takes clean.')]
    st = ''.join(f'''<div style="display: flex; flex-direction: column; gap: 12px; padding-top: 18px; border-top: 1px solid {RULE}">
<span style="{MONO}; font-size: 12px">0{i + 1}</span>
<h3 style="margin: 0; {SANS}; font-size: clamp(26px, 2.6vw, 34px); line-height: 1; letter-spacing: -0.04em">{h}</h3>
<p style="margin: 0; font-size: 16px; line-height: 1.5; color: #3a362f">{p}</p>
</div>''' for i, (h, p) in enumerate(steps))
    strip = ''.join(cov(t, BY[t][4], '1 / 1' if BY[t][1] == 'Record' else '2 / 3', BY[t][5], 'Play')
                    for t in ['LUX', 'Oppenheimer', 'Bridgerton', 'Romani: The Untold Story', 'The Mandalorian', 'Baby Shark 10th Anniversary'])
    inner = f'''<header style="position: relative">
{band('#120f22 0%, #3b2a6a 24%, #8a76c9 50%, #cdc8ef 74%', 320)}
{nav('#ece8ff', 'Work with Kyle')}
<div style="{WRAP}; padding-top: 230px; display: grid; grid-template-columns: repeat(auto-fit, minmax(min(420px, 100%), 1fr)); gap: 48px 80px; align-items: start">
<div class="rise" style="display: flex; flex-direction: column; gap: 24px">
<h1 style="margin: 0; {COND}; font-size: clamp(72px, 10vw, 150px); line-height: 0.84; color: {C['sky']}">Work<br>with<br>Kyle</h1>
<p style="margin: 0; font-size: 20px; line-height: 1.45; max-width: 46ch">Orchestration, pop string arrangements and conducting for composers, artists and labels, from first sketch to final session.</p>
<p style="margin: 0; font-size: 17px; max-width: 58ch; color: #3a362f">Recent work includes the orchestrations for Rosalía's LUX with the London Symphony Orchestra, orchestration on Oppenheimer and Bridgerton, and arrangements for the BBC Proms. Projects can start at any stage: a mockup that needs a full score, an album that needs an orchestra, or a session that needs a conductor.</p>
<div style="display: flex; flex-wrap: wrap; gap: 10px"><a class="btn solid" href="mailto:kylegordonmusic@gmail.com">Email Kyle</a><a class="btn line" href="Home.dc.html#credits">See all credits</a></div>
</div>
<figure class="rise" style="animation-delay: .15s; margin: 0; display: flex; flex-direction: column; gap: 10px"><img src="{PHOTO_LUX}" alt="Kyle Daniel Gordon conducting the London Symphony Orchestra" style="display: block; width: 100%; aspect-ratio: 4 / 5; object-fit: cover; object-position: 50% 40%"><figcaption style="{MONO}; font-size: 11px; color: {MUTE}">London Symphony Orchestra, LUX sessions</figcaption></figure>
</div>
</header>

<section aria-label="Capabilities" style="position: relative; margin-top: 140px; background: {C['tang']}; overflow: hidden; padding: 70px 0 80px">
{grain(0.3)}
<div style="{WRAP}; display: flex; flex-direction: column; gap: 52px">
<h2 style="margin: 0; {COND}; font-weight: 900; font-size: clamp(80px, 15vw, 230px); line-height: 0.8; color: {C['celery']}; text-align: center">Capabilities</h2>
<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(min(300px, 100%), 1fr)); gap: 40px 32px; background: {PAPER}; padding: 36px 32px 40px">
{cap}</div>
</div>
</section>

<section aria-label="How I work" style="{WRAP}; margin-top: 140px; display: flex; flex-direction: column; gap: 44px">
{staff_head('A', 'How a project runs', 'Any stage')}
<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(min(300px, 100%), 1fr)); gap: 40px">
{st}</div>
</section>

<section aria-label="Recent work" style="{WRAP}; margin-top: 140px; display: flex; flex-direction: column; gap: 32px">
{staff_head('B', 'Recent work', 'Hover to play')}
<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(min(150px, 45%), 1fr)); gap: 14px; align-items: end">
{strip}</div>
</section>

{footer('#8a76c9 30%, #3b2a6a 62%, #120f22 100%')}'''
    return page('Work with Kyle Daniel Gordon', root(inner), CSS, PAPER, h=4300)


# ------------------------------------------------------------------ EXTRA PAGES (SEO)
def crumbs(*parts):
    links = ' / '.join(parts)
    return f'<span style="{MONO}; font-size: 12px; color: {MUTE}">{links}</span>'


def spec(rows):
    sp = ''.join(f'<dt style="padding: 11px 18px 11px 0; color: {MUTE}; border-top: 1px solid {RULE}">{a}</dt><dd style="margin: 0; padding: 11px 0; border-top: 1px solid {RULE}">{b}</dd>' for a, b in rows)
    return f'<dl style="margin: 0; display: grid; grid-template-columns: max-content minmax(0, 1fr); {MONO}; font-size: 12px; border-bottom: 1px solid {RULE}">{sp}</dl>'


def hero_title(kicker, big, size='clamp(76px, 12vw, 190px)'):
    return (f'<h1 style="margin: 0; display: flex; flex-direction: column; gap: 6px"><span style="{MONO}; font-size: 14px; font-weight: 400">{kicker}</span>'
            f'<span style="{COND}; font-size: {size}; line-height: 0.86; letter-spacing: -0.01em">{big}</span></h1>')


def next_link(label, title, href):
    return f'''<section aria-label="Next" style="{WRAP}; margin-top: 140px">
<div style="display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 18px 40px; border-top: 1px solid {INK}; padding-top: 22px">
<span style="{MONO}; font-size: 12px; color: {MUTE}">{label}</span>
<a href="{href}" class="cl" style="{COND}; font-size: clamp(34px, 5vw, 64px); line-height: 1">{title}</a>
</div></section>'''


def oppenheimer():
    o = BY['Oppenheimer']
    more = ''.join(tile(t, s, '2 / 3') for t, s in [('Black Panther: Wakanda Forever', 'Ludwig Göransson · orchestration'),
                                                    ('The Mandalorian', 'Ludwig Göransson · orchestration')]
                   if t in BY)
    inner = f'''<header style="position: relative">
{band('#050302 0%, #3a1406 24%, #c2521a 50%, #efc9a0 76%', 320)}
{nav('#f6e8d8')}
<div style="{WRAP}; padding-top: 230px; display: grid; grid-template-columns: repeat(auto-fit, minmax(min(460px, 100%), 1fr)); gap: 48px 80px; align-items: start">
<div class="rise" style="display: flex; flex-direction: column; gap: 22px">
{crumbs('<a class="cl" href="Home.dc.html#work" style="padding: 10px 0">Work</a>', 'Film', 'Oppenheimer')}
{hero_title('Christopher Nolan · 2023', 'Oppenheimer', 'clamp(56px, 8vw, 128px)')}
<p style="margin: 0; {MONO}; font-size: 15px; line-height: 1.45; max-width: 42ch">Orchestration on Ludwig Göransson’s Academy Award-winning score.</p>
<p style="margin: 0; font-size: 17px; max-width: 58ch">Kyle Daniel Gordon was an orchestrator on Ludwig Göransson’s score for <em>Oppenheimer</em>, Christopher Nolan’s 2023 film about J. Robert Oppenheimer. The score won the Academy Award for Best Original Score.</p>
<p style="margin: 0; font-size: 17px; max-width: 58ch; color: #3a362f">Nolan asked for a score led by the solo violin, which he heard as Oppenheimer’s own voice. Around two and a half hours of music runs through the three-hour film, and the orchestra recorded it in five days.</p>
<div style="display: flex; flex-wrap: wrap; gap: 10px; margin-top: 6px"><a class="btn solid" href="{o[5]}">{PLAY}Listen on Spotify</a><a class="btn line" href="WorkWith.dc.html">Work with Kyle</a></div>
</div>
<div class="rise" style="animation-delay: .15s; display: flex; flex-direction: column; gap: 22px; max-width: 460px">
{cov('Oppenheimer', o[4], '2 / 3', o[5])}
{spec([('Film', 'Oppenheimer (2023)'), ('Director', 'Christopher Nolan'), ('Composer', 'Ludwig Göransson'), ('Orchestration', 'Kyle Daniel Gordon'), ('Studio', 'Universal Pictures'), ('Recognition', 'Academy Award, Best Original Score')])}
</div>
</div>
</header>

<section aria-label="With Ludwig Göransson" style="{WRAP}; margin-top: 130px; display: flex; flex-direction: column; gap: 32px">
{staff_head('A', 'More with Ludwig Göransson', 'Film &amp; television')}
<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(min(200px, 46%), 1fr)); gap: 32px 24px">{more}</div>
</section>

{next_link('Next — Record', 'Rosalía · LUX', 'Project.dc.html')}

{footer('#c2521a 30%, #3a1406 62%, #050302 100%')}'''
    return page('Oppenheimer orchestration, Kyle Daniel Gordon', root(inner), CSS, PAPER, h=3600)


def live():
    reviews = ''.join(f'''<a class="press" href="{u}"><span style="{MONO}; font-size: 11px; color: {MUTE}">{o}</span>
<span class="h" style="{SANS}; font-size: 22px; line-height: 1.2; letter-spacing: -0.02em">{h} {ARROW}</span>
<span style="font-size: 15px; line-height: 1.45; color: #3a362f">{dsc}</span></a>''' for o, h, dsc, u in PRESS if 'Proms' in h)
    shows = ''.join(tile(t, s, '1 / 1') for t, s in [('Hawthorne Heights', 'Orchestral show · arranger'), ('Escape the Fate', 'Orchestral show · arranger')] if t in BY and BY[t][4])
    inner = f'''<header style="position: relative">
{band('#2b0f2a 0%, #8e2a5e 26%, #f08a5d 52%, #f4dcc4 76%', 320)}
{nav('#fbeee6', 'Live')}
<div style="{WRAP}; padding-top: 230px; display: flex; flex-direction: column; gap: 22px" class="rise">
{crumbs('<a class="cl" href="Home.dc.html" style="padding: 10px 0">Home</a>', 'Live')}
{hero_title('BBC Proms · San Francisco Symphony', 'Live')}
<p style="margin: 0; {MONO}; font-size: 15px; line-height: 1.45; max-width: 52ch">Arrangements, new music and the occasional turn at the Royal Albert Hall organ.</p>
<p style="margin: 0; font-size: 17px; max-width: 64ch">At the BBC Proms, Kyle Daniel Gordon was lead orchestrator on <em>Soul Revolution</em> (2025) with the BBC Concert Orchestra, writing its finale and playing the Royal Albert Hall organ. In 2026 he arranged for <em>Bond and Beyond</em>, performing his arrangement of Radiohead’s “Spectre” on the organ, and contributed arrangements to <em>Marvin Gaye: Prince of Soul</em>. His piece <em>The Little Bird</em> was premiered by the San Francisco Symphony in May 2026.</p>
</div>
</header>

<section aria-label="Concerts" style="{WRAP}; margin-top: 110px; display: flex; flex-direction: column; gap: 32px">
{staff_head('A', 'Concerts', 'Newest first')}
<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(min(300px, 100%), 1fr)); gap: 18px">{prom_cards()}</div>
</section>

<section aria-label="Reviews" style="{WRAP}; margin-top: 120px; display: grid; grid-template-columns: repeat(auto-fit, minmax(min(420px, 100%), 1fr)); gap: 32px 80px; align-items: start">
{staff_head('B', 'Reviews', 'Press')}
<div style="display: flex; flex-direction: column">{reviews}</div>
</section>

{next_link('Hire for a concert', 'Work with Kyle', 'WorkWith.dc.html')}

{footer('#f08a5d 30%, #8e2a5e 62%, #2b0f2a 100%')}'''
    return page('Live: BBC Proms arrangements and premieres, Kyle Daniel Gordon', root(inner), CSS, PAPER, h=3400)


def popstrings():
    recs = ''.join(tile(t, s, '1 / 1', 'Project.dc.html' if t == 'LUX' else None) for t, s in
                   [('LUX', 'Rosalía · supervising orchestrator · LSO'), ('People Pleaser', 'Mollie Elizabeth · arranger'),
                    ('Grace Kelly with Strings: At The Movies', 'Arranger, orchestrator, co-producer'), ('Magia en Dos', 'Ariza · orchestrator'),
                    ('Baby Shark 10th Anniversary', 'London Symphony Orchestra'), ('Romani: The Untold Story', 'Billboard #1 Classical Album')])
    steps = ''.join(f'''<li style="display: grid; grid-template-columns: 44px minmax(0, 1fr); gap: 14px; padding: 18px 0; border-top: 1px solid {RULE}">
<span style="{MONO}; font-size: 12px; color: {MUTE}">0{i + 1}</span><span style="display: flex; flex-direction: column; gap: 4px"><strong style="font-size: 18px; letter-spacing: -0.01em">{a}</strong><span style="color: #3a362f">{b}</span></span></li>''' for i, (a, b) in enumerate([
        ('Send the song', 'A demo, stems or a rough mix is enough. Tell him the size: a string quartet, a section, or a full orchestra.'),
        ('Arrangement', 'Strings written to sit around the vocal and the production, with mockups to sign off before anyone plays a note.'),
        ('Session', 'Players booked and parts prepared for Los Angeles, Nashville or London (AIR, Abbey Road), or for remote recording.'),
        ('Stage', 'The same charts adapted for live shows, from a string section on tour to a symphony orchestra.')]))
    inner = f'''<header style="position: relative">
{band('#0e1a12 0%, #31502c 24%, #a8b85a 50%, #eef0cf 76%', 320)}
{nav('#f1f4e0')}
<div style="{WRAP}; padding-top: 230px; display: grid; grid-template-columns: repeat(auto-fit, minmax(min(460px, 100%), 1fr)); gap: 48px 80px; align-items: end">
<div class="rise" style="display: flex; flex-direction: column; gap: 22px">
{crumbs('<a class="cl" href="WorkWith.dc.html" style="padding: 10px 0">Work with Kyle</a>', 'Pop strings')}
{hero_title('String &amp; orchestral arrangements for artists', 'Pop strings', 'clamp(76px, 12vw, 190px)')}
</div>
<div class="rise" style="animation-delay: .1s; display: flex; flex-direction: column; gap: 18px">
<p style="margin: 0; font-size: 18px; max-width: 58ch">Kyle Daniel Gordon writes string and orchestral arrangements for pop and alternative artists. He was supervising orchestrator on Rosalía’s <em>LUX</em>, recorded with the London Symphony Orchestra, and arranges for records, sessions and live shows.</p>
<div style="display: flex; flex-wrap: wrap; gap: 10px"><a class="btn solid" href="mailto:kylegordonmusic@gmail.com?subject=String%20arrangement">Email Kyle</a><a class="btn line" href="Project.dc.html">The LUX story</a></div>
</div>
</div>
</header>

<section aria-label="Records" style="{WRAP}; margin-top: 120px; display: flex; flex-direction: column; gap: 32px">
{staff_head('A', 'Records', 'Strings &amp; orchestra')}
<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(min(200px, 46%), 1fr)); gap: 32px 24px">{recs}</div>
</section>

<section aria-label="How it works" style="{WRAP}; margin-top: 120px; display: grid; grid-template-columns: repeat(auto-fit, minmax(min(420px, 100%), 1fr)); gap: 32px 80px; align-items: start">
{staff_head('B', 'How it works', 'Demo to stage')}
<ol style="margin: 0; padding: 0; list-style: none; font-size: 16px; border-bottom: 1px solid {RULE}">{steps}</ol>
</section>

{next_link('Live', 'BBC Proms &amp; premieres', 'Live.dc.html')}

{footer('#a8b85a 30%, #31502c 62%, #0e1a12 100%')}'''
    return page('Pop string arrangements, Kyle Daniel Gordon', root(inner), CSS, PAPER, h=3800)


for fn, f in [('Home.dc.html', home), ('Project.dc.html', lux), ('WorkWith.dc.html', workwith), ('Oppenheimer.dc.html', oppenheimer), ('Live.dc.html', live), ('PopStrings.dc.html', popstrings)]:
    open(os.path.join(OUT, fn), 'w', encoding='utf-8').write(f().replace('family=Instrument+Sans:wght@400;500;600', 'family=Instrument+Sans:wght@400;500;600&amp;family=Instrument+Serif:ital@0;1'))
print('written', len(P), 'projects,', sum(1 for p in P if p[5]), 'with Spotify links')
# ------------------------------------------------------------------ PITCH PAGES (/for/<slug>/, noindex)
PITCH_SETS = {
    'film': ('Film &amp; television', ['Oppenheimer', 'Frozen II', 'Star Wars: The Last Jedi', 'Black Panther: Wakanda Forever', 'The Gilded Age', 'The Mandalorian']),
    'tv': ('Television', ['The Gilded Age', 'Bridgerton', 'Star Trek: Strange New Worlds', 'Outer Banks', 'Bluey', 'The Book of Boba Fett']),
    'artist': ('Records', ['LUX', 'People Pleaser', 'Grace Kelly with Strings: At The Movies', 'Magia en Dos', 'Romani: The Untold Story', 'Baby Shark 10th Anniversary']),
    'orchestra': ('Records', ['LUX', 'Romani: The Untold Story', 'Baby Shark 10th Anniversary', 'Grace Kelly with Strings: At The Movies']),
}
PITCHES = json.load(open('/home/claude/kdg_scripts/pitches.json'))


def pitch(pt):
    head, titles = PITCH_SETS.get(pt['kind'], PITCH_SETS['film'])
    ratio = '1 / 1' if pt['kind'] in ('artist', 'orchestra') else '2 / 3'
    tiles = ''.join(tile(t, f'{BY[t][2]} · {BY[t][3]}' if BY[t][3] else BY[t][2], ratio, 'Project.dc.html' if t == 'LUX' else ('Oppenheimer.dc.html' if t == 'Oppenheimer' else None)) for t in titles if t in BY)
    live = ''
    if pt['kind'] == 'orchestra':
        live = f'''<section aria-label="Live" style="{WRAP}; margin-top: 110px; display: flex; flex-direction: column; gap: 32px">
{staff_head('B', 'Live', 'BBC Proms · San Francisco Symphony')}
<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(min(300px, 100%), 1fr)); gap: 18px">{prom_cards()}</div></section>'''
    first = pt['name'].split()[0]
    inner = f'''<header style="position: relative">
{band('#120f22 0%, #3b2a6a 26%, #a9c3ff 54%, #eef1f8 78%', 300)}
{nav('#eef1ff')}
<div style="{WRAP}; padding-top: 220px; display: grid; grid-template-columns: repeat(auto-fit, minmax(min(460px, 100%), 1fr)); gap: 40px 80px; align-items: end" class="rise">
<div style="display: flex; flex-direction: column; gap: 18px">
<span style="{MONO}; font-size: 12px; color: {MUTE}">For {pt['name']}</span>
<h1 style="margin: 0; {SANS}; font-size: clamp(44px, 6vw, 88px); line-height: 0.95; letter-spacing: -0.05em; font-weight: 600">Hi {first}.</h1>
</div>
<div style="display: flex; flex-direction: column; gap: 18px">
<p style="margin: 0; font-size: 20px; line-height: 1.5; max-width: 54ch">{pt['note']}</p>
<span style="{MONO}; font-size: 12px; color: {MUTE}">— Kyle Daniel Gordon · orchestrator, arranger, conductor</span>
<div style="display: flex; flex-wrap: wrap; gap: 10px"><a class="btn solid" href="mailto:kylegordonmusic@gmail.com?subject=Hi%20Kyle%20%E2%80%94%20from%20{pt['name'].replace(' ', '%20')}">Reply to Kyle</a><a class="btn line" href="Home.dc.html#credits">All credits</a></div>
</div>
</div>
</header>

<section aria-label="Selected work" style="{WRAP}; margin-top: 110px; display: flex; flex-direction: column; gap: 32px">
{staff_head('A', head, 'Selected for you')}
<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(min(200px, 46%), 1fr)); gap: 32px 24px">{tiles}</div>
</section>
{live}

<section aria-label="LUX" style="{WRAP}; margin-top: 110px">
<a href="Project.dc.html" class="press" style="border-top: 2px solid {C['tang']}"><span style="{MONO}; font-size: 11px; color: #b5410b">Rosalía · LUX · 6 Latin Grammys · 10 Grammy nominations</span>
<span class="h" style="{SANS}; font-size: clamp(24px, 3vw, 36px); line-height: 1.15; letter-spacing: -0.03em">Supervising orchestrator on LUX, recorded with the London Symphony Orchestra {ARROW}</span></a>
</section>

{footer('#a9c3ff 30%, #3b2a6a 62%, #120f22 100%')}'''
    return page(f'For {pt["name"]}, Kyle Daniel Gordon', root(inner), CSS, PAPER, h=3200)


for pt in PITCHES:
    open(os.path.join(OUT, f'Pitch-{pt["slug"]}.dc.html'), 'w', encoding='utf-8').write(
        pitch(pt).replace('family=Instrument+Sans:wght@400;500;600', 'family=Instrument+Sans:wght@400;500;600&amp;family=Instrument+Serif:ital@0;1'))
# ------------------------------------------------------------------ PRESS KIT
BIO_SHORT = ('Kyle Daniel Gordon is a Los Angeles orchestrator, arranger and conductor. He was supervising orchestrator on Rosalía’s '
             '<em>LUX</em>, recorded with the London Symphony Orchestra, and orchestrated Ludwig Göransson’s score for <em>Oppenheimer</em>.')
BIO_MED = ('Kyle Daniel Gordon is an orchestrator, arranger and conductor based in Los Angeles. He was supervising orchestrator on Rosalía’s '
           '<em>LUX</em> (2025), recorded with the London Symphony Orchestra, which won six Latin Grammys including Album of the Year. '
           'In film and television he orchestrated Ludwig Göransson’s score for <em>Oppenheimer</em> and has worked on <em>Frozen II</em>, '
           '<em>Star Wars: The Last Jedi</em>, <em>Black Panther: Wakanda Forever</em>, <em>The Mandalorian</em> and <em>The Gilded Age</em>. '
           'At the BBC Proms he was lead orchestrator on <em>Soul Revolution</em> (2025) and arranged for <em>Bond and Beyond</em> (2026), '
           'playing his arrangement of Radiohead’s “Spectre” on the Royal Albert Hall organ. His piece <em>The Little Bird</em> was premiered by the '
           'San Francisco Symphony in 2026. He holds a master’s in music from the University of North Texas.')


def press():
    photos = [('conducting-london-symphony-orchestra-for-rosalia-lux-lso', 'Kyle Daniel Gordon conducting', 'Square · 1200 × 1200'),
              ('conducting-london-symphony-orchestra', 'Kyle Daniel Gordon with the London Symphony Orchestra', 'Landscape · 1200 × 675')]
    ph = ''.join(f'''<figure style="margin: 0; display: flex; flex-direction: column; gap: 10px">
<a href="{A[k]}" download class="cov" style="aspect-ratio: {'1 / 1' if 'lux' in k else '16 / 9'}"><img src="{A[k]}" alt="{alt}" loading="lazy"><span class="play">Download</span></a>
<figcaption style="{MONO}; font-size: 11px; color: {MUTE}">{alt} · {sz}</figcaption></figure>''' for k, alt, sz in photos)
    facts = spec([('Name', 'Kyle Daniel Gordon (also credited as Kyle Gordon)'), ('Based in', 'Los Angeles'),
                  ('Work', 'Orchestrator · arranger · conductor · composer'), ('Selected', 'Rosalía, LUX · Oppenheimer · BBC Proms'),
                  ('Orchestras', 'London Symphony Orchestra · New York Philharmonic · San Francisco Symphony · BBC Concert Orchestra'),
                  ('Education', 'University of North Texas (MM)'), ('Credit as', 'Kyle Daniel Gordon')])
    links = ''.join(f'''<a class="press" href="{u}"><span style="{MONO}; font-size: 11px; color: {MUTE}">{o}</span>
<span class="h" style="{SANS}; font-size: 20px; line-height: 1.2; letter-spacing: -0.02em">{h} {ARROW}</span></a>''' for o, h, dsc, u in PRESS)
    def bio(label, text, words):
        return f'''<div style="display: flex; flex-direction: column; gap: 12px; padding-top: 18px; border-top: 1.5px solid {INK}">
<span style="{MONO}; font-size: 12px; color: {MUTE}">{label} · {words}</span>
<p style="margin: 0; font-size: 17px; line-height: 1.6; max-width: 70ch">{text}</p></div>'''
    inner = f'''<header style="position: relative">
{band('#1b1a17 0%, #4b463e 26%, #b9b0a0 54%, #efeadf 78%', 300)}
{nav('#f2efe8')}
<div style="{WRAP}; padding-top: 220px; display: flex; flex-direction: column; gap: 20px" class="rise">
{crumbs('<a class="cl" href="Home.dc.html" style="padding: 10px 0">Home</a>', 'Press')}
{hero_title('Bios, photos and facts for programmes and press', 'Press kit', 'clamp(64px, 10vw, 160px)')}
<div style="display: flex; flex-wrap: wrap; gap: 10px"><a class="btn solid" href="mailto:kylegordonmusic@gmail.com?subject=Press%20request">Press requests</a></div>
</div>
</header>

<section aria-label="Biographies" style="{WRAP}; margin-top: 110px; display: flex; flex-direction: column; gap: 32px">
{staff_head('A', 'Biographies', 'Free to use')}
<div style="display: flex; flex-direction: column; gap: 36px">{bio('Short', BIO_SHORT, '40 words')}{bio('Programme', BIO_MED, '150 words')}</div>
</section>

<section aria-label="Photos" style="{WRAP}; margin-top: 110px; display: flex; flex-direction: column; gap: 32px">
{staff_head('B', 'Photos', 'Click to download')}
<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(min(360px, 100%), 1fr)); gap: 28px; align-items: start">{ph}</div>
</section>

<section aria-label="Facts" style="{WRAP}; margin-top: 110px; display: grid; grid-template-columns: repeat(auto-fit, minmax(min(420px, 100%), 1fr)); gap: 32px 80px; align-items: start">
{staff_head('C', 'Facts', 'At a glance')}
{facts}
</section>

<section aria-label="Coverage" style="{WRAP}; margin-top: 110px; display: grid; grid-template-columns: repeat(auto-fit, minmax(min(420px, 100%), 1fr)); gap: 32px 80px; align-items: start">
{staff_head('D', 'Coverage', 'Press')}
<div style="display: flex; flex-direction: column">{links}</div>
</section>

{footer('#b9b0a0 30%, #4b463e 62%, #1b1a17 100%')}'''
    return page('Press kit, Kyle Daniel Gordon', root(inner), CSS, PAPER, h=3800)


open(os.path.join(OUT, 'Press.dc.html'), 'w', encoding='utf-8').write(press().replace('family=Instrument+Sans:wght@400;500;600', 'family=Instrument+Sans:wght@400;500;600&amp;family=Instrument+Serif:ital@0;1'))
# ------------------------------------------------------------------ LUX (español)
ES = [
 ('Orchestrations for an album sung in thirteen languages, with the London Symphony Orchestra on every track.',
  'Orquestaciones para un álbum cantado en trece idiomas, con la Orquesta Sinfónica de Londres en todas las canciones.'),
 ("LUX is Rosalía's fourth studio album, released in November 2025. Kyle Daniel Gordon was the album’s supervising orchestrator. The album was recorded with the London Symphony Orchestra at AIR Studios in London, conducted by Daníel Bjarnason.",
  'LUX es el cuarto álbum de estudio de Rosalía, publicado en noviembre de 2025. Kyle Daniel Gordon fue el orquestador supervisor del álbum, grabado con la Orquesta Sinfónica de Londres en los AIR Studios de Londres bajo la dirección de Daníel Bjarnason.'),
 ('LUX won six Latin Grammys at the 27th Latin Grammy Awards, including Album of the Year, and received ten nominations at the 69th Grammy Awards, including Album of the Year.',
  'LUX ganó seis Latin Grammy en la 27.ª edición de los premios, entre ellos Álbum del Año, y recibió diez nominaciones en la 69.ª edición de los Grammy, entre ellas Álbum del Año.'),
 ('Gordon tells the story of the call from the London Symphony Orchestra that brought him onto the album.',
  'Gordon cuenta la llamada de la Orquesta Sinfónica de Londres que lo llevó al álbum (artículo en inglés).'),
 ('LUX sessions with the London Symphony Orchestra', 'Sesiones de LUX con la Orquesta Sinfónica de Londres'),
 ('The London Symphony Orchestra plays on every song. LUX (Complete Works) adds three more.',
  'La Orquesta Sinfónica de Londres toca en todas las canciones. LUX (Complete Works) añade tres más.'),
 ('>Work</a> / Records / Rosalía', '>Trabajo</a> / Discos / Rosalía'),
 ('<a class="cl" href="ProjectES.dc.html" hreflang="es" lang="es" style="padding: 10px 0">Español</a>', '<a class="cl" href="Project.dc.html" hreflang="en" lang="en" style="padding: 10px 0">English</a>'),
 ('>Artist<', '>Artista<'), ('>Album<', '>Álbum<'), ('>Supervising orchestrator<', '>Orquestador supervisor<'),
 ('>Orchestra<', '>Orquesta<'), ('>London Symphony Orchestra<', '>Orquesta Sinfónica de Londres<'), ('>Conductor<', '>Director<'),
 ('>Recorded<', '>Grabación<'), ('>AIR Studios, London<', '>AIR Studios, Londres<'), ('>Label<', '>Sello<'),
 ('>Recognition<', '>Reconocimientos<'), ('>Tracklist<', '>Canciones<'), ('>LUX · 15 tracks<', '>LUX · 15 canciones<'),
 ('Listen on Spotify</a>', 'Escuchar en Spotify</a>'), ('Play the album</a>', 'Escuchar el álbum</a>'),
 ('>Play on Spotify<', '>Escuchar en Spotify<'), ('Next — Film', 'Siguiente — Cine'),
 ('>Latin Grammys<', '>Latin Grammy<'),
 ('Album of the Year, Song of the Year (“La Perla”), Best Alternative Music Album and more · 27th Latin Grammy Awards, 2026',
  'Álbum del Año, Canción del Año («La Perla»), Mejor Álbum de Música Alternativa y más · 27.ª edición de los Latin Grammy, 2026'),
 ('>Grammy nominations<', '>nominaciones al Grammy<'),
 ('Including Album of the Year · 69th Grammy Awards, 2027', 'Entre ellas Álbum del Año · 69.ª edición de los Grammy, 2027'),
 ('>Start a project<', '>Empezar un proyecto<'), ('>Contact<', '>Contacto<'),
]


def lux_es():
    s = lux()
    missing = [a for a, b in ES if a not in s]
    if missing:
        print('ES: not found ->', [m[:40] for m in missing])
    for a, b in ES:
        s = s.replace(a, b)
    return s


open(os.path.join(OUT, 'ProjectES.dc.html'), 'w', encoding='utf-8').write(lux_es().replace('family=Instrument+Sans:wght@400;500;600', 'family=Instrument+Sans:wght@400;500;600&amp;family=Instrument+Serif:ital@0;1'))

# ------------------------------------------------------------------ PRIVACY
def privacy():
    items = [('What is measured', 'This site uses Cloudflare Web Analytics (page views, no cookies) and Microsoft Clarity (anonymous heatmaps and session recordings that show how pages are used). Text you type into forms is masked. Neither tool is used for advertising.'),
             ('Cookies', 'Cloudflare Web Analytics sets no cookies. Microsoft Clarity may set first-party cookies to link page views within a visit; where consent is required it runs without them. You can block both with any standard content blocker.'),
             ('Your data', 'No personal information is collected unless you email Kyle. Email is used only to reply. For questions or deletion requests, write to kylegordonmusic@gmail.com.'),
             ('Third parties', 'Microsoft’s privacy statement: privacy.microsoft.com. Cloudflare’s privacy policy: cloudflare.com/privacypolicy.')]
    body = ''.join(f'''<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(min(260px, 100%), 1fr)); gap: 12px 60px; padding: 22px 0; border-top: 1px solid {RULE}">
<h2 style="margin: 0; {SANS}; font-size: 22px; letter-spacing: -0.02em">{h}</h2><p style="margin: 0; font-size: 17px; line-height: 1.6; max-width: 62ch">{t}</p></div>''' for h, t in items)
    inner = f'''<header style="position: relative">
{band('#1b1a17 0%, #4b463e 26%, #b9b0a0 54%, #efeadf 78%', 260)}
{nav('#f2efe8')}
<div style="{WRAP}; padding-top: 200px; display: flex; flex-direction: column; gap: 14px" class="rise">
{hero_title('Updated November 2026', 'Privacy', 'clamp(64px, 10vw, 150px)')}
</div></header>
<section aria-label="Privacy" style="{WRAP}; margin-top: 70px; border-bottom: 1px solid {RULE}">{body}</section>
{footer('#b9b0a0 30%, #4b463e 62%, #1b1a17 100%')}'''
    return page('Privacy, Kyle Daniel Gordon', root(inner), CSS, PAPER, h=2200)


open(os.path.join(OUT, 'Privacy.dc.html'), 'w', encoding='utf-8').write(privacy().replace('family=Instrument+Sans:wght@400;500;600', 'family=Instrument+Sans:wght@400;500;600&amp;family=Instrument+Serif:ital@0;1'))

# credits for structured data (read by build_static.py)
json.dump([dict(title=t, cat=c, role=r, with_=w, spotify=s) for t, c, r, w, k, s in P],
          open('/home/claude/kdg_scripts/credits.json', 'w'), ensure_ascii=False, indent=0)
