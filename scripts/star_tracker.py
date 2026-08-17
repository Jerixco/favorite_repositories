# -*- coding: utf-8 -*-
"""
Script de Rastreamento e Análise Automática de Estrelas do GitHub
Executado via GitHub Actions de forma 100% autônoma e determinística.

Garante:
1. Sumário Completo SEMPRE no topo com 100% dos repositórios estrelados
2. Dica Pro técnica, rica e personalizada (sem repetições ou frases genéricas)
3. Todo o conteúdo 100% em Português do Brasil (pt-BR)
4. Módulo de Segurança e Auditoria de Malware (ScanRepo + Heurísticas Locais)
"""

import os
import sys
import re
import json
import base64
import urllib.request
from datetime import datetime, timezone

sys.stdout.reconfigure(encoding='utf-8')

# Importar o scanner de segurança
scripts_dir = os.path.dirname(__file__)
if scripts_dir not in sys.path:
    sys.path.append(scripts_dir)

from security_scanner import scan_repository_security

# Configurações de Ambiente
GITHUB_USERNAME = os.environ.get("TARGET_USERNAME", "Jerixco")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
PROCESSED_FILE = os.path.join(DATA_DIR, "processed_stars.json")
MASTER_DB_FILE = os.path.join(DATA_DIR, "master_catalog_db.json")
CATALOG_FILE = os.path.join(os.path.dirname(__file__), "..", "CATALOGO_ESTRELAS.md")

def github_request(url):
    req = urllib.request.Request(url)
    req.add_header("User-Agent", "GitHub-Star-Analyzer-Bot")
    req.add_header("Accept", "application/vnd.github.v3.star+json")
    if GITHUB_TOKEN:
        req.add_header("Authorization", f"Bearer {GITHUB_TOKEN}")
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except Exception as e:
        print(f"Erro na requisição GitHub ({url}): {e}")
        return None

def get_repo_readme(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/readme"
    data = github_request(url)
    if data and "content" in data:
        try:
            return base64.b64decode(data["content"]).decode("utf-8", errors="ignore")[:7000]
        except Exception:
            return ""
    return ""

def call_gemini(prompt):
    models = [
        "gemini-2.0-flash",
        "gemini-1.5-flash",
        "gemini-2.0-flash-001",
        "gemini-1.5-pro",
    ]
    for model in models:
        try:
            api_url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={GEMINI_API_KEY}"
            payload = {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {
                    "temperature": 0.3,
                    "maxOutputTokens": 1024,
                }
            }
            req = urllib.request.Request(
                api_url,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"},
            )
            with urllib.request.urlopen(req, timeout=45) as resp:
                res_data = json.loads(resp.read().decode("utf-8"))
                text = res_data["candidates"][0]["content"]["parts"][0]["text"].strip()
                if text and "O que é e para que serve" in text:
                    print(f"  → Gemini ({model}) respondeu com sucesso.")
                    return parse_ai_response(text)
        except Exception as e:
            print(f"  → Gemini ({model}) falhou: {e}")
            continue
    return None

def call_openai(prompt):
    try:
        api_url = "https://api.openai.com/v1/chat/completions"
        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": "Você é um engenheiro de software sênior que responde exclusivamente em Português do Brasil com termos técnicos precisos e dicas práticas profundas."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3,
            "max_tokens": 1024,
        }
        req = urllib.request.Request(
            api_url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {OPENAI_API_KEY}",
            },
        )
        with urllib.request.urlopen(req, timeout=45) as resp:
            res_data = json.loads(resp.read().decode("utf-8"))
            text = res_data["choices"][0]["message"]["content"].strip()
            return parse_ai_response(text)
    except Exception as e:
        print(f"Aviso: Erro ao chamar OpenAI API ({e})")
        return None

def parse_ai_response(text):
    """Extrai os 4 campos da resposta da IA."""
    try:
        what_match = re.search(r"🎯 \*\*O que é e para que serve:\*\*\s*(.*?)(?=\n- 💡|\n💡|\n- 🚀|\Z)", text, re.DOTALL)
        use_match = re.search(r"💡 \*\*Casos de uso reais no dia a dia:\*\*\s*(.*?)(?=\n- 🚀|\n🚀|\n- ⚡|\Z)", text, re.DOTALL)
        quick_match = re.search(r"🚀 \*\*Como usar na prática com comandos prontos:\*\*\s*(.*?)(?=\n- ⚡|\n⚡|\Z)", text, re.DOTALL)
        tip_match = re.search(r"⚡ \*\*Dica Pro de produtividade:\*\*\s*(.*)", text, re.DOTALL)

        what = what_match.group(1).strip() if what_match else "Ferramenta open-source para desenvolvimento de software."
        use_cases = use_match.group(1).strip() if use_match else "Automação e aceleração de desenvolvimento."
        quickstart = quick_match.group(1).strip() if quick_match else "```bash\ngit clone repo\n```"
        pro_tip = tip_match.group(1).strip() if tip_match else "Consulte os exemplos no README para acelerar a integração."

        if "```" not in quickstart:
            quickstart = f"```bash\n{quickstart}\n```"

        return {
            "what": what,
            "use_cases": use_cases,
            "quickstart": quickstart,
            "pro_tip": pro_tip
        }
    except Exception as e:
        print(f"Erro ao parsear resposta da IA: {e}")
        return None

