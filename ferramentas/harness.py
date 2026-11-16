import sys, io, os, json, traceback, builtins, tempfile, types, re

os.environ.setdefault("MPLBACKEND", "Agg")

def _input(prompt=""):
    raise RuntimeError("input() não é usado nos exercícios: os dados já estão nas variáveis indicadas.")
builtins.input = _input

# ------------------------------------------------------------------
# Simulador de SMTP (o navegador não envia e-mails de verdade)
# ------------------------------------------------------------------
import smtplib as _smtplib
_smtplib.ENVIADOS = []

class _SMTPFake:
    def __init__(self, host="", port=0, *a, **k):
        self.host, self.port, self.tls, self.usuario, self.senha, self.fechado = host, port, False, None, None, False
    def __enter__(self): return self
    def __exit__(self, *a): self.quit()
    def ehlo(self, *a): return (250, b"ok")
    def starttls(self, *a, **k): self.tls = True; return (220, b"ok")
    def login(self, usuario, senha):
        self.usuario, self.senha = usuario, senha; return (235, b"ok")
    def send_message(self, msg, from_addr=None, to_addrs=None, **k):
        _smtplib.ENVIADOS.append({"msg": msg, "servidor": self, "de": from_addr, "para": to_addrs}); return {}
    def sendmail(self, de, para, texto, *a, **k):
        _smtplib.ENVIADOS.append({"msg": texto, "servidor": self, "de": de, "para": para}); return {}
    def quit(self): self.fechado = True; return (221, b"bye")
    close = quit

_smtplib.SMTP = _SMTPFake
_smtplib.SMTP_SSL = _SMTPFake

# ------------------------------------------------------------------
# Simulador de Selenium (navegador falso sobre páginas HTML em memória)
# ------------------------------------------------------------------
from html.parser import HTMLParser as _HP

_VOID = {"input", "br", "img", "hr", "meta", "link", "area", "base", "col", "source", "wbr"}

class _No:
    def __init__(self, tag, attrs, pai):
        self.tag, self.attrs, self.pai, self.filhos, self.textos = tag, dict(attrs), pai, [], []
    def todos(self):
        for f in self.filhos:
            if isinstance(f, _No):
                yield f
                yield from f.todos()
    def texto(self):
        partes = []
        for f in self.filhos:
            partes.append(f.texto() if isinstance(f, _No) else f)
        return " ".join(" ".join(partes).split())

class _Parser(_HP):
    def __init__(self):
        super().__init__(); self.raiz = _No("#doc", {}, None); self.cur = self.raiz
    def handle_starttag(self, tag, attrs):
        n = _No(tag, [(k, v if v is not None else "") for k, v in attrs], self.cur); self.cur.filhos.append(n)
        if tag not in _VOID: self.cur = n
    def handle_startendtag(self, tag, attrs):
        self.cur.filhos.append(_No(tag, [(k, v if v is not None else "") for k, v in attrs], self.cur))
    def handle_endtag(self, tag):
        n = self.cur
        while n is not None and n.tag != tag: n = n.pai
        if n is not None and n.pai is not None: self.cur = n.pai
    def handle_data(self, d):
        if d.strip(): self.cur.filhos.append(d)

class NoSuchElementException(Exception): pass

def _css_simples(sel, n):
    m = re.fullmatch(r"([a-zA-Z0-9]*|\*)?((?:[#.][\w-]+|\[[\w-]+(?:=['\"]?[^\]'\"]*['\"]?)?\])*)", sel.strip())
    if not m: raise NoSuchElementException("Seletor CSS não suportado pelo simulador: " + sel)
    tag, resto = m.group(1), m.group(2)
    if tag and tag != "*" and n.tag != tag: return False
    for p in re.findall(r"[#.][\w-]+|\[[^\]]+\]", resto):
        if p[0] == "#" and n.attrs.get("id") != p[1:]: return False
        if p[0] == "." and p[1:] not in n.attrs.get("class", "").split(): return False
        if p[0] == "[":
            a = p[1:-1]
            if "=" in a:
                k, v = a.split("=", 1); v = v.strip("'\"")
                if n.attrs.get(k) != v: return False
            elif a not in n.attrs: return False
    return True

