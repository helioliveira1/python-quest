/* Service worker: deixa o sistema disponível offline depois da 1ª visita (inclui o Python/Pyodide em cache). */
const VERSAO = "pyquest-v1";
const APP = ["./", "index.html", "assets/app.css", "assets/app.js", "assets/harness.js", "assets/icon.svg",
  "vendor/codemirror.css", "vendor/codemirror.js", "data/fundamentos.js", "data/basico.js", "data/intermediario.js", "manifest.webmanifest"];
self.addEventListener("install", e => { e.waitUntil(caches.open(VERSAO).then(c => c.addAll(APP)).then(() => self.skipWaiting())); });
self.addEventListener("activate", e => {
  e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== VERSAO && k !== "pyquest-cdn").map(k => caches.delete(k)))).then(() => self.clients.claim()));
});
self.addEventListener("fetch", e => {
  const url = new URL(e.request.url);
  if (e.request.method !== "GET") return;
  if (url.origin === location.origin) {
    // app: rede primeiro (pega atualizações), cache como reserva offline
    e.respondWith(fetch(e.request).then(r => { const c = r.clone(); caches.open(VERSAO).then(ca => ca.put(e.request, c)); return r; })
      .catch(() => caches.match(e.request, {ignoreSearch: true}).then(r => r || caches.match("index.html"))));
  } else if (/cdn\.jsdelivr\.net\/pyodide|files\.pythonhosted\.org|pypi\.org/.test(url.href)) {
    // Python e pacotes: cache primeiro (arquivos versionados)
    e.respondWith(caches.open("pyquest-cdn").then(c => c.match(e.request).then(hit => hit || fetch(e.request).then(r => { if (r.ok) c.put(e.request, r.clone()); return r; }))));
  }
});