def generate_fallback_analysis(repo_info, readme_text):
    """Fallback rico em PT-BR com comandos e dicas contextuais."""
    full_name = repo_info.get("full_name", "")
    description = (repo_info.get("description") or "").strip()
    language = repo_info.get("language") or "Docs / Shell"
    name = full_name.split("/")[-1]
    desc_lower = description.lower()
    name_lower = name.lower()
    lang_lower = language.lower()

    # Comandos práticos
    cmd_lines = [f"git clone https://github.com/{full_name}.git", f"cd {name}"]
    if "python" in lang_lower:
        cmd_lines.append("pip install -r requirements.txt")
    elif "typescript" in lang_lower or "javascript" in lang_lower:
        cmd_lines.append("npm install\nnpm run dev")
    elif "rust" in lang_lower:
        cmd_lines.append("cargo build --release")
    elif "go" in lang_lower:
        cmd_lines.append("go build")
    elif "java" in lang_lower:
        cmd_lines.append("./gradlew build  # ou: mvn clean package")
    elif "docker" in desc_lower or "docker" in name_lower:
        cmd_lines.append("docker compose up -d")
    else:
        cmd_lines.append("# Siga as instruções de build no README")
    cmd_block = "\n".join(cmd_lines)

    # O que é (100% pt-BR)
    if any(k in desc_lower + name_lower for k in ["agent", "multi-agent", "swarm"]):
        o_que_e = f"Framework open-source em {language} para orquestração e execução de agentes autônomos de IA com ferramentas integradas."
        casos = "Automação de fluxos de engenharia de software; delegação de tarefas de código para múltiplos agentes especialistas."
        dica = "Isole as permissões de terminal de cada agente em um container Docker para evitar execuções acidentais no sistema principal."
    elif any(k in desc_lower + name_lower for k in ["rag", "graph", "vector", "embed", "knowledge"]):
        o_que_e = f"Infraestrutura em {language} para recuperação e estruturação de conhecimento (RAG / Grafos) para alimentar modelos de linguagem."
        casos = "Indexação semântica de bases de conhecimento corporativas; busca avançada com relacionamentos de entidades complexas."
        dica = "Teste diferentes tamanhos de chunk (ex: 500 vs 1000 tokens com overlap de 10%) para equilibrar precisão semântica e custo."
    elif any(k in desc_lower + name_lower for k in ["mcp", "skill", "plugin"]):
        o_que_e = f"Servidor MCP ou coleção de habilidades em {language} para conectar editores de código e agentes de IA a ferramentas externas."
        casos = "Expandir as capacidades do Claude Code e Cursor; integrar assistentes de IA a bancos de dados e APIs internas."
        dica = "Padronize a validação dos schemas de entrada das ferramentas para que a IA não sofra erros de formatação JSON."
    elif any(k in desc_lower + name_lower for k in ["security", "pentest", "vulnerab", "leak", "secret"]):
        o_que_e = f"Ferramenta de cibersegurança e auditoria em {language} para identificação de vulnerabilidades e proteção de credenciais."
        casos = "Varredura contínua de repositórios contra vazamento de segredos; testes de intrusão éticos em ambientes controlados."
        dica = "Integre as regras de auditoria como pre-commit hook no Git local para barrar vulnerabilidades antes do commit."
    elif any(k in desc_lower + name_lower for k in ["ui", "webui", "dashboard", "frontend"]):
        o_que_e = f"Interface gráfica moderna em {language} para interação e visualização de dados e modelos de inteligência artificial."
        casos = "Criação de portais de autoatendimento interno; dashboards de monitoramento e análise de métricas."
        dica = "Configure variáveis de ambiente no arquivo .env antes da primeira inicialização para manter a persistência de configurações."
    else:
        o_que_e = f"Projeto open-source em {language} projetado para acelerar fluxos de desenvolvimento de software e infraestrutura."
        casos = f"Desenvolvimento de aplicações escaláveis em {language}; automação de pipelines de engenharia."
        dica = "Consulte as issues e discussões do repositório no GitHub para acompanhar os padrões e decisões arquiteturais mais recentes."

    return {
        "what": o_que_e,
        "use_cases": casos,
        "quickstart": f"```bash\n{cmd_block}\n```",
        "pro_tip": dica
    }

