# -*- coding: utf-8 -*-
"""
Script de Rastreamento e Análise Automática de Estrelas do GitHub
Executado via GitHub Actions sem nenhuma intervenção manual.

Melhorias:
- Força conteúdo em Português do Brasil (mesmo no fallback)
- Fallback contextual e variado (não mais texto genérico idêntico)
- Chamada Gemini mais robusta (tenta vários modelos)
- Regenera o Sumário Completo a cada atualização
- Trata language=None corretamente
"""

import os
import re
import json
import base64
import urllib.request
from datetime import datetime

# Configurações de Ambiente
GITHUB_USERNAME = os.environ.get("TARGET_USERNAME", "Jerixco")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")

DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "processed_stars.json")
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
            return base64.b64decode(data["content"]).decode("utf-8", errors="ignore")[:8000]
        except Exception:
            return ""
    return ""

def call_gemini(prompt):
    """Tenta vários modelos Gemini em sequência."""
    models = [
        "gemini-2.0-flash",
        "gemini-1.5-flash",
        "gemini-1.5-flash-latest",
        "gemini-2.0-flash-001",
    ]
    for model in models:
        try:
            api_url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={GEMINI_API_KEY}"
            payload = {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {
                    "temperature": 0.4,
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
                    print(f"  → Gemini ({model}) respondeu com sucesso")
                    return text
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
                {"role": "system", "content": "Você responde exclusivamente em Português do Brasil."},
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
            return res_data["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print(f"Aviso: Erro ao chamar OpenAI API ({e})")
        return None

def generate_fallback(repo_info):
    """Gera conteúdo 100% em PT-BR de forma contextual (sem IA)."""
    full_name = repo_info.get("full_name", "")
    description = (repo_info.get("description") or "").strip()
    language = repo_info.get("language") or "Não especificada"
    topics = repo_info.get("topics") or []
    name = full_name.split("/")[-1]

    # Comandos de instalação mais inteligentes
    cmd_lines = [
        f"git clone https://github.com/{full_name}.git",
        f"cd {name}",
    ]
    lang_lower = language.lower() if language else ""
    if "python" in lang_lower:
        cmd_lines.append("pip install -r requirements.txt  # ou: pip install -e .")
    elif lang_lower in ("javascript", "typescript") or "js" in lang_lower:
        cmd_lines.append("npm install")
        cmd_lines.append("npm run dev  # ou npm start")
    elif "rust" in lang_lower:
        cmd_lines.append("cargo build --release")
    elif "go" in lang_lower:
        cmd_lines.append("go build -o bin/")
    elif "java" in lang_lower:
        cmd_lines.append("# Maven: mvn clean package  |  Gradle: ./gradlew build")
    elif "c++" in lang_lower or "cpp" in lang_lower:
        cmd_lines.append("# compile conforme o README (geralmente cmake ou make)")
    else:
        cmd_lines.append("# Siga as instruções de instalação no README do repositório")

    cmd_block = "\n".join(cmd_lines)

    # O que é e para que serve (sempre em português + descrição original como referência)
    if description:
        o_que_e = (
            f"Projeto open-source em **{language}**. "
            f"Descrição oficial: {description}"
        )
    else:
        o_que_e = f"Repositório open-source escrito principalmente em {language}, voltado para desenvolvimento e automação."

    # Casos de uso (variam conforme a linguagem / tópicos)
    casos = []
    if any(t in ["ai", "llm", "agent", "gpt", "ml", "machine-learning"] for t in topics) or "ai" in name.lower() or "llm" in name.lower():
        casos.append("Integração de agentes e modelos de linguagem em produtos reais")
        casos.append("Prototipagem rápida de aplicações com IA generativa")
    elif any(t in ["security", "pentest", "hacking", "vulnerability"] for t in topics):
        casos.append("Testes de segurança e análise de vulnerabilidades em ambientes controlados")
        casos.append("Aprendizado prático de técnicas ofensivas e defensivas")
    elif "python" in lang_lower:
        casos.append("Automação de scripts e pipelines de dados")
        casos.append("Desenvolvimento de APIs, CLIs e ferramentas internas")
    elif lang_lower in ("javascript", "typescript"):
        casos.append("Construção de interfaces web modernas e dashboards")
        casos.append("Backend Node.js e integrações front-end")
    elif "rust" in lang_lower or "go" in lang_lower:
        casos.append("Ferramentas de alta performance e CLIs de sistema")
        casos.append("Serviços backend com baixo consumo de recursos")
    else:
        casos.append("Aprendizado e experimentação da stack do projeto")
        casos.append("Reutilização de padrões e arquiteturas em projetos pessoais ou de equipe")

    casos_texto = "; ".join(casos[:2]) + "."

    # Dica Pro (também contextual)
    if "python" in lang_lower:
        dica = "Crie um ambiente virtual (venv ou poetry) antes de instalar as dependências para evitar conflitos."
    elif lang_lower in ("javascript", "typescript"):
        dica = "Prefira `npm ci` em CI/CD e use o arquivo de lock para builds reproduzíveis."
    elif "docker" in description.lower() or "docker" in " ".join(topics).lower():
        dica = "Rode com Docker Compose quando disponível — facilita o ambiente isolado e a reprodução."
    else:
        dica = "Leia a seção de exemplos e o arquivo CONTRIBUTING.md (quando existir) para acelerar a curva de aprendizado."

    return f"""- 🎯 **O que é e para que serve:** {o_que_e}
- 💡 **Casos de uso reais no dia a dia:** {casos_texto}
- 🚀 **Como usar na prática com comandos prontos:**
```bash
{cmd_block}
```
- ⚡ **Dica Pro de produtividade:** {dica}"""

def generate_ai_analysis(repo_info, readme_text):
    full_name = repo_info.get("full_name", "")
    description = repo_info.get("description") or "Sem descrição"
    language = repo_info.get("language") or "Não especificada"
    topics = ", ".join(repo_info.get("topics") or [])

    prompt = f"""Você é um especialista em engenharia de software brasileiro.
Analise o repositório GitHub '{full_name}' (linguagem principal: {language}).

Descrição oficial: {description}
Tópicos: {topics}
Trecho do README:
{readme_text[:3500]}

Responda EXCLUSIVAMENTE em Português do Brasil (pt-BR).
Gere EXATAMENTE neste formato Markdown (sem nenhuma introdução ou conclusão):

- 🎯 **O que é e para que serve:** (2 a 3 frases claras sobre o propósito e o diferencial do projeto)
- 💡 **Casos de uso reais no dia a dia:** (2 a 3 cenários práticos de uso no trabalho ou projetos pessoais)
- 🚀 **Como usar na prática com comandos prontos:**
```bash
(comandos reais de instalação e execução rápida – Docker, pip, npm, cargo, go, etc.)
```
- ⚡ **Dica Pro de produtividade:** (uma dica técnica avançada e útil)

Regras obrigatórias:
- Todo o texto deve estar em português do Brasil.
- Não copie a descrição em inglês literalmente; traduza e contextualize.
- Seja específico ao projeto (não use frases genéricas).
- Responda somente os 4 tópicos acima."""

    # 1. Tenta Gemini
    if GEMINI_API_KEY:
        result = call_gemini(prompt)
        if result:
            return result

    # 2. Tenta OpenAI
    if OPENAI_API_KEY:
        result = call_openai(prompt)
        if result:
            return result

    # 3. Fallback 100% PT-BR e contextual
    print("  → Usando fallback heurístico em PT-BR")
    return generate_fallback(repo_info)

def extract_entries_for_sumario(content):
    """Extrai todas as entradas detalhadas para montar o sumário."""
    # Procura blocos ### 📦 [owner/repo](url)
    pattern = r"### 📦 \[([^\]]+)\]\(([^)]+)\)\s*\n- \*\*⭐ Stars:\*\* ([\d,]+) \| \*\*💻 Linguagem:\*\* `([^`]+)`"
    matches = re.findall(pattern, content)
    entries = []
    for full_name, url, stars, language in matches:
        # Gera um id de âncora simples
        anchor = re.sub(r"[^a-z0-9]", "", full_name.lower())
        entries.append({
            "full_name": full_name,
            "url": url,
            "stars": stars,
            "language": language,
            "anchor": anchor,
        })
    return entries

def rebuild_sumario(entries):
    if not entries:
        return ""
    lines = ["## 📑 Sumário Completo dos Repositórios", ""]
    for i, e in enumerate(entries, 1):
        lines.append(
            f"{i:02d}. [{e['full_name']}](#{e['anchor']}) — ⭐ {e['stars']} (`{e['language']})"
        )
    lines.append("")
    return "\n".join(lines)

def update_header_total(content, total):
    """Atualiza o contador no cabeçalho."""
    content = re.sub(
        r"(\*\*Total de Repositórios Analisados:\*\* )\d+",
        rf"\g<1>{total}",
        content,
    )
    return content

def main():
    print(f"Iniciando verificação de estrelas para o usuário: {GITHUB_USERNAME}")

    # 1. Carregar histórico
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            processed_data = json.load(f)
    else:
        processed_data = {"processed_ids": []}

    processed_ids = set(processed_data.get("processed_ids", []))

    # 2. Buscar estrelas (até 100 mais recentes – suficiente para detectar novos)
    stars_url = f"https://api.github.com/users/{GITHUB_USERNAME}/starred?per_page=100&sort=created"
    starred_items = github_request(stars_url)

    if not starred_items:
        print("Nenhum repositório retornado ou erro na API.")
        return

    new_stars = []
    for item in starred_items:
        repo = item.get("repo", item)
        repo_id = repo.get("id")
        if repo_id and repo_id not in processed_ids:
            new_stars.append(repo)

    print(f"Total de novos repositórios estrelados encontrados: {len(new_stars)}")

    if not new_stars:
        print("Nenhum novo favorito encontrado. Finalizando.")
        return

    # 3. Processar novos
    new_entries = []
    for repo in new_stars:
        full_name = repo.get("full_name")
        owner, name = full_name.split("/")
        html_url = repo.get("html_url")
        stars_count = repo.get("stargazers_count", 0)
        language = repo.get("language") or "Não especificada"

        print(f"-> Analisando novo repositório: {full_name}")
        readme_text = get_repo_readme(owner, name)
        analysis_markdown = generate_ai_analysis(repo, readme_text)

        # Âncora para o sumário
        anchor = re.sub(r"[^a-z0-9]", "", full_name.lower())

        entry = f"""<a id=\"{anchor}\"></a>
### 📦 [{full_name}]({html_url})
- **⭐ Stars:** {stars_count:,} | **💻 Linguagem:** `{language}`
{analysis_markdown}

---
"""
        new_entries.append(entry)
        processed_ids.add(repo.get("id"))

    # 4. Atualizar CATALOGO_ESTRELAS.md
    if os.path.exists(CATALOG_FILE):
        with open(CATALOG_FILE, "r", encoding="utf-8") as f:
            existing_content = f.read()
    else:
        existing_content = """# 🌟 Dossiê Completo: Análise Minuciosa das Estrelas do GitHub

> **Perfil:** [@Jerixco](https://github.com/Jerixco) (Matheus Salustiano)  
> **Total de Repositórios Analisados:** 0  
> **Estrutura Obrigatória por Item:**  
> 🎯 *O que é e para que serve* | 💡 *Casos de uso reais no dia a dia* | 🚀 *Como usar na prática (Docker, pip, npm, CLI)* | ⚡ *Dica Pro de produtividade*

---

"""

    # Inserir novas entradas no topo (depois do primeiro ---
    header_split = existing_content.split("---\n\n", 1)
    if len(header_split) == 2:
        body = header_split[1]
        # Remove sumário antigo se existir (vamos regenerar)
        body = re.sub(
            r"## 📑 Sumário Completo dos Repositórios\n.*?(?=\n---\n|\n### 📦 |\Z)",
            "",
            body,
            flags=re.DOTALL,
        )
        updated_content = header_split[0] + "---\n\n" + "\n".join(new_entries) + "\n" + body
    else:
        updated_content = existing_content + "\n\n" + "\n".join(new_entries)

    # Regenerar sumário a partir de todas as entradas atuais
    all_entries = extract_entries_for_sumario(updated_content)
    sumario_md = rebuild_sumario(all_entries)

    if sumario_md:
        # Insere o sumário logo após o cabeçalho (depois do primeiro ---)
        parts = updated_content.split("---\n\n", 1)
        if len(parts) == 2:
            # Coloca o sumário no final do arquivo (ou logo após o header se preferir)
            # Aqui colocamos no final para não atrapalhar a leitura das análises recentes
            if "## 📑 Sumário Completo dos Repositórios" not in updated_content:
                updated_content = updated_content.rstrip() + "\n\n" + sumario_md
            else:
                # Já limpamos o antigo, então só adiciona
                updated_content = updated_content.rstrip() + "\n\n" + sumario_md

    # Atualiza o total no header
    total = len(all_entries)
    updated_content = update_header_total(updated_content, total)

    with open(CATALOG_FILE, "w", encoding="utf-8") as f:
        f.write(updated_content)

    # 5. Salvar estado
    processed_data["processed_ids"] = list(processed_ids)
    processed_data["last_updated"] = datetime.utcnow().isoformat()
    processed_data["total"] = total
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(processed_data, f, indent=2, ensure_ascii=False)

    print(f"Catálogo atualizado com sucesso! Total de repositórios no sumário: {total}")

if __name__ == "__main__":
    main()
