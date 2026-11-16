TOPIC = dict(
    name="Arquivos de texto (e PDF)", short="ler e gravar dados em arquivos",
    cdesc="open, modos r/w/a, with, linhas, encoding, CSV e noções de PDF",
    map="arvore", src="Intermediário • Módulo 25",
    groups=[
        ["Abrir", [["open(caminho, modo)", "r ler, w gravar (apaga), a acrescentar"], ["encoding=\"utf-8\"", "evita problema com acentos"], ["with open(...) as f:", "fecha o arquivo sozinho"]]],
        ["Ler", [["f.read()", "tudo num texto só"], ["f.readlines()", "lista de linhas (com \\n)"], ["for linha in f:", "linha a linha, economiza memória"]]],
        ["Gravar", [["f.write(texto)", "não põe \\n sozinho"], ["modo \"a\"", "acrescenta no fim"], ["f.writelines(lista)", "várias linhas de uma vez"]]],
        ["Tratar o texto", [["strip()", "tira \\n e espaços das pontas"], ["split(\";\")", "separa as colunas"], ["csv.reader / DictReader", "lê CSV respeitando aspas"]]],
        ["PDF (no seu PC)", [["pypdf / PyPDF2", "PdfReader, PdfWriter, juntar e separar páginas"], ["extract_text()", "pegar texto de uma página"], ["tabula", "ler tabelas de PDF para o pandas"]]],
    ],
    hot=[
        "Use sempre with open(...): o arquivo é fechado mesmo se der erro.",
        "Modo \"w\" APAGA o conteúdo anterior; para acrescentar use \"a\".",
        "write não pula linha: escreva \"\\n\" no final.",
        "Cada linha lida termina com \\n; use strip() antes de comparar ou converter.",
        "Informe encoding=\"utf-8\" para não estragar acentos.",
    ],
    trap="Abrir com \"w\" para \"adicionar uma linha\" apaga o arquivo inteiro. Para adicionar, use \"a\".",
    examples=[["arquivos.py", '''with open("clientes.txt", "w", encoding="utf-8") as f:
    f.write("Ana\\n")
    f.write("Leo\\n")

with open("clientes.txt", "a", encoding="utf-8") as f:
    f.write("Bia\\n")

with open("clientes.txt", encoding="utf-8") as f:
    nomes = [linha.strip() for linha in f]
print(nomes)   # ['Ana', 'Leo', 'Bia']'''], ["pdf_no_seu_pc.py", '''# Não roda no navegador: execute no seu computador (pip install pypdf)
from pypdf import PdfReader, PdfWriter

leitor = PdfReader("relatorio.pdf")
print(leitor.pages[0].extract_text())

escritor = PdfWriter()
for pagina in leitor.pages[:2]:
    escritor.add_page(pagina)
escritor.write("duas_paginas.pdf")''']],
    ex=[
        dict(t="Ler um arquivo", p="O arquivo <code>mensagem.txt</code> já existe na pasta. Leia todo o conteúdo e guarde em <code>conteudo</code>.", s='with open("mensagem.txt", "w", encoding="utf-8") as f:\n    f.write("Olá, Python!\\nArquivos são fáceis.")',
             sol='with open("mensagem.txt", encoding="utf-8") as f:\n    conteudo = f.read()', test='assert conteudo == "Olá, Python!\\nArquivos são fáceis.", "Use f.read()"',
             h=["with open(\"mensagem.txt\", encoding=\"utf-8\") as f:", "conteudo = f.read()"]),
        dict(t="Gravar um arquivo", p="Crie o arquivo <code>saida.txt</code> com o texto de <code>texto</code>.", s='texto = "Relatório gerado pelo Python"',
             sol='with open("saida.txt", "w", encoding="utf-8") as f:\n    f.write(texto)', test='assert open("saida.txt", encoding="utf-8").read() == texto, "O arquivo deve conter exatamente o texto"',
             h=["Modo \"w\" cria/regrava o arquivo", "f.write(texto)"]),
        dict(t="Uma linha por item", p="Grave cada nome de <code>nomes</code> em uma linha do arquivo <code>nomes.txt</code>.", s='nomes = ["Ana", "Leo", "Bia"]',
             sol='with open("nomes.txt", "w", encoding="utf-8") as f:\n    for nome in nomes:\n        f.write(nome + "\\n")', test='assert open("nomes.txt", encoding="utf-8").read().splitlines() == ["Ana", "Leo", "Bia"], "Uma linha por nome"',
             h=["write não pula linha sozinho", "f.write(nome + \"\\n\")"]),
        dict(t="Acrescentar sem apagar", p="O arquivo <code>log.txt</code> já tem 2 linhas. Acrescente a linha <code>evento</code> no final <b>sem apagar</b> o que existe.", s='with open("log.txt", "w", encoding="utf-8") as f:\n    f.write("inicio\\nprocessando\\n")\nevento = "fim"',
             sol='with open("log.txt", "a", encoding="utf-8") as f:\n    f.write(evento + "\\n")', test='assert open("log.txt", encoding="utf-8").read().splitlines() == ["inicio", "processando", "fim"], "Use o modo \\"a\\" (append)"',
             h=["Modo \"a\" = append", "Não esqueça o \\n"]),
        dict(t="Linhas sem o \\n", p="Leia <code>produtos.txt</code> e guarde em <code>produtos</code> a lista de linhas <b>sem</b> o <code>\\n</code> e sem linhas vazias.", s='with open("produtos.txt", "w", encoding="utf-8") as f:\n    f.write("Café\\nPão\\n\\nLeite\\n")',
             sol='with open("produtos.txt", encoding="utf-8") as f:\n    produtos = [linha.strip() for linha in f if linha.strip()]', test='assert produtos == ["Café", "Pão", "Leite"], "Use strip() e ignore linhas vazias"',
             h=["for linha in f percorre linha a linha", "linha.strip() remove o \\n"]),
        dict(t="Somar valores do arquivo", p="<code>vendas.txt</code> tem um valor por linha. Calcule <code>total</code> (float).", s='with open("vendas.txt", "w", encoding="utf-8") as f:\n    f.write("150.50\\n200\\n99.50\\n")',
             sol='total = 0\nwith open("vendas.txt", encoding="utf-8") as f:\n    for linha in f:\n        total += float(linha)', test='assert total == 450.0, "150.50 + 200 + 99.50 = 450"',
             h=["Cada linha é texto: converta com float()", "float(\"200\\n\") funciona, o \\n é ignorado"]),
        dict(t="Separar colunas", p="<code>clientes.txt</code> tem linhas <code>nome;cidade</code>. Crie o dicionário <code>cidade_de</code> <code>{nome: cidade}</code>.", s='with open("clientes.txt", "w", encoding="utf-8") as f:\n    f.write("Ana;Recife\\nLeo;Olinda\\nBia;Caruaru\\n")',
             sol='cidade_de = {}\nwith open("clientes.txt", encoding="utf-8") as f:\n    for linha in f:\n        nome, cidade = linha.strip().split(";")\n        cidade_de[nome] = cidade', test='assert cidade_de == {"Ana": "Recife", "Leo": "Olinda", "Bia": "Caruaru"}, "Faça strip() antes do split(\\";\\")"',
             h=["linha.strip().split(\";\")", "Desempacote: nome, cidade = ..."]),
        dict(t="Contar palavras", p="Leia <code>texto.txt</code> e guarde em <code>qtd_palavras</code> o número de palavras e em <code>qtd_linhas</code> o número de linhas.", s='with open("texto.txt", "w", encoding="utf-8") as f:\n    f.write("Python é uma linguagem\\nmuito usada em dados\\ne automação\\n")',
             sol='with open("texto.txt", encoding="utf-8") as f:\n    linhas = f.readlines()\nqtd_linhas = len(linhas)\nqtd_palavras = sum(len(l.split()) for l in linhas)', test='assert qtd_linhas == 3, "3 linhas"\nassert qtd_palavras == 10, "4 + 4 + 2 = 10 palavras"',
             h=["readlines() devolve a lista de linhas", "split() sem argumentos separa por espaços"]),
        dict(t="Ler CSV com csv.DictReader", p="Leia <code>notas.csv</code> com <code>csv.DictReader</code> e crie <code>aprovados</code>: lista de nomes com nota ≥ 7.", s='with open("notas.csv", "w", encoding="utf-8", newline="") as f:\n    f.write("nome,nota\\nAna,8.5\\nLeo,6.0\\nBia,7.0\\n")',
             sol='import csv\nwith open("notas.csv", encoding="utf-8", newline="") as f:\n    aprovados = [l["nome"] for l in csv.DictReader(f) if float(l["nota"]) >= 7]', test='assert aprovados == ["Ana", "Bia"], "Converta a nota com float()"\nassert "DictReader" in codigo',
             h=["Cada linha do DictReader é um dicionário", "linha[\"nota\"] é texto: use float()"]),
        dict(t="Gravar CSV", p="Grave <code>vendas</code> (lista de tuplas) em <code>vendas.csv</code> com cabeçalho <code>produto,quantidade</code>, usando <code>csv.writer</code>.", s='vendas = [("Café", 30), ("Pão", 45)]',
             sol='import csv\nwith open("vendas.csv", "w", encoding="utf-8", newline="") as f:\n    escritor = csv.writer(f)\n    escritor.writerow(["produto", "quantidade"])\n    escritor.writerows(vendas)', test='assert open("vendas.csv", encoding="utf-8").read().splitlines() == ["produto,quantidade", "Café,30", "Pão,45"]',
             h=["csv.writer(f).writerow([...])", "writerows(lista) grava várias linhas"]),
        dict(t="Copiar filtrando", p="Copie para <code>erros.txt</code> apenas as linhas de <code>sistema.log</code> que contêm <code>ERRO</code>.", s='with open("sistema.log", "w", encoding="utf-8") as f:\n    f.write("INFO inicio\\nERRO disco cheio\\nINFO ok\\nERRO timeout\\n")',
             sol='with open("sistema.log", encoding="utf-8") as origem, open("erros.txt", "w", encoding="utf-8") as destino:\n    for linha in origem:\n        if "ERRO" in linha:\n            destino.write(linha)', test='assert open("erros.txt", encoding="utf-8").read().splitlines() == ["ERRO disco cheio", "ERRO timeout"]',
             h=["Dá para abrir dois arquivos no mesmo with", "if \"ERRO\" in linha: destino.write(linha)"]),
        dict(t="Arquivo inexistente", p="Crie <code>ler_seguro(caminho)</code> que retorna o conteúdo do arquivo ou a string <code>\"arquivo não encontrado\"</code> se ele não existir.", s='with open("existe.txt", "w") as f:\n    f.write("ok")',
             sol='def ler_seguro(caminho):\n    try:\n        with open(caminho, encoding="utf-8") as f:\n            return f.read()\n    except FileNotFoundError:\n        return "arquivo não encontrado"', test='assert ler_seguro("existe.txt") == "ok"\nassert ler_seguro("nao_existe.txt") == "arquivo não encontrado", "Trate FileNotFoundError"',
             h=["Arquivo inexistente gera FileNotFoundError", "try / except FileNotFoundError"]),
        dict(t="Relatório em arquivo", p="Gere <code>relatorio.txt</code> com uma linha por vendedor no formato <code>Ana: R$ 1,500.00</code> (ordem do dicionário) e, na última linha, <code>Total: R$ 2,750.50</code>.", s='vendas = {"Ana": 1500, "Leo": 1250.5}',
             sol='with open("relatorio.txt", "w", encoding="utf-8") as f:\n    for nome, valor in vendas.items():\n        f.write(f"{nome}: R$ {valor:,.2f}\\n")\n    f.write(f"Total: R$ {sum(vendas.values()):,.2f}\\n")', test='assert open("relatorio.txt", encoding="utf-8").read().splitlines() == ["Ana: R$ 1,500.00", "Leo: R$ 1,250.50", "Total: R$ 2,750.50"]',
             h=["f-string com :,.2f", "sum(vendas.values()) para o total"]),
        dict(t="Atualizar estoque", p="<code>estoque.txt</code> tem linhas <code>produto;quantidade</code>. Subtraia as quantidades de <code>vendidos</code> (dict) e <b>regrave</b> o arquivo no mesmo formato e ordem.", s='with open("estoque.txt", "w", encoding="utf-8") as f:\n    f.write("Café;50\\nPão;30\\nLeite;20\\n")\nvendidos = {"Café": 5, "Leite": 20}',
             sol='with open("estoque.txt", encoding="utf-8") as f:\n    linhas = [l.strip().split(";") for l in f if l.strip()]\nwith open("estoque.txt", "w", encoding="utf-8") as f:\n    for produto, qtd in linhas:\n        f.write(f"{produto};{int(qtd) - vendidos.get(produto, 0)}\\n")', test='assert open("estoque.txt", encoding="utf-8").read().splitlines() == ["Café;45", "Pão;30", "Leite;0"], "Leia tudo primeiro, depois regrave"',
             h=["Leia o arquivo inteiro antes de abrir com \"w\"", "vendidos.get(produto, 0) para quem não vendeu"]),
        dict(t="Desafio: consolidar arquivos", p="Os arquivos <code>loja_a.txt</code>, <code>loja_b.txt</code> e <code>loja_c.txt</code> têm linhas <code>produto;valor</code>. Crie <code>consolidado.csv</code> com cabeçalho <code>produto,total</code> e o total de cada produto somando as três lojas, em ordem alfabética, com 2 casas decimais.", s='dados = {"loja_a.txt": "Café;10.5\\nPão;3\\n", "loja_b.txt": "Pão;2.5\\nLeite;7\\n", "loja_c.txt": "Café;4.5\\nLeite;1\\n"}\nfor nome, conteudo in dados.items():\n    with open(nome, "w", encoding="utf-8") as f:\n        f.write(conteudo)',
             sol='totais = {}\nfor nome in ["loja_a.txt", "loja_b.txt", "loja_c.txt"]:\n    with open(nome, encoding="utf-8") as f:\n        for linha in f:\n            produto, valor = linha.strip().split(";")\n            totais[produto] = totais.get(produto, 0) + float(valor)\nwith open("consolidado.csv", "w", encoding="utf-8") as f:\n    f.write("produto,total\\n")\n    for produto in sorted(totais):\n        f.write(f"{produto},{totais[produto]:.2f}\\n")',
             test='assert open("consolidado.csv", encoding="utf-8").read().splitlines() == ["produto,total", "Café,15.00", "Leite,8.00", "Pão,5.50"]',
             h=["Acumule num dicionário com get(produto, 0)", "sorted(dicionario) ordena as chaves"]),
    ],
)
