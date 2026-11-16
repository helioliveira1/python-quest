"""Monta data/*.js a partir das fases reaproveitadas (reused.json) e das novas (content/*.py)."""
import json, importlib.util, os, copy

R = {t["name"]: t for t in json.load(open("fases_reaproveitadas.json", encoding="utf-8"))}

def load(nome):
    spec = importlib.util.spec_from_file_location(nome, f"content/{nome}.py")
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m.TOPIC

def reuse(nome, **extra):
    t = copy.deepcopy(R[nome]); t.update(extra); t["origem"] = "reaproveitada"
    return t

# ---------- ajustes nas fases reaproveitadas ----------
it = reuse("Iteráveis", name="Iteráveis, range e set", short="percorrer, gerar e eliminar repetidos",
           cdesc="iteráveis, iteradores, range, set (conjuntos) e geradores", map="bolhas", src="Fundamentos • Módulo 13")
it["groups"].insert(1, ["range e set", [["range(início, fim, passo)", "sequência de números (fim não incluso)"],
                                         ["set", "sem repetidos e sem ordem: {1, 2, 3}"],
                                         ["Operações de set", "& interseção, | união, - diferença"]]])
it["hot"] += ["set(lista) remove duplicados num passo só (mas perde a ordem).", "range(10) vai de 0 a 9: o fim nunca entra."]
it["ex"][9] = dict(t="Remover duplicados com set", p="Crie <code>unicos</code>: os produtos de <code>vendidos</code> sem repetição, em ordem alfabética, e <code>qtd_unicos</code> com quantos são.",
                   s='vendidos = ["café", "pão", "café", "leite", "pão", "bolo"]',
                   sol="unicos = sorted(set(vendidos))\nqtd_unicos = len(set(vendidos))",
                   test='assert unicos == ["bolo", "café", "leite", "pão"]\nassert qtd_unicos == 4\nassert rodar(vendidos=["a", "a"])["unicos"] == ["a"], "Use a variável vendidos"',
                   h=["set(lista) elimina os repetidos", "sorted(set(...)) devolve uma lista ordenada"])
it["ex"][13] = dict(t="Clientes em comum (set)", p="Com sets, crie <code>ambos</code> (clientes que compraram nas duas lojas), <code>so_a</code> (só na loja A) e <code>todos</code> (qualquer loja), cada um como lista ordenada.",
                    s='loja_a = ["Ana", "Leo", "Bia", "Ana"]\nloja_b = ["Bia", "Caio", "Leo"]',
                    sol="a, b = set(loja_a), set(loja_b)\nambos = sorted(a & b)\nso_a = sorted(a - b)\ntodos = sorted(a | b)",
                    test='assert ambos == ["Bia", "Leo"], "Interseção: &"\nassert so_a == ["Ana"], "Diferença: -"\nassert todos == ["Ana", "Bia", "Caio", "Leo"], "União: |"',
                    h=["Converta as listas com set()", "& interseção, - diferença, | união"])

lam = reuse("Functions (avançado)", name="Funções como parâmetro e lambda", short="funções que recebem e criam funções",
            cdesc="lambda, funções como argumento (map, sorted, key), closures e decoradores", map="chaves", src="Intermediário • Módulo 20")
lam["groups"][1][1].append(["key=", "sorted(lista, key=lambda x: x[1]) / max(..., key=...)"])
lam["hot"].insert(0, "lambda é uma função de uma linha: lambda x: x * 1.1 — ideal para key= e map.")

FUND = [
    load("f01_logica"),
    reuse("Variáveis", map="arvore", src="Fundamentos • Módulo 5"),
    reuse("Condições", name="Condições (if, elif, else)", map="fluxo", src="Fundamentos • Módulo 6"),
    reuse("Strings", map="chaves", src="Fundamentos • Módulo 7"),
    reuse("Listas", map="radial", src="Fundamentos • Módulo 8"),
    reuse("Laço FOR", map="fluxo", src="Fundamentos • Módulo 9"),
    reuse("Laço WHILE", map="fluxo", src="Fundamentos • Módulo 10"),
    reuse("Tuplas", map="bolhas", src="Fundamentos • Módulo 11"),
    reuse("Dicionários", map="radial", src="Fundamentos • Módulo 12"),
    it,
]
BAS = [
    reuse("Função (básico)", name="Funções", map="fluxo", src="Básico • Módulo 14"),
    load("b02_argumentos"),
    reuse("List Comprehension", map="chaves", src="Básico • Módulo 15"),
    load("b04_modulos"),
    reuse("Orientação a Objetos", name="Orientação a Objetos (introdução)", map="radial", src="Básico • Módulo 17"),
]
INTER = [
    lam,
    load("i02_numpy"),
    reuse("Pandas", map="arvore", src="Intermediário • Módulo 22", pkgs=["pandas"]),
    load("i04_docs"),
    load("i05_graficos"),
    load("i06_arquivos"),
    load("i07_pastas"),
    load("i08_email"),
    load("i09_sql"),
    load("i10_selenium"),
    load("i11_bs4"),
]

MODS = [
    dict(id="fundamentos", name="Fundamentos", icon="🧱", color="#1E5AA8", pdf="0_PYTHON_FUNDAMENTOS.pdf",
         desc="Lógica, variáveis, if, strings, listas, for, while, tuplas, dicionários e iteráveis.", topics=FUND),
    dict(id="basico", name="Básico", icon="🧩", color="#0B2545", pdf="1_PYTHON_BASICO.pdf",
         desc="Funções, argumentos e exceções, list comprehension, módulos e orientação a objetos.", topics=BAS),
    dict(id="intermediario", name="Intermediário", icon="🚀", color="#5C6773", pdf="2_PYTHON_INTERMEDIARIO.pdf",
         desc="Lambda, NumPy, Pandas, datas e APIs, gráficos, arquivos, e-mail, SQL, Selenium e web scraping.", topics=INTER),
]

if __name__ == "__main__":
    out = "../data"
    os.makedirs(out, exist_ok=True)
    allt = []
    for m in MODS:
        for t in m["topics"]:
            assert len(t["ex"]) == 15, (m["id"], t["name"])
            for k in ("name", "short", "cdesc", "groups", "hot", "trap", "examples", "ex", "map", "src"):
                assert k in t, (t["name"], k)
            allt.append(t)
        js = "window.PQ_DATA = window.PQ_DATA || {};\nwindow.PQ_DATA[%s] = %s;\n" % (json.dumps(m["id"]), json.dumps(m, ensure_ascii=False, separators=(",", ":")))
        open(f"{out}/{m['id']}.js", "w", encoding="utf-8").write(js)
        print(m["id"], len(m["topics"]), "fases,", sum(len(t["ex"]) for t in m["topics"]), "exercícios,", len(js) // 1024, "KB")
    json.dump(allt, open("all_topics.json", "w"), ensure_ascii=False)
    print("total:", len(allt), "fases,", sum(len(t["ex"]) for t in allt), "exercícios")
    h = open("harness.py", encoding="utf-8").read()
    open("../assets/harness.js", "w", encoding="utf-8").write("window.PQ_HARNESS = " + json.dumps(h, ensure_ascii=False) + ";\n")
    print("assets/harness.js atualizado")
