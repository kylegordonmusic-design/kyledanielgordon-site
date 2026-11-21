import asyncio
from playwright.async_api import async_playwright
D='/home/claude/kdg_scripts/icons/'
async def m():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        for name,src,size in [('favicon-48.png','favicon.svg',48),('apple-touch-icon.png','square.svg',180),('icon-192.png','favicon.svg',192),('icon-512.png','favicon.svg',512)]:
            pg=await b.new_page(viewport={'width':size,'height':size})
            svg=open(D+src).read()
            await pg.set_content(f'<html><body style="margin:0;background:transparent">{svg.replace("<svg ","<svg width=\"%d\" height=\"%d\" "%(size,size),1)}</body></html>')
            await pg.screenshot(path=D+name,omit_background=True)
        await b.close()
asyncio.run(m())
