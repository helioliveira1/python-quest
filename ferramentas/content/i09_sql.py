DB = '''import sqlite3
conexao = sqlite3.connect(":memory:")
cursor = conexao.cursor()
cursor.execute("CREATE TABLE Clientes (id INTEGER PRIMARY KEY, nome TEXT NOT NULL, email TEXT, cidade TEXT)")
cursor.execute("CREATE TABLE Vendas (id INTEGER PRIMARY KEY, cliente_id INTEGER, produto TEXT, valor REAL, data TEXT)")
cursor.executemany("INSERT INTO Clientes (nome, email, cidade) VALUES (?, ?, ?)", [
    ("Ana Souza", "ana@x.com", "Recife"), ("Leo Lima", "leo@x.com", "Olinda"),
    ("Bia Rocha", None, "Recife"), ("Caio Melo", "caio@x.com", "Caruaru")])
cursor.executemany("INSERT INTO Vendas (cliente_id, produto, valor, data) VALUES (?, ?, ?, ?)", [
    (1, "Notebook", 3500, "2026-01-10"), (1, "Mouse", 80, "2026-01-12"), (2, "Monitor", 1200, "2026-02-03"),
    (3, "Teclado", 150, "2026-02-15"), (2, "Mouse", 80, "2026-03-01"), (4, "Notebook", 3400, "2026-03-20")])
conexao.commit()
'''
TOPIC = dict(
    name="Python + SQL (banco de dados)", short="CRUD direto do Python",
    cdesc="conectar, executar comandos, parâmetros seguros, commit, CRUD e pandas.read_sql",
    map="fluxo", src="Intermediário • Módulo 28", pkgs=["sqlite3"],
    groups=[
        ["Conectar", [["pyodbc.connect(...)", "SQL Server (no seu PC, com o driver ODBC)"], ["sqlite3.connect(arquivo)", "banco em arquivo (usado aqui)"], ["conexao.cursor()", "objeto que executa os comandos"]]],
        ["CRUD", [["Create: INSERT INTO", "inserir linhas"], ["Read: SELECT", "fetchone, fetchall"], ["Update / Delete", "UPDATE ... SET / DELETE ... WHERE"]]],
        ["Parâmetros", [["? no SQL", "execute(sql, (v1, v2)) — pyodbc e sqlite3"], ["Nunca f-string com dados", "evita SQL Injection"], ["executemany", "vários registros de uma vez"]]],
        ["Confirmar e fechar", [["conexao.commit()", "grava INSERT/UPDATE/DELETE"], ["rollback()", "desfaz se der erro"], ["cursor.close() / conexao.close()", "libera a conexão"]]],
        ["Com pandas", [["pd.read_sql(sql, conexao)", "consulta direto num DataFrame"], ["df.to_sql(...)", "grava um DataFrame numa tabela"], ["SQLAlchemy", "ORM: tabelas como classes Python"]]],
    ],
    hot=[
        "O fluxo é sempre: conectar → cursor → execute → (commit) → fechar.",
        "SELECT não precisa de commit; INSERT, UPDATE e DELETE precisam.",
        "Use ? como parâmetro: execute(\"... WHERE id = ?\", (id,)). Nunca monte o SQL com f-string.",
        "fetchall() devolve uma lista de tuplas; fetchone() devolve uma tupla (ou None).",
        "UPDATE e DELETE sem WHERE afetam a tabela INTEIRA.",
        "Senha do banco fica em variável de ambiente, não na string de conexão do código.",
    ],
    trap="(id) não é tupla! Para um único parâmetro escreva (id,) com vírgula, senão o execute dá erro.",
    examples=[["crud_sqlite.py", '''import sqlite3

conexao = sqlite3.connect("loja.db")
cursor = conexao.cursor()
cursor.execute("INSERT INTO Clientes (nome, email) VALUES (?, ?)", ("Ana", "ana@x.com"))
conexao.commit()

cursor.execute("SELECT id, nome FROM Clientes WHERE nome LIKE ?", ("A%",))
for id_, nome in cursor.fetchall():
    print(id_, nome)

cursor.close()
conexao.close()'''], ["sql_server_no_seu_pc.py", '''# No seu PC, com SQL Server (pip install pyodbc):
import os, pyodbc
dados_conexao = (
    "Driver={ODBC Driver 18 for SQL Server};"
    "Server=localhost;Database=Loja;"
    f"UID={os.environ['DB_USER']};PWD={os.environ['DB_PASS']};TrustServerCertificate=yes"
)
conexao = pyodbc.connect(dados_conexao)
# O resto (cursor, execute com ?, commit) é IGUAL ao sqlite3.

import pandas as pd
df = pd.read_sql("SELECT * FROM Vendas", conexao)''']],
    ex=[
        dict(t="Primeira consulta", p="O banco já está conectado em <code>conexao</code> e <code>cursor</code>. Execute <code>SELECT nome FROM Clientes</code> e guarde em <code>linhas</code> o resultado de <code>fetchall()</code>.<br><small class='muted'>Aqui usamos SQLite no navegador; no SQL Server com pyodbc o código é o mesmo.</small>", s=DB,
             sol='cursor.execute("SELECT nome FROM Clientes")\nlinhas = cursor.fetchall()', test='assert linhas == [("Ana Souza",), ("Leo Lima",), ("Bia Rocha",), ("Caio Melo",)], "fetchall() devolve lista de tuplas"',
             h=["cursor.execute(\"SELECT ...\")", "linhas = cursor.fetchall()"]),
        dict(t="Lista de nomes", p="Transforme o resultado de <code>SELECT nome FROM Clientes ORDER BY nome</code> numa lista simples de textos em <code>nomes</code>.", s=DB,
             sol='cursor.execute("SELECT nome FROM Clientes ORDER BY nome")\nnomes = [linha[0] for linha in cursor.fetchall()]', test='assert nomes == ["Ana Souza", "Bia Rocha", "Caio Melo", "Leo Lima"], "Pegue o item [0] de cada tupla"',
             h=["Cada linha é uma tupla com uma coluna", "[linha[0] for linha in cursor.fetchall()]"]),
        dict(t="Um único registro", p="Busque o e-mail do cliente de <code>id = 2</code> com <code>fetchone()</code> e guarde só o texto em <code>email</code>. Use parâmetro <code>?</code>.", s=DB,
             sol='cursor.execute("SELECT email FROM Clientes WHERE id = ?", (2,))\nemail = cursor.fetchone()[0]', test='assert email == "leo@x.com"\nassert "?" in codigo, "Use o parâmetro ? no WHERE"',
             h=["fetchone() devolve uma tupla", "Um parâmetro: (2,) com vírgula"]),
        dict(t="Inserir com parâmetros", p="Insira o cliente com <code>nome</code>, <code>email</code> e <code>cidade</code> (variáveis) na tabela <code>Clientes</code> usando <code>?</code> e confirme com <code>commit()</code>.", s=DB + 'nome = "Duda Alves"\nemail = "duda@x.com"\ncidade = "Paulista"\n',
             sol='cursor.execute("INSERT INTO Clientes (nome, email, cidade) VALUES (?, ?, ?)", (nome, email, cidade))\nconexao.commit()',
             test='assert conexao.in_transaction is False, "Confirme com conexao.commit()"\nc = conexao.execute("SELECT nome, email, cidade FROM Clientes WHERE id = 5").fetchone()\nassert c == ("Duda Alves", "duda@x.com", "Paulista")\nassert "Duda" not in codigo, "Use as variáveis com ?, não valores fixos no SQL"',
             h=["INSERT INTO Clientes (nome, email, cidade) VALUES (?, ?, ?)", "Passe a tupla (nome, email, cidade) e depois commit()"]),
        dict(t="Contar registros", p="Use <code>SELECT COUNT(*) FROM Vendas</code> para guardar em <code>qtd</code> o número de vendas (inteiro).", s=DB,
             sol='cursor.execute("SELECT COUNT(*) FROM Vendas")\nqtd = cursor.fetchone()[0]', test='assert qtd == 6', h=["COUNT(*) conta as linhas", "fetchone()[0]"]),
        dict(t="Atualizar dado", p="Atualize o e-mail da cliente <code>Bia Rocha</code> (que está vazio) para <code>novo_email</code>, filtrando pelo nome com <code>?</code>. Guarde em <code>afetadas</code> o <code>cursor.rowcount</code> e faça <code>commit</code>.", s=DB + 'novo_email = "bia@x.com"\n',
             sol='cursor.execute("UPDATE Clientes SET email = ? WHERE nome = ?", (novo_email, "Bia Rocha"))\nafetadas = cursor.rowcount\nconexao.commit()',
             test='assert afetadas == 1, "Só uma linha deve ser alterada (não esqueça o WHERE)"\nassert conexao.execute("SELECT email FROM Clientes WHERE nome = \'Bia Rocha\'").fetchone()[0] == "bia@x.com"\nassert conexao.execute("SELECT COUNT(*) FROM Clientes WHERE email = \'bia@x.com\'").fetchone()[0] == 1\nassert not conexao.in_transaction, "Faça commit()"',
             h=["UPDATE Clientes SET email = ? WHERE nome = ?", "rowcount = quantas linhas mudaram"]),
        dict(t="Excluir com segurança", p="Exclua as vendas do produto <code>produto</code> (variável) com <code>DELETE ... WHERE</code> e <code>?</code>. Faça <code>commit</code> e guarde em <code>restantes</code> quantas vendas sobraram.", s=DB + 'produto = "Mouse"\n',
             sol='cursor.execute("DELETE FROM Vendas WHERE produto = ?", (produto,))\nconexao.commit()\ncursor.execute("SELECT COUNT(*) FROM Vendas")\nrestantes = cursor.fetchone()[0]',
             test='assert restantes == 4, "6 vendas - 2 de Mouse = 4"\nassert rodar(produto="Notebook")["restantes"] == 4\nassert "?" in codigo',
             h=["DELETE FROM Vendas WHERE produto = ?", "(produto,) é uma tupla com um item"]),
        dict(t="Vários registros de uma vez", p="Insira todas as vendas de <code>novas</code> (lista de tuplas <code>(cliente_id, produto, valor, data)</code>) com <code>executemany</code> e faça <code>commit</code>.", s=DB + 'novas = [(4, "Cabo HDMI", 45, "2026-04-01"), (1, "Webcam", 230, "2026-04-02")]\n',
             sol='cursor.executemany("INSERT INTO Vendas (cliente_id, produto, valor, data) VALUES (?, ?, ?, ?)", novas)\nconexao.commit()',
             test='assert conexao.execute("SELECT COUNT(*) FROM Vendas").fetchone()[0] == 8\nassert conexao.execute("SELECT produto FROM Vendas WHERE id = 8").fetchone()[0] == "Webcam"\nassert "executemany" in codigo and not conexao.in_transaction',
             h=["cursor.executemany(sql, lista_de_tuplas)", "Um ? para cada coluna"]),
        dict(t="Consulta com JOIN", p="Guarde em <code>compras</code> a lista de tuplas <code>(nome do cliente, produto, valor)</code> das vendas acima de <code>minimo</code>, ordenadas pelo valor (maior primeiro). Use <code>JOIN</code> entre <code>Vendas</code> e <code>Clientes</code>.", s=DB + "minimo = 1000\n",
             sol='cursor.execute("""\n    SELECT c.nome, v.produto, v.valor\n    FROM Vendas v\n    JOIN Clientes c ON c.id = v.cliente_id\n    WHERE v.valor > ?\n    ORDER BY v.valor DESC\n""", (minimo,))\ncompras = cursor.fetchall()',
             test='assert compras == [("Ana Souza", "Notebook", 3500.0), ("Caio Melo", "Notebook", 3400.0), ("Leo Lima", "Monitor", 1200.0)]\nassert len(rodar(minimo=3450)["compras"]) == 1, "Use o parâmetro minimo"',
             h=["JOIN Clientes c ON c.id = v.cliente_id", "WHERE v.valor > ? ORDER BY v.valor DESC"]),
        dict(t="read_sql do pandas", p="Use <code>pd.read_sql</code> para carregar <code>SELECT produto, valor FROM Vendas</code> num DataFrame <code>df</code> e guarde em <code>total_produto</code> a soma de valor por produto (Series ordenada pelo índice, como o groupby faz).", s=DB + "import pandas as pd\n",
             sol='df = pd.read_sql("SELECT produto, valor FROM Vendas", conexao)\ntotal_produto = df.groupby("produto")["valor"].sum()',
             test='assert list(df.columns) == ["produto", "valor"] and len(df) == 6\nassert total_produto.to_dict() == {"Monitor": 1200.0, "Mouse": 160.0, "Notebook": 6900.0, "Teclado": 150.0}',
             h=["pd.read_sql(sql, conexao)", "df.groupby(\"produto\")[\"valor\"].sum()"]),
        dict(t="Agregação no SQL", p="Calcule no próprio SQL o total vendido por cidade (<code>GROUP BY</code>), do maior para o menor, e guarde em <code>por_cidade</code> como dicionário <code>{cidade: total}</code>.", s=DB,
             sol='cursor.execute("""\n    SELECT c.cidade, SUM(v.valor) AS total\n    FROM Vendas v JOIN Clientes c ON c.id = v.cliente_id\n    GROUP BY c.cidade\n    ORDER BY total DESC\n""")\npor_cidade = dict(cursor.fetchall())',
             test='assert por_cidade == {"Recife": 3730.0, "Caruaru": 3400.0, "Olinda": 1280.0}\nassert list(por_cidade) == ["Recife", "Caruaru", "Olinda"], "Ordene do maior para o menor"',
             h=["SUM(v.valor) ... GROUP BY c.cidade", "dict(lista de tuplas de 2 itens) vira dicionário"]),
        dict(t="Transação com rollback", p="Crie <code>inserir_lote(lote)</code> que insere todas as vendas de uma lista de tuplas <code>(cliente_id, produto, valor, data)</code>. Se <b>qualquer</b> linha tiver produto vazio (<code>None</code> ou <code>\"\"</code>), gere <code>ValueError</code>, faça <code>rollback()</code> para não gravar nada e retorne <code>False</code>. Se tudo der certo, faça <code>commit()</code> e retorne <code>True</code>.", s=DB + 'lote = [(1, "Pendrive", 50, "2026-05-01"), (2, None, 20, "2026-05-02")]\n',
             sol='def inserir_lote(lote):\n    try:\n        for cliente_id, produto, valor, data in lote:\n            if not produto:\n                raise ValueError("Produto vazio")\n            cursor.execute("INSERT INTO Vendas (cliente_id, produto, valor, data) VALUES (?, ?, ?, ?)", (cliente_id, produto, valor, data))\n        conexao.commit()\n        return True\n    except ValueError:\n        conexao.rollback()\n        return False\n\nresultado = inserir_lote(lote)',
             test='assert inserir_lote([(1, "Pendrive", 50, "2026-05-01"), (2, None, 20, "2026-05-02")]) is False\nassert conexao.execute("SELECT COUNT(*) FROM Vendas").fetchone()[0] == 6, "Com rollback, nada do lote é gravado"\nassert inserir_lote([(1, "Cabo", 10, "2026-05-03")]) is True\nassert conexao.execute("SELECT COUNT(*) FROM Vendas").fetchone()[0] == 7',
             h=["try: ... commit() / except: rollback()", "rollback() desfaz o que não foi confirmado"]),
        dict(t="Evitar SQL Injection", p="A função <code>buscar_cliente(nome)</code> abaixo é vulnerável. Reescreva-a com parâmetro <code>?</code> (mesmo nome, retornando <code>fetchall()</code>).<pre class='code'>def buscar_cliente(nome):\n    cursor.execute(f\"SELECT id, nome FROM Clientes WHERE nome = '{nome}'\")\n    return cursor.fetchall()</pre>", s=DB,
             sol='def buscar_cliente(nome):\n    cursor.execute("SELECT id, nome FROM Clientes WHERE nome = ?", (nome,))\n    return cursor.fetchall()',
             test='assert buscar_cliente("Leo Lima") == [(2, "Leo Lima")]\nassert buscar_cliente("x\' OR \'1\'=\'1") == [], "Com ? o texto malicioso é tratado como dado, não como SQL"\nassert "f\\"SELECT" not in codigo and "?" in codigo',
             h=["Troque a f-string por ? no SQL", "execute(sql, (nome,))"]),
        dict(t="Criar tabela e importar", p="Crie a tabela <code>Produtos</code> (<code>id INTEGER PRIMARY KEY</code>, <code>nome TEXT</code>, <code>preco REAL</code>) <b>se não existir</b> e importe <code>catalogo</code> (lista de dicts) com <code>executemany</code>. Faça <code>commit</code>.", s=DB + 'catalogo = [{"nome": "Café", "preco": 18.9}, {"nome": "Chá", "preco": 9.5}]\n',
             sol='cursor.execute("CREATE TABLE IF NOT EXISTS Produtos (id INTEGER PRIMARY KEY, nome TEXT, preco REAL)")\ncursor.executemany("INSERT INTO Produtos (nome, preco) VALUES (?, ?)", [(p["nome"], p["preco"]) for p in catalogo])\nconexao.commit()',
             test='assert conexao.execute("SELECT nome, preco FROM Produtos ORDER BY id").fetchall() == [("Café", 18.9), ("Chá", 9.5)]\nassert "IF NOT EXISTS" in codigo.upper()\nassert not conexao.in_transaction',
             h=["CREATE TABLE IF NOT EXISTS ...", "Converta os dicts em tuplas para o executemany"]),
        dict(t="Desafio: mini CRUD", p="Crie 4 funções: <code>criar(nome, email)</code> → retorna o id novo (<code>cursor.lastrowid</code>); <code>ler(id)</code> → tupla <code>(nome, email)</code> ou <code>None</code>; <code>atualizar(id, email)</code> → <code>True</code> se alterou; <code>excluir(id)</code> → <code>True</code> se excluiu. Todas com <code>?</code> e <code>commit</code> quando alterarem dados.", s=DB,
             sol='def criar(nome, email):\n    cursor.execute("INSERT INTO Clientes (nome, email) VALUES (?, ?)", (nome, email))\n    conexao.commit()\n    return cursor.lastrowid\n\ndef ler(id_):\n    cursor.execute("SELECT nome, email FROM Clientes WHERE id = ?", (id_,))\n    return cursor.fetchone()\n\ndef atualizar(id_, email):\n    cursor.execute("UPDATE Clientes SET email = ? WHERE id = ?", (email, id_))\n    conexao.commit()\n    return cursor.rowcount == 1\n\ndef excluir(id_):\n    cursor.execute("DELETE FROM Clientes WHERE id = ?", (id_,))\n    conexao.commit()\n    return cursor.rowcount == 1',
             test='n = criar("Eva Dias", "eva@x.com")\nassert n == 5, "lastrowid do novo cliente"\nassert ler(n) == ("Eva Dias", "eva@x.com")\nassert ler(99) is None\nassert atualizar(n, "eva@novo.com") is True and ler(n)[1] == "eva@novo.com"\nassert atualizar(99, "x") is False\nassert excluir(n) is True and ler(n) is None\nassert excluir(n) is False\nassert not conexao.in_transaction, "Faça commit nas alterações"',
             h=["cursor.lastrowid tem o id do último INSERT", "cursor.rowcount diz quantas linhas o UPDATE/DELETE afetou"]),
    ],
)
