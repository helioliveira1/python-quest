/* Sincronização do progresso na nuvem (Supabase).
   - Login com e-mail e senha.
   - O progresso continua salvo no navegador (funciona offline) e é enviado para a nuvem quando há login.
   - Ao entrar em outro aparelho, os dois progressos são MESCLADOS (nada é perdido). */
"use strict";
const PQSync = (() => {
  const C = window.PQ_CONFIG || {};
  const enabled = !!(C.SUPABASE_URL && C.SUPABASE_KEY && window.supabase && window.supabase.createClient);
  let sb = null, user = null, pushT = null, pushing = false, pendingPush = false, lastSync = null, lastPull = 0, state = "off";
  const $ = s => document.querySelector(s);
  const esc = s => String(s ?? "").replace(/[&<>"]/g, c => ({"&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;"}[c]));
  const redirectTo = () => location.origin + location.pathname;

  /* ---------- mesclagem de dois progressos ---------- */
  const better = (a, b) => { // true se a é melhor que b
    if (!b) return true; if (!a) return false;
    if (!!a.solved !== !!b.solved) return !!a.solved;
    if (a.solved && (a.stars || 0) !== (b.stars || 0)) return (a.stars || 0) > (b.stars || 0);
    return (a.attempts || 0) > (b.attempts || 0);
  };
  function merge(local, remote) {
    if (!remote || typeof remote !== "object") return local;
    const tl = Date.parse(local.updated || 0) || 0, tr = Date.parse(remote.updated || 0) || 0;
    const newer = tr > tl ? remote : local, older = newer === remote ? local : remote;
    const out = JSON.parse(JSON.stringify(newer));
    out.ex = out.ex || {}; out.map = out.map || {}; out.quiz = out.quiz || {}; out.achv = out.achv || {}; out.layout = out.layout || {};
    for (const [k, v] of Object.entries(older.ex || {})) {
      const n = out.ex[k];
      if (!n) out.ex[k] = v;
      else if (better(v, n)) out.ex[k] = Object.assign({}, v, {code: n.code ?? v.code});
    }
    for (const [k, v] of Object.entries(older.map || {})) {
      const n = out.map[k] || {seen: [], done: false};
      out.map[k] = {seen: [...new Set([...(n.seen || []), ...(v.seen || [])])], done: !!(n.done || v.done)};
    }
    for (const [k, v] of Object.entries(older.quiz || {})) {
      const n = out.quiz[k] || {best: 0, done: false, plays: 0};
      out.quiz[k] = {best: Math.max(n.best || 0, v.best || 0), done: !!(n.done || v.done), plays: Math.max(n.plays || 0, v.plays || 0)};
    }
    for (const [k, v] of Object.entries(older.achv || {})) if (!out.achv[k] || v < out.achv[k]) out.achv[k] = v;
    out.days = [...new Set([...(newer.days || []), ...(older.days || [])])].sort();
    out.layout = Object.assign({}, older.layout || {}, newer.layout || {});
    out.created = [local.created, remote.created].filter(Boolean).sort()[0] || out.created;
    // XP é recalculado a partir das partes, para não somar em dobro
    out.xp = Object.values(out.ex).reduce((a, x) => a + (x.solved ? (x.xp || 0) : 0), 0)
      + 10 * Object.values(out.map).filter(m => m.done).length + 15 * Object.values(out.quiz).filter(q => q.done).length;
    out.updated = new Date(Math.max(tl, tr, Date.now())).toISOString();
    return out;
  }

  /* ---------- status no topo ---------- */
  function status(s, extra) {
    state = s;
    const chip = $("#syncChip"); if (!chip) return;
    const map = {off: ["☁️", "Entrar"], sync: ["☁️", "Sincronizando…"], ok: ["✅", "Sincronizado"], err: ["⚠️", "Sem conexão"], local: ["☁️", "Entrar"]};
    const [ic, txt] = map[s] || map.off;
    chip.innerHTML = `${ic}<span class="lbl">&nbsp;${txt}</span>`;
    chip.title = user ? `Conectado como ${user.email}${lastSync ? " • última sincronização " + lastSync.toLocaleTimeString("pt-BR") : ""}${extra ? " • " + extra : ""}` : "Entre para sincronizar seu progresso entre aparelhos";
    const box = $("#syncBox"); if (box) box.innerHTML = boxInner();
    bindBox();
  }

  /* ---------- nuvem ---------- */
  async function pull(force) {
    if (!user || (!force && Date.now() - lastPull < 20000)) return;
    lastPull = Date.now(); status("sync");
    const {data, error} = await sb.from("progresso").select("dados, atualizado_em").eq("user_id", user.id).maybeSingle();
    if (error) { status("err", error.message); return; }
    const local = window.PQ.getState();
    if (data && data.dados && Object.keys(data.dados).length) {
      const merged = merge(local, data.dados);
      window.PQ.setState(merged);
    }
    await push(true);
  }
  async function push(now) {
    if (!user) return;
    if (!now) { clearTimeout(pushT); pushT = setTimeout(() => push(true), 2500); return; }
    if (pushing) { pendingPush = true; return; }
    pushing = true; status("sync");
    try {
      const dados = window.PQ.getState();
      const {error} = await sb.from("progresso").upsert({user_id: user.id, dados}, {onConflict: "user_id"});
      if (error) throw error;
      lastSync = new Date(); status("ok");
    } catch (e) { status("err", e.message || String(e)); }
    finally { pushing = false; if (pendingPush) { pendingPush = false; push(); } }
  }

  /* ---------- telas de login ---------- */
  function modalAuth(msg) {
    const m = $("#mbox"); if (!m) return;
    m.innerHTML = `<div class="big">☁️</div><h3>Sincronizar progresso</h3>
      <p class="muted" style="font-size:.88rem">Entre para salvar seu progresso na nuvem e continuar em qualquer computador ou celular.</p>
      <form id="authF" class="authf" autocomplete="on">
        <input id="aEmail" type="email" placeholder="seu e-mail" autocomplete="email" required>
        <input id="aPass" type="password" placeholder="senha (mín. 6 caracteres)" autocomplete="current-password" minlength="6" required>
        <div id="aMsg" class="amsg">${msg || ""}</div>
        <div class="row" style="justify-content:center"><button class="btn" type="submit" id="aIn">Entrar</button><button class="btn alt" type="button" id="aUp">Criar conta</button></div>
        <div class="row" style="justify-content:center;margin-top:4px"><button class="linkbtn" type="button" id="aForgot">Esqueci a senha</button><button class="linkbtn" type="button" data-close>Agora não</button></div>
      </form>`;
    $("#modal").classList.add("show");
    const say = (t, ok) => { const a = $("#aMsg"); a.className = "amsg " + (ok ? "ok" : "no"); a.textContent = t; };
    const creds = () => ({email: $("#aEmail").value.trim(), password: $("#aPass").value});
    $("#authF").onsubmit = async e => {
      e.preventDefault(); say("Entrando…", true);
      const {error} = await sb.auth.signInWithPassword(creds());
      if (error) say(traduz(error.message)); else { $("#modal").classList.remove("show"); }
    };
    $("#aUp").onclick = async () => {
      const c = creds(); if (!c.email || c.password.length < 6) { say("Informe e-mail e uma senha com 6 caracteres ou mais."); return; }
      say("Criando conta…", true);
      const {data, error} = await sb.auth.signUp(Object.assign(c, {options: {emailRedirectTo: redirectTo()}}));
      if (error) say(traduz(error.message));
      else if (data.session) $("#modal").classList.remove("show");
      else say("Conta criada! Abra o e-mail de confirmação que enviamos e clique no link. Depois volte aqui e entre.", true);
    };
    $("#aForgot").onclick = async () => {
      const email = $("#aEmail").value.trim(); if (!email) { say("Digite seu e-mail acima primeiro."); return; }
      const {error} = await sb.auth.resetPasswordForEmail(email, {redirectTo: redirectTo()});
      say(error ? traduz(error.message) : "Se o e-mail existir, enviamos um link para criar uma nova senha.", !error);
    };
    setTimeout(() => $("#aEmail") && $("#aEmail").focus(), 50);
  }
  function modalConta() {
    const m = $("#mbox"); if (!m) return;
    m.innerHTML = `<div class="big">✅</div><h3>Progresso na nuvem</h3>
      <p class="muted" style="font-size:.9rem">Conectado como <b>${esc(user.email)}</b>.<br>${lastSync ? "Última sincronização: " + lastSync.toLocaleString("pt-BR") : "Ainda não sincronizado."}</p>
      <div class="row" style="justify-content:center"><button class="btn" id="sNow">🔄 Sincronizar agora</button><button class="btn alt" id="sOut">Sair</button></div>
      <p class="muted" style="font-size:.78rem;margin-bottom:0">Ao sair, o progresso some deste aparelho, mas continua salvo na sua conta.</p>`;
    $("#modal").classList.add("show");
    $("#sNow").onclick = async () => { $("#modal").classList.remove("show"); await pull(true); window.PQ.toast("🔄 Progresso sincronizado"); };
    $("#sOut").onclick = sair;
  }
  function modalNovaSenha() {
    const m = $("#mbox"); if (!m) return;
    m.innerHTML = `<div class="big">🔑</div><h3>Criar nova senha</h3>
      <form id="npF" class="authf"><input id="np" type="password" minlength="6" placeholder="nova senha (mín. 6)" autocomplete="new-password" required>
      <div id="aMsg" class="amsg"></div><div class="row" style="justify-content:center"><button class="btn" type="submit">Salvar senha</button></div></form>`;
    $("#modal").classList.add("show");
    $("#npF").onsubmit = async e => {
      e.preventDefault();
      const {error} = await sb.auth.updateUser({password: $("#np").value});
      const a = $("#aMsg"); a.className = "amsg " + (error ? "no" : "ok"); a.textContent = error ? traduz(error.message) : "Senha alterada! Você já está conectado.";
      if (!error) setTimeout(() => $("#modal").classList.remove("show"), 1200);
    };
  }
  async function sair() {
    await push(true);
    await sb.auth.signOut();
    $("#modal").classList.remove("show");
    window.PQ.resetLocal();
    window.PQ.toast("Você saiu. Seu progresso continua salvo na conta.");
  }
  function traduz(m) {
    const t = {"Invalid login credentials": "E-mail ou senha incorretos.", "Email not confirmed": "Confirme seu e-mail pelo link que enviamos antes de entrar.",
      "User already registered": "Este e-mail já tem conta. Use Entrar.", "Password should be at least 6 characters": "A senha precisa ter pelo menos 6 caracteres."};
    for (const [k, v] of Object.entries(t)) if (m && m.includes(k)) return v;
    if (/rate limit/i.test(m || "")) return "Muitos e-mails enviados em pouco tempo. Aguarde alguns minutos e tente de novo.";
    return m || "Erro desconhecido.";
  }

  /* ---------- caixa na tela de Progresso ---------- */
  function boxInner() {
    if (!enabled) return `<p style="margin:0" class="muted">Sincronização desligada neste site.</p>`;
    if (!user) return `<p style="margin-top:0">Entre com e-mail e senha para guardar seu progresso na nuvem e continuar em <b>qualquer computador ou celular</b>. Os progressos dos aparelhos são mesclados, nada se perde.</p><div class="row"><button class="btn acc" data-sync="login">☁️ Entrar ou criar conta</button></div>`;
    return `<p style="margin-top:0">Conectado como <b>${esc(user.email)}</b> • ${state === "ok" && lastSync ? "✅ sincronizado às " + lastSync.toLocaleTimeString("pt-BR") : state === "err" ? "⚠️ sem conexão: tentaremos de novo" : "sincronizando…"}</p>
      <div class="row"><button class="btn" data-sync="now">🔄 Sincronizar agora</button><button class="btn alt" data-sync="out">Sair</button></div>`;
  }
  function bindBox() {
    document.querySelectorAll("[data-sync]").forEach(b => b.onclick = async () => {
      const a = b.dataset.sync;
      if (a === "login") modalAuth(); else if (a === "now") { await pull(true); window.PQ.toast("🔄 Progresso sincronizado"); } else if (a === "out") sair();
    });
  }

  /* ---------- início ---------- */
  function init() {
    const chip = $("#syncChip");
    if (!enabled) { if (chip) chip.style.display = "none"; return; }
    sb = window.supabase.createClient(C.SUPABASE_URL, C.SUPABASE_KEY, {auth: {persistSession: true, autoRefreshToken: true, detectSessionInUrl: true}});
    status("off");
    if (chip) chip.onclick = () => user ? modalConta() : modalAuth();
    sb.auth.onAuthStateChange((ev, session) => {
      const was = user && user.id;
      user = session ? session.user : null;
      if (ev === "PASSWORD_RECOVERY") { setTimeout(modalNovaSenha, 300); }
      if (user && user.id !== was) { setTimeout(() => pull(true), 0); if (ev === "SIGNED_IN") window.PQ.toast(`☁️ Conectado como <b>${esc(user.email)}</b>`); }
      if (!user) status("off");
      if (/#access_token|type=(signup|recovery)/.test(location.hash)) setTimeout(() => history.replaceState(null, "", location.pathname + "#/"), 50);
    });
    document.addEventListener("visibilitychange", () => { if (!document.hidden) pull(false); else if (user) push(true); });
    window.addEventListener("online", () => user && push(true));
  }

  return {enabled, init, push, pull, merge, boxHTML: () => `<div id="syncBox">${boxInner()}</div>`, bindBox, login: () => modalAuth()};
})();
window.PQSync = PQSync;
