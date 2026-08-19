# -*- coding: utf-8 -*-
"""
Unificação e Reconstrução do Catálogo Master de todos os Repositórios Estrelados
Com Auditoria de Segurança Integrada (ScanRepo + Scanner Heurístico Local)
"""

import json
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Importar o scanner de segurança
scripts_dir = os.path.dirname(os.path.abspath(__file__))
if scripts_dir not in sys.path:
    sys.path.append(scripts_dir)

from security_scanner import scan_repository_security
from star_tracker import analyze_repository, generate_smart_dynamic_analysis

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
ALL_STARS_FILE = os.path.join(DATA_DIR, "all_starred_github.json")
MASTER_DB_FILE = os.path.join(DATA_DIR, "master_catalog_db.json")
CATALOG_DB_FILE = os.path.join(DATA_DIR, "catalog_db.json")
PROCESSED_FILE = os.path.join(DATA_DIR, "processed_stars.json")
CATALOG_FILE = os.path.join(BASE_DIR, "CATALOGO_ESTRELAS.md")

def generate_master_catalog():
    if not os.path.exists(ALL_STARS_FILE):
        print(f"Erro: Arquivo {ALL_STARS_FILE} não encontrado.")
        return

    with open(ALL_STARS_FILE, "r", encoding="utf-8") as f:
        all_stars = json.load(f)

    if os.path.exists(MASTER_DB_FILE):
        with open(MASTER_DB_FILE, "r", encoding="utf-8") as f:
            master_db = json.load(f)
    else:
        master_db = {}

    total = len(all_stars)
    print(f"Gerando catálogo com módulo de segurança para {total} repositórios...")

    doc = []

    # 1. CABEÇALHO OFICIAL
    doc.append("# 🌟 Dossiê Completo: Análise Minuciosa das Estrelas do GitHub")
    doc.append("")
    doc.append("> **Perfil:** [@Jerixco](https://github.com/Jerixco) (Matheus Salustiano)  ")
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

    # 3. SEÇÃO DETALHADA REPOSITÓRIO POR REPOSITÓRIO
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
            try:
                info = analyze_repository(r)
            except Exception as e:
                print(f"  Aviso: analyze_repository falhou para {name}: {e}. Usando análise dinâmica inteligente.")
                info = generate_smart_dynamic_analysis(r, "")
            master_db[name] = info

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

    full_md = "\n".join(doc)

    # Salvar CATALOGO_ESTRELAS.md principal
    with open(CATALOG_FILE, "w", encoding="utf-8") as f:
        f.write(full_md)
    print(f"Salvo: {CATALOG_FILE}")

    # Salvar espelhos se existirem
    mirror_paths = [
        r"C:\Users\Bktech\.gemini\antigravity\scratch\ANALISE_COMPLETA_ESTRELAS_GITHUB.md",
        r"C:\Users\Bktech\.gemini\antigravity\scratch\github-star-automation\CATALOGO_ESTRELAS.md",
        r"C:\Users\Bktech\OneDrive\Projetos_Trabalho\documentos\4_Documentacoes_Tecnicas_e_Projetos\ANALISE_COMPLETA_ESTRELAS_GITHUB.md",
        r"C:\Users\Bktech\OneDrive\Projetos_Trabalho\favorite_repositories\CATALOGO_ESTRELAS.md",
    ]

    for p in mirror_paths:
        try:
            if os.path.exists(os.path.dirname(p)):
                with open(p, "w", encoding="utf-8") as f:
                    f.write(full_md)
                print(f"Salvo espelho: {p}")
        except Exception as e:
            pass

    # Sincronizar bases JSON
    with open(MASTER_DB_FILE, "w", encoding="utf-8") as f:
        json.dump(master_db, f, indent=2, ensure_ascii=False)

    with open(CATALOG_DB_FILE, "w", encoding="utf-8") as f:
        json.dump(master_db, f, indent=2, ensure_ascii=False)

    ids = [r["id"] for r in all_stars if "id" in r]
    state = {
        "processed_ids": ids,
        "total": len(ids)
    }
    with open(PROCESSED_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)

    print(f"Catálogo completo gerado com sucesso para todos os {total} repositórios!")

if __name__ == '__main__':
    generate_master_catalog()