def _css(raiz, sel):
    res = []
    for parte in sel.split(","):
        passos = parte.split()
        cands = [raiz]
        for i, p in enumerate(passos):
            prox = []
            for c in cands:
                for n in c.todos():
                    if _css_simples(p, n) and n not in prox: prox.append(n)
            cands = prox
        res += [c for c in cands if c not in res]
    return res

def _xpath(raiz, xp):
    passos = re.findall(r"(//|/)([^/\[]+(?:\[[^\]]*\])*)", xp)
    if not passos: raise NoSuchElementException("XPath não suportado pelo simulador: " + xp)
    cands = [raiz]
    for eixo, passo in passos:
        m = re.fullmatch(r"([\w*]+)((?:\[[^\]]*\])*)", passo)
        if not m: raise NoSuchElementException("XPath não suportado pelo simulador: " + xp)
        tag, conds = m.group(1), re.findall(r"\[([^\]]*)\]", m.group(2))
        prox = []
        for c in cands:
            base = list(c.todos()) if eixo == "//" else [f for f in c.filhos if isinstance(f, _No)]
            for n in base:
                if tag != "*" and n.tag != tag: continue
                ok = True
                for cd in conds:
                    cd = cd.strip()
                    a = re.fullmatch(r"@([\w-]+)\s*=\s*['\"](.*)['\"]", cd)
                    t = re.fullmatch(r"text\(\)\s*=\s*['\"](.*)['\"]", cd)
                    ct = re.fullmatch(r"contains\(\s*(@[\w-]+|text\(\))\s*,\s*['\"](.*)['\"]\s*\)", cd)
                    if a: ok = n.attrs.get(a.group(1)) == a.group(2)
                    elif t: ok = n.texto() == t.group(1)
                    elif ct:
                        alvo = n.texto() if ct.group(1) == "text()" else n.attrs.get(ct.group(1)[1:], "")
                        ok = ct.group(2) in alvo
                    elif cd.isdigit():
                        irmaos = [f for f in n.pai.filhos if isinstance(f, _No) and (tag == "*" or f.tag == tag)]
                        ok = irmaos.index(n) == int(cd) - 1
                    else: raise NoSuchElementException("Condição XPath não suportada pelo simulador: " + cd)
                    if not ok: break
                if ok and n not in prox: prox.append(n)
        cands = prox
    return cands

class By:
    ID = "id"; NAME = "name"; CLASS_NAME = "class name"; TAG_NAME = "tag name"
    CSS_SELECTOR = "css selector"; XPATH = "xpath"; LINK_TEXT = "link text"; PARTIAL_LINK_TEXT = "partial link text"

def _buscar(raiz, by, valor):
    if by == By.ID: return [n for n in raiz.todos() if n.attrs.get("id") == valor]
    if by == By.NAME: return [n for n in raiz.todos() if n.attrs.get("name") == valor]
    if by == By.CLASS_NAME:
        if " " in valor.strip(): raise NoSuchElementException("By.CLASS_NAME aceita UMA classe só. Para várias, use By.CSS_SELECTOR ('.classe1.classe2').")
        return [n for n in raiz.todos() if valor in n.attrs.get("class", "").split()]
    if by == By.TAG_NAME: return [n for n in raiz.todos() if n.tag == valor]
    if by == By.CSS_SELECTOR: return _css(raiz, valor)
    if by == By.XPATH: return _xpath(raiz, valor)
    if by == By.LINK_TEXT: return [n for n in raiz.todos() if n.tag == "a" and n.texto() == valor]
    if by == By.PARTIAL_LINK_TEXT: return [n for n in raiz.todos() if n.tag == "a" and valor in n.texto()]
    raise NoSuchElementException("Estratégia de busca desconhecida: " + repr(by))