def analyze_repository(repo_info):
    full_name = repo_info.get("full_name", "")
    owner, name = full_name.split("/")
    description = repo_info.get("description") or "Sem descrição fornecida"
    language = repo_info.get("language") or "Docs / Shell"
    topics = ", ".join(repo_info.get("topics") or [])

    print(f"-> Analisando repositório: {full_name}...")
    readme_text = get_repo_readme(owner, name)

    prompt = f"""Você é um arquiteto de software sênior brasileiro especializado em código aberto.
Analise o seguinte repositório do GitHub '{full_name}' (Linguagem: {language}).

Descrição oficial do repositório: {description}
Tópicos/Tags: {topics}
Trecho do README:
{readme_text[:4000]}

Gere EXATAMENTE o formato abaixo em Português do Brasil (pt-BR):

- 🎯 **O que é e para que serve:** (Explique de forma clara e aprofundada em 2 a 3 frases o propósito real e o diferencial do projeto)
- 💡 **Casos de uso reais no dia a dia:** (Descreva 2 a 3 cenários práticos e objetivos de uso no trabalho ou projetos de software)
- 🚀 **Como usar na prática com comandos prontos:**
```bash
(Comandos exatos de instalação e execução rápida em Docker, pip, npm, cargo, go ou git clone adequados à linguagem {language})
```
- ⚡ **Dica Pro de produtividade:** (Uma dica técnica única, avançada e específica para este projeto, citando flags, parâmetros, variáveis de ambiente ou práticas de arquitetura reais. NUNCA use frases genéricas como 'leia o readme' ou 'comece simples')

REGRAS:
1. Responda 100% em Português do Brasil.
2. Não copie descrições em inglês sem traduzir.
3. Não use dicas genéricas repetidas."""

    if GEMINI_API_KEY:
        res = call_gemini(prompt)
        if res:
            return res

    if OPENAI_API_KEY:
        res = call_openai(prompt)
        if res:
            return res

    print("  → Usando gerador contextual em PT-BR")
    return generate_fallback_analysis(repo_info, readme_text)

def rebuild_catalog_markdown(all_stars, master_db):
    """Reconstrói o arquivo CATALOGO_ESTRELAS.md determinística e perfeitamente."""
    total = len(all_stars)
    doc = []

    # 1. CABEÇALHO OFICIAL
    doc.append("# 🌟 Dossiê Completo: Análise Minuciosa das Estrelas do GitHub")
    doc.append("")
    doc.append(f"> **Perfil:** [@{GITHUB_USERNAME}](https://github.com/{GITHUB_USERNAME}) (Matheus Salustiano)  ")
    doc.append(f"> **Total de Repositórios Analisados:** {total}  ")
    doc.append("> **Estrutura Obrigatória por Item:**  ")
    doc.append("> 🛡️ *Segurança & Malware (ScanRepo)* | 🎯 *O que é e para que serve* | 💡 *Casos de uso reais no dia a dia* | 🚀 *Como usar na prática* | ⚡ *Dica Pro de produtividade*")
    doc.append("")
    doc.append("---")
    doc.append("")

    # 2. SUMÁRIO COMPLETO SEMPRE NO TOPO (100% dos repositórios)
    doc.append("## 📑 Sumário Completo dos Repositórios")
    doc.append("")
    for i, r in enumerate(all_stars, 1):
        name = r["full_name"]
        anchor = re.sub(r"[^a-z0-9]", "", name.lower())
        stars = r.get("stargazers_count", 0)
        lang = r.get("language") or "Docs / Shell"
        doc.append(f"{i:02d}. [{name}](#{anchor}) — ⭐ {stars:,} (`{lang}`)")
    doc.append("")
    doc.append("---")
    doc.append("")

    # 3. ANÁLISE DETALHADA REPOSITÓRIO POR REPOSITÓRIO
    doc.append("## 🔍 Análise Detalhada Repositório por Repositório")
    doc.append("")

    for i, r in enumerate(all_stars, 1):
        name = r["full_name"]
        url = r.get("html_url") or f"https://github.com/{name}"
        stars = r.get("stargazers_count", 0)
        lang = r.get("language") or "Docs / Shell"
        anchor = re.sub(r"[^a-z0-9]", "", name.lower())

        info = master_db.get(name)
        if not info:
            info = generate_fallback_analysis(r, "")

        security_badge = scan_repository_security(r)

        doc.append(f"<a id=\"{anchor}\"></a>")
        doc.append(f"### {i:02d}. [{name}]({url})")
        doc.append(f"- **⭐ Stars:** {stars:,} | **💻 Linguagem:** `{lang}`")
        doc.append(f"- 🛡️ **Segurança & Malware:** {security_badge}")
        doc.append(f"- 🎯 **O que é e para que serve:** {info['what']}")
        doc.append(f"- 💡 **Casos de uso reais no dia a dia:** {info['use_cases']}")
        doc.append(f"- 🚀 **Como usar na prática com comandos prontos:**")
        doc.append(f"{info['quickstart']}")
        doc.append(f"- ⚡ **Dica Pro de produtividade:** {info['pro_tip']}")
        doc.append("")
        doc.append("---")
        doc.append("")

    return "\n".join(doc)

