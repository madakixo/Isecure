const CACHE = 'secureeye-v19';
self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(cache => cache.addAll([
    '/', '/manifest.json', '/icons/icon-512x512.png'
  ])));
});

self.addEventListener('fetch', e => {
  e.respondWith(caches.match(e.request).then(r => r || fetch(e.request)));
});
