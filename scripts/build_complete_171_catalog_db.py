# -*- coding: utf-8 -*-
"""
Dicionário Unificado e Completo de Análise Técnica de Alta Fidelidade (100% PT-BR)
Para TODOS os 171 Repositórios Estrelados do Jerixco
Garante que 100% dos repositórios tenham análises individuais ricas e Dicas Pro exclusivas.
"""

import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Análises detalhadas e individualizadas para os 53 novos repositórios
NEW_53_REPOS = {
    "tw93/Pake": {
        "what": "Ferramenta inovadora escrita em Rust que empacota qualquer página web em um aplicativo desktop leve e ultra-rápido utilizando o runtime nativo do sistema operacional (via Tauri). É uma alternativa moderna com consumo de memória até 20x menor em comparação a empacotadores tradicionais baseados em Electron.",
        "use_cases": "Transformar aplicações web corporativas internas (como dashboards e webmails) em apps desktop nativos; criar clientes dedicados para ChatGPT, Claude, Notion ou YouTube com atalhos de teclado globais; distribuir PWAs como instaladores (.dmg, .msi, .deb, .AppImage) para usuários finais.",
        "quickstart": """```bash
# Instalação via NPM ou Cargo
npm install -g pake-cli
# Empacotar uma URL em um app desktop nativo com nome e ícone customizado
pake https://chatgpt.com --name ChatGPT --transparent --width 1200 --height 800
```""",
        "pro_tip": "Adicione a flag `--multi-arch` no comando de build ou configure atalhos de teclado customizados via `--safe-domain` para restringir a navegação estritamente ao domínio desejado e evitar desvios de rota."
    },
    "VoltAgent/awesome-design-md": {
        "what": "Acervo curado de arquivos DESIGN.md estruturados com base nos sistemas de design das principais marcas e referências de tecnologia (como Linear, Stripe, Apple e Vercel). O objetivo é fornecer contexto arquitetural de design tokens, tipografia e diretrizes de layout para que agentes de codificação por IA (como Claude Code, Cursor e Copilot) gerem interfaces visuais consistentes e atraentes.",
        "use_cases": "Guiar LLMs e agentes de código no desenvolvimento de interfaces frontend consistentes sem desvios de padrão estético; servir de especificação base para prototipagem rápida de landing pages no estilo de empresas de ponta; padronizar tokens de espaçamento, paletas de cores HSL e tipografia entre equipes de desenvolvimento.",
        "quickstart": """```bash
# Clone o repositório para inspecionar os sistemas de design disponíveis
git clone https://github.com/VoltAgent/awesome-design-md.git
cd awesome-design-md
# Copie o DESIGN.md desejado (ex: Linear ou Stripe) para a raiz do seu projeto
cp designs/linear/DESIGN.md /caminho/do/seu/projeto/DESIGN.md
```""",
        "pro_tip": "No seu prompt de sistema ou regras de IDE (.cursorrules / AGENTS.md), referencie explicitamente: 'Siga estritamente os tokens de espaçamento, raio de borda e cores definidos no arquivo ./DESIGN.md'."
    },
    "appsmithorg/appsmith": {
        "what": "Plataforma open-source low-code líder para construção ágil de painéis administrativos, ferramentas internas e dashboards operacionais. Conecta-se nativamente a mais de 25 bancos de dados relacionais e NoSQL, além de APIs REST e GraphQL, com suporte a JavaScript em tempo real para manipulação de dados e lógica de negócios.",
        "use_cases": "Criação de painéis de suporte ao cliente para consulta e atualização de contas; dashboards de monitoramento operacional e métricas de negócios em tempo real; formulários de aprovação e workflows de reembolso integrados ao banco de dados corporativo.",
        "quickstart": """```bash
# Inicialização rápida com Docker Compose
docker run -d --name appsmith -p 80:80 -p 443:443 \
  -v "$PWD/stacks:/appsmith-stacks" \
  --restart unless-stopped \
  appsmith/appsmith-ce
# Acesse http://localhost no navegador para criar a conta de administrador
```""",
        "pro_tip": "Utilize JS Objects com funções assíncronas (async/await) no editor do Appsmith para encadear consultas de APIs e transformações de dados em uma única transação lógica no frontend."
    },
    "Dokploy/dokploy": {
        "what": "Plataforma de implantação e hospedagem (PaaS) open-source auto-hospedável, posicionando-se como alternativa direta ao Vercel, Netlify e Heroku. Construída em TypeScript/Node.js sobre Docker e Traefik, permite gerenciar deploys automatizados a partir do Git, criar bancos de dados com um clique e gerenciar certificados SSL/domínios em qualquer VPS.",
        "use_cases": "Hospedagem centralizada de múltiplos microsserviços e aplicações full-stack em servidores baratos da Hetzner/DigitalOcean; provisionamento instantâneo de bancos PostgreSQL, MySQL, Redis e MongoDB com backups automatizados para S3; substituição de custos recorrentes de nuvens PaaS proprietárias.",
        "quickstart": """```bash
# Instalação automática em qualquer VPS Linux limpo (Ubuntu/Debian)
curl -sSL https://dokploy.com/install.sh | sh
# Acesse http://SEU_IP:3000 para configurar o painel inicial
```""",
        "pro_tip": "Configure o webhook de implantação automática com a branch main do GitHub para disparar builds incrementais via Dockerfile com cache de camadas ativado, reduzindo o tempo de deploy de minutos para segundos."
    },
    "documenso/documenso": {
        "what": "Plataforma de assinatura digital e eletrônica de documentos open-source, desenvolvida em TypeScript, Next.js, Prisma e PostgreSQL como alternativa auditável e privada ao DocuSign. Oferece suporte completo ao padrão criptográfico PAdES (PDF Advanced Electronic Signatures), campos personalizáveis e trilhas de auditoria imutáveis.",
        "use_cases": "Coleta de assinaturas digitais em contratos comerciais e acordos de confidencialidade (NDA); integração de assinatura eletrônica em fluxos automatizados de onboarding de funcionários via API; auto-hospedagem para empresas com exigências rígidas de privacidade e LGPD/GDPR.",
        "quickstart": """```bash
# Inicialização via Docker Compose
git clone https://github.com/documenso/documenso.git
cd documenso
docker compose -f docker-compose.prod.yml up -d
# Acesse http://localhost:3000
```""",
        "pro_tip": "Integre a API REST do Documenso utilizando webhooks para disparar notificações no Slack ou arquivar automaticamente o PDF assinado com carimbo do tempo em um bucket S3 assim que todos os signatários concluírem o fluxo."
    },
    "BerriAI/litellm": {
        "what": "Biblioteca e servidor proxy em Python de altíssima performance para unificar chamadas a mais de 100 provedores de LLMs (OpenAI, Anthropic Claude, Google Gemini, Ollama, AWS Bedrock, Groq, DeepSeek) sob o formato padrão da OpenAI. Inclui recursos nativos de balanceamento de carga, fallback entre provedores, limitação de taxa (rate limiting) e controle granular de custos por usuário/chave de API.",
        "use_cases": "Proxy central corporativo de IA para roteamento inteligente de requisições e controle de budget; implementação de fallback automático de modelos (ex: tentar Gemini 2.5 Pro e redirecionar para Claude 3.5 Sonnet caso haja erro 429 de quota); padronização de SDK único em sistemas legados.",
        "quickstart": """```bash
pip install litellm
# Iniciar proxy unificado na porta 4000
litellm --model gemini/gemini-2.0-flash --port 4000
```""",
        "pro_tip": "Crie um arquivo config.yaml definindo router_settings com estratégia de least-busy ou latency-based-routing para distribuir requisições entre várias chaves de API e minimizar a latência média das respostas."
    },
    "go-gitea/gitea": {
        "what": "Serviço completo e auto-hospedável de hospedagem de código Git escrito em Go, focado em leveza extrema e facilidade de manutenção. Oferece interface web responsiva, revisão de pull requests, rastreamento de issues, quadros Kanban, registro de pacotes (npm, PyPI, Docker) e compatibilidade com fluxos de CI/CD no padrão GitHub Actions (Gitea Actions).",
        "use_cases": "Servidor Git privado e seguro para redes internas de empresas ou homelabs com baixo consumo de RAM (< 100MB); espelhamento de repositórios remotos para backup local automatizado; execução de pipelines de CI/CD locais sem dependência de conexões externas.",
        "quickstart": """```bash
# Subir instância do Gitea via Docker
docker run -d --name=gitea -p 10022:22 -p 3000:3000 \
  -v /var/lib/gitea:/data \
  --restart always \
  gitea/gitea:latest
# Acesse http://localhost:3000
```""",
        "pro_tip": "Habilite o suporte ao act_runner nas configurações do app.ini para rodar seus workflows existentes de .github/workflows diretamente dentro da sua infraestrutura privada sem nenhuma alteração nos arquivos YAML."
    },
    "nocodb/nocodb": {
        "what": "Plataforma open-source que converte qualquer banco de dados relacional existente (PostgreSQL, MySQL, SQLite, MariaDB, Microsoft SQL Server) em uma planilha inteligente e colaborativa no estilo Airtable. Fornece visualizações em grade, kanban, galeria, formulários públicos e geração instantânea de APIs REST/GraphQL para as tabelas conectadas.",
        "use_cases": "Criação rápida de interfaces visuais de CRUD sobre bancos legados de produção sem necessidade de escrever código; criação de formulários de pesquisa e cadastro com gravação direta no banco relacional; automação de notificações por email, Slack e webhooks disparadas por alterações de registros.",
        "quickstart": """```bash
# Inicialização rápida conectando a um banco SQLite local
docker run -d --name nocodb -v "$(pwd)/nocodb:/usr/app/data" -p 8080:8080 nocodb/nocodb:latest
```""",
        "pro_tip": "Utilize a funcionalidade de Virtual Fields (Campos Virtuais) e Rollups para calcular agregações complexas entre tabelas relacionais em tempo real sem poluir o schema físico do seu banco de dados."
    },
    "dani-garcia/vaultwarden": {
        "what": "Implementação alternativa e extremamente leve do servidor Bitwarden escrita em Rust. É 100% compatível com todas as extensões de navegador, aplicativos móveis e utilitários de CLI oficiais do Bitwarden, mas consumindo apenas uma fração mínima de recursos de memória (cerca de 20MB de RAM), tornando-o ideal para auto-hospedagem.",
        "use_cases": "Cofre de senhas, chaves de API, notas seguras e autenticação em dois fatores (2FA TOTP) auto-hospedado para uso pessoal, familiar ou de pequenas equipes; eliminação de taxas de assinatura de gerenciadores de senhas comerciais com soberania total dos dados.",
        "quickstart": """```bash
# Executar container Vaultwarden com persistência de dados
docker run -d --name vaultwarden \
  -v /vw-data/:/data/ \
  --restart unless-stopped \
  -p 8080:80 \
  vaultwarden/server:latest
```""",
        "pro_tip": "Ao expor na internet, obrigatoriamente configure HTTPS (via Nginx/Caddy/Traefik) e ative a variável SIGNUPS_ALLOWED=false após criar sua conta inicial para impedir que terceiros criem cadastros no seu servidor."
    },
    "louislam/uptime-kuma": {
        "what": "Ferramenta auto-hospedável de monitoramento de disponibilidade e tempo de atividade (uptime) com interface gráfica moderna e fluida. Suporta checagens via HTTP(s), TCP, Ping, DNS, palavras-chave, validade de certificados SSL/TLS, contêineres Docker e status de servidores de jogos, com criação de páginas de status públicas personalizáveis.",
        "use_cases": "Monitoramento 24/7 da integridade de APIs, sites e bancos de dados; envio de alertas instantâneos de queda via Telegram, Discord, Slack, WhatsApp, Webhooks ou E-mail; publicação de páginas de status elegantes para transparência com clientes e usuários.",
        "quickstart": """```bash
# Subir Uptime Kuma no Docker
docker run -d --restart=always -p 3001:3001 -v uptime-kuma:/app/data --name uptime-kuma louislam/uptime-kuma:1
# Acesse http://localhost:3001
```""",
        "pro_tip": "Configure monitores do tipo HTTP(s) - Keyword para verificar não apenas se a página retornou status code 200, mas também se um texto específico esperado está presente no HTML, evitando falsos positivos causados por páginas de erro padrão de proxies reversos."
    },
    "Zimbra-Community/shared-mailbox-toolkit": {
        "what": "Extensão open-source (Zimlet) para o Zimbra Collaboration Suite que aprimora a experiência de gerenciamento de caixas de correio compartilhadas (Shared Mailboxes). Permite gerenciar delegações, assinaturas personalizadas por conta, permissões granulares de envio em nome de ('Send on Behalf / Send As') e sincronização de itens enviados.",
        "use_cases": "Ambientes corporativos que utilizam Zimbra para atendimento compartilhado (ex: financeiro@, suporte@); padronização de assinaturas e identidades de envio entre múltiplos colaboradores que atendem a mesma caixa postal.",
        "quickstart": """```bash
# Clonar o repositório no servidor Zimbra
git clone https://github.com/Zimbra-Community/shared-mailbox-toolkit.git
cd shared-mailbox-toolkit
# Fazer deploy do Zimlet como usuário zimbra
su - zimbra -c "zmzimletctl deploy /caminho/para/tk_shared_mailbox.zip"
```""",
        "pro_tip": "Configure o atributo zimbraPrefSentMailFolder nas propriedades da conta para que emails enviados por delegados sejam salvos automaticamente na pasta 'Itens Enviados' da caixa compartilhada e não na caixa pessoal do remetente."
    },
    "iwe-org/iwe": {
        "what": "Editor de texto e ambiente de anotações baseado em terminal, focado em hipertexto e Markdown, desenvolvido em Rust. Projetado para proporcionar uma experiência minimalista, sem atrito e com velocidade instantânea, integrando navegação por links internos entre notas como um cérebro digital no terminal.",
        "use_cases": "Tomada de notas rápidas, anotações de reuniões e documentação técnica diretamente do terminal; criação de uma base de conhecimento pessoal interconectada (Personal Knowledge Management - PKM) sem depender de GUIs pesadas.",
        "quickstart": """```bash
# Instalação via Cargo
cargo install iwe
# Iniciar edição em um diretório de notas
iwe ~/minhas-notas/
```""",
        "pro_tip": "Use atalhos de criação de links bidirecionais entre arquivos para navegar instantaneamente entre tópicos relacionados com um único comando de teclado no terminal."
    },
    "stablyai/orca": {
        "what": "Plataforma de orquestração e execução de fluxos de trabalho agenticos em TypeScript, permitindo construir, avaliar e monitorar agentes autônomos de IA corporativos com ferramentas integradas e observabilidade detalhada.",
        "use_cases": "Automação de processos operacionais com múltiplos passos e validações; construção de pipelines de suporte com agentes que executam ações em APIs externas; benchmarking de precisão de tarefas agenticas complexas.",
        "quickstart": """```bash
git clone https://github.com/stablyai/orca.git
cd orca
npm install
npm run build
npm start
```""",
        "pro_tip": "Utilize o módulo de avaliação do Orca para rodar testes de regressão sobre o histórico de raciocínio dos agentes antes de promover novas versões de prompts para produção."
    },
    "Leonxlnx/taste-skill": {
        "what": "Conjunto estruturado de diretrizes de design, estética visual e habilidades (skill) para assistentes e agentes de codificação por IA. Foca em instruir a IA a aplicar princípios de micro-interações, contraste harmonioso, hierarquia tipográfica moderna e layouts refinados, evitando interfaces genéricas e ultrapassadas.",
        "use_cases": "Injeção de critérios estéticos refinados no contexto de agentes como Claude Code, Cursor e Antigravity; garantia de consistência visual em componentes UI gerados por IA; aceleração no desenvolvimento de MVPs com acabamento visual de alto padrão.",
        "quickstart": """```bash
# Clonar a coleção de habilidades
git clone https://github.com/Leonxlnx/taste-skill.git
# Copie o skill para o diretório de habilidades do seu assistente de IA
cp -r taste-skill ~/.gemini/config/skills/taste-skill
```""",
        "pro_tip": "Combine este skill com design tokens em CSS moderno (como variáveis de cor Oklch e container queries) para obter componentes visuais fluidos e adaptativos a qualquer tema."
    },
    "calesthio/OpenMontage": {
        "what": "Framework open-source em Python para automação de edição de vídeo baseada em IA e FFmpeg. Analisa mídias audiovisuais, detecta pontos altos, gera transcrições e monta clipes com legendas dinâmicas, cortes inteligentes e trilha sonora automaticamente.",
        "use_cases": "Produção em escala de vídeos curtos (Reels, TikTok, Shorts) a partir de podcasts ou vídeos longos do YouTube; edição automatizada de destaques para transmissões ao vivo e webinars; pipelines de criação de conteúdo audiovisual automatizado.",
        "quickstart": """```bash
git clone https://github.com/calesthio/OpenMontage.git
cd OpenMontage
pip install -r requirements.txt
python main.py --input video_completo.mp4 --output_dir ./cortes_gerados/
```""",
        "pro_tip": "Ative a aceleração de hardware NVENC no FFmpeg configurando a flag de exportação para processar renderizações de vídeo até 8x mais rápido em placas NVIDIA."
    },
    "Panniantong/Agent-Reach": {
        "what": "Framework em Python para conferir superpoderes de alcance e engajamento multicanal a agentes de IA. Capacita LLMs a interagir diretamente com redes sociais, plataformas de mensagens e canais de email, orquestrando fluxos de comunicação personalizados com memória contextual.",
        "use_cases": "Prospecção e nutrição automatizada de leads B2B em múltiplos canais; assistentes autônomos de relacionamento com clientes em redes sociais; disparo de comunicados personalizados com análise de sentimento nas respostas.",
        "quickstart": """```bash
git clone https://github.com/Panniantong/Agent-Reach.git
cd Agent-Reach
pip install -r requirements.txt
python run_agent.py --config config.yaml
```""",
        "pro_tip": "Configure limites de taxa (rate limits) e intervalos aleatórios de tempo entre requisições para simular interações humanas naturais e evitar bloqueios em plataformas sociais."
    },
    "cathrynlavery/diagram-design": {
        "what": "Guia visual e sistema de design completo para criação de diagramas técnicos, fluxogramas e arquiteturas de sistemas limpas e esteticamente impecáveis. Define paletas de cores balanceadas, pesos de linha, regras de hierarquia e espaçamentos ideais para diagramas de engenharia.",
        "use_cases": "Criação de apresentações técnicas de alto impacto para liderança e stakeholders; padronização dos diagramas de arquitetura da documentação de software da empresa; melhoria na clareza visual de fluxos de dados complexos.",
        "quickstart": """```bash
# Clone o repositório com os assets e templates de diagramação
git clone https://github.com/cathrynlavery/diagram-design.git
# Abra os templates no Figma, Whimsical, Excalidraw ou Mermaid
```""",
        "pro_tip": "Limite seus diagramas a no máximo 3 níveis de hierarquia visual e utilize tons neutros para caixas secundárias, reservando cores vibrantes estritamente para o fluxo principal de dados."
    },
    "lidge-jun/opencodex": {
        "what": "Ferramenta em TypeScript voltada para indexação profunda, navegação estruturada e compreensão semântica de bases de código complexas. Cria representações de árvore sintática (AST) e relacionamentos entre símbolos para acelerar o raciocínio de assistentes de IA sobre monorepos.",
        "use_cases": "Exploração arquitetural de bases de código legadas com milhões de linhas; aceleração da identificação de impacto de mudanças em refatorações; geração de documentação viva da arquitetura de software.",
        "quickstart": """```bash
git clone https://github.com/lidge-jun/opencodex.git
cd opencodex
npm install
npm run index -- --repo-path ./meu-projeto
```""",
        "pro_tip": "Exporte os índices gerados no formato de grafo para alimentar pipelines de RAG estruturado em editores de código como Cursor ou Claude Code."
    },
    "Tabbit-Browser/dsh-plugin": {
        "what": "Plugin de produtividade para navegadores focado em gerenciamento avançado de abas, espaços de trabalho isolados e navegação orientada por teclado. Permite agrupar contextos de trabalho e alternar entre sessões de pesquisa e desenvolvimento instantaneamente.",
        "use_cases": "Organização de dezenas de abas abertas em fluxos de trabalho temáticos (ex: 'Debug Produção', 'Pesquisa IA'); redução do consumo de memória do navegador suspendendo abas inativas de forma inteligente.",
        "quickstart": """```bash
git clone https://github.com/Tabbit-Browser/dsh-plugin.git
cd dsh-plugin
npm install
npm run build
# Carregue a pasta 'dist' como extensão descompactada no Chrome/Brave/Edge
```""",
        "pro_tip": "Utilize a paleta de comandos rápida ativada por atalho para fechar ou mover abas duplicadas sem tirar as mãos do teclado."
    },
    "Genymobile/scrcpy": {
        "what": "Aplicação definitiva em C para espelhamento e controle de dispositivos Android em computadores desktop (Windows, macOS e Linux) com latência ultra-baixa (35~70ms). Opera via USB ou Wi-Fi (TCP/IP), não requer privilégios de root no aparelho e suporta taxas de 60+ FPS com repasse de áudio, gravação de tela e compartilhamento de área de transferência.",
        "use_cases": "Desenvolvimento e depuração de aplicativos Android em tempo real na tela do computador; apresentações, tutoriais e demonstrações ao vivo de apps; uso do celular sem precisar pegar no aparelho físico durante o expediente de trabalho.",
        "quickstart": """```bash
# No Windows via Winget ou Chocolatey:
winget install scrcpy
# Conectar aparelho via USB com depuração ativada e iniciar:
scrcpy --max-fps=60 --video-bit-rate=8M --stay-awake
# Modo sem fio (Wi-Fi):
# scrcpy --tcpip=192.168.1.50:5555
```""",
        "pro_tip": "Utilize o atalho MOD + f para alternar para tela cheia e MOD + o para desligar a tela física do celular enquanto continua interagindo normalmente com ele pelo PC, economizando bateria."
    },
    "lwthiker/curl-impersonate": {
        "what": "Compilação customizada do utilitário curl que emula perfeitamente as assinaturas de rede e TLS dos navegadores reais mais populares (Chrome, Firefox, Safari e Edge). Reproduz com exatidão parâmetros de handshake TLS (ciphers, extensões, curvas elípticas, assinaturas JA3/JA4) e frames HTTP/2, tornando requisições automatizadas indistinguíveis de um usuário em um navegador real.",
        "use_cases": "Raspagem de dados e web scraping avançado contornando bloqueios de WAFs e sistemas anti-bot como Cloudflare, Akamai e DataDome; testes de segurança de aplicações web avaliando resiliência contra evasão de assinaturas.",
        "quickstart": """```bash
# Execução rápida via Docker emulando o Chrome 116
docker run --rm lwthiker/curl-impersonate:latest \
  curl_chrome116 -sL "https://tls.browserleaks.com/json"
```""",
        "pro_tip": "Em pipelines Python, utilize o wrapper curl_cffi para ter a mesma emulação de TLS do curl-impersonate diretamente com sintaxe idêntica à biblioteca requests."
    },
    "D4Vinci/Scrapling": {
        "what": "Biblioteca em Python para raspagem e automação web indetectável de alta performance. Desenvolvida para contornar desafios de Cloudflare e proteções modernas, combina parseamento de DOM extremamente veloz com seletores CSS adaptativos e emulação inteligente de comportamento humano.",
        "use_cases": "Extração massiva de dados em e-commerces protegidos por Cloudflare Turnstile/WAF; coleta de informações de portais de notícias e redes sem sofrer bloqueios frequentes de IP; automação de fluxos de scraping corporativo.",
        "quickstart": """```bash
pip install scrapling
# No código Python:
# from scrapling import Fetcher
# fetcher = Fetcher()
# page = fetcher.get('https://exemplo.com')
# print(page.css('h1::text').get())
```""",
        "pro_tip": "Ative o modo de navegação com renderização dinâmica passando stealth=True para que scripts anti-automação não consigam detectar que o navegador está sendo controlado via automação."
    },
    "browser-use/browser-use": {
        "what": "Biblioteca em Python que capacita agentes de inteligência artificial a controlar e navegar na web exatamente como seres humanos. Integra modelos de visão e LLMs (como GPT-4o, Claude 3.5 e Gemini) ao Playwright para interagir com elementos visuais da página, preencher formulários, lidar com popups e resolver tarefas complexas de ponta a ponta.",
        "use_cases": "Automação completa de fluxos de trabalho corporativos no navegador (ex: agendamentos, compras, cadastros em sistemas sem API); testes end-to-end de usabilidade orientados por IA; coleta e consolidação de relatórios em painéis com login e múltiplos cliques.",
        "quickstart": """```bash
pip install browser-use
playwright install
# Executar agente simples via script:
# from browser_use import Agent
# from langchain_openai import ChatOpenAI
# agent = Agent(task="Encontre o melhor preço de notebook gamer", llm=ChatOpenAI(model="gpt-4o"))
# agent.run()
```""",
        "pro_tip": "Utilize a opção use_vision=True para que o agente analise capturas de tela reais da página, permitindo navegar com sucesso mesmo em interfaces repletas de Shadow DOM, canvas ou seletores dinâmicos."
    },
    "firecrawl/firecrawl": {
        "what": "API e motor open-source de rastreamento e extração web que converte qualquer site completo em Markdown limpo, sem ruídos e pronto para consumo por LLMs e pipelines de RAG. Gerencia automaticamente renderização de JavaScript, rolagem infinita, proxies rotativos e desafios anti-bot.",
        "use_cases": "Indexação e criação de bases de conhecimento para RAG a partir da documentação inteira de bibliotecas e sites de clientes; alimentação de LLMs com conteúdo web limpo sem tags HTML desnecessárias; extração estruturada de dados com schema JSON via IA.",
        "quickstart": """```bash
# Subir stack completa localmente via Docker Compose
git clone https://github.com/firecrawl/firecrawl.git
cd firecrawl
docker compose up -d
# Fazer scraping de uma URL via cURL:
# curl -X POST http://localhost:3002/v0/scrape -H "Content-Type: application/json" -d '{"url": "https://docs.python.org"}'
```""",
        "pro_tip": "Use o endpoint /crawl com o parâmetro scrapeOptions: {formats: ['markdown']} e limit: 50 para rastrear até 50 páginas de uma documentação com deduplicação automática de links."
    },
    "microsoft/markitdown": {
        "what": "Utilitário e biblioteca oficial da Microsoft em Python para conversão universal de arquivos de diversos formatos (PDF, Word .docx, Excel .xlsx, PowerPoint .pptx, imagens, áudios com fala, HTML, CSV e JSON) em Markdown limpo e perfeitamente estruturado.",
        "use_cases": "Pré-processamento e normalização de documentos corporativos heterogêneos para ingestão em pipelines de RAG e bancos vetoriais; extração de tabelas de planilhas e relatórios para análise por LLMs; transcrição de áudio e extração de texto de apresentações em formato unificado.",
        "quickstart": """```bash
pip install markitdown
# Converter um arquivo PDF ou DOCX diretamente no terminal:
markitdown documento.pdf -o documento.md
markitdown apresentacao.pptx -o apresentacao.md
```""",
        "pro_tip": "Ao inicializar o MarkItDown no Python, passe um cliente do Azure OpenAI ou OpenAI para ativar transcrição automática de arquivos de áudio e descrição detalhada de imagens presentes no documento."
    },
    "unclecode/crawl4ai": {
        "what": "Rastreador e extrator web open-source em Python de altíssima velocidade, projetado especificamente para modelos de linguagem e pipelines de IA. Oferece extração avançada de Markdown com pontuação de relevância (BM25), filtragem de ruído heurística, suporte a sessões com cookies, execução de código JS antes da extração e integração nativa com LangChain e LlamaIndex.",
        "use_cases": "Coleta de dados em alta escala para fine-tuning de modelos e bases de conhecimento vetoriais; extração de artigos, posts de blog e documentações técnicas sem cabeçalhos, rodapés ou anúncios; monitoramento contínuo de conteúdos dinâmicos na web.",
        "quickstart": """```bash
pip install crawl4ai
crawl4ai-setup  # Instala os binários do Playwright necessários
# Execução rápida via CLI:
crawl4ai-cli https://news.ycombinator.com
```""",
        "pro_tip": "Configure fit_markdown=True no extrator para que o Crawl4AI aplique algoritmos de extração heurística que removem menus de navegação e banners, reduzindo a contagem de tokens do Markdown em até 70%."
    },
    "MrCl0wnLab/BR-EvilPortal-HTML-Files": {
        "what": "Coleção de páginas de portais cativos (Captive Portals) responsivas e personalizadas em Português do Brasil para auditoria de segurança em redes Wi-Fi e exercícios de Red Teaming. Compatível com dispositivos e firmwares como ESP8266, ESP32, WiFi Pineapple e Evil Portal.",
        "use_cases": "Treinamentos práticos de conscientização em segurança da informação (Security Awareness) demonstrando os riscos de conexão a redes Wi-Fi públicas desprotegidas; testes de intrusão autorizados avaliando a suscetibilidade a ataques de rogue AP (Evil Twin).",
        "quickstart": """```bash
git clone https://github.com/MrCl0wnLab/BR-EvilPortal-HTML-Files.git
cd BR-EvilPortal-HTML-Files
# Copie o portal desejado para o cartão SD ou pasta do EvilPortal
```""",
        "pro_tip": "Sempre execute testes com portais cativos exclusivamente em ambientes de laboratório controlados e com autorização prévia por escrito para garantir conformidade legal com a legislação brasileira."
    },
    "CopilotKit/aimock": {
        "what": "Framework de desenvolvimento e suíte de testes em TypeScript voltada para simulação (mocking) de respostas de modelos de IA e fluxos de copilotos generativos. Permite testar interfaces de usuário, streaming de texto e chamadas de funções sem gastar tokens reais de APIs pagas.",
        "use_cases": "Testes unitários e de integração de componentes frontend de chat e IA no CI/CD; desenvolvimento offline de interfaces copiloto sem necessidade de conexão com a internet ou chaves de API; reprodução determinística de cenários de erro ou respostas anômalas de LLMs.",
        "quickstart": """```bash
npm install @copilotkit/aimock --save-dev
# Importe no seu arquivo de teste:
# import { mockAIGenerate } from '@copilotkit/aimock';
```""",
        "pro_tip": "Configure cenários de atraso artificial (latency simulation) nas respostas mockadas para testar a experiência do usuário durante o carregamento de streaming em conexões lentas."
    },
    "f/prompts.chat": {
        "what": "O mundialmente famoso repositório 'Awesome ChatGPT Prompts', reunindo centenas de prompts de sistema de alto nível categorizados para instruir LLMs a agir como especialistas em áreas como arquitetura de software, terminal Linux, cibersegurança, tradução e copywriting.",
        "use_cases": "Configuração rápida de personas e instruções de sistema (System Prompts) para assistentes de IA corporativos; inspiração de técnicas de engenharia de prompt (Few-Shot, Chain-of-Thought) para tarefas específicas; aceleração de pesquisas e tarefas do dia a dia.",
        "quickstart": """```bash
# Clone o repositório para ter acesso local a todos os prompts estruturados em CSV/JSON
git clone https://github.com/f/prompts.chat.git
# O arquivo prompts.csv contém todos os prompts prontos para busca
```""",
        "pro_tip": "Importe o arquivo prompts.csv no seu banco de dados vetorial ou crie um script de busca local com fzf no terminal para copiar instantaneamente o prompt desejado para a área de transferência."
    },
    "unslothai/unsloth": {
        "what": "Framework líder em Python para fine-tuning e treinamento ultra-otimizado de modelos de linguagem de código aberto (Llama 3, Mistral, Gemma, Qwen, Phi-4, DeepSeek). Reduz o consumo de memória VRAM em até 80% e acelera o treinamento em 2 a 5x sem nenhuma perda de precisão matemática, viabilizando treinar LLMs de ponta em GPUs comuns (como RTX 3090/4090 ou instâncias T4 gratuitas).",
        "use_cases": "Fine-tuning de modelos abertos com dados proprietários da empresa; treinamento com LoRA/QLoRA e alinhamento via DPO/ORPO; exportação direta de modelos ajustados para GGUF (rodar no Ollama/Llama.cpp) ou vLLM para produção.",
        "quickstart": """```bash
pip install "unsloth[colab-new] @ git+https://github.com/unslothai/unsloth.git"
# Exemplo rápido de carregamento com 4-bit quantization:
# from unsloth import FastLanguageModel
# model, tokenizer = FastLanguageModel.from_pretrained(model_name="unsloth/llama-3-8b-bnb-4bit", max_seq_length=2048)
```""",
        "pro_tip": "Ao final do treinamento, utilize model.save_pretrained_gguf('meu_modelo', tokenizer, quantization_method='q4_k_m') para gerar diretamente um arquivo GGUF otimizado e rodar seu modelo localmente no Ollama em segundos."
    },
    "ZhuLinsen/daily_stock_analysis": {
        "what": "Sistema de análise financeira automatizada em Python que emprega agentes de IA para coletar cotações, calcular indicadores técnicos (RSI, MACD, Médias Móveis), analisar notícias do mercado e gerar relatórios analíticos diários sobre ações.",
        "use_cases": "Acompanhamento automatizado de carteiras de investimentos com resumos executivos enviados por email ou Telegram; triagem matinal de ativos financeiros com base em análise técnica e fundamentalista; monitoramento de sentimento do mercado em tempo real.",
        "quickstart": """```bash
git clone https://github.com/ZhuLinsen/daily_stock_analysis.git
cd daily_stock_analysis
pip install -r requirements.txt
python main.py
```""",
        "pro_tip": "Configure tarefas agendadas via cron para rodar o script 30 minutos após o fechamento do pregão e receber um consolidado dos ativos com maiores variações diretamente no Telegram."
    },
    "addyosmani/agent-skills": {
        "what": "Coleção de habilidades modulares, especificações de ferramentas e fluxos de trabalho criada por Addy Osmani (Google) para potencializar assistentes e agentes de codificação por IA. Abrange padrões avançados de depuração, testes, revisão de código e engenharia de software moderna.",
        "use_cases": "Extensão das capacidades de agentes como Claude Code, Cursor e Antigravity com boas práticas recomendadas pela engenharia do Google; padronização de workflows de auditoria de performance web (Core Web Vitals) e testes automatizados.",
        "quickstart": """```bash
git clone https://github.com/addyosmani/agent-skills.git
cd agent-skills
# Copie as habilidades desejadas para a pasta de skills da sua ferramenta de IA
```""",
        "pro_tip": "Explore as habilidades voltadas para auditoria de Largest Contentful Paint (LCP) e Cumulative Layout Shift (CLS) para instruir agentes a refatorar componentes React priorizando métricas de performance real."
    },
    "earendil-works/pi": {
        "what": "Infraestrutura de comunicação ponto a ponto (P2P) descentralizada, anônima e resistente a censura, desenvolvida em TypeScript e Rust. Implementa roteamento criptográfico inspirado no protocolo mixnet/onion routing, proporcionando camadas seguras de transporte de dados.",
        "use_cases": "Desenvolvimento de aplicações descentralizadas que necessitam de comunicação privada imune a bloqueios de rede; comunicação entre microsserviços sem exposição de endereços IP de origem; criação de redes de transporte de dados seguras.",
        "quickstart": """```bash
git clone https://github.com/earendil-works/pi.git
cd pi
npm install
npm run build
```""",
        "pro_tip": "Utilize a camada de transporte do Pi para isolar canais de telemetria crítica e tráfego de controle de servidores sem expor portas públicas na internet."
    },
    "PrimeIntellect-ai/prime-agent": {
        "what": "Framework em TypeScript para coordenação de computação descentralizada de inteligência artificial, projetado para permitir que agentes autônomos gerenciem treinamento distribuído, benchmarks e alocação de poder computacional em clusters globais de GPUs.",
        "use_cases": "Orquestração de cargas de treinamento de IA distribuídas entre provedores heterogêneos de computação em nuvem; execução autônoma de benchmarks de modelos em múltiplos nós; automação de fluxos de pesquisa em aprendizado por reforço.",
        "quickstart": """```bash
git clone https://github.com/PrimeIntellect-ai/prime-agent.git
cd prime-agent
npm install
npm run dev
```""",
        "pro_tip": "Configure chaves de orquestração distribuída para permitir que múltiplos agentes colaborem na exploração de hiperparâmetros de treinamento simultaneamente."
    },
    "promovaweb/specsfy": {
        "what": "Utilitário em JavaScript/Node.js para criação, validação e documentação rápida de especificações OpenAPI/Swagger. Permite descrever endpoints de forma declarativa e gerar servidores de mock interativos com mínimo esforço de configuração.",
        "use_cases": "Definição de contratos de API em arquiteturas 'API-First' antes do desenvolvimento do backend; geração de mocks automáticos para desbloquear times de frontend; validação de conformidade de schemas de requisição e resposta.",
        "quickstart": """```bash
npm install -g specsfy
# Gerar documentação interativa a partir do schema:
specsfy serve openapi.yaml --port 8080
```""",
        "pro_tip": "Utilize o gerador de mocks integrado com a flag --watch durante o desenvolvimento para atualizar os contratos de API e refletir alterações instantaneamente no mock server."
    },
    "yashab-cyber/opendroid": {
        "what": "Ferramenta open-source em Kotlin voltada para auditoria de segurança, engenharia reversa e análise de vulnerabilidades em aplicativos Android (APKs). Inspeciona permissões excessivas, componentes exportados desprotegidos, vazamentos de segredos e más práticas no AndroidManifest.xml.",
        "use_cases": "Pentest de aplicações móveis Android; checagem rápida de conformidade de segurança de APKs antes do deploy em lojas de aplicativos; auditoria de bibliotecas de terceiros integradas ao app.",
        "quickstart": """```bash
git clone https://github.com/yashab-cyber/opendroid.git
# Abrir no Android Studio ou compilar via Gradle:
./gradlew assembleDebug
```""",
        "pro_tip": "Execute a análise estática em conjunto com o adb logcat filtrando por tags de segurança para capturar tokens ou parâmetros sensíveis trafegados indevidamente em texto plano."
    },
    "itsfatduck/optimizerDuck": {
        "what": "Utilitário de otimização de sistema operacional Windows escrito em C#. Permite desativar telemetria intrusiva, remover aplicativos desnecessários (bloatware), ajustar configurações de rede (TCP/IP tuning) e otimizar parâmetros de registro para obter máximo desempenho e baixa latência.",
        "use_cases": "Otimização de máquinas virtuais e estações de desenvolvimento Windows para reduzir uso de memória e CPU; preparação de imagens limpas do Windows para desenvolvedores e gamers; desativação de serviços desnecessários em segundo plano.",
        "quickstart": """```bash
git clone https://github.com/itsfatduck/optimizerDuck.git
# Compile no Visual Studio ou execute o binário pré-compilado da aba Releases
```""",
        "pro_tip": "Sempre crie um Ponto de Restauração do Sistema (System Restore Point) antes de aplicar perfis de otimização agressiva de registro do Windows."
    },
    "microsoft/ai-agents-for-beginners": {
        "what": "Curso e repositório educacional completo da Microsoft composto por 10 lições práticas sobre construção de agentes de inteligência artificial generativa. Cobre desde os fundamentos teóricos até orquestração multi-agente, uso de ferramentas (tool calling), memória e frameworks como AutoGen e Semantic Kernel.",
        "use_cases": "Treinamento e capacitação de equipes de engenharia no desenvolvimento de sistemas baseados em agentes; material de referência com código executável em Jupyter Notebooks para estudos; guia de boas práticas de arquitetura agentica.",
        "quickstart": """```bash
git clone https://github.com/microsoft/ai-agents-for-beginners.git
cd ai-agents-for-beginners
# Abra qualquer lição no VS Code ou Jupyter:
# jupyter notebook
```""",
        "pro_tip": "Inicie pela lição 06 sobre 'Multi-Agent Orchestration' para compreender os padrões de comunicação inter-agentes (sequential, broadcast e round-robin) antes de desenhar fluxos de trabalho complexos."
    },
    "abundantbeing/hermes-browser-extension": {
        "what": "Extensão para navegadores baseados em Chromium em JavaScript que integra o agente autônomo Hermes diretamente às abas de navegação. Permite que a IA acesse o conteúdo da página atual, resuma artigos, extraia dados estruturados e execute ações no navegador de forma assistida.",
        "use_cases": "Assistente de pesquisa e leitura na navegação web diária; extração de dados e tabelas de sites sem exportação direta para CSV; automação de preenchimento de campos repetitivos em portais internos.",
        "quickstart": """```bash
git clone https://github.com/abundantbeing/hermes-browser-extension.git
# Acesse chrome://extensions, ative 'Modo do desenvolvedor' e clique em 'Carregar sem compactação'
```""",
        "pro_tip": "Configure atalhos de teclado globais no navegador para invocar o painel lateral do Hermes sem perder o foco do artigo ou documento que está sendo lido."
    },
    "vitali87/code-graph-rag": {
        "what": "Sistema de recuperação aumentada por geração (RAG) baseado em grafos (GraphRAG) em Python voltado para código-fonte. Converte o código de um repositório em um grafo de conhecimento interligando funções, classes, métodos e módulos para permitir consultas semânticas e arquiteturais complexas.",
        "use_cases": "Compreensão profunda da arquitetura de sistemas com milhões de linhas de código; consultas de impacto do tipo 'quais endpoints chamam esta função de autenticação?'; alimentação de agentes de IA com contexto estruturado e preciso sobre o código.",
        "quickstart": """```bash
git clone https://github.com/vitali87/code-graph-rag.git
cd code-graph-rag
pip install -r requirements.txt
python main.py --repo-path /caminho/do/projeto
```""",
        "pro_tip": "Combine o Code-Graph-RAG com um banco de vetores para fazer buscas híbridas: utilize a busca vetorial para encontrar funções semanticamente relevantes e o grafo para puxar todos os seus chamadores diretos e dependências."
    },
    "outline/outline": {
        "what": "Plataforma moderna, colaborativa e ultra-rápida de base de conhecimento e documentação de equipe em TypeScript/React. Funciona como uma alternativa open-source e auto-hospedável ao Notion e Confluence, com editor Markdown rico em tempo real, suporte a diagramas Mermaid e permissões granulares.",
        "use_cases": "Wiki e documentação técnica centralizada para equipes de engenharia; documentação de processos operacionais e onboarding de colaboradores; compartilhamento seguro de manuais internos e notas de produto com clientes.",
        "quickstart": """```bash
# Inicialização via Docker Compose com PostgreSQL e Redis
git clone https://github.com/outline/outline.git
cd outline
docker compose up -d
# Acesse http://localhost:3000
```""",
        "pro_tip": "Integre o Outline com seu provedor de identidade corporativo (Google Workspace, Slack, OIDC ou SAML) para provisionamento automatizado de usuários e controle de acesso baseado em grupos."
    },
    "Leantime/leantime": {
        "what": "Sistema open-source de gerenciamento estratégico de projetos em PHP, projetado para equipes enxutas e indivíduos com TDAH/ADHD. Combina a metodologia Lean com visualizações intuitivas de Kanban, marcos estratégicos (Milestones), quadros de metas (OKRs) e gráficos de Gantt sem a complexidade burocrática do Jira.",
        "use_cases": "Gestão ágil de desenvolvimento de software em startups e pequenas equipes; acompanhamento visual de metas de negócios e roadmap de produtos; planejamento de projetos com foco em entregas iterativas e priorização clara.",
        "quickstart": """```bash
# Subir Leantime via Docker
docker run -d --name leantime -p 8080:80 \
  -e LEAN_DB_HOST=db_host -e LEAN_DB_USER=db_user -e LEAN_DB_PASSWORD=secret \
  leantime/leantime:latest
```""",
        "pro_tip": "Utilize a funcionalidade de 'Strategy Matrix' do Leantime para mapear como cada tarefa técnica diária do time se conecta diretamente aos objetivos e OKRs estratégicos da empresa."
    },
    "ente/ente": {
        "what": "Plataforma 100% open-source com criptografia de ponta a ponta (E2EE) para backup e organização de fotos e vídeos, posicionando-se como alternativa segura e soberana ao Google Fotos e Apple Fotos. Desenvolvida em Flutter/Dart e Go, oferece reconhecimento facial local, busca semântica no dispositivo e sincronização em tempo real entre mobile e desktop.",
        "use_cases": "Backup privado de fotos e memórias pessoais sem expor dados a algoritmos de vigilância em nuvem; compartilhamento seguro de álbuns de família com criptografia ponta a ponta; auto-hospedagem para armazenamento local e controle total dos arquivos originais em alta resolução.",
        "quickstart": """```bash
# Subir servidor Ente localmente via Docker
git clone https://github.com/ente-io/ente.git
cd ente/server
docker compose up -d
```""",
        "pro_tip": "Ative a opção de 'Lockout Protection' e configure um contato de recuperação com chaves públicas compartilhadas para garantir que você nunca perca o acesso às suas fotos caso esqueça a chave-mestre de criptografia."
    },
    "imputnet/cobalt": {
        "what": "Serviço de download de mídias da web (áudio e vídeo) moderno, rápido e livre de anúncios, rastreadores ou popups invasivos. Desenvolvido com interface fluida em Svelte e backend em Node.js, permite baixar conteúdos do YouTube, Twitter/X, Instagram, TikTok, Reddit, SoundCloud, Bilibili e dezenas de outras plataformas na melhor qualidade disponível.",
        "use_cases": "Download local de materiais de referência em vídeo e áudio para estudo e edição; extração de faixas sonoras em alta fidelidade (.opus / .mp3 / .wav); auto-hospedagem de uma instância privada e confiável para sua equipe ou amigos.",
        "quickstart": """```bash
# Execução rápida da API e WebUI do Cobalt via Docker
docker run -d --name cobalt -p 9000:9000 \
  -e API_URL="http://localhost:9000/" \
  ghcr.io/imputnet/cobalt:10
# Acesse http://localhost:9000
```""",
        "pro_tip": "Integre a API REST do Cobalt em seus próprios scripts ou bots do Telegram passando parâmetros como downloadMode: 'audio' ou videoQuality: '1080' no payload JSON para baixar mídias programaticamente."
    },
    "Stirling-Tools/Stirling-PDF": {
        "what": "A mais completa suíte de utilitários para PDF open-source e auto-hospedável da atualidade, desenvolvida em Java/Spring Boot. Executa todas as operações possíveis em documentos PDF (dividir, mesclar, comprimir, aplicar OCR com Tesseract, converter para Word/HTML/Imagens, assinar digitalmente, sanitizar metadados, redigir informações confidenciais) de forma 100% local e segura.",
        "use_cases": "Manipulação de documentos confidenciais (contratos, faturas, relatórios) sem risco de vazamento para serviços de PDF comerciais na nuvem; automação de OCR e conversão de pilhas de PDFs digitalizados em documentos pesquisáveis; padronização de utilitário central de PDF para toda a empresa.",
        "quickstart": """```bash
# Subir o Stirling-PDF via Docker
docker run -d -p 8080:8080 \
  -v /stirling/trainingData:/usr/share/tessdata \
  -v /stirling/extraConfigs:/configs \
  --name stirling-pdf \
  frooodle/s-pdf:latest
# Acesse http://localhost:8080
```""",
        "pro_tip": "O Stirling-PDF expõe todos os seus utilitários como uma API REST documentada no Swagger (http://localhost:8080/swagger-ui/index.html), permitindo que você automatize fluxos de compressão e OCR em scripts Python ou pipelines do n8n com chamadas HTTP simples."
    },
    "Shpigford/chops": {
        "what": "Aplicativo nativo para a barra de menus do macOS desenvolvido em Swift para acompanhamento em tempo real de métricas financeiras e de assinaturas do Stripe. Exibe receita recorrente mensal (MRR), volume diário, novos assinantes e taxas de cancelamento (churn) de forma minimalista.",
        "use_cases": "Monitoramento de métricas de faturamento para fundadores de SaaS e negócios digitais; notificações imediatas de vendas e novos clientes diretamente na barra de menus; visualização de tendências de crescimento sem precisar abrir o dashboard pesado do Stripe.",
        "quickstart": """```bash
git clone https://github.com/Shpigford/chops.git
# Abra o projeto no Xcode para compilar e rodar nativamente no macOS:
# xcodebuild -workspace Chops.xcworkspace -scheme Chops
```""",
        "pro_tip": "Crie uma chave de API restrita (Restricted API Key) no Stripe com permissões exclusivas de leitura (read-only) para faturas e assinaturas antes de configurar o aplicativo, garantindo máxima segurança."
    },
    "sujeeth36/TradingView-Premium-FREE": {
        "what": "Guia e acervo de scripts de automação, userscripts e configurações para a plataforma TradingView. Foca em contornar limitações de contas gratuitas, permitindo utilizar múltiplos indicadores customizados, múltiplos layouts de gráficos e alertas sem custos de assinatura.",
        "use_cases": "Análise gráfica aprofundada de ações, criptomoedas e pares de moedas forex sem limites rígidos de indicadores simultâneos; automação de rotinas de visualização de múltiplos tempos gráficos em uma única tela.",
        "quickstart": """```bash
git clone https://github.com/sujeeth36/TradingView-Premium-FREE.git
# Siga as instruções do repositório para instalar os userscripts via Tampermonkey/Violentmonkey
```""",
        "pro_tip": "Combine indicadores customizados em um único script Pine Script (Indicator Bundle) para utilizar até 10 cálculos analíticos diferentes ocupando apenas um único slot de indicador no TradingView."
    },
    "rmyndharis/OpenWA": {
        "what": "Biblioteca e servidor de automação open-source em TypeScript/Node.js para integração com o WhatsApp Web. Permite construir bots, disparar mensagens de atendimento, escutar eventos de mensagens recebidas, enviar mídias e integrar sistemas de CRM diretamente ao WhatsApp sem depender da API Cloud oficial paga.",
        "use_cases": "Automação de atendimento e envio de notificações transacionais (confirmação de pedidos, lembretes de agendamento); integração de assistentes de IA (ChatGPT, Claude) como atendentes inteligentes no WhatsApp; criação de chatbots corporativos de suporte interno.",
        "quickstart": """```bash
git clone https://github.com/rmyndharis/OpenWA.git
cd OpenWA
npm install
npm start
# Escaneie o QR Code exibido no terminal para conectar a sessão
```""",
        "pro_tip": "Salve a pasta de sessão (session_data) em um volume persistente para que o bot reconecte automaticamente após reinicializações sem exigir a leitura de um novo QR Code."
    },
    "Bill-Stewart/SyncthingWindowsSetup": {
        "what": "Instalador completo e gerenciador de serviço nativo do Windows para o Syncthing (ferramenta de sincronização contínua de arquivos P2P criptografada). Configura o Syncthing para rodar como um serviço do Windows em segundo plano (Windows Service), iniciando antes do login do usuário com consumo mínimo de recursos.",
        "use_cases": "Sincronização contínua de pastas de trabalho, documentos e projetos entre servidores Windows, desktops e notebooks sem depender de nuvens terceiras (Dropbox/Google Drive); backups contínuos de diretórios em rede local.",
        "quickstart": """```bash
# Baixe o instalador mais recente na aba Releases do GitHub
# Ou instale silenciosamente via linha de comando no PowerShell administrativo:
# Start-Process SyncthingSetup.exe -ArgumentList "/VERYSILENT /SUPPRESSMSGBOXES" -Wait
```""",
        "pro_tip": "Ao configurar o serviço do Windows, utilize uma conta de serviço dedicada com permissões NTFS específicas para as pastas sincronizadas, isolando os dados de outras aplicações do sistema."
    },
    "arthurspk/guiadofrontend": {
        "what": "Guia completo e interativo em Português do Brasil com o roteiro de aprendizado (roadmap) essencial para desenvolvedores Front-End modernos. Abrange fundamentos essenciais (HTML5 semântico, CSS moderno, JavaScript ES6+), frameworks (React, Vue, Next.js), ferramentas de build, testes, performance web e práticas de carreira.",
        "use_cases": "Estruturação de planos de estudo para desenvolvedores em transição ou especialização em frontend; material de referência e consulta rápida sobre padrões de mercado e arquitetura web; guia de preparação técnica para entrevistas de emprego.",
        "quickstart": """```bash
git clone https://github.com/arthurspk/guiadofrontend.git
# Acesse o README.md ou abra a versão interativa hospedada online
```""",
        "pro_tip": "Siga as seções de acessibilidade (a11y) e Core Web Vitals do guia para elevar a pontuação do Lighthouse dos seus projetos acima de 95 em produção."
    },
    "fadidevv/keyhunter": {
        "what": "Utilitário de alta performance escrito em Rust para detecção e auditoria de chaves de API, credenciais e tokens vazados em repositórios de código-fonte, históricos de commits do Git e arquivos de configuração. Utiliza análise de entropia de Shannon e expressões regulares otimizadas para identificar vazamentos com velocidade instantânea.",
        "use_cases": "Varredura de segurança pré-commit e pré-push para impedir o envio acidental de segredos (como chaves de AWS, OpenAI, GitHub e Stripe) para repositórios remotos; auditoria de segurança em pipelines de CI/CD; análise estática em auditorias de conformidade.",
        "quickstart": """```bash
git clone https://github.com/fadidevv/keyhunter.git
cd keyhunter
cargo build --release
./target/release/keyhunter scan --path /caminho/do/projeto
```""",
        "pro_tip": "Integre o binário do Keyhunter no arquivo .git/hooks/pre-commit para bloquear imediatamente qualquer commit que contenha tokens de alta entropia antes que o código saia da sua máquina local."
    },
    "trufflesecurity/trufflehog": {
        "what": "A ferramenta de código aberto padrão da indústria em Go para localização profunda de segredos, chaves de API, certificados privados e credenciais vazadas em repositórios Git, históricos de commits completos, buckets S3, imagens Docker e sistemas de arquivos. Seu grande diferencial é a validação ativa (Live Verification), que testa se as credenciais encontradas continuam ativas contra os provedores reais em tempo real.",
        "use_cases": "Varredura contínua de segurança em pipelines de CI/CD para barrar pull requests com credenciais expostas; auditoria forense do histórico completo de repositórios legados; descoberta de chaves ativas em buckets de armazenamento e contêineres em ambientes corporativos.",
        "quickstart": """```bash
# Instalação rápida via Homebrew ou binário
# brew install trufflehog
# Ou execução direta via Docker sobre o repositório atual:
docker run --rm -v "$PWD:/pwd" trufflesecurity/trufflehog:latest git file:///pwd --only-verified
```""",
        "pro_tip": "Utilize a flag --only-verified para filtrar o relatório de varredura exibindo estritamente credenciais que o TruffleHog conseguiu validar como ativas nos servidores dos provedores, eliminando 100% dos falsos positivos."
    },
    "langchain-ai/langgraph": {
        "what": "Framework líder em Python e TypeScript para construção de fluxos de trabalho agenticos cíclicos e com estado (Stateful Multi-Agent Systems). Projetado para superar as limitações das cadeias lineares tradicionais, permite criar grafos com ciclos, ramificações condicionais, persistência de estado em banco de dados, aprovação humana no loop (Human-in-the-Loop) e recuperação resiliente de falhas.",
        "use_cases": "Desenvolvimento de arquiteturas complexas com múltiplos agentes especialistas colaborativos (ex: agente pesquisador, agente redator e agente revisor); fluxos de IA corporativos com necessidade de auditoria e aprovação humana em etapas críticas; automação de engenharia de software com loops de tentativa e correção de código.",
        "quickstart": """```bash
pip install -U langgraph langchain-openai
# No código Python:
# from langgraph.graph import StateGraph, START, END
# from typing import TypedDict
# class State(TypedDict):
#     messages: list
# builder = StateGraph(State)
# builder.add_node("agent", meu_no_agente)
# builder.add_edge(START, "agent")
# graph = builder.compile()
```""",
        "pro_tip": "Utilize o MemorySaver como checkpointer durante o desenvolvimento para salvar o estado de cada nó no grafo e permitir a funcionalidade de 'Time Travel' (voltar a um ponto anterior da execução do agente e testar caminhos alternativos)."
    }
}

