S = "import matplotlib.pyplot as plt\n"
SM = S + "meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun']\nvendas = [120, 150, 90, 180, 210, 160]\n"
TOPIC = dict(
    name="Gráficos (Matplotlib e Seaborn)", short="dados que se explicam sozinhos",
    cdesc="linha, barra, dispersão e histograma; títulos, eixos, cores, rótulos, legendas e Seaborn",
    map="bolhas", src="Intermediário • Módulo 24", pkgs=["matplotlib"],
    groups=[
        ["Estrutura", [["fig, ax = plt.subplots()", "figura (tela) + eixo (gráfico)"], ["plt.subplots(1, 2)", "vários gráficos lado a lado"], ["plt.show() / savefig", "mostrar / salvar em arquivo"]]],
        ["Tipos", [["plot", "linha: evolução no tempo"], ["bar / barh", "barras: comparar categorias"], ["scatter / hist", "relação entre variáveis / distribuição"]]],
        ["Personalizar", [["set_title, set_xlabel, set_ylabel", "títulos e rótulos dos eixos"], ["color, linestyle, marker", "argumentos de palavra-chave"], ["set_ylim / axis", "limites dos eixos"]]],
        ["Ler melhor", [["bar_label", "valor em cima de cada barra"], ["legend(label=...)", "identifica as séries"], ["grid / spines", "linhas de grade; tirar bordas"]]],
        ["Seaborn", [["import seaborn as sns", "gráficos estatísticos prontos"], ["sns.barplot(data=df, x=, y=)", "trabalha direto com DataFrame"], ["histplot, boxplot, heatmap", "distribuição, outliers, correlação"]]],
    ],
    hot=[
        "Prefira o estilo orientado a objeto: fig, ax = plt.subplots() e depois ax.metodo().",
        "No plot(x, y) a ordem importa: primeiro o eixo X, depois o Y.",
        "Barras comparam categorias; linha mostra evolução no tempo.",
        "ax.bar_label(barras) coloca o valor em cima de cada barra.",
        "Seaborn recebe o DataFrame inteiro: data=df, x=\"coluna\", y=\"coluna\".",
    ],
    trap="Em plt.axis([xmin, xmax, ymin, ymax]) a ordem é fixa. Trocar faz o gráfico \"sumir\" da área visível.",
    examples=[["grafico_barras.py", '''import matplotlib.pyplot as plt

meses = ["Jan", "Fev", "Mar"]
vendas = [120, 150, 90]

fig, ax = plt.subplots(figsize=(6, 4))
barras = ax.bar(meses, vendas, color="#1E5AA8")
ax.bar_label(barras)
ax.set_title("Vendas por mês")
ax.set_ylabel("Unidades")
ax.spines[["top", "right"]].set_visible(False)
plt.show()'''], ["seaborn.py", '''import seaborn as sns
import pandas as pd

df = pd.DataFrame({"loja": ["A", "B", "A", "B"], "valor": [10, 12, 14, 9]})
ax = sns.barplot(data=df, x="loja", y="valor", errorbar=None)
ax.set_title("Média por loja")''']],
    ex=[
        dict(t="Primeiro gráfico de linha", p="Crie <code>fig, ax = plt.subplots()</code> e desenhe a linha de <code>vendas</code> por <code>meses</code> com <code>ax.plot</code>.<br><small class='muted'>O gráfico aparece abaixo do console quando você executa.</small>", s=SM,
             sol="fig, ax = plt.subplots()\nax.plot(meses, vendas)", test='assert len(ax.lines) == 1, "Desenhe uma linha com ax.plot"\nassert list(ax.lines[0].get_ydata()) == vendas, "No eixo Y vão as vendas: plot(meses, vendas)"',
             h=["fig, ax = plt.subplots()", "ax.plot(eixo_x, eixo_y)"]),
        dict(t="Título e rótulos", p="Faça um gráfico de linha de <code>vendas</code> por <code>meses</code> com o título <code>Vendas 2026</code>, eixo X <code>Mês</code> e eixo Y <code>Unidades</code>.", s=SM,
             sol='fig, ax = plt.subplots()\nax.plot(meses, vendas)\nax.set_title("Vendas 2026")\nax.set_xlabel("Mês")\nax.set_ylabel("Unidades")',
             test='assert ax.get_title() == "Vendas 2026"\nassert (ax.get_xlabel(), ax.get_ylabel()) == ("Mês", "Unidades"), "Use set_xlabel e set_ylabel"',
             h=["ax.set_title(\"...\")", "ax.set_xlabel / ax.set_ylabel"]),
        dict(t="Barras", p="Faça um gráfico de <b>barras</b> de <code>vendas</code> por <code>meses</code> com a cor <code>#1E5AA8</code>.", s=SM,
             sol='fig, ax = plt.subplots()\nax.bar(meses, vendas, color="#1E5AA8")',
             test='import matplotlib.colors as _mc\nassert len(ax.patches) == 6, "Use ax.bar: uma barra por mês"\nassert [p.get_height() for p in ax.patches] == vendas\nassert _mc.to_hex(ax.patches[0].get_facecolor()).lower() == "#1e5aa8", "Use color=\\"#1E5AA8\\""',
             h=["ax.bar(x, y)", "Cor por palavra-chave: color=\"#1E5AA8\""]),
        dict(t="Barras horizontais", p="Faça um gráfico de barras <b>horizontais</b> (<code>barh</code>) de <code>vendas</code> por <code>produtos</code>.", s=S + "produtos = ['Café', 'Pão', 'Leite']\nvendas = [320, 210, 180]",
             sol="fig, ax = plt.subplots()\nax.barh(produtos, vendas)", test='assert [round(p.get_width()) for p in ax.patches] == vendas, "Em barh o comprimento é a largura (width)"',
             h=["ax.barh(categorias, valores)", "No barh as categorias ficam no eixo Y"]),
        dict(t="Salvar em arquivo", p="Crie um gráfico de linha de <code>vendas</code> por <code>meses</code> e salve como <code>grafico.png</code> com <code>fig.savefig</code>.", s=SM,
             sol='fig, ax = plt.subplots()\nax.plot(meses, vendas)\nfig.savefig("grafico.png")', test='import os\nassert os.path.exists("grafico.png") and os.path.getsize("grafico.png") > 1000, "Use fig.savefig(\\"grafico.png\\")"',
             h=["fig.savefig(\"nome.png\")", "Salve depois de desenhar"]),
        dict(t="Valores nas barras", p="Faça as barras de <code>vendas</code> por <code>meses</code> e coloque o valor em cima de cada barra com <code>ax.bar_label</code>.", s=SM,
             sol="fig, ax = plt.subplots()\nbarras = ax.bar(meses, vendas)\nax.bar_label(barras)", test='assert len(ax.patches) == 6, "Desenhe as barras"\nrotulos = [t.get_text() for t in ax.texts]\nassert rotulos == [str(v) for v in vendas], "Use ax.bar_label(barras)"',
             h=["Guarde o retorno: barras = ax.bar(...)", "ax.bar_label(barras)"]),
        dict(t="Duas séries com legenda", p="No mesmo eixo, desenhe <code>vendas_2025</code> e <code>vendas_2026</code> (por <code>meses</code>) com <code>label=\"2025\"</code> e <code>label=\"2026\"</code>, e mostre a legenda.", s=S + "meses = ['Jan', 'Fev', 'Mar']\nvendas_2025 = [100, 120, 90]\nvendas_2026 = [130, 125, 140]",
             sol='fig, ax = plt.subplots()\nax.plot(meses, vendas_2025, label="2025")\nax.plot(meses, vendas_2026, label="2026")\nax.legend()',
             test='assert len(ax.lines) == 2, "Duas chamadas de ax.plot"\nleg = ax.get_legend()\nassert leg is not None, "Chame ax.legend()"\nassert [t.get_text() for t in leg.get_texts()] == ["2025", "2026"], "Use label=\\"2025\\" e label=\\"2026\\""',
             h=["Cada plot recebe label=\"...\"", "ax.legend() mostra as legendas"]),
        dict(t="Limites do eixo", p="Gráfico de linha de <code>vendas</code> por <code>meses</code> com o eixo Y começando em 0 e indo até o maior valor + 50.", s=SM,
             sol="fig, ax = plt.subplots()\nax.plot(meses, vendas)\nax.set_ylim(0, max(vendas) + 50)", test='assert ax.get_ylim() == (0, 260), "Y de 0 até max(vendas) + 50 = 260"\nassert rodar(vendas=[1, 2, 3, 4, 5, 6])["ax"].get_ylim() == (0, 56), "Use max(vendas)"',
             h=["ax.set_ylim(minimo, maximo)", "max(vendas) + 50"]),
        dict(t="Dispersão", p="Faça um gráfico de dispersão (<code>scatter</code>) de <code>preco</code> (X) por <code>vendidos</code> (Y), com pontos vermelhos (<code>color=\"red\"</code>).", s=S + "preco = [10, 15, 20, 25, 30]\nvendidos = [200, 170, 120, 90, 40]",
             sol='fig, ax = plt.subplots()\nax.scatter(preco, vendidos, color="red")', test='import numpy as _np\npts = ax.collections[0].get_offsets()\nassert _np.array(pts).tolist() == [[10, 200], [15, 170], [20, 120], [25, 90], [30, 40]], "scatter(preco, vendidos)"\nassert tuple(ax.collections[0].get_facecolor()[0][:3]) == (1.0, 0.0, 0.0), "Pontos vermelhos: color=\\"red\\""',
             h=["ax.scatter(x, y)", "color=\"red\""]),
        dict(t="Histograma", p="Faça o histograma de <code>idades</code> com 5 faixas (<code>bins=5</code>) e guarde as contagens em <code>contagens</code> (o 1º valor retornado por <code>ax.hist</code>).", s=S + "idades = [18, 22, 25, 25, 31, 33, 35, 41, 44, 52, 58, 60]",
             sol="fig, ax = plt.subplots()\ncontagens, faixas, _ = ax.hist(idades, bins=5)", test='assert list(contagens) == [4, 2, 2, 1, 3], "Use bins=5"\nassert len(ax.patches) == 5',
             h=["ax.hist(dados, bins=5)", "Ele retorna (contagens, limites, barras)"]),
        dict(t="Dois gráficos lado a lado", p="Crie <code>fig, (ax1, ax2) = plt.subplots(1, 2)</code>: em <code>ax1</code> barras de <code>vendas</code> e em <code>ax2</code> linha de <code>vendas</code>, ambos por <code>meses</code>. Título de <code>ax1</code>: <code>Barras</code>; de <code>ax2</code>: <code>Linha</code>.", s=SM,
             sol='fig, (ax1, ax2) = plt.subplots(1, 2)\nax1.bar(meses, vendas)\nax1.set_title("Barras")\nax2.plot(meses, vendas)\nax2.set_title("Linha")',
             test='assert len(fig.axes) == 2, "plt.subplots(1, 2)"\nassert len(ax1.patches) == 6 and len(ax2.lines) == 1\nassert (ax1.get_title(), ax2.get_title()) == ("Barras", "Linha")',
             h=["subplots(1, 2) = 1 linha, 2 colunas", "Cada eixo tem seus próprios métodos"]),
        dict(t="Destacar o maior", p="Faça barras de <code>vendas</code> por <code>meses</code> em cinza (<code>#A39E93</code>), exceto a maior, que deve ficar azul (<code>#1E5AA8</code>). Monte a lista <code>cores</code> e passe em <code>color=cores</code>.", s=SM,
             sol='cores = ["#1E5AA8" if v == max(vendas) else "#A39E93" for v in vendas]\nfig, ax = plt.subplots()\nax.bar(meses, vendas, color=cores)',
             test='import matplotlib.colors as _mc\nc = [_mc.to_hex(p.get_facecolor()).upper() for p in ax.patches]\nassert c == ["#A39E93"] * 4 + ["#1E5AA8", "#A39E93"], "Só a maior (Mai) em azul"\nr = rodar(vendas=[9, 1, 1, 1, 1, 1])\nassert _mc.to_hex(r["ax"].patches[0].get_facecolor()).upper() == "#1E5AA8", "Calcule a partir de vendas"',
             h=["Monte a lista de cores com if/else", "color aceita uma lista, uma cor por barra"]),
        dict(t="Gráfico a partir do pandas", p="Agrupe <code>df</code> por <code>loja</code>, some <code>valor</code> e faça barras com o resultado (lojas no X). Título: <code>Total por loja</code>.", s=S + "import pandas as pd\ndf = pd.DataFrame({'loja': ['A', 'B', 'A', 'C', 'B'], 'valor': [100, 80, 50, 120, 40]})",
             sol='total = df.groupby("loja")["valor"].sum()\nfig, ax = plt.subplots()\nax.bar(total.index, total.values)\nax.set_title("Total por loja")',
             test='assert [p.get_height() for p in ax.patches] == [150, 120, 120], "A=150, B=120, C=120"\nassert ax.get_title() == "Total por loja"',
             h=["df.groupby(\"loja\")[\"valor\"].sum()", "ax.bar(total.index, total.values)"]),
        dict(t="Barras com Seaborn", p="Com Seaborn, faça <code>ax = sns.barplot(data=df, x=\"loja\", y=\"valor\", errorbar=None, estimator=\"sum\")</code> e título <code>Vendas por loja</code>.<br><small class='muted'>Na 1ª vez o Seaborn é baixado (alguns segundos).</small>", s=S + "import pandas as pd\nimport seaborn as sns\ndf = pd.DataFrame({'loja': ['A', 'B', 'A', 'C', 'B'], 'valor': [100, 80, 50, 120, 40]})",
             sol='ax = sns.barplot(data=df, x="loja", y="valor", errorbar=None, estimator="sum")\nax.set_title("Vendas por loja")',
             test='assert [round(p.get_height()) for p in ax.patches] == [150, 120, 120], "Some por loja com estimator=\\"sum\\""\nassert ax.get_title() == "Vendas por loja"',
             h=["sns.barplot(data=df, x=..., y=...)", "estimator=\"sum\" soma em vez de tirar a média"]),
        dict(t="Desafio: painel de vendas", p="Crie <code>fig, axs = plt.subplots(2, 1)</code>. Em <code>axs[0]</code>: linha de <code>vendas</code> por <code>meses</code> com marcadores <code>\"o\"</code> e a média como linha horizontal tracejada (<code>axhline</code>, <code>linestyle=\"--\"</code>). Em <code>axs[1]</code>: barras do crescimento mês a mês (<code>vendas[i] - vendas[i-1]</code>, a partir de Fev), verde se ≥ 0 e vermelho se &lt; 0.", s=SM,
             sol='media = sum(vendas) / len(vendas)\ncresc = [vendas[i] - vendas[i - 1] for i in range(1, len(vendas))]\nfig, axs = plt.subplots(2, 1)\naxs[0].plot(meses, vendas, marker="o")\naxs[0].axhline(media, linestyle="--")\naxs[1].bar(meses[1:], cresc, color=["green" if c >= 0 else "red" for c in cresc])',
             test='import matplotlib.colors as _mc\nl = axs[0].lines\nassert len(l) == 2, "Uma linha de vendas + a linha da média"\nassert l[0].get_marker() == "o", "marker=\\"o\\""\nassert l[1].get_linestyle() == "--" and list(l[1].get_ydata()) == [sum(vendas) / len(vendas)] * 2, "axhline(media, linestyle=\\"--\\")"\nassert [p.get_height() for p in axs[1].patches] == [30, -60, 90, 30, -50], "Crescimento a partir de Fev"\nassert [_mc.to_hex(p.get_facecolor()) for p in axs[1].patches] == ["#008000", "#ff0000", "#008000", "#008000", "#ff0000"], "Verde se >= 0, vermelho se < 0"',
             h=["axs[0].axhline(valor, linestyle=\"--\")", "Lista de cores com list comprehension"]),
    ],
)
