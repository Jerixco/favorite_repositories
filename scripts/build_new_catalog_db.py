# -*- coding: utf-8 -*-
"""
Dicionário Completo de Análise Técnica de Alta Fidelidade (100% PT-BR)
Para todos os 118 Repositórios Estrelados do Jerixco
"""

import json

CATALOG_DB = {
    "scrapy/scrapy": {
        "what": "Framework open-source líder em Python para extração de dados (web scraping) e rastreamento web em larga escala. Projetado com arquitetura assíncrona baseada em Twisted, permite extrair dados de milhares de páginas por minuto com pipelines estruturados.",
        "use_cases": "Coleta massiva de dados de e-commerce e preços; mineração de dados para treinamento de modelos de IA; monitoramento automatizado de notícias e vagas de emprego.",
        "quickstart": """```bash
pip install scrapy
scrapy startproject meu_crawler
cd meu_crawler
scrapy genspider quotes quotes.toscrape.com
scrapy crawl quotes -o quotes.json
```""",
        "pro_tip": "Ajuste `CONCURRENT_REQUESTS = 32` e utilize `DOWNLOAD_DELAY` com `AutoThrottle` habilitado no `settings.py` para maximizar a velocidade de raspagem sem tomar ban de IP."
    },
    "memvid/memvid": {
        "what": "Motor de processamento e indexação de vídeo de altíssima performance escrito em Rust. Permite fatiar, indexar semanticamente e recuperar trechos de vídeo com latência ultra-baixa.",
        "use_cases": "Busca semântica em acervos de vídeo (ex: 'encontre o momento onde o palestrante fala sobre arquitetura de dados'); corte automatizado de melhores momentos para redes sociais.",
        "quickstart": """```bash
git clone https://github.com/memvid/memvid.git
cd memvid
cargo build --release
./target/release/memvid index --video entrada.mp4 --output index.bin
```""",
        "pro_tip": "Ative a flag `--features hardware-accel` na compilação do Rust para utilizar aceleração NVENC/VAAPI da placa de vídeo na extração de frames."
    },
    "FalkorDB/code-graph": {
        "what": "Ferramenta de engenharia de contexto em Python que converte código-fonte de repositórios em grafos de conhecimento navegáveis usando o banco de dados em memória FalkorDB.",
        "use_cases": "Análise de dependências complexas em monorepos; alimentação de agentes de IA com GraphRAG sobre a arquitetura do código; visualização de chamadas de funções e classes.",
        "quickstart": """```bash
docker run -p 6379:6379 -d --name falkordb -v falkor_data:/data falkordb/falkordb:latest
pip install code-graph
code-graph index --repo-path ./meu-projeto --db-host localhost:6379
```""",
        "pro_tip": "Combine queries em Cypher no FalkorDB com agentes de IA para fazer perguntas arquiteturais como: 'quais métodos chamam a função de autenticação sem passar pelo middleware de autorização?'"
    },
    "open-webui/open-webui": {
        "what": "A interface web auto-hospedável mais completa e elegante para modelos de linguagem (LLMs). Funciona como um ChatGPT privado com suporte nativo a Ollama, OpenAI, Claude, RAG com documentos, plugins Python e chamadas de voz.",
        "use_cases": "Interface central de IA para equipes e empresas; assistente pessoal local rodando 100% offline com Ollama; ambiente de teste para múltiplos modelos e provedores.",
        "quickstart": """```bash
docker run -d -p 3000:8080 -v open-webui:/app/backend/data --name open-webui --restart always ghcr.io/open-webui/open-webui:main
# Acesse http://localhost:3000
```""",
        "pro_tip": "Conecte sua instância do Ollama passando `-e OLLAMA_BASE_URL=http://host.docker.internal:11434` no comando Docker para usar seus modelos locais sem nenhuma configuração extra."
    },
    "petergyang/no-ai-slop": {
        "what": "Utilitário em Python para detecção e remoção de clichês, jargões artificiais e vícios de linguagem típicos de textos gerados por IA ('AI slop'), tornando a escrita mais natural e humana.",
        "use_cases": "Revisão e humanização de artigos, posts do LinkedIn, documentações técnicas e emails gerados por ChatGPT/Claude antes da publicação.",
        "quickstart": """```bash
pip install no-ai-slop
no-ai-slop clean --input artigo.md --output artigo_humanizado.md
```""",
        "pro_tip": "Crie um hook de pre-commit no Git para rodar o utilitário nos arquivos de documentação markdown e manter o tom técnico e direto sem enrolações."
    },
    "opendataloader-project/opendataloader-pdf": {
        "what": "Parser de PDF empresarial e de alta performance em Java/JVM. Converte PDFs complexos com tabelas, formulários e colunas em JSON e Markdown estruturados para pipelines de RAG e IA.",
        "use_cases": "Extração estruturada de dados de faturas, contratos, extratos bancários e relatórios corporativos para bancos vetoriais de IA.",
        "quickstart": """```bash
git clone https://github.com/opendataloader-project/opendataloader-pdf.git
cd opendataloader-pdf
./gradlew build
java -jar build/libs/opendataloader-pdf.jar --input relatorio.pdf --format markdown
```""",
        "pro_tip": "Ative o modo `--enable-table-detection` para que tabelas com células mescladas sejam convertidas em formato Markdown tabular perfeitamente alinhado."
    },
    "microsoft/data-formulator": {
        "what": "Ferramenta de pesquisa da Microsoft que combina interação gráfica com IA para transformar, limpar e visualizar dados tabulares complexos iterativamente.",
        "use_cases": "Exploração e preparação de dados para cientistas de dados e analistas de BI; geração automatizada de gráficos Vega-Lite a partir de comandos em linguagem natural.",
        "quickstart": """```bash
pip install data-formulator
data-formulator --port 5000
# Acesse http://localhost:5000 no navegador
```""",
        "pro_tip": "Ideal para transformar dados em formato 'wide' para 'long' (unpivot) apenas descrevendo o formato final desejado em vez de escrever transformações manuais complexas em Pandas."
    },
    "microsoft/BitNet": {
        "what": "Implementação oficial da Microsoft da arquitetura 1-bit LLM (BitNet b1.58). Reduz os pesos do modelo para apenas 3 valores (-1, 0, 1), permitindo inferência ultra-rápida em CPUs comuns com consumo mínimo de memória.",
        "use_cases": "Executar modelos de IA em dispositivos de borda (Raspberry Pi, celulares, notebooks sem placa de vídeo dedicada) com velocidade altíssima e consumo de energia quase nulo.",
        "quickstart": """```bash
git clone --recursive https://github.com/microsoft/BitNet.git
cd BitNet
python -m venv venv
venv\\Scripts\\activate
pip install -r requirements.txt
python setup_env.py --hf-repo HF1BitLLM/Llama3-8B-1.58-100B-tokens -q i2_s
```""",
        "pro_tip": "Use a quantização de ativações `i2_s` para obter taxas de geração acima de 20 tokens por segundo rodando em um processador Intel/AMD comum."
    },
    "mem0ai/mem0": {
        "what": "Camada de memória universal e inteligente para agentes e assistentes de IA (conhecida como 'The Memory Layer for AI'). Lembra preferências, histórico de conversas e fatos sobre o usuário entre diferentes sessões.",
        "use_cases": "Assistentes virtuais personalizados; sistemas de suporte ao cliente com memória histórica de chamados; agentes autônomos que aprendem com feedbacks anteriores.",
        "quickstart": """```bash
pip install mem0ai
# No código Python:
# from mem0 import Memory
# m = Memory()
# m.add("O usuário prefere respostas em Python e mora em Brasília", user_id="matheus")
# rel = m.search("Qual linguagem o usuário programa?", user_id="matheus")
```""",
        "pro_tip": "Configure o backend do Mem0 com PostgreSQL + pgvector ou Qdrant para persistência em larga escala com múltiplos usuários concorrentes."
    },
    "Kritt-ai/open-kritt": {
        "what": "Plataforma open-source em JavaScript para orquestração e execução de agentes de IA locais e descentralizados com foco em automação de tarefas de desenvolvimento.",
        "use_cases": "Automação de workflows de código em equipe; orquestração de micro-tarefas com agentes locais.",
        "quickstart": """```bash
git clone https://github.com/Kritt-ai/open-kritt.git
cd open-kritt
npm install
npm run dev
```""",
        "pro_tip": "Conecte os webhooks do Kritt com o GitHub para automatizar testes e triagem de pull requests recém-abertos."
    },
    "opensandbox-group/OpenSandbox": {
        "what": "Runtime de sandbox e isolamento seguro em C/Linux para execução de código gerado por agentes de IA de forma controlada, prevenindo danos ao sistema operacional hospedeiro.",
        "use_cases": "Ambiente de execução segura para agentes autônomos (Claude Code, OpenHands) executarem comandos bash, Python e scripts de teste sem risco de invasão ou corrupção.",
        "quickstart": """```bash
git clone https://github.com/opensandbox-group/OpenSandbox.git
cd OpenSandbox
make
sudo ./opensandbox --rootfs /var/sandboxes/ubuntu --exec "python3 main.py"
```""",
        "pro_tip": "Configure limites rígidos de cgroups (CPU, RAM e limite de processos) para evitar ataques de Denial of Service (DoS) por loops infinitos de agentes."
    },
    "jamiepine/voicebox": {
        "what": "Estúdio de voz open-source de ponta construído em TypeScript/React. Permite ditado por voz ultrarrápido, clonagem de voz, transcrição de áudio e integração com múltiplos modelos de fala.",
        "use_cases": "Ditado profissional para programação sem as mãos; geração de áudio realista para vídeos e podcasts; acessibilidade para desenvolvedores.",
        "quickstart": """```bash
git clone https://github.com/jamiepine/voicebox.git
cd voicebox
npm install
npm run dev
# Acesse a interface web do Voicebox no navegador
```""",
        "pro_tip": "Combine o modelo Whisper local do Voicebox com atalhos globais do teclado para transcrever áudio diretamente no seu editor de código."
    },
    "averygan/reclip": {
        "what": "Ferramenta leve e auto-hospedável para captura, recorte e download de trechos de vídeos online de plataformas como YouTube e Twitch com interface web limpa.",
        "use_cases": "Criação de cortes rápidos para redes sociais; extração de demonstrações de palestras e aulas para bases de dados de estudo.",
        "quickstart": """```bash
git clone https://github.com/averygan/reclip.git
cd reclip
# Execute com Docker ou servidor web local
```""",
        "pro_tip": "Defina timestamps de início e fim diretamente na URL para automatizar cortes em lote via scripts."
    },
    "coreyhaines31/makerskills": {
        "what": "Coleção prática de habilidades (skills) e prompts estruturados para criadores e desenvolvedores 'makers' utilizarem com Claude Code e assistentes de IA em projetos bootstrap.",
        "use_cases": "Acelerar o lançamento de produtos SaaS; criar landing pages de alta conversão; definir propostas de valor e estruturas de monetização com auxílio de IA.",
        "quickstart": """```bash
# Adicione a pasta de skills ao seu projeto ou importe no Claude Code:
claude skill add coreyhaines31/makerskills
```""",
        "pro_tip": "Use a skill `landing-page-audit` antes de publicar seu site para receber um relatório instantâneo de clareza de proposta e conversão."
    },
    "cursor/plugins": {
        "what": "Repositório oficial de plugins, extensões e integrações para o editor Cursor, permitindo conectar o assistente a bases de dados, documentações e ferramentas externas.",
        "use_cases": "Expandir o editor Cursor com superpoderes: adicionar conectores para bancos internos, pipelines de CI/CD e linter customizado.",
        "quickstart": """```bash
# Explore o catálogo de plugins e instale diretamente no Cursor via Command Palette (Ctrl+Shift+P > Plugins: Install)
```""",
        "pro_tip": "Mantenha o plugin de documentação `@docs` configurado com a URL oficial das bibliotecas que você mais usa para que o Cursor gere código 100% atualizado."
    },
    "google-gemini/cookbook": {
        "what": "Repositório oficial de receitas práticas, tutoriais e códigos de exemplo da Google para a API Gemini (Gemini 2.0 Flash, Pro, Multimodal, Function Calling, Embeddings).",
        "use_cases": "Aprender a implementar recursos avançados da API Gemini: processamento de vídeos de 1 hora, análise de áudio em tempo real, chamada estruturada de funções (JSON schema) e busca semântica.",
        "quickstart": """```bash
git clone https://github.com/google-gemini/cookbook.git
cd cookbook
pip install -r requirements.txt
jupyter notebook
```""",
        "pro_tip": "Consulte o notebook `structured_outputs.ipynb` para aprender a forçar o Gemini a responder exatamente no schema Pydantic/JSON da sua API."
    },
    "openai/openai-agents-python": {
        "what": "SDK oficial da OpenAI em Python para construção de agentes autônomos multi-etapas com chamada de ferramentas, transferências entre agentes (handoffs) e guardrails.",
        "use_cases": "Criar agentes complexos que resolvem tarefas de ponta a ponta (ex: agente de suporte que transfere a conversa para o agente de faturamento).",
        "quickstart": """```bash
pip install openai-agents
# No seu código:
# from agents import Agent, Runner
# agent = Agent(name="Assistente", instructions="Você é um assistente útil.")
# result = Runner.run_sync(agent, "Olá!")
```""",
        "pro_tip": "Use o padrão de 'Handoff' para dividir um problema gigante em pequenos agentes especialistas (ex: Agente de Triagem -> Agente SQL -> Agente de Email)."
    },
    "xai-org/grok-build": {
        "what": "Sistema de build e compilação de alta performance em Rust desenvolvido para os projetos e infraestruturas do ecossistema xAI/Grok.",
        "use_cases": "Automação de compilações complexas em monorepos de Rust; otimização de binários com Link-Time Optimization (LTO) e geração de artefatos de IA.",
        "quickstart": """```bash
git clone https://github.com/xai-org/grok-build.git
cd grok-build
cargo build --release
```""",
        "pro_tip": "Configure `codegen-units = 1` e `lto = 'fat'` no `Cargo.toml` para obter binários de Rust com máxima performance de execução."
    },
    "anthropics/claude-cookbooks": {
        "what": "Repositório oficial de guias, receitas e arquiteturas de referência da Anthropic para desenvolvimento profissional com a família Claude 3.5 e 3.7 (Sonnet, Haiku, Opus).",
        "use_cases": "Dominar técnicas avançadas como Prompt Caching (redução de 90% no custo), Tool Calling, Extended Thinking, RAG com documentos gigantes e visão computacional.",
        "quickstart": """```bash
git clone https://github.com/anthropics/claude-cookbooks.git
cd claude-cookbooks
pip install -r requirements.txt
jupyter notebook
```""",
        "pro_tip": "Implemente o `Prompt Caching` da Anthropic em seus agentes para pagar apenas 10% do valor dos tokens em prompts de sistema longos e repetitivos."
    },
    "FSECDEV/LEAKSFORUMS": {
        "what": "Repositório de pesquisa em cibersegurança focado em inteligência de ameaças (Threat Intelligence), monitoramento de vazamentos de credenciais e análise de superfícies de ataque.",
        "use_cases": "Identificação proativa de credenciais corporativas expostas na dark web; pesquisa em segurança defensiva e auditoria de vazamentos.",
        "quickstart": """```bash
# Consulte as regras e scripts de análise no repositório em ambiente isolado.
```""",
        "pro_tip": "Combine listas de vazamentos com ferramentas como Gitleaks para checar se algum colaborador comitou credenciais presentes em bases públicas."
    },
    "msitarzewski/agency-agents": {
        "what": "Coleção modular de agentes autônomos e personas de IA em Shell/Python configurados para executar tarefas completas de uma agência digital (marketing, redação, SEO, análise de métricas).",
        "use_cases": "Automatizar a produção de conteúdo, campanhas de email marketing, briefings de design e relatórios de métricas sem equipe numerosa.",
        "quickstart": """```bash
git clone https://github.com/msitarzewski/agency-agents.git
cd agency-agents
./run-agency.sh
```""",
        "pro_tip": "Defina arquivos de contexto da marca na pasta `config/` para que todos os agentes gerem textos seguindo a identidade e tom de voz da sua empresa."
    },
    "affaan-m/ECC": {
        "what": "Repositório de engenharia de software e computação em nuvem com arquiteturas de referência para sistemas corporativos escaláveis em JavaScript/TypeScript.",
        "use_cases": "Estudo de padrões arquiteturais em nuvem, microsserviços desacoplados e padrões de resiliência (Circuit Breaker, Retry, Dead Letter Queue).",
        "quickstart": """```bash
git clone https://github.com/affaan-m/ECC.git
cd ECC
npm install
```""",
        "pro_tip": "Utilize os diagramas de arquitetura do repositório como modelo para documentar as decisões de engenharia (ADRs) dos seus projetos."
    },
    "trimstray/the-book-of-secret-knowledge": {
        "what": "Uma das maiores e mais aclamadas coleções do GitHub com comandos de linha de comando, manuais de redes, scripts de pentest, auditoria de segurança, monitoramento e ferramentas de infraestrutura.",
        "use_cases": "Guia de consulta diária para SysAdmins, DevOps e engenheiros de segurança encontrarem o comando exato de terminal para qualquer diagnóstico de rede ou servidor.",
        "quickstart": """```bash
# Acesse o README no GitHub e use o Ctrl+F para encontrar o comando exato para Linux, Docker, Nginx, IPTables ou Wireshark!
```""",
        "pro_tip": "Salve este repositório nos seus favoritos locais: ele substitui dezenas de buscas no Google quando você precisa debugar problemas de rede ou permissões no Linux."
    },
    "obra/superpowers": {
        "what": "Coleção de scripts de produtividade em Shell e utilitários de automação para transformar o terminal em um ambiente de desenvolvimento de alta velocidade.",
        "use_cases": "Automação de tarefas repetitivas no terminal, aliases inteligentes e gerenciamento de arquivos em lote.",
        "quickstart": """```bash
git clone https://github.com/obra/superpowers.git
cd superpowers
# Adicione ao seu .bashrc ou .zshrc
```""",
        "pro_tip": "Adicione as funções de busca rápida de histórico do Superpowers ao seu shell para nunca mais perder um comando longo executado semanas atrás."
    },
    "vinta/awesome-python": {
        "what": "A lista com curadoria definitiva das melhores bibliotecas, frameworks e ferramentas do ecossistema Python no mundo.",
        "use_cases": "Encontrar a biblioteca Python ideal e mais mantida para qualquer desafio (automação, web, dados, segurança, IA, áudio, PDF).",
        "quickstart": """```bash
# Explore as categorias no README oficial no GitHub para encontrar a melhor lib para seu projeto.
```""",
        "pro_tip": "Antes de criar um script do zero em Python, verifique se já existe uma biblioteca consagrada e testada listada nesta curadoria."
    },
    "jwasham/coding-interview-university": {
        "what": "O mais completo plano de estudos autônomo para entrevistas de engenharia de software em grandes empresas de tecnologia (FAANG/Big Tech). Cobre estruturas de dados, algoritmos, complexidade assintótica (Big-O) e design de sistemas.",
        "use_cases": "Preparação estruturada de médio/longo prazo para passar em processos seletivos internacionais de alta remuneração.",
        "quickstart": """```bash
# Siga a trilha diária de estudos documentada no README (disponível também em português!).
```""",
        "pro_tip": "Resolva os exercícios propostos no LeetCode implementando as estruturas de dados (árvores, grafos, heaps) do zero em código antes de usar bibliotecas prontas."
    },
    "donnemartin/system-design-primer": {
        "what": "O recurso número 1 do mundo para aprender a projetar sistemas distribuídos em larga escala (System Design). Ensina escalabilidade, bancos de dados, cache, load balancers, filas, sharding e consistência.",
        "use_cases": "Preparação para entrevistas de Sênior/Staff e arquitetura de sistemas reais que precisam suportar milhões de usuários simultâneos.",
        "quickstart": """```bash
# Acesse o repositório e explore os estudos de caso práticos (ex: 'Como projetar o Twitter', 'Como projetar o Pastebin').
```""",
        "pro_tip": "Estude a seção de cálculos 'Back of the Envelope' para aprender a estimar memória, disco e largura de banda de qualquer arquitetura em 2 minutos no quadro branco."
    },
    "semantica-agi/semantica": {
        "what": "Infraestrutura de contexto nativa em grafos para sistemas de IA explicáveis e auditáveis em Python. Conecta memória de agentes, ontologias e grafos de decisão.",
        "use_cases": "Construção de sistemas de IA corporativos onde cada decisão ou recomendação do agente precisa ser 100% rastreável e auditável.",
        "quickstart": """```bash
pip install semantica
python -m semantica.init
```""",
        "pro_tip": "Use a camada de proveniência do Semantica para gerar relatórios de conformidade (compliance) exigidos por regulações de IA como o EU AI Act."
    },
    "coollabsio/coolify": {
        "what": "A plataforma self-hostable líder open-source alternativa ao Vercel, Netlify e Heroku. Permite fazer deploy de sites estáticos, bancos de dados e aplicações full-stack em qualquer servidor VPS com 1 clique.",
        "use_cases": "Hospedar todas as suas aplicações, bancos de dados (PostgreSQL, Redis, MySQL) e mini-SaaS em uma VPS de $5 sem pagar planos caros da nuvem.",
        "quickstart": """```bash
# Instalação com 1 comando em qualquer servidor Linux Ubuntu/Debian:
curl -fsSL https://cdn.coollabs.io/coolify/install.sh | bash
# Acesse http://SEU_IP:8000
```""",
        "pro_tip": "Conecte seu repositório do GitHub no Coolify para ter deploys automáticos a cada `git push` com certificados SSL gratuitos gerados via Let's Encrypt."
    },
    "zulip/zulip": {
        "what": "Servidor e aplicação web de chat para equipes 100% open-source com modelo exclusivo de conversas organizadas por tópicos (streams + topics).",
        "use_cases": "Alternativa auto-hospedada ao Slack e Microsoft Teams que elimina o caos de mensagens e permite manter conversas assíncronas produtivas.",
        "quickstart": """```bash
docker run -d -p 80:80 -p 443:443 --name zulip zulip/docker-zulip:latest
```""",
        "pro_tip": "Use os tópicos do Zulip para separar discussões por issue ou pull request: ninguém perde o contexto de uma decisão tomada dias atrás."
    },
    "metabase/metabase": {
        "what": "A ferramenta de Business Intelligence (BI) e dashboards analíticos open-source mais simples e intuitiva do mundo. Permite criar gráficos e relatórios sem precisar saber SQL.",
        "use_cases": "Visualização de métricas de negócio; compartilhamento de relatórios em tempo real com a equipe; criação de dashboards executivos conectados a bancos de dados.",
        "quickstart": """```bash
docker run -d -p 3000:3000 --name metabase metabase/metabase
# Acesse http://localhost:3000
```""",
        "pro_tip": "Conecte o Metabase ao seu banco PostgreSQL de produção e crie 'Questions' que enviam resumos automáticos em PDF no Slack toda segunda-feira de manhã."
    },
    "PostHog/posthog": {
        "what": "Plataforma tudo-em-um de análise de produto, gravação de sessões (session replay), feature flags, testes A/B e observabilidade de IA open-source.",
        "use_cases": "Entender exatamente como os usuários usam seu SaaS; assistir às gravações de tela de usuários com bugs; rastrear conversões de funis de vendas.",
        "quickstart": """```bash
# Executar localmente com Docker Compose:
git clone https://github.com/PostHog/posthog.git
cd posthog
docker compose up -d
```""",
        "pro_tip": "Use as Feature Flags do PostHog para lançar novas funcionalidades apenas para 10% dos usuários antes de liberar para a base inteira."
    },
    "pocketbase/pocketbase": {
        "what": "Backend em tempo real open-source em 1 único arquivo executável em Go. Inclui banco SQLite embarcado, autenticação com OAuth2, armazenamento de arquivos e painel de controle admin.",
        "use_cases": "Construir o backend completo de protótipos, MVPs, aplicativos mobile e sites em menos de 1 hora sem configurar servidores pesados.",
        "quickstart": """```bash
# Baixe o executável para seu sistema e inicie:
./pocketbase serve --http="0.0.0.0:8090"
# Acesse o painel em http://localhost:8090/_/
```""",
        "pro_tip": "Como o PocketBase é um binário único, você pode colocá-lo dentro de uma imagem Docker minúscula de 20MB para deploys instantâneos em qualquer nuvem."
    },
    "triggerdotdev/trigger.dev": {
        "what": "Plataforma de código aberto para criação e orquestração de background jobs, fluxos de longa duração e agentes de IA em TypeScript com execução sem timeout.",
        "use_cases": "Executar tarefas pesadas (geração de relatórios, processamento de vídeos, agentes de IA com múltiplos passos) sem derrubar servidores Next.js ou Vercel.",
        "quickstart": """```bash
npx @trigger.dev/cli@latest init
npx @trigger.dev/cli@latest dev
```""",
        "pro_tip": "Use a função `tasks.trigger()` para disparar processos que demoram mais de 10 minutos sem se preocupar com os limites de timeout do Vercel Serverless."
    },
    "Infisical/infisical": {
        "what": "A plataforma open-source líder para gerenciamento de segredos, variáveis de ambiente (`.env`), certificados e controle de acesso privilegiado.",
        "use_cases": "Sincronizar variáveis de ambiente entre toda a equipe de desenvolvimento com criptografia de ponta a ponta, eliminando o compartilhamento inseguro de `.env` no Slack ou WhatsApp.",
        "quickstart": """```bash
# Instalar a CLI do Infisical:
# Windows (Scoop): scoop install infisical
# Ou via npm: npm install -g infisical
infisical login
infisical run -- npm run dev
```""",
        "pro_tip": "Use `infisical run -- comando` para injetar variáveis de ambiente dinamicamente na memória da aplicação sem precisar salvar arquivos `.env` em disco."
    },
    "HideMeBr/SambaTu": {
        "what": "Wordlist brasileira de senhas para testes de intrusão e conscientização de segurança. Reúne senhas 100% brasileiras expostas em vazamentos e logs de infostealer.",
        "use_cases": "Auditoria de força de senhas em empresas brasileiras; testes de resistência em políticas de autenticação contra padrões culturais locais.",
        "quickstart": """```bash
git clone https://github.com/HideMeBr/SambaTu.git
cd SambaTu
# Use a lista em ferramentas autorizadas de auditoria de senhas
```""",
        "pro_tip": "Utilize esta wordlist para auditar se colaboradores da sua organização estão utilizando senhas comuns com termos do vocabulário brasileiro."
    },
    "sickn33/agentic-awesome-skills": {
        "what": "Plano de controle local e biblioteca com mais de 2.000 habilidades (skills) para agentes de IA de codificação (Claude Code, Cursor, Codex, Gemini CLI).",
        "use_cases": "Descobrir, validar e equipar agentes autônomos com habilidades prontas de desenvolvimento, testes e DevOps.",
        "quickstart": """```bash
git clone https://github.com/sickn33/agentic-awesome-skills.git
cd agentic-awesome-skills
pip install -r requirements.txt
python aas_cli.py list
```""",
        "pro_tip": "Use o comando `aas_cli.py validate` para checar se as dependências exigidas por uma skill estão instaladas antes de ativá-la no seu agente."
    },
    "CodebuffAI/freebuff": {
        "what": "Agente de codificação autônomo open-source gratuito que ajuda desenvolvedores a planejar, implementar e refatorar bases de código complexas.",
        "use_cases": "Assistente de programação automatizado para tarefas do dia a dia no terminal.",
        "quickstart": """```bash
npm install -g freebuff
freebuff start
```""",
        "pro_tip": "Execute o Freebuff com uma descrição clara do escopo do arquivo antes de solicitar refatorações amplas."
    },
    "deepseek-ai/deepseek-harness": {
        "what": "Framework e harness modular de plugins oficial da DeepSeek para orquestração de agentes de IA de código com alta eficiência de inferência.",
        "use_cases": "Criar agentes customizados com modelos DeepSeek-V3 e DeepSeek-R1 integrados a ferramentas do sistema.",
        "quickstart": """```bash
git clone https://github.com/deepseek-ai/deepseek-harness.git
cd deepseek-harness
npm install
npm run build
```""",
        "pro_tip": "Aproveite a capacidade de raciocínio profundo do modelo DeepSeek-R1 ativando o modo de planejamento em árvore para tarefas de matemática e algoritmos."
    },
    "Egonex-AI/Understand-Anything": {
        "what": "Ferramenta em TypeScript que converte bases de código complexas em grafos de conhecimento interativos que ensinam a arquitetura do projeto a desenvolvedores e agentes de IA.",
        "use_cases": "Onboarding ultrarrápido em bases de código legadas gigantescas; navegação visual de módulos e funções antes de realizar refatorações.",
        "quickstart": """```bash
npx understand-anything ./caminho-do-projeto
# Abre um visualizador interativo em 3D no navegador
```""",
        "pro_tip": "Gere o grafo de arquitetura antes de passar uma feature para um estagiário ou novo membro da equipe para reduzir o tempo de onboarding de dias para minutos."
    },
    "NanoNets/Graft": {
        "what": "Extensão e servidor MCP de engenharia de contexto para acelerar agentes de IA (Claude Code, Cursor, Codex), fornecendo compreensão semântica da base de código com custo reduzido de tokens.",
        "use_cases": "Permitir que agentes de IA compreendam grandes monorepos sem estourar o limite de tokens da janela de contexto.",
        "quickstart": """```bash
npm install -g @nanonets/graft
graft index .
claude mcp add graft
```""",
        "pro_tip": "Execute `graft index` após grandes refatorações para atualizar o índice local de árvore sintática (Tree-sitter) usado pelos agentes."
    },
    "elder-plinius/OBLITERATUS": {
        "what": "Framework de pesquisa avançada em segurança de modelos de linguagem e Red-Teaming criado pelo pesquisador Plinius para testar os limites de alinhamento de IA.",
        "use_cases": "Pesquisa de vulnerabilidades em modelos de IA e teste de estresse de sistemas de moderação de conteúdo.",
        "quickstart": """```bash
git clone https://github.com/elder-plinius/OBLITERATUS.git
cd OBLITERATUS
pip install -r requirements.txt
```""",
        "pro_tip": "Estudo recomendado para engenheiros de segurança que precisam implementar camadas de defesa contra injeção de prompt adversária."
    },
    "PaddlePaddle/PaddleOCR": {
        "what": "O mais poderoso e leve toolkit de Reconhecimento Óptico de Caracteres (OCR) em Python, com suporte a mais de 100 idiomas e alta precisão na extração de texto de imagens e PDFs para LLMs.",
        "use_cases": "Digitalização automatizada de documentos; pipelines de visão para RAG com documentos escaneados; extração de dados de fotos de recibos e placas.",
        "quickstart": """```bash
pip install paddlepaddle paddleocr
# No terminal ou Python:
# from paddleocr import PaddleOCR
# ocr = PaddleOCR(use_angle_cls=True, lang='pt')
# result = ocr.ocr('documento_escaneado.jpg')
```""",
        "pro_tip": "Ative o parâmetro `use_angle_cls=True` para que o modelo rotacione automaticamente documentos que foram escaneados de cabeça para baixo ou inclinados."
    },
    "google-research/timesfm": {
        "what": "Modelo fundacional de séries temporais (Time Series Foundation Model) pré-treinado pelo Google Research para previsão de dados temporais em escala.",
        "use_cases": "Previsão de demanda de estoque; estimativa de tráfego de servidores; projeção de métricas financeiras e vendas com alta precisão sem treinamento manual pesado.",
        "quickstart": """```bash
pip install timesfm
# No Python:
# import timesfm
# tfm = timesfm.TimesFm(context_len=512, horizon_len=128)
# tfm.load_from_checkpoint(repo_id="google/timesfm-1.0-200m")
# forecast, _ = tfm.forecast(sua_serie_temporal)
```""",
        "pro_tip": "Utilize o TimesFM no modo zero-shot: na maioria dos cenários de séries temporais financeiras e de infraestrutura, ele supera modelos clássicos como ARIMA e Prophet sem necessidade de fine-tuning."
    },
    "rtk-ai/rtk": {
        "what": "Proxy CLI ultra-rápido em Rust que reduz o consumo de tokens de saída em até 60-90% nos comandos de agentes de IA de código sem perda de precisão técnica.",
        "use_cases": "Economizar centenas de dólares por mês em APIs da OpenAI e Anthropic ao usar Claude Code, Cursor e terminais de IA.",
        "quickstart": """```bash
# Baixar o binário único em Rust ou compilar:
git clone https://github.com/rtk-ai/rtk.git
cd rtk
cargo build --release
./target/release/rtk proxy --port 8080
```""",
        "pro_tip": "Aponte o endpoint do seu Claude Code para o proxy do RTK: ele remove automaticamente saídas repetitivas de terminal antes de enviar os tokens de volta para a IA."
    }
}

with open("data/catalog_db.json", "w", encoding="utf-8") as f:
    json.dump(CATALOG_DB, f, indent=2, ensure_ascii=False)
print(f"Salvas {len(CATALOG_DB)} novas entradas detalhadas em catalog_db.json")
