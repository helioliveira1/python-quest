# Python Quest: sistema de estudo de Python

Painel com 3 módulos (**Fundamentos**, **Básico** e **Intermediário**), **26 fases** e **390 exercícios** corrigidos automaticamente com Python de verdade rodando no navegador ([Pyodide](https://pyodide.org)).

Cada fase tem:
- **Mapa mental interativo** em 6 formatos (radial, árvore, chaves, bolhas, fluxograma e comparação) com **modo memória**: as descrições ficam escondidas e você toca para revelar (+10 XP ao revelar tudo).
- **Quiz relâmpago**, gerado a partir do mapa (+15 XP com 5 acertos ou mais em 6).
- **Flashcards**.
- **15 exercícios** (5 fáceis, 5 médios e 5 desafios), com editor, dicas progressivas e solução de referência liberada só depois da 1ª tentativa.
- Gamificação: XP, níveis, estrelas, conquistas, sequência de dias, "próximo recomendado" e "revisar erros".

## Estrutura

```
index.html              ← o sistema (abre o painel)
assets/app.js           ← lógica: rotas, mapas, quiz, flashcards, exercícios, motor Python
assets/app.css          ← visual (paleta azul/areia)
assets/harness.js       ← código Python que roda os testes (gerado a partir de ferramentas/harness.py)
data/fundamentos.js     ← conteúdo de cada módulo (mapas + exercícios)
data/basico.js
data/intermediario.js
vendor/codemirror.*     ← editor de código (funciona offline)
sw.js, manifest.webmanifest ← funcionamento offline e "instalar app" no celular
ferramentas/            ← fontes do conteúdo + scripts para gerar e validar
```

O progresso fica no `localStorage` do navegador (funciona offline) e, quando você entra com sua conta (botão **☁️ Entrar** no topo), é sincronizado na nuvem pelo **Supabase**. Ao entrar em outro aparelho, os dois progressos são **mesclados**: vale o melhor resultado de cada exercício, e o XP é recalculado.

## Sincronização (Supabase)

- Projeto Supabase: `python-quest` (região São Paulo). Tabela `public.progresso` (uma linha por usuário, `dados jsonb`) com **RLS**: cada usuário só lê e grava a própria linha.
- `assets/config.js` tem a URL do projeto e a **chave publicável** (feita para ficar no navegador; a segurança vem do RLS). Para desligar a sincronização, deixe `SUPABASE_URL` vazio.
- `assets/sync.js`: login (e-mail e senha), envio automático 2,5 s depois de cada mudança, busca ao voltar para a aba e mesclagem.
- `vendor/supabase.js`: biblioteca oficial `@supabase/supabase-js` 2.118.0 (MIT), servida pelo próprio site.

**Configuração única no painel do Supabase** (Authentication › URL Configuration):
- **Site URL:** `https://helioliveira1.github.io/python-quest/`
- **Redirect URLs:** adicione `https://helioliveira1.github.io/python-quest/**` (e `http://localhost:8000/**` se for testar localmente).

Sem isso, os links de confirmação de cadastro e de "esqueci a senha" apontam para `localhost:3000`. Se quiser cadastro sem e-mail de confirmação, desligue **Authentication › Sign In / Providers › Email › Confirm email**.

> No plano gratuito, o Supabase pausa o projeto depois de 7 dias sem uso. Se a sincronização parar, reative em supabase.com/dashboard (o progresso local continua funcionando).

## Abrir no computador

- **Com dois cliques:** abra o `index.html`. Tudo funciona; só o modo offline (service worker) não é ativado em `file://`.
- **Como site local (recomendado para testar):** na pasta do projeto, rode
  ```
  python -m http.server 8000
  ```
  e acesse `http://localhost:8000`.

Na 1ª execução de código o navegador baixa o Python (cerca de 10 MB) e, nas fases que precisam, numpy, pandas, matplotlib, bs4, sqlite3 ou seaborn. Depois disso fica em cache.

## Publicar no GitHub Pages

1. Crie um repositório no GitHub (ex.: `python-quest`), público.
2. Na pasta do projeto:
   ```
   git init
   git add .
   git commit -m "Python Quest: sistema de estudo"
   git branch -M main
   git remote add origin https://github.com/SEU_USUARIO/python-quest.git
   git push -u origin main
   ```
3. No GitHub: **Settings › Pages › Build and deployment › Source: Deploy from a branch › Branch: `main` / `(root)` › Save**.
4. Em 1 ou 2 minutos o site fica em `https://SEU_USUARIO.github.io/python-quest/`.
5. No celular, abra o link e use **"Adicionar à tela inicial"**: vira um app que funciona offline depois da 1ª visita.

O arquivo `.nojekyll` já está incluído (evita processamento extra do GitHub Pages).

> Ao publicar uma nova versão, troque `VERSAO` em `sw.js` (ex.: `pyquest-v2`) para os aparelhos receberem a atualização.

## Como editar ou criar exercícios

O conteúdo fica em `ferramentas/`:
- `content/*.py`: as **12 fases novas** (uma por arquivo, no formato `TOPIC = dict(...)`).
- `fases_reaproveitadas.json`: as **14 fases** que vieram do `Python_Quest_Mapa_Mental.html` original (validadas e mantidas). Os ajustes aplicados a elas estão em `build.py`.
- `harness.py`: o executor Python (testes, simuladores de Selenium e SMTP, captura de gráficos).

Formato de um exercício:
```python
dict(
    t="Título",
    p="Enunciado em HTML (use <code>variavel</code>)",
    s="código que roda ANTES do aluno (dados prontos)",
    sol="solução de referência",
    test='assert resultado == 10, "mensagem que o aluno vê"\nassert rodar(x=5)["resultado"] == 7, "testa com outros valores"',
    h=["dica 1", "dica 2"],
)
```
Nos testes ficam disponíveis: as variáveis do aluno, `saida` (tudo o que ele imprimiu), `rodar(**novos_valores)` (roda de novo trocando dados), `codigo` (texto do código), `_smtp.ENVIADOS` (e-mails simulados) e `_nav` (navegadores simulados).

Depois de editar:
```
cd ferramentas
python build.py                      # gera data/*.js e assets/harness.js
python validate.py all_topics.json   # roda TODAS as soluções e confere que o editor vazio falha
```
Para validar as fases com pacotes, instale as mesmas versões do Pyodide 0.27.2:
`pip install numpy==2.0.2 pandas==2.2.3 matplotlib==3.8.4 beautifulsoup4==4.12.3 seaborn==0.13.2`.

## Limites (transparência)

- **Selenium** (fase 10 do Intermediário) roda num **simulador** feito para o navegador: suporta `By.ID/NAME/CLASS_NAME/TAG_NAME/CSS_SELECTOR/XPATH/LINK_TEXT`, `send_keys`, `click`, `Select`, `iframe`, `WebDriverWait`. O código é o mesmo que você usará no seu PC, mas o simulador não executa JavaScript da página nem cobre todos os recursos de XPath/CSS.
- **E-mail**: o `smtplib.SMTP` é **simulado** (nada é enviado). Montagem de mensagens, anexos e leitura de e-mails usam o módulo `email` real.
- **SQL**: usa **SQLite** no navegador. A API (`cursor.execute` com `?`, `commit`, `fetchall`) é a mesma do `pyodbc` com SQL Server; recursos exclusivos do T-SQL não são testados aqui.
- **PDF** (Módulo 25) e **requests/APIs reais**: não rodam no navegador. Estão no mapa mental com exemplos para executar no seu PC; os exercícios cobrem arquivos de texto/CSV e respostas JSON.
- Os **Módulos 1 e 2** dos PDFs (introdução e instalação) não viraram fases, porque não têm conteúdo de código para exercitar.
- **Seaborn** é instalado sob demanda via `micropip` (precisa de internet na 1ª vez).
- Os exercícios são **autorais**, baseados nos temas das apostilas.