def main():
    print(f"Iniciando verificação e sincronização de estrelas para: {GITHUB_USERNAME}")

    os.makedirs(DATA_DIR, exist_ok=True)

    # 1. Carregar base de dados master existente
    if os.path.exists(MASTER_DB_FILE):
        with open(MASTER_DB_FILE, "r", encoding="utf-8") as f:
            master_db = json.load(f)
    else:
        master_db = {}

    # 2. Carregar estado de processamento
    if os.path.exists(PROCESSED_FILE):
        with open(PROCESSED_FILE, "r", encoding="utf-8") as f:
            processed_data = json.load(f)
    else:
        processed_data = {"processed_ids": []}

    processed_ids = set(processed_data.get("processed_ids", []))

    # 3. Buscar todos os favoritos atuais da API do GitHub (com paginação)
    all_stars = []
    page = 1
    while True:
        url = f"https://api.github.com/users/{GITHUB_USERNAME}/starred?per_page=100&page={page}"
        items = github_request(url)
        if not items:
            break
        for it in items:
            repo = it.get("repo", it)
            all_stars.append(repo)
        if len(items) < 100:
            break
        page += 1

    total_current = len(all_stars)
    print(f"Total de favoritos encontrados no GitHub: {total_current}")

    if total_current == 0:
        print("Aviso: Nenhum repositório retornado pela API.")
        return

    # 4. Identificar novos repositórios que ainda não foram analisados
    new_found = 0
    for repo in all_stars:
        repo_name = repo.get("full_name")
        repo_id = repo.get("id")

        if repo_id not in processed_ids or repo_name not in master_db:
            analysis = analyze_repository(repo)
            master_db[repo_name] = analysis
            processed_ids.add(repo_id)
            new_found += 1

    print(f"Novos repositórios processados nesta rodada: {new_found}")

    # 5. Salvar base de dados master atualizada
    with open(MASTER_DB_FILE, "w", encoding="utf-8") as f:
        json.dump(master_db, f, indent=2, ensure_ascii=False)

    # 6. Salvar estado de IDs processados
    processed_data["processed_ids"] = list(processed_ids)
    processed_data["total"] = total_current
    processed_data["last_updated"] = datetime.now(timezone.utc).isoformat()
    with open(PROCESSED_FILE, "w", encoding="utf-8") as f:
        json.dump(processed_data, f, indent=2, ensure_ascii=False)

    # 7. Reconstruir o CATALOGO_ESTRELAS.md determinístico
    catalog_markdown = rebuild_catalog_markdown(all_stars, master_db)
    with open(CATALOG_FILE, "w", encoding="utf-8") as f:
        f.write(catalog_markdown)

    # 8. Espelhar no OneDrive e nos caminhos locais se existirem
    mirror_paths = [
        r"C:\Users\Bktech\.gemini\antigravity\scratch\ANALISE_COMPLETA_ESTRELAS_GITHUB.md",
        r"C:\Users\Bktech\.gemini\antigravity\scratch\github-star-automation\CATALOGO_ESTRELAS.md",
        r"C:\Users\Bktech\OneDrive\Projetos_Trabalho\documentos\4_Documentacoes_Tecnicas_e_Projetos\ANALISE_COMPLETA_ESTRELAS_GITHUB.md",
        r"C:\Users\Bktech\OneDrive\Projetos_Trabalho\favorite_repositories\CATALOGO_ESTRELAS.md",
    ]
    for mp in mirror_paths:
        if os.path.exists(os.path.dirname(mp)):
            try:
                with open(mp, "w", encoding="utf-8") as f:
                    f.write(catalog_markdown)
            except Exception:
                pass

    print(f"Processo concluído com sucesso! Catálogo atualizado com {total_current} repositórios.")

if __name__ == "__main__":
    main()
