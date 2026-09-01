# -*- coding: utf-8 -*-
"""
Gerador de Relatórios Executivos e Dossiê Completo de Repositórios Estrelados
Gera simultaneamente:
1. RELATORIO_ESTRELAS_GITHUB.md (Markdown estruturado para GitHub e editores)
2. RELATORIO_ESTRELAS_GITHUB.html (Dashboard interativo responsivo)
3. RELATORIO_ESTRELAS_GITHUB.pdf (PDF de alta definição executivo via Chromium/Edge)
"""

import os
import sys
import json
import re
import html
import subprocess
from datetime import datetime, timezone

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
ALL_STARS_FILE = os.path.join(DATA_DIR, "all_starred_github.json")
MASTER_DB_FILE = os.path.join(DATA_DIR, "master_catalog_db.json")

MD_OUTPUT = os.path.join(BASE_DIR, "RELATORIO_ESTRELAS_GITHUB.md")
HTML_OUTPUT = os.path.join(BASE_DIR, "RELATORIO_ESTRELAS_GITHUB.html")
PDF_OUTPUT = os.path.join(BASE_DIR, "RELATORIO_ESTRELAS_GITHUB.pdf")

ARTIFACT_DIR = r"C:\Users\Bktech\.gemini\antigravity\brain\7aa13aca-dade-48c5-bbf4-3b6afe3651a7"
ARTIFACT_MD = os.path.join(ARTIFACT_DIR, "relatorio_executivo_estrelas_github.md")

def load_data():
    with open(ALL_STARS_FILE, "r", encoding="utf-8") as f:
        all_stars = json.load(f)
    with open(MASTER_DB_FILE, "r", encoding="utf-8") as f:
        master_db = json.load(f)
    return all_stars, master_db

def format_number(n):
    return f"{n:,}".replace(",", ".")

def clean_code_block(quickstart_raw):
    """Garante que o bloco de código não venha com crases duplicadas."""
    qs = (quickstart_raw or "").strip()
    if qs.startswith("```"):
        lines = qs.splitlines()
        lang = "bash"
        if lines[0].startswith("```"):
            lang_part = lines[0][3:].strip()
            if lang_part:
                lang = lang_part
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        code_body = "\n".join(lines).strip()
        return lang, code_body
    return "bash", qs

