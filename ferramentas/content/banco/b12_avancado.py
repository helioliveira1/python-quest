import sys, os; sys.path.insert(0, os.path.dirname(__file__))
from _h import E, ENT

TOPIC = dict(
    name="Python avançado", short="recursos que deixam o código profissional",
    cdesc="geradores, itertools, gerenciadores de contexto, regex, datetime, enum, namedtuple e type hints",
    map="bolhas", src="Banco • Avançado + Python na Prática cap. 10",
    groups=[
        ["Geradores", [["yield", "produz valores sob demanda"], ["(x for x in ...)", "expressão geradora"], ["Economia de memória", "processa um item por vez"]]],
        ["itertools", [["chain, islice", "juntar e fatiar"], ["groupby", "agrupar consecutivos"], ["product, permutations, combinations", "combinatória"]]],
        ["Contexto", [["with", "abre e fecha recursos"], ["__enter__ / __exit__", "classe gerenciadora"], ["@contextmanager", "com yield"]]],
        ["Texto e tempo", [["re", "padrões: findall, sub, match"], ["datetime / timedelta", "datas e intervalos"], ["strftime / strptime", "formatar e ler"]]],
        ["Tipos", [["Enum", "constantes com nome"], ["namedtuple", "tupla com campos"], ["Type hints", "def f(x: int) -> str"]]],
    ],
    hot=["Geradores só podem ser percorridos uma vez.",
         "groupby só agrupa itens CONSECUTIVOS: ordene antes.",
         "Use raw strings em regex: r\"\\d+\".",
         "Type hints documentam, mas o Python não os verifica em tempo de execução."],
    trap="Converter um gerador gigante com list() joga fora a vantagem de economizar memória.",
    examples=[["gerador.py", '''def pares(limite):
    n = 0
    while n <= limite:
        yield n
        n += 2

print(list(pares(10)))  # [0, 2, 4, 6, 8, 10]'''], ["contexto.py", '''from contextlib import contextmanager
import time

@contextmanager
def cronometro(nome):
    ini = time.perf_counter()
    yield
    print(f"{nome}: {time.perf_counter() - ini:.3f}s")

with cronometro("soma"):
    sum(range(1_000_000))''']],
    ex=[
        E(0, "Gerador de pares", "Crie o gerador <code>pares(limite)</code> com <code>yield</code> que produz os pares de 0 até limite.",
          'def pares(limite):\n    n = 0\n    while n <= limite:\n        yield n\n        n += 2', 'import types\nassert list(pares(10)) == [0, 2, 4, 6, 8, 10] and isinstance(pares(3), types.GeneratorType)', ["yield em vez de return", "Teste com list(pares(10))"]),
        E(0, "Expressão geradora", "Calcule <code>soma_quadrados</code> dos números de 1 a 1.000.000 com uma expressão geradora (sem criar lista).",
          'soma_quadrados = sum(x * x for x in range(1, 1_000_001))', 'assert soma_quadrados == 333333833333500000\nassert "[" not in codigo', ["sum(x * x for x in ...)", "Parênteses, não colchetes"]),
        E(0, "Enum de status", "Crie <code>Status(Enum)</code> com PENDENTE=1, PAGO=2, CANCELADO=3 e <code>pode_cancelar(s)</code> (só PENDENTE).",
          'from enum import Enum\n\nclass Status(Enum):\n    PENDENTE = 1\n    PAGO = 2\n    CANCELADO = 3\n\ndef pode_cancelar(s):\n    return s is Status.PENDENTE', 'assert pode_cancelar(Status.PENDENTE) and not pode_cancelar(Status.PAGO)\nassert Status(2) is Status.PAGO and Status["CANCELADO"].value == 3', ["from enum import Enum", "Compare com is"]),
        E(0, "namedtuple", "Crie <code>Ponto = namedtuple(...)</code> com x e y e <code>distancia(a, b)</code> (2 casas).",
          'from collections import namedtuple\nimport math\n\nPonto = namedtuple("Ponto", ["x", "y"])\n\ndef distancia(a, b):\n    return round(math.hypot(a.x - b.x, a.y - b.y), 2)', 'p, q = Ponto(0, 0), Ponto(3, 4)\nassert distancia(p, q) == 5 and q.x == 3 and q[1] == 4 and q._replace(x=0) == Ponto(0, 4)', ["namedtuple(\"Ponto\", [\"x\", \"y\"])", "math.hypot"]),
        E(1, "Fibonacci infinito", "Crie o gerador infinito <code>fib()</code> e use <code>itertools.islice</code> para guardar os 10 primeiros em <code>primeiros</code> e o primeiro termo acima de 1000 em <code>acima</code>.",
          'from itertools import islice\n\ndef fib():\n    a, b = 0, 1\n    while True:\n        yield a\n        a, b = b, a + b\n\nprimeiros = list(islice(fib(), 10))\nacima = next(x for x in fib() if x > 1000)', 'assert primeiros == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34] and acima == 1597', ["while True com yield", "next(gerador) pega o primeiro"]),
        E(1, "Pipeline de geradores", "Processe <code>linhas</code> com geradores encadeados: remova vazias, converta para int ignorando inválidas e some só os positivos em <code>total</code>.",
          'def nao_vazias(ls):\n    for l in ls:\n        if l.strip():\n            yield l.strip()\n\ndef inteiros(ls):\n    for l in ls:\n        try:\n            yield int(l)\n        except ValueError:\n            pass\n\ntotal = sum(x for x in inteiros(nao_vazias(linhas)) if x > 0)', 'assert total == 17', ["Cada etapa é um gerador", "try/except dentro do gerador"], s='linhas = ["10", "", " 5 ", "abc", "-3", "2", "  "]'),
        E(1, "groupby", "Agrupe <code>vendas</code> (mes, valor) por mês com <code>itertools.groupby</code> e crie <code>por_mes</code> ({mes: total}).",
          'from itertools import groupby\nordenadas = sorted(vendas, key=lambda v: v[0])\npor_mes = {m: sum(v for _, v in g) for m, g in groupby(ordenadas, key=lambda v: v[0])}', 'assert por_mes == {"fev": 50, "jan": 130, "mar": 5}\nassert "groupby" in codigo', ["Ordene antes de agrupar", "groupby(lista, key=...)"], s='vendas = [("jan", 100), ("fev", 50), ("jan", 30), ("mar", 5)]'),
        E(1, "Combinatória", "Com itertools: <code>senhas</code> = quantas senhas de 3 dígitos com <code>\"0123\"</code> (product), <code>duplas</code> = combinações de 2 de <code>nomes</code>, <code>ordens</code> = permutações de 3 letras de <code>\"ABC\"</code> como strings.",
          'from itertools import product, combinations, permutations\nsenhas = len(list(product("0123", repeat=3)))\nduplas = list(combinations(nomes, 2))\nordens = ["".join(p) for p in permutations("ABC")]', 'assert senhas == 64 and duplas == [("Ana", "Leo"), ("Ana", "Bia"), ("Leo", "Bia")]\nassert ordens == ["ABC", "ACB", "BAC", "BCA", "CAB", "CBA"]', ["product(..., repeat=3)", "combinations ignora a ordem"], s='nomes = ["Ana", "Leo", "Bia"]'),
        E(1, "Regex: extrair dados", "De <code>texto</code>, extraia <code>emails</code>, <code>telefones</code> (formato (81) 99999-9999) e <code>valores</code> (floats a partir de R$ 1.234,56).",
          'import re\nemails = re.findall(r"[\\w.+-]+@[\\w-]+\\.[\\w.]+", texto)\ntelefones = re.findall(r"\\(\\d{2}\\) \\d{4,5}-\\d{4}", texto)\nvalores = [float(v.replace(".", "").replace(",", ".")) for v in re.findall(r"R\\$ ([\\d.]+,\\d{2})", texto)]', 'assert emails == ["ana@email.com", "leo.silva@empresa.com.br"]\nassert telefones == ["(81) 99999-1234", "(11) 3333-4444"]\nassert valores == [1234.56, 99.9]', ["re.findall devolve todas as ocorrências", "Grupo () captura só o número"], s='texto = "Contato: ana@email.com, (81) 99999-1234. Outro: leo.silva@empresa.com.br / (11) 3333-4444. Total R$ 1.234,56 e frete R$ 99,90."'),
        E(1, "Validar com regex", "Crie <code>cpf_formatado(t)</code> (aceita só <code>000.000.000-00</code>) e <code>senha_forte(s)</code> (8+ caracteres, maiúscula, minúscula, dígito).",
          'import re\n\ndef cpf_formatado(t):\n    return re.fullmatch(r"\\d{3}\\.\\d{3}\\.\\d{3}-\\d{2}", t) is not None\n\ndef senha_forte(s):\n    return len(s) >= 8 and all(re.search(p, s) for p in [r"[A-Z]", r"[a-z]", r"\\d"])', 'assert cpf_formatado("123.456.789-09") and not cpf_formatado("12345678909") and not cpf_formatado("123.456.789-090")\nassert senha_forte("Abcdefg1") and not senha_forte("abcdefg1") and not senha_forte("Ab1")', ["re.fullmatch exige o texto inteiro", "Escape o ponto: \\."]),
        E(1, "Datas", "Com <code>datetime</code>: <code>dias</code> entre <code>inicio</code> e <code>fim</code> (textos dd/mm/aaaa), <code>vencimento</code> = inicio + 30 dias formatado dd/mm/aaaa e <code>dia_semana</code> do fim (0 = segunda).",
          'from datetime import datetime, timedelta\na = datetime.strptime(inicio, "%d/%m/%Y")\nb = datetime.strptime(fim, "%d/%m/%Y")\ndias = (b - a).days\nvencimento = (a + timedelta(days=30)).strftime("%d/%m/%Y")\ndia_semana = b.weekday()', 'assert dias == 59 and vencimento == "31/01/2026" and dia_semana == 6', ["strptime lê, strftime formata", "timedelta(days=30)"], s='inicio = "01/01/2026"\nfim = "01/03/2026"'),
        E(1, "Type hints", "Crie <code>media_notas(notas: list[float]) -> float | None</code> (None se vazia) e <code>indexar(itens: list[str]) -> dict[str, int]</code> (palavra → posição).",
          'def media_notas(notas: list[float]) -> float | None:\n    return sum(notas) / len(notas) if notas else None\n\ndef indexar(itens: list[str]) -> dict[str, int]:\n    return {s: i for i, s in enumerate(itens)}', 'assert media_notas([7.0, 9.0]) == 8 and media_notas([]) is None and indexar(["a", "b"]) == {"a": 0, "b": 1}\nassert media_notas.__annotations__["return"] is not None and "->" in codigo', ["Anotações depois de : e ->", "float | None aceita None"]),
        E(2, "Gerenciador de contexto", "Crie a classe <code>Transacao</code> (com <code>__enter__</code>/<code>__exit__</code>) sobre um dicionário: se o bloco lançar erro, restaura o estado original e não propaga o erro.",
          'import copy\n\nclass Transacao:\n    def __init__(self, dados):\n        self.dados = dados\n\n    def __enter__(self):\n        self.copia = copy.deepcopy(self.dados)\n        return self.dados\n\n    def __exit__(self, tipo, valor, tb):\n        if tipo is not None:\n            self.dados.clear()\n            self.dados.update(self.copia)\n            return True\n        return False', 'conta = {"saldo": 100, "hist": []}\nwith Transacao(conta) as c:\n    c["saldo"] -= 30; c["hist"].append(-30)\nassert conta == {"saldo": 70, "hist": [-30]}\nwith Transacao(conta) as c:\n    c["saldo"] -= 500; c["hist"].append(-500)\n    raise ValueError("saldo negativo")\nassert conta == {"saldo": 70, "hist": [-30]}', ["Guarde uma cópia profunda no __enter__", "__exit__ devolvendo True engole o erro"]),
        E(2, "@contextmanager", "Crie <code>pasta_temporaria()</code> com <code>@contextmanager</code>: cria uma pasta nova, entrega o caminho e a apaga ao final, mesmo com erro.",
          'import os, shutil, tempfile\nfrom contextlib import contextmanager\n\n@contextmanager\ndef pasta_temporaria():\n    p = tempfile.mkdtemp()\n    try:\n        yield p\n    finally:\n        shutil.rmtree(p)', 'import os\nwith pasta_temporaria() as p:\n    open(os.path.join(p, "a.txt"), "w").write("x")\n    assert os.path.isdir(p)\nassert not os.path.exists(p)\ntry:\n    with pasta_temporaria() as q:\n        raise RuntimeError\nexcept RuntimeError:\n    pass\nassert not os.path.exists(q)', ["try/finally em volta do yield", "tempfile.mkdtemp e shutil.rmtree"]),
        E(2, "Leitura em lotes", "Crie o gerador <code>lotes(iteravel, n)</code> que entrega listas de até n itens, funcionando com qualquer iterável (inclusive geradores infinitos).",
          'from itertools import islice\n\ndef lotes(iteravel, n):\n    it = iter(iteravel)\n    while True:\n        bloco = list(islice(it, n))\n        if not bloco:\n            return\n        yield bloco', 'assert list(lotes(range(7), 3)) == [[0, 1, 2], [3, 4, 5], [6]] and list(lotes([], 2)) == []\nimport itertools as _it\nassert next(lotes(_it.count(), 4)) == [0, 1, 2, 3]', ["iter() + islice", "Pare quando o bloco vier vazio"]),
    ],
)
