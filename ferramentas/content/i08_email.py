ENV = 'import os\nos.environ["EMAIL_USUARIO"] = "relatorios@empresa.com"\nos.environ["EMAIL_SENHA"] = "senha-de-app-123"\n'
RAW = '''bruto = """From: Financeiro <financeiro@fornecedor.com>
To: compras@empresa.com
Subject: Nota fiscal 4521
Date: Mon, 16 Nov 2026 09:30:00 -0300
MIME-Version: 1.0
Content-Type: multipart/mixed; boundary="XYZ"

--XYZ
Content-Type: text/plain; charset="utf-8"

Segue a nota fiscal do pedido 4521. Valor: R$ 1.250,00.
--XYZ
Content-Type: text/csv; name="itens.csv"
Content-Disposition: attachment; filename="itens.csv"

produto,qtd
Papel A4,10
Toner,2
--XYZ--
"""
'''
TOPIC = dict(
    name="E-mails com Python", short="relatórios que se enviam sozinhos",
    cdesc="montar mensagens (texto, HTML, anexos), enviar por SMTP e ler e-mails recebidos",
    map="fluxo", src="Intermediário • Módulo 27",
    groups=[
        ["Formas de enviar", [["SMTP (smtplib)", "Gmail, Outlook.com e qualquer servidor"], ["Outlook (pywin32)", "usa o Outlook instalado no Windows"], ["APIs (SendGrid etc.)", "envio em massa e profissional"]]],
        ["Montar a mensagem", [["EmailMessage()", "objeto do e-mail"], ["msg[\"Subject\"], [\"From\"], [\"To\"]", "cabeçalhos"], ["set_content / add_alternative", "texto puro / versão HTML"]]],
        ["Anexos", [["add_attachment(bytes, ...)", "maintype, subtype, filename"], ["Ler o arquivo em \"rb\"", "anexo vai como bytes"], ["Imagem no corpo", "HTML com <img> + anexo"]]],
        ["Enviar (SMTP)", [["smtplib.SMTP(host, 587)", "conecta no servidor"], ["starttls() + login()", "criptografa e autentica"], ["send_message(msg) / quit()", "envia e encerra"]]],
        ["Segurança", [["Senha de app", "o Gmail exige senha de app, não a senha normal"], ["Variáveis de ambiente", "os.environ[\"EMAIL_SENHA\"]"], ["Nunca no código", "nem no GitHub"]]],
        ["Ler e-mails", [["imaplib / IMAP", "acessar a caixa de entrada"], ["email.message_from_string", "texto bruto → objeto"], ["walk() / get_filename()", "percorrer partes e achar anexos"]]],
    ],
    hot=[
        "Monte o e-mail com EmailMessage: cabeçalhos com msg[\"Subject\"] etc.",
        "Para HTML, use set_content (texto) + add_alternative(html, subtype=\"html\").",
        "Anexo: leia em modo \"rb\" e use add_attachment com maintype, subtype e filename.",
        "Gmail: porta 587 + starttls() + senha de app.",
        "Senha e usuário vêm de variáveis de ambiente, nunca escritos no código.",
    ],
    trap="Colocar a senha direto no código e subir para o GitHub expõe sua conta. Use os.environ (ou um arquivo .env fora do repositório).",
    examples=[["enviar_email.py", '''import os, smtplib
from email.message import EmailMessage

msg = EmailMessage()
msg["Subject"] = "Relatório de vendas"
msg["From"] = os.environ["EMAIL_USUARIO"]
msg["To"] = "chefe@empresa.com"
msg.set_content("Segue o relatório em anexo.")

with open("relatorio.csv", "rb") as f:
    msg.add_attachment(f.read(), maintype="text", subtype="csv", filename="relatorio.csv")

with smtplib.SMTP("smtp.gmail.com", 587) as servidor:
    servidor.starttls()
    servidor.login(os.environ["EMAIL_USUARIO"], os.environ["EMAIL_SENHA"])
    servidor.send_message(msg)'''], ["ler_email.py", '''import email
from email import policy

msg = email.message_from_string(texto_bruto, policy=policy.default)
print(msg["Subject"], msg["From"])
for parte in msg.walk():
    if parte.get_filename():
        print("Anexo:", parte.get_filename())''']],
    ex=[
        dict(t="Criar a mensagem", p="Crie <code>msg = EmailMessage()</code> com assunto <code>Relatório diário</code>, remetente <code>remetente</code>, destinatário <code>destino</code> e corpo <code>Bom dia! Segue o relatório.</code>.<br><small class='muted'>Nenhum e-mail sai daqui: o envio é simulado.</small>", s='remetente = "relatorios@empresa.com"\ndestino = "chefe@empresa.com"',
             sol='from email.message import EmailMessage\nmsg = EmailMessage()\nmsg["Subject"] = "Relatório diário"\nmsg["From"] = remetente\nmsg["To"] = destino\nmsg.set_content("Bom dia! Segue o relatório.")',
             test='assert msg["Subject"] == "Relatório diário"\nassert (msg["From"], msg["To"]) == (remetente, destino)\nassert msg.get_content().strip() == "Bom dia! Segue o relatório.", "Use msg.set_content(...)"',
             h=["from email.message import EmailMessage", "Cabeçalhos funcionam como dicionário: msg[\"Subject\"] = ..."]),
        dict(t="Vários destinatários", p="Crie a mensagem <code>msg</code> com assunto <code>Aviso</code>, corpo <code>Reunião às 10h</code> e envie para todos os e-mails da lista <code>equipe</code> no campo <code>To</code> (separados por <code>, </code>).", s='equipe = ["ana@x.com", "leo@x.com", "bia@x.com"]',
             sol='from email.message import EmailMessage\nmsg = EmailMessage()\nmsg["Subject"] = "Aviso"\nmsg["To"] = ", ".join(equipe)\nmsg.set_content("Reunião às 10h")',
             test='assert msg["To"] == "ana@x.com, leo@x.com, bia@x.com", "Use \\", \\".join(equipe)"\nassert msg["Subject"] == "Aviso"',
             h=["\", \".join(lista)", "msg[\"To\"] aceita vários endereços separados por vírgula"]),
        dict(t="Corpo com f-string", p="Monte <code>msg</code> com assunto <code>Faturamento</code> e corpo <code>O faturamento foi de R$ 12,345.60</code>, formatando <code>faturamento</code>.", s="faturamento = 12345.6",
             sol='from email.message import EmailMessage\nmsg = EmailMessage()\nmsg["Subject"] = "Faturamento"\nmsg.set_content(f"O faturamento foi de R$ {faturamento:,.2f}")',
             test='assert msg.get_content().strip() == "O faturamento foi de R$ 12,345.60"\nassert rodar(faturamento=10)["msg"].get_content().strip() == "O faturamento foi de R$ 10.00", "Use a variável"',
             h=["f\"... {faturamento:,.2f}\"", "msg.set_content(texto)"]),
        dict(t="Credenciais do ambiente", p="Leia o usuário e a senha das variáveis de ambiente <code>EMAIL_USUARIO</code> e <code>EMAIL_SENHA</code> em <code>usuario</code> e <code>senha</code>. <b>Não</b> escreva a senha no código.", s=ENV,
             sol='usuario = os.environ["EMAIL_USUARIO"]\nsenha = os.environ["EMAIL_SENHA"]',
             test='assert (usuario, senha) == ("relatorios@empresa.com", "senha-de-app-123")\nassert "senha-de-app-123" not in codigo, "A senha não pode estar escrita no código"',
             h=["os.environ[\"NOME\"]", "os.environ.get(\"NOME\") devolve None se não existir"]),
        dict(t="Enviar por SMTP", p="Envie <code>msg</code> (já pronta) pelo Gmail: <code>smtplib.SMTP(\"smtp.gmail.com\", 587)</code>, <code>starttls()</code>, <code>login</code> com as variáveis de ambiente e <code>send_message</code>. Feche com <code>quit()</code> (ou use <code>with</code>).", s=ENV + 'from email.message import EmailMessage\nmsg = EmailMessage()\nmsg["Subject"] = "Teste"\nmsg["To"] = "chefe@empresa.com"\nmsg.set_content("ok")\n',
             sol='import smtplib\nservidor = smtplib.SMTP("smtp.gmail.com", 587)\nservidor.starttls()\nservidor.login(os.environ["EMAIL_USUARIO"], os.environ["EMAIL_SENHA"])\nservidor.send_message(msg)\nservidor.quit()',
             test='env = _smtp.ENVIADOS\nassert len(env) == 1, "Chame send_message(msg) uma vez"\ns = env[0]["servidor"]\nassert (s.host, s.port) == ("smtp.gmail.com", 587), "smtplib.SMTP(\\"smtp.gmail.com\\", 587)"\nassert s.tls, "Chame starttls() antes do login"\nassert s.senha == "senha-de-app-123" and "senha-de-app-123" not in codigo, "Faça login com os.environ[\\"EMAIL_SENHA\\"]"\nassert s.fechado, "Feche a conexão com quit() ou use with"',
             h=["Sequência: SMTP(...) → starttls() → login(...) → send_message(msg)", "with smtplib.SMTP(...) as servidor: fecha sozinho"]),
        dict(t="Versão em HTML", p="Crie <code>msg</code> com assunto <code>Promoção</code>, texto puro <code>Veja nossas ofertas</code> e uma versão HTML <code>&lt;h1&gt;Ofertas&lt;/h1&gt;</code> com <code>add_alternative(..., subtype=\"html\")</code>.", s="",
             sol='from email.message import EmailMessage\nmsg = EmailMessage()\nmsg["Subject"] = "Promoção"\nmsg.set_content("Veja nossas ofertas")\nmsg.add_alternative("<h1>Ofertas</h1>", subtype="html")',
             test='assert msg.get_content_type() == "multipart/alternative", "Use set_content e depois add_alternative"\ntipos = [p.get_content_type() for p in msg.iter_parts()]\nassert tipos == ["text/plain", "text/html"]\nassert "<h1>Ofertas</h1>" in msg.get_body(("html",)).get_content()',
             h=["Primeiro set_content (texto), depois add_alternative (HTML)", "subtype=\"html\""]),
        dict(t="Anexar arquivo", p="O arquivo <code>vendas.csv</code> existe na pasta. Crie <code>msg</code> com assunto <code>Vendas</code>, corpo <code>Segue anexo</code> e anexe o arquivo (leia em <code>\"rb\"</code>, <code>maintype=\"text\"</code>, <code>subtype=\"csv\"</code>, <code>filename=\"vendas.csv\"</code>).", s='with open("vendas.csv", "w") as f:\n    f.write("produto,valor\\nCafé,10\\n")',
             sol='from email.message import EmailMessage\nmsg = EmailMessage()\nmsg["Subject"] = "Vendas"\nmsg.set_content("Segue anexo")\nwith open("vendas.csv", "rb") as f:\n    msg.add_attachment(f.read(), maintype="text", subtype="csv", filename="vendas.csv")',
             test='anexos = list(msg.iter_attachments())\nassert len(anexos) == 1, "Use msg.add_attachment(...)"\nassert anexos[0].get_filename() == "vendas.csv"\nassert "Café,10" in anexos[0].get_payload(decode=True).decode("utf-8"), "Anexe o conteúdo do arquivo"',
             h=["Leia como bytes: open(..., \"rb\")", "add_attachment(dados, maintype=..., subtype=..., filename=...)"]),
        dict(t="Ler um e-mail recebido", p="<code>bruto</code> é o texto de um e-mail recebido. Converta com <code>email.message_from_string(bruto, policy=policy.default)</code> e guarde em <code>assunto</code> e <code>remetente</code> o assunto e o endereço do remetente (só o e-mail).", s=RAW,
             sol='import email\nfrom email import policy\nfrom email.utils import parseaddr\nmsg = email.message_from_string(bruto, policy=policy.default)\nassunto = msg["Subject"]\nremetente = parseaddr(msg["From"])[1]',
             test='assert assunto == "Nota fiscal 4521"\nassert remetente == "financeiro@fornecedor.com", "Só o endereço: use email.utils.parseaddr"',
             h=["msg[\"Subject\"] e msg[\"From\"]", "parseaddr(\"Nome <a@b.com>\") devolve (\"Nome\", \"a@b.com\")"]),
        dict(t="Extrair anexos", p="Do e-mail em <code>bruto</code>, encontre os anexos e salve cada um na pasta atual com o nome original. Guarde os nomes salvos na lista <code>salvos</code>.", s=RAW,
             sol='import email\nfrom email import policy\nmsg = email.message_from_string(bruto, policy=policy.default)\nsalvos = []\nfor parte in msg.iter_attachments():\n    nome = parte.get_filename()\n    with open(nome, "wb") as f:\n        f.write(parte.get_payload(decode=True))\n    salvos.append(nome)',
             test='assert salvos == ["itens.csv"]\nassert open("itens.csv", encoding="utf-8").read().splitlines()[:2] == ["produto,qtd", "Papel A4,10"], "Grave o conteúdo do anexo"',
             h=["msg.iter_attachments() percorre só os anexos", "parte.get_payload(decode=True) devolve os bytes"]),
        dict(t="Extrair valor do corpo", p="Do e-mail em <code>bruto</code>, leia o texto do corpo (<code>msg.get_body((\"plain\",)).get_content()</code>) e extraia o valor em reais como <code>float</code> em <code>valor</code> (R$ 1.250,00 → 1250.0).", s=RAW,
             sol='import email, re\nfrom email import policy\nmsg = email.message_from_string(bruto, policy=policy.default)\ncorpo = msg.get_body(("plain",)).get_content()\ntexto = re.search(r"R\\$ ([\\d.,]+\\d)", corpo).group(1)\nvalor = float(texto.replace(".", "").replace(",", "."))',
             test='assert valor == 1250.0, "Troque . de milhar por nada e , decimal por ."',
             h=["Encontre o trecho depois de \"R$ \" (com split ou re)", "\"1.250,00\".replace(\".\", \"\").replace(\",\", \".\")"]),
        dict(t="Função de envio", p="Crie <code>enviar(destino, assunto, corpo)</code> que monta a mensagem (From = <code>EMAIL_USUARIO</code>) e envia por <code>smtplib.SMTP(\"smtp.gmail.com\", 587)</code> com <code>starttls</code> e login pelas variáveis de ambiente. Depois chame <code>enviar(\"ana@x.com\", \"Oi\", \"Teste\")</code>.", s=ENV,
             sol='import smtplib\nfrom email.message import EmailMessage\n\ndef enviar(destino, assunto, corpo):\n    msg = EmailMessage()\n    msg["Subject"] = assunto\n    msg["From"] = os.environ["EMAIL_USUARIO"]\n    msg["To"] = destino\n    msg.set_content(corpo)\n    with smtplib.SMTP("smtp.gmail.com", 587) as servidor:\n        servidor.starttls()\n        servidor.login(os.environ["EMAIL_USUARIO"], os.environ["EMAIL_SENHA"])\n        servidor.send_message(msg)\n\nenviar("ana@x.com", "Oi", "Teste")',
             test='e = _smtp.ENVIADOS\nassert len(e) == 1, "Chame enviar(...) uma vez"\nm = e[0]["msg"]\nassert (m["To"], m["Subject"], m["From"]) == ("ana@x.com", "Oi", "relatorios@empresa.com")\nassert e[0]["servidor"].tls and e[0]["servidor"].fechado\nenviar("leo@x.com", "A", "B")\nassert _smtp.ENVIADOS[-1]["msg"]["To"] == "leo@x.com", "Use o parâmetro destino"\nassert "senha-de-app-123" not in codigo',
             h=["Monte a mensagem dentro da função", "with smtplib.SMTP(...) as servidor:"]),
        dict(t="E-mail personalizado em massa", p="Para cada cliente de <code>clientes</code> (lista de dicts com <code>nome</code>, <code>email</code> e <code>valor</code>), envie um e-mail com assunto <code>Sua fatura</code> e corpo <code>Olá, NOME! Sua fatura é de R$ VALOR.</code> (valor com 2 casas). Use <b>uma</b> conexão SMTP para todos.", s=ENV + 'clientes = [{"nome": "Ana", "email": "ana@x.com", "valor": 150}, {"nome": "Leo", "email": "leo@x.com", "valor": 89.9}]\n',
             sol='import smtplib\nfrom email.message import EmailMessage\nwith smtplib.SMTP("smtp.gmail.com", 587) as servidor:\n    servidor.starttls()\n    servidor.login(os.environ["EMAIL_USUARIO"], os.environ["EMAIL_SENHA"])\n    for c in clientes:\n        msg = EmailMessage()\n        msg["Subject"] = "Sua fatura"\n        msg["From"] = os.environ["EMAIL_USUARIO"]\n        msg["To"] = c["email"]\n        msg.set_content(f"Olá, {c[\'nome\']}! Sua fatura é de R$ {c[\'valor\']:.2f}.")\n        servidor.send_message(msg)',
             test='e = _smtp.ENVIADOS\nassert [x["msg"]["To"] for x in e] == ["ana@x.com", "leo@x.com"], "Um e-mail por cliente"\nassert e[1]["msg"].get_content().strip() == "Olá, Leo! Sua fatura é de R$ 89.90."\nassert e[0]["servidor"] is e[1]["servidor"], "Use a mesma conexão SMTP para todos (abra antes do for)"',
             h=["Abra a conexão antes do for e envie dentro dele", "Crie uma EmailMessage nova a cada cliente"]),
        dict(t="Imagem no corpo do e-mail", p="Crie <code>msg</code> com texto <code>Veja o gráfico</code> e versão HTML contendo <code>&lt;img src=\"cid:grafico\"&gt;</code>. Anexe <code>grafico.png</code> à parte HTML com <code>add_related(..., maintype=\"image\", subtype=\"png\", cid=\"&lt;grafico&gt;\")</code>.", s='with open("grafico.png", "wb") as f:\n    f.write(b"\\x89PNG\\r\\n\\x1a\\nfake")',
             sol='from email.message import EmailMessage\nmsg = EmailMessage()\nmsg["Subject"] = "Gráfico"\nmsg.set_content("Veja o gráfico")\nmsg.add_alternative(\'<p>Vendas:</p><img src="cid:grafico">\', subtype="html")\nwith open("grafico.png", "rb") as f:\n    msg.get_payload()[1].add_related(f.read(), maintype="image", subtype="png", cid="<grafico>")',
             test='html = msg.get_body(("related",))\nassert html is not None, "Use add_related na parte HTML"\npartes = [p.get_content_type() for p in html.iter_parts()]\nassert partes == ["text/html", "image/png"], "A imagem fica junto do HTML (multipart/related)"\nassert "cid:grafico" in html.get_body(("html",)).get_content()\nassert [p for p in html.iter_parts()][1]["Content-ID"] == "<grafico>"',
             h=["A parte HTML é msg.get_payload()[1] depois do add_alternative", "No HTML use src=\"cid:grafico\" e no anexo cid=\"<grafico>\""]),
        dict(t="Filtrar caixa de entrada", p="<code>caixa</code> é uma lista de e-mails brutos. Crie <code>notas</code>: lista com o <b>assunto</b> dos e-mails cujo assunto contém <code>Nota fiscal</code> e que têm pelo menos um anexo.", s=RAW + 'simples = "From: a@b.com\\nSubject: Nota fiscal 9\\n\\nsem anexo"\noutro = bruto.replace("Nota fiscal 4521", "Boleto 77")\ncaixa = [bruto, simples, outro]\n',
             sol='import email\nfrom email import policy\nnotas = []\nfor texto in caixa:\n    m = email.message_from_string(texto, policy=policy.default)\n    if "Nota fiscal" in m["Subject"] and list(m.iter_attachments()):\n        notas.append(m["Subject"])',
             test='assert notas == ["Nota fiscal 4521"], "Só a nota fiscal COM anexo"',
             h=["Converta cada texto com message_from_string", "list(m.iter_attachments()) vazia = sem anexo"]),
        dict(t="Desafio: relatório automático", p="Calcule a partir de <code>vendas</code> (dict loja → valor) o <code>total</code>, gere <code>resumo.csv</code> (<code>loja,valor</code>), monte a mensagem para <code>destino</code> com assunto <code>Resumo de vendas</code>, corpo <code>Total: R$ X</code> (2 casas, milhar com vírgula) e o CSV anexado, e envie pelo SMTP do Gmail com credenciais do ambiente.", s=ENV + 'vendas = {"Recife": 15200.5, "Olinda": 8300, "Caruaru": 4999.5}\ndestino = "diretoria@empresa.com"\n',
             sol='import csv, smtplib\nfrom email.message import EmailMessage\ntotal = sum(vendas.values())\nwith open("resumo.csv", "w", newline="", encoding="utf-8") as f:\n    w = csv.writer(f)\n    w.writerow(["loja", "valor"])\n    w.writerows(vendas.items())\nmsg = EmailMessage()\nmsg["Subject"] = "Resumo de vendas"\nmsg["From"] = os.environ["EMAIL_USUARIO"]\nmsg["To"] = destino\nmsg.set_content(f"Total: R$ {total:,.2f}")\nwith open("resumo.csv", "rb") as f:\n    msg.add_attachment(f.read(), maintype="text", subtype="csv", filename="resumo.csv")\nwith smtplib.SMTP("smtp.gmail.com", 587) as s:\n    s.starttls()\n    s.login(os.environ["EMAIL_USUARIO"], os.environ["EMAIL_SENHA"])\n    s.send_message(msg)',
             test='assert total == 28500.0\ne = _smtp.ENVIADOS\nassert len(e) == 1, "Envie uma mensagem"\nm = e[0]["msg"]\nassert m["To"] == destino and m["Subject"] == "Resumo de vendas"\nassert m.get_body(("plain",)).get_content().strip() == "Total: R$ 28,500.00"\na = list(m.iter_attachments())\nassert len(a) == 1 and a[0].get_filename() == "resumo.csv"\nassert a[0].get_payload(decode=True).decode("utf-8").splitlines()[:2] == ["loja,valor", "Recife,15200.5"]\nassert e[0]["servidor"].tls and "senha-de-app-123" not in codigo',
             h=["Etapas: calcular → gravar CSV → montar mensagem → anexar → enviar", "Reaproveite o que fez nos exercícios anteriores"]),
    ],
)