class WebElement:
    def __init__(self, no, driver): self._n, self._d = no, driver
    def __repr__(self): return f"<WebElement {self._n.tag} id={self._n.attrs.get('id')!r}>"
    def __eq__(self, o): return isinstance(o, WebElement) and o._n is self._n
    def __hash__(self): return id(self._n)
    @property
    def tag_name(self): return self._n.tag
    @property
    def text(self): return self._n.texto()
    def get_attribute(self, nome):
        if nome in ("value",) and self._n.tag == "textarea": return self._n.attrs.get("value", self._n.texto())
        if nome in ("innerText", "textContent"): return self._n.texto()
        if nome == "checked": return "true" if "checked" in self._n.attrs else None
        return self._n.attrs.get(nome)
    def is_selected(self): return "checked" in self._n.attrs or "selected" in self._n.attrs
    def is_displayed(self): return "hidden" not in self._n.attrs and "display:none" not in self._n.attrs.get("style", "").replace(" ", "")
    def is_enabled(self): return "disabled" not in self._n.attrs
    def send_keys(self, *textos):
        if not self.is_enabled(): raise Exception("Elemento desabilitado: não aceita texto.")
        if self._n.tag not in ("input", "textarea"): raise Exception(f"send_keys só funciona em campos (input/textarea), não em <{self._n.tag}>.")
        txt = "".join(str(t) for t in textos)
        if "" in txt:
            txt = txt.replace("", ""); self._n.attrs["value"] = self._n.attrs.get("value", "") + txt; self._enviar(); return
        self._n.attrs["value"] = self._n.attrs.get("value", "") + txt
        self._d.log.append(("send_keys", self._n.attrs.get("id") or self._n.attrs.get("name"), txt))
    def clear(self): self._n.attrs["value"] = ""
    def _form(self):
        n = self._n
        while n is not None and n.tag != "form": n = n.pai
        return n
    def _enviar(self):
        f = self._form()
        if f is None: return
        dados = {}
        for c in f.todos():
            nome = c.attrs.get("name") or c.attrs.get("id")
            if not nome: continue
            if c.tag == "input" and c.attrs.get("type") in ("checkbox", "radio"):
                if "checked" in c.attrs: dados.setdefault(nome, []).append(c.attrs.get("value", "on"))
            elif c.tag == "input" and c.attrs.get("type") not in ("submit", "button"): dados[nome] = c.attrs.get("value", "")
            elif c.tag == "textarea": dados[nome] = c.attrs.get("value", c.texto())
            elif c.tag == "select":
                sel = [o for o in c.todos() if o.tag == "option" and "selected" in o.attrs]
                dados[nome] = (sel[0].attrs.get("value", sel[0].texto()) if sel else "")
        dados = {k: (v[0] if isinstance(v, list) and len(v) == 1 else v) for k, v in dados.items()}
        self._d.formularios_enviados.append(dados); self._d.log.append(("submit", f.attrs.get("id")))
    def click(self):
        n = self._n
        if not self.is_enabled(): raise Exception("Elemento desabilitado: não pode ser clicado.")
        self._d.log.append(("click", n.attrs.get("id") or n.attrs.get("name") or n.texto()))
        if n.tag == "input" and n.attrs.get("type") == "checkbox":
            if "checked" in n.attrs: del n.attrs["checked"]
            else: n.attrs["checked"] = ""
        elif n.tag == "input" and n.attrs.get("type") == "radio":
            f = self._form() or self._d._raiz
            for o in f.todos():
                if o.tag == "input" and o.attrs.get("type") == "radio" and o.attrs.get("name") == n.attrs.get("name"): o.attrs.pop("checked", None)
            n.attrs["checked"] = ""
        elif n.tag == "a" and n.attrs.get("href"):
            self._d.get(n.attrs["href"])
        elif (n.tag == "button" and n.attrs.get("type", "submit") == "submit") or (n.tag == "input" and n.attrs.get("type") == "submit"):
            self._enviar()
    def submit(self): self._enviar()
    def find_element(self, by=By.ID, value=None):
        r = _buscar(self._n, by, value)
        if not r: raise NoSuchElementException(f"Elemento não encontrado: ({by!r}, {value!r})")
        return WebElement(r[0], self._d)
    def find_elements(self, by=By.ID, value=None): return [WebElement(n, self._d) for n in _buscar(self._n, by, value)]

class Select:
    def __init__(self, el):
        if el.tag_name != "select": raise Exception("Select() só funciona com elementos <select>.")
        self._el = el
    @property
    def options(self): return [WebElement(n, self._el._d) for n in self._el._n.todos() if n.tag == "option"]
    def _marcar(self, alvo):
        for o in self.options: o._n.attrs.pop("selected", None)
        alvo._n.attrs["selected"] = ""
    def select_by_visible_text(self, t):
        for o in self.options:
            if o.text == t: return self._marcar(o)
        raise NoSuchElementException("Nenhuma opção com o texto " + repr(t))
    def select_by_value(self, v):
        for o in self.options:
            if o.get_attribute("value") == v: return self._marcar(o)
        raise NoSuchElementException("Nenhuma opção com o value " + repr(v))
    def select_by_index(self, i): self._marcar(self.options[i])
    @property
    def first_selected_option(self):
        for o in self.options:
            if o.is_selected(): return o
        return self.options[0]

