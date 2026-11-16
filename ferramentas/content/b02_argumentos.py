TOPIC = dict(
    name="Argumentos, retornos e exceções", short="funções flexíveis e seguras",
    cdesc="posição × palavra-chave, valores padrão, vários retornos, docstrings, try/except e *args/**kwargs",
    map="chaves", src="Básico • Módulo 14",
    groups=[
        ["Argumentos", [["Posicionais", "f(10, 5): a ordem define quem é quem"], ["Palavra-chave", "f(nota2=5, nota1=10): ordem livre"], ["Regra", "depois de um keyword, todos os seguintes também"]]],
        ["Valores padrão", [["def f(x, padrao='m')", "argumento opcional"], ["Exemplo do Python", "sort() usa reverse=False por padrão"], ["Ordem", "parâmetros com padrão ficam no final"]]],
        ["Return", [["Encerra a função", "nada depois do return roda"], ["Vários valores", "return a, b vira uma tupla"], ["Unpacking", "perc, lista = funcao(...)"]]],
        ["Documentação", [["Docstring", "'''texto''' logo abaixo do def"], ["Annotations", "def f(x: int) -> float"], ["help(f)", "mostra a docstring"]]],
        ["Erros", [["try / except", "trata o erro sem parar o programa"], ["else / finally", "else: deu certo; finally: sempre roda"], ["raise", "cria seu próprio erro com mensagem"]]],
        ["Múltiplos argumentos", [["*args", "recebe vários posicionais numa tupla"], ["**kwargs", "recebe várias palavras-chave num dict"], ["Ordem", "normais, *args, com padrão, **kwargs"]]],
    ],
    hot=[
        "Argumentos por posição seguem a ordem do def; por palavra-chave, não.",
        "Depois que você usa um argumento por palavra-chave, os seguintes também precisam ser por palavra-chave.",
        "O return encerra a função imediatamente, mesmo dentro de um for.",
        "return a, b devolve uma TUPLA: desempacote com x, y = funcao().",
        "Todo try precisa de pelo menos um except (ou finally).",
        "*args vira tupla e **kwargs vira dicionário dentro da função.",
    ],
    trap="Colocar return dentro do for faz a função parar na 1ª volta. Acumule numa lista e retorne depois do laço.",
    examples=[["argumentos.py", '''def gerar_codigo(nome, padrao="m"):
    """Gera o código do produto. padrao: 'm' minúsculo ou 'M' maiúsculo."""
    codigo = nome.replace(" ", "_")
    return codigo.upper() if padrao == "M" else codigo.lower()

print(gerar_codigo("Vinho Tinto"))              # vinho_tinto
print(gerar_codigo("Vinho Tinto", padrao="M"))  # VINHO_TINTO

def operacoes(a: float, b: float) -> tuple:
    return a + b, a - b, a * b, a / b

soma, dif, mult, div = operacoes(10, 2)'''], ["erros_e_args.py", '''def descobrir_servidor(email):
    try:
        servidor = email.split("@")[1]
    except IndexError:
        raise ValueError("E-mail sem @")
    else:
        return servidor.split(".")[0]

def media(*notas):              # notas é uma tupla
    return sum(notas) / len(notas)

def preco_final(preco, **adicionais):   # adicionais é um dict
    preco -= adicionais.get("desconto", 0)
    preco += adicionais.get("garantia_extra", 0)
    return preco * (1 + adicionais.get("imposto", 0))''']],
    ex=[
        dict(t="Bebida alcoólica?", p="Crie <code>eh_alcoolico(codigo)</code> que retorna <code>True</code> se o código começa com <code>BEB</code> e <code>False</code> caso contrário (ex.: <code>BSA11104</code> é não alcoólico).", s="",
             sol='def eh_alcoolico(codigo):\n    return codigo.startswith("BEB")',
             test='assert eh_alcoolico("BEB12302") is True, "BEB... é alcoólico"\nassert eh_alcoolico("BSA11104") is False, "BSA... não é"\nassert eh_alcoolico("beb1") is False, "Só o prefixo BEB em maiúsculas"',
             h=["str tem o método startswith()", "return codigo.startswith(\"BEB\")"]),
        dict(t="Valor padrão", p="Crie <code>gerar_codigo(nome, padrao=\"m\")</code> que troca espaços por <code>_</code> e devolve tudo em minúsculas; se <code>padrao == \"M\"</code>, devolve em maiúsculas.", s="",
             sol='def gerar_codigo(nome, padrao="m"):\n    codigo = nome.replace(" ", "_")\n    if padrao == "M":\n        return codigo.upper()\n    return codigo.lower()',
             test='assert gerar_codigo("Vinho Tinto") == "vinho_tinto", "O padrão é minúsculo"\nassert gerar_codigo("Vinho Tinto", padrao="M") == "VINHO_TINTO", "Com padrao=\\"M\\" deve ser maiúsculo"\nassert gerar_codigo("Suco Uva", "M") == "SUCO_UVA", "Também deve aceitar por posição"',
             h=["def gerar_codigo(nome, padrao=\"m\"):", "Use replace(\" \", \"_\") e depois upper()/lower()"]),
        dict(t="Chamada por palavra-chave", p="A função <code>classificar(produto, categoria)</code> já existe. Chame-a passando os argumentos <b>por palavra-chave</b> em ordem invertida (categoria primeiro), com <code>produto=\"Vinho\"</code> e <code>categoria=\"bebida\"</code>, e guarde em <code>resultado</code>.",
             s='def classificar(produto, categoria):\n    return f"{produto} -> {categoria}"',
             sol='resultado = classificar(categoria="bebida", produto="Vinho")',
             test='assert resultado == "Vinho -> bebida", "Com palavra-chave a ordem não importa"\nassert "categoria=" in codigo and "produto=" in codigo, "Passe os dois argumentos por palavra-chave"',
             h=["nome_do_parametro=valor", "classificar(categoria=..., produto=...)"]),
        dict(t="Vários retornos", p="Crie <code>operacoes(a, b)</code> que retorna soma, diferença, produto e divisão (nessa ordem). Depois desempacote <code>operacoes(10, 2)</code> em <code>soma, dif, mult, div</code>.", s="",
             sol='def operacoes(a, b):\n    return a + b, a - b, a * b, a / b\n\nsoma, dif, mult, div = operacoes(10, 2)',
             test='assert operacoes(9, 3) == (12, 6, 27, 3.0), "Retorne uma tupla (soma, diferença, produto, divisão)"\nassert (soma, dif, mult, div) == (12, 8, 20, 5.0), "Desempacote o resultado de operacoes(10, 2)"',
             h=["return a + b, a - b, ... vira uma tupla", "soma, dif, mult, div = operacoes(10, 2)"]),
        dict(t="Docstring e annotations", p="Crie <code>area(base: float, altura: float) -&gt; float</code> que retorna base × altura e tenha uma docstring (qualquer texto).", s="",
             sol='def area(base: float, altura: float) -> float:\n    """Calcula a área de um retângulo."""\n    return base * altura',
             test='assert area(3, 4) == 12, "3 × 4 = 12"\nassert area.__doc__ and area.__doc__.strip(), "Escreva uma docstring logo abaixo do def"\nassert area.__annotations__ == {"base": float, "altura": float, "return": float}, "Anote base: float, altura: float e -> float"',
             h=["Docstring = texto com três aspas na 1ª linha da função", "def area(base: float, altura: float) -> float:"]),
        dict(t="Return dentro do for", p="A função abaixo deveria devolver a lista de números pares, mas devolve só o primeiro. Corrija e mantenha o nome <code>pares</code>.<pre class='code'>def pares(numeros):\n    for n in numeros:\n        if n % 2 == 0:\n            return n</pre>", s="",
             sol='def pares(numeros):\n    resultado = []\n    for n in numeros:\n        if n % 2 == 0:\n            resultado.append(n)\n    return resultado',
             test='assert pares([1, 2, 3, 4, 6]) == [2, 4, 6], "Deve retornar todos os pares numa lista"\nassert pares([1, 3]) == [], "Sem pares: lista vazia"',
             h=["O return encerra a função na hora", "Acumule numa lista e retorne depois do for"]),
        dict(t="Vendedores acima da meta", p="Crie <code>bateram_meta(vendas, meta)</code> que recebe um dicionário <code>{vendedor: valor}</code> e retorna uma tupla: (percentual de vendedores que bateram a meta, lista dos que bateram). O percentual vai de 0 a 1.", s="",
             sol='def bateram_meta(vendas, meta):\n    acima = [v for v, valor in vendas.items() if valor >= meta]\n    return len(acima) / len(vendas), acima',
             test='perc, lista = bateram_meta({"Ana": 1200, "Leo": 800, "Bia": 1500, "Rui": 900}, 1000)\nassert perc == 0.5, "2 de 4 bateram: 0.5"\nassert lista == ["Ana", "Bia"], "Lista na ordem do dicionário"\nassert bateram_meta({"X": 10}, 10) == (1.0, ["X"]), "Quem iguala a meta também bateu"',
             h=["Percorra vendas.items()", "return percentual, lista"]),
        dict(t="Tratar erro de conversão", p="Crie <code>converter(texto)</code> que tenta <code>int(texto)</code>; se der <code>ValueError</code>, retorna <code>None</code>.", s="",
             sol='def converter(texto):\n    try:\n        return int(texto)\n    except ValueError:\n        return None',
             test='assert converter("42") == 42, "\\"42\\" vira 42"\nassert converter("abc") is None, "Texto inválido retorna None"\nassert converter("7") == 7\nassert "except" in codigo, "Use try/except"',
             h=["try: ... except ValueError: ...", "Dentro do except: return None"]),
        dict(t="Média com *args", p="Crie <code>media(*notas)</code> que aceita qualquer quantidade de notas e retorna a média. Sem notas, retorne <code>0</code>.", s="",
             sol='def media(*notas):\n    if not notas:\n        return 0\n    return sum(notas) / len(notas)',
             test='assert media(10, 5) == 7.5, "media(10, 5) = 7.5"\nassert media(7, 8, 9, 10) == 8.5, "Deve aceitar mais de 2 notas"\nassert media() == 0, "Sem notas: 0"',
             h=["*notas vira uma tupla", "sum(notas) / len(notas) e trate o caso vazio"]),
        dict(t="Preço final com **kwargs", p="Crie <code>preco_final(preco, **adicionais)</code>: subtraia <code>desconto</code>, some <code>garantia_extra</code> e aplique <code>imposto</code> (fração, ex. 0.1) se existirem. Arredonde para 2 casas.", s="",
             sol='def preco_final(preco, **adicionais):\n    preco = preco - adicionais.get("desconto", 0)\n    preco = preco + adicionais.get("garantia_extra", 0)\n    preco = preco * (1 + adicionais.get("imposto", 0))\n    return round(preco, 2)',
             test='assert preco_final(100) == 100, "Sem adicionais, o preço não muda"\nassert preco_final(100, desconto=10) == 90, "Desconto subtrai"\nassert preco_final(100, desconto=10, garantia_extra=20, imposto=0.1) == 121.0, "(100 - 10 + 20) × 1.1 = 121"\nassert preco_final(50, imposto=0.2) == 60.0, "50 × 1.2 = 60"',
             h=["**adicionais é um dicionário", "adicionais.get(\"desconto\", 0) evita KeyError"]),
        dict(t="Descobrir o servidor", p="Crie <code>descobrir_servidor(email)</code> que retorna o nome do servidor (<code>ana@gmail.com</code> → <code>gmail</code>). Se não houver <code>@</code>, faça <code>raise ValueError(\"E-mail inválido\")</code>.", s="",
             sol='def descobrir_servidor(email):\n    try:\n        dominio = email.split("@")[1]\n    except IndexError:\n        raise ValueError("E-mail inválido")\n    return dominio.split(".")[0]',
             test='assert descobrir_servidor("ana@gmail.com") == "gmail"\nassert descobrir_servidor("leo@empresa.com.br") == "empresa"\ntry:\n    descobrir_servidor("semarroba.com")\n    assert False, "Sem @ deve gerar ValueError"\nexcept ValueError as e:\n    assert "inválido" in str(e), "Mensagem: E-mail inválido"',
             h=["email.split(\"@\")[1] dá IndexError se não houver @", "raise ValueError(\"E-mail inválido\")"]),
        dict(t="try / except / else / finally", p="Crie <code>dividir(a, b)</code> que retorna <code>a / b</code>; se <code>b</code> for zero retorna a string <code>\"erro\"</code>. Em todos os casos, adicione <code>\"fim\"</code> à lista global <code>log</code> (use <code>finally</code>).", s="log = []",
             sol='def dividir(a, b):\n    try:\n        resultado = a / b\n    except ZeroDivisionError:\n        return "erro"\n    else:\n        return resultado\n    finally:\n        log.append("fim")',
             test='assert dividir(10, 2) == 5\nassert dividir(1, 0) == "erro", "Divisão por zero retorna \\"erro\\""\nassert log == ["fim", "fim"], "O finally roda nas duas chamadas"\nassert "finally" in codigo, "Use finally"',
             h=["except ZeroDivisionError:", "finally: roda sempre, mesmo depois de um return"]),
        dict(t="Ordem dos argumentos", p="Crie <code>registrar(nome, *telefones, pais=\"BR\", **extras)</code> que retorna um dicionário com as chaves <code>nome</code>, <code>telefones</code> (lista), <code>pais</code> e todas as chaves de <code>extras</code>.", s="",
             sol='def registrar(nome, *telefones, pais="BR", **extras):\n    dados = {"nome": nome, "telefones": list(telefones), "pais": pais}\n    dados.update(extras)\n    return dados',
             test='assert registrar("Ana") == {"nome": "Ana", "telefones": [], "pais": "BR"}\nassert registrar("Leo", "1111", "2222", pais="PT", idade=30) == {"nome": "Leo", "telefones": ["1111", "2222"], "pais": "PT", "idade": 30}',
             h=["Ordem: normais, *args, com padrão, **kwargs", "dados.update(extras) junta os extras no dicionário"]),
        dict(t="Validar entrada com raise", p="Crie <code>sacar(saldo, valor)</code> que retorna o novo saldo. Gere <code>ValueError</code> se o valor for menor ou igual a zero e gere <code>ValueError(\"Saldo insuficiente\")</code> se o valor for maior que o saldo.", s="",
             sol='def sacar(saldo, valor):\n    if valor <= 0:\n        raise ValueError("Valor inválido")\n    if valor > saldo:\n        raise ValueError("Saldo insuficiente")\n    return saldo - valor',
             test='assert sacar(100, 30) == 70\nfor args in [(100, 0), (100, -5)]:\n    try:\n        sacar(*args); assert False, "Valor <= 0 deve gerar ValueError"\n    except ValueError:\n        pass\ntry:\n    sacar(50, 80); assert False, "Saque maior que o saldo deve gerar ValueError"\nexcept ValueError as e:\n    assert "insuficiente" in str(e), "Mensagem: Saldo insuficiente"',
             h=["raise ValueError(\"mensagem\") interrompe a função", "Teste as condições antes de calcular"]),
        dict(t="Desafio: processar pedidos", p="Crie <code>processar(pedidos)</code>. Cada pedido é um texto <code>\"produto;quantidade;preço\"</code>. Retorne a tupla <code>(total, erros)</code>: a soma de quantidade × preço das linhas válidas e a lista das linhas que deram erro (formato errado ou números inválidos).", s="",
             sol='def processar(pedidos):\n    total = 0\n    erros = []\n    for linha in pedidos:\n        try:\n            produto, qtd, preco = linha.split(";")\n            total += int(qtd) * float(preco)\n        except ValueError:\n            erros.append(linha)\n    return total, erros',
             test='t, e = processar(["caneta;2;1.5", "caderno;x;10", "lapis;3;0.5", "borracha;1"])\nassert t == 4.5, "2×1.5 + 3×0.5 = 4.5"\nassert e == ["caderno;x;10", "borracha;1"], "Linhas com erro, na ordem"\nassert processar([]) == (0, []), "Lista vazia: (0, [])"',
             h=["Desempacotar com split(\";\") gera ValueError se não houver 3 partes", "Um único except ValueError trata os dois casos"]),
    ],
)
