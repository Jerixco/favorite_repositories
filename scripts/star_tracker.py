# -*- coding: utf-8 -*-
"""
Script de Rastreamento e Análise Automática de Estrelas do GitHub
Executado via GitHub Actions sem nenhuma intervenção manual.
"""

import os
import sys
import json
import base64
import urllib.request
import urllib.parse
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
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode('utf-8'))
    except Exception as e:
        print(f"Erro na requisição GitHub ({url}): {e}")
        return None

def get_repo_readme(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/readme"
    data = github_request(url)
    if data and "content" in data:
        try:
            return base64.b64decode(data["content"]).decode('utf-8', errors='ignore')[:8000]
        except Exception:
            return ""
    return ""

def generate_ai_analysis(repo_info, readme_text):
    full_name = repo_info.get("full_name", "")
    description = repo_info.get("description", "Sem descrição")
    language = repo_info.get("language", "Geral")
    topics = ", ".join(repo_info.get("topics", []))
    
    prompt = f"""Você é um especialista em engenharia de software e análise de código aberto.
Analise o repositório '{full_name}' ({language}) com base na descrição e no README abaixo:

Descrição: {description}
Tópicos: {topics}
Trecho do README:
{readme_text[:4000]}

Gere EXATAMENTE o seguinte formato em Markdown (em Português do Brasil), com riqueza de detalhes práticos:

- 🎯 **O que é e para que serve:** (Explique claramente o propósito central e o diferencial do projeto em 2 a 3 frases)
- 💡 **Casos de uso reais no dia a dia:** (Explique 2 a 3 cenários práticos onde o desenvolvedor usará isso no trabalho ou projetos)
- 🚀 **Como usar na prática com comandos prontos:**
```bash
(Comandos exatos de instalação e execução rápida: Docker, pip, npm, npx, cargo ou git clone conforme a linguagem do projeto)
```
- ⚡ **Dica Pro de produtividade:** (Uma dica técnica avançada para tirar o máximo proveito da ferramenta)

IMPORTANTE: Responda APENAS os 4 tópicos acima, sem introduções ou mensagens de fechamento."""

    # Tenta usar a API do Google Gemini se a chave estiver presente
    if GEMINI_API_KEY:
        try:
            api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
            payload = {
                "contents": [{"parts": [{"text": prompt}]}]
            }
            req = urllib.request.Request(api_url, data=json.dumps(payload).encode('utf-8'), headers={'Content-Type': 'application/json'})
            with urllib.request.urlopen(req) as resp:
                res_data = json.loads(resp.read().decode('utf-8'))
                return res_data['candidates'][0]['content']['parts'][0]['text'].strip()
        except Exception as e:
            print(f"Aviso: Erro ao chamar Gemini API ({e}). Tentando fallback...")

    # Tenta usar OpenAI se configurado
    if OPENAI_API_KEY:
        try:
            api_url = "https://api.openai.com/v1/chat/completions"
            payload = {
                "model": "gpt-4o-mini",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.3
            }
            req = urllib.request.Request(api_url, data=json.dumps(payload).encode('utf-8'), headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {OPENAI_API_KEY}'
            })
            with urllib.request.urlopen(req) as resp:
                res_data = json.loads(resp.read().decode('utf-8'))
                return res_data['choices'][0]['message']['content'].strip()
        except Exception as e:
            print(f"Aviso: Erro ao chamar OpenAI API ({e}). Usando fallback heurístico...")

    # Fallback Heurístico (caso nenhuma chave de API de IA esteja configurada)
    cmd = f"git clone https://github.com/{full_name}.git\ncd {full_name.split('/')[-1]}"
    if language == "Python":
        cmd += "\npip install -r requirements.txt"
    elif language in ["JavaScript", "TypeScript"]:
        cmd += "\nnpm install\nnpm run dev"
    elif language == "Rust":
        cmd += "\ncargo build --release"
    elif language == "Go":
        cmd += "\ngo build"

    return f"""- 🎯 **O que é e para que serve:** {description or 'Projeto de software para automação e desenvolvimento.'}
- 💡 **Casos de uso reais no dia a dia:** Otimização de fluxos de desenvolvimento, integração contínua e arquitetura em {language}.
- 🚀 **Como usar na prática com comandos prontos:**
```bash
{cmd}
```
- ⚡ **Dica Pro de produtividade:** Consulte os exemplos na pasta do repositório para personalização rápida."""

def main():
    print(f"Iniciando verificação de estrelas para o usuário: {GITHUB_USERNAME}")
    
    # 1. Carregar histórico de repositórios já processados
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            processed_data = json.load(f)
    else:
        processed_data = {"processed_ids": []}

    processed_ids = set(processed_data.get("processed_ids", []))

    # 2. Buscar últimos favoritos via GitHub API
    stars_url = f"https://api.github.com/users/{GITHUB_USERNAME}/starred?per_page=100"
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

    # 3. Processar cada novo repositório
    new_entries = []
    for repo in new_stars:
        full_name = repo.get("full_name")
        owner, name = full_name.split("/")
        html_url = repo.get("html_url")
        stars_count = repo.get("stargazers_count", 0)
        language = repo.get("language") or "Geral"
        
        print(f"-> Analisando novo repositório: {full_name}")
        readme_text = get_repo_readme(owner, name)
        analysis_markdown = generate_ai_analysis(repo, readme_text)
        
        entry = f"""### 📦 [{full_name}]({html_url})
- **⭐ Stars:** {stars_count:,} | **💻 Linguagem:** `{language}`
{analysis_markdown}

---
"""
        new_entries.append(entry)
        processed_ids.add(repo.get("id"))

    # 4. Atualizar o arquivo CATALOGO_ESTRELAS.md
    if os.path.exists(CATALOG_FILE):
        with open(CATALOG_FILE, "r", encoding="utf-8") as f:
            existing_content = f.read()
    else:
        existing_content = "# 🌟 Catálogo Automatizado de Repositórios Estrelados\n\nAtualizado automaticamente via GitHub Actions.\n\n---\n\n"

    # Inserir as novas análises no topo da lista
    header_split = existing_content.split("---\n\n", 1)
    if len(header_split) == 2:
        updated_content = header_split[0] + "---\n\n" + "\n".join(new_entries) + "\n" + header_split[1]
    else:
        updated_content = existing_content + "\n\n" + "\n".join(new_entries)

    with open(CATALOG_FILE, "w", encoding="utf-8") as f:
        f.write(updated_content)

    # 5. Salvar estado atualizado
    processed_data["processed_ids"] = list(processed_ids)
    processed_data["last_updated"] = datetime.utcnow().isoformat()
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(processed_data, f, indent=2)

    print("Catálogo de estrelas atualizado com sucesso!")

if __name__ == "__main__":
    main()
