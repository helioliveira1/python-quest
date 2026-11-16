HTML = '''from bs4 import BeautifulSoup
html = """
<html><head><title>Livraria Exemplo</title></head>
<body>
  <h1 id="titulo">Mais vendidos</h1>
  <ul id="categorias"><li><a href="/ficcao">Ficção</a></li><li><a href="/tecnologia">Tecnologia</a></li><li><a href="https://outro.site/promo">Promoções</a></li></ul>
  <div class="livro" data-isbn="111">
    <h2 class="nome">Python para Dados</h2><span class="autor">Ana Lima</span>
    <p class="preco">R$ 89,90</p><p class="avaliacao">4.5</p>
  </div>
  <div class="livro destaque" data-isbn="222">
    <h2 class="nome">SQL na Prática</h2><span class="autor">Leo Rocha</span>
    <p class="preco">R$ 59,90</p><p class="avaliacao">4.8</p>
  </div>
  <div class="livro" data-isbn="333">
    <h2 class="nome">Lógica de Programação</h2><span class="autor">Bia Melo</span>
    <p class="preco">R$ 39,50</p>
  </div>
  <table id="vendas">
    <tr><th>Mês</th><th>Unidades</th></tr>
    <tr><td>Jan</td><td>120</td></tr><tr><td>Fev</td><td>95</td></tr><tr><td>Mar</td><td>143</td></tr>
  </table>
</body></html>"""
'''
SOUP = HTML + 'site = BeautifulSoup(html, "html.parser")\n'
TOPIC = dict(
    name="Web Scraping (BeautifulSoup)", short="extrair dados de páginas",
    cdesc="ler o HTML, encontrar tags por nome, classe e id, navegar na árvore e tratar dados faltantes",
    map="radial", src="Intermediário • Módulo 30", pkgs=["beautifulsoup4"],
    groups=[
        ["Fluxo", [["requests.get(url).text", "baixa o HTML (no seu PC)"], ["BeautifulSoup(html, \"html.parser\")", "transforma em árvore navegável"], ["Extrair e salvar", "listas, dicionários, pandas, CSV"]]],
        ["Encontrar", [["find(tag, class_=...)", "o 1º que atende (ou None)"], ["find_all(...)", "lista com todos"], ["select(\"css\")", "seletor CSS: \".livro .nome\""]]],
        ["Ler", [[".text / get_text(strip=True)", "texto da tag"], ["tag[\"href\"] / tag.get(\"href\")", "atributos"], ["attrs", "dicionário de atributos"]]],
        ["Navegar", [["parent / parents", "subir na árvore"], ["contents / children", "filhos diretos"], ["find_next / next_sibling", "andar para os lados"]]],
        ["Regras e cuidados", [["robots.txt e termos", "respeite o site"], ["Tags faltantes", "find devolve None: trate antes de usar .text"], ["Site dinâmico", "conteúdo por JavaScript → Selenium"]]],
    ],
    hot=[
        "class é palavra reservada: no find use class_=\"nome\".",
        "find devolve UM elemento (ou None); find_all devolve uma lista.",
        "get_text(strip=True) já tira espaços e quebras de linha.",
        "Antes de usar .text, confira se o find não devolveu None.",
        "Se o dado aparece só depois do JavaScript, o requests não vê: use Selenium.",
    ],
    trap="site.find(\"p\", class_=\"avaliacao\").text quebra (AttributeError: 'NoneType') quando o livro não tem avaliação. Teste se é None primeiro.",
    examples=[["raspagem.py", '''import requests
from bs4 import BeautifulSoup

resposta = requests.get("https://site-exemplo.com/livros")
site = BeautifulSoup(resposta.text, "html.parser")

for livro in site.find_all("div", class_="livro"):
    nome = livro.find("h2", class_="nome").get_text(strip=True)
    preco = livro.find("p", class_="preco").get_text(strip=True)
    print(nome, preco)'''], ["navegacao.py", '''titulo = site.find(id="titulo").text
links = [a["href"] for a in site.find_all("a")]
nomes = [h.text for h in site.select("div.livro h2.nome")]

nota = site.find("p", class_="avaliacao")
valor = float(nota.text) if nota else None    # trata o dado faltante''']],
    ex=[
        dict(t="Criar a sopa", p="A variável <code>html</code> tem o código da página. Crie <code>site = BeautifulSoup(html, \"html.parser\")</code> e guarde o texto do <code>&lt;title&gt;</code> em <code>titulo</code>.<br><small class='muted'>No seu PC o HTML viria de <code>requests.get(url).text</code>.</small>", s=HTML,
             sol='site = BeautifulSoup(html, "html.parser")\ntitulo = site.title.text', test='assert titulo == "Livraria Exemplo"',
             h=["BeautifulSoup(html, \"html.parser\")", "site.title.text"]),
        dict(t="Achar pelo id", p="Guarde em <code>cabecalho</code> o texto do elemento de id <code>titulo</code>.", s=SOUP,
             sol='cabecalho = site.find(id="titulo").text', test='assert cabecalho == "Mais vendidos"',
             h=["site.find(id=\"...\")", ".text pega o texto"]),
        dict(t="Todos os nomes", p="Crie <code>nomes</code> com o texto de todos os <code>h2</code> de classe <code>nome</code>.", s=SOUP,
             sol='nomes = [h.text for h in site.find_all("h2", class_="nome")]', test='assert nomes == ["Python para Dados", "SQL na Prática", "Lógica de Programação"]',
             h=["find_all(\"h2\", class_=\"nome\")", "class_ com underline"]),
        dict(t="Links da página", p="Crie <code>links</code> com o atributo <code>href</code> de todos os <code>&lt;a&gt;</code>.", s=SOUP,
             sol='links = [a["href"] for a in site.find_all("a")]', test='assert links == ["/ficcao", "/tecnologia", "https://outro.site/promo"]',
             h=["Atributo: tag[\"href\"] ou tag.get(\"href\")", "Percorra find_all(\"a\")"]),
        dict(t="Seletor CSS", p="Use <code>site.select</code> para pegar o nome do(s) livro(s) com as classes <code>livro</code> e <code>destaque</code>, guardando em <code>destaques</code>.", s=SOUP,
             sol='destaques = [h.text for h in site.select("div.livro.destaque h2.nome")]', test='assert destaques == ["SQL na Prática"]\nassert "select(" in codigo',
             h=["select usa sintaxe CSS", "\"div.livro.destaque h2.nome\""]),
        dict(t="Preço como número", p="Crie <code>precos</code>: lista de floats a partir dos textos de preço (<code>R$ 89,90</code> → <code>89.9</code>).", s=SOUP,
             sol='precos = [float(p.text.replace("R$", "").strip().replace(".", "").replace(",", ".")) for p in site.find_all("p", class_="preco")]',
             test='assert precos == [89.9, 59.9, 39.5]', h=["Tire o R$ e os espaços", "Troque a vírgula decimal por ponto"]),
        dict(t="Dados de cada card", p="Para cada <code>div.livro</code>, monte um dicionário com <code>nome</code>, <code>autor</code> e <code>isbn</code> (atributo <code>data-isbn</code>) e guarde todos na lista <code>livros</code>.", s=SOUP,
             sol='livros = []\nfor card in site.find_all("div", class_="livro"):\n    livros.append({\n        "nome": card.find("h2", class_="nome").get_text(strip=True),\n        "autor": card.find("span", class_="autor").get_text(strip=True),\n        "isbn": card["data-isbn"],\n    })',
             test='assert livros[0] == {"nome": "Python para Dados", "autor": "Ana Lima", "isbn": "111"}\nassert [l["isbn"] for l in livros] == ["111", "222", "333"]',
             h=["Busque DENTRO do card: card.find(...)", "card[\"data-isbn\"]"]),
        dict(t="Dado faltante", p="Crie <code>avaliacoes</code>: dicionário <code>{nome: nota}</code> com a avaliação (float) de cada livro, ou <code>None</code> quando o livro não tiver avaliação.", s=SOUP,
             sol='avaliacoes = {}\nfor card in site.find_all("div", class_="livro"):\n    nome = card.find("h2", class_="nome").text\n    nota = card.find("p", class_="avaliacao")\n    avaliacoes[nome] = float(nota.text) if nota else None',
             test='assert avaliacoes == {"Python para Dados": 4.5, "SQL na Prática": 4.8, "Lógica de Programação": None}, "O 3º livro não tem avaliação: use None"',
             h=["find devolve None quando não acha", "float(nota.text) if nota else None"]),
        dict(t="Tabela HTML", p="Leia a tabela <code>vendas</code> e crie o dicionário <code>unidades</code> <code>{mês: int}</code>, pulando o cabeçalho.", s=SOUP,
             sol='unidades = {}\nfor linha in site.find(id="vendas").find_all("tr")[1:]:\n    mes, qtd = [td.text for td in linha.find_all("td")]\n    unidades[mes] = int(qtd)',
             test='assert unidades == {"Jan": 120, "Fev": 95, "Mar": 143}', h=["find_all(\"tr\")[1:] pula o cabeçalho", "Cada linha tem 2 <td>"]),
        dict(t="Subir na árvore (parent)", p="Encontre o <code>span</code> com o autor <code>Leo Rocha</code> (use <code>string=</code>) e, subindo com <code>.parent</code>, guarde o <code>data-isbn</code> do card em <code>isbn_leo</code>.", s=SOUP,
             sol='autor = site.find("span", string="Leo Rocha")\nisbn_leo = autor.parent["data-isbn"]', test='assert isbn_leo == "222"\nassert ".parent" in codigo',
             h=["find(\"span\", string=\"Leo Rocha\")", "O card é o pai do span: .parent"]),
        dict(t="Links internos e externos", p="Separe os links em <code>internos</code> (começam com <code>/</code>) e <code>externos</code> (começam com <code>http</code>). Monte também <code>completos</code> transformando os internos em URL completa com <code>urljoin(base, href)</code>.", s=SOUP + 'base = "https://livraria.exemplo"\n',
             sol='from urllib.parse import urljoin\nhrefs = [a["href"] for a in site.find_all("a")]\ninternos = [h for h in hrefs if h.startswith("/")]\nexternos = [h for h in hrefs if h.startswith("http")]\ncompletos = [urljoin(base, h) for h in internos]',
             test='assert internos == ["/ficcao", "/tecnologia"] and externos == ["https://outro.site/promo"]\nassert completos == ["https://livraria.exemplo/ficcao", "https://livraria.exemplo/tecnologia"]',
             h=["startswith(\"/\") e startswith(\"http\")", "from urllib.parse import urljoin"]),
        dict(t="Filtrar por preço", p="Crie <code>baratos</code> com os nomes dos livros com preço menor ou igual a <code>limite</code>.", s=SOUP + "limite = 60\n",
             sol='baratos = []\nfor card in site.select("div.livro"):\n    preco = float(card.select_one(".preco").text.replace("R$", "").strip().replace(",", "."))\n    if preco <= limite:\n        baratos.append(card.select_one(".nome").text)',
             test='assert baratos == ["SQL na Prática", "Lógica de Programação"]\nassert rodar(limite=40)["baratos"] == ["Lógica de Programação"], "Use a variável limite"',
             h=["Converta o preço em float primeiro", "select_one devolve o 1º elemento do seletor"]),
        dict(t="Para o pandas", p="Monte o DataFrame <code>df</code> com as colunas <code>nome</code>, <code>autor</code> e <code>preco</code> (float) de todos os livros, e ordene pelo preço (menor primeiro).", s=SOUP + "import pandas as pd\n",
             sol='dados = []\nfor card in site.find_all("div", class_="livro"):\n    dados.append({\n        "nome": card.find(class_="nome").text,\n        "autor": card.find(class_="autor").text,\n        "preco": float(card.find(class_="preco").text.replace("R$", "").strip().replace(",", ".")),\n    })\ndf = pd.DataFrame(dados).sort_values("preco")',
             test='assert list(df.columns) == ["nome", "autor", "preco"]\nassert df["nome"].tolist() == ["Lógica de Programação", "SQL na Prática", "Python para Dados"]\nassert df["preco"].tolist() == [39.5, 59.9, 89.9]',
             h=["Lista de dicionários → pd.DataFrame(lista)", "sort_values(\"preco\")"]),
        dict(t="Função raspadora segura", p="Crie <code>extrair(html)</code> que retorna a lista de <code>(nome, preço float)</code> dos livros. Se a página não tiver nenhum livro, retorne lista vazia; se um card não tiver preço, pule o card.", s="from bs4 import BeautifulSoup\n",
             sol='def extrair(html):\n    site = BeautifulSoup(html, "html.parser")\n    resultado = []\n    for card in site.find_all("div", class_="livro"):\n        nome = card.find(class_="nome")\n        preco = card.find(class_="preco")\n        if not nome or not preco:\n            continue\n        valor = float(preco.text.replace("R$", "").strip().replace(",", "."))\n        resultado.append((nome.get_text(strip=True), valor))\n    return resultado',
             test='h = \'<div class="livro"><h2 class="nome">A</h2><p class="preco">R$ 10,00</p></div><div class="livro"><h2 class="nome">B</h2></div>\'\nassert extrair(h) == [("A", 10.0)], "Pule o card sem preço"\nassert extrair("<p>vazio</p>") == []',
             h=["Confira se nome e preco não são None", "continue pula para o próximo card"]),
        dict(t="Desafio: relatório da vitrine", p="Gere <code>relatorio</code> (dicionário) com: <code>qtd</code> (livros), <code>preco_medio</code> (2 casas), <code>mais_caro</code> (nome), <code>melhor_avaliado</code> (nome, ignorando sem avaliação) e <code>categorias</code> (texto dos links). Grave também <code>livros.csv</code> com <code>nome,preco</code>.", s=SOUP,
             sol='import csv\nlivros = []\nfor card in site.find_all("div", class_="livro"):\n    nota = card.find(class_="avaliacao")\n    livros.append({\n        "nome": card.find(class_="nome").text,\n        "preco": float(card.find(class_="preco").text.replace("R$", "").strip().replace(",", ".")),\n        "nota": float(nota.text) if nota else None,\n    })\navaliados = [l for l in livros if l["nota"] is not None]\nrelatorio = {\n    "qtd": len(livros),\n    "preco_medio": round(sum(l["preco"] for l in livros) / len(livros), 2),\n    "mais_caro": max(livros, key=lambda l: l["preco"])["nome"],\n    "melhor_avaliado": max(avaliados, key=lambda l: l["nota"])["nome"],\n    "categorias": [a.text for a in site.select("#categorias a")],\n}\nwith open("livros.csv", "w", newline="", encoding="utf-8") as f:\n    w = csv.writer(f)\n    w.writerow(["nome", "preco"])\n    for l in livros:\n        w.writerow([l["nome"], l["preco"]])',
             test='assert relatorio == {"qtd": 3, "preco_medio": 63.1, "mais_caro": "Python para Dados", "melhor_avaliado": "SQL na Prática", "categorias": ["Ficção", "Tecnologia", "Promoções"]}\nassert open("livros.csv", encoding="utf-8").read().splitlines() == ["nome,preco", "Python para Dados,89.9", "SQL na Prática,59.9", "Lógica de Programação,39.5"]',
             h=["Monte primeiro uma lista de dicionários com tudo", "max(lista, key=lambda l: l[\"preco\"])"]),
    ],
)