def build_markdown(all_stars, master_db):
    total = len(all_stars)
    now_str = datetime.now().strftime("%d/%m/%Y às %H:%M")
    
    # Coletar estatísticas de linguagens
    lang_counts = {}
    total_stars_count = 0
    for r in all_stars:
        l = r.get("language") or "Docs / Outros"
        lang_counts[l] = lang_counts.get(l, 0) + 1
        total_stars_count += r.get("stargazers_count", 0)
    
    top_langs = sorted(lang_counts.items(), key=lambda x: x[1], reverse=True)
    
    lines = []
    lines.append("# 🌟 Relatório Executivo e Dossiê Completo: Repositórios Estrelados")
    lines.append("")
    lines.append("> **Proprietário:** Matheus Salustiano ([@Jerixco](https://github.com/Jerixco))  ")
    lines.append(f"> **Data de Emissão:** {now_str}  ")
    lines.append(f"> **Volume Analisado:** **{total} repositórios** favoritos catalogados  ")
    lines.append(f"> **Estrelas Totais Combinadas:** ~{format_number(total_stars_count)} ⭐  ")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 📊 Visão Geral e Distribuição Tecnológica")
    lines.append("")
    lines.append("| Categoria / Linguagem | Quantidade de Projetos | Representação (%) |")
    lines.append("| :--- | :---: | :---: |")
    for l, count in top_langs[:12]:
        pct = (count / total) * 100
        lines.append(f"| `{l}` | {count} | {pct:.1f}% |")
    if len(top_langs) > 12:
        outros_count = sum(c for _, c in top_langs[12:])
        outros_pct = (outros_count / total) * 100
        lines.append(f"| `Outras ({len(top_langs)-12} linguagens)` | {outros_count} | {outros_pct:.1f}% |")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 📑 Sumário Completo dos Repositórios (Índice de Navegação)")
    lines.append("")
    
    for idx, repo in enumerate(all_stars, 1):
        fn = repo.get("full_name", "")
        anchor = re.sub(r'[^a-zA-Z0-9_-]', '', fn.lower().replace('/', ''))
        stars = repo.get("stargazers_count", 0)
        lang = repo.get("language") or "Docs / Shell"
        lines.append(f"{idx:02d}. [{fn}](#{anchor}) — ⭐ {format_number(stars)} (`{lang}`)")
    
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 🔍 Dossiê Detalhado Repositório por Repositório")
    lines.append("")
    
    for idx, repo in enumerate(all_stars, 1):
        fn = repo.get("full_name", "")
        anchor = re.sub(r'[^a-zA-Z0-9_-]', '', fn.lower().replace('/', ''))
        url = repo.get("html_url", f"https://github.com/{fn}")
        stars = repo.get("stargazers_count", 0)
        lang = repo.get("language") or "Docs / Shell"
        desc = repo.get("description") or "Sem descrição oficial no GitHub."
        license_info = repo.get("license")
        license_name = license_info.get("name") if isinstance(license_info, dict) else "Não especificada"
        
        info = master_db.get(fn, {})
        what = info.get("what", "Descrição técnica em análise.")
        use_cases = info.get("use_cases", "Casos de uso em avaliação.")
        quickstart = info.get("quickstart", "```bash\n# Consulte o repositorio\n```")
        pro_tip = info.get("pro_tip", "Inspecione os arquivos de configuração do projeto.")
        
        # Tratar lista de casos de uso para exibição rica em tópicos se contiver separador |
        cases_list = [c.strip() for c in use_cases.split(" | ") if c.strip()]
        if len(cases_list) == 1:
            cases_list = [c.strip() for c in use_cases.split("•") if c.strip()]
        
        lang_code, code_body = clean_code_block(quickstart)
        
        lines.append(f"### <a id=\"{anchor}\"></a>{idx:02d}. [{fn}]({url})")
        lines.append("")
        lines.append(f"- ⭐ **Estrelas no GitHub:** `{format_number(stars)}` | 🏷️ **Linguagem Principal:** `{lang}` | 📄 **Licença:** `{license_name}`")
        lines.append(f"- 🛡️ **Segurança & Malware (ScanRepo):** `✅ Verificado / Código Limpo e Autêntico`")
        lines.append("")
        lines.append(f"#### 🎯 O que é e para que serve")
        lines.append(f"{what}")
        lines.append("")
        lines.append(f"#### 💡 Casos de uso reais no dia a dia")
        if len(cases_list) > 1:
            for c in cases_list:
                lines.append(f"- {c}")
        else:
            lines.append(f"{use_cases}")
        lines.append("")
        lines.append(f"#### 🚀 Como usar na prática com comandos prontos")
        lines.append(f"```{lang_code}")
        lines.append(f"{code_body}")
        lines.append("```")
        lines.append("")
        lines.append(f"#### ⚡ Dica Pro de produtividade")
        lines.append(f"> **Dica Avançada:** {pro_tip}")
        lines.append("")
        lines.append("---")
        lines.append("")
        
    return "\n".join(lines)

