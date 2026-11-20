"""Speed pass applied to the built site: responsive WebP images, instant navigation, service worker."""
import os, re, json, hashlib, shutil
from PIL import Image
from bs4 import BeautifulSoup

FONTS_SRC = '/home/claude/kyledanielgordon-site/fonts'
FONT_CSS = '''<link rel="preload" href="/fonts/archivo-62-800.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/fonts/dm-mono-400.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/fonts/instrument-sans.woff2" as="font" type="font/woff2" crossorigin>
<style>
@font-face{font-family:'Archivo';font-style:normal;font-weight:800;font-stretch:62%;font-display:swap;src:url(/fonts/archivo-62-800.woff2) format('woff2')}
@font-face{font-family:'DM Mono';font-style:normal;font-weight:400;font-display:swap;src:url(/fonts/dm-mono-400.woff2) format('woff2')}
@font-face{font-family:'DM Mono';font-style:normal;font-weight:500;font-display:swap;src:url(/fonts/dm-mono-500.woff2) format('woff2')}
@font-face{font-family:'Instrument Sans';font-style:normal;font-weight:400 700;font-stretch:100%;font-display:swap;src:url(/fonts/instrument-sans.woff2) format('woff2')}
@font-face{font-family:'Instrument Serif';font-style:normal;font-weight:400;font-display:swap;src:url(/fonts/instrument-serif.woff2) format('woff2')}
@font-face{font-family:'Instrument Serif';font-style:italic;font-weight:400;font-display:swap;src:url(/fonts/instrument-serif-italic.woff2) format('woff2')}
</style>'''

WIDTHS = (160, 320, 640, 1000)

SPECULATION = '''<script type="speculationrules">
{"prerender":[{"where":{"and":[{"href_matches":"/*"},{"not":{"href_matches":"/img/*"}}]},"eagerness":"moderate"}],
 "prefetch":[{"where":{"and":[{"href_matches":"/*"},{"not":{"href_matches":"/img/*"}}]},"eagerness":"moderate"}]}
</script>
<script>
/* hover / touch prefetch for browsers without speculation rules (Safari, Firefox) */
(function(){if(HTMLScriptElement.supports&&HTMLScriptElement.supports('speculationrules'))return;
var done={},t;function go(a){var u=a.href;if(!u||done[u]||a.origin!==location.origin||a.hasAttribute('download')||/\\/img\\//.test(a.pathname))return;done[u]=1;
var l=document.createElement('link');l.rel='prefetch';l.href=u;document.head.appendChild(l);}
document.addEventListener('mouseover',function(e){var a=e.target.closest&&e.target.closest('a');if(!a)return;clearTimeout(t);t=setTimeout(function(){go(a)},65)},{passive:true});
document.addEventListener('touchstart',function(e){var a=e.target.closest&&e.target.closest('a');if(a)go(a)},{passive:true});})();
</script>
<style>@view-transition{navigation:auto}</style>'''

SW_REG = '''<script>if('serviceWorker' in navigator){addEventListener('load',function(){navigator.serviceWorker.register('/sw.js')})}</script>'''

SW = '''const V = '%s';
const CORE = %s;
self.addEventListener('install', e => { e.waitUntil(caches.open('kdg-' + V).then(c => c.addAll(CORE)).then(() => self.skipWaiting())); });
self.addEventListener('activate', e => { e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== 'kdg-' + V).map(k => caches.delete(k)))).then(() => self.clients.claim())); });
self.addEventListener('fetch', e => {
  const r = e.request; if (r.method !== 'GET') return;
  const u = new URL(r.url);
  const asset = /\\/(img|fonts)\\//.test(u.pathname) || u.host === 'fonts.gstatic.com' || u.host === 'fonts.googleapis.com';
  if (asset) {  // cache first: images and fonts never change under the same name
    e.respondWith(caches.match(r).then(hit => hit || fetch(r).then(res => { const c = res.clone(); caches.open('kdg-' + V).then(x => x.put(r, c)); return res; })));
  }  // pages are left to the browser so hover prefetch/prerender stays instant
});
'''


def variants(out, rel):
    src = os.path.join(out, rel.lstrip('/'))
    base = rel[:-4]
    im = Image.open(src).convert('RGB')
    res = []
    for w in WIDTHS:
        if w > im.width and res:
            break
        ww = min(w, im.width)
        dst = os.path.join(out, base.lstrip('/') + f'-{ww}.webp')
        if not os.path.exists(dst):
            im.resize((ww, round(im.height * ww / im.width)), Image.LANCZOS).save(dst, 'WEBP', quality=76, method=6)
        res.append((f'{base}-{ww}.webp', ww))
    return res


def sizes_for(img):
    cls = ' '.join(' '.join(p.get('class', [])) for p in img.parents if p.name)
    if 'wall' in cls: return '(max-width: 600px) 31vw, 150px'
    if 'peek' in cls: return '80px'
    if 'tile' in cls: return '(max-width: 700px) 46vw, 340px'
    return '(max-width: 800px) 100vw, 50vw'


def optimize(out):
    shutil.copytree(FONTS_SRC, os.path.join(out, 'fonts'), dirs_exist_ok=True)
    pages = []
    for d, _, fs in os.walk(out):
        for f in fs:
            if f.endswith('.html') and not f.startswith('google'):
                pages.append(os.path.join(d, f))
    cache = {}
    for p in pages:
        html = open(p, encoding='utf-8').read()
        soup = BeautifulSoup(html, 'html.parser')
        first = True
        for img in soup.find_all('img'):
            s = img.get('src', '')
            if not (s.startswith('/img/') and s.endswith('.jpg')) or '/share-' in s:
                continue
            if s not in cache:
                cache[s] = variants(out, s)
            v = cache[s]
            img['src'] = v[min(1, len(v) - 1)][0]
            img['srcset'] = ', '.join(f'{u} {w}w' for u, w in v)
            img['sizes'] = sizes_for(img)
            if first and img.find_parent('header') is not None:
                img['loading'] = 'eager'; img['fetchpriority'] = 'high'
                first = False
        head = soup.head
        for l in head.find_all('link'):
            if 'fonts.googleapis.com' in l.get('href', '') or 'fonts.gstatic.com' in l.get('href', ''):
                l.decompose()
        vp = head.find('meta', attrs={'name': 'viewport'}) or head.find('meta')
        vp.insert_after(BeautifulSoup(FONT_CSS, 'html.parser'))
        head.append(BeautifulSoup(SPECULATION + SW_REG, 'html.parser'))
        open(p, 'w', encoding='utf-8').write(str(soup))
    # grain texture as WebP (lossless) and point CSS at it
    g = os.path.join(out, 'img', 'grain.png')
    if os.path.exists(g):
        Image.open(g).convert('RGB').save(os.path.join(out, 'img', 'grain.webp'), 'WEBP', quality=60, method=6)
        for p in pages:
            s = open(p, encoding='utf-8').read().replace('/img/grain.png', '/img/grain.webp')
            open(p, 'w', encoding='utf-8').write(s)
    core = ['/img/grain.webp', '/favicon.svg', '/fonts/archivo-62-800.woff2', '/fonts/dm-mono-400.woff2', '/fonts/instrument-sans.woff2']
    ver = hashlib.sha1(''.join(open(p, 'rb').read().hex()[:2000] for p in pages).encode()).hexdigest()[:10]
    open(os.path.join(out, 'sw.js'), 'w').write(SW % (ver, json.dumps(core)))
    print('speed: pages', len(pages), 'images', len(cache))


if __name__ == '__main__':
    import sys
    optimize(sys.argv[1])
