# -*- coding: utf-8 -*-
"""
Unificação e Reconstrução do Catálogo Master de todos os 118 Repositórios
Com Auditoria de Segurança Integrada (ScanRepo + Scanner Heurístico Local)
"""

import json
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

from security_scanner import scan_repository_security

def load_master_db():
    try:
        from generate_final_markdown import REPO_DETAILS as orig_details
    except:
        orig_details = {}
        
    with open("data/catalog_db.json", "r", encoding="utf-8") as f:
        new_details = json.load(f)
        
    master = {}
    master.update(orig_details)
    master.update(new_details)
    return master

def generate_master_catalog():
    with open("data/all_starred_github.json", "r", encoding="utf-8") as f:
        all_stars = json.load(f)
        
    master_db = load_master_db()
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
    
    # 2. SUMÁRIO COMPLETO SEMPRE NO TOPO
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
            info = {
                "what": f"Projeto open-source em {lang} voltado para desenvolvimento e engenharia de software.",
                "use_cases": f"Automação e aceleração de desenvolvimento em {lang}; integração em pipelines corporativas.",
                "quickstart": f"```bash\ngit clone https://github.com/{name}.git\ncd {name.split('/')[-1]}\n```",
                "pro_tip": "Consulte os exemplos na pasta do repositório para personalização rápida."
            }
            
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
    
    paths = [
        r"C:\Users\Bktech\CascadeProjects\favorite_repositories\CATALOGO_ESTRELAS.md",
        r"C:\Users\Bktech\.gemini\antigravity\scratch\github-star-automation\CATALOGO_ESTRELAS.md",
        r"C:\Users\Bktech\.gemini\antigravity\scratch\ANALISE_COMPLETA_ESTRELAS_GITHUB.md",
        r"C:\Users\Bktech\OneDrive\Projetos_Trabalho\documentos\4_Documentacoes_Tecnicas_e_Projetos\ANALISE_COMPLETA_ESTRELAS_GITHUB.md",
        r"C:\Users\Bktech\OneDrive\Projetos_Trabalho\favorite_repositories\CATALOGO_ESTRELAS.md",
        r"C:\Users\Bktech\.gemini\antigravity\brain\8dd56937-6945-4170-b062-7eeb40da7a67\analise_github_stars.md"
    ]
    
    for p in paths:
        try:
            os.makedirs(os.path.dirname(p), exist_ok=True)
            with open(p, "w", encoding="utf-8") as f:
                f.write(full_md)
            print(f"Salvo: {p}")
        except Exception as e:
            print(f"Erro ao salvar em {p}: {e}")
            
    with open("data/master_catalog_db.json", "w", encoding="utf-8") as f:
        json.dump(master_db, f, indent=2, ensure_ascii=False)
        
    ids = [r["id"] for r in all_stars if "id" in r]
    state = {
        "processed_ids": ids,
        "total": len(ids)
    }
    with open("data/processed_stars.json", "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)
        
    print(f"Catálogo completo com segurança gerado para todos os {total} repositórios!")

if __name__ == '__main__':
    sys.path.append(r"C:\Users\Bktech\.gemini\antigravity\scratch")
    sys.path.append(r"C:\Users\Bktech\CascadeProjects\favorite_repositories\scripts")
    generate_master_catalog()
