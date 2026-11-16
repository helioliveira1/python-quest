S = "import numpy as np\n"
TOPIC = dict(
    name="NumPy", short="a base da análise de dados",
    cdesc="arrays, operações vetorizadas, estatísticas, filtros com where e reshape com eixos",
    map="radial", src="Intermediário • Módulo 21", pkgs=["numpy"],
    groups=[
        ["Arrays", [["np.array([...])", "sequência de valores do MESMO tipo"], ["Lista × array", "lista + 1 dá erro; array + 1 soma em todos"], ["dtype", "int64, float64, <U32 (texto)"]]],
        ["Índices e fatias", [["a[0], a[-1]", "como nas listas"], ["a[1:4]", "fim não incluso"], ["a[a > 10]", "filtro booleano"]]],
        ["Funções", [["sum, max, min, mean", "a.sum() ou np.sum(a)"], ["argmax / argmin", "POSIÇÃO do maior/menor"], ["sort, dot", "ordenar; produto escalar (unidades × preços)"]]],
        ["Estatística e aleatórios", [["percentile, var, std", "posição relativa e dispersão"], ["rng = np.random.default_rng(42)", "gerador com semente"], ["rng.integers / rng.normal", "números aleatórios"]]],
        ["Condições", [["np.where(cond)", "índices que atendem"], ["np.where(cond, a, b)", "escolhe valor por condição"], ["& e |", "and/or entre condições (use parênteses)"]]],
        ["Forma", [["reshape(2, 7)", "muda a forma (mesma quantidade)"], ["ndim / shape", "dimensões e tamanho"], ["axis=0 / axis=1", "ao longo das linhas / colunas"]]],
    ],
    hot=[
        "Operações com array são aplicadas em TODOS os elementos de uma vez (vetorização).",
        "argmax devolve a POSIÇÃO do maior valor, não o valor.",
        "Condições combinadas usam & e | com parênteses: (a > 3) & (a < 8).",
        "axis=0 percorre as linhas (resultado por coluna); axis=1 percorre as colunas (resultado por linha).",
        "default_rng(seed) torna os aleatórios reprodutíveis para toda a equipe.",
    ],
    trap="Usar and/or com arrays dá erro (\"truth value is ambiguous\"). Use & e | com cada condição entre parênteses.",
    examples=[["numpy_basico.py", '''import numpy as np

precos = np.array([10.0, 25.5, 8.0, 40.0])
print(precos * 1.1)          # aumenta 10% em todos
print(precos.max(), precos.argmax())

unidades = np.array([3, 1, 5, 2])
print(np.dot(unidades, precos))   # total vendido

print(precos[precos > 9])         # filtro booleano'''], ["numpy_analise.py", '''rng = np.random.default_rng(seed=42)
vendas = rng.integers(100, 500, size=14)

semanas = vendas.reshape(2, 7)    # 2 semanas × 7 dias
print(semanas.sum(axis=1))        # total por semana
print(semanas.sum(axis=0))        # total por dia da semana

salarios = np.array([2500, 3800, 4200, 6000])
print(np.where(salarios > salarios.mean(), "acima", "abaixo"))
print(salarios[(salarios >= 3000) & (salarios <= 4500)])''']],
    ex=[
        dict(t="Primeiro array", p="Crie o array <code>precos</code> a partir da lista <code>lista_precos</code> e guarde em <code>tipo</code> o <code>dtype</code> como texto (<code>str(precos.dtype)</code>).", s=S + "lista_precos = [10.0, 25.5, 8.0]",
             sol="precos = np.array(lista_precos)\ntipo = str(precos.dtype)", test='assert isinstance(precos, np.ndarray), "Use np.array(...)"\nassert precos.tolist() == [10.0, 25.5, 8.0]\nassert tipo == "float64", "dtype de números decimais: float64"',
             h=["np.array(lista)", "O tipo interno fica em .dtype"]),
        dict(t="Reajuste vetorizado", p="Aumente todos os <code>precos</code> em 10% (sem <code>for</code>) e guarde em <code>reajustados</code>, arredondados para 2 casas com <code>np.round</code>.", s=S + "precos = np.array([10.0, 25.5, 8.0, 40.0])",
             sol="reajustados = np.round(precos * 1.1, 2)", test='assert reajustados.tolist() == [11.0, 28.05, 8.8, 44.0], "Multiplique o array por 1.1"\nassert "for " not in codigo, "Sem for: a operação é aplicada no array inteiro"',
             h=["array * 1.1 multiplica todos os elementos", "np.round(array, 2)"]),
        dict(t="Fatias", p="De <code>vendas</code>, guarde em <code>primeiros</code> os 3 primeiros valores e em <code>ultimo</code> o último (índice negativo).", s=S + "vendas = np.array([120, 340, 90, 410, 275, 180])",
             sol="primeiros = vendas[:3]\nultimo = vendas[-1]", test='assert primeiros.tolist() == [120, 340, 90]\nassert ultimo == 180, "Índice -1 é o último"',
             h=["Fatia: vendas[:3]", "Último: vendas[-1]"]),
        dict(t="Mais caro e mais barato", p="Guarde em <code>maior</code> e <code>menor</code> o maior e o menor preço, e em <code>pos_maior</code> a <b>posição</b> do maior.", s=S + "precos = np.array([35.9, 12.5, 89.0, 47.3])",
             sol="maior = precos.max()\nmenor = precos.min()\npos_maior = precos.argmax()", test='assert (maior, menor) == (89.0, 12.5)\nassert pos_maior == 2, "argmax devolve a posição: 2"',
             h=["max() e min()", "argmax() devolve o índice do maior"]),
        dict(t="Total com dot", p="Calcule o faturamento <code>total</code> multiplicando <code>unidades</code> por <code>precos</code> e somando, usando <code>np.dot</code>.", s=S + "unidades = np.array([3, 1, 5, 2])\nprecos = np.array([10.0, 25.5, 8.0, 40.0])",
             sol="total = np.dot(unidades, precos)", test='assert total == 175.5, "3×10 + 1×25.5 + 5×8 + 2×40 = 175.5"\nassert "dot" in codigo, "Use np.dot"',
             h=["np.dot(a, b) = soma dos produtos", "É o mesmo que (a * b).sum()"]),
        dict(t="Filtro booleano", p="Crie <code>acima</code> com os salários maiores que a média de <code>salarios</code> e <code>qtd_acima</code> com quantos são.", s=S + "salarios = np.array([2500, 3800, 4200, 6000, 3100])",
             sol="acima = salarios[salarios > salarios.mean()]\nqtd_acima = len(acima)", test='assert acima.tolist() == [4200, 6000], "Média = 3920: acima ficam 4200 e 6000"\nassert qtd_acima == 2',
             h=["salarios > salarios.mean() gera True/False", "Use isso entre colchetes para filtrar"]),
        dict(t="Faixa salarial", p="Guarde em <code>faixa</code> os salários entre 3000 e 4500 (inclusive) usando <code>&amp;</code>.", s=S + "salarios = np.array([2500, 3800, 4200, 6000, 3100, 4500])",
             sol="faixa = salarios[(salarios >= 3000) & (salarios <= 4500)]", test='assert faixa.tolist() == [3800, 4200, 3100, 4500]\nassert "&" in codigo, "Combine as condições com &"',
             h=["Cada condição entre parênteses", "(cond1) & (cond2)"]),
        dict(t="np.where com dois retornos", p="Crie <code>situacao</code> com <code>\"acima\"</code> para salários maiores que a média e <code>\"abaixo\"</code> para os demais, usando <code>np.where</code>.", s=S + "salarios = np.array([2500, 3800, 4200, 6000])",
             sol='situacao = np.where(salarios > salarios.mean(), "acima", "abaixo")', test='assert situacao.tolist() == ["abaixo", "abaixo", "acima", "acima"], "Média = 4125"\nassert "where" in codigo',
             h=["np.where(condição, valor_se_verdadeiro, valor_se_falso)", "A condição usa salarios.mean()"]),
        dict(t="Aleatórios com semente", p="Crie <code>rng = np.random.default_rng(seed=42)</code> e gere <code>vendas</code> com 30 inteiros entre 100 e 500 (<code>rng.integers(100, 500, size=30)</code>). Depois guarde em <code>dia_top</code> o <b>dia</b> (posição + 1) com a maior venda.", s=S,
             sol="rng = np.random.default_rng(seed=42)\nvendas = rng.integers(100, 500, size=30)\ndia_top = vendas.argmax() + 1",
             test='_v = np.random.default_rng(seed=42).integers(100, 500, size=30)\nassert vendas.tolist() == _v.tolist(), "Use default_rng(seed=42) e integers(100, 500, size=30)"\nassert dia_top == _v.argmax() + 1, "Dia = posição do maior + 1"',
             h=["argmax() dá a posição (começa em 0)", "Some 1 para virar \"dia\""]),
        dict(t="Medidas estatísticas", p="Calcule a <code>media</code>, a <code>mediana</code> (percentil 50) e a <code>variancia</code> de <code>notas</code> com NumPy.", s=S + "notas = np.array([6.0, 7.5, 8.0, 9.0, 4.5])",
             sol="media = np.mean(notas)\nmediana = np.percentile(notas, 50)\nvariancia = np.var(notas)", test='assert media == 7.0 and mediana == 7.5\nassert abs(variancia - 2.5) < 1e-9, "np.var dá 2.5"\nassert "percentile" in codigo, "Use np.percentile(notas, 50) para a mediana"',
             h=["np.mean, np.percentile(x, 50), np.var", "O percentil 50 é a mediana"]),
        dict(t="Reshape em semanas", p="<code>vendas</code> tem 14 dias. Reorganize em 2 linhas × 7 colunas em <code>semanas</code> e guarde em <code>total_semana</code> o total de cada semana (soma ao longo do eixo 1).", s=S + "vendas = np.array([10, 20, 15, 30, 25, 40, 35, 12, 18, 22, 28, 30, 45, 50])",
             sol="semanas = vendas.reshape(2, 7)\ntotal_semana = semanas.sum(axis=1)", test='assert semanas.shape == (2, 7), "Use reshape(2, 7)"\nassert total_semana.tolist() == [175, 205], "Soma por linha: axis=1"',
             h=["vendas.reshape(2, 7)", "sum(axis=1) soma cada linha"]),
        dict(t="Total por dia da semana", p="Com <code>semanas</code> (2×7), guarde em <code>por_dia</code> a soma de cada coluna (dia da semana) e em <code>melhor_dia</code> o nome do dia com maior soma, usando a lista <code>dias</code>.", s=S + "semanas = np.array([[10, 20, 15, 30, 25, 40, 35], [12, 18, 22, 28, 30, 45, 50]])\ndias = ['seg', 'ter', 'qua', 'qui', 'sex', 'sab', 'dom']",
             sol="por_dia = semanas.sum(axis=0)\nmelhor_dia = dias[por_dia.argmax()]", test='assert por_dia.tolist() == [22, 38, 37, 58, 55, 85, 85], "Soma por coluna: axis=0"\nassert melhor_dia == "sab", "Empate: argmax pega a primeira ocorrência (sab)"',
             h=["axis=0 soma ao longo das linhas (resultado por coluna)", "dias[posição]"]),
        dict(t="Ajuste salarial condicional", p="Dê 10% de aumento só para quem ganha menos de 3000 e guarde o resultado em <code>novos</code> (use <code>np.where</code>; arredonde para 2 casas).", s=S + "salarios = np.array([2500.0, 3800.0, 2900.0, 6000.0])",
             sol="novos = np.round(np.where(salarios < 3000, salarios * 1.1, salarios), 2)", test='assert novos.tolist() == [2750.0, 3800.0, 3190.0, 6000.0]\nassert salarios.tolist() == [2500.0, 3800.0, 2900.0, 6000.0], "Não altere o array original"',
             h=["np.where(condição, salarios * 1.1, salarios)", "np.round(..., 2)"]),
        dict(t="Normalizar notas", p="Converta <code>notas</code> para a escala 0–1 com a fórmula (x − mín) ÷ (máx − mín) e guarde em <code>normal</code>, com 3 casas.", s=S + "notas = np.array([4.0, 6.0, 8.0, 10.0, 7.0])",
             sol="normal = np.round((notas - notas.min()) / (notas.max() - notas.min()), 3)", test='assert normal.tolist() == [0.0, 0.333, 0.667, 1.0, 0.5]',
             h=["Operações entre array e número valem para todos", "(notas - notas.min()) / (notas.max() - notas.min())"]),
        dict(t="Desafio: matriz de vendas", p="<code>vendas</code> tem 4 lojas (linhas) × 3 meses (colunas). Crie: <code>total_loja</code> (soma por loja), <code>media_mes</code> (média de cada mês, 1 casa), <code>loja_top</code> (índice da loja com maior total) e <code>meses_meta</code> (quantas células ≥ <code>meta</code>).", s=S + "vendas = np.array([[120, 150, 130], [90, 110, 95], [200, 180, 210], [60, 75, 80]])\nmeta = 120",
             sol="total_loja = vendas.sum(axis=1)\nmedia_mes = np.round(vendas.mean(axis=0), 1)\nloja_top = int(total_loja.argmax())\nmeses_meta = int((vendas >= meta).sum())",
             test='assert total_loja.tolist() == [400, 295, 590, 215]\nassert media_mes.tolist() == [117.5, 128.8, 128.8]\nassert loja_top == 2\nassert meses_meta == 6, "6 células com venda >= 120"\nassert rodar(meta=200)["meses_meta"] == 2, "Use a variável meta"',
             h=["Por loja = linhas → axis=1; por mês = colunas → axis=0", "(vendas >= meta).sum() conta os True"]),
    ],
)
