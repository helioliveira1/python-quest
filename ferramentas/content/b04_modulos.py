TOPIC = dict(
    name="Módulos e bibliotecas", short="usar código pronto",
    cdesc="import, from ... import, apelidos, time, math, random e instalação com pip",
    map="radial", src="Básico • Módulo 17",
    groups=[
        ["Importar", [["import modulo", "usa como modulo.funcao()"], ["import modulo as apelido", "import numpy as np"], ["from modulo import x", "usa x direto, sem prefixo"]]],
        ["Módulo time", [["time.time()", "segundos desde a EPOCH (01/01/1970)"], ["time.sleep(s)", "pausa o programa"], ["time.gmtime() / ctime()", "data detalhada / texto"]]],
        ["Outros da biblioteca padrão", [["math", "sqrt, ceil, floor, pi"], ["random", "randint, choice, shuffle; seed repete o sorteio"], ["statistics / collections", "mean, median; Counter"]]],
        ["Explorar", [["dir(modulo)", "lista o que o módulo tem"], ["help(funcao)", "mostra a documentação"], ["Documentação oficial", "docs.python.org"]]],
        ["Instalar", [["pip install nome", "baixa bibliotecas de terceiros"], ["pip freeze", "lista o que está instalado"], ["ModuleNotFoundError", "biblioteca não instalada (ou nome errado)"]]],
    ],
    hot=[
        "Depois de import modulo, sempre use modulo.funcao().",
        "from modulo import funcao traz só aquela função, sem prefixo.",
        "random.seed(n) faz o sorteio se repetir: ótimo para testes.",
        "time.time() serve para medir quanto tempo um trecho demora.",
        "ModuleNotFoundError: confira o nome e instale com pip install.",
    ],
    trap="Não dê ao seu arquivo o mesmo nome de uma biblioteca (ex.: random.py): o import passa a pegar o SEU arquivo.",
    examples=[["modulos.py", '''import math
import random as rd
from time import time, sleep

inicio = time()
print(math.sqrt(16), math.ceil(2.1), math.pi)

rd.seed(42)
print(rd.randint(1, 6), rd.choice(["a", "b", "c"]))

sleep(0.5)
print(f"Levou {time() - inicio:.2f} s")'''], ["explorar.py", '''import statistics
from collections import Counter

print(dir(statistics)[:5])     # o que existe no módulo
help(statistics.median)        # documentação

print(Counter("banana"))       # Counter({'a': 3, 'n': 2, 'b': 1})

try:
    import biblioteca_que_nao_existe
except ModuleNotFoundError:
    print("Instale com: pip install ...")''']],
    ex=[
        dict(t="Raiz quadrada", p="Importe <code>math</code> e guarde em <code>raiz</code> a raiz quadrada de <code>numero</code>.", s="numero = 81",
             sol="import math\nraiz = math.sqrt(numero)", test='assert raiz == 9, "√81 = 9"\nassert rodar(numero=2)["raiz"] == 2 ** 0.5, "Use a variável numero"\nassert "math" in codigo, "Use o módulo math"',
             h=["import math", "math.sqrt(numero)"]),
        dict(t="Apelido", p="Importe <code>statistics</code> com o apelido <code>st</code> e calcule a <code>mediana</code> da lista <code>idades</code>.", s="idades = [30, 18, 45, 22, 27]",
             sol="import statistics as st\nmediana = st.median(idades)", test='assert mediana == 27, "Mediana de [18, 22, 27, 30, 45] = 27"\nassert st.median is not None and "as st" in codigo, "Use import statistics as st"',
             h=["import statistics as st", "st.median(lista)"]),
        dict(t="from ... import", p="Usando <code>from math import ceil, floor</code>, guarde em <code>cima</code> o arredondamento para cima e em <code>baixo</code> o arredondamento para baixo de <code>valor</code>.", s="valor = 7.3",
             sol="from math import ceil, floor\ncima = ceil(valor)\nbaixo = floor(valor)", test='assert (cima, baixo) == (8, 7), "ceil(7.3) = 8 e floor(7.3) = 7"\nassert "from math import" in codigo, "Use from math import ..."',
             h=["Com from ... import a função é usada sem prefixo", "ceil arredonda para cima; floor para baixo"]),
        dict(t="Área do círculo com pi", p="Calcule a <code>area</code> do círculo de raio <code>raio</code> usando <code>math.pi</code>, arredondada para 2 casas.", s="raio = 3",
             sol="import math\narea = round(math.pi * raio ** 2, 2)", test='assert area == 28.27, "π × 3² ≈ 28.27"\nassert rodar(raio=1)["area"] == 3.14, "Use a variável raio"',
             h=["math.pi", "round(valor, 2)"]),
        dict(t="Ano da EPOCH", p="Use <code>time.gmtime(0)</code> para descobrir o ano da EPOCH (o \"marco zero\") e guarde em <code>ano_epoch</code>.", s="",
             sol="import time\nano_epoch = time.gmtime(0).tm_year", test='assert ano_epoch == 1970, "A EPOCH é 01/01/1970"\nassert "gmtime" in codigo, "Use time.gmtime(0)"',
             h=["time.gmtime(0) devolve uma estrutura com campos", "O ano fica em .tm_year"]),
        dict(t="Sorteio reprodutível", p="Defina <code>random.seed(semente)</code> e sorteie 3 números com <code>random.randint(1, 60)</code>, guardando-os na lista <code>sorteados</code> (na ordem).", s="semente = 42",
             sol="import random\nrandom.seed(semente)\nsorteados = [random.randint(1, 60) for _ in range(3)]",
             test='import random as _r\n_r.seed(42); esperado = [_r.randint(1, 60) for _ in range(3)]\nassert sorteados == esperado, "Chame random.seed(semente) ANTES de sortear"\n_r.seed(7); esp7 = [_r.randint(1, 60) for _ in range(3)]\nassert rodar(semente=7)["sorteados"] == esp7, "Use a variável semente"',
             h=["A semente fixa a sequência de sorteios", "random.randint(1, 60) três vezes"]),
        dict(t="Escolher e embaralhar", p="Com <code>random.seed(1)</code>, escolha um vencedor de <code>participantes</code> com <code>random.choice</code> e guarde em <code>vencedor</code>. Depois embaralhe uma <b>cópia</b> da lista em <code>ordem</code> com <code>random.shuffle</code>, sem alterar <code>participantes</code>.", s='participantes = ["Ana", "Bia", "Caio", "Davi", "Eva"]',
             sol="import random\nrandom.seed(1)\nvencedor = random.choice(participantes)\nordem = participantes.copy()\nrandom.shuffle(ordem)",
             test='import random as _r\n_r.seed(1); v = _r.choice(participantes); o = list(participantes); _r.shuffle(o)\nassert vencedor == v, "Use random.seed(1) e depois random.choice"\nassert ordem == o, "Embaralhe a cópia com random.shuffle logo depois do choice"\nassert participantes == ["Ana", "Bia", "Caio", "Davi", "Eva"], "A lista original não pode mudar"',
             h=["shuffle altera a lista no lugar e retorna None", "Use participantes.copy()"]),
        dict(t="Medir tempo", p="Use <code>time.time()</code> antes e depois de somar os números de 0 a <code>n</code> (com <code>sum(range(n + 1))</code>). Guarde a soma em <code>total</code> e o tempo gasto (em segundos) em <code>duracao</code>.", s="n = 100000",
             sol="import time\ninicio = time.time()\ntotal = sum(range(n + 1))\nduracao = time.time() - inicio",
             test='assert total == 5000050000, "Soma de 0 a 100000"\nassert isinstance(duracao, float) and 0 <= duracao < 5, "duracao = fim - inicio, em segundos"\nassert codigo.count("time.time()") >= 2 or codigo.count("time()") >= 2, "Chame time.time() antes e depois"',
             h=["inicio = time.time()", "duracao = time.time() - inicio"]),
        dict(t="Contar com Counter", p="Use <code>collections.Counter</code> para contar as vendas por produto em <code>vendas</code> e guarde os 2 mais vendidos em <code>top2</code> (lista de tuplas, use <code>most_common</code>).", s='vendas = ["café", "pão", "café", "leite", "pão", "café", "bolo"]',
             sol="from collections import Counter\ncontagem = Counter(vendas)\ntop2 = contagem.most_common(2)",
             test='assert top2 == [("café", 3), ("pão", 2)], "Os 2 mais vendidos: café (3) e pão (2)"',
             h=["from collections import Counter", "Counter(lista).most_common(2)"]),
        dict(t="Explorar com dir()", p="Usando <code>dir(math)</code>, crie a lista <code>funcoes_trig</code> com os nomes que começam com <code>\"a\"</code> e terminam com <code>\"h\"</code> (ex.: <code>acosh</code>), em ordem alfabética.", s="",
             sol='import math\nfuncoes_trig = sorted(n for n in dir(math) if n.startswith("a") and n.endswith("h"))',
             test='assert funcoes_trig == ["acosh", "asinh", "atanh"], "Esperado [\\"acosh\\", \\"asinh\\", \\"atanh\\"]"',
             h=["dir(math) devolve uma lista de nomes (str)", "Filtre com startswith e endswith"]),
        dict(t="Import seguro", p="Tente importar o módulo cujo nome está em <code>nome_modulo</code> usando <code>importlib.import_module</code>. Se der <code>ModuleNotFoundError</code>, guarde em <code>mensagem</code> o texto <code>Instale com: pip install X</code> (X = nome); se der certo, <code>mensagem = \"ok\"</code>.", s='nome_modulo = "biblioteca_fantasia"',
             sol='import importlib\ntry:\n    importlib.import_module(nome_modulo)\n    mensagem = "ok"\nexcept ModuleNotFoundError:\n    mensagem = f"Instale com: pip install {nome_modulo}"',
             test='assert mensagem == "Instale com: pip install biblioteca_fantasia"\nassert rodar(nome_modulo="json")["mensagem"] == "ok", "Módulo existente: mensagem = \\"ok\\""',
             h=["importlib.import_module(\"nome\") importa pelo texto", "except ModuleNotFoundError:"]),
        dict(t="Arredondar parcelas", p="Uma compra de <code>valor</code> será paga em <code>parcelas</code> iguais, arredondadas <b>para cima</b> no centavo. Calcule <code>parcela</code> com <code>math.ceil</code> (dica: trabalhe em centavos).", s="valor = 100\nparcelas = 3",
             sol="import math\nparcela = math.ceil(valor * 100 / parcelas) / 100",
             test='assert parcela == 33.34, "100 / 3 arredondado para cima = 33.34"\nassert rodar(valor=10, parcelas=4)["parcela"] == 2.5\nassert rodar(valor=50, parcelas=6)["parcela"] == 8.34',
             h=["Multiplique por 100, arredonde com ceil e divida por 100", "math.ceil(valor * 100 / parcelas) / 100"]),
        dict(t="Estatísticas da turma", p="Com o módulo <code>statistics</code>, crie o dicionário <code>resumo</code> com as chaves <code>media</code>, <code>mediana</code> e <code>desvio</code> (desvio padrão amostral, <code>stdev</code>) das <code>notas</code>, arredondadas para 2 casas.", s="notas = [7.5, 8.0, 6.0, 9.5, 7.0, 8.5]",
             sol='import statistics as st\nresumo = {\n    "media": round(st.mean(notas), 2),\n    "mediana": round(st.median(notas), 2),\n    "desvio": round(st.stdev(notas), 2),\n}',
             test='import statistics as _s\nassert resumo == {"media": 7.75, "mediana": 7.75, "desvio": round(_s.stdev(notas), 2)}, "Confira as 3 medidas com round(..., 2)"\nr = rodar(notas=[1, 2, 3])["resumo"]\nassert r == {"media": 2, "mediana": 2, "desvio": 1.0}, "Use a variável notas"',
             h=["st.mean, st.median e st.stdev", "Monte o dicionário com round(..., 2)"]),
        dict(t="Senha aleatória", p="Usando <code>random</code> (com <code>random.seed(semente)</code>) e <code>string</code>, gere <code>senha</code> com <code>tamanho</code> caracteres sorteados com <code>random.choice</code> de <code>string.ascii_letters + string.digits</code>.", s="semente = 10\ntamanho = 8",
             sol='import random, string\nrandom.seed(semente)\nletras = string.ascii_letters + string.digits\nsenha = "".join(random.choice(letras) for _ in range(tamanho))',
             test='import random as _r, string as _st\n_r.seed(10); esp = "".join(_r.choice(_st.ascii_letters + _st.digits) for _ in range(8))\nassert senha == esp, "Sorteie com random.choice, depois de random.seed(semente)"\nassert len(rodar(tamanho=12)["senha"]) == 12, "Use a variável tamanho"',
             h=["string.ascii_letters + string.digits", "\"\".join(...) junta os caracteres"]),
        dict(t="Desafio: cronômetro de funções", p="Crie <code>cronometrar(funcao, *args)</code> que executa <code>funcao(*args)</code> e retorna a tupla <code>(resultado, segundos)</code>, medindo com <code>time.perf_counter()</code>.", s="",
             sol='import time\n\ndef cronometrar(funcao, *args):\n    inicio = time.perf_counter()\n    resultado = funcao(*args)\n    return resultado, time.perf_counter() - inicio',
             test='r, s = cronometrar(sum, [1, 2, 3])\nassert r == 6, "Retorne o resultado da função"\nassert isinstance(s, float) and s >= 0, "Segundos = fim - início"\nimport time as _t\nr2, s2 = cronometrar(_t.sleep, 0.05)\nassert s2 >= 0.04, "Meça o tempo em volta da chamada"\nassert cronometrar(max, 4, 9, 2)[0] == 9, "Repasse os argumentos com *args"',
             h=["Funções também podem ser passadas como argumento", "inicio = time.perf_counter(); resultado = funcao(*args)"]),
    ],
)