class Keys:
    ENTER = ""; RETURN = ""; TAB = ""

class _Switch:
    def __init__(self, d): self._d = d
    def frame(self, ref):
        if isinstance(ref, WebElement): no = ref._n
        else:
            achados = [n for n in self._d._raiz.todos() if n.tag == "iframe" and (n.attrs.get("id") == ref or n.attrs.get("name") == ref)]
            if not achados: raise NoSuchElementException("iframe não encontrado: " + repr(ref))
            no = achados[0]
        url = no.attrs.get("src", "")
        if url not in PAGINAS: raise NoSuchElementException("Conteúdo do iframe não encontrado: " + url)
        self._d._pilha.append(self._d._raiz); self._d._raiz = _parse(PAGINAS[url])
    def default_content(self):
        if self._d._pilha: self._d._raiz = self._d._pilha[0]; self._d._pilha = []
    def parent_frame(self):
        if self._d._pilha: self._d._raiz = self._d._pilha.pop()

PAGINAS = {}

def _parse(html):
    p = _Parser(); p.feed(html); return p.raiz

class Chrome:
    def __init__(self, *a, **k):
        self._raiz = _parse("<html><head><title></title></head><body></body></html>")
        self.current_url, self.log, self.formularios_enviados, self.historico, self._pilha, self.fechado = "about:blank", [], [], [], [], False
        self.switch_to = _Switch(self); self.esperas = []
        NAVEGADORES.append(self)
    def get(self, url):
        if url not in PAGINAS: raise Exception(f"Página não encontrada no simulador: {url}. Use uma das URLs de PAGINAS.")
        self._raiz, self._pilha, self.current_url = _parse(PAGINAS[url]), [], url
        self.historico.append(url)
    @property
    def title(self):
        t = [n for n in self._raiz.todos() if n.tag == "title"]
        return t[0].texto() if t else ""
    @property
    def page_source(self): return PAGINAS.get(self.current_url, "")
    def find_element(self, by=By.ID, value=None):
        r = _buscar(self._raiz, by, value)
        if not r: raise NoSuchElementException(f"Elemento não encontrado: ({by!r}, {value!r})")
        return WebElement(r[0], self)
    def find_elements(self, by=By.ID, value=None): return [WebElement(n, self) for n in _buscar(self._raiz, by, value)]
    def implicitly_wait(self, s): self.esperas.append(s)
    def maximize_window(self): self.log.append(("maximize",))
    def execute_script(self, script, *args): self.log.append(("script", script)); return None
    def save_screenshot(self, arquivo):
        with open(arquivo, "wb") as f: f.write(b"\x89PNG\r\n\x1a\n")
        return True
    def back(self):
        if len(self.historico) > 1: self.historico.pop(); u = self.historico.pop(); self.get(u)
    def quit(self): self.fechado = True
    close = quit

Edge = Firefox = Chrome
NAVEGADORES = []

class _EC:
    @staticmethod
    def presence_of_element_located(loc): return lambda d: d.find_element(*loc)
    visibility_of_element_located = element_to_be_clickable = presence_of_element_located
    @staticmethod
    def title_contains(t): return lambda d: t in d.title

class WebDriverWait:
    def __init__(self, driver, timeout, *a, **k): self._d, self.timeout = driver, timeout; driver.esperas.append(timeout)
    def until(self, cond):
        r = cond(self._d)
        if not r: raise Exception("TimeoutException: a condição não foi atendida.")
        return r

