PAG_LOGIN = '''from simulador_web import PAGINAS
PAGINAS["https://loja.exemplo/login"] = """
<html><head><title>Login - Loja Exemplo</title></head><body>
  <h1 class="titulo">Acesso ao sistema</h1>
  <form id="form-login">
    <input id="email" name="email" type="text">
    <input id="senha" name="senha" type="password">
    <input id="lembrar" name="lembrar" type="checkbox" value="sim">
    <button id="entrar" type="submit">Entrar</button>
  </form>
  <a id="esqueci" href="https://loja.exemplo/recuperar">Esqueci a senha</a>
</body></html>"""
PAGINAS["https://loja.exemplo/recuperar"] = """
<html><head><title>Recuperar senha</title></head><body><p id="msg">Informe seu e-mail.</p></body></html>"""
'''

PAG_PRODUTOS = '''from simulador_web import PAGINAS
PAGINAS["https://loja.exemplo/produtos"] = """
<html><head><title>Produtos</title></head><body>
  <h1>Catálogo</h1>
  <div class="produto" data-id="101"><span class="nome">Notebook</span> <span class="preco">3500.00</span> <span class="estoque">5</span></div>
  <div class="produto destaque" data-id="102"><span class="nome">Mouse</span> <span class="preco">80.00</span> <span class="estoque">0</span></div>
  <div class="produto" data-id="103"><span class="nome">Teclado</span> <span class="preco">150.00</span> <span class="estoque">12</span></div>
  <div class="produto destaque" data-id="104"><span class="nome">Monitor</span> <span class="preco">1200.00</span> <span class="estoque">3</span></div>
  <table id="tabela-vendas">
    <tr><th>Mês</th><th>Vendas</th></tr>
    <tr><td>Jan</td><td>100</td></tr>
    <tr><td>Fev</td><td>140</td></tr>
    <tr><td>Mar</td><td>90</td></tr>
  </table>
  <a class="link" href="https://loja.exemplo/login">Entrar</a>
  <a class="link" href="https://loja.exemplo/carrinho">Carrinho (0)</a>
</body></html>"""
PAGINAS["https://loja.exemplo/login"] = "<html><head><title>Login</title></head><body></body></html>"
PAGINAS["https://loja.exemplo/carrinho"] = "<html><head><title>Carrinho</title></head><body><p id='vazio'>Seu carrinho está vazio</p></body></html>"
'''

PAG_FORM = '''from simulador_web import PAGINAS
PAGINAS["https://rh.exemplo/cadastro"] = """
<html><head><title>Cadastro de Funcionário</title></head><body>
  <form id="cadastro">
    <input id="nome" name="nome" type="text">
    <input id="cpf" name="cpf" type="text" value="000.000.000-00">
    <select id="setor" name="setor">
      <option value="">-- escolha --</option>
      <option value="fin">Financeiro</option>
      <option value="ti">Tecnologia</option>
      <option value="rh">Recursos Humanos</option>
    </select>
    <input type="radio" name="turno" id="manha" value="manha">
    <input type="radio" name="turno" id="tarde" value="tarde">
    <input type="checkbox" name="beneficios" id="vr" value="VR">
    <input type="checkbox" name="beneficios" id="vt" value="VT">
    <input type="checkbox" name="beneficios" id="plano" value="Plano de saúde">
    <textarea id="obs" name="obs"></textarea>
    <button id="salvar" type="submit">Salvar</button>
  </form>
</body></html>"""
'''

PAG_IFRAME = '''from simulador_web import PAGINAS
PAGINAS["https://portal.exemplo/"] = """
<html><head><title>Portal</title></head><body>
  <h1 id="topo">Portal do Cliente</h1>
  <iframe id="quadro-cotacao" src="https://portal.exemplo/cotacao"></iframe>
</body></html>"""
PAGINAS["https://portal.exemplo/cotacao"] = """
<html><body><span id="dolar">5.43</span><span id="euro">5.91</span></body></html>"""
'''

