// var CACHE_NAME = 'static-cache';
// var urlsToCache = [
//     '/static/bootstrap/js/jquery-3.4.1.min.js',
//     '/static/bootstrap/js/bootstrap.min.js',
//     '/static/js/ajax.js',
//     '/static/js/main.js',
//     '/static/bootstrap/css/bootstrap.css',
// ];
// version track
const vn = "version-x";

// files to cache
const appCash = [
    '/static/bootstrap/js/jquery-3.4.1.min.js',
    '/static/bootstrap/js/bootstrap.min.js',
    '/static/js/ajax.js',
    '/static/js/main.js',
    '/static/bootstrap/css/bootstrap.css',
    '/static/css/mana.css',
    '/static/css/styles.css',
    '/static/images/mana.svg',
];

// install and save files to cache
self.addEventListener('install', (e) => {
    e.waitUntil(
        caches.open(vn).then((cache) => {
            return cache.addAll(appCash);
        })
    );
});

// Listen for messages from client
self.addEventListener('message', (event) => {
    if (event.data.action === 'skipWaiting') {
        self.skipWaiting();
    } else if (event.data.action === 'clearOld') {
        // Delete the old caches
        event.waitUntil(
            caches.keys().then((keys) => Promise.all(
                keys.map((k) => {
                    if (!k.includes(vn)) {
                        return caches.delete(k);
                    }
                })
            )).then(() => {
                console.log('old caches are cleared');
            })
        )
    }
});

// Serve if request already exists in cache else fetch
self.addEventListener('fetch', e => {
    const url = new URL(e.request.url);
    (appCash.includes(url.pathname)) ? e.respondWith(caches.match(url)) : console.log("Fetching: " + url);
});