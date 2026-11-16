/* Python Quest — sistema de estudo em 3 módulos
   Mapa mental interativo + quiz + flashcards + exercícios com Python real (Pyodide). */
"use strict";

/* ===================== dados ===================== */
const MOD_ORDER = ["fundamentos", "basico", "intermediario"];
const MODS = MOD_ORDER.map(id => window.PQ_DATA && window.PQ_DATA[id]).filter(Boolean);
const MOD = Object.fromEntries(MODS.map(m => [m.id, m]));
const KEY = "pyquest_sistema_v1";
const PYBASE = window.PQ_PYBASE || "https://cdn.jsdelivr.net/pyodide/v0.27.2/full/";

/* ===================== estado persistente ===================== */
const blank = () => ({xp: 0, ex: {}, map: {}, quiz: {}, free: false, last: null, days: [], achv: {}, layout: {}, memo: true,
  created: new Date().toISOString(), updated: null});
let S = blank(), storageOk = true;
try { const raw = localStorage.getItem(KEY); if (raw) S = Object.assign(blank(), JSON.parse(raw)); } catch (e) { storageOk = false; }
let saveT;
function save(now) {
  S.updated = new Date().toISOString();
  const w = () => { try { localStorage.setItem(KEY, JSON.stringify(S)); } catch (e) { storageOk = false; } };
  clearTimeout(saveT); now ? w() : (saveT = setTimeout(w, 200));
}
window.addEventListener("beforeunload", () => { flushDraft(); save(true); });
document.addEventListener("visibilitychange", () => { if (document.hidden) { flushDraft(); save(true); } });

