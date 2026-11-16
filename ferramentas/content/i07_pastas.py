BASE = '''import os
for pasta in ["relatorios", "fotos"]:
    os.makedirs(pasta, exist_ok=True)
arquivos = {"vendas_jan.xlsx": "x", "vendas_fev.xlsx": "x", "nota.txt": "lembrar", "foto1.jpg": "img",
            "relatorios/r1.pdf": "pdf", "relatorios/r2.pdf": "pdf", "fotos/praia.jpg": "img"}
for caminho, conteudo in arquivos.items():
    with open(caminho, "w") as f:
        f.write(conteudo)
'''
TOPIC = dict(
    name="Arquivos e pastas do computador", short="automatizar a organização de arquivos",
    cdesc="os, os.path, pathlib e shutil: listar, criar, renomear, mover e copiar",
    map="arvore", src="Intermediário • Módulo 26",
    groups=[
        ["Onde estou?", [["os.getcwd()", "pasta atual do programa"], ["Caminho relativo", "\"relatorios/r1.pdf\" a partir da pasta atual"], ["os.path.join(a, b)", "monta caminhos sem errar a barra"]]],
        ["Listar", [["os.listdir(pasta)", "nomes de arquivos e pastas"], ["os.path.isfile / isdir", "é arquivo? é pasta?"], ["Path(pasta).glob(\"*.pdf\")", "filtra por padrão"]]],
        ["Criar e verificar", [["os.makedirs(p, exist_ok=True)", "cria pastas (e subpastas)"], ["os.path.exists(p)", "já existe?"], ["os.path.splitext(nome)", "separa nome e extensão"]]],
        ["Mover e copiar (shutil)", [["shutil.copy(origem, destino)", "copia arquivo"], ["shutil.move(origem, destino)", "move ou renomeia"], ["os.rename / os.remove", "renomear / apagar"]]],
        ["pathlib (moderno)", [["Path(\"a\") / \"b.txt\"", "monta caminho com /"], ["p.suffix, p.stem, p.name", "extensão, nome sem extensão, nome"], ["p.read_text() / write_text()", "ler e gravar rápido"]]],
    ],
    hot=[
        "Use os.path.join ou Path para montar caminhos: funciona no Windows e no Linux.",
        "os.listdir devolve só os NOMES; junte com a pasta para ter o caminho completo.",
        "makedirs(..., exist_ok=True) não dá erro se a pasta já existir.",
        "shutil.move serve tanto para mover quanto para renomear.",
        "Teste a automação numa cópia da pasta antes de rodar nos arquivos reais.",
    ],
    trap="os.remove e shutil.move não pedem confirmação nem mandam para a lixeira. Imprima o que vai fazer antes de executar de verdade.",
    examples=[["organizar.py", '''import os, shutil

for nome in os.listdir("."):
    if os.path.isfile(nome):
        extensao = os.path.splitext(nome)[1].lower().strip(".") or "sem_extensao"
        os.makedirs(extensao, exist_ok=True)
        shutil.move(nome, os.path.join(extensao, nome))'''], ["pathlib.py", '''from pathlib import Path

pasta = Path("relatorios")
for arquivo in pasta.glob("*.pdf"):
    print(arquivo.name, arquivo.stem, arquivo.suffix)

(Path("saida") / "resumo.txt").parent.mkdir(exist_ok=True)
(Path("saida") / "resumo.txt").write_text("ok", encoding="utf-8")''']],
    ex=[
        dict(t="Listar a pasta", p="Guarde em <code>itens</code> a lista <b>ordenada</b> com os nomes do que existe na pasta atual (<code>os.listdir(\".\")</code>).", s=BASE,
             sol='import os\nitens = sorted(os.listdir("."))', test='assert itens == ["foto1.jpg", "fotos", "nota.txt", "relatorios", "vendas_fev.xlsx", "vendas_jan.xlsx"]',
             h=["import os", "sorted(os.listdir(\".\"))"]),
        dict(t="Só arquivos", p="Crie <code>arquivos</code> com os nomes (ordenados) que são <b>arquivos</b> na pasta atual, ignorando as pastas.", s=BASE,
             sol='import os\narquivos = sorted(n for n in os.listdir(".") if os.path.isfile(n))', test='assert arquivos == ["foto1.jpg", "nota.txt", "vendas_fev.xlsx", "vendas_jan.xlsx"], "Use os.path.isfile"',
             h=["os.path.isfile(nome)", "Filtre a lista do listdir"]),
        dict(t="Montar caminho", p="Use <code>os.path.join</code> para montar o caminho da pasta <code>relatorios</code> com o arquivo <code>r1.pdf</code> em <code>caminho</code>, e guarde em <code>existe</code> se ele existe.", s=BASE,
             sol='import os\ncaminho = os.path.join("relatorios", "r1.pdf")\nexiste = os.path.exists(caminho)', test='import os as _o\nassert caminho == _o.path.join("relatorios", "r1.pdf"), "Use os.path.join"\nassert existe is True',
             h=["os.path.join(\"pasta\", \"arquivo\")", "os.path.exists(caminho)"]),
        dict(t="Criar pasta", p="Crie a pasta <code>backup/2026</code> (com a subpasta) sem dar erro se já existir.", s=BASE,
             sol='import os\nos.makedirs(os.path.join("backup", "2026"), exist_ok=True)', test='import os as _o\nassert _o.path.isdir(_o.path.join("backup", "2026")), "Use os.makedirs(..., exist_ok=True)"',
             h=["os.makedirs cria as pastas intermediárias", "exist_ok=True evita erro"]),
        dict(t="Separar a extensão", p="Para cada nome em <code>nomes</code>, guarde a extensão (sem o ponto, minúscula) na lista <code>extensoes</code>, usando <code>os.path.splitext</code>.", s='nomes = ["Planilha.XLSX", "foto.jpg", "contrato.final.pdf"]',
             sol='import os\nextensoes = [os.path.splitext(n)[1].lower().lstrip(".") for n in nomes]', test='assert extensoes == ["xlsx", "jpg", "pdf"], "splitext(\\"a.b.pdf\\") devolve (\\"a.b\\", \\".pdf\\")"',
             h=["os.path.splitext(nome) devolve (nome, \".ext\")", "lower() e lstrip(\".\")"]),
        dict(t="Copiar arquivo", p="Copie <code>nota.txt</code> para a pasta <code>relatorios</code> com <code>shutil.copy</code>, mantendo o original.", s=BASE,
             sol='import shutil\nshutil.copy("nota.txt", "relatorios")', test='import os as _o\nassert _o.path.exists(_o.path.join("relatorios", "nota.txt")), "A cópia deve estar em relatorios"\nassert _o.path.exists("nota.txt"), "O original deve continuar na pasta"',
             h=["import shutil", "shutil.copy(origem, pasta_destino)"]),
        dict(t="Mover por extensão", p="Mova todos os arquivos <code>.jpg</code> da pasta atual para a pasta <code>fotos</code>.", s=BASE,
             sol='import os, shutil\nfor nome in os.listdir("."):\n    if os.path.isfile(nome) and nome.endswith(".jpg"):\n        shutil.move(nome, os.path.join("fotos", nome))', test='import os as _o\nassert sorted(_o.listdir("fotos")) == ["foto1.jpg", "praia.jpg"]\nassert not _o.path.exists("foto1.jpg"), "Mova (não copie)"',
             h=["nome.endswith(\".jpg\")", "shutil.move(origem, destino)"]),
        dict(t="Renomear em lote", p="Renomeie os arquivos que começam com <code>vendas_</code> trocando o prefixo por <code>2026_vendas_</code> (ex.: <code>vendas_jan.xlsx</code> → <code>2026_vendas_jan.xlsx</code>).", s=BASE,
             sol='import os\nfor nome in os.listdir("."):\n    if nome.startswith("vendas_"):\n        os.rename(nome, "2026_" + nome)', test='import os as _o\nassert sorted(n for n in _o.listdir(".") if "vendas" in n) == ["2026_vendas_fev.xlsx", "2026_vendas_jan.xlsx"]',
             h=["os.rename(nome_antigo, nome_novo)", "\"2026_\" + nome"]),
        dict(t="Glob com pathlib", p="Use <code>Path(\"relatorios\").glob(\"*.pdf\")</code> para criar <code>pdfs</code>: lista ordenada só com os <b>nomes sem extensão</b> (<code>.stem</code>).", s=BASE,
             sol='from pathlib import Path\npdfs = sorted(p.stem for p in Path("relatorios").glob("*.pdf"))', test='assert pdfs == ["r1", "r2"]\nassert "glob" in codigo',
             h=["from pathlib import Path", ".stem é o nome sem extensão"]),
        dict(t="Tamanho dos arquivos", p="Crie <code>tamanhos</code>: dicionário <code>{nome: tamanho em bytes}</code> dos arquivos da pasta atual (ignore pastas), com <code>os.path.getsize</code>.", s=BASE,
             sol='import os\ntamanhos = {n: os.path.getsize(n) for n in os.listdir(".") if os.path.isfile(n)}', test='assert tamanhos == {"vendas_jan.xlsx": 1, "vendas_fev.xlsx": 1, "nota.txt": 7, "foto1.jpg": 3}',
             h=["os.path.getsize(caminho)", "Dict comprehension com filtro isfile"]),
        dict(t="Percorrer subpastas", p="Use <code>os.walk(\".\")</code> para contar quantos arquivos existem no total (pasta atual + subpastas) em <code>total</code>.", s=BASE,
             sol='import os\ntotal = 0\nfor raiz, pastas, arquivos in os.walk("."):\n    total += len(arquivos)', test='assert total == 7, "4 na raiz + 2 em relatorios + 1 em fotos"\nassert "walk" in codigo',
             h=["os.walk devolve (pasta, subpastas, arquivos) para cada pasta", "Some len(arquivos)"]),
        dict(t="Ler e gravar com Path", p="Com <code>pathlib</code>, leia <code>nota.txt</code>, converta para maiúsculas e grave em <code>saida/NOTA.txt</code> (crie a pasta <code>saida</code>).", s=BASE,
             sol='from pathlib import Path\ntexto = Path("nota.txt").read_text()\ndestino = Path("saida") / "NOTA.txt"\ndestino.parent.mkdir(exist_ok=True)\ndestino.write_text(texto.upper())', test='from pathlib import Path as _P\nassert (_P("saida") / "NOTA.txt").read_text() == "LEMBRAR"',
             h=["Path(\"a\") / \"b\" monta caminhos", "read_text(), write_text() e parent.mkdir()"]),
        dict(t="Organizar por extensão", p="Mova cada arquivo da pasta atual para uma pasta com o nome da sua extensão (<code>xlsx</code>, <code>txt</code>, <code>jpg</code>...). Pastas existentes não devem ser mexidas.", s=BASE,
             sol='import os, shutil\nfor nome in os.listdir("."):\n    if os.path.isfile(nome):\n        ext = os.path.splitext(nome)[1].lstrip(".").lower()\n        os.makedirs(ext, exist_ok=True)\n        shutil.move(nome, os.path.join(ext, nome))', test='import os as _o\nassert sorted(_o.listdir("xlsx")) == ["vendas_fev.xlsx", "vendas_jan.xlsx"]\nassert _o.listdir("txt") == ["nota.txt"] and _o.listdir("jpg") == ["foto1.jpg"]\nassert sorted(_o.listdir("relatorios")) == ["r1.pdf", "r2.pdf"], "Não mexa nas pastas que já existiam"\nassert not [n for n in _o.listdir(".") if _o.path.isfile(n)], "Não deve sobrar arquivo solto"',
             h=["Pegue a extensão com splitext", "makedirs(ext, exist_ok=True) e depois shutil.move"]),
        dict(t="Backup com data", p="Copie a pasta <code>relatorios</code> inteira para <code>backup_relatorios_AAAA-MM-DD</code> usando a data de <code>hoje</code> e <code>shutil.copytree</code>. Guarde o nome da pasta criada em <code>pasta_backup</code>.", s=BASE + "from datetime import date\nhoje = date(2026, 11, 16)\n",
             sol='import shutil\npasta_backup = f"backup_relatorios_{hoje:%Y-%m-%d}"\nshutil.copytree("relatorios", pasta_backup)', test='import os as _o\nassert pasta_backup == "backup_relatorios_2026-11-16"\nassert sorted(_o.listdir(pasta_backup)) == ["r1.pdf", "r2.pdf"], "Use shutil.copytree"',
             h=["f\"{hoje:%Y-%m-%d}\" formata a data", "shutil.copytree(origem, destino)"]),
        dict(t="Desafio: relatório da pasta", p="Percorra a pasta atual e subpastas (<code>os.walk</code>) e crie <code>por_extensao</code>: <code>{extensão: quantidade}</code> com as chaves em ordem alfabética. Depois grave <code>inventario.txt</code> com uma linha <code>ext: qtd</code> por extensão.", s=BASE,
             sol='import os\ncontagem = {}\nfor raiz, pastas, arquivos in os.walk("."):\n    for nome in arquivos:\n        ext = os.path.splitext(nome)[1].lstrip(".").lower()\n        contagem[ext] = contagem.get(ext, 0) + 1\npor_extensao = dict(sorted(contagem.items()))\nwith open("inventario.txt", "w", encoding="utf-8") as f:\n    for ext, qtd in por_extensao.items():\n        f.write(f"{ext}: {qtd}\\n")',
             test='assert por_extensao == {"jpg": 2, "pdf": 2, "txt": 1, "xlsx": 2}\nassert list(por_extensao) == ["jpg", "pdf", "txt", "xlsx"], "Chaves em ordem alfabética"\nassert open("inventario.txt", encoding="utf-8").read().splitlines() == ["jpg: 2", "pdf: 2", "txt: 1", "xlsx: 2"]',
             h=["Conte antes de criar o inventario.txt (senão ele entra na contagem)", "dict(sorted(d.items())) ordena pelas chaves"]),
    ],
)
