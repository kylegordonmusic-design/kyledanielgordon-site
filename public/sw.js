const V = '6a806cde07';
const CORE = ["/img/grain.webp", "/favicon.svg", "/fonts/archivo-62-800.v2.woff2", "/fonts/dm-mono-400.v2.woff2", "/fonts/instrument-sans.v2.woff2"];
self.addEventListener('install', e => { e.waitUntil(caches.open('kdg-' + V).then(c => c.addAll(CORE)).then(() => self.skipWaiting())); });
self.addEventListener('activate', e => { e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== 'kdg-' + V).map(k => caches.delete(k)))).then(() => self.clients.claim())); });
self.addEventListener('fetch', e => {
  const r = e.request; if (r.method !== 'GET') return;
  const u = new URL(r.url);
  const asset = /\/(img|fonts)\//.test(u.pathname) || u.host === 'fonts.gstatic.com' || u.host === 'fonts.googleapis.com';
  if (asset) {  // cache first: images and fonts never change under the same name
    e.respondWith(caches.match(r).then(hit => hit || fetch(r).then(res => { const c = res.clone(); caches.open('kdg-' + V).then(x => x.put(r, c)); return res; })));
  }  // pages are left to the browser so hover prefetch/prerender stays instant
});
