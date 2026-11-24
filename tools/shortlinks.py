"""Short tracked links: kyledanielgordon.com/r/<code> -> clean page, no visible UTM.
The /r/<code> page is counted by Cloudflare Web Analytics as its own path, then forwards.
Mapping (code -> outlet) lives only here in shortlinks.json, never on the site.
Usage:  python3 shortlinks.py new <source> <dest-path>   -> prints the short URL
        python3 shortlinks.py build <outdir>              -> writes the /r/ pages
"""
import json, os, sys, secrets, string, html
DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'shortlinks.json')
SITE = 'https://kyledanielgordon.com'
TOKEN = '74d2ccc3aba8442e8ffe162baef5f751'
def load():
    return json.load(open(DB)) if os.path.exists(DB) else {}
def new(source, dest):
    db = load()
    for c, v in db.items():
        if v['src'] == source and v['dest'] == dest:
            return c
    alpha = string.ascii_lowercase + string.digits
    while True:
        c = ''.join(secrets.choice(alpha) for _ in range(3))
        if c not in db: break
    db[c] = {'src': source, 'dest': dest}
    json.dump(db, open(DB, 'w'), indent=1, ensure_ascii=False)
    return c
PAGE = '''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="robots" content="noindex"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Kyle Daniel Gordon</title>
<link rel="canonical" href="{full}">{og}<style>html,body{{margin:0;height:100%;background:#f7f4ec}}</style>
<script>var d={dest_js},done=false;function go(){{if(!done){{done=true;location.replace(d)}}}}setTimeout(go,1200);</script>
<script defer src="https://static.cloudflareinsights.com/beacon.min.js" data-cf-beacon='{{"token": "{token}"}}' onload="setTimeout(go,350)" onerror="go()"></script>
<noscript><meta http-equiv="refresh" content="0;url={dest_h}"></noscript></head><body></body></html>'''
# Link-preview card for library links, so a pasted or forwarded /r/ link shows the catalog's card (link unfurlers don't follow JS redirects)
LIB_OG = ('<meta property="og:type" content="website"><meta property="og:site_name" content="Kyle Daniel Gordon">'
    '<meta property="og:title" content="Holiday Library · Kyle Daniel Gordon">'
    '<meta property="og:description" content="Holiday arrangements for orchestra, available to rent. Orchestrator on Rosalía’s LUX.">'
    '<meta property="og:image" content="https://www.kyledanielgordon.com/holiday-library/share.jpg?v=1"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">'
    '<meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="https://www.kyledanielgordon.com/holiday-library/share.jpg?v=1">')
def build(out):
    for c, v in load().items():
        d = os.path.join(out, 'r', c); os.makedirs(d, exist_ok=True)
        lib = v['dest'].startswith('/holiday-library/')
        page = PAGE.format(full=html.escape(SITE + v['dest']), dest_js=json.dumps(v['dest']), dest_h=html.escape(v['dest']), token=TOKEN, og=LIB_OG if lib else '')
        if lib:
            page = page.replace('<title>Kyle Daniel Gordon</title>', '<title>Holiday Library · Kyle Daniel Gordon</title>')
        open(os.path.join(d, 'index.html'), 'w').write(page)
if __name__ == '__main__':
    if sys.argv[1] == 'new':
        print(f"{SITE}/r/{new(sys.argv[2], sys.argv[3])}")
    else:
        build(sys.argv[2])
