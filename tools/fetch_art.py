"""Download poster/album art listed in tools/art.json into art/<slug>.jpg (max 1000px tall).
Runs on GitHub Actions. Existing files are skipped. Approved by Kyle 2026-11-20."""
import json, os, io, sys, urllib.request
from PIL import Image
art = json.load(open('tools/art.json'))
os.makedirs('art', exist_ok=True)
ok = 0
for slug, url in art.items():
    out = f'art/{slug}.jpg'
    if os.path.exists(out): continue
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (KDG site art fetcher)'})
        data = urllib.request.urlopen(req, timeout=30).read()
        im = Image.open(io.BytesIO(data)).convert('RGB')
        if im.height > 1000:
            im = im.resize((round(im.width * 1000 / im.height), 1000), Image.LANCZOS)
        im.save(out, 'JPEG', quality=86, optimize=True, progressive=True)
        print('saved', out, im.size); ok += 1
    except Exception as e:
        print('FAILED', slug, url, e, file=sys.stderr)
print(ok, 'new images')

# Raw files (fonts etc.) listed in tools/files.json -> fonts/<name>, downloaded as-is.
if os.path.exists('tools/files.json'):
    os.makedirs('fonts', exist_ok=True)
    for name, url in json.load(open('tools/files.json')).items():
        out = f'fonts/{name}'
        if os.path.exists(out): continue
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (KDG site asset fetcher)'})
            open(out, 'wb').write(urllib.request.urlopen(req, timeout=30).read()); print('saved', out)
        except Exception as e:
            print('FAILED', name, url, e, file=sys.stderr)
