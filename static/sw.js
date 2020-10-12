// This is based on the First Progressive Web App Tutorial by Google
// https://codelabs.developers.google.com/codelabs/your-first-pwapp/
const cacheName = 'modern-spike-PWA-1.2.12';
const filesToCache = [
    '/static/bootstrap/js/jquery-3.5.1.min.js',
    '/static/bootstrap/js/bootstrap.min.js',
    '/static/bootstrap/css/bootstrap.css',
    '/static/bootstrap/js/popper.min.js',
    '/static/bootstrap/js/bootstrap.bundle.js',
    '/static/js/main.js',
    '/static/js/ga.js',
    '/static/css/mana.css',
    '/static/css/styles.css',
    '/static/css/animate.min.css',
    '/static/images/logo-mtgjson-light-blue.svg',
    '/static/images/bootstrap-icons/arrow-left-circle.svg',
    '/static/images/bootstrap-icons/check-circle.svg',
    '/static/images/bootstrap-icons/check.svg',
    '/static/images/bootstrap-icons/filter-circle.svg',
    '/static/images/bootstrap-icons/info-circle.svg',
    '/static/images/bootstrap-icons/x-circle.svg',
    '/static/images/bootstrap-icons/chat-square-text.svg',
    '/static/images/bootstrap-icons/envelope.svg',
    '/static/images/bootstrap-icons/house-fill.svg',
    '/static/images/bootstrap-icons/x.svg',
    '/static/images/mana.svg',
    '/static/favicon.ico',
    '/static/fonts/Beleren-Bold/beleren-boldP101.otf',
    '/static/fonts/Beleren-Bold/beleren-boldP101.eot',
    '/static/fonts/Beleren-Bold/beleren-boldP101.svg',
    '/static/fonts/Beleren-Bold/beleren-boldP101.ttf',
    '/static/fonts/Beleren-Bold/beleren-boldP101.woff',
    '/static/fonts/Beleren-Bold/beleren-boldP101.woff2',
    '/static/fonts/mplantin/mplantin.otf',
    '/static/fonts/mplantin/mplantin.eot',
    '/static/fonts/mplantin/mplantin.svg',
    '/static/fonts/mplantin/mplantin.ttf',
    '/static/fonts/mplantin/mplantin.woff',
    '/static/fonts/mplantin/mplantin.woff2',
    '/offline.html',
    '/about',
];


// When the 'install' event is fired we will cache
// the html, javascript, css, images and any other files important
// to the operation of the application shell
self.addEventListener('install', function (e) {
    // console.log('[ServiceWorker] Install');
    e.waitUntil(caches.open(cacheName).then(function (cache) {
            // console.log('[ServiceWorker] Caching app shell');
            return cache.addAll(filesToCache);
        })
    );
});

// We then listen for the service worker to be activated/started. Once it is
// ensures that your service worker updates its cache whenever any of the app shell files change.
// In order for this to work, you'd need to increment the cacheName variable at the top of this service worker file.
self.addEventListener('activate', function (e) {
    // console.log('[ServiceWorker] Activate');
    e.waitUntil(
        caches.keys().then(function (keyList) {
            return Promise.all(keyList.map(function (key) {
                if (key !== cacheName) {
                    // console.log('[ServiceWorker] Removing old cache', key);
                    return caches.delete(key);
                }
            }));
        })
    );
    return self.clients.claim();
});


// Serve the app shell from the cache
// If the file is not in the cache then try to get it via the network.
// otherwise give an error and display an offline page
// This is a just basic example, a better solution is to use the
// Service Worker Precache module https://github.com/GoogleChromeLabs/sw-precache
self.addEventListener('fetch', function (e) {
    // fetch(e.request.clone()).catch(error => {
    //
    // });
    if (e.request.method !== 'GET') {
        return;
    }

    // if (e.request.method !== "GET") {
    //     return Promise.reject('no-match')
    //     // return Promise.reject('no-match')
    // }
    // console.log('[ServiceWorker] Fetch', e.request.url);
    // if (e.request.method === "POST") {
    e.respondWith(fromCache(e.request));
    e.waitUntil(update(e.request));
    // }
});

function fromCache(request) {
    return caches.open(cacheName).then(function (cache) {
        return cache.match(request).then(function (matching) {
            return matching || fetch(request.clone()).catch(error => {
                // console.log('Fetch failed; returning offline page instead.', error);
                // location.reload();
                return caches.match('offline.html');
            });
        });
    });
}

function update(request) {
    return caches.open(cacheName).then(function (cache) {
        return fetch(request).then(function (response) {
            // console.log('URL OF REQUEST ' + request.url);


            if (request.url == self.location.origin + "/") {
                // self.console.log(self.location.origin + "/");

                // return response;
            } else if (request.url.indexOf("google-analytics") > -1) {
                self.console.log("google analytics not cached");

                // return response;
            } else {
                // self.console.log(request,response.clone());

                return cache.put(request, response.clone()).then(function () {
                    return response;
                });
            }
        });
    });
}

addEventListener('message', e => {
    if (e.data === 'skipWaiting') {
        skipWaiting();
    }
});