/* ===================== helpers de progresso ===================== */
const tk = (m, ti) => m + ":" + ti;
const ek = (m, ti, ei) => m + ":" + ti + ":" + ei;
const topic = (m, ti) => MOD[m].topics[ti];
const exState = (m, ti, ei) => S.ex[ek(m, ti, ei)] || (S.ex[ek(m, ti, ei)] = {solved: false, stars: 0, xp: 0, attempts: 0, hints: 0, sawSol: false, code: null});
const peek = (m, ti, ei) => S.ex[ek(m, ti, ei)] || {};
const solvedIn = (m, ti) => topic(m, ti).ex.filter((_, ei) => peek(m, ti, ei).solved).length;
const starsIn = (m, ti) => topic(m, ti).ex.reduce((a, _, ei) => a + (peek(m, ti, ei).stars || 0), 0);
const modTotal = m => MOD[m].topics.reduce((a, t) => a + t.ex.length, 0);
const modSolved = m => MOD[m].topics.reduce((a, _, ti) => a + solvedIn(m, ti), 0);
const modPhasesDone = m => MOD[m].topics.filter((t, ti) => solvedIn(m, ti) === t.ex.length).length;
const totalEx = MODS.reduce((a, m) => a + modTotal(m.id), 0);
const totalTopics = MODS.reduce((a, m) => a + m.topics.length, 0);
const diffOf = ei => ei < 5 ? 0 : ei < 10 ? 1 : 2;
const DIFF = ["Fácil", "Médio", "Desafio"];
const baseXP = ei => [10, 20, 30][diffOf(ei)];
const unlocked = (m, ti) => S.free || ti === 0 || solvedIn(m, ti - 1) >= 5;
const esc = s => String(s ?? "").replace(/[&<>"]/g, c => ({"&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;"}[c]));
const starsHTML = n => "★".repeat(n) + "<s>" + "★".repeat(3 - n) + "</s>";
const GC = ["var(--mid)", "var(--graphite)", "var(--slate)", "var(--dark)", "#2B6CB0", "#4A5568"];
const shuffle = a => { a = a.slice(); for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };

/* ===================== níveis, sequência e conquistas ===================== */
const LEVELS = [[0, "Iniciante"], [150, "Aprendiz"], [400, "Estagiário"], [800, "Júnior"], [1400, "Júnior II"], [2200, "Pleno"],
  [3200, "Pleno II"], [4400, "Sênior"], [5800, "Especialista"], [7400, "Arquiteto"], [9200, "Mestre Python"]];
function levelInfo(xp) {
  let i = 0; while (i + 1 < LEVELS.length && xp >= LEVELS[i + 1][0]) i++;
  const cur = LEVELS[i][0], nxt = LEVELS[i + 1] ? LEVELS[i + 1][0] : cur;
  return {n: i + 1, name: LEVELS[i][1], pct: nxt > cur ? (xp - cur) / (nxt - cur) * 100 : 100, toNext: nxt - xp, max: !LEVELS[i + 1]};
}
const today = () => new Date().toLocaleDateString("sv-SE");
function markDay() { if (!S.days.includes(today())) S.days.push(today()); }
function streak() {
  const set = new Set(S.days); let d = new Date(), n = 0;
  if (!set.has(today())) d.setDate(d.getDate() - 1);
  while (set.has(d.toLocaleDateString("sv-SE"))) { n++; d.setDate(d.getDate() - 1); }
  return n;
}
function stats() {
  const all = Object.values(S.ex);
  return {
    solved: all.filter(x => x.solved).length,
    perfect: all.filter(x => x.solved && x.stars === 3).length,
    firstTry: all.filter(x => x.solved && x.firstTry).length,
    hard: Object.entries(S.ex).filter(([k, x]) => x.solved && diffOf(+k.split(":")[2]) === 2).length,
    persist: all.some(x => x.solved && x.attempts >= 4),
    phasesDone: MODS.reduce((a, m) => a + modPhasesDone(m.id), 0),
    maps: Object.values(S.map).filter(x => x.done).length,
    quizzes: Object.values(S.quiz).filter(x => x.done).length,
    modDone: id => modPhasesDone(id) === MOD[id].topics.length,
    streak: streak()
  };
}
const ACH = [
  ["first", "🚀", "Primeiro passo", "Resolva seu primeiro exercício", s => s.solved >= 1],
  ["ten", "⚡", "Embalado", "Resolva 10 exercícios", s => s.solved >= 10],
  ["fifty", "🏃", "Maratonista", "Resolva 50 exercícios", s => s.solved >= 50],
  ["hundred", "💯", "Centurião", "Resolva 100 exercícios", s => s.solved >= 100],
  ["twohundred", "🏔️", "Alpinista", "Resolva 200 exercícios", s => s.solved >= 200],
  ["perfect", "⭐", "Sem rodinhas", "20 exercícios com 3 estrelas", s => s.perfect >= 20],
  ["firsttry", "🎯", "Na mosca", "Acerte 15 exercícios de primeira", s => s.firstTry >= 15],
  ["hard", "🧗", "Desafiante", "Resolva 10 desafios", s => s.hard >= 10],
  ["persist", "🛡️", "Persistente", "Resolva após 4 ou mais tentativas", s => s.persist],
  ["map1", "🧠", "Memória afiada", "Revele um mapa inteiro no modo memória", s => s.maps >= 1],
  ["map10", "🗺️", "Cartógrafo", "Revise 10 mapas no modo memória", s => s.maps >= 10],
  ["quiz1", "❓", "Rápido no gatilho", "Faça 5/6 ou mais em um quiz relâmpago", s => s.quizzes >= 1],
  ["quiz10", "🧩", "Quizzeiro", "Domine 10 quizzes", s => s.quizzes >= 10],
  ["phase", "🏁", "Fase concluída", "Complete os 15 exercícios de uma fase", s => s.phasesDone >= 1],
  ["streak3", "🔥", "Constância", "Estude 3 dias seguidos", s => s.streak >= 3],
  ["streak7", "📅", "Disciplina", "Estude 7 dias seguidos", s => s.streak >= 7],
  ["modF", "🧱", "Base sólida", "Conclua o módulo Fundamentos", s => s.modDone("fundamentos")],
  ["modB", "🧩", "Peças no lugar", "Conclua o módulo Básico", s => s.modDone("basico")],
  ["modI", "🚀", "Decolou", "Conclua o módulo Intermediário", s => s.modDone("intermediario")],
  ["master", "👑", "Mestre Python", "Conclua os 3 módulos", s => MOD_ORDER.every(s.modDone)],
];
function checkAch() {
  const s = stats(), novos = [];
  ACH.forEach(([id, ic, nm, ds, fn]) => { if (!S.achv[id] && fn(s)) { S.achv[id] = new Date().toISOString(); novos.push([ic, nm, ds]); } });
  return novos;
}
function gainXP(n, why) {
  const before = levelInfo(S.xp).n; S.xp += n; markDay();
  const novos = checkAch(); save(true); renderHUD();
  const after = levelInfo(S.xp);
  if (after.n > before) setTimeout(() => modal(`<div class="big">🎉</div><h3>Subiu para o nível ${after.n}!</h3><p>Agora você é <b>${after.name}</b>.</p><button class="btn acc" data-close>Bora!</button>`), 700);
  else if (novos.length) setTimeout(() => modal(`<div class="big">${novos[0][0]}</div><h3>Conquista desbloqueada!</h3><p><b>${novos[0][1]}</b><br><span class="muted">${novos[0][2]}</span></p><button class="btn acc" data-close>Show!</button>`), 700);
  if (why) toast(`+${n} XP • ${why}`);
}

/* ===================== UI utilitários ===================== */
const $ = s => document.querySelector(s);
function toast(msg, ms = 2600) { const t = $("#toast"); t.innerHTML = msg; t.classList.add("show"); clearTimeout(t._t); t._t = setTimeout(() => t.classList.remove("show"), ms); }
function modal(html) { $("#mbox").innerHTML = html; $("#modal").classList.add("show"); }
$("#modal").addEventListener("click", e => { if (e.target.id === "modal" || e.target.dataset.close !== undefined) $("#modal").classList.remove("show"); });
function confirmBox(title, text, okLbl, cb) {
  modal(`<div class="big">🤔</div><h3>${title}</h3><p class="muted">${text}</p><div class="row" style="justify-content:center"><button class="btn alt" data-close>Cancelar</button><button class="btn" id="mOk">${okLbl}</button></div>`);
  $("#mOk").onclick = () => { $("#modal").classList.remove("show"); cb(); };
}
function confetti() {
  if (matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  const cols = ["#4FA3E0", "#1E5AA8", "#F2C14E", "#3DDC97", "#8DB3E2", "#ECE6DC"];
  for (let i = 0; i < 70; i++) {
    const d = document.createElement("div"); d.className = "confetti";
    d.style.left = Math.random() * 100 + "vw"; d.style.background = cols[i % cols.length];
    d.style.animationDuration = 1.6 + Math.random() * 1.6 + "s"; d.style.animationDelay = Math.random() * .4 + "s";
    document.body.appendChild(d); setTimeout(() => d.remove(), 3800);
  }
}
function renderHUD() {
  const L = levelInfo(S.xp);
  $("#lvlNum").textContent = L.n; $("#lvlName").textContent = `Nv. ${L.n} • ${L.name}`;
  $("#xpBar").style.width = L.pct + "%";
  $("#xpTxt").textContent = L.max ? `${S.xp} XP • nível máximo` : `${S.xp} XP • faltam ${L.toNext}`;
  const sk = streak(); $("#streak").textContent = sk; $("#streakLbl").innerHTML = sk === 1 ? "&nbsp;dia" : "&nbsp;dias";
}
function ring(p, label, color) { return `<div class="ring" style="--p:${p};--c:${color || "var(--mid)"}"><span>${label}</span></div>`; }
function copyText(txt) { navigator.clipboard?.writeText(txt).then(() => toast("Copiado ⧉"), () => toast("Não foi possível copiar")); }

/* ===================== roteamento (hash) ===================== */
let CUR = {view: "home"};
function hashOf(r) {
  switch (r.view) {
    case "mod": return `#/m/${r.m}`;
    case "topic": return `#/m/${r.m}/${r.ti}` + (r.tab ? `?${r.tab}` : "");
    case "ex": return `#/m/${r.m}/${r.ti}/${r.ei}`;
    case "home": return "#/";
    default: return "#/" + r.view;
  }
}
function parseHash() {
  const h = location.hash.replace(/^#\/?/, ""), [path, q] = h.split("?"), p = path.split("/").filter(Boolean);
  if (p[0] === "m" && MOD[p[1]]) {
    const m = p[1], ti = p[2] !== undefined ? +p[2] : null, ei = p[3] !== undefined ? +p[3] : null;
    if (ti !== null && MOD[m].topics[ti]) {
      if (ei !== null && MOD[m].topics[ti].ex[ei]) return {view: "ex", m, ti, ei};
      return {view: "topic", m, ti, tab: q || null};
    }
    return {view: "mod", m};
  }
  if (["ach", "prog", "rev"].includes(p[0])) return {view: p[0]};
  return {view: "home"};
}
function go(r, opts = {}) {
  const h = hashOf(r);
  if (location.hash !== h) { opts.fromGo = true; history.pushState(null, "", h); }
  render(r, opts);
}
window.addEventListener("popstate", () => render(parseHash()));
window.addEventListener("hashchange", () => { const r = parseHash(); if (hashOf(r) !== hashOf(CUR)) render(r); });
function render(r, opts = {}) {
  flushDraft();
  if ((r.view === "topic" || r.view === "ex") && !unlocked(r.m, r.ti)) { toast("🔒 Fase bloqueada: resolva 5 exercícios da anterior (ou ative o Modo livre)."); r = {view: "mod", m: r.m}; history.replaceState(null, "", hashOf(r)); }
  CUR = r;
  if (["mod", "topic", "ex"].includes(r.view)) { S.last = Object.assign({}, r); save(); }
  setNav(r.view);
  document.onkeydown = null; CM = null; draftKey = null;
  const app = $("#app"); app.innerHTML = "";
  ({home: viewHome, mod: viewMod, topic: viewTopic, ex: viewEx, ach: viewAch, prog: viewProg, rev: viewRev})[r.view](app, r);
  app.firstElementChild && app.firstElementChild.classList.add("view");
  if (!opts.keepScroll) window.scrollTo({top: 0});
}
function setNav(v) { document.querySelectorAll("[data-go]").forEach(b => b.classList.toggle("on", b.dataset.go === v || (["mod", "topic"].includes(v) && b.dataset.go === "home") || (v === "ex" && b.dataset.go === "ex"))); }
document.querySelectorAll("[data-go]").forEach(b => b.onclick = () => {
  const g = b.dataset.go;
  if (g === "ex") { const L = S.last; if (L && L.view === "ex" && MOD[L.m]) go({view: "ex", m: L.m, ti: L.ti, ei: L.ei}); else go(recommend()); }
  else go({view: g});
});
$("#home").onclick = () => go({view: "home"});

function recommendIn(m) {
  const T = MOD[m].topics;
  for (let ti = 0; ti < T.length; ti++) {
    if (!unlocked(m, ti)) break;
    const tried = T[ti].ex.findIndex((_, ei) => peek(m, ti, ei).attempts && !peek(m, ti, ei).solved);
    if (tried >= 0) return {view: "ex", m, ti, ei: tried};
    const nx = T[ti].ex.findIndex((_, ei) => !peek(m, ti, ei).solved);
    if (nx >= 0) return {view: "ex", m, ti, ei: nx};
  }
  return null;
}
function recommend() {
  const L = S.last;
  if (L && MOD[L.m]) { const r = recommendIn(L.m); if (r) return r; }
  for (const m of MOD_ORDER) { const r = recommendIn(m); if (r) return r; }
  return {view: "ex", m: MOD_ORDER[0], ti: 0, ei: 0};
}
function labelOf(r) { return r && r.view === "ex" ? `${MOD[r.m].name} › ${topic(r.m, r.ti).name} › ${r.ei + 1}. ${topic(r.m, r.ti).ex[r.ei].t}` : ""; }

/* ===================== PAINEL (3 módulos) ===================== */
function viewHome(app) {
  const s = stats(), rec = recommend(), L = S.last;
  const hasResume = S.updated && L && MOD[L.m] && L.view === "ex";
  const el = document.createElement("div");
  el.innerHTML = `
  <div class="resume" ${hasResume ? "" : "hidden"}>📌<span style="flex:1">Você parou em <b>${hasResume ? esc(labelOf(L)) : ""}</b></span><button class="btn" id="contBtn">Continuar ▶</button></div>
  <div class="hero">
    <div class="welcome"><h2>Bem-vindo ao Python Quest! 🐍</h2>
      <p>Três módulos, <b>${totalTopics} fases</b> e <b>${totalEx} exercícios</b> corrigidos por testes automáticos com Python de verdade rodando no navegador.
      Em cada fase: mapa mental interativo, quiz relâmpago, flashcards e exercícios fáceis, médios e desafios.</p>
      <div class="hacts"><button class="btn acc" id="recBtn">▶ Próximo recomendado</button>
      <button class="btn ghost" id="revBtn">🔁 Revisar erros</button></div>
      <p style="margin:10px 0 0;font-size:.8rem;color:var(--light)">Próximo: ${esc(labelOf(rec))}</p></div>
    <div class="stats4">
      <div class="stat"><b>${s.solved}/${totalEx}</b><small>exercícios resolvidos</small></div>
      <div class="stat"><b>${s.phasesDone}/${totalTopics}</b><small>fases concluídas</small></div>
      <div class="stat"><b>${s.maps + s.quizzes}</b><small>mapas e quizzes dominados</small></div>
      <div class="stat"><b>${Object.keys(S.achv).length}/${ACH.length}</b><small>conquistas</small></div>
    </div>
  </div>
  <div class="sec-title"><h2>📚 Módulos</h2><span class="pill gray">recomendado: na ordem</span></div>
  <div class="modgrid">${MODS.map((m, i) => {
    const tot = modTotal(m.id), sol = modSolved(m.id), done = modPhasesDone(m.id);
    const st = m.topics.reduce((a, _, ti) => a + starsIn(m.id, ti), 0);
    const r = recommendIn(m.id);
    return `<div class="modcard" data-m="${m.id}" style="--mc:${m.color}" role="button" tabindex="0">
      <div class="mtop"><div class="micon">${m.icon}</div><div><small>Módulo ${i + 1}</small><h3>${esc(m.name)}</h3></div></div>
      <div class="mbody"><p class="mdesc">${esc(m.desc)}</p>
        <div class="mstats"><div><b>${m.topics.length}</b><small>fases</small></div><div><b>${sol}/${tot}</b><small>exercícios</small></div><div><b>⭐ ${st}</b><small>estrelas</small></div></div>
        <div><div class="mbar"><i style="width:${tot ? sol / tot * 100 : 0}%"></i></div><small class="muted">${Math.round(tot ? sol / tot * 100 : 0)}% concluído • ${done} fase(s) completa(s)</small></div>
        <div class="mfoot"><button class="btn" data-open="${m.id}">🗺️ Abrir trilha</button>${r ? `<button class="btn acc" data-cont="${m.id}">▶ Continuar</button>` : `<span class="pill ok">✓ Completo</span>`}</div>
      </div></div>`;
  }).join("")}</div>
  <div class="two">
    <div class="card"><h3 style="margin-top:0">🎮 Como jogar</h3><ol class="hot">
      <li>Abra uma fase e estude o <b>mapa mental</b>. No <b>modo memória</b>, as descrições ficam escondidas: lembre e toque para revelar (+10 XP).</li>
      <li>Faça o <b>quiz relâmpago</b> (+15 XP com 5 ou mais acertos de 6) e revise com os <b>flashcards</b>.</li>
      <li>Resolva os exercícios: <b>Executar</b> roda seu código; <b>Verificar</b> roda os testes com outros valores.</li>
      <li>5 exercícios resolvidos liberam a próxima fase. Dicas e solução custam estrelas.</li></ol></div>
    <div class="card"><h3 style="margin-top:0">💡 Bom saber</h3><ul style="margin:0;padding-left:18px;font-size:.92rem">
      <li>O Python roda no seu navegador (Pyodide). Na 1ª vez precisa de internet; depois fica em cache.</li>
      <li>Selenium e envio de e-mail são <b>simulados</b> (o código é o mesmo que você usará no seu PC).</li>
      <li>SQL usa <b>SQLite</b> no navegador; a sintaxe do <code>pyodbc</code> (SQL Server) é a mesma.</li>
      <li>Progresso salvo automaticamente. Faça backup em <b>Progresso</b>.</li></ul></div>
  </div>`;
  app.appendChild(el);
  el.querySelectorAll(".modcard").forEach(c => {
    c.onclick = e => { if (e.target.closest("[data-cont]")) return; go({view: "mod", m: c.dataset.m}); };
    c.onkeydown = e => { if (e.key === "Enter") go({view: "mod", m: c.dataset.m}); };
  });
  el.querySelectorAll("[data-cont]").forEach(b => b.onclick = () => go(recommendIn(b.dataset.cont)));
  $("#recBtn").onclick = () => go(rec);
  if (hasResume) $("#contBtn").onclick = () => go(L);
  $("#revBtn").onclick = () => go({view: "rev"});
}

/* ===================== TRILHA DO MÓDULO ===================== */
function viewMod(app, r) {
  const m = r.m, M = MOD[m], rec = recommendIn(m);
  const el = document.createElement("div");
  el.innerHTML = `
  <div class="crumbs"><button id="bk">← Painel</button><span>›</span><span>${esc(M.name)}</span></div>
  <div class="hero" style="grid-template-columns:1fr">
    <div class="welcome" style="background:linear-gradient(135deg,${M.color},var(--navy))"><h2>${M.icon} ${esc(M.name)}</h2><p>${esc(M.desc)}</p>
      <div class="hacts">${rec ? `<button class="btn acc" id="recBtn">▶ Próximo: ${esc(topic(m, rec.ti).ex[rec.ei].t)}</button>` : `<span class="pill ok">✓ Módulo completo!</span>`}
      <span class="pill gray">${modSolved(m)}/${modTotal(m)} exercícios</span></div></div>
  </div>
  <div class="maphead"><h2>🗺️ Trilha de fases</h2>
    <label class="toggle" title="Libera todas as fases sem precisar concluir as anteriores"><input type="checkbox" id="freeT" ${S.free ? "checked" : ""}>Modo livre</label></div>
  <p class="muted" style="margin-top:-6px">Resolva <b>5 exercícios</b> de uma fase para desbloquear a próxima. 🧠 = mapa revisado • ❓ = quiz dominado.</p>
  <div class="trail">${M.topics.map((t, ti) => {
    const n = solvedIn(m, ti), lock = !unlocked(m, ti), done = n === t.ex.length;
    const mp = S.map[tk(m, ti)] && S.map[tk(m, ti)].done, qz = S.quiz[tk(m, ti)] && S.quiz[tk(m, ti)].done;
    return `<button class="world ${lock ? "locked" : ""} ${done ? "done" : ""} ${rec && rec.ti === ti ? "cur" : ""}" data-ti="${ti}" style="--c:${ti % 3 === 0 ? "var(--mid)" : ti % 3 === 1 ? "var(--graphite)" : "var(--sky)"}">
      <div class="ring" style="--p:${n / t.ex.length * 100}"><span>${String(ti + 1).padStart(2, "0")}</span></div>
      <div class="wt"><span class="src">${esc(t.src || "")}</span><b>${esc(t.name)}</b><small>${n}/${t.ex.length} resolvidos • ⭐ ${starsIn(m, ti)}/${t.ex.length * 3}</small><br><small>${esc(t.cdesc)}</small>
        <div class="badges">${mp ? '<span class="pill ok">🧠 mapa</span>' : ""}${qz ? '<span class="pill ok">❓ quiz</span>' : ""}${t.origem === "reaproveitada" ? "" : '<span class="pill">novo</span>'}</div></div>
      ${lock ? '<span class="lock">🔒</span>' : done ? '<span class="lock">🏅</span>' : ""}</button>`;
  }).join("")}</div>`;
  app.appendChild(el);
  $("#bk").onclick = () => go({view: "home"});
  if (rec) $("#recBtn").onclick = () => go(rec);
  el.querySelectorAll(".world").forEach(w => w.onclick = () => {
    const ti = +w.dataset.ti;
    if (!unlocked(m, ti)) { toast(`🔒 Resolva 5 exercícios de <b>${esc(topic(m, ti - 1).name)}</b> para liberar (ou ative o Modo livre).`); return; }
    go({view: "topic", m, ti});
  });
  $("#freeT").onchange = e => { S.free = e.target.checked; save(); render({view: "mod", m}, {keepScroll: true}); toast(S.free ? "🔓 Todas as fases liberadas" : "🔒 Modo campanha ativado"); };
}

/* ===================== FASE ===================== */
const LAYOUTS = [["radial", "◎ Radial"], ["arvore", "🌳 Árvore"], ["chaves", "{ } Chaves"], ["bolhas", "🫧 Bolhas"], ["fluxo", "⬇ Fluxo"], ["cmp", "▦ Comparação"]];
function viewTopic(app, r) {
  const m = r.m, ti = r.ti, t = topic(m, ti), tab = r.tab || "mapa";
  const el = document.createElement("div");
  el.innerHTML = `
  <div class="crumbs"><button id="bkHome">Painel</button><span>›</span><button id="bkMod">${esc(MOD[m].name)}</button><span>›</span><span>Fase ${ti + 1}</span></div>
  <div class="thead"><div style="flex:1;min-width:220px"><h2>${esc(t.name)}</h2><small class="muted">${esc(t.src || "")} • ${esc(t.cdesc)}</small></div>
    <span class="pill gray">${solvedIn(m, ti)}/${t.ex.length} • ⭐ ${starsIn(m, ti)}</span></div>
  <div class="tabs2" id="tabs2">
    <button data-t="mapa">🧠 Mapa mental</button><button data-t="quiz">⚡ Quiz relâmpago</button>
    <button data-t="cards">🃏 Flashcards</button><button data-t="ex">💻 Exercícios (${solvedIn(m, ti)}/${t.ex.length})</button></div>
  <div id="tb"></div>`;
  app.appendChild(el);
  $("#bkHome").onclick = () => go({view: "home"});
  $("#bkMod").onclick = () => go({view: "mod", m});
  el.querySelectorAll("#tabs2 button").forEach(b => b.classList.toggle("on", b.dataset.t === tab));
  el.querySelectorAll("#tabs2 button").forEach(b => b.onclick = () => go({view: "topic", m, ti, tab: b.dataset.t}, {keepScroll: true}));
  const box = $("#tb");
  ({mapa: tabMapa, quiz: tabQuiz, cards: tabCards, ex: tabEx})[tab] ? ({mapa: tabMapa, quiz: tabQuiz, cards: tabCards, ex: tabEx})[tab](box, m, ti) : tabMapa(box, m, ti);
}

/* ---------- mapa mental interativo ---------- */
function leafList(t) { const L = []; t.groups.forEach((g, gi) => g[1].forEach((l, li) => L.push({id: gi + "-" + li, gi, k: l[0], v: l[1], g: g[0]}))); return L; }
function tabMapa(box, m, ti) {
  const t = topic(m, ti), key = tk(m, ti);
  const layout = S.layout[key] || t.map || "arvore";
  const ms = S.map[key] || (S.map[key] = {seen: [], done: false});
  const leaves = leafList(t);
  box.innerHTML = `
  <div class="mapbar"><div class="seg" id="lay">${LAYOUTS.map(([k, n]) => `<button data-l="${k}">${n}</button>`).join("")}</div>
    <label class="toggle" title="Esconde as descrições: tente lembrar e toque para revelar"><input type="checkbox" id="memoT" ${S.memo ? "checked" : ""}>🧠 Modo memória</label>
    <span class="memo-info" id="memoInfo"></span></div>
  <div class="mapwrap ${S.memo ? "memo" : ""}" id="mw"></div>
  <div class="two"><div class="card"><h3 style="margin-top:0">🎯 O que mais importa</h3><ol class="hot">${t.hot.map(h => `<li>${esc(h)}</li>`).join("")}</ol>
      ${t.trap ? `<div class="trap"><b>⚠ ARMADILHA COMUM</b>${esc(t.trap)}</div>` : ""}</div>
    <div class="card"><h3 style="margin-top:0">🧪 Exemplos de código</h3>${t.examples.map((e, i) => `<p class="muted" style="margin:0 0 6px;font-size:.8rem;font-weight:700">${esc(e[0])}</p><div class="codebox"><pre class="code">${esc(e[1])}</pre><button class="copybtn" data-cp="${i}">⧉ copiar</button></div>`).join('<div style="height:10px"></div>')}</div></div>
  <div class="row" style="margin-top:16px"><button class="btn acc" id="startEx">💻 Ir para os exercícios</button><button class="btn ghost" id="toQuiz">⚡ Fazer o quiz</button></div>`;
  box.querySelectorAll("[data-cp]").forEach(b => b.onclick = () => copyText(t.examples[+b.dataset.cp][1]));
  box.querySelectorAll("#lay button").forEach(b => { b.classList.toggle("on", b.dataset.l === layout); b.onclick = () => { S.layout[key] = b.dataset.l; save(); tabMapa(box, m, ti); }; });
  $("#memoT").onchange = e => { S.memo = e.target.checked; save(); tabMapa(box, m, ti); };
  $("#startEx").onclick = () => { const nx = t.ex.findIndex((_, ei) => !peek(m, ti, ei).solved); go({view: "ex", m, ti, ei: nx < 0 ? 0 : nx}); };
  $("#toQuiz").onclick = () => go({view: "topic", m, ti, tab: "quiz"});
  const mw = $("#mw");
  const updInfo = () => {
    const n = ms.seen.filter(id => leaves.some(l => l.id === id)).length;
    $("#memoInfo").innerHTML = S.memo ? `<div class="bar"><i style="width:${n / leaves.length * 100}%;background:${ms.done ? "var(--ok)" : "var(--mid)"}"></i></div>${n}/${leaves.length} revelados${ms.done ? " • ✓ revisado" : ""}` : `<span class="muted">Toque nos itens para destacar</span>`;
  };
  const reveal = (id, node) => {
    if (node) { node.classList.add("seen", "flash"); setTimeout(() => node.classList.remove("flash"), 600); }
    if (!S.memo || ms.seen.includes(id)) return;
    ms.seen.push(id); save(); updInfo();
    if (!ms.done && leaves.every(l => ms.seen.includes(l.id))) { ms.done = true; confetti(); gainXP(10, "mapa revisado no modo memória 🧠"); }
  };
  const isSeen = id => !S.memo || ms.seen.includes(id);
  const lfHTML = (l, tag = "div", extra = "") => `<${tag} class="lf ${isSeen(l.id) ? "seen" : ""} ${extra}" data-id="${l.id}"><b>${esc(l.k)}</b><span class="d">${esc(l.v)}</span></${tag}>`;
  const bind = root => root.querySelectorAll(".lf").forEach(n => n.onclick = () => { if (n.closest(".bub-l")) n.classList.toggle("open"); reveal(n.dataset.id, n); });
  const R = {
    arvore() {
      mw.innerHTML = `<div class="tree"><div class="mm-center"><b>${esc(t.name.toUpperCase())}</b><span>${esc(t.cdesc)}</span></div>
        <div class="groups">${t.groups.map((g, gi) => `<div class="grp" style="--gc:${GC[gi % GC.length]}"><h4>${esc(g[0])}</h4>${leaves.filter(l => l.gi === gi).map(l => lfHTML(l, "div", "leaf")).join("")}</div>`).join("")}</div></div>`;
      mw.querySelectorAll(".grp h4").forEach(h => h.onclick = () => h.parentElement.classList.toggle("closed"));
    },
    chaves() {
      mw.innerHTML = `<div class="braces"><div class="bcenter">${esc(t.name)}<small>${esc(t.short || "")}</small></div><div class="brace"></div>
        <div class="bgroups">${t.groups.map((g, gi) => `<div class="bg" style="--gc:${GC[gi % GC.length]}"><div class="bname">${esc(g[0])}</div><div class="brace"></div><div class="bleaves">${leaves.filter(l => l.gi === gi).map(l => lfHTML(l)).join("")}</div></div>`).join("")}</div></div>`;
    },
    bolhas() {
      mw.innerHTML = `<div class="bubbles"><div class="bub-center">${esc(t.name)}</div><div class="bub-groups">${t.groups.map((g, gi) => `<div class="bub-g" style="--gc:${GC[gi % GC.length]}"><b>${esc(g[0])}</b><div class="bub-l">${leaves.filter(l => l.gi === gi).map(l => lfHTML(l)).join("")}</div></div>`).join("")}</div>
        <p class="rhint">Toque numa bolha para ver a explicação.</p></div>`;
    },
    fluxo() {
      mw.innerHTML = `<div class="flow"><div class="fstart">${esc(t.name)}</div>${t.groups.map((g, gi) => `<div class="farrow"></div><div class="fstep" style="--gc:${GC[gi % GC.length]}"><b><i>${gi + 1}</i>${esc(g[0])}</b><div class="fleaves">${leaves.filter(l => l.gi === gi).map(l => lfHTML(l)).join("")}</div></div>`).join("")}</div>`;
    },
    cmp() {
      const rows = Math.max(...t.groups.map(g => g[1].length));
      mw.innerHTML = `<div class="cmp"><table><thead><tr>${t.groups.map((g, gi) => `<th style="--gc:${GC[gi % GC.length]};background:${GC[gi % GC.length]}">${esc(g[0])}</th>`).join("")}</tr></thead><tbody>
        ${Array.from({length: rows}, (_, ri) => `<tr>${t.groups.map((g, gi) => { const l = leaves.find(x => x.id === gi + "-" + ri); return `<td>${l ? lfHTML(l, "span") : ""}</td>`; }).join("")}</tr>`).join("")}</tbody></table></div>`;
    },
    radial() {
      const W = 900, H = 600, cx = W / 2, cy = H / 2, G = t.groups.length, small = mw.clientWidth < 620, FS = small ? 30 : 16, RH = small ? 64 : 42;
      const rx = 300, ry = 205, gpos = t.groups.map((g, gi) => { const a = -Math.PI / 2 + gi * 2 * Math.PI / G; return {a, x: cx + rx * Math.cos(a), y: cy + ry * Math.sin(a)}; });
      let svg = `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Mapa mental radial de ${esc(t.name)}">`;
      gpos.forEach((p, gi) => { svg += `<line x1="${cx}" y1="${cy}" x2="${p.x}" y2="${p.y}" stroke="#8DB3E2" stroke-width="3"/>`; });
      gpos.forEach((p, gi) => {
        const ls = leaves.filter(l => l.gi === gi), n = ls.length;
        ls.forEach((l, li) => {
          const spread = 0.62, a = p.a + (n === 1 ? 0 : (li - (n - 1) / 2) * spread / Math.max(1, (n - 1) / 2) * 0.9);
          const lx = p.x + 120 * Math.cos(a), ly = p.y + 74 * Math.sin(a);
          const anchor = Math.cos(a) > .25 ? "start" : Math.cos(a) < -.25 ? "end" : "middle";
          const tx = lx + (anchor === "start" ? 10 : anchor === "end" ? -10 : 0), ty = ly + (anchor === "middle" ? (Math.sin(a) > 0 ? 22 : -12) : 4);
          const label = l.k.length > 26 ? l.k.slice(0, 25) + "…" : l.k;
          svg += `<line x1="${p.x}" y1="${p.y}" x2="${lx}" y2="${ly}" stroke="#D5CDBF" stroke-width="2"/>
            <g class="ldot ${isSeen(l.id) ? "seen" : ""}" data-id="${l.id}" data-g="${gi}"><circle cx="${lx}" cy="${ly}" r="${small ? 13 : 8}" fill="#8DB3E2" stroke="#fff" stroke-width="2"/>
            <text class="ltxt" x="${tx}" y="${ty}" text-anchor="${anchor}" font-size="14" fill="#2F3640">${esc(label)}</text></g>`;
        });
      });
      gpos.forEach((p, gi) => {
        const name = t.groups[gi][0], lbl = name.length > 22 ? name.slice(0, 21) + "…" : name, w = Math.max(110, lbl.length * FS * 0.6 + 30);
        svg += `<g class="gnode" data-g="${gi}"><rect x="${p.x - w / 2}" y="${p.y - RH / 2}" width="${w}" height="${RH}" rx="${RH / 2}" fill="${["#1E5AA8", "#2F3640", "#5C6773", "#13315C", "#2B6CB0", "#4A5568"][gi % 6]}"/>
          <text x="${p.x}" y="${p.y + FS * 0.36}" text-anchor="middle" font-size="${FS}" font-weight="800" fill="#fff">${esc(lbl)}</text></g>`;
      });
      svg += `<circle cx="${cx}" cy="${cy}" r="78" fill="#0B2545"/><foreignObject x="${cx - 70}" y="${cy - 40}" width="140" height="80"><div xmlns="http://www.w3.org/1999/xhtml" style="height:80px;display:flex;align-items:center;justify-content:center;text-align:center;color:#fff;font:800 ${small ? 19 : 15}px system-ui,sans-serif;line-height:1.1">${esc(t.name)}</div></foreignObject></svg>`;
      mw.innerHTML = `<div class="radial">${svg}<p class="rhint">Toque num ramo para abrir os detalhes.</p><div class="rdetail" id="rdet"></div></div>`;
      const showG = gi => {
        mw.querySelectorAll(".gnode").forEach(n => n.classList.toggle("sel", +n.dataset.g === gi));
        const d = $("#rdet"); d.innerHTML = leaves.filter(l => l.gi === gi).map(l => lfHTML(l)).join(""); bind(d);
      };
      mw.querySelectorAll(".gnode").forEach(n => n.onclick = () => showG(+n.dataset.g));
      mw.querySelectorAll(".ldot").forEach(n => n.onclick = () => {
        showG(+n.dataset.g);
        const node = $(`#rdet .lf[data-id="${n.dataset.id}"]`); if (node) { reveal(n.dataset.id, node); node.scrollIntoView({behavior: "smooth", block: "nearest"}); }
        n.classList.add("seen");
      });
      const svgEl = mw.querySelector("svg");
      try { const bb = svgEl.getBBox(); if (bb.width) svgEl.setAttribute("viewBox", `${bb.x - 16} ${bb.y - 16} ${bb.width + 32} ${bb.height + 32}`); } catch (e) {}
      showG(0);
    }
  };
  (R[layout] || R.arvore)();
  bind(mw); updInfo();
}

/* ---------- quiz relâmpago (gerado do mapa) ---------- */
function makeQuiz(t) {
  const L = leafList(t), qs = [];
  shuffle(L).slice(0, 6).forEach((l, i) => {
    const others = shuffle(L.filter(x => x.id !== l.id));
    if (i % 2 === 0) {
      const opts = shuffle([l.k, ...others.map(o => o.k).filter(k => k !== l.k).slice(0, 3)]);
      qs.push({q: `Qual item corresponde a: “${l.v}”?`, opts, ans: l.k, g: l.g});
    } else {
      const opts = shuffle([l.v, ...others.map(o => o.v).filter(v => v !== l.v).slice(0, 3)]);
      qs.push({q: `O que significa “${l.k}”?`, opts, ans: l.v, g: l.g});
    }
  });
  return qs;
}
function tabQuiz(box, m, ti) {
  const t = topic(m, ti), key = tk(m, ti), qz = S.quiz[key] || (S.quiz[key] = {best: 0, done: false, plays: 0});
  let qs = makeQuiz(t), i = 0, hits = 0;
  const step = () => {
    if (i >= qs.length) return end();
    const q = qs[i];
    box.innerHTML = `<div class="quiz"><div class="qhead"><b>Pergunta ${i + 1}/${qs.length}</b><div class="bar"><i style="width:${i / qs.length * 100}%"></i></div><span class="pill">✔ ${hits}</span></div>
      <div class="qcard"><span class="pill gray">${esc(q.g)}</span><p class="qq" style="margin-top:10px">${esc(q.q)}</p>
      <div class="qopts">${q.opts.map((o, k) => `<button class="qopt" data-k="${k}">${esc(o)}</button>`).join("")}</div>
      <div id="qfb" style="margin-top:12px"></div></div></div>`;
    box.querySelectorAll(".qopt").forEach(b => b.onclick = () => {
      const ok = q.opts[+b.dataset.k] === q.ans; if (ok) hits++;
      box.querySelectorAll(".qopt").forEach(x => { x.disabled = true; if (q.opts[+x.dataset.k] === q.ans) x.classList.add("right"); });
      if (!ok) b.classList.add("wrong");
      $("#qfb").innerHTML = `<div class="row" style="justify-content:space-between;align-items:center"><b style="color:${ok ? "var(--ok)" : "var(--bad)"}">${ok ? "✔ Isso!" : "✗ Quase: a certa está em verde."}</b><button class="btn" id="qn">${i + 1 < qs.length ? "Próxima ▶" : "Ver resultado"}</button></div>`;
      $("#qn").onclick = () => { i++; step(); }; $("#qn").focus();
    });
  };
  const end = () => {
    qz.plays++; const first = !qz.done && hits >= 5; qz.best = Math.max(qz.best, hits);
    if (first) { qz.done = true; confetti(); gainXP(15, "quiz dominado ⚡"); } else { markDay(); save(); }
    box.innerHTML = `<div class="quiz"><div class="qcard qend"><div class="big">${hits >= 5 ? "🏆" : hits >= 3 ? "👍" : "📚"}</div><h3>${hits}/${qs.length} acertos</h3>
      <p class="muted">${hits >= 5 ? (first ? "Quiz dominado! +15 XP." : "Mandou bem de novo!") : "Revise o mapa mental e tente de novo: 5 acertos dominam o quiz."}<br>Melhor resultado: ${qz.best}/6 • Jogadas: ${qz.plays}</p>
      <div class="row" style="justify-content:center"><button class="btn acc" id="again">🔄 Jogar de novo</button><button class="btn alt" id="toMap">🧠 Mapa</button><button class="btn" id="toEx">💻 Exercícios</button></div></div></div>`;
    $("#again").onclick = () => { qs = makeQuiz(t); i = 0; hits = 0; step(); };
    $("#toMap").onclick = () => go({view: "topic", m, ti, tab: "mapa"});
    $("#toEx").onclick = () => go({view: "topic", m, ti, tab: "ex"});
  };
  step();
}

/* ---------- flashcards ---------- */
function tabCards(box, m, ti) {
  const t = topic(m, ti);
  let cards = leafList(t).map(l => ({f: l.k, b: l.v, g: l.g}));
  if (t.trap) cards.push({f: "⚠ Armadilha", b: t.trap, g: "Cuidado"});
  let i = 0;
  const draw = () => {
    const c = cards[i];
    box.innerHTML = `<div class="fc-wrap"><div class="fc" id="fc" tabindex="0"><div class="face front"><small>${esc(c.g)}</small><b>${esc(c.f)}</b><small style="margin-top:14px;color:var(--pale)">toque para virar</small></div>
      <div class="face back">${esc(c.b)}<small>${esc(c.g)}</small></div></div>
      <div class="fc-nav"><button class="btn alt" id="fp">◀</button><span class="pill gray">${i + 1}/${cards.length}</span><button class="btn alt" id="fn">▶</button><button class="btn ghost" id="fs">🔀 Embaralhar</button></div>
      <p class="rhint">Atalhos: espaço vira, ← → navegam.</p></div>`;
    const fc = $("#fc"); fc.onclick = () => fc.classList.toggle("flip");
    $("#fp").onclick = () => { i = (i - 1 + cards.length) % cards.length; draw(); };
    $("#fn").onclick = () => { i = (i + 1) % cards.length; draw(); };
    $("#fs").onclick = () => { cards = shuffle(cards); i = 0; draw(); toast("Cartas embaralhadas"); };
  };
  document.onkeydown = e => {
    if (CUR.view !== "topic" || !$("#fc")) return;
    if (e.key === " ") { e.preventDefault(); $("#fc").classList.toggle("flip"); }
    if (e.key === "ArrowRight") $("#fn").click(); if (e.key === "ArrowLeft") $("#fp").click();
  };
  draw();
}

/* ---------- lista de exercícios ---------- */
function tabEx(box, m, ti) {
  const t = topic(m, ti);
  let f = "all";
  const draw = () => {
    box.innerHTML = `<div class="filters"><div class="seg" id="flt">${[["all", "Todos"], ["0", "Fáceis"], ["1", "Médios"], ["2", "Desafios"], ["todo", "Pendentes"]].map(([k, n]) => `<button data-f="${k}" class="${f === k ? "on" : ""}">${n}</button>`).join("")}</div></div>
    <div class="exlist">${t.ex.map((x, ei) => {
      const st = peek(m, ti, ei), cls = st.solved ? "solved" : st.attempts ? "tried" : "";
      if (f === "todo" && st.solved) return ""; if (["0", "1", "2"].includes(f) && diffOf(ei) !== +f) return "";
      return `<button class="exc ${cls}" data-ei="${ei}"><div class="num">${st.solved ? "✓" : ei + 1}</div><div class="et"><b>${esc(x.t)}</b>
        <span class="diff d${diffOf(ei)}">${DIFF[diffOf(ei)]}</span><span class="muted" style="font-size:.75rem"> • ${baseXP(ei)} XP</span></div><div class="stars">${st.solved ? starsHTML(st.stars) : ""}</div></button>`;
    }).join("") || '<p class="muted">Nada aqui. 🎉</p>'}</div>`;
    box.querySelectorAll("#flt button").forEach(b => b.onclick = () => { f = b.dataset.f; draw(); });
    box.querySelectorAll(".exc").forEach(b => b.onclick = () => go({view: "ex", m, ti, ei: +b.dataset.ei}));
  };
  draw();
}

/* ===================== EXERCÍCIO ===================== */
let CM = null, draftKey = null, draftT;
function flushDraft() { if (CM && draftKey) { const [m, ti, ei] = draftKey.split(":"); exState(m, +ti, +ei).code = CM.getValue(); } }
const PKG_RX = [["numpy", /\bnumpy\b|\bnp\./], ["pandas", /\bpandas\b|\bpd\./], ["matplotlib", /\bmatplotlib\b|\bplt\./], ["beautifulsoup4", /\bbs4\b|BeautifulSoup/], ["sqlite3", /\bsqlite3\b/], ["seaborn", /\bseaborn\b|\bsns\./]];
function pkgsFor(x, code) { const txt = (code || "") + "\n" + (x.s || ""); return PKG_RX.filter(([, rx]) => rx.test(txt)).map(([n]) => n); }
function starterPy(x) {
  const vars = [...(x.s || "").matchAll(/^([A-Za-z_]\w*)\s*=/gm)].map(m => m[1]).filter(v => !["pd", "np", "plt", "sns"].includes(v));
  return "# Escreva seu código abaixo." + (vars.length ? "\n# Já disponível: " + [...new Set(vars)].slice(0, 8).join(", ") : "") + "\n\n";
}
function viewEx(app, r) {
  const m = r.m, ti = r.ti, ei = r.ei, t = topic(m, ti), x = t.ex[ei];
  const st = exState(m, ti, ei), pk = pkgsFor(x, x.sol);
  const el = document.createElement("div");
  const longSetup = (x.s || "").split("\n").length > 12;
  el.innerHTML = `
  <div class="crumbs"><button id="bkMod">${esc(MOD[m].name)}</button><span>›</span><button id="bkTopic">${esc(t.name)}</button><span>›</span><span>Exercício ${ei + 1} de ${t.ex.length}</span></div>
  <div class="exwrap">
    <div>
      <div class="card">
        <div class="exhead"><h2>${ei + 1}. ${esc(x.t)}</h2><span class="diff d${diffOf(ei)}">${DIFF[diffOf(ei)]}</span><span class="stars" id="exStars">${st.solved ? starsHTML(st.stars) : ""}</span></div>
        ${pk.length ? `<div class="pkgs" style="margin-bottom:8px">${pk.map(p => `<span class="pill gray">📦 ${p}</span>`).join("")}</div>` : ""}
        <div class="prompt">${x.p}</div>
        ${x.s ? `<div class="box"><details class="setup" ${longSetup ? "" : "open"}><summary>📦 Dados disponíveis (carregados antes do seu código)${longSetup ? " — toque para ver" : ""}</summary><div class="codebox"><pre class="code">${esc(x.s)}</pre></div></details></div>` : ""}
        <div class="box"><h5>💡 Dicas <span class="muted" id="hintCount"></span></h5><div class="hints" id="hints"></div></div>
        <div class="feedback" id="fb"></div>
        <div class="solution" id="sol"></div>
      </div>
      <div class="exnav"><button class="btn alt" id="prev">◀ Anterior</button><button class="btn alt" id="next">Próximo ▶</button></div>
    </div>
    <div>
      <div class="card editor-card">
        <div class="ed-bar"><span class="fname">main.py</span><span class="sp"></span>
          <button id="fmt" title="Recarregar o código inicial">↺ Resetar</button><button id="copy" title="Copiar código">⧉ Copiar</button></div>
        <textarea id="code"></textarea>
        <div class="actions">
          <button class="btn run" id="runBtn">▶ Executar <span class="kbd">Ctrl+Enter</span></button>
          <button class="btn check" id="chkBtn">✔ Verificar <span class="kbd">Ctrl+S</span></button>
          <span class="grow"></span>
          <button class="btn warn" id="hintBtn">💡 Dica</button>
          <button class="btn ghost" id="solBtn">👁 Solução</button>
        </div>
        <div class="console" id="out"><span class="sys">A saída do seu programa aparece aqui.</span></div>
        <div class="plots" id="plots"></div>
      </div>
    </div>
  </div>`;
  app.appendChild(el);
  $("#bkMod").onclick = () => go({view: "mod", m});
  $("#bkTopic").onclick = () => go({view: "topic", m, ti, tab: "ex"});
  const prv = ei > 0 ? {view: "ex", m, ti, ei: ei - 1} : (ti > 0 ? {view: "ex", m, ti: ti - 1, ei: topic(m, ti - 1).ex.length - 1} : null);
  const nxt = ei + 1 < t.ex.length ? {view: "ex", m, ti, ei: ei + 1} : (ti + 1 < MOD[m].topics.length ? {view: "ex", m, ti: ti + 1, ei: 0} : null);
  $("#prev").disabled = !prv; $("#next").disabled = !nxt;
  $("#prev").onclick = () => prv && go(prv);
  $("#next").onclick = () => { if (!nxt) return; if (!unlocked(nxt.m, nxt.ti)) { toast("🔒 Resolva 5 exercícios desta fase para liberar a próxima."); return; } go(nxt); };
  const starter = starterPy(x);
  const ta = $("#code"); ta.value = st.code ?? starter;
  draftKey = ek(m, ti, ei);
  if (window.CodeMirror) {
    CM = CodeMirror.fromTextArea(ta, {mode: "python", theme: "game", lineNumbers: true, indentUnit: 4, tabSize: 4, indentWithTabs: false,
      matchBrackets: true, autoCloseBrackets: true, styleActiveLine: true, lineWrapping: false, placeholder: "Digite seu código aqui…",
      extraKeys: {"Tab": cm => cm.somethingSelected() ? cm.indentSelection("add") : cm.replaceSelection("    ", "end"), "Shift-Tab": cm => cm.indentSelection("subtract"),
        "Ctrl-Enter": () => runIt(), "Cmd-Enter": () => runIt(), "Ctrl-S": () => checkIt(), "Cmd-S": () => checkIt()}});
    CM.on("change", () => { clearTimeout(draftT); draftT = setTimeout(() => { flushDraft(); save(); }, 400); clearErrLine(); });
    setTimeout(() => CM.refresh(), 30);
  } else {
    CM = {getValue: () => ta.value, setValue: v => ta.value = v, focus: () => ta.focus(), addLineClass() {}, removeLineClass() {}, lineCount: () => 0, refresh() {}};
    ta.style.cssText = "width:100%;height:320px;background:#0B1628;color:#E8F1FB;font-family:var(--mono);font-size:14px;padding:12px;border:0;resize:vertical";
    ta.addEventListener("input", () => { clearTimeout(draftT); draftT = setTimeout(() => { flushDraft(); save(); }, 400); });
  }
  document.onkeydown = e => {
    if (CUR.view !== "ex") return;
    if ((e.ctrlKey || e.metaKey) && e.key === "Enter") { e.preventDefault(); runIt(); }
    if ((e.ctrlKey || e.metaKey) && (e.key === "s" || e.key === "S")) { e.preventDefault(); checkIt(); }
  };
  const renderHints = () => {
    $("#hints").innerHTML = x.h.slice(0, st.hints).map((h, i) => `<div class="hint"><b>Dica ${i + 1}:</b> ${esc(h)}</div>`).join("") || `<span class="muted" style="font-size:.85rem">Tente sozinho primeiro. Cada dica usada vale 1 estrela a menos.</span>`;
    $("#hintCount").textContent = `(${st.hints}/${x.h.length})`;
    $("#hintBtn").disabled = st.hints >= x.h.length;
  };
  renderHints();
  if (st.sawSol) showSolution();
  $("#hintBtn").onclick = () => { if (st.hints < x.h.length) { st.hints++; save(); renderHints(); } };
  $("#solBtn").onclick = () => {
    if (st.sawSol || st.solved) { showSolution(); return; }
    if (!st.attempts) { feedback("info", "Tente primeiro 🙂", "A solução de referência é liberada depois da sua <b>primeira verificação</b>. Escreva sua tentativa e clique em <b>✔ Verificar</b>."); return; }
    confirmBox("Ver a solução?", "Ver a solução agora deixa este exercício com 1 estrela e sem XP. Você ainda pode resolvê-lo para registrar o progresso.", "Mostrar solução", () => { st.sawSol = true; save(); showSolution(); });
  };
  function showSolution() {
    $("#sol").innerHTML = `<div class="box"><h5>👁 Solução de referência</h5><pre class="code">${esc(x.sol)}</pre>
      <div class="row"><button class="btn alt" id="useSol">Copiar para o editor</button></div>
      <p class="muted" style="font-size:.8rem;margin:6px 0 0">Existem outras soluções corretas: o que vale é passar na verificação.</p></div>`;
    $("#useSol").onclick = () => { CM.setValue(x.sol); toast("Solução copiada. Leia linha a linha e rode para entender!"); };
  }
  $("#fmt").onclick = () => confirmBox("Resetar o código?", "Seu código atual deste exercício será substituído pelo código inicial.", "Resetar", () => { CM.setValue(starter); flushDraft(); save(); });
  $("#copy").onclick = () => copyText(CM.getValue());
  $("#runBtn").onclick = runIt; $("#chkBtn").onclick = checkIt;
  function busy(b) { ["#runBtn", "#chkBtn"].forEach(s => { const e = $(s); if (e) e.disabled = b; }); }
  async function runIt() {
    busy(true); out(`<span class="sys">Executando…</span>`); clearErrLine();
    try { await Engine.run(x, CM.getValue(), false); } finally { busy(false); }
  }
  async function checkIt() {
    busy(true); clearErrLine();
    try {
      const res = await Engine.run(x, CM.getValue(), true);
      if (!res) return;
      if (res.selfCheck) {
        feedback("info", "Motor offline: autoavaliação", `Sem internet, o Python não pôde ser carregado. Compare seu código com a solução e, se estiver equivalente, marque como resolvido.<div class="row"><button class="btn alt" id="showS">👁 Ver solução</button><button class="btn check" id="selfOk">✔ Conferi: está certo</button></div>`);
        $("#showS").onclick = () => { st.attempts = Math.max(st.attempts, 1); showSolution(); };
        $("#selfOk").onclick = () => { st.attempts++; st.hints = Math.max(st.hints, 1); onSolved(); };
        return;
      }
      if (res.empty) { feedback("no", res.title, res.html); return; }
      st.attempts++;
      if (res.ok) onSolved(); else { save(); feedback("no", res.title || "Ainda não…", res.html); }
    } finally { busy(false); }
  }
  function onSolved() {
    const first = !st.solved; let gained = 0;
    if (first) {
      const stars = st.sawSol ? 1 : Math.max(1, 3 - st.hints);
      st.stars = stars; st.solved = true; st.firstTry = st.attempts === 1 && !st.hints && !st.sawSol;
      gained = st.sawSol ? 0 : Math.round(baseXP(ei) * stars / 3) + (st.firstTry ? 5 : 0);
      st.xp = gained; st.solvedAt = new Date().toISOString();
      $("#exStars").innerHTML = starsHTML(stars); confetti();
      gainXP(gained);
      if (solvedIn(m, ti) === 5 && ti + 1 < MOD[m].topics.length && !S.free) setTimeout(() => toast(`🔓 Fase <b>${esc(topic(m, ti + 1).name)}</b> desbloqueada!`, 3500), 1600);
    } else save();
    feedback("ok", first ? `✔ Correto! +${gained} XP ${st.firstTry ? "(bônus de primeira!)" : ""}` : "✔ Correto de novo!",
      `${starsHTML(st.stars)} ${st.sawSol ? "<br>Você viu a solução antes: sem XP, mas o progresso foi registrado." : st.hints ? `<br>Você usou ${st.hints} dica(s). Tente o próximo sem dicas para ganhar 3 estrelas!` : "<br>Perfeito, sem dicas!"}
      <div class="row">${nxt ? `<button class="btn check" id="goNext">Próximo exercício ▶</button>` : ""}<button class="btn alt" id="goTopic">Ver fase</button></div>`);
    if ($("#goNext")) $("#goNext").onclick = () => $("#next").click();
    $("#goTopic").onclick = () => go({view: "topic", m, ti, tab: "ex"});
  }
  if (r.focus !== false) setTimeout(() => CM.focus && CM.focus(), 60);
}
function out(html) { const o = $("#out"); if (o) o.innerHTML = html; }
function plots(imgs) { const p = $("#plots"); if (p) p.innerHTML = (imgs || []).map(b => `<img alt="Gráfico gerado pelo seu código" src="data:image/png;base64,${b}">`).join(""); }
function feedback(kind, title, html) { const f = $("#fb"); if (!f) return; f.className = "feedback show " + kind; f.innerHTML = `<h4>${title}</h4>${html || ""}`; f.scrollIntoView({behavior: "smooth", block: "nearest"}); }
let errLine = null;
function markErrLine(n) { if (!CM || !n || !CM.lineCount || n > CM.lineCount()) return; errLine = n - 1; CM.addLineClass(errLine, "background", "err-line"); }
function clearErrLine() { if (CM && errLine !== null) { CM.removeLineClass(errLine, "background", "err-line"); errLine = null; } }

/* ===================== REVISAR ===================== */
function viewRev(app) {
  const items = [];
  MODS.forEach(M => M.topics.forEach((t, ti) => t.ex.forEach((x, ei) => {
    const s = peek(M.id, ti, ei);
    if ((s.attempts && !s.solved) || (s.solved && s.sawSol)) items.push({m: M.id, ti, ei, x, s});
  })));
  const el = document.createElement("div");
  el.innerHTML = `<h2>🔁 Revisar</h2><p class="muted" style="margin-top:-6px">Exercícios tentados e ainda não resolvidos, e os que você resolveu depois de ver a solução (refaça sem olhar!).</p>
  ${items.length ? `<div class="review-list">${items.map((it, k) => `<button class="exc ${it.s.solved ? "solved" : "tried"}" data-k="${k}"><div class="num">${it.s.solved ? "👁" : "!"}</div><div class="et"><b>${esc(it.x.t)}</b>
    <span class="muted" style="font-size:.78rem">${esc(MOD[it.m].name)} › ${esc(topic(it.m, it.ti).name)} • ${it.s.attempts} tentativa(s)</span></div><span class="diff d${diffOf(it.ei)}">${DIFF[diffOf(it.ei)]}</span></button>`).join("")}</div>`
    : `<div class="card"><p style="margin:0">✅ Nada para revisar. Continue avançando!</p><div class="row"><button class="btn acc" id="recB">▶ Próximo recomendado</button></div></div>`}`;
  app.appendChild(el);
  el.querySelectorAll("[data-k]").forEach(b => b.onclick = () => { const it = items[+b.dataset.k]; go({view: "ex", m: it.m, ti: it.ti, ei: it.ei}); });
  if ($("#recB")) $("#recB").onclick = () => go(recommend());
}

/* ===================== CONQUISTAS ===================== */
function viewAch(app) {
  const el = document.createElement("div");
  el.innerHTML = `<h2>🏆 Conquistas (${Object.keys(S.achv).length}/${ACH.length})</h2>
  <div class="ach">${ACH.map(([id, ic, nm, ds]) => `<div class="badge-c ${S.achv[id] ? "on" : ""}"><div class="ic">${ic}</div><div><b>${nm}</b><small>${ds}${S.achv[id] ? "<br>✓ " + new Date(S.achv[id]).toLocaleDateString("pt-BR") : ""}</small></div></div>`).join("")}</div>
  <h3>🎚️ Níveis</h3><div class="ach">${LEVELS.map(([xp, nm], i) => `<div class="badge-c ${S.xp >= xp ? "on" : ""}"><div class="ic" style="font-size:1rem;font-weight:900">${i + 1}</div><div><b>${nm}</b><small>${xp} XP</small></div></div>`).join("")}</div>
  <h3>📐 Como funciona a pontuação</h3><div class="card"><ul style="margin:0;padding-left:18px">
   <li>Exercício fácil = 10 XP • médio = 20 XP • desafio = 30 XP.</li><li>3 estrelas sem dicas; cada dica usada vale 1 estrela a menos (e menos XP).</li>
   <li>Acertou na 1ª verificação, sem dicas: +5 XP de bônus.</li><li>Viu a solução antes de resolver: sem XP, mas conta como feito.</li>
   <li>Mapa revelado inteiro no modo memória: +10 XP (uma vez por fase). Quiz com 5+ acertos: +15 XP (uma vez por fase).</li>
   <li>5 exercícios resolvidos liberam a próxima fase (ou ative o Modo livre na trilha).</li></ul></div>`;
  app.appendChild(el);
}

/* ===================== PROGRESSO ===================== */
function viewProg(app) {
  const s = stats();
  const el = document.createElement("div");
  el.innerHTML = `<h2>📊 Progresso</h2>
  <div class="stats4" style="grid-template-columns:repeat(auto-fit,minmax(150px,1fr))">
    <div class="stat"><b>${S.xp}</b><small>XP total</small></div><div class="stat"><b>${s.solved}/${totalEx}</b><small>resolvidos</small></div>
    <div class="stat"><b>${s.perfect}</b><small>com 3 estrelas</small></div><div class="stat"><b>${s.maps}/${totalTopics}</b><small>mapas revisados</small></div>
    <div class="stat"><b>${s.quizzes}/${totalTopics}</b><small>quizzes dominados</small></div><div class="stat"><b>${s.streak} 🔥</b><small>dias seguidos</small></div></div>
  ${MODS.map(M => `<h3>${M.icon} ${esc(M.name)} <small class="muted">${modSolved(M.id)}/${modTotal(M.id)}</small></h3>
    ${M.topics.map((t, ti) => { const n = solvedIn(M.id, ti), tried = t.ex.filter((_, ei) => peek(M.id, ti, ei).attempts && !peek(M.id, ti, ei).solved).length;
      const mp = S.map[tk(M.id, ti)]?.done, qz = S.quiz[tk(M.id, ti)]?.done;
      return `<div class="prow"><div class="nm"><b>${ti + 1}. ${esc(t.name)}</b> <small class="muted">${n}/${t.ex.length}${tried ? ` • ${tried} para revisar` : ""}${mp ? " • 🧠" : ""}${qz ? " • ❓" : ""}${unlocked(M.id, ti) ? "" : " • 🔒"}</small><div class="bar"><i style="width:${n / t.ex.length * 100}%;background:${n === t.ex.length ? "var(--ok)" : "var(--mid)"}"></i></div></div>
      <button class="btn alt" data-m="${M.id}" data-ti="${ti}" ${unlocked(M.id, ti) ? "" : "disabled"}>Abrir</button></div>`; }).join("")}`).join("")}
  <h3>💾 Salvamento e backup</h3>
  <div class="card">
    <p style="margin-top:0">O progresso é salvo <b>automaticamente</b> neste navegador: exercícios, códigos digitados, estrelas, XP, mapas, quizzes e o ponto onde você parou.
    Para usar em outro aparelho ou como garantia, exporte um backup e importe no outro navegador.</p>
    ${storageOk ? "" : `<p class="feedback no show">⚠ Este navegador está bloqueando o salvamento automático (modo anônimo?). Use o backup.</p>`}
    <p class="muted" style="font-size:.85rem">Último salvamento: ${S.updated ? new Date(S.updated).toLocaleString("pt-BR") : "—"}</p>
    <div class="row"><button class="btn" id="exp">⬇ Exportar backup</button><button class="btn alt" id="imp">⬆ Importar backup</button><button class="btn ghost" id="rst">🗑 Zerar progresso</button></div>
  </div>`;
  app.appendChild(el);
  el.querySelectorAll(".prow .btn").forEach(b => b.onclick = () => go({view: "topic", m: b.dataset.m, ti: +b.dataset.ti, tab: "ex"}));
  $("#exp").onclick = () => {
    flushDraft(); save(true);
    const blob = new Blob([JSON.stringify({app: KEY, data: S}, null, 1)], {type: "application/json"});
    const a = document.createElement("a"); a.href = URL.createObjectURL(blob); a.download = `backup-python-quest-${today()}.json`; a.click();
    setTimeout(() => URL.revokeObjectURL(a.href), 1500); toast("⬇ Backup exportado");
  };
  $("#imp").onclick = () => $("#impFile").click();
  $("#rst").onclick = () => confirmBox("Zerar todo o progresso?", "XP, estrelas, conquistas, mapas, quizzes e códigos serão apagados. Exporte um backup antes, se quiser.", "Zerar", () => { S = blank(); save(true); renderHUD(); go({view: "home"}); toast("Progresso zerado"); });
}
$("#impFile").onchange = e => {
  const f = e.target.files[0]; if (!f) return;
  const rd = new FileReader();
  rd.onload = () => { try { const o = JSON.parse(rd.result); if (o.app !== KEY || typeof o.data !== "object") throw 0; S = Object.assign(blank(), o.data); save(true); renderHUD(); go({view: "prog"}); toast("⬆ Backup importado com sucesso"); } catch (er) { toast("❌ Arquivo de backup inválido para este sistema"); } };
  rd.readAsText(f); e.target.value = "";
};

/* ===================== MOTOR PYTHON (Pyodide em Web Worker) ===================== */
const PY_ERRORS = {
  NameError: m => { const v = (m.match(/'([^']+)'/) || [])[1]; return `Você usou <code>${esc(v || "um nome")}</code>, mas ele não existe. Confira a grafia (Python diferencia maiúsculas de minúsculas), se a variável foi criada antes de ser usada e se o import foi feito.`; },
  SyntaxError: () => "Erro de sintaxe: confira dois-pontos <code>:</code> no fim de <code>if/for/while/def/class/with</code>, parênteses e aspas fechados e vírgulas.",
  IndentationError: () => "Indentação incorreta: o conteúdo de <code>if/for/while/def/with</code> precisa estar recuado com 4 espaços, sempre do mesmo jeito.",
  TabError: () => "Mistura de TAB e espaços. Use apenas espaços (a tecla Tab do editor já insere 4 espaços).",
  TypeError: () => "Operação com tipos incompatíveis (ex.: somar texto com número) ou quantidade errada de argumentos. Confira os tipos com <code>type()</code>.",
  ZeroDivisionError: () => "Divisão por zero. Verifique o divisor antes de dividir.",
  IndexError: () => "Índice fora do intervalo: a primeira posição é 0 e a última é <code>len(x) - 1</code>.",
  KeyError: m => `A chave ${esc(m)} não existe. Use <code>.get(chave, padrão)</code> ou verifique com <code>in</code>.`,
  AttributeError: m => /NoneType/.test(m) ? "Você usou um atributo em <code>None</code>: provavelmente um <code>find</code>/<code>fetchone</code> não encontrou nada. Teste se o resultado é <code>None</code> antes." : "Esse objeto não tem o atributo/método usado. Confira o nome e o tipo da variável.",
  ValueError: () => "Valor inválido para a operação (ex.: <code>int(\"abc\")</code> ou desempacotar quantidade errada). Confira o conteúdo da variável.",
  FileNotFoundError: () => "Arquivo não encontrado. Confira o nome e a pasta (use <code>os.listdir()</code> para ver o que existe).",
  ModuleNotFoundError: () => "Módulo não encontrado. No navegador estão disponíveis a biblioteca padrão, numpy, pandas, matplotlib, seaborn, bs4 e sqlite3.",
  NoSuchElementException: () => "Elemento não encontrado na página. Confira o seletor (id, classe, XPath) olhando o HTML em “Dados disponíveis”.",
  OperationalError: m => `Erro no SQL: <code>${esc(m)}</code>. Confira nomes de tabelas/colunas e a sintaxe.`,
  RecursionError: () => "Recursão infinita: garanta um caso base que retorne sem nova chamada.",
  UnboundLocalError: () => "Variável usada antes de receber valor dentro da função.",
  RuntimeError: m => esc(m),
};
const Engine = (() => {
  let worker = null, seq = 0, pend = {}, readyP = null, online = null;
  const status = (cls, txt) => { const d = $("#engDot"); if (d) { d.className = "dot " + cls; $("#engTxt").textContent = txt; } };
  const WSRC = [
    "let py = null; const loaded = new Set();",
    "self.onmessage = async (e) => { const m = e.data;",
    " try {",
    "  if (!py) { importScripts(m.base + 'pyodide.js'); py = await loadPyodide({indexURL: m.base}); py.runPython(m.harness); }",
    "  if (m.type === 'init') { self.postMessage({id: m.id, type: 'ready'}); return; }",
    "  const need = (m.pkgs || []).filter(p => !loaded.has(p));",
    "  if (need.length) {",
    "    self.postMessage({id: m.id, type: 'status', msg: 'Baixando ' + need.join(', ') + ' (só na primeira vez, pode levar alguns segundos)…'});",
    "    const nat = need.filter(p => p !== 'seaborn');",
    "    if (need.includes('seaborn')) nat.push('micropip', 'pandas', 'matplotlib');",
    "    if (nat.length) await py.loadPackage(nat);",
    "    if (nat.includes('matplotlib') || need.includes('seaborn')) py.runPython(\"import matplotlib\\nmatplotlib.use('Agg')\");",
    "    if (need.includes('seaborn')) { await py.runPythonAsync(\"import micropip\\nawait micropip.install('seaborn')\"); }",
    "    need.concat(nat).forEach(p => loaded.add(p));",
    "  }",
    "  self.postMessage({id: m.id, type: 'running'});",
    "  py.globals.set('_args', m.args);",
    "  const r = py.runPython('run_json(_args)');",
    "  self.postMessage({id: m.id, type: 'result', res: r});",
    " } catch (err) { self.postMessage({id: m.id, type: 'fatal', msg: String((err && err.message) || err)}); }",
    "};"].join("\n");
  function spawn() {
    worker = new Worker(URL.createObjectURL(new Blob([WSRC], {type: "text/javascript"})));
    worker.onmessage = e => {
      const m = e.data, p = pend[m.id]; if (!p) return;
      if (m.type === "status") { out(`<span class="sys">${esc(m.msg)}</span>`); return; }
      if (m.type === "running") { p.timer = setTimeout(() => { delete pend[m.id]; restart(); p.rej({timeout: true}); }, p.limit); return; }
      clearTimeout(p.timer); delete pend[m.id];
      if (m.type === "ready") p.res(true); else if (m.type === "result") p.res(JSON.parse(m.res)); else p.rej(new Error(m.msg));
    };
    worker.onerror = e => { Object.values(pend).forEach(p => { clearTimeout(p.timer); p.rej(new Error(e.message || "erro no worker")); }); pend = {}; };
    status("load", "Carregando Python…");
    readyP = call({type: "init"}, 0, 90000).then(() => { online = true; status("on", "Python pronto"); return true; })
      .catch(() => { online = false; status("off", "Python offline"); return false; });
  }
  function call(msg, limit, initLimit) {
    return new Promise((res, rej) => {
      const id = ++seq; pend[id] = {res, rej, limit};
      if (initLimit) pend[id].timer = setTimeout(() => { delete pend[id]; rej(new Error("timeout")); }, initLimit);
      worker.postMessage(Object.assign({}, msg, {id, base: PYBASE, harness: window.PQ_HARNESS}));
    });
  }
  function restart() { try { worker.terminate(); } catch (e) {} spawn(); }
  function explain(r) {
    const f = PY_ERRORS[r.err];
    return `<b>${esc(r.err)}</b>${r.line ? ` na linha <b>${r.line}</b>` : ""}: <code>${esc(r.msg)}</code><br>${f ? f(r.msg) : "Leia a mensagem e confira a linha indicada."}`;
  }
  return {
    init() { $("#engineChip").onclick = () => toast(online === false ? "⚠ O Python roda no navegador e precisa de internet na 1ª vez. Sem internet, use a autoavaliação com a solução." : "🐍 Python 3.12 completo rodando no seu navegador (Pyodide), com testes automáticos.", 5000); spawn(); },
    async run(x, code, verify) {
      if (!code.trim() || code.trim() === starterPy(x).trim()) { out(`<span class="err">O editor está vazio. Escreva seu código primeiro.</span>`); return verify ? {empty: true, title: "Nada para verificar", html: "Escreva sua solução no editor."} : null; }
      let ok = await readyP;
      if (!ok) { status("load", "Tentando de novo…"); restart(); ok = await readyP; }
      if (!ok) { out(`<span class="err">Motor Python indisponível (sem conexão para baixá-lo).</span>`); return verify ? {selfCheck: true} : null; }
      const pk = pkgsFor(x, code + "\n" + x.sol);
      out(`<span class="sys">Executando…</span>`); plots([]);
      let r;
      try { r = await call({type: "run", args: JSON.stringify({code, setup: x.s || "", test: verify ? x.test : "", mode: verify ? "test" : "run"}), pkgs: pk}, pk.length ? 30000 : 8000); }
      catch (e) {
        if (e && e.timeout) { out(`<span class="err">⏱ Tempo esgotado: o código rodou por tempo demais e foi interrompido.</span>`);
          return verify ? {ok: false, title: "⏱ Tempo esgotado", html: "Provável laço infinito: confira se a condição do <code>while</code> fica falsa em algum momento."} : null; }
        out(`<span class="err">Falha no motor: ${esc(e.message || e)}</span>`); return verify ? {ok: false, title: "Falha no motor", html: "Tente novamente. Se baixou pacotes, confira a internet."} : null;
      }
      const o = r.out ? esc(r.out) : "";
      plots(r.imgs);
      if (r.err) {
        markErrLine(r.line);
        out((o ? o + "\n" : "") + `<span class="err">${esc(r.err)}: ${esc(r.msg)}${r.line ? " (linha " + r.line + ")" : ""}</span>`);
        const html = explain(r);
        if (!verify) feedback("no", "Erro ao executar", html);
        return verify ? {ok: false, title: "Erro ao executar", html} : null;
      }
      out(o || `<span class="sys">(o programa não imprimiu nada — tudo bem se o exercício pede variáveis/funções)</span>`);
      if (!verify) { feedback("info", "Execução concluída", "Quando estiver pronto, clique em <b>✔ Verificar</b> para rodar os testes automáticos."); return null; }
      if (r.ok) return {ok: true};
      if (r.line) markErrLine(r.line);
      return {ok: false, title: "Quase lá! Um teste falhou", html: `<b>Teste:</b> ${esc(r.fail)}<br><span class="muted" style="font-size:.85rem">Os testes também rodam seu código com outros valores, então evite números fixos.</span>`};
    }
  };
})();

/* ===================== início ===================== */
if (!MODS.length) { $("#app").innerHTML = `<div class="feedback no show">Não foi possível carregar os dados (pasta <code>data/</code>).</div>`; }
else {
  renderHUD();
  Engine.init();
  let r0 = parseHash();
  if (r0.view === "home" && !location.hash && S.updated && S.last && MOD[S.last.m] && S.last.view === "ex") { r0 = Object.assign({}, S.last, {focus: false}); history.replaceState(null, "", hashOf(r0)); setTimeout(() => toast("📌 Bem-vindo de volta! Você continua de onde parou."), 600); }
  render(r0);
  if (!storageOk) setTimeout(() => toast("⚠ O navegador bloqueou o salvamento automático. Use Progresso › Exportar backup."), 1500);
}
if ("serviceWorker" in navigator && location.protocol.startsWith("http")) {
  window.addEventListener("load", () => navigator.serviceWorker.register("sw.js").catch(() => {}));
}
