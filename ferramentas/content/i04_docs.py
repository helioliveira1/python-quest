TOPIC = dict(
    name="Documentação, datas e APIs", short="aprender qualquer biblioteca sozinho",
    cdesc="ler documentação, datetime, conversão de datas no pandas, merge e respostas JSON de APIs",
    map="fluxo", src="Intermediário • Módulo 23",
    groups=[
        ["Como ler documentação", [["Pesquisar", "\"nome_da_biblioteca python\" no Google / PyPI"], ["Getting Started", "Quickstart / User Guide primeiro"], ["Testar o exemplo", "copie, rode e adapte aos seus dados"]]],
        ["Dentro do Python", [["help(obj)", "mostra a documentação"], ["dir(obj)", "lista métodos e atributos"], ["obj.__doc__", "a docstring em texto"]]],
        ["datetime", [["from datetime import datetime", "importa só a classe"], ["datetime.strptime(txt, fmt)", "texto → data"], ["strftime(fmt) / timedelta", "data → texto; somar/subtrair dias"]]],
        ["Códigos de formato", [["%d %m %Y", "dia, mês, ano com 4 dígitos"], ["%H:%M:%S", "hora, minuto, segundo"], ["%A %B", "nome do dia / do mês"]]],
        ["Pandas na documentação", [["df.dtypes", "tipo de cada coluna"], ["pd.to_datetime(col, format=...)", "converte texto em data"], ["merge(left_on=, right_on=)", "juntar tabelas com colunas de nomes diferentes"]]],
        ["APIs", [["requests.get(url)", "faz a requisição (precisa de internet)"], ["Parâmetros na URL", "?function=...&symbol=...&apikey=..."], ["resposta.json()", "vira dicionário/lista Python"]]],
    ],
    hot=[
        "Comece pelo Getting Started/Quickstart; teste o exemplo antes de ler tudo.",
        "strptime converte TEXTO em data; strftime converte DATA em texto.",
        "Subtrair duas datas gera um timedelta; use .days para os dias.",
        "Sem format, o pandas pode trocar dia e mês: informe format=\"%d/%m/%Y\".",
        "Chaves de API são segredo: use variáveis de ambiente, nunca deixe no código.",
    ],
    trap="%m é mês e %M é minuto. Trocar os dois gera datas erradas sem nenhum erro aparente.",
    examples=[["datas.py", '''from datetime import datetime, timedelta

pagamento = datetime.strptime("15/03/2026", "%d/%m/%Y")
hoje = datetime(2026, 4, 2)
atraso = (hoje - pagamento).days          # 18
vencimento = pagamento + timedelta(days=30)
print(vencimento.strftime("%d/%m/%Y"))    # 14/04/2026'''], ["pandas_e_api.py", '''import pandas as pd, json

tabela["Data Pagamento"] = pd.to_datetime(tabela["Data Pagamento"], format="%d/%m/%Y")
completa = tabela.merge(emails, left_on="Cliente", right_on="Nome")

# no seu PC: resposta = requests.get(url).json()
resposta = json.loads(texto_da_api)
for mes, dados in resposta["Monthly Adjusted Time Series"].items():
    print(mes, dados["4. close"])''']],
    ex=[
        dict(t="Ler a docstring", p="Guarde em <code>doc</code> a documentação (docstring) da função <code>len</code>, usando o atributo <code>__doc__</code>.", s="",
             sol="doc = len.__doc__", test='assert doc == len.__doc__ and "number of items" in doc, "Use len.__doc__"',
             h=["Toda função documentada tem __doc__", "doc = len.__doc__"]),
        dict(t="Métodos disponíveis", p="Usando <code>dir(str)</code>, crie a lista <code>metodos_is</code> com os métodos de texto que começam com <code>is</code> (ex.: <code>isdigit</code>).", s="",
             sol='metodos_is = [m for m in dir(str) if m.startswith("is")]', test='assert metodos_is == [m for m in dir(str) if m.startswith("is")] and "isdigit" in metodos_is, "Filtre dir(str) pelos que começam com is"',
             h=["dir(str) lista nomes", "startswith(\"is\")"]),
        dict(t="Criar uma data", p="Importe com <code>from datetime import datetime</code> e crie <code>natal</code> com a data 25/12/2026.", s="",
             sol="from datetime import datetime\nnatal = datetime(2026, 12, 25)", test='import datetime as _dt\nassert isinstance(natal, _dt.date) and (natal.year, natal.month, natal.day) == (2026, 12, 25), "datetime(ano, mês, dia)"',
             h=["datetime(ano, mês, dia)", "A ordem é ano, mês, dia"]),
        dict(t="Texto para data", p="Converta <code>texto</code> (formato dia/mês/ano) em data com <code>datetime.strptime</code> e guarde em <code>data</code>.", s='from datetime import datetime\ntexto = "15/03/2026"',
             sol='data = datetime.strptime(texto, "%d/%m/%Y")', test='assert (data.year, data.month, data.day) == (2026, 3, 15), "Formato: %d/%m/%Y"\nd = rodar(texto="01/12/2025")["data"]\nassert (d.month, d.day) == (12, 1), "Use a variável texto"',
             h=["strptime = string parse time", "\"%d/%m/%Y\""]),
        dict(t="Data para texto", p="Formate <code>data</code> como <code>2026-03-15 às 09:05</code> com <code>strftime</code> e guarde em <code>texto</code>.", s="from datetime import datetime\ndata = datetime(2026, 3, 15, 9, 5)",
             sol='texto = data.strftime("%Y-%m-%d às %H:%M")', test='assert texto == "2026-03-15 às 09:05", "Use %Y-%m-%d às %H:%M"',
             h=["strftime = string format time", "%H hora, %M minuto (M maiúsculo!)"]),
        dict(t="Dias em atraso", p="Calcule <code>atraso</code> (em dias, inteiro) entre <code>pagamento</code> e <code>hoje</code>.", s="from datetime import datetime\npagamento = datetime(2026, 3, 15)\nhoje = datetime(2026, 4, 2)",
             sol="atraso = (hoje - pagamento).days", test='assert atraso == 18, "De 15/03 a 02/04 = 18 dias"\nassert rodar(hoje=datetime(2026, 3, 20))["atraso"] == 5, "Use as variáveis"',
             h=["Datas podem ser subtraídas", "O resultado (timedelta) tem .days"]),
        dict(t="Vencimento com timedelta", p="Crie <code>vencimentos</code>: lista de textos <code>dd/mm/aaaa</code> com 3 parcelas a cada 30 dias, começando 30 dias após <code>compra</code>.", s="from datetime import datetime\ncompra = datetime(2026, 1, 10)",
             sol='from datetime import timedelta\nvencimentos = [(compra + timedelta(days=30 * i)).strftime("%d/%m/%Y") for i in range(1, 4)]',
             test='assert vencimentos == ["09/02/2026", "11/03/2026", "10/04/2026"], "30, 60 e 90 dias depois da compra"',
             h=["from datetime import timedelta", "compra + timedelta(days=30 * i)"]),
        dict(t="Tipos das colunas", p="Guarde em <code>tipos</code> o resultado de <code>tabela.dtypes</code> e em <code>texto_data</code> se a coluna <code>Data Pagamento</code> está como texto (<code>True</code> se o dtype for <code>object</code>).", s='import pandas as pd\ntabela = pd.DataFrame({"Cliente": ["Ana", "Leo"], "Data Pagamento": ["15/03/2026", "02/04/2026"]})',
             sol='tipos = tabela.dtypes\ntexto_data = tabela["Data Pagamento"].dtype == object', test='assert list(tipos.index) == ["Cliente", "Data Pagamento"], "Use tabela.dtypes"\nassert texto_data == True, "A coluna veio como texto (object)"',
             h=["df.dtypes mostra o tipo de cada coluna", "Compare tabela[\"Data Pagamento\"].dtype == object"]),
        dict(t="pd.to_datetime com format", p="Converta a coluna <code>Data Pagamento</code> em data usando <code>pd.to_datetime</code> com <code>format=\"%d/%m/%Y\"</code> (a mesma coluna recebe o resultado).", s='import pandas as pd\ntabela = pd.DataFrame({"Cliente": ["Ana", "Leo", "Bia"], "Data Pagamento": ["05/03/2026", "12/01/2026", "01/02/2026"]})',
             sol='tabela["Data Pagamento"] = pd.to_datetime(tabela["Data Pagamento"], format="%d/%m/%Y")',
             test='assert str(tabela["Data Pagamento"].dtype).startswith("datetime64"), "A coluna deve virar data"\nassert tabela["Data Pagamento"].dt.month.tolist() == [3, 1, 2], "Dia/mês trocados? Use format=\\"%d/%m/%Y\\""',
             h=["pd.to_datetime(coluna, format=...)", "Atribua de volta: tabela[\"col\"] = ..."]),
        dict(t="Merge com nomes diferentes", p="Junte <code>tabela</code> (coluna <code>Cliente</code>) com <code>emails</code> (coluna <code>Nome</code>) em <code>completa</code>, usando <code>left_on</code> e <code>right_on</code>.", s='import pandas as pd\ntabela = pd.DataFrame({"Cliente": ["Ana", "Leo", "Bia"], "Valor": [100, 250, 80]})\nemails = pd.DataFrame({"Nome": ["Bia", "Ana", "Leo"], "Email": ["bia@x.com", "ana@x.com", "leo@x.com"]})',
             sol='completa = tabela.merge(emails, left_on="Cliente", right_on="Nome")', test='assert len(completa) == 3 and "Email" in completa.columns, "Use merge(..., left_on=\\"Cliente\\", right_on=\\"Nome\\")"\nassert completa.set_index("Cliente").loc["Leo", "Email"] == "leo@x.com", "Cada cliente com seu e-mail"',
             h=["df.merge(outro, left_on=\"col_da_esquerda\", right_on=\"col_da_direita\")", "A ordem das linhas segue a tabela da esquerda"]),
        dict(t="Ler a resposta de uma API", p="<code>texto_api</code> tem a resposta (JSON) de uma API de cotações. Converta com <code>json.loads</code> e guarde em <code>fechamentos</code> o dicionário <code>{mês: fechamento (float)}</code> a partir de <code>\"Monthly Adjusted Time Series\"</code> e da chave <code>\"4. close\"</code>.",
             s='texto_api = \'{"Meta Data": {"2. Symbol": "IBM"}, "Monthly Adjusted Time Series": {"2026-03-31": {"1. open": "180.1", "4. close": "185.2"}, "2026-02-28": {"1. open": "170.0", "4. close": "179.9"}}}\'',
             sol='import json\ndados = json.loads(texto_api)\nfechamentos = {mes: float(v["4. close"]) for mes, v in dados["Monthly Adjusted Time Series"].items()}',
             test='assert fechamentos == {"2026-03-31": 185.2, "2026-02-28": 179.9}, "Percorra a série mensal e converta \\"4. close\\" para float"',
             h=["json.loads(texto) devolve um dicionário", "Percorra dados[\"Monthly Adjusted Time Series\"].items()"]),
        dict(t="Montar a URL da API", p="Use <code>urllib.parse.urlencode</code> para montar <code>url</code> = <code>base</code> + <code>\"?\"</code> + parâmetros <code>function=TIME_SERIES_MONTHLY_ADJUSTED</code>, <code>symbol=simbolo</code> e <code>apikey=chave</code>. A chave vem de <code>os.environ[\"API_KEY\"]</code>.", s='import os\nos.environ["API_KEY"] = "demo123"\nbase = "https://www.alphavantage.co/query"\nsimbolo = "IBM"',
             sol='from urllib.parse import urlencode\nchave = os.environ["API_KEY"]\nparametros = {"function": "TIME_SERIES_MONTHLY_ADJUSTED", "symbol": simbolo, "apikey": chave}\nurl = base + "?" + urlencode(parametros)',
             test='assert url == "https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY_ADJUSTED&symbol=IBM&apikey=demo123", "Confira a ordem: function, symbol, apikey"\nassert "demo123" not in codigo, "Não escreva a chave no código: leia de os.environ"\nassert rodar(simbolo="PETR4.SA")["url"].endswith("symbol=PETR4.SA&apikey=demo123")',
             h=["urlencode(dicionario) gera a=1&b=2", "chave = os.environ[\"API_KEY\"]"]),
        dict(t="Dia da semana", p="Para cada data em <code>datas</code> (texto dd/mm/aaaa), descubra o dia da semana (0 = segunda … 6 = domingo, com <code>.weekday()</code>) e crie <code>uteis</code> só com as datas que caem de segunda a sexta (mantendo o texto).", s='datas = ["06/04/2026", "11/04/2026", "12/04/2026", "15/04/2026"]',
             sol='from datetime import datetime\nuteis = [d for d in datas if datetime.strptime(d, "%d/%m/%Y").weekday() < 5]',
             test='assert uteis == ["06/04/2026", "15/04/2026"], "11/04 é sábado e 12/04 é domingo"',
             h=["weekday(): segunda = 0, sábado = 5, domingo = 6", "Mantenha as datas com weekday() < 5"]),
        dict(t="Cobranças em atraso", p="Em <code>tabela</code>, converta <code>Vencimento</code> para data (formato dd/mm/aaaa), crie a coluna <code>Dias Atraso</code> = (<code>hoje</code> − vencimento) em dias e guarde em <code>atrasados</code> só as linhas com atraso &gt; 0.", s='import pandas as pd\nfrom datetime import datetime\nhoje = datetime(2026, 4, 10)\ntabela = pd.DataFrame({"Cliente": ["Ana", "Leo", "Bia"], "Vencimento": ["01/04/2026", "20/04/2026", "05/03/2026"]})',
             sol='tabela["Vencimento"] = pd.to_datetime(tabela["Vencimento"], format="%d/%m/%Y")\ntabela["Dias Atraso"] = (hoje - tabela["Vencimento"]).dt.days\natrasados = tabela[tabela["Dias Atraso"] > 0]',
             test='assert tabela["Dias Atraso"].tolist() == [9, -10, 36], "hoje - vencimento, em dias"\nassert atrasados["Cliente"].tolist() == ["Ana", "Bia"], "Filtre Dias Atraso > 0"',
             h=["Subtrair datas numa coluna gera timedelta: use .dt.days", "Filtro: tabela[tabela[\"Dias Atraso\"] > 0]"]),
        dict(t="Desafio: resumo da API", p="<code>texto_api</code> tem cotações diárias. Crie <code>resumo</code> com: <code>maior</code> (maior fechamento), <code>data_maior</code> (data do maior, em <code>dd/mm/aaaa</code>) e <code>variacao</code> (% do primeiro para o último dia em ordem de data, 2 casas).",
             s='texto_api = \'{"Time Series (Daily)": {"2026-04-03": {"4. close": "112.0"}, "2026-04-01": {"4. close": "100.0"}, "2026-04-02": {"4. close": "118.5"}}}\'',
             sol='import json\nfrom datetime import datetime\nserie = json.loads(texto_api)["Time Series (Daily)"]\nprecos = {d: float(v["4. close"]) for d, v in serie.items()}\ndatas = sorted(precos)\ndata_max = max(precos, key=precos.get)\nresumo = {\n    "maior": precos[data_max],\n    "data_maior": datetime.strptime(data_max, "%Y-%m-%d").strftime("%d/%m/%Y"),\n    "variacao": round((precos[datas[-1]] / precos[datas[0]] - 1) * 100, 2),\n}',
             test='assert resumo == {"maior": 118.5, "data_maior": "02/04/2026", "variacao": 12.0}, "Ordene as datas (aaaa-mm-dd ordena como texto) antes da variação"',
             h=["Datas no formato aaaa-mm-dd podem ser ordenadas com sorted()", "max(dicionario, key=dicionario.get) devolve a chave do maior valor"]),
    ],
)