TOPIC = dict(
    name="Automação Web (Selenium)", short="navegador no piloto automático",
    cdesc="controlar o navegador por código: abrir páginas, achar elementos e preencher formulários",
    map="fluxo", src="Intermediário • Módulo 29",
    groups=[
        ["Começar", [["webdriver.Chrome()", "abre o navegador controlado pelo Python"], ["navegador.get(url)", "acessa uma página"], ["navegador.quit()", "fecha o navegador ao final"]]],
        ["Encontrar elementos", [["find_element(By.ID, ...)", "1º elemento que atende; erro se não achar"], ["find_elements(...)", "lista com todos (vazia se nenhum)"], ["By.*", "ID, NAME, CLASS_NAME, TAG_NAME, CSS_SELECTOR, XPATH"]]],
        ["Interagir", [["send_keys / clear", "digitar e limpar campos"], ["click()", "botões, links, checkbox e radio"], ["Select(...)", "listas suspensas: select_by_visible_text / value"]]],
        ["Ler informações", [[".text", "texto visível do elemento"], ["get_attribute('...')", "value, href, class, data-*"], ["Árvore HTML", "buscar dentro de um elemento: el.find_element(...)"]]],
        ["Robustez", [["Esperas", "implicitly_wait / WebDriverWait + expected_conditions"], ["iframe", "switch_to.frame(...) e default_content()"], ["Boas práticas", "seletores estáveis (id), não guardar senha no código"]]],
    ],
    hot=[
        "find_element devolve UM elemento (e dá erro se não achar); find_elements devolve uma LISTA.",
        "Prefira By.ID quando existir: é o seletor mais estável.",
        "By.CLASS_NAME aceita só UMA classe; para várias use CSS: '.produto.destaque'.",
        ".text pega o texto visível; get_attribute('value') pega o que está digitado num input.",
        "Elemento dentro de iframe só é encontrado depois de switch_to.frame(...).",
        "Use esperas (WebDriverWait) em vez de time.sleep fixo quando a página carrega dados dinamicamente.",
    ],
    trap="send_keys ACRESCENTA texto ao que já existe no campo. Se o campo já vem preenchido, chame clear() antes.",
    examples=[["selenium_basico.py", '''from selenium import webdriver
from selenium.webdriver.common.by import By

navegador = webdriver.Chrome()
navegador.get("https://loja.exemplo/login")

navegador.find_element(By.ID, "email").send_keys("ana@exemplo.com")
navegador.find_element(By.ID, "senha").send_keys(senha)   # senha vinda de variável de ambiente
navegador.find_element(By.ID, "entrar").click()

produtos = navegador.find_elements(By.CLASS_NAME, "produto")
for p in produtos:
    print(p.find_element(By.CLASS_NAME, "nome").text)

navegador.quit()'''], ["formulario.py", '''from selenium.webdriver.support.ui import Select

Select(navegador.find_element(By.ID, "setor")).select_by_visible_text("Tecnologia")
navegador.find_element(By.ID, "manha").click()        # radio
navegador.find_element(By.XPATH, "//input[@value='VT']").click()
campo = navegador.find_element(By.ID, "cpf")
campo.clear()                                          # apaga o valor antigo
campo.send_keys("123.456.789-00")''']],
    ex=[
        dict(t="Abrir a página", p="Crie o navegador com <code>webdriver.Chrome()</code> na variável <code>navegador</code>, acesse <code>https://loja.exemplo/login</code> e guarde o título da página em <code>titulo</code>.<br><small class='muted'>Aqui o Selenium é um <b>simulador</b> que roda no navegador; no seu PC o código é o mesmo.</small>",
             s=PAG_LOGIN, sol='from selenium import webdriver\n\nnavegador = webdriver.Chrome()\nnavegador.get("https://loja.exemplo/login")\ntitulo = navegador.title',
             test='assert navegador.current_url == "https://loja.exemplo/login", "Acesse a URL com navegador.get(...)"\nassert titulo == "Login - Loja Exemplo", "Use navegador.title para pegar o título"',
             h=["from selenium import webdriver", "navegador.get(url) e depois navegador.title"]),
        dict(t="Achar pela classe", p="A página de login já está aberta em <code>navegador</code>. Encontre o título <code>&lt;h1&gt;</code> pela classe <code>titulo</code> e guarde o texto em <code>cabecalho</code>.",
             s=PAG_LOGIN + 'from selenium import webdriver\nfrom selenium.webdriver.common.by import By\nnavegador = webdriver.Chrome()\nnavegador.get("https://loja.exemplo/login")\n',
             sol='cabecalho = navegador.find_element(By.CLASS_NAME, "titulo").text',
             test='assert cabecalho == "Acesso ao sistema", "Use find_element(By.CLASS_NAME, \\"titulo\\").text"',
             h=["find_element(By.CLASS_NAME, ...)", "O texto visível está em .text"]),
        dict(t="Preencher o login", p="Com o login aberto, digite <code>usuario</code> no campo de id <code>email</code> e <code>senha</code> no campo de id <code>senha</code>. As duas variáveis já existem.",
             s=PAG_LOGIN + 'from selenium import webdriver\nfrom selenium.webdriver.common.by import By\nnavegador = webdriver.Chrome()\nnavegador.get("https://loja.exemplo/login")\nusuario = "ana@exemplo.com"\nsenha = "s3nh@"\n',
             sol='navegador.find_element(By.ID, "email").send_keys(usuario)\nnavegador.find_element(By.ID, "senha").send_keys(senha)',
             test='assert navegador.find_element(By.ID, "email").get_attribute("value") == "ana@exemplo.com", "O campo email deve conter o usuário"\nassert navegador.find_element(By.ID, "senha").get_attribute("value") == "s3nh@", "O campo senha deve conter a senha"\nr = rodar(usuario="leo@x.com", senha="123")\nn = r["navegador"]\nassert n.find_element(By.ID, "email").get_attribute("value") == "leo@x.com", "Use as variáveis usuario e senha, não textos fixos"',
             h=["find_element(By.ID, \"email\")", ".send_keys(usuario)"]),
        dict(t="Clicar em Entrar", p="Preencha o e-mail com <code>usuario</code>, marque a caixa <b>lembrar</b> (id <code>lembrar</code>) e clique no botão <code>entrar</code>. O simulador registra o formulário enviado em <code>navegador.formularios_enviados</code>.",
             s=PAG_LOGIN + 'from selenium import webdriver\nfrom selenium.webdriver.common.by import By\nnavegador = webdriver.Chrome()\nnavegador.get("https://loja.exemplo/login")\nusuario = "ana@exemplo.com"\n',
             sol='navegador.find_element(By.ID, "email").send_keys(usuario)\nnavegador.find_element(By.ID, "lembrar").click()\nnavegador.find_element(By.ID, "entrar").click()',
             test='env = navegador.formularios_enviados\nassert env, "O formulário não foi enviado: clique no botão entrar"\nassert env[-1].get("email") == usuario, "Preencha o e-mail antes de clicar em Entrar"\nassert env[-1].get("lembrar") == "sim", "Marque a caixa lembrar com .click() antes de enviar"',
             h=["Checkbox também se marca com .click()", "A ordem importa: preencha e marque ANTES de clicar em entrar"]),
        dict(t="Ler o link", p="Guarde em <code>destino</code> o endereço (atributo <code>href</code>) do link de id <code>esqueci</code>.",
             s=PAG_LOGIN + 'from selenium import webdriver\nfrom selenium.webdriver.common.by import By\nnavegador = webdriver.Chrome()\nnavegador.get("https://loja.exemplo/login")\n',
             sol='destino = navegador.find_element(By.ID, "esqueci").get_attribute("href")',
             test='assert destino == "https://loja.exemplo/recuperar", "Use get_attribute(\\"href\\")"',
             h=["Atributos HTML: get_attribute(\"nome\")", "O texto do link (.text) não é o endereço"]),
        dict(t="Listar produtos", p="Na página de produtos (já aberta), crie a lista <code>nomes</code> com o texto de todos os elementos de classe <code>nome</code>, na ordem da página.",
             s=PAG_PRODUTOS + 'from selenium import webdriver\nfrom selenium.webdriver.common.by import By\nnavegador = webdriver.Chrome()\nnavegador.get("https://loja.exemplo/produtos")\n',
             sol='nomes = [el.text for el in navegador.find_elements(By.CLASS_NAME, "nome")]',
             test='assert nomes == ["Notebook", "Mouse", "Teclado", "Monitor"], "Use find_elements (no plural) e pegue o .text de cada um"',
             h=["find_elements devolve uma lista", "Percorra com for (ou list comprehension) pegando .text"]),
        dict(t="Busca dentro do elemento", p="Para cada <code>div.produto</code>, pegue o nome e o preço (como <code>float</code>) <b>dentro do próprio card</b> e monte o dicionário <code>precos</code> no formato <code>{nome: preço}</code>.",
             s=PAG_PRODUTOS + 'from selenium import webdriver\nfrom selenium.webdriver.common.by import By\nnavegador = webdriver.Chrome()\nnavegador.get("https://loja.exemplo/produtos")\n',
             sol='precos = {}\nfor card in navegador.find_elements(By.CLASS_NAME, "produto"):\n    nome = card.find_element(By.CLASS_NAME, "nome").text\n    precos[nome] = float(card.find_element(By.CLASS_NAME, "preco").text)',
             test='assert precos == {"Notebook": 3500.0, "Mouse": 80.0, "Teclado": 150.0, "Monitor": 1200.0}, "Esperado {nome: preço float} para os 4 produtos"',
             h=["Um elemento também tem find_element: card.find_element(...)", "Converta o texto do preço com float()"]),
        dict(t="Seletor CSS", p="Usando <code>By.CSS_SELECTOR</code>, guarde em <code>destaques</code> a lista com o <b>nome</b> dos produtos que têm as classes <code>produto</code> e <code>destaque</code> ao mesmo tempo.",
             s=PAG_PRODUTOS + 'from selenium import webdriver\nfrom selenium.webdriver.common.by import By\nnavegador = webdriver.Chrome()\nnavegador.get("https://loja.exemplo/produtos")\n',
             sol='destaques = [el.text for el in navegador.find_elements(By.CSS_SELECTOR, ".produto.destaque .nome")]',
             test='assert destaques == ["Mouse", "Monitor"], "Os destaques são Mouse e Monitor"\nassert "CSS_SELECTOR" in codigo, "Use By.CSS_SELECTOR"',
             h=["Duas classes juntas, sem espaço: .produto.destaque", "Espaço = descendente: \".produto.destaque .nome\""]),
        dict(t="Formulário com lista suspensa", p="No cadastro (já aberto), digite <code>nome</code> no campo <code>nome</code>, escolha o setor <b>Tecnologia</b> pelo texto visível e o turno <b>manhã</b> (radio de id <code>manha</code>). Depois clique em <code>salvar</code>.",
             s=PAG_FORM + 'from selenium import webdriver\nfrom selenium.webdriver.common.by import By\nfrom selenium.webdriver.support.ui import Select\nnavegador = webdriver.Chrome()\nnavegador.get("https://rh.exemplo/cadastro")\nnome = "Bruna Lima"\n',
             sol='navegador.find_element(By.ID, "nome").send_keys(nome)\nSelect(navegador.find_element(By.ID, "setor")).select_by_visible_text("Tecnologia")\nnavegador.find_element(By.ID, "manha").click()\nnavegador.find_element(By.ID, "salvar").click()',
             test='f = navegador.formularios_enviados\nassert f, "Clique em salvar para enviar o formulário"\nassert f[-1]["nome"] == nome, "Preencha o nome"\nassert f[-1]["setor"] == "ti", "Escolha Tecnologia com Select(...).select_by_visible_text"\nassert f[-1].get("turno") == "manha", "Clique no radio de id manha"',
             h=["Select(elemento).select_by_visible_text(\"Tecnologia\")", "Radio button: .click()"]),
        dict(t="Corrigir campo preenchido", p="O campo <code>cpf</code> já vem com <code>000.000.000-00</code>. Substitua pelo valor de <code>cpf</code> e guarde o valor final do campo em <code>valor_final</code>.",
             s=PAG_FORM + 'from selenium import webdriver\nfrom selenium.webdriver.common.by import By\nnavegador = webdriver.Chrome()\nnavegador.get("https://rh.exemplo/cadastro")\ncpf = "123.456.789-00"\n',
             sol='campo = navegador.find_element(By.ID, "cpf")\ncampo.clear()\ncampo.send_keys(cpf)\nvalor_final = campo.get_attribute("value")',
             test='assert valor_final == "123.456.789-00", "O campo deve ter só o CPF novo. send_keys acrescenta: use clear() antes"\nassert rodar(cpf="111.222.333-44")["valor_final"] == "111.222.333-44", "Use a variável cpf"',
             h=["send_keys acrescenta ao texto existente", "campo.clear() antes de digitar"]),
        dict(t="Ler tabela HTML", p="Leia a tabela <code>tabela-vendas</code> e monte o dicionário <code>vendas</code> <code>{mês: vendas (int)}</code>, ignorando a linha de cabeçalho.",
             s=PAG_PRODUTOS + 'from selenium import webdriver\nfrom selenium.webdriver.common.by import By\nnavegador = webdriver.Chrome()\nnavegador.get("https://loja.exemplo/produtos")\n',
             sol='vendas = {}\ntabela = navegador.find_element(By.ID, "tabela-vendas")\nfor linha in tabela.find_elements(By.TAG_NAME, "tr")[1:]:\n    celulas = linha.find_elements(By.TAG_NAME, "td")\n    vendas[celulas[0].text] = int(celulas[1].text)',
             test='assert vendas == {"Jan": 100, "Fev": 140, "Mar": 90}, "Esperado {\\"Jan\\": 100, \\"Fev\\": 140, \\"Mar\\": 90}"',
             h=["Linhas: find_elements(By.TAG_NAME, \"tr\"); pule a primeira com [1:]", "Células: find_elements(By.TAG_NAME, \"td\")"]),
        dict(t="XPath por atributo", p="Marque os benefícios cujos <b>values</b> estão na lista <code>escolhidos</code>, usando <b>XPath</b> (<code>//input[@value='...']</code>). Depois clique em <code>salvar</code>.",
             s=PAG_FORM + 'from selenium import webdriver\nfrom selenium.webdriver.common.by import By\nnavegador = webdriver.Chrome()\nnavegador.get("https://rh.exemplo/cadastro")\nescolhidos = ["VR", "Plano de saúde"]\n',
             sol='for b in escolhidos:\n    navegador.find_element(By.XPATH, f"//input[@value=\'{b}\']").click()\nnavegador.find_element(By.ID, "salvar").click()',
             test='f = navegador.formularios_enviados\nassert f, "Clique em salvar"\nassert sorted(f[-1].get("beneficios", [])) == ["Plano de saúde", "VR"], "Marque exatamente os benefícios de escolhidos"\nn = rodar(escolhidos=["VT"])["navegador"]\nassert n.formularios_enviados[-1].get("beneficios") == "VT", "Percorra a lista escolhidos"\nassert "XPATH" in codigo, "Use By.XPATH"',
             h=["f-string no XPath: f\"//input[@value='{b}']\"", "Use aspas simples dentro e duplas fora"]),
        dict(t="Conteúdo dentro de iframe", p="A cotação está num <code>iframe</code> de id <code>quadro-cotacao</code>. Entre nele, leia o dólar (id <code>dolar</code>) como <code>float</code> em <code>dolar</code>, volte para a página principal e guarde o texto do <code>h1</code> (id <code>topo</code>) em <code>titulo</code>.",
             s=PAG_IFRAME + 'from selenium import webdriver\nfrom selenium.webdriver.common.by import By\nnavegador = webdriver.Chrome()\nnavegador.get("https://portal.exemplo/")\n',
             sol='quadro = navegador.find_element(By.ID, "quadro-cotacao")\nnavegador.switch_to.frame(quadro)\ndolar = float(navegador.find_element(By.ID, "dolar").text)\nnavegador.switch_to.default_content()\ntitulo = navegador.find_element(By.ID, "topo").text',
             test='assert dolar == 5.43, "Entre no iframe com navegador.switch_to.frame(...) e leia o id dolar"\nassert titulo == "Portal do Cliente", "Volte com switch_to.default_content() antes de buscar o h1"',
             h=["navegador.switch_to.frame(elemento_do_iframe)", "Para voltar: navegador.switch_to.default_content()"]),
        dict(t="Espera explícita", p="Use <code>WebDriverWait(navegador, 10)</code> com <code>EC.presence_of_element_located</code> para aguardar o elemento de id <code>vazio</code> na página do carrinho (clique no link que contém o texto <b>Carrinho</b>). Guarde o texto em <code>aviso</code>.",
             s=PAG_PRODUTOS + 'from selenium import webdriver\nfrom selenium.webdriver.common.by import By\nfrom selenium.webdriver.support.ui import WebDriverWait\nfrom selenium.webdriver.support import expected_conditions as EC\nnavegador = webdriver.Chrome()\nnavegador.get("https://loja.exemplo/produtos")\n',
             sol='navegador.find_element(By.PARTIAL_LINK_TEXT, "Carrinho").click()\nel = WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.ID, "vazio")))\naviso = el.text',
             test='assert navegador.current_url == "https://loja.exemplo/carrinho", "Clique no link do carrinho (By.PARTIAL_LINK_TEXT)"\nassert aviso == "Seu carrinho está vazio", "Leia o texto do elemento retornado pela espera"\nassert 10 in navegador.esperas, "Use WebDriverWait(navegador, 10)"',
             h=["O localizador vai como tupla: (By.ID, \"vazio\")", "until(...) devolve o elemento encontrado"]),
        dict(t="Desafio: relatório de estoque", p="Na página de produtos, crie a lista <code>sem_estoque</code> com os nomes de produtos com estoque 0 e o dicionário <code>valor_estoque</code> <code>{nome: preço × estoque}</code> só dos que têm estoque. No fim, feche o navegador com <code>quit()</code>.",
             s=PAG_PRODUTOS + 'from selenium import webdriver\nfrom selenium.webdriver.common.by import By\nnavegador = webdriver.Chrome()\nnavegador.get("https://loja.exemplo/produtos")\n',
             sol='sem_estoque = []\nvalor_estoque = {}\nfor card in navegador.find_elements(By.CSS_SELECTOR, "div.produto"):\n    nome = card.find_element(By.CLASS_NAME, "nome").text\n    preco = float(card.find_element(By.CLASS_NAME, "preco").text)\n    qtd = int(card.find_element(By.CLASS_NAME, "estoque").text)\n    if qtd == 0:\n        sem_estoque.append(nome)\n    else:\n        valor_estoque[nome] = preco * qtd\nnavegador.quit()',
             test='assert sem_estoque == ["Mouse"], "Só o Mouse está sem estoque"\nassert valor_estoque == {"Notebook": 17500.0, "Teclado": 1800.0, "Monitor": 3600.0}, "valor = preço × estoque, só para estoque > 0"\nassert navegador.fechado, "Feche o navegador com navegador.quit()"',
             h=["Converta preço com float() e estoque com int()", "if qtd == 0 ... else ...; e navegador.quit() no final"]),
    ],
)
