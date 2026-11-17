import sys, os; sys.path.insert(0, os.path.dirname(__file__))
from _h import E, ENT

TOPIC = dict(
    name="Algoritmos e estruturas de dados", short="pensar como programador",
    cdesc="busca, ordenação, pilha, fila, conjuntos, grafos, programação dinâmica e complexidade (Big O)",
    map="fluxo", src="Banco • Algoritmos + Python na Prática cap. 9",
    groups=[
        ["Busca", [["Linear O(n)", "olha um por um"], ["Binária O(log n)", "lista ordenada, corta pela metade"], ["Dicionário / set O(1)", "consulta direta"]]],
        ["Ordenação", [["Bubble / Selection O(n²)", "didáticos"], ["Merge / Quick O(n log n)", "dividir para conquistar"], ["sorted()", "Timsort: use no dia a dia"]]],
        ["Estruturas", [["Pilha (LIFO)", "append / pop"], ["Fila (FIFO)", "collections.deque"], ["heapq", "sempre pega o menor"]]],
        ["Grafos", [["Lista de adjacência", "dict de vizinhos"], ["BFS", "menor caminho em passos"], ["DFS", "explorar até o fim"]]],
        ["Técnicas", [["Dois ponteiros", "início e fim"], ["Janela deslizante", "subsequências"], ["Programação dinâmica", "guarda resultados parciais"]]],
    ],
    hot=["Antes de otimizar, escreva a versão simples que funciona.",
         "x in lista é O(n); x in set é O(1) em média.",
         "list.pop(0) é lento: para filas use deque.popleft().",
         "Recursão profunda estoura a pilha: prefira laço ou memoização."],
    trap="Busca binária só funciona em dados ORDENADOS; e cuidado com os limites (esq <= dir) para não entrar em laço infinito.",
    examples=[["busca_binaria.py", '''def busca(lista, alvo):
    esq, dir = 0, len(lista) - 1
    while esq <= dir:
        meio = (esq + dir) // 2
        if lista[meio] == alvo:
            return meio
        if lista[meio] < alvo:
            esq = meio + 1
        else:
            dir = meio - 1
    return -1'''], ["bfs.py", '''from collections import deque

def bfs(grafo, inicio):
    visitados, fila = [inicio], deque([inicio])
    while fila:
        v = fila.popleft()
        for viz in grafo[v]:
            if viz not in visitados:
                visitados.append(viz)
                fila.append(viz)
    return visitados''']],
    ex=[
        E(0, "Busca linear", "Crie <code>busca_linear(lista, alvo)</code> que devolve o índice da primeira ocorrência ou −1 (sem <code>index</code>).",
          'def busca_linear(lista, alvo):\n    for i, x in enumerate(lista):\n        if x == alvo:\n            return i\n    return -1', 'assert busca_linear([4, 2, 9, 2], 2) == 1 and busca_linear([], 1) == -1 and busca_linear([1], 5) == -1\nassert ".index(" not in codigo', ["enumerate", "return −1 depois do laço"]),
        E(0, "Segundo maior", "Crie <code>segundo_maior(l)</code> (valores distintos) em uma passada, sem ordenar.",
          'def segundo_maior(l):\n    p = s = float("-inf")\n    for x in l:\n        if x > p:\n            p, s = x, p\n        elif p > x > s:\n            s = x\n    return s', 'assert segundo_maior([3, 9, 7, 9, 1]) == 7 and segundo_maior([-1, -5]) == -5\nassert "sort" not in codigo', ["Guarde primeiro e segundo", "Ao achar um novo maior, o antigo vira segundo"]),
        E(0, "Pilha: parênteses", "Crie <code>balanceado(t)</code> que verifica se <code>()[]{}</code> estão corretamente abertos e fechados.",
          'def balanceado(t):\n    pares = {")": "(", "]": "[", "}": "{"}\n    pilha = []\n    for c in t:\n        if c in "([{":\n            pilha.append(c)\n        elif c in pares:\n            if not pilha or pilha.pop() != pares[c]:\n                return False\n    return not pilha', 'assert balanceado("{[()()]}") and balanceado("a(b)c") and not balanceado("([)]") and not balanceado("((") and not balanceado(")")', ["Abre → empilha; fecha → desempilha e compara", "No fim, a pilha deve estar vazia"]),
        E(0, "Fila de atendimento", "Simule com <code>deque</code>: chegam <code>clientes</code>; atenda 2 (popleft) e guarde os atendidos em <code>atendidos</code> e os que esperam em <code>restantes</code> (lista).",
          'from collections import deque\nfila = deque(clientes)\natendidos = [fila.popleft() for _ in range(2)]\nrestantes = list(fila)', 'assert atendidos == ["Ana", "Leo"] and restantes == ["Bia", "Caio"]\nassert "deque" in codigo', ["from collections import deque", "popleft() remove do início"], s='clientes = ["Ana", "Leo", "Bia", "Caio"]'),
        E(0, "Interseção rápida", "Crie <code>comuns(a, b)</code> que devolve a lista ordenada de elementos presentes nas duas listas usando conjuntos.",
          'def comuns(a, b):\n    return sorted(set(a) & set(b))', 'assert comuns([1, 2, 3, 4], [3, 4, 5, 3]) == [3, 4] and comuns([1], [2]) == []', ["set(a) & set(b)", "sorted()"]),
        E(0, "Dois números que somam", "Crie <code>dois_soma(nums, alvo)</code> que devolve os índices (i, j) de dois números que somam o alvo, em O(n) com dicionário (ou None).",
          'def dois_soma(nums, alvo):\n    vistos = {}\n    for i, x in enumerate(nums):\n        if alvo - x in vistos:\n            return (vistos[alvo - x], i)\n        vistos[x] = i\n    return None', 'assert dois_soma([2, 7, 11, 15], 9) == (0, 1) and dois_soma([3, 2, 4], 6) == (1, 2) and dois_soma([1, 2], 9) is None', ["Guarde valor → índice", "Procure o complemento alvo − x"]),
        E(1, "Busca binária iterativa", "Crie <code>busca_binaria(l, alvo)</code> que devolve (índice, passos) — passos = quantas comparações com o meio foram feitas. Índice −1 se não achar.",
          'def busca_binaria(l, alvo):\n    esq, dir, passos = 0, len(l) - 1, 0\n    while esq <= dir:\n        meio = (esq + dir) // 2\n        passos += 1\n        if l[meio] == alvo:\n            return meio, passos\n        if l[meio] < alvo:\n            esq = meio + 1\n        else:\n            dir = meio - 1\n    return -1, passos', 'l = list(range(0, 1000, 2))\nassert busca_binaria(l, 500)[0] == 250 and busca_binaria(l, 501)[0] == -1\nassert busca_binaria(l, 998)[1] <= 9', ["esq <= dir", "Conte cada iteração"]),
        E(1, "Selection sort", "Implemente <code>selection_sort(l)</code> devolvendo uma nova lista ordenada (sem sort/sorted).",
          'def selection_sort(l):\n    r = list(l)\n    for i in range(len(r)):\n        m = i\n        for j in range(i + 1, len(r)):\n            if r[j] < r[m]:\n                m = j\n        r[i], r[m] = r[m], r[i]\n    return r', 'import random as _r\nfor _ in range(20):\n    d = [_r.randint(-50, 50) for _ in range(_r.randint(0, 15))]\n    assert selection_sort(d) == sorted(d)\nassert "sort(" not in codigo.replace("selection_sort(", "")', ["Ache o menor do resto", "Troque com a posição i"]),
        E(1, "Insertion sort", "Implemente <code>insertion_sort(l)</code> (nova lista, sem sort/sorted).",
          'def insertion_sort(l):\n    r = list(l)\n    for i in range(1, len(r)):\n        x, j = r[i], i - 1\n        while j >= 0 and r[j] > x:\n            r[j + 1] = r[j]\n            j -= 1\n        r[j + 1] = x\n    return r', 'import random as _r\nfor _ in range(20):\n    d = [_r.randint(0, 99) for _ in range(_r.randint(0, 15))]\n    assert insertion_sort(d) == sorted(d)\nassert "sorted(" not in codigo', ["Pegue o elemento e desloque os maiores", "Como ordenar cartas na mão"]),
        E(1, "Merge sort", "Implemente <code>merge_sort(l)</code> recursivo (divida ao meio, ordene e intercale).",
          'def merge_sort(l):\n    if len(l) <= 1:\n        return list(l)\n    m = len(l) // 2\n    a, b = merge_sort(l[:m]), merge_sort(l[m:])\n    r, i, j = [], 0, 0\n    while i < len(a) and j < len(b):\n        if a[i] <= b[j]:\n            r.append(a[i]); i += 1\n        else:\n            r.append(b[j]); j += 1\n    return r + a[i:] + b[j:]', 'import random as _r\nfor _ in range(20):\n    d = [_r.randint(-99, 99) for _ in range(_r.randint(0, 30))]\n    assert merge_sort(d) == sorted(d)\nassert "sorted(" not in codigo and ".sort(" not in codigo', ["Caso base: 0 ou 1 elemento", "Intercale com dois índices"]),
        E(1, "Quick sort", "Implemente <code>quick_sort(l)</code> com pivô e compreensões de lista.",
          'def quick_sort(l):\n    if len(l) <= 1:\n        return list(l)\n    p = l[len(l) // 2]\n    return quick_sort([x for x in l if x < p]) + [x for x in l if x == p] + quick_sort([x for x in l if x > p])', 'import random as _r\nfor _ in range(20):\n    d = [_r.randint(0, 20) for _ in range(_r.randint(0, 30))]\n    assert quick_sort(d) == sorted(d)\nassert "sorted(" not in codigo', ["Menores + iguais + maiores", "Recursão nos dois lados"]),
        E(1, "Anagramas agrupados", "Crie <code>agrupar(palavras)</code> que devolve uma lista de grupos de anagramas (cada grupo ordenado, grupos ordenados pelo primeiro elemento).",
          'from collections import defaultdict\n\ndef agrupar(palavras):\n    g = defaultdict(list)\n    for p in palavras:\n        g["".join(sorted(p))].append(p)\n    return sorted(sorted(v) for v in g.values())', 'assert agrupar(["amor", "roma", "pato", "topa", "mora", "sol"]) == [["amor", "mora", "roma"], ["pato", "topa"], ["sol"]]', ["Chave = letras ordenadas", "defaultdict(list)"]),
        E(1, "Mais frequente", "Crie <code>top_k(lista, k)</code> que devolve os k elementos mais frequentes (empate: menor valor primeiro).",
          'from collections import Counter\n\ndef top_k(lista, k):\n    return [x for x, _ in sorted(Counter(lista).items(), key=lambda p: (-p[1], p[0]))[:k]]', 'assert top_k([3, 1, 1, 2, 2, 3, 3, 4], 2) == [3, 1] and top_k(["b", "a"], 1) == ["a"]', ["Counter conta", "Ordene por (−freq, valor)"]),
        E(1, "Janela deslizante", "Crie <code>maior_soma(l, k)</code>: a maior soma de k elementos consecutivos, em O(n).",
          'def maior_soma(l, k):\n    s = sum(l[:k])\n    m = s\n    for i in range(k, len(l)):\n        s += l[i] - l[i - k]\n        m = max(m, s)\n    return m', 'assert maior_soma([2, 1, 5, 1, 3, 2], 3) == 9 and maior_soma([-1, -2, -3], 2) == -3 and maior_soma([5], 1) == 5', ["Some a primeira janela", "Some o que entra, subtraia o que sai"]),
        E(1, "Dois ponteiros", "Crie <code>sem_repetidos(l)</code> que, numa lista ORDENADA, devolve a lista sem repetições usando dois índices (sem set).",
          'def sem_repetidos(l):\n    if not l:\n        return []\n    r = [l[0]]\n    i = 0\n    for j in range(1, len(l)):\n        if l[j] != l[i]:\n            r.append(l[j])\n            i = j\n    return r', 'assert sem_repetidos([1, 1, 2, 3, 3, 3, 7]) == [1, 2, 3, 7] and sem_repetidos([]) == []\nassert "set(" not in codigo', ["Compare com o último diferente", "Lista vazia é caso especial"]),
        E(1, "Heap: k menores", "Use <code>heapq</code> para criar <code>k_menores(l, k)</code> e simule uma fila de prioridade: <code>ordem</code> = tarefas de <code>tarefas</code> (prioridade, nome) atendidas da menor prioridade para a maior.",
          'import heapq\n\ndef k_menores(l, k):\n    return heapq.nsmallest(k, l)\n\nh = list(tarefas)\nheapq.heapify(h)\nordem = [heapq.heappop(h)[1] for _ in range(len(h))]', 'assert k_menores([9, 4, 7, 1, 8], 2) == [1, 4]\nassert ordem == ["urgente", "normal", "depois"]', ["heapq.nsmallest", "heapify + heappop"], s='tarefas = [(3, "depois"), (1, "urgente"), (2, "normal")]'),
        E(1, "BFS: menor caminho", "Crie <code>menor_caminho(grafo, ini, fim)</code> com BFS que devolve a lista de vértices do caminho com menos passos (ou None).",
          'from collections import deque\n\ndef menor_caminho(grafo, ini, fim):\n    pai = {ini: None}\n    fila = deque([ini])\n    while fila:\n        v = fila.popleft()\n        if v == fim:\n            c = []\n            while v is not None:\n                c.append(v)\n                v = pai[v]\n            return c[::-1]\n        for w in grafo.get(v, []):\n            if w not in pai:\n                pai[w] = v\n                fila.append(w)\n    return None', 'g = {"A": ["B", "C"], "B": ["D"], "C": ["D", "E"], "D": ["F"], "E": ["F"], "F": [], "X": []}\nassert menor_caminho(g, "A", "F") == ["A", "B", "D", "F"] and menor_caminho(g, "A", "X") is None and menor_caminho(g, "C", "C") == ["C"]', ["Guarde o pai de cada vértice", "Reconstrua o caminho de trás para frente"]),
        E(1, "DFS: componentes", "Crie <code>componentes(grafo)</code> (não direcionado) que devolve quantos grupos conectados existem.",
          'def componentes(grafo):\n    vistos = set()\n    n = 0\n    for v in grafo:\n        if v not in vistos:\n            n += 1\n            pilha = [v]\n            while pilha:\n                x = pilha.pop()\n                if x not in vistos:\n                    vistos.add(x)\n                    pilha.extend(grafo[x])\n    return n', 'g = {1: [2], 2: [1, 3], 3: [2], 4: [5], 5: [4], 6: []}\nassert componentes(g) == 3 and componentes({}) == 0', ["Cada DFS iniciada é um novo componente", "Pilha + set de visitados"]),
        E(2, "Moedas (programação dinâmica)", "Crie <code>min_moedas(moedas, valor)</code>: o menor número de moedas para formar o valor (−1 se impossível).",
          'def min_moedas(moedas, valor):\n    inf = float("inf")\n    dp = [0] + [inf] * valor\n    for v in range(1, valor + 1):\n        for m in moedas:\n            if m <= v and dp[v - m] + 1 < dp[v]:\n                dp[v] = dp[v - m] + 1\n    return dp[valor] if dp[valor] != inf else -1', 'assert min_moedas([1, 5, 10, 25], 63) == 6 and min_moedas([1, 3, 4], 6) == 2 and min_moedas([2], 3) == -1 and min_moedas([5], 0) == 0', ["dp[v] = menor nº de moedas para v", "O guloso falha em [1, 3, 4] para 6"]),
        E(2, "Mochila 0/1", "Crie <code>mochila(itens, cap)</code> (itens = [(peso, valor)]) que devolve o maior valor possível.",
          'def mochila(itens, cap):\n    dp = [0] * (cap + 1)\n    for p, v in itens:\n        for c in range(cap, p - 1, -1):\n            dp[c] = max(dp[c], dp[c - p] + v)\n    return dp[cap]', 'assert mochila([(1, 1), (3, 4), (4, 5), (5, 7)], 7) == 9 and mochila([(5, 10)], 4) == 0', ["dp[c] = melhor valor com capacidade c", "Percorra a capacidade de trás para frente"]),
        E(2, "Maior subsequência comum", "Crie <code>lcs(a, b)</code> que devolve o tamanho da maior subsequência comum entre duas strings.",
          'def lcs(a, b):\n    dp = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]\n    for i in range(1, len(a) + 1):\n        for j in range(1, len(b) + 1):\n            if a[i - 1] == b[j - 1]:\n                dp[i][j] = dp[i - 1][j - 1] + 1\n            else:\n                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])\n    return dp[-1][-1]', 'assert lcs("ABCBDAB", "BDCABA") == 4 and lcs("abc", "xyz") == 0 and lcs("", "a") == 0', ["Tabela (len(a)+1) × (len(b)+1)", "Letras iguais: diagonal + 1"]),
        E(2, "Distância de edição", "Crie <code>levenshtein(a, b)</code>: menor número de inserções, remoções ou trocas para transformar a em b.",
          'def levenshtein(a, b):\n    ant = list(range(len(b) + 1))\n    for i, ca in enumerate(a, 1):\n        atual = [i]\n        for j, cb in enumerate(b, 1):\n            atual.append(min(ant[j] + 1, atual[j - 1] + 1, ant[j - 1] + (ca != cb)))\n        ant = atual\n    return ant[-1]', 'assert levenshtein("gato", "rato") == 1 and levenshtein("kitten", "sitting") == 3 and levenshtein("", "abc") == 3', ["Três operações: min das três", "Basta guardar a linha anterior"]),
        E(2, "Dijkstra", "Crie <code>dijkstra(grafo, ini)</code> (grafo = {v: [(vizinho, peso)]}) que devolve as menores distâncias a partir de ini.",
          'import heapq\n\ndef dijkstra(grafo, ini):\n    dist = {ini: 0}\n    h = [(0, ini)]\n    while h:\n        d, v = heapq.heappop(h)\n        if d > dist[v]:\n            continue\n        for w, p in grafo.get(v, []):\n            nd = d + p\n            if nd < dist.get(w, float("inf")):\n                dist[w] = nd\n                heapq.heappush(h, (nd, w))\n    return dist', 'g = {"A": [("B", 4), ("C", 1)], "C": [("B", 2), ("D", 7)], "B": [("D", 1)]}\nassert dijkstra(g, "A") == {"A": 0, "B": 3, "C": 1, "D": 4}', ["Heap de (distância, vértice)", "Ignore entradas desatualizadas"]),
        E(2, "Ordenação topológica", "Crie <code>ordem_topologica(deps)</code> (deps = {tarefa: [pré-requisitos]}) que devolve uma ordem válida (empate: ordem alfabética) ou ValueError se houver ciclo.",
          'import heapq\n\ndef ordem_topologica(deps):\n    nos = set(deps) | {p for ps in deps.values() for p in ps}\n    grau = {n: 0 for n in nos}\n    saem = {n: [] for n in nos}\n    for t, ps in deps.items():\n        for p in ps:\n            grau[t] += 1\n            saem[p].append(t)\n    h = [n for n in nos if grau[n] == 0]\n    heapq.heapify(h)\n    r = []\n    while h:\n        n = heapq.heappop(h)\n        r.append(n)\n        for t in saem[n]:\n            grau[t] -= 1\n            if grau[t] == 0:\n                heapq.heappush(h, t)\n    if len(r) != len(nos):\n        raise ValueError("Ciclo")\n    return r', 'assert ordem_topologica({"deploy": ["testes"], "testes": ["codigo"], "docs": ["codigo"]}) == ["codigo", "docs", "testes", "deploy"]\ntry:\n    ordem_topologica({"a": ["b"], "b": ["a"]}); assert False\nexcept ValueError:\n    pass', ["Conte quantos pré-requisitos cada tarefa tem", "Algoritmo de Kahn"]),
        E(2, "Cache LRU", "Crie <code>LRU(capacidade)</code> com <code>get(k)</code> (−1 se não existir) e <code>put(k, v)</code>; ao estourar, remove o item usado há mais tempo.",
          'from collections import OrderedDict\n\nclass LRU:\n    def __init__(self, capacidade):\n        self.cap = capacidade\n        self.d = OrderedDict()\n\n    def get(self, k):\n        if k not in self.d:\n            return -1\n        self.d.move_to_end(k)\n        return self.d[k]\n\n    def put(self, k, v):\n        self.d[k] = v\n        self.d.move_to_end(k)\n        if len(self.d) > self.cap:\n            self.d.popitem(last=False)', 'c = LRU(2)\nc.put(1, "a"); c.put(2, "b"); c.get(1); c.put(3, "c")\nassert c.get(2) == -1 and c.get(1) == "a" and c.get(3) == "c"', ["OrderedDict guarda a ordem de uso", "move_to_end e popitem(last=False)"]),
        E(2, "N rainhas", "Crie <code>n_rainhas(n)</code> que devolve quantas formas existem de colocar n rainhas sem ataque (backtracking).",
          'def n_rainhas(n):\n    cols, d1, d2 = set(), set(), set()\n    def colocar(l):\n        if l == n:\n            return 1\n        t = 0\n        for c in range(n):\n            if c in cols or l - c in d1 or l + c in d2:\n                continue\n            cols.add(c); d1.add(l - c); d2.add(l + c)\n            t += colocar(l + 1)\n            cols.remove(c); d1.remove(l - c); d2.remove(l + c)\n        return t\n    return colocar(0)', 'assert [n_rainhas(n) for n in range(1, 9)] == [1, 0, 0, 2, 10, 4, 40, 92]', ["Uma rainha por linha", "Sets para colunas e diagonais; desfaça ao voltar"]),
    ],
)
