# -*- coding: utf-8 -*-
"""
Atualização com Análise Técnica Individualizada de Alta Fidelidade (100% PT-BR)
Para os 42 repositórios recentes que estavam com análises de fallback genéricas.
"""

import json
import sys

sys.stdout.reconfigure(encoding="utf-8")

UPDATES = {
    "iwe-org/iwe": {
        "what": "Grafo de conhecimento baseado em Markdown escrito em Rust, projetado para atuar como Language Server Protocol (LSP) no seu editor e fornecer memória contextual via CLI e protocolo MCP para agentes autônomos de IA.",
        "use_cases": "Construção de segundo cérebro (Zettelkasten) conectado diretamente ao Cursor/Claude Code; busca semântica em bases de notas e documentações markdown; fornecimento de contexto estruturado para agentes de código.",
        "quickstart": """```bash
cargo install iwe
# ou inicialize seu cofre de notas:
iwe init meu-vault
iwe mcp --serve
```""",
        "pro_tip": "Conecte o `iwe` como servidor MCP no Claude Desktop ou Cursor configurando `{\"command\": \"iwe\", \"args\": [\"mcp\", \"--vault\", \"/caminho/notas\"]}` para que a IA consulte seus grafos de notas em tempo real."
    },
    "stablyai/orca": {
        "what": "Ambiente de Desenvolvimento de Agentes (ADE - Agent Development Environment) em TypeScript para orquestrar frotas de agentes de código rodando em paralelo. Permite executar qualquer agente de programação usando suas próprias assinaturas de IA no desktop, mobile ou VPS.",
        "use_cases": "Execução paralela de múltiplos agentes em diferentes branches de um monorepo; monitoramento visual de tarefas de refatoração em lote; gerenciamento centralizado de cotas de APIs de IA para times.",
        "quickstart": """```bash
git clone https://github.com/stablyai/orca.git
cd orca
npm install
npm run dev
# Acesse http://localhost:3000
```""",
        "pro_tip": "Use o modo Headless (`orca run --fleet 4 --task refactor-tests`) em servidores VPS para disparar 4 agentes simultâneos resolvendo issues do GitHub via webhook."
    },
    "Leonxlnx/taste-skill": {
        "what": "Conjunto de habilidades e regras de design ('Taste-Skill') para assistentes de IA (Claude Code, Cursor, Copilot). Fornece diretrizes estéticas refinadas e impede que a IA gere layouts genéricos, clichês visuais ('AI slop') ou designs sem personalidade.",
        "use_cases": "Criação de interfaces web modernas com tipografia equilibrada e micro-interações elegantes; refinamento visual automático de componentes React, Vue e Tailwind; padronização estética para produtos de software.",
        "quickstart": """```bash
npx skills add Leonxlnx/taste-skill
# ou importe no seu arquivo .cursorrules / CLAUDE.md
```""",
        "pro_tip": "Adicione as diretrizes do `taste-skill` diretamente no seu arquivo `AGENTS.md` ou `.cursorrules` para que qualquer componente gerado pela IA já venha com espaçamentos harmoniosos e paleta HSL balanceada."
    },
    "calesthio/OpenMontage": {
        "what": "Primeiro sistema de produção de vídeo agentico 100% open-source em Python. Possui 12 pipelines integradas, mais de 100 ferramentas e 700+ arquivos de conhecimento para transformar assistentes de código em um estúdio completo de edição e geração de vídeo.",
        "use_cases": "Automação completa da criação de vídeos institucionais, trailers e tutoriais; geração procedural de efeitos visuais e legendagem sincronizada; renderização em lote de conteúdo multimídia para marketing.",
        "quickstart": """```bash
git clone https://github.com/calesthio/OpenMontage.git
cd OpenMontage
pip install -r requirements.txt
python -m montage.studio --config project.yaml
```""",
        "pro_tip": "Utilize a pipeline de renderização acelerada por GPU passando `--gpu-acceleration cuda` para processar transições de vídeo e interpolação de frames em alta taxa de quadros."
    },
    "Panniantong/Agent-Reach": {
        "what": "CLI e biblioteca em Python que dá 'olhos' para agentes de IA navegarem e extraírem dados da internet inteira. Permite ler e pesquisar no Twitter/X, Reddit, YouTube, GitHub, Bilibili e XiaoHongShu via um único comando e sem custo de APIs oficiais.",
        "use_cases": "Agentes de inteligência competitiva que monitoram menções à marca em redes sociais; pesquisa de tendências em múltiplos fóruns em tempo real; raspagem de discussões técnicas para síntese de relatórios.",
        "quickstart": """```bash
pip install agent-reach
# Buscar no Twitter e Reddit simultaneamente:
agent-reach search "Claude Code release" --platforms twitter,reddit --limit 20
```""",
        "pro_tip": "Encaminhe o output em JSON (`--format json`) diretamente para o pipe de contexto da sua LLM ou servidor MCP para enriquecer prompts com discussões quentes da web."
    },
    "cathrynlavery/diagram-design": {
        "what": "Biblioteca com 27 tipos de diagramas editoriais e arquiteturais em HTML + SVG puro desenvolvidos especificamente para Claude Code. Não possui sombras pesadas ou estilos 'Mermaid-slop', priorizando clareza editorial e elegância visual.",
        "use_cases": "Documentação de arquitetura de microsserviços e fluxos de dados em repositórios; criação de infográficos técnicos para apresentações e documentações; relatórios executivos com visual editorial moderno.",
        "quickstart": """```bash
git clone https://github.com/cathrynlavery/diagram-design.git
cd diagram-design
# Abra a galeria de templates no navegador:
start index.html
```""",
        "pro_tip": "Copie o template SVG desejado diretamente para o seu `README.md` ou documentação Markdown; o SVG é renderizado nativamente no GitHub sem necessidade de plugins externos."
    },
    "lidge-jun/opencodex": {
        "what": "Proxy agregador e universal em TypeScript para OpenAI Codex e Claude Code. Permite utilizar qualquer modelo de linguagem (DeepSeek, Gemini, Grok, Claude, Ollama, Kimi) na CLI, App e SDK do Codex e no Claude Code sem restrição de provedor.",
        "use_cases": "Redução de custos operacionais usando modelos locais ou mais baratos (DeepSeek-V3, Gemini Flash) dentro do Claude Code; contorno de limites de cota e bloqueios regionais de provedores de IA.",
        "quickstart": """```bash
npm install -g opencodex
opencodex config --provider deepseek --api-key sua_chave
opencodex start --port 8080
```""",
        "pro_tip": "Configure `export ANTHROPIC_BASE_URL=http://localhost:8080` no terminal para redirecionar o Claude Code para rodar com DeepSeek ou Gemini mantendo todas as ferramentas MCP ativas."
    },
    "Tabbit-Browser/dsh-plugin": {
        "what": "Coleção de plugins e extensões em JavaScript para o Tabbit Browser integrados ao DeepSeek Harness (DSH). Permite que agentes da DeepSeek interajam diretamente com o navegador, manipulando abas, formulários e extraindo dados DOM.",
        "use_cases": "Automação de fluxos de navegação web supervisionados por IA; testes end-to-end com agentes autônomos; extração e preenchimento inteligente de formulários em sistemas legados.",
        "quickstart": """```bash
git clone https://github.com/Tabbit-Browser/dsh-plugin.git
cd dsh-plugin
npm install
npm run build
```""",
        "pro_tip": "Carregue o diretório `dist/` como extensão descompactada no Chrome/Brave para permitir que o agente interaja com sessões já autenticadas nos seus sites de trabalho."
    },
    "Genymobile/scrcpy": {
        "what": "A ferramenta de referência open-source em C para espelhamento e controle de dispositivos Android no computador via USB ou Wi-Fi. Não exige root, possui latência baixíssima (35-70ms) e performance de 60fps+ com alta resolução.",
        "use_cases": "Gravação e transmissão de tela de celulares Android; testes automatizados de aplicativos móveis em tempo real; controle do smartphone direto pelo teclado e mouse no Windows/Linux.",
        "quickstart": """```bash
winget install Genymobile.scrcpy
# Conecte o cabo USB com depuração ativada e execute:
scrcpy
```""",
        "pro_tip": "Use o comando `scrcpy --tcpip --max-size=1080 --video-bit-rate=8M --stay-awake` para controlar seu Android 100% sem fio pela rede Wi-Fi mantendo a tela do aparelho desligada no PC."
    },
    "lwthiker/curl-impersonate": {
        "what": "Build customizada do cURL que emula com precisão cirúrgica as assinaturas de rede TLS/HTTP2 de navegadores reais (Chrome, Firefox, Safari), permitindo fazer requisições HTTP sem ser bloqueado por Cloudflare, Akamai e sistemas anti-bot.",
        "use_cases": "Raspagem de dados em sites com proteção rigorosa anti-bot; auditoria de segurança em WAFs e regras de fingerprinting TLS; automação de downloads e integrações HTTP resilientes.",
        "quickstart": """```bash
docker run -it lwthiker/curl-impersonate:chrome curl_chrome116 https://tls.browserleaks.com/json
```""",
        "pro_tip": "Utilize o wrapper Python `curl_cffi` para integrar o `curl-impersonate` diretamente em scripts de automação substituindo a biblioteca `requests` com compatibilidade imediata."
    },
    "D4Vinci/Scrapling": {
        "what": "Framework adaptativo de Web Scraping em Python de altíssima performance. Combina seletores rápidos (CSS/XPath), bypass nativo de proteções antibot (Cloudflare Turnstile) e suporte transparente a requisições estáticas e navegadores dinâmicos.",
        "use_cases": "Extração de dados em sites com proteções agressivas de fingerprinting; pipelines de coleta de dados para alimentação de LLMs; automação de monitoramento de preços e estoques.",
        "quickstart": """```bash
pip install scrapling
# Exemplo de extração:
from scrapling import Fetcher
page = Fetcher().get('https://quotes.toscrape.com')
print(page.find_all('span.text'))
```""",
        "pro_tip": "Ative o motor de stealth com `Fetcher(stealth=True, headless=True)` para passar despercebido por desafios Cloudflare sem precisar pagar por proxies residenciais caros."
    },
    "browser-use/browser-use": {
        "what": "Framework em Python líder para permitir que modelos de linguagem (LLMs) controlem navegadores web de forma 100% autônoma. Permite que a IA clique em botões, preencha formulários, resolva captchas e execute tarefas complexas na web.",
        "use_cases": "Automação de compras online e reservas; preenchimento automatizado de planilhas e sistemas web corporativos; testes de ponta a ponta e auditoria de interfaces web.",
        "quickstart": """```bash
pip install browser-use
playwright install
# Execute seu agente:
python -c "from browser_use import Agent; import asyncio; asyncio.run(Agent(task='Buscar o melhor preço de RTX 4080 na Amazon').run())"
```""",
        "pro_tip": "Conecte sua própria sessão do Chrome passando `browser = Browser(config=BrowserConfig(chrome_instance_path='...'))` para usar cookies e logins já salvos sem precisar autenticar de novo."
    },
    "firecrawl/firecrawl": {
        "what": "A API de contexto definitiva para IA converter qualquer website em Markdown limpo e dados estruturados em larga escala. Desenvolvido em TypeScript, executa JavaScript, lida com paginação, sitemaps e contorna bloqueios anti-bot.",
        "use_cases": "Extração de documentações e blogs para indexação em bases de RAG; coleta estruturada de dados de e-commerce e portais de notícias; alimentação em tempo real de agentes autônomos.",
        "quickstart": """```bash
docker compose up -d
# Ou use a CLI oficial:
npx firecrawl-cli scrape https://docs.github.com
```""",
        "pro_tip": "Utilize o endpoint `/crawl` com o parâmetro `scrapeOptions: { formats: ['markdown'] }` para indexar domínios inteiros recursivamente gerando arquivos prontos para bases vetoriais."
    },
    "microsoft/markitdown": {
        "what": "Utilitário oficial da Microsoft em Python para conversão de arquivos e documentos de escritório (PDF, Word DOCX, PowerPoint PPTX, Excel XLSX, imagens com OCR, áudios com transcrição) em texto Markdown limpo.",
        "use_cases": "Padronização de acervos documentais para treinamento e RAG com LLMs; extração rápida de tabelas de planilhas e slides de apresentações corporativas; ingestão em lote de relatórios em Markdown.",
        "quickstart": """```bash
pip install markitdown
markitdown documento.pdf -o documento.md
# Suporta DOCX, PPTX, XLSX, etc.
```""",
        "pro_tip": "Passe o modelo multimodal da OpenAI ou Gemini (`markitdown imagem.png --llm-client ...`) para gerar descrições textuais ricas de gráficos e ilustrações embutidas nos documentos."
    },
    "unclecode/crawl4ai": {
        "what": "Rastreador web assíncrono e extrator em Python focado em IA, ultrarrápido e open-source. Extrai Markdown estruturado, executa JavaScript, filtra 'ruídos' (menus, rodapés, anúncios) e suporta heurísticas de chunking inteligente.",
        "use_cases": "Pipelines de RAG de alta velocidade; raspagem de dados web com execução de JavaScript dinâmico; geração de datasets para fine-tuning de modelos de linguagem.",
        "quickstart": """```bash
pip install -U crawl4ai
crawl4ai-setup
# No Python:
import asyncio; from crawl4ai import AsyncWebCrawler; asyncio.run(AsyncWebCrawler().arun(url='https://news.ycombinator.com'))
```""",
        "pro_tip": "Ative a estratégia `extraction_strategy=LLMExtractionStrategy(provider='gemini/gemini-1.5-flash')` para extrair diretamente JSON com schema validado de páginas complexas."
    },
    "MrCl0wnLab/BR-EvilPortal-HTML-Files": {
        "what": "Coleção de templates de portais cativos (Evil Portal) adaptados para o contexto e provedores brasileiros 🇧🇷 em HTML. Projetados para testes de intrusão, pesquisas de engenharia social e conscientização em cibersegurança.",
        "use_cases": "Simulações de ataques de Evil Twin e conscientização de segurança em redes Wi-Fi corporativas; testes de vulnerabilidade em roteadores e pontos de acesso; treinamentos de equipe de Red Team.",
        "quickstart": """```bash
git clone https://github.com/MrCl0wnLab/BR-EvilPortal-HTML-Files.git
cd BR-EvilPortal-HTML-Files
# Utilize em ambientes de laboratório com ESP32 / WiFi Pineapple
```""",
        "pro_tip": "Utilize exclusivamente em ambientes de teste autorizados e utilize as telas para instruir colaboradores sobre os riscos de conectar em redes Wi-Fi públicas desprotegidas."
    },
    "CopilotKit/aimock": {
        "what": "Servidor de mocks completo em TypeScript para aplicações de IA. Permite simular respostas de APIs de LLMs, servidores MCP, protocolos A2A, interfaces AG-UI, bancos vetoriais e buscas com um único pacote, uma porta e zero dependências.",
        "use_cases": "Testes automatizados e CI/CD de aplicações de IA sem gastar tokens nem depender de chaves de API; desenvolvimento offline de interfaces Copilot; simulação de cenários de erro e streaming de texto.",
        "quickstart": """```bash
npx aimock
# Inicia o servidor mock na porta 3000 simulando respostas de streaming e chamadas de ferramentas
```""",
        "pro_tip": "Configure `AIMOCK_SCENARIO=slow-network` para testar como sua interface reage a latências elevadas e quedas de conexão no streaming de respostas de IA."
    },
    "f/prompts.chat": {
        "what": "O repositório clássico e oficial 'Awesome ChatGPT Prompts' em HTML/JS. Reúne a maior coleção comunitária de personas, prompts de sistema e templates de engenharia de contexto para ChatGPT, Claude e outros LLMs.",
        "use_cases": "Descoberta de instruções de sistema eficientes para tarefas complexas (programador, revisor, mentor, arquiteto); auto-hospedagem de um portal interno de prompts para equipes com privacidade.",
        "quickstart": """```bash
git clone https://github.com/f/prompts.chat.git
cd prompts.chat
# Abra index.html ou execute:
npx serve
```""",
        "pro_tip": "Utilize o arquivo `prompts.csv` do repositório para carregar dinamicamente centenas de personas direto no seu assistente ou sistema RAG."
    },
    "unslothai/unsloth": {
        "what": "A biblioteca mais rápida e eficiente em Python para fine-tuning e treinamento local de LLMs e modelos de difusão (Llama 3.3, DeepSeek-V3, Qwen 2.5, Gemma 2). Reduz o uso de VRAM em 80% e treina até 5x mais rápido que o Hugging Face padrão.",
        "use_cases": "Fine-tuning de modelos abertos em GPUs de consumo (ex: RTX 3060/4090 ou Google Colab gratuito); especialização de LLMs para dados e terminologia da sua empresa; exportação direta para formato GGUF (Ollama).",
        "quickstart": """```bash
pip install "unsloth[colab-new] @ git+https://github.com/unslothai/unsloth.git"
# Execute o script de treinamento com FastLanguageModel
```""",
        "pro_tip": "Use o método `model.save_pretrained_gguf('meu_modelo', tokenizer, quantization_method='q4_k_m')` para gerar um arquivo GGUF pronto para rodar offline no Ollama em segundos."
    },
    "ZhuLinsen/daily_stock_analysis": {
        "what": "Sistema inteligente em Python alimentado por LLMs para análise diária de múltiplos mercados financeiros (Ações, Cripto, Índices). Agrega notícias em tempo real, indicadores técnicos, dashboard de decisões e disparos automatizados de relatórios.",
        "use_cases": "Automação de relatórios matinais de carteira de investimentos; monitoramento automatizado de ativos e indicadores técnicos (RSI, MACD); envio de alertas via Telegram, Discord e WeChat.",
        "quickstart": """```bash
git clone https://github.com/ZhuLinsen/daily_stock_analysis.git
cd daily_stock_analysis
pip install -r requirements.txt
python main.py
```""",
        "pro_tip": "Configure a execução diária gratuita via GitHub Actions com cron agendado para 30 minutos antes da abertura do mercado e receba o PDF resumido no Telegram."
    },
    "addyosmani/agent-skills": {
        "what": "Coleção de habilidades de engenharia em JavaScript criadas por Addy Osmani (líder de engenharia do Google Chrome) para agentes de código de IA. Inclui boas práticas de arquitetura, performance web e padrões de refatoração.",
        "use_cases": "Capacitar agentes de IA (Claude Code, Cursor, Windsurf) a realizarem auditorias de performance Core Web Vitals, refatoração de código limpo e diagnósticos de acessibilidade.",
        "quickstart": """```bash
npx skills add addyosmani/agent-skills
# Ou copie as regras para o seu .cursorrules / CLAUDE.md
```""",
        "pro_tip": "Ative a skill de 'web-performance' antes de pedir para a IA otimizar componentes React para que ela aplique automaticamente memoization, code-splitting e métricas INP/LCP corretas."
    },
    "earendil-works/pi": {
        "what": "Toolkit e runtime para agentes de IA em TypeScript. Oferece uma API unificada para múltiplos LLMs, loop determinístico de execução de agente, interface visual no terminal (TUI) e CLI especializada em engenharia de software autônoma.",
        "use_cases": "Assistente de terminal para refatoração e escrita de testes; desenvolvimento de agentes CLI customizados com controle fino de permissões; execução de comandos de terminal com aprovação interativa.",
        "quickstart": """```bash
npm install -g @earendil/pi
pi "Analise os testes unitários deste repositório e corrija os que estão falhando"
```""",
        "pro_tip": "Use o parâmetro `--safe-mode` para exigir confirmação antes de qualquer modificação destrutiva em arquivos de configuração ou migrações de banco."
    },
    "PrimeIntellect-ai/prime-agent": {
        "what": "Agente autônomo auto-aprimorável (RLM - Reinforcement Learning Model) em TypeScript desenvolvido pela Prime Intellect para orquestração de computação descentralizada e execução de tarefas de código de longa duração.",
        "use_cases": "Treinamento e fine-tuning de modelos em clusters distribuídos na nuvem; execução autônoma de benchmarks de machine learning; automação de infraestrutura em nuvens descentralizadas.",
        "quickstart": """```bash
git clone https://github.com/PrimeIntellect-ai/prime-agent.git
cd prime-agent
npm install
npm run build
```""",
        "pro_tip": "Integre com a API da Prime Intellect para provisionar GPUs H100 sob demanda e disparar jobs de treinamento diretamente do agente via comandos naturais."
    },
    "promovaweb/specsfy": {
        "what": "Ferramenta em JavaScript para transformar ideias brutas em software testado e especificado sem dispersar requisitos, histórias de usuário e planos técnicos em dezenas de arquivos desconexos.",
        "use_cases": "Estruturação de especificações técnicas completas para produtos de software; alinhamento de escopo entre desenvolvedores e clientes; geração de planos de testes automatizados.",
        "quickstart": """```bash
git clone https://github.com/promovaweb/specsfy.git
cd specsfy
npm install
npm start
```""",
        "pro_tip": "Utilize os templates de 'Especificação Viva' para que as alterações nos requisitos reflitam diretamente nos casos de testes unitários do seu repositório."
    },
    "yashab-cyber/opendroid": {
        "what": "Assistente autônomo e agente de segurança para Android em Kotlin. Opera localmente ou com LLMs remotas, combinando automação de tela baseada em serviços de acessibilidade com análise estática e dinâmica de apps.",
        "use_cases": "Automação de fluxos repetitivos em dispositivos Android; testes de segurança e engenharia reversa em APKs; assistente pessoal que opera o smartphone por comandos de voz.",
        "quickstart": """```bash
git clone https://github.com/yashab-cyber/opendroid.git
cd opendroid
# Compile o APK no Android Studio ou via Gradle:
./gradlew assembleDebug
```""",
        "pro_tip": "Habilite as permissões de acessibilidade via ADB (`adb shell settings put secure enabled_accessibility_services ...`) para automatizar testes sem precisar tocar no aparelho."
    },
    "itsfatduck/optimizerDuck": {
        "what": "Utilitário open-source em C# para otimização avançada, privacidade e limpeza de desempenho no Windows. Remove bloatwares, desativa telemetrias invasivas, otimiza serviços de rede e melhora a taxa de quadros (FPS).",
        "use_cases": "Otimização de máquinas Windows para desenvolvimento e jogos; limpeza de arquivos temporários e resíduos de sistema; redução do uso de memória RAM em inicializações de sistema.",
        "quickstart": """```bash
git clone https://github.com/itsfatduck/optimizerDuck.git
cd optimizerDuck
# Baixe a versão compilada em Releases ou abra no Visual Studio (.NET 8)
```""",
        "pro_tip": "Crie um ponto de restauração do sistema diretamente pelo aplicativo antes de aplicar os 'Tweaks Agressivos' para poder reverter qualquer mudança com segurança."
    },
    "microsoft/ai-agents-for-beginners": {
        "what": "Currículo educacional oficial da Microsoft com 18 lições completas em Jupyter Notebooks para dominar a criação de agentes de inteligência artificial autônomos, cobrindo AutoGen, Semantic Kernel, LangChain e padrões multi-agente.",
        "use_cases": "Capacitação técnica em engenharia de agentes de IA; aprendizado prático com exemplos de código prontos para execução; base de referência para arquiteturas corporativas de IA.",
        "quickstart": """```bash
git clone https://github.com/microsoft/ai-agents-for-beginners.git
cd ai-agents-for-beginners
pip install jupyter
jupyter notebook
```""",
        "pro_tip": "Comece pelas lições 06 e 07 (Multi-Agent Collaboration) para entender na prática como implementar padrões de reflexão e debate entre agentes especialistas."
    },
    "abundantbeing/hermes-browser-extension": {
        "what": "Extensão de navegador em JavaScript que traz o poder do Hermes Agent (Nous Research) em um painel lateral nativo no Chrome/Brave. Conecta o contexto da página que você está visualizando diretamente ao seu runtime local do Hermes.",
        "use_cases": "Resumo e extração de dados da página ativa diretamente via Hermes local; navegação e preenchimento assistido por IA; interação com modelos locais sem enviar dados para nuvens públicas.",
        "quickstart": """```bash
git clone https://github.com/abundantbeing/hermes-browser-extension.git
cd hermes-browser-extension
npm install && npm run build
# Carregue a pasta dist/ em chrome://extensions
```""",
        "pro_tip": "Conecte a extensão ao seu endpoint local do Ollama ou Hermes CLI na porta 11434 para usar seu modelo local sem nenhuma latência de rede."
    },
    "vitali87/code-graph-rag": {
        "what": "Sistema avançado de RAG baseado em Grafos de Conhecimento (GraphRAG) em Python especializado em monorepos e bases de código multilíngues. Mapeia hierarquias de classes, chamadas de funções e dependências cruzadas.",
        "use_cases": "Consultas arquiteturais complexas em monorepos corporativos; análise de impacto de refatorações de código; alimentação de agentes com contexto relacional preciso.",
        "quickstart": """```bash
git clone https://github.com/vitali87/code-graph-rag.git
cd code-graph-rag
pip install -r requirements.txt
python indexer.py --repo /caminho/do/projeto
```""",
        "pro_tip": "Gere o grafo com visualização no Neo4j passando `--export-neo4j` para inspecionar visualmente os nós de acoplamento mais críticos do seu software."
    },
    "outline/outline": {
        "what": "A plataforma de base de conhecimento e wiki em equipe mais rápida, moderna e bonita do ecossistema open-source. Desenvolvida em TypeScript/React, oferece edição colaborativa em tempo real em Markdown com alta segurança.",
        "use_cases": "Documentação centralizada para empresas e equipes de engenharia; documentação de APIs, manuais de onboarding e processos internos; alternativa superior ao Notion e Confluence.",
        "quickstart": """```bash
docker compose up -d
# Acesse http://localhost:3000 e configure autenticação via Google/Slack/OIDC
```""",
        "pro_tip": "Habilite a busca vetorial integrada configurando os parâmetros de embedding no `.env` para que a busca encontre documentos pelo significado semântico das palavras."
    },
    "Leantime/leantime": {
        "what": "Sistema open-source de gerenciamento de projetos em PHP focado em equipes e profissionais com TDAH, autismo e perfis não tradicionais. Combina metodologias ágeis (Kanban, Scrum, Lean) com recursos de suporte cognitivo e IA.",
        "use_cases": "Gestão visual de projetos e tarefas diárias com foco em redução de sobrecarga mental; planejamento estratégico de startups e pequenas empresas; organização de roadmaps orientados a metas.",
        "quickstart": """```bash
docker run -p 8080:80 -d leantime/leantime:latest
# Acesse http://localhost:8080
```""",
        "pro_tip": "Ative os plugins de 'Timeboxing' e 'AI Milestone Generator' para dividir tarefas complexas em etapas menores e fáceis de concluir sem procrastinação."
    },
    "ente/ente": {
        "what": "Plataforma em nuvem 100% criptografada de ponta a ponta (E2EE) em Dart/Flutter para armazenamento seguro de fotos, vídeos e autenticação em dois fatores (2FA). A melhor alternativa com privacidade total ao Google Fotos e Apple Fotos.",
        "use_cases": "Backup automático e sincronização de fotos e vídeos pessoais com privacidade absoluta; compartilhamento de álbuns criptografados com familiares; gerenciador de códigos 2FA (Ente Auth).",
        "quickstart": """```bash
git clone https://github.com/ente-io/ente.git
cd ente/server
docker compose up -d
```""",
        "pro_tip": "Utilize o app móvel do Ente apontando para o seu próprio servidor auto-hospedado para ter armazenamento infinito com criptografia onde ninguém, nem o provedor, pode ver suas fotos."
    },
    "imputnet/cobalt": {
        "what": "O melhor e mais rápido utilitário de download de mídias da web em Svelte/Node.js. Permite baixar vídeos, áudios e imagens do YouTube, Twitter/X, TikTok, Reddit, Instagram e dezenas de outros serviços sem anúncios ou rastreadores.",
        "use_cases": "Download de vídeos em alta resolução (4K/60fps) e áudios em MP3 sem propagandas; arquivamento de postagens e mídias de redes sociais; integração em bots de automação via API REST.",
        "quickstart": """```bash
docker run -d -p 9000:9000 --name cobalt -e API_URL=http://localhost:9000 ghcr.io/imputnet/cobalt:latest
```""",
        "pro_tip": "Acesse a API REST do Cobalt via `POST /api/json` passando `{\"url\": \"...\", \"videoQuality\": \"max\"}` para automatizar downloads de mídia diretamente em scripts Python ou bots do Telegram."
    },
    "Stirling-Tools/Stirling-PDF": {
        "what": "A aplicação web nº 1 no GitHub para manipulação completa de arquivos PDF em Java/Spring. Permite mesclar, dividir, girar, comprimir, aplicar OCR em mais de 100 línguas, assinar digitalmente e converter arquivos 100% localmente.",
        "use_cases": "Manipulação e edição de documentos confidenciais sem enviar para sites externos; extração de texto via OCR de documentos escaneados; automação corporativa de assinatura e proteção de PDFs.",
        "quickstart": """```bash
docker run -d -p 8080:8080 -v ./stirling-data:/configs --name stirling-pdf frooodle/s-pdf:latest
# Acesse http://localhost:8080
```""",
        "pro_tip": "Ative a flag de segurança de dados `SYSTEM_ENABLE_SECURITY=false` para uso em rede local fechada ou integre com autenticação OAuth2 corporativa para uso compartilhado."
    },
    "Shpigford/chops": {
        "what": "Aplicativo nativo para macOS em Swift para gerenciar, editar e organizar habilidades de agentes de IA (*skills*) de forma centralizada entre Claude Code, Cursor, Codex, Windsurf e Amp.",
        "use_cases": "Gerenciamento visual de prompts de sistema e MCPs em um único menu na barra superior do Mac; sincronização de skills entre diferentes editores de código; ativação e desativação rápida de habilidades.",
        "quickstart": """```bash
git clone https://github.com/Shpigford/chops.git
cd chops
# Abra no Xcode e faça o build para a barra de menu do macOS
```""",
        "pro_tip": "Use os atalhos globais de teclado do Chops para injetar snippets e skills específicas no terminal do Claude Code com um único clique."
    },
    "sujeeth36/TradingView-Premium-FREE": {
        "what": "Suite de scripts e extensão para desbloquear funcionalidades avançadas e múltiplos layouts de gráficos no TradingView sem exigência de assinatura paga.",
        "use_cases": "Análise técnica em múltiplos tempos gráficos simultâneos; uso de múltiplos indicadores na mesma tela; estudos e backtests de estratégias de trading.",
        "quickstart": """```bash
git clone https://github.com/sujeeth36/TradingView-Premium-FREE.git
# Siga as instruções do README para carregar o script via Violentmonkey / Tampermonkey
```""",
        "pro_tip": "Utilize com contas de teste para validar seus estudos de análise técnica e estratégias quantitativas sem custos iniciais."
    },
    "rmyndharis/OpenWA": {
        "what": "Gateway de API para WhatsApp gratuito, open-source e auto-hospedável em TypeScript. Desenvolvido sobre Baileys/Puppeteer, permite enviar e receber mensagens de texto, mídias, botões e webhooks de múltiplos números.",
        "use_cases": "Criação de bots de atendimento e suporte via WhatsApp; envio automatizado de notificações de sistemas (alertas de compras, relatórios, códigos 2FA); integração de IA em conversas de WhatsApp.",
        "quickstart": """```bash
git clone https://github.com/rmyndharis/OpenWA.git
cd OpenWA
npm install
npm run start:dev
# Escaneie o QR Code no terminal para conectar seu WhatsApp
```""",
        "pro_tip": "Configure o endpoint de Webhook no `.env` para repassar mensagens recebidas diretamente para uma rota FastAPI ou servidor de agentes de IA e responder em tempo real."
    },
    "Bill-Stewart/SyncthingWindowsSetup": {
        "what": "Instalador nativo e pacote de serviço em Inno Setup para o Syncthing no Windows. Configura o Syncthing como serviço de sistema contínuo em segundo plano, sem necessidade de janelas de terminal abertas.",
        "use_cases": "Sincronização contínua e criptografada de pastas entre múltiplos computadores Windows, Linux e Android; backup descentralizado de projetos e documentos sem depender de nuvens pagas.",
        "quickstart": """```bash
winget install BillStewart.SyncthingWindowsSetup
# Ou baixe o executável Syncthing-Setup.exe em Releases
```""",
        "pro_tip": "Marque a opção 'Run as Windows Service' durante a instalação para que as pastas continuem sincronizando mesmo antes do usuário fazer login no Windows."
    },
    "arthurspk/guiadofrontend": {
        "what": "Guia completo e estruturado para formação e carreira de desenvolvedores Front-End no Brasil. Reúne mapas mentais, trilhas de aprendizado (HTML, CSS, JS, TypeScript, React, Next.js), cursos recomendados e projetos práticos.",
        "use_cases": "Orientação de estudos e nivelamento técnico para desenvolvedores front-end; preparação para entrevistas e processos seletivos; consulta rápida de tecnologias e ferramentas do ecossistema web.",
        "quickstart": """```bash
git clone https://github.com/arthurspk/guiadofrontend.git
cd guiadofrontend
# Acesse o roadmap e materiais organizados por módulos
```""",
        "pro_tip": "Siga a trilha de 'Projetos Práticos' para construir um portfólio sólido no GitHub com testes automatizados, CI/CD e boas práticas de acessibilidade."
    },
    "fadidevv/keyhunter": {
        "what": "Scanner de altíssima velocidade em Rust projetado para caçar chaves de API, tokens e segredos vazados no GitHub e em repositórios locais. Suporta mais de 45 provedores (OpenAI, Anthropic, AWS, Stripe, HuggingFace) e valida chaves ativas instantaneamente.",
        "use_cases": "Auditoria preventiva em repositórios públicos e privados antes de commits; caça de credenciais vazadas em organizações de software; resposta rápida a incidentes de vazamento de segredos.",
        "quickstart": """```bash
git clone https://github.com/fadidevv/keyhunter.git
cd keyhunter
cargo build --release
./target/release/keyhunter scan --org minha-empresa
```""",
        "pro_tip": "Use a flag `--verify` para testar ativamente se as chaves encontradas ainda possuem saldo ou permissões válidas nos provedores sem disparar alertas falsos."
    },
    "trufflesecurity/trufflehog": {
        "what": "A ferramenta open-source líder em cibersegurança em Go para detecção e verificação de segredos e credenciais em código. Analisa repositórios Git, histórico de commits, buckets S3, Docker images e valida segredos contra mais de 800 APIs.",
        "use_cases": "Varredura contínua de pipelines de CI/CD para barrar commits com senhas e chaves privadas; auditoria de todo o histórico do Git em busca de segredos antigos esquecidos; proteção de segredos em infraestrutura como código.",
        "quickstart": """```bash
docker run -it trufflesecurity/trufflehog:latest github --repo https://github.com/meu-usuario/meu-repo
```""",
        "pro_tip": "Integre o TruffleHog no GitHub Actions com a flag `--only-verified` para falhar a build apenas quando uma chave de API for 100% funcional e ativa, eliminando 100% dos falsos positivos."
    },
    "langchain-ai/langgraph": {
        "what": "Framework em Python líder para construção de agentes autônomos e fluxos de IA multi-agente resilientes, cíclicos e com controle de estado. Oferece suporte nativo a persistência de memória, execução paralela e controle 'Human-in-the-Loop'.",
        "use_cases": "Orquestração de sistemas multi-agente complexos com tomada de decisão iterativa; fluxos de trabalho que exigem aprovação humana antes de ações críticas; assistentes de suporte com checkpoints de conversa persistidos em banco.",
        "quickstart": """```bash
pip install -U langgraph langchain-openai
# Crie um StateGraph com nós de decisão e transições condicionais
```""",
        "pro_tip": "Utilize o `MemorySaver` ou `SqliteSaver` como checkpointer para poder pausar a execução de um agente, inspecionar o estado e retomar exatamente de onde parou."
    }
}

def main():
    with open("data/master_catalog_db.json", "r", encoding="utf-8") as f:
        master_db = json.load(f)

    count = 0
    for k, v in UPDATES.items():
        master_db[k] = v
        count += 1

    with open("data/master_catalog_db.json", "w", encoding="utf-8") as f:
        json.dump(master_db, f, indent=2, ensure_ascii=False)

    print(f"Sucesso! {count} repositórios atualizados com análises individuais em data/master_catalog_db.json.")

if __name__ == "__main__":
    main()
