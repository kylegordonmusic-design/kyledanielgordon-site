# Instance variable fonts to the exact styles used and subset to the characters the site uses (+ Latin-1).
import glob, re, html, os, sys
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from fontTools import subset
SRC = '/home/claude/kyledanielgordon-site/fonts'; OUT = '/home/claude/kdg_scripts/fonts_opt'; SITE = sys.argv[1]
chars = set(chr(c) for c in range(0x20, 0x7f)) | set(chr(c) for c in range(0xa0, 0x180)) | set('‘’“”–—•·…→←↗×′″€™')
for f in glob.glob(SITE + '/**/*.html', recursive=True):
    t = open(f, encoding='utf-8').read()
    t = re.sub(r'<script[\s\S]*?</script>|<style[\s\S]*?</style>', ' ', t)
    chars |= set(html.unescape(re.sub(r'<[^>]+>', ' ', t)))
    chars |= set(html.unescape(' '.join(re.findall(r'(?:alt|title|aria-label|content)="([^"]*)"', t))))
chars = {c for c in chars if ord(c) >= 0x20}
print(len(chars), 'chars')
jobs = {'archivo-62-800': {'wdth': 62, 'wght': 800}, 'instrument-sans': {'wdth': 100, 'wght': (400, 700)}}
for fn in os.listdir(SRC):
    if not fn.endswith('.woff2'): continue
    name = fn[:-6]; f = TTFont(os.path.join(SRC, fn))
    if 'fvar' in f and name in jobs:
        axes = {a.axisTag: a for a in f['fvar'].axes}
        loc = {k: v for k, v in jobs[name].items() if k in axes}
        f = instancer.instantiateVariableFont(f, loc)
    opts = subset.Options(); opts.flavor = 'woff2'; opts.layout_features = ['kern', 'liga', 'calt', 'ccmp', 'locl', 'mark', 'mkmk', 'tnum', 'case']
    opts.name_IDs = [1, 2, 3, 4, 6]; opts.hinting = False; opts.desubroutinize = True
    s = subset.Subsetter(opts); s.populate(unicodes=[ord(c) for c in chars]); s.subset(f)
    out = os.path.join(OUT, name + '.v2.woff2'); f.flavor = 'woff2'; f.save(out)
    print(fn, os.path.getsize(os.path.join(SRC, fn)), '->', os.path.getsize(out))
