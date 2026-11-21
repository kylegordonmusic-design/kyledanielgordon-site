import json, sys
from playwright.sync_api import sync_playwright
BASE='http://localhost:8770'
PAGES=['/','/work/rosalia-lux/','/es/rosalia-lux/','/work/oppenheimer/','/live/','/pop-strings/','/orchestrator-los-angeles/','/what-does-an-orchestrator-do/','/contact/','/work-with-kyle/','/press/','/privacy/','/for/example-artist/','/404.html']
VPS_ALL=[(320,568,True,'se1'),(360,740,True,'and-s'),(375,667,True,'se'),(390,844,True,'ip15'),(412,915,True,'pixel'),(430,932,True,'promax'),(844,390,True,'land'),(768,1024,True,'ipad'),(1024,768,True,'ipad-l'),(1280,800,False,'lap'),(1440,900,False,'mac'),(1920,1080,False,'fhd'),(2560,1440,False,'qhd')]
VPS=[v for v in VPS_ALL if v[2]]
JS='''() => { const W=innerWidth, out=[], small=[], tiny=[];
 const sw=document.documentElement.scrollWidth;
 for (const e of document.querySelectorAll('body *')) { const r=e.getBoundingClientRect(); if(!r.width||!r.height) continue;
   const cs=getComputedStyle(e); if(cs.visibility=='hidden'||cs.display=='none') continue;
   if (r.right>W+1 && !e.closest('[style*="overflow"]')) out.push((e.tagName+'.'+(e.className||'')).slice(0,40)+' '+Math.round(r.right));
   if (e.matches('a,button') && (r.height<24||r.width<24) && e.innerText.trim()) small.push(e.innerText.trim().slice(0,20)+' '+Math.round(r.width)+'x'+Math.round(r.height));
   if (e.childNodes.length && [...e.childNodes].some(n=>n.nodeType==3&&n.textContent.trim()) && parseFloat(cs.fontSize)<11) tiny.push(e.innerText.trim().slice(0,20)+' '+cs.fontSize);
 }
 return {sw, W, out:[...new Set(out)].slice(0,6), small:[...new Set(small)].slice(0,6), tiny:[...new Set(tiny)].slice(0,4)} }'''
res={}
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
    for w,h,mob,tag in VPS:
        ctx=b.new_context(viewport={'width':w,'height':h}, is_mobile=mob, has_touch=mob, device_scale_factor=2 if mob else 1)
        pg=ctx.new_page()
        for path in PAGES:
            pg.goto(BASE+path, wait_until='networkidle', timeout=30000); pg.wait_for_timeout(300)
            r=pg.evaluate(JS)
            if r['sw']>w or r['out'] or r['small'] or r['tiny']: res[f'{tag} {path}']=r
            if path in ('/','/work/rosalia-lux/','/contact/') : pg.screenshot(path=f'/home/claude/shots/vp/{tag}{path.replace("/","_")}.png', full_page=False)
        ctx.close()
    b.close()
for k,v in res.items(): print(k, json.dumps(v)[:400])
print('issues', len(res))
