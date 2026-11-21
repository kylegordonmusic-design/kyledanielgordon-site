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
<link rel="canonical" href="{full}"><style>html,body{{margin:0;height:100%;background:#f7f4ec}}</style>
<script>var d={dest_js},done=false;function go(){{if(!done){{done=true;location.replace(d)}}}}setTimeout(go,1200);</script>
<script defer src="https://static.cloudflareinsights.com/beacon.min.js" data-cf-beacon='{{"token": "{token}"}}' onload="setTimeout(go,350)" onerror="go()"></script>
<noscript><meta http-equiv="refresh" content="0;url={dest_h}"></noscript></head><body></body></html>'''
def build(out):
    for c, v in load().items():
        d = os.path.join(out, 'r', c); os.makedirs(d, exist_ok=True)
        open(os.path.join(d, 'index.html'), 'w').write(PAGE.format(full=html.escape(SITE + v['dest']), dest_js=json.dumps(v['dest']), dest_h=html.escape(v['dest']), token=TOKEN))
if __name__ == '__main__':
    if sys.argv[1] == 'new':
        print(f"{SITE}/r/{new(sys.argv[2], sys.argv[3])}")
    else:
        build(sys.argv[2])