def _registrar_selenium():
    m = {n: types.ModuleType(n) for n in ["selenium", "selenium.webdriver", "selenium.webdriver.common", "selenium.webdriver.common.by",
        "selenium.webdriver.common.keys", "selenium.webdriver.support", "selenium.webdriver.support.ui", "selenium.webdriver.support.select",
        "selenium.webdriver.support.expected_conditions", "selenium.common", "selenium.common.exceptions"]}
    wd = m["selenium.webdriver"]; wd.Chrome = Chrome; wd.Edge = Edge; wd.Firefox = Firefox
    m["selenium"].webdriver = wd; wd.common = m["selenium.webdriver.common"]; wd.support = m["selenium.webdriver.support"]
    m["selenium.webdriver.common.by"].By = By; m["selenium.webdriver.common.keys"].Keys = Keys
    m["selenium.webdriver.support.ui"].Select = Select; m["selenium.webdriver.support.ui"].WebDriverWait = WebDriverWait
    m["selenium.webdriver.support.select"].Select = Select
    ec = m["selenium.webdriver.support.expected_conditions"]
    for k in ("presence_of_element_located", "visibility_of_element_located", "element_to_be_clickable", "title_contains"): setattr(ec, k, getattr(_EC, k))
    m["selenium.webdriver.support"].expected_conditions = ec
    m["selenium.common.exceptions"].NoSuchElementException = NoSuchElementException
    m["selenium.common"].exceptions = m["selenium.common.exceptions"]
    sim = types.ModuleType("simulador_web"); sim.PAGINAS = PAGINAS; sim.NAVEGADORES = NAVEGADORES
    m["simulador_web"] = sim
    sys.modules.update(m)

_registrar_selenium()

# ------------------------------------------------------------------
# Execução
# ------------------------------------------------------------------
_last = {"out": "", "imgs": []}
_BASE = os.getcwd()

def _novo_dir():
    d = tempfile.mkdtemp(prefix="exercicio_")
    os.chdir(d)
    return d

def _exec(code, setup, kw):
    ns = {"__name__": "__main__"}
    if "matplotlib.pyplot" in sys.modules:
        sys.modules["matplotlib.pyplot"].close("all")
    _smtplib.ENVIADOS.clear(); NAVEGADORES.clear(); PAGINAS.clear()
    _novo_dir()
    buf = io.StringIO(); old = sys.stdout; sys.stdout = buf
    try:
        if setup:
            exec(compile(setup, "<dados>", "exec"), ns)
        ns.update(kw)
        exec(compile(code, "<seu código>", "exec"), ns)
    finally:
        sys.stdout = old
        _last["out"] = buf.getvalue()
    ns["saida"] = buf.getvalue()
    return ns

def _figuras():
    imgs = []
    plt = sys.modules.get("matplotlib.pyplot")
    if not plt: return imgs
    import base64
    for num in plt.get_fignums()[:4]:
        b = io.BytesIO()
        try:
            plt.figure(num).savefig(b, format="png", dpi=80, bbox_inches="tight")
            imgs.append(base64.b64encode(b.getvalue()).decode())
        except Exception:
            pass
    return imgs

def _err_info(e):
    line = None
    if isinstance(e, SyntaxError) and e.filename == "<seu código>":
        line = e.lineno
    else:
        for f in traceback.extract_tb(e.__traceback__):
            if f.filename == "<seu código>":
                line = f.lineno
    return {"err": type(e).__name__, "msg": str(e), "line": line}

def run_json(args):
    a = json.loads(args)
    code, setup, test, mode = a["code"], a.get("setup", ""), a.get("test", ""), a["mode"]
    r = {"ok": False, "out": "", "err": None, "msg": "", "line": None, "fail": None, "imgs": []}
    try:
        ns = _exec(code, setup, {})
        r["out"] = ns["saida"]
        if a.get("imgs", True): r["imgs"] = _figuras()
    except BaseException as e:
        r["out"] = _last["out"]
        r.update(_err_info(e))
        os.chdir(_BASE)
        return json.dumps(r, ensure_ascii=False)
    if mode == "test":
        env = dict(ns)
        env["rodar"] = lambda **kw: _exec(code, setup, kw)
        env["codigo"] = code
        env["_smtp"] = _smtplib
        env["_nav"] = NAVEGADORES
        buf = io.StringIO(); old = sys.stdout; sys.stdout = buf
        try:
            exec(compile(test, "<teste>", "exec"), env)
            r["ok"] = True
        except AssertionError as e:
            r["fail"] = str(e) or "O resultado não é o esperado. Confira o enunciado."
        except BaseException as e:
            info = _err_info(e)
            r["fail"] = f"{info['err']}: {info['msg']}"
            if info["line"]:
                r["line"] = info["line"]
        finally:
            sys.stdout = old
    os.chdir(_BASE)
    return json.dumps(r, ensure_ascii=False)