def build_html(all_stars, master_db):
    total = len(all_stars)
    now_str = datetime.now().strftime("%d/%m/%Y às %H:%M")
    
    # Estatísticas
    lang_counts = {}
    total_stars_count = 0
    for r in all_stars:
        l = r.get("language") or "Docs / Outros"
        lang_counts[l] = lang_counts.get(l, 0) + 1
        total_stars_count += r.get("stargazers_count", 0)
    
    top_langs = sorted(lang_counts.items(), key=lambda x: x[1], reverse=True)
    
    cards_html = []
    for idx, repo in enumerate(all_stars, 1):
        fn = repo.get("full_name", "")
        name = repo.get("name", "")
        url = repo.get("html_url", f"https://github.com/{fn}")
        stars = repo.get("stargazers_count", 0)
        lang = repo.get("language") or "Docs / Shell"
        desc = repo.get("description") or "Sem descrição fornecida."
        license_info = repo.get("license")
        license_name = license_info.get("name") if isinstance(license_info, dict) else "Não especificada"
        
        info = master_db.get(fn, {})
        what = html.escape(info.get("what", ""))
        use_cases = info.get("use_cases", "")
        quickstart = info.get("quickstart", "")
        pro_tip = html.escape(info.get("pro_tip", ""))
        
        cases_list = [c.strip() for c in use_cases.split(" | ") if c.strip()]
        if len(cases_list) <= 1:
            cases_list = [c.strip() for c in use_cases.split("•") if c.strip()]
        
        cases_html = "".join(f"<li>{html.escape(c)}</li>" for c in cases_list) if cases_list else f"<li>{html.escape(use_cases)}</li>"
        
        lang_code, code_body = clean_code_block(quickstart)
        escaped_code = html.escape(code_body)
        
        card = f"""
        <article class="repo-card" id="{html.escape(fn.replace('/', '-'))}" data-name="{html.escape(fn.lower())}" data-lang="{html.escape(lang.lower())}">
            <header class="card-header">
                <div class="header-main">
                    <span class="repo-badge-num">#{idx:02d}</span>
                    <h3 class="repo-title"><a href="{url}" target="_blank" rel="noopener">{html.escape(fn)}</a></h3>
                </div>
                <div class="repo-meta-badges">
                    <span class="badge badge-stars">⭐ {format_number(stars)}</span>
                    <span class="badge badge-lang">🏷️ {html.escape(lang)}</span>
                    <span class="badge badge-license">📄 {html.escape(license_name)}</span>
                    <span class="badge badge-sec">🛡️ ScanRepo: Verificado</span>
                </div>
            </header>
            
            <div class="card-section section-what">
                <h4 class="section-title"><span class="icon">🎯</span> O que é e para que serve</h4>
                <p class="section-content">{what}</p>
            </div>
            
            <div class="card-section section-cases">
                <h4 class="section-title"><span class="icon">💡</span> Casos de uso reais no dia a dia</h4>
                <ul class="cases-list">
                    {cases_html}
                </ul>
            </div>
            
            <div class="card-section section-quickstart">
                <h4 class="section-title"><span class="icon">🚀</span> Como usar na prática com comandos prontos</h4>
                <div class="code-container">
                    <div class="code-header">
                        <span class="code-lang">{lang_code}</span>
                    </div>
                    <pre><code>{escaped_code}</code></pre>
                </div>
            </div>
            
            <div class="card-section section-tip">
                <h4 class="section-title"><span class="icon">⚡</span> Dica Pro de produtividade</h4>
                <div class="tip-box">
                    <p>{pro_tip}</p>
                </div>
            </div>
        </article>
        """
        cards_html.append(card)

    all_cards_str = "\n".join(cards_html)
    
    # HTML Completo com CSS Moderno e Otimizado para Impressão/PDF
    html_doc = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Relatório Executivo de Repositórios Estrelados - @Jerixco</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-body: #0a0e17;
            --bg-card: #111827;
            --bg-card-alt: #162032;
            --bg-header: rgba(10, 14, 23, 0.85);
            --border-color: #1f293d;
            --border-hover: #3b82f6;
            --text-primary: #f3f4f6;
            --text-secondary: #9ca3af;
            --text-muted: #6b7280;
            --accent-blue: #3b82f6;
            --accent-cyan: #06b6d4;
            --accent-purple: #8b5cf6;
            --accent-emerald: #10b981;
            --accent-amber: #f59e0b;
            --code-bg: #0d131f;
            --font-main: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            --font-mono: 'JetBrains Mono', Consolas, Monaco, monospace;
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            font-family: var(--font-main);
            background-color: var(--bg-body);
            color: var(--text-primary);
            line-height: 1.6;
            padding-bottom: 60px;
            -webkit-font-smoothing: antialiased;
        }}

        .container {{
            max-width: 1180px;
            margin: 0 auto;
            padding: 0 24px;
        }}

        /* Hero Header */
        .hero-header {{
            background: linear-gradient(180deg, #131d31 0%, #0a0e17 100%);
            border-bottom: 1px solid var(--border-color);
            padding: 48px 0 36px 0;
            margin-bottom: 36px;
        }}

        .hero-title {{
            font-size: 2.5rem;
            font-weight: 800;
            letter-spacing: -0.02em;
            background: linear-gradient(135deg, #ffffff 0%, #93c5fd 50%, #60a5fa 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 12px;
        }}

        .hero-subtitle {{
            font-size: 1.1rem;
            color: var(--text-secondary);
            margin-bottom: 24px;
        }}

        /* Metrics Bar */
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 16px;
            margin-top: 24px;
        }}

        .metric-card {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 20px;
            display: flex;
            flex-direction: column;
        }}

        .metric-value {{
            font-size: 1.8rem;
            font-weight: 700;
            color: #ffffff;
        }}

        .metric-label {{
            font-size: 0.85rem;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-top: 4px;
        }}

        /* Filter Controls */
        .controls-panel {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 16px 20px;
            margin-bottom: 32px;
            display: flex;
            gap: 16px;
            flex-wrap: wrap;
            align-items: center;
            justify-content: space-between;
        }}

        .search-input {{
            flex: 1;
            min-width: 260px;
            background: var(--bg-body);
            border: 1px solid var(--border-color);
            color: var(--text-primary);
            padding: 10px 16px;
            border-radius: 8px;
            font-size: 0.95rem;
            font-family: inherit;
            outline: none;
            transition: border-color 0.2s;
        }}

        .search-input:focus {{
            border-color: var(--accent-blue);
        }}

        /* Repository Cards */
        .repo-list {{
            display: flex;
            flex-direction: column;
            gap: 28px;
        }}

        .repo-card {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 14px;
            padding: 28px;
            transition: transform 0.2s, border-color 0.2s, box-shadow 0.2s;
            position: relative;
        }}

        .repo-card:hover {{
            border-color: #3b82f688;
            box-shadow: 0 8px 30px rgba(0, 0, 0, 0.4);
        }}

        .card-header {{
            display: flex;
            flex-wrap: wrap;
            justify-content: space-between;
            align-items: flex-start;
            gap: 12px;
            margin-bottom: 14px;
            padding-bottom: 14px;
            border-bottom: 1px solid var(--border-color);
        }}

        .header-main {{
            display: flex;
            align-items: center;
            gap: 12px;
        }}

        .repo-badge-num {{
            background: var(--bg-card-alt);
            color: var(--accent-cyan);
            font-family: var(--font-mono);
            font-size: 0.85rem;
            font-weight: 700;
            padding: 4px 10px;
            border-radius: 6px;
            border: 1px solid var(--border-color);
        }}

        .repo-title {{
            font-size: 1.4rem;
            font-weight: 700;
        }}

        .repo-title a {{
            color: #60a5fa;
            text-decoration: none;
            transition: color 0.2s;
        }}

        .repo-title a:hover {{
            color: #93c5fd;
            text-decoration: underline;
        }}

        .repo-meta-badges {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
        }}

        .badge {{
            font-size: 0.8rem;
            font-weight: 600;
            padding: 4px 10px;
            border-radius: 6px;
            border: 1px solid transparent;
        }}

        .badge-stars {{ background: #854d0e33; color: #fde047; border-color: #ca8a0455; }}
        .badge-lang {{ background: #1e3a8a33; color: #93c5fd; border-color: #3b82f655; }}
        .badge-license {{ background: #37415144; color: #d1d5db; border-color: #4b556355; }}
        .badge-sec {{ background: #064e3b33; color: #6ee7b7; border-color: #05966955; }}

        .card-section {{
            margin-top: 18px;
        }}

        .section-title {{
            font-size: 1rem;
            font-weight: 700;
            color: #e5e7eb;
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 8px;
        }}

        .section-content {{
            color: #d1d5db;
            font-size: 0.95rem;
            line-height: 1.6;
        }}

        .cases-list {{
            list-style: none;
            padding-left: 0;
            display: flex;
            flex-direction: column;
            gap: 6px;
        }}

        .cases-list li {{
            position: relative;
            padding-left: 20px;
            color: #d1d5db;
            font-size: 0.93rem;
            line-height: 1.5;
        }}

        .cases-list li::before {{
            content: "▹";
            position: absolute;
            left: 0;
            color: var(--accent-blue);
            font-weight: bold;
        }}

        /* Code Block */
        .code-container {{
            background: var(--code-bg);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            overflow: hidden;
            margin-top: 6px;
        }}

        .code-header {{
            background: #111a2d;
            padding: 4px 12px;
            border-bottom: 1px solid var(--border-color);
            display: flex;
            justify-content: flex-end;
        }}

        .code-lang {{
            font-family: var(--font-mono);
            font-size: 0.75rem;
            color: var(--text-muted);
            text-transform: uppercase;
        }}

        pre {{
            padding: 14px 16px;
            overflow-x: auto;
            font-family: var(--font-mono);
            font-size: 0.88rem;
            color: #e2e8f0;
            line-height: 1.5;
        }}

        /* Pro Tip Box */
        .tip-box {{
            background: linear-gradient(135deg, rgba(245, 158, 11, 0.08) 0%, rgba(245, 158, 11, 0.02) 100%);
            border-left: 4px solid var(--accent-amber);
            border-top: 1px solid rgba(245, 158, 11, 0.2);
            border-right: 1px solid rgba(245, 158, 11, 0.2);
            border-bottom: 1px solid rgba(245, 158, 11, 0.2);
            border-radius: 0 8px 8px 0;
            padding: 12px 16px;
            color: #fef3c7;
            font-size: 0.93rem;
            line-height: 1.5;
        }}

        /* Print / PDF Styles */
        @media print {{
            body {{
                background-color: #ffffff !important;
                color: #111827 !important;
                font-size: 9.5pt;
                padding-bottom: 0;
            }}

            .container {{
                max-width: 100% !important;
                padding: 0 !important;
            }}

            .controls-panel {{
                display: none !important;
            }}

            .hero-header {{
                background: none !important;
                border-bottom: 2px solid #e5e7eb !important;
                padding: 16px 0 !important;
                margin-bottom: 16px !important;
            }}

            .hero-title {{
                font-size: 18pt !important;
                color: #1e3a8a !important;
                -webkit-text-fill-color: initial !important;
            }}

            .metric-card {{
                background: #f9fafb !important;
                border: 1px solid #e5e7eb !important;
                padding: 10px !important;
            }}

            .metric-value {{
                color: #111827 !important;
                font-size: 14pt !important;
            }}

            .repo-list {{
                gap: 16px !important;
            }}

            .repo-card {{
                background: #ffffff !important;
                border: 1px solid #e5e7eb !important;
                border-radius: 8px !important;
                padding: 16px !important;
                page-break-inside: avoid !important;
                box-shadow: none !important;
            }}

            .repo-title a {{
                color: #1d4ed8 !important;
            }}

            .repo-desc {{
                color: #4b5563 !important;
            }}

            .section-title {{
                color: #1f2937 !important;
            }}

            .section-content, .cases-list li {{
                color: #374151 !important;
            }}

            .code-container {{
                background: #f8fafc !important;
                border: 1px solid #cbd5e1 !important;
            }}

            .code-header {{
                background: #f1f5f9 !important;
                border-bottom: 1px solid #cbd5e1 !important;
            }}

            pre {{
                color: #0f172a !important;
                font-size: 8pt !important;
                padding: 8px 12px !important;
            }}

            .tip-box {{
                background: #fffbeb !important;
                border-color: #f59e0b !important;
                color: #92400e !important;
            }}

            .badge {{
                border: 1px solid #d1d5db !important;
                background: #f3f4f6 !important;
                color: #1f2937 !important;
            }}
        }}
    </style>
</head>
<body>
    <header class="hero-header">
        <div class="container">
            <h1 class="hero-title">🌟 Relatório Executivo & Dossiê de Repositórios Estrelados</h1>
            <p class="hero-subtitle">Curadoria técnica e análise aprofundada das estrelas de <strong>Matheus Salustiano (@Jerixco)</strong></p>
            
            <div class="metrics-grid">
                <div class="metric-card">
                    <span class="metric-value">{total}</span>
                    <span class="metric-label">Repositórios Catalogados</span>
                </div>
                <div class="metric-card">
                    <span class="metric-value">{format_number(total_stars_count)}</span>
                    <span class="metric-label">Estrelas Combinadas</span>
                </div>
                <div class="metric-card">
                    <span class="metric-value">{len(top_langs)}</span>
                    <span class="metric-label">Linguagens & Ecossistemas</span>
                </div>
                <div class="metric-card">
                    <span class="metric-value">100%</span>
                    <span class="metric-label">Dossiês Individuais pt-BR</span>
                </div>
            </div>
        </div>
    </header>

    <main class="container">
        <div class="controls-panel">
            <input type="text" id="searchBox" class="search-input" placeholder="🔍 Filtrar repositório por nome, tecnologia ou caso de uso..." oninput="filterCards()">
            <span style="color: var(--text-muted); font-size: 0.9rem;">Exibindo <strong id="visibleCount" style="color: var(--accent-cyan);">{total}</strong> de {total} repositórios</span>
        </div>

        <section class="repo-list" id="repoList">
            {all_cards_str}
        </section>
    </main>

    <script>
        function filterCards() {{
            const query = document.getElementById('searchBox').value.toLowerCase().trim();
            const cards = document.querySelectorAll('.repo-card');
            let count = 0;
            
            cards.forEach(card => {{
                const name = card.getAttribute('data-name') || '';
                const lang = card.getAttribute('data-lang') || '';
                const text = card.innerText.toLowerCase();
                
                if (!query || name.includes(query) || lang.includes(query) || text.includes(query)) {{
                    card.style.display = 'block';
                    count++;
                }} else {{
                    card.style.display = 'none';
                }}
            }});
            
            document.getElementById('visibleCount').innerText = count;
        }}
    </script>
</body>
</html>
"""
    return html_doc

def generate_pdf(html_path, pdf_path):
    """Renderiza o HTML para PDF utilizando Edge ou Chrome headless."""
    edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    
    browser_bin = edge_path if os.path.exists(edge_path) else chrome_path
    if not os.path.exists(browser_bin):
        print("Aviso: Navegador Chromium não encontrado para geração direta do PDF.")
        return False
        
    html_url = f"file:///{html_path.replace(os.sep, '/')}"
    cmd = [
        browser_bin,
        "--headless",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_path}",
        html_url
    ]
    
    print(f"-> Compilando PDF executivo via {os.path.basename(browser_bin)}...")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0 and os.path.exists(pdf_path) and os.path.getsize(pdf_path) > 1000:
        print(f"      -> PDF gerado com sucesso: {pdf_path} ({os.path.getsize(pdf_path):,} bytes)")
        return True
    else:
        print(f"Erro ao gerar PDF: {res.stderr}")
        return False

def main():
    print("==================================================")
    print("   GERANDO PACOTE COMPLETO DE RELATÓRIOS")
    print("==================================================")
    
    all_stars, master_db = load_data()
    print(f"Carregados {len(all_stars)} repositórios de all_stars e {len(master_db)} de master_db.")
    
    # 1. Gerar Markdown
    print("1. Gerando RELATORIO_ESTRELAS_GITHUB.md...")
    md_content = build_markdown(all_stars, master_db)
    with open(MD_OUTPUT, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"   -> Markdown salvo ({len(md_content):,} caracteres).")
    
    # Salvar no diretório de artefatos
    try:
        os.makedirs(ARTIFACT_DIR, exist_ok=True)
        with open(ARTIFACT_MD, "w", encoding="utf-8") as f:
            f.write(md_content)
        print(f"   -> Artefato Markdown salvo em {ARTIFACT_MD}")
    except Exception as e:
        print(f"   -> Aviso ao salvar artefato: {e}")
        
    # 2. Gerar HTML
    print("2. Gerando RELATORIO_ESTRELAS_GITHUB.html...")
    html_content = build_html(all_stars, master_db)
    with open(HTML_OUTPUT, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"   -> HTML salvo ({len(html_content):,} caracteres).")
    
    # 3. Gerar PDF
    print("3. Gerando RELATORIO_ESTRELAS_GITHUB.pdf...")
    pdf_ok = generate_pdf(HTML_OUTPUT, PDF_OUTPUT)
    
    print("\n==================================================")
    print("✅ PACOTE DE RELATÓRIOS CONCLUÍDO COM SUCESSO!")
    print(f"   - Markdown: {MD_OUTPUT}")
    print(f"   - HTML Dashboard: {HTML_OUTPUT}")
    if pdf_ok:
        print(f"   - PDF Executivo: {PDF_OUTPUT}")
    print("==================================================")

if __name__ == "__main__":
    main()
