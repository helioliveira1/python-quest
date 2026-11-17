import sys, os; sys.path.insert(0, os.path.dirname(__file__))
from _h import E, ENT

TOPIC = dict(
    name="Ciência de dados na prática", short="números que contam histórias",
    cdesc="NumPy, pandas (limpeza, groupby, merge, pivot), estatística, gráficos com matplotlib e uma regressão linear do zero",
    map="arvore", src="Banco • Dados + Python na Prática cap. 11",
    groups=[
        ["NumPy", [["np.array", "operações vetorizadas"], ["mean, std, percentile", "estatística rápida"], ["Máscaras", "a[a > 0]"]]],
        ["pandas: limpar", [["isna / fillna / dropna", "valores faltando"], ["drop_duplicates", "linhas repetidas"], ["astype / to_datetime", "tipos corretos"]]],
        ["pandas: analisar", [["groupby().agg()", "resumos por grupo"], ["merge", "juntar tabelas"], ["pivot_table", "tabela dinâmica"]]],
        ["Visualizar", [["plt.plot / bar / hist", "linha, barras, distribuição"], ["Título e rótulos", "gráfico que se explica"], ["savefig", "salvar imagem"]]],
        ["Modelar", [["Correlação", "força da relação"], ["Regressão linear", "y = a·x + b"], ["Treino × teste", "avaliar com dados novos"]]],
    ],
    hot=["Explore antes de analisar: shape, head, info, describe.",
         "Operações vetorizadas (df[\"a\"] * 2) são muito mais rápidas que laços.",
         "groupby + agg resolve a maioria dos relatórios.",
         "Correlação não é causalidade."],
    trap="Esquecer de tratar valores faltando (NaN): a média ignora, mas a contagem e os modelos podem dar resultados enganosos.",
    examples=[["analise.py", '''import pandas as pd
df = pd.DataFrame({"loja": ["A", "B", "A"], "valor": [100, 50, 30]})
print(df.groupby("loja")["valor"].agg(["sum", "mean"]))'''], ["grafico.py", '''import matplotlib.pyplot as plt
meses = ["jan", "fev", "mar"]
vendas = [120, 150, 90]
plt.bar(meses, vendas, color="#1E5AA8")
plt.title("Vendas por mês")
plt.show()''']],
    ex=[
        E(0, "NumPy básico", "Com <code>np</code>, crie <code>a</code> = array de <code>notas</code> e calcule <code>media</code>, <code>desvio</code> (2 casas) e <code>acima</code> (notas acima da média, como lista).",
          'import numpy as np\na = np.array(notas)\nmedia = a.mean()\ndesvio = round(float(a.std()), 2)\nacima = a[a > media].tolist()', 'assert media == 7 and desvio == 1.41 and acima == [9, 8]', ["np.array(lista)", "Máscara: a[a > media]"], s="notas = [5, 9, 7, 6, 8]"),
        E(0, "Primeiro DataFrame", "Crie <code>df</code> a partir de <code>dados</code>, adicione a coluna <code>total = preco * qtd</code> e guarde em <code>caro</code> o nome do produto de maior total.",
          'import pandas as pd\ndf = pd.DataFrame(dados)\ndf["total"] = df["preco"] * df["qtd"]\ncaro = df.loc[df["total"].idxmax(), "produto"]', 'assert list(df["total"]) == [20, 45, 24] and caro == "pão"', ["pd.DataFrame(dict)", "idxmax devolve o índice do maior"], s='dados = {"produto": ["café", "pão", "leite"], "preco": [10, 1.5, 4], "qtd": [2, 30, 6]}'),
        E(0, "Filtrar e ordenar", "Em <code>df</code> (alunos), crie <code>aprovados</code> (nota ≥ 7, ordenado pela nota decrescente) e <code>nomes</code> (lista).",
          'aprovados = df[df["nota"] >= 7].sort_values("nota", ascending=False)\nnomes = aprovados["nome"].tolist()', 'assert nomes == ["Bia", "Ana", "Caio"]', ["df[condição]", "sort_values(..., ascending=False)"], s='import pandas as pd\ndf = pd.DataFrame({"nome": ["Ana", "Leo", "Bia", "Caio"], "nota": [8, 5, 9.5, 7]})'),
        E(1, "Limpeza de dados", "Limpe <code>df</code>: remova duplicatas, padronize <code>cidade</code> (strip + title), preencha <code>idade</code> vazia com a mediana e converta para int. Guarde em <code>limpo</code> (índice reiniciado).",
          'limpo = df.drop_duplicates().copy()\nlimpo["cidade"] = limpo["cidade"].str.strip().str.title()\nlimpo["idade"] = limpo["idade"].fillna(limpo["idade"].median()).astype(int)\nlimpo = limpo.reset_index(drop=True)', 'assert limpo["cidade"].tolist() == ["Recife", "Olinda", "Recife"] and limpo.index.tolist() == [0, 1, 2]\nassert limpo["idade"].tolist() == [30, 25, 27] and str(limpo["idade"].dtype).startswith("int")', ["drop_duplicates()", "fillna(mediana)"], s='import pandas as pd\ndf = pd.DataFrame({"nome": ["Ana", "Leo", "Ana", "Bia"], "cidade": [" recife", "OLINDA ", " recife", "Recife"], "idade": [30, 25, 30, None]})'),
        E(1, "groupby e agg", "Agrupe <code>vendas</code> por <code>regiao</code> e crie <code>resumo</code> com colunas <code>total</code> (soma), <code>media</code> (média, 1 casa) e <code>pedidos</code> (contagem).",
          'resumo = vendas.groupby("regiao")["valor"].agg(total="sum", media="mean", pedidos="count").round(1)', 'assert resumo.loc["NE", "total"] == 450 and resumo.loc["NE", "media"] == 150 and resumo.loc["S", "pedidos"] == 2 and resumo.loc["S", "media"] == 62.5', ["groupby(\"regiao\")[\"valor\"]", "agg(nome=\"função\")"], s='import pandas as pd\nvendas = pd.DataFrame({"regiao": ["NE", "S", "NE", "S", "NE"], "valor": [100, 50, 200, 75, 150]})'),
        E(1, "merge", "Junte <code>pedidos</code> e <code>clientes</code> pela coluna <code>cliente_id</code> e crie <code>gasto</code>: {nome: total gasto}.",
          'import pandas as pd\nj = pedidos.merge(clientes, on="cliente_id")\ngasto = j.groupby("nome")["valor"].sum().to_dict()', 'assert gasto == {"Ana": 150, "Leo": 80}', ["merge(..., on=\"cliente_id\")", "groupby + to_dict"], s='import pandas as pd\nclientes = pd.DataFrame({"cliente_id": [1, 2], "nome": ["Ana", "Leo"]})\npedidos = pd.DataFrame({"cliente_id": [1, 2, 1], "valor": [100, 80, 50]})'),
        E(1, "Tabela dinâmica", "Com <code>pivot_table</code>, crie <code>tabela</code>: linhas = mes, colunas = produto, valores = soma de valor (vazios = 0).",
          'tabela = df.pivot_table(index="mes", columns="produto", values="valor", aggfunc="sum", fill_value=0)', 'assert tabela.loc["jan", "café"] == 30 and tabela.loc["fev", "pão"] == 0 and tabela.loc["fev", "café"] == 15', ["index, columns, values", "fill_value=0"], s='import pandas as pd\ndf = pd.DataFrame({"mes": ["jan", "jan", "fev", "jan"], "produto": ["café", "pão", "café", "café"], "valor": [10, 5, 15, 20]})'),
        E(1, "Gráfico de barras", "Faça um gráfico de barras de <code>vendas</code> por mês com título <code>Vendas por mês</code> e rótulo do eixo y <code>R$</code>.",
          'import matplotlib.pyplot as plt\nplt.bar(list(vendas), list(vendas.values()), color="#1E5AA8")\nplt.title("Vendas por mês")\nplt.ylabel("R$")\nplt.show()', 'import matplotlib.pyplot as _p\nax = _p.gcf().axes[0]\nassert ax.get_title() == "Vendas por mês" and ax.get_ylabel() == "R$" and len(ax.patches) == 3', ["plt.bar(x, y)", "plt.title / plt.ylabel"], s='vendas = {"jan": 120, "fev": 150, "mar": 90}'),
        E(2, "Séries temporais", "Converta <code>data</code> para datetime, agrupe por mês (<code>resample(\"MS\")</code>) e crie <code>mensal</code> (lista de somas) e <code>crescimento</code> (variação % do último mês sobre o anterior, 1 casa).",
          'import pandas as pd\ndf["data"] = pd.to_datetime(df["data"], format="%d/%m/%Y")\ns = df.set_index("data")["valor"].resample("MS").sum()\nmensal = s.tolist()\ncrescimento = round((s.iloc[-1] / s.iloc[-2] - 1) * 100, 1)', 'assert mensal == [150, 200, 300] and crescimento == 50.0', ["to_datetime com format", "set_index + resample"], s='import pandas as pd\ndf = pd.DataFrame({"data": ["05/01/2026", "20/01/2026", "03/02/2026", "10/03/2026", "28/03/2026"], "valor": [100, 50, 200, 120, 180]})'),
        E(2, "Outliers pelo IQR", "Encontre em <code>outliers</code> (lista ordenada) os valores de <code>salarios</code> fora de [Q1 − 1,5·IQR, Q3 + 1,5·IQR].",
          'import numpy as np\na = np.array(salarios)\nq1, q3 = np.percentile(a, [25, 75])\niqr = q3 - q1\noutliers = sorted(a[(a < q1 - 1.5 * iqr) | (a > q3 + 1.5 * iqr)].tolist())', 'assert outliers == [500, 30000]', ["np.percentile(a, [25, 75])", "Combine máscaras com |"], s="salarios = [3000, 3200, 2800, 3500, 30000, 3100, 2900, 500, 3300]"),
        E(2, "Regressão linear do zero", "Ajuste <code>y = a·x + b</code> por mínimos quadrados com NumPy (sem bibliotecas de ML). Calcule <code>a</code>, <code>b</code> (2 casas), <code>r2</code> (2 casas) e <code>previsao</code> para x = 10 (1 casa).",
          'import numpy as np\nx, y = np.array(xs, dtype=float), np.array(ys, dtype=float)\na = round(float(((x - x.mean()) * (y - y.mean())).sum() / ((x - x.mean()) ** 2).sum()), 2)\nb = round(float(y.mean() - a * x.mean()), 2)\npred = a * x + b\nr2 = round(float(1 - ((y - pred) ** 2).sum() / ((y - y.mean()) ** 2).sum()), 2)\nprevisao = round(a * 10 + b, 1)', 'assert (a, b) == (1.97, 1.12) and r2 == 1.0 and previsao == 20.8', ["a = Σ(x−x̄)(y−ȳ) / Σ(x−x̄)²", "b = ȳ − a·x̄"], s="xs = [1, 2, 3, 4, 5, 6]\nys = [3.1, 5.0, 7.0, 9.1, 11.0, 12.9]"),
        E(2, "Relatório completo", "Para <code>df</code> (vendedor, produto, valor): crie <code>ranking</code> (vendedores por total, decrescente), <code>campeao_por_produto</code> ({produto: vendedor que mais vendeu}) e <code>participacao</code> ({vendedor: % do total, 1 casa}).",
          'tot = df.groupby("vendedor")["valor"].sum().sort_values(ascending=False)\nranking = tot.index.tolist()\ng = df.groupby(["produto", "vendedor"])["valor"].sum().reset_index()\ncampeao_por_produto = {p: s.loc[s["valor"].idxmax(), "vendedor"] for p, s in g.groupby("produto")}\nparticipacao = (tot / tot.sum() * 100).round(1).to_dict()', 'assert ranking == ["Ana", "Leo", "Bia"]\nassert campeao_por_produto == {"mouse": "Leo", "notebook": "Ana"}\nassert participacao == {"Ana": 60.0, "Leo": 30.0, "Bia": 10.0}', ["groupby com duas colunas", "idxmax dentro de cada grupo"], s='import pandas as pd\ndf = pd.DataFrame({"vendedor": ["Ana", "Leo", "Bia", "Ana", "Leo"], "produto": ["notebook", "mouse", "mouse", "notebook", "notebook"], "valor": [3000, 1000, 500, 0, 500]})'),
    ],
)
