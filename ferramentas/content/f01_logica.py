TOPIC = dict(
    name="Lógica e primeiros programas", short="o computador faz exatamente o que você manda",
    cdesc="sequência de comandos, print, ordem de execução e indicadores formatados",
    map="fluxo", src="Fundamentos • Módulos 3, 4 e 5",
    groups=[
        ["Lógica de programação", [["Passo a passo", "descreva em português o que faria manualmente"], ["Seja explícito", "se você não mandar, o computador não faz"], ["De cima para baixo", "o Python lê e executa linha por linha"]]],
        ["Primeiros comandos", [["print()", "mostra textos e números na tela"], ["Textos entre aspas", "\"texto\" ou 'texto'; números sem aspas"], ["Comentários", "# o Python ignora a linha"]]],
        ["Variáveis", [["Caixa com nome", "faturamento = 1000 (= significa \"recebe\")"], ["Ordem importa", "usar antes de criar gera NameError"], ["Recalcular", "mudar o custo NÃO atualiza o lucro sozinho"]]],
        ["1º projeto (automação)", [["Bibliotecas", "pyautogui, pandas: código pronto de outras pessoas"], ["Indicadores", "faturamento = soma; quantidade = soma"], ["Relatório", "texto com f-string e números formatados"]]],
        ["Formatação", [["f\"{x}\"", "coloca o valor da variável no texto"], ["{x:,.2f}", "milhar com vírgula e 2 casas"], [".format()", "\"{} e {}\".format(a, b): a ordem importa"]]],
    ],
    hot=[
        "O Python executa de cima para baixo: uma variável precisa existir ANTES de ser usada.",
        "Mudar uma variável depois não recalcula as contas feitas antes; refaça o cálculo.",
        "Números com casas decimais usam ponto (1.5), não vírgula.",
        "f\"R$ {valor:,.2f}\" formata dinheiro com separador de milhar e 2 casas.",
        "Não formate os números cedo demais: calcule primeiro, formate só para mostrar.",
    ],
    trap="lucro = faturamento - custo; custo = 50 → o lucro NÃO muda. A conta foi feita com o custo antigo.",
    examples=[["primeiro_programa.py", '''print("Meu primeiro código")
print(10 + 5)

faturamento = 1500
custo = 1200
lucro = faturamento - custo
print("Lucro:", lucro)

custo = 1000              # mudou o custo...
lucro = faturamento - custo   # ...então recalcule!
print(f"Novo lucro: {lucro}")'''], ["indicadores.py", '''faturamento = 1234567.891
qtde_produtos = 8540

texto = f"""Prezados,
Faturamento: R$ {faturamento:,.2f}
Quantidade de produtos: {qtde_produtos:,}"""
print(texto)

# .format() — a ordem dos valores importa
print("Faturamento de {} e custo de {}".format(1000, 600))''']],
    ex=[
        dict(t="Olá, Python", p="Imprima exatamente a frase <code>Meu primeiro código</code>.", s="",
             sol='print("Meu primeiro código")', test='assert saida.strip() == "Meu primeiro código", "A saída deve ser exatamente: Meu primeiro código"',
             h=["Use print(\"...\")", "Textos ficam entre aspas"]),
        dict(t="Duas linhas", p="Imprima o nome da empresa (<code>empresa</code>) em uma linha e, na linha de baixo, o ano (<code>ano</code>). Use dois <code>print</code>.",
             s='empresa = "Hashtag"\nano = 2026', sol='print(empresa)\nprint(ano)',
             test='assert saida.split("\\n")[:2] == ["Hashtag", "2026"], "Primeira linha: empresa; segunda: ano"\nassert rodar(empresa="Loja", ano=1999)["saida"].split("\\n")[:2] == ["Loja", "1999"], "Use as variáveis, não textos fixos"',
             h=["Cada print gera uma linha", "print(empresa) e depois print(ano)"]),
        dict(t="Calcular o lucro", p="Crie <code>lucro</code> como <code>faturamento - custo</code>.", s="faturamento = 100\ncusto = 80",
             sol="lucro = faturamento - custo", test='assert lucro == 20, "100 - 80 = 20"\nassert rodar(faturamento=500, custo=120)["lucro"] == 380, "Use as variáveis, não números fixos"',
             h=["O sinal = guarda o resultado à direita na variável da esquerda", "lucro = faturamento - custo"]),
        dict(t="Ordem de execução", p="O código abaixo dá <b>NameError</b> porque usa <code>nome</code> antes de criar. Reescreva na ordem certa para imprimir <code>João</code>:<pre class='code'>print(nome)\nnome = \"João\"</pre>", s="",
             sol='nome = "João"\nprint(nome)', test='assert saida.strip() == "João", "Crie a variável antes de imprimir"',
             h=["O Python lê de cima para baixo", "Primeiro nome = \"João\", depois print(nome)"]),
        dict(t="Recalcule!", p="O <code>custo</code> mudou para <code>novo_custo</code> depois do primeiro cálculo. Atualize <code>custo</code> e <b>recalcule</b> <code>lucro</code>.",
             s="faturamento = 100\ncusto = 80\nlucro = faturamento - custo\nnovo_custo = 50",
             sol="custo = novo_custo\nlucro = faturamento - custo",
             test='assert custo == 50, "custo deve receber novo_custo"\nassert lucro == 50, "Recalcule o lucro depois de mudar o custo: 100 - 50 = 50"\nassert rodar(novo_custo=30)["lucro"] == 70, "Use novo_custo"',
             h=["Mudar o custo não atualiza o lucro sozinho", "Escreva de novo: lucro = faturamento - custo"]),
        dict(t="Indicadores do relatório", p="Calcule <code>faturamento</code> (soma de <code>venda1</code>, <code>venda2</code> e <code>venda3</code>) e <code>ticket_medio</code> (faturamento dividido pela quantidade de vendas, 3).",
             s="venda1 = 1500.0\nvenda2 = 820.5\nvenda3 = 679.5",
             sol="faturamento = venda1 + venda2 + venda3\nticket_medio = faturamento / 3",
             test='assert faturamento == 3000.0, "1500 + 820.5 + 679.5 = 3000"\nassert ticket_medio == 1000.0, "3000 / 3 = 1000"\nr = rodar(venda1=10.0, venda2=20.0, venda3=30.0)\nassert (r["faturamento"], r["ticket_medio"]) == (60.0, 20.0), "Use as variáveis"',
             h=["Some as três vendas", "Ticket médio = faturamento / 3"]),
        dict(t="Dinheiro formatado", p="Imprima o faturamento no formato <code>Faturamento: R$ 1,234,567.89</code> (separador de milhar e 2 casas), usando f-string.",
             s="faturamento = 1234567.891", sol='print(f"Faturamento: R$ {faturamento:,.2f}")',
             test='assert saida.strip() == "Faturamento: R$ 1,234,567.89", "Use {faturamento:,.2f}"\nassert rodar(faturamento=1500)["saida"].strip() == "Faturamento: R$ 1,500.00", "Use a variável"',
             h=["Dentro das chaves: {variavel:formato}", ":,.2f = vírgula de milhar + 2 casas decimais"]),
        dict(t="Usando .format()", p="Usando o método <code>.format()</code>, imprima <code>O faturamento foi de 1000 e o custo de 600</code> com as variáveis <code>faturamento</code> e <code>custo</code>.",
             s="faturamento = 1000\ncusto = 600", sol='print("O faturamento foi de {} e o custo de {}".format(faturamento, custo))',
             test='assert saida.strip() == "O faturamento foi de 1000 e o custo de 600", "Confira o texto e a ordem dos valores"\nassert ".format(" in codigo, "Use o método .format()"\nassert rodar(faturamento=5, custo=2)["saida"].strip() == "O faturamento foi de 5 e o custo de 2", "A ordem no format importa"',
             h=["Cada {} recebe um valor do .format(...)", "A ordem dos argumentos define a ordem no texto"]),
        dict(t="Corrigir tipos", p="<code>\"Total: \" + total</code> gera TypeError, porque soma texto com número. Crie <code>mensagem</code> com o texto <code>Total: 250</code> convertendo <code>total</code> com <code>str()</code>.",
             s="total = 250", sol='mensagem = "Total: " + str(total)',
             test='assert mensagem == "Total: 250", "mensagem deve ser \\"Total: 250\\""\nassert rodar(total=7)["mensagem"] == "Total: 7", "Use a variável total"',
             h=["Só dá para concatenar str com str", "str(total) converte o número em texto"]),
        dict(t="Quantidade com milhar", p="Imprima <code>Quantidade de produtos: 8,540</code> usando f-string e o formato de milhar (sem casas decimais).",
             s="qtde_produtos = 8540", sol='print(f"Quantidade de produtos: {qtde_produtos:,}")',
             test='assert saida.strip() == "Quantidade de produtos: 8,540", "Use {qtde_produtos:,}"\nassert rodar(qtde_produtos=1234567)["saida"].strip() == "Quantidade de produtos: 1,234,567", "Use a variável"',
             h=["Só a vírgula, sem .2f", "{qtde_produtos:,}"]),
        dict(t="Corpo do e-mail", p="Monte a variável <code>texto</code> (string de várias linhas com <code>\"\"\"</code>) exatamente assim:<pre class='code'>Prezados,\nFaturamento: R$ 3,000.00\nQuantidade: 1,250</pre>Use <code>faturamento</code> e <code>quantidade</code>.",
             s="faturamento = 3000\nquantidade = 1250",
             sol='texto = f"""Prezados,\nFaturamento: R$ {faturamento:,.2f}\nQuantidade: {quantidade:,}"""',
             test='assert texto.strip() == "Prezados,\\nFaturamento: R$ 3,000.00\\nQuantidade: 1,250", "Confira as 3 linhas do texto"\nassert rodar(faturamento=10, quantidade=2)["texto"].strip() == "Prezados,\\nFaturamento: R$ 10.00\\nQuantidade: 2", "Use as variáveis"',
             h=["f-string também funciona com três aspas: f\"\"\"...\"\"\"", "Cada quebra de linha dentro das aspas vira uma linha do texto"]),
        dict(t="Margem de lucro", p="Calcule <code>margem</code> = lucro ÷ faturamento × 100 (lucro = faturamento − custo) e imprima <code>Margem: 37.5%</code> com 1 casa decimal.",
             s="faturamento = 800\ncusto = 500",
             sol='lucro = faturamento - custo\nmargem = lucro / faturamento * 100\nprint(f"Margem: {margem:.1f}%")',
             test='assert abs(margem - 37.5) < 1e-9, "(800 - 500) / 800 × 100 = 37.5"\nassert saida.strip() == "Margem: 37.5%", "Formate com :.1f e o símbolo %"\nassert rodar(faturamento=200, custo=150)["saida"].strip() == "Margem: 25.0%", "Use as variáveis"',
             h=["Calcule o lucro antes da margem", "{margem:.1f} dá 1 casa decimal"]),
        dict(t="Troco em notas", p="Para pagar <code>valor</code> reais, calcule quantas notas de 100 (<code>notas100</code>), de 10 (<code>notas10</code>) e quanto sobra em moedas de 1 (<code>moedas1</code>). Use <code>//</code> e <code>%</code>.",
             s="valor = 387", sol="notas100 = valor // 100\nresto = valor % 100\nnotas10 = resto // 10\nmoedas1 = resto % 10",
             test='assert (notas100, notas10, moedas1) == (3, 8, 7), "387 = 3×100 + 8×10 + 7"\nr = rodar(valor=1009)\nassert (r["notas100"], r["notas10"], r["moedas1"]) == (10, 0, 9), "Use // (divisão inteira) e % (resto)"',
             h=["valor // 100 = quantas notas de 100", "O resto (valor % 100) segue para as notas de 10"]),
        dict(t="Relatório em sequência", p="Escreva o passo a passo em código: (1) <code>faturamento</code> = preço × quantidade; (2) <code>imposto</code> = 10% do faturamento; (3) <code>liquido</code> = faturamento − imposto; (4) imprima <code>Líquido: R$ 1,350.00</code>.",
             s="preco = 30\nquantidade = 50",
             sol='faturamento = preco * quantidade\nimposto = faturamento * 0.10\nliquido = faturamento - imposto\nprint(f"Líquido: R$ {liquido:,.2f}")',
             test='assert faturamento == 1500, "30 × 50 = 1500"\nassert abs(imposto - 150) < 1e-9 and abs(liquido - 1350) < 1e-9, "imposto 150 e líquido 1350"\nassert saida.strip() == "Líquido: R$ 1,350.00", "Formate com :,.2f"\nassert rodar(preco=1000, quantidade=3)["saida"].strip() == "Líquido: R$ 2,700.00", "Use as variáveis"',
             h=["Uma linha para cada passo, na ordem", "10% = * 0.10"]),
        dict(t="Desafio: segundos para horário", p="Converta <code>segundos</code> para o formato <code>HH:MM:SS</code> com 2 dígitos cada e guarde em <code>horario</code> (ex.: 3725 → <code>01:02:05</code>).",
             s="segundos = 3725",
             sol='h = segundos // 3600\nm = segundos % 3600 // 60\ns = segundos % 60\nhorario = f"{h:02}:{m:02}:{s:02}"',
             test='assert horario == "01:02:05", "3725 s = 01:02:05"\nassert rodar(segundos=86399)["horario"] == "23:59:59", "Use // e %"\nassert rodar(segundos=59)["horario"] == "00:00:59", "Complete com zeros à esquerda: {x:02}"',
             h=["1 hora = 3600 s; 1 minuto = 60 s", "Zero à esquerda: f\"{h:02}\""]),
    ],
)