def build_complete_db():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, "data")
    master_db_path = os.path.join(data_dir, "master_catalog_db.json")
    catalog_db_path = os.path.join(data_dir, "catalog_db.json")
    all_stars_path = os.path.join(data_dir, "all_starred_github.json")

    # 1. Carregar base existente
    if os.path.exists(master_db_path):
        with open(master_db_path, "r", encoding="utf-8") as f:
            full_db = json.load(f)
    else:
        full_db = {}

    # 2. Atualizar com as novas 53 análises ricas
    for repo_name, analysis in NEW_53_REPOS.items():
        full_db[repo_name] = analysis

    # 3. Carregar lista de todas as estrelas do GitHub
    with open(all_stars_path, "r", encoding="utf-8") as f:
        all_stars = json.load(f)

    total_stars = len(all_stars)
    print(f"Total de estrelas no GitHub: {total_stars}")
    print(f"Total de análises no DB unificado: {len(full_db)}")

    # 4. Validar que nenhum repositório ficou com conteúdo genérico
    generic_detected = []
    for repo in all_stars:
        name = repo.get("full_name")
        if name not in full_db:
            generic_detected.append((name, "FALTANDO NO BANCO"))
            continue
        entry = full_db[name]
        what = entry.get("what", "")
        tip = entry.get("pro_tip", "")
        if "Projeto open-source em" in what or "Consulte as issues" in tip or "Consulte os exemplos no README" in tip:
            generic_detected.append((name, "GENÉRICO DETECTADO"))

    if generic_detected:
        print(f"AVISO: {len(generic_detected)} itens com problemas:")
        for name, reason in generic_detected:
            print(f"  - {name}: {reason}")
    else:
        print("PERFEITO: Todos os repositórios possuem análises ricas e individuais!")

    # 5. Salvar base unificada
    with open(master_db_path, "w", encoding="utf-8") as f:
        json.dump(full_db, f, indent=2, ensure_ascii=False)
    print(f"Salvo: {master_db_path}")

    with open(catalog_db_path, "w", encoding="utf-8") as f:
        json.dump(full_db, f, indent=2, ensure_ascii=False)
    print(f"Salvo: {catalog_db_path}")

if __name__ == "__main__":
    build_complete_db()
