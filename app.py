# -*- coding: utf-8 -*-
"""
🌟 GitHub Starred Hub - Web App
Aplicação web leve, moderna e responsiva para consulta, busca e sincronização
em tempo real dos repositórios favoritos de @Jerixco.

Para rodar:
    python app.py
Acessar:
    http://localhost:8000
"""

import os
import sys
import json
import asyncio
import threading
import subprocess
from datetime import datetime, timezone

sys.stdout.reconfigure(encoding='utf-8')

import uvicorn
from starlette.applications import Starlette
from starlette.responses import JSONResponse, HTMLResponse
from starlette.routing import Route
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
ALL_STARS_FILE = os.path.join(DATA_DIR, "all_starred_github.json")
MASTER_DB_FILE = os.path.join(DATA_DIR, "master_catalog_db.json")
SCRIPTS_DIR = os.path.join(BASE_DIR, "scripts")

# Estado global de sincronização
SYNC_STATE = {
    "is_syncing": False,
    "last_sync_time": None,
    "last_sync_result": None,
    "progress_message": "Pronto",
    "logs": []
}

def load_catalog_data():
    """Carrega all_stars e master_db combinados."""
    all_stars = []
    master_db = {}
    
    if os.path.exists(ALL_STARS_FILE):
        try:
            with open(ALL_STARS_FILE, "r", encoding="utf-8") as f:
                all_stars = json.load(f)
        except Exception as e:
            print(f"Erro ao carregar all_stars: {e}")

    if os.path.exists(MASTER_DB_FILE):
        try:
            with open(MASTER_DB_FILE, "r", encoding="utf-8") as f:
                master_db = json.load(f)
        except Exception as e:
            print(f"Erro ao carregar master_db: {e}")

    # Combinar dados enriquecidos
    combined = []
    for idx, repo in enumerate(all_stars, 1):
        fn = repo.get("full_name", "")
        info = master_db.get(fn, {})
        
        license_info = repo.get("license")
        license_name = license_info.get("name") if isinstance(license_info, dict) else "Não especificada"
        
        combined.append({
            "index": idx,
            "id": repo.get("id"),
            "name": repo.get("name", ""),
            "full_name": fn,
            "html_url": repo.get("html_url", f"https://github.com/{fn}"),
            "description": repo.get("description") or "Sem descrição oficial no GitHub.",
            "stars": repo.get("stargazers_count", 0),
            "language": repo.get("language") or "Docs / Shell",
            "topics": repo.get("topics") or [],
            "license": license_name,
            "created_at": repo.get("created_at"),
            "updated_at": repo.get("updated_at"),
            "what": info.get("what", "Análise contextual em atualização."),
            "use_cases": info.get("use_cases", "Casos de uso personalizados em atualização."),
            "quickstart": info.get("quickstart", "```bash\n# Consulte a documentação específica do projeto\n```"),
            "pro_tip": info.get("pro_tip", "Dica Pro personalizada em atualização.")
        })
        
    return combined

def run_sync_thread():
    """Executa scripts/star_tracker.py em thread separada."""
    global SYNC_STATE
    SYNC_STATE["is_syncing"] = True
    SYNC_STATE["progress_message"] = "Buscando favoritos no GitHub e gerando análises..."
    SYNC_STATE["logs"] = [f"[{datetime.now().strftime('%H:%M:%S')}] Iniciando sincronização com GitHub..."]
    
    tracker_script = os.path.join(SCRIPTS_DIR, "star_tracker.py")
    try:
        cmd = [sys.executable, tracker_script]
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=BASE_DIR
        )
        
        for line in iter(proc.stdout.readline, ''):
            line_str = line.strip()
            if line_str:
                SYNC_STATE["logs"].append(line_str)
                if len(SYNC_STATE["logs"]) > 50:
                    SYNC_STATE["logs"].pop(0)
                if "Analisando repositório:" in line_str:
                    SYNC_STATE["progress_message"] = line_str
                elif "Processo concluído" in line_str:
                    SYNC_STATE["progress_message"] = line_str
                    
        proc.stdout.close()
        proc.wait()
        
        if proc.returncode == 0:
            SYNC_STATE["last_sync_result"] = "Sucesso"
            SYNC_STATE["progress_message"] = "Sincronização concluída com sucesso!"
            SYNC_STATE["last_sync_time"] = datetime.now().strftime("%d/%m/%Y às %H:%M:%S")
            
            # Atualizar pacote de relatórios
            bundle_script = os.path.join(SCRIPTS_DIR, "generate_report_bundle.py")
            if os.path.exists(bundle_script):
                subprocess.run([sys.executable, bundle_script], cwd=BASE_DIR, capture_output=True)
        else:
            SYNC_STATE["last_sync_result"] = f"Erro (código {proc.returncode})"
            SYNC_STATE["progress_message"] = f"Falha na sincronização (código {proc.returncode})"
    except Exception as e:
        SYNC_STATE["last_sync_result"] = f"Erro: {str(e)}"
        SYNC_STATE["progress_message"] = f"Erro de execução: {str(e)}"
        SYNC_STATE["logs"].append(f"Exceção: {str(e)}")
    finally:
        SYNC_STATE["is_syncing"] = False

# ── Endpoints de API ─────────────────────────────────────────────────────────

async def api_stars(request):
    """Retorna lista de repositórios estrelados com filtros opcionais."""
    data = load_catalog_data()
    q = request.query_params.get("q", "").lower().strip()
    lang = request.query_params.get("lang", "").lower().strip()
    
    if q:
        data = [
            r for r in data
            if q in r["full_name"].lower()
            or q in r["description"].lower()
            or q in r["what"].lower()
            or q in r["use_cases"].lower()
            or any(q in t.lower() for t in r["topics"])
        ]
        
    if lang and lang != "todos":
        data = [r for r in data if r["language"].lower() == lang]
        
    return JSONResponse(data)

async def api_stats(request):
    """Retorna métricas gerais do catálogo."""
    data = load_catalog_data()
    total = len(data)
    total_stars = sum(r["stars"] for r in data)
    
    lang_counts = {}
    for r in data:
        l = r["language"]
        lang_counts[l] = lang_counts.get(l, 0) + 1
        
    top_langs = sorted(
        [{"name": k, "count": v, "pct": round((v/total)*100, 1)} for k, v in lang_counts.items()],
        key=lambda x: x["count"],
        reverse=True
    )
    
    return JSONResponse({
        "total_repositories": total,
        "total_stars": total_stars,
        "languages_count": len(lang_counts),
        "languages": top_langs,
        "last_sync_time": SYNC_STATE["last_sync_time"],
        "is_syncing": SYNC_STATE["is_syncing"]
    })

async def api_sync_start(request):
    """Dispara a sincronização em segundo plano."""
    global SYNC_STATE
    if SYNC_STATE["is_syncing"]:
        return JSONResponse({"status": "already_running", "message": "Sincronização já está em andamento."})
        
    t = threading.Thread(target=run_sync_thread, daemon=True)
    t.start()
    return JSONResponse({"status": "started", "message": "Sincronização iniciada com sucesso!"})

async def api_sync_status(request):
    """Retorna o status atual da sincronização."""
    return JSONResponse(SYNC_STATE)

# ── Frontend Web Dashboard ───────────────────────────────────────────────────

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🌟 Starred Repositories Hub - @Jerixco</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-body: #0a0e17;
            --bg-card: #111827;
            --bg-card-alt: #162032;
            --border: #1f293d;
            --border-hover: #3b82f6;
            --text-main: #f3f4f6;
            --text-sub: #9ca3af;
            --text-muted: #6b7280;
            --accent-blue: #3b82f6;
            --accent-cyan: #06b6d4;
            --accent-amber: #f59e0b;
            --accent-emerald: #10b981;
            --font-sans: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
            --font-mono: 'JetBrains Mono', Consolas, monospace;
        }

        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: var(--font-sans);
            background-color: var(--bg-body);
            color: var(--text-main);
            line-height: 1.5;
            padding-bottom: 60px;
            -webkit-font-smoothing: antialiased;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }

        /* Top Navbar */
        .navbar {
            background: rgba(17, 24, 39, 0.85);
            backdrop-filter: blur(12px);
            border-bottom: 1px solid var(--border);
            position: sticky;
            top: 0;
            z-index: 100;
            padding: 14px 0;
        }
        .nav-content {
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 12px;
        }
        .brand {
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .brand-logo {
            font-size: 1.6rem;
        }
        .brand-title {
            font-size: 1.2rem;
            font-weight: 800;
            background: linear-gradient(135deg, #ffffff 0%, #93c5fd 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .btn-sync {
            background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
            color: #ffffff;
            border: 1px solid #3b82f6;
            padding: 8px 18px;
            border-radius: 8px;
            font-weight: 600;
            font-size: 0.9rem;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 8px;
            transition: all 0.2s;
        }
        .btn-sync:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 15px rgba(37, 99, 235, 0.4);
        }
        .btn-sync:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }

        /* Hero Banner & Stats */
        .hero {
            padding: 30px 0 20px 0;
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 14px;
            margin-top: 16px;
        }
        .stat-card {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 16px;
        }
        .stat-val {
            font-size: 1.7rem;
            font-weight: 800;
            color: #ffffff;
        }
        .stat-label {
            font-size: 0.8rem;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-top: 2px;
        }

        /* Controls Panel */
        .controls {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 14px 18px;
            margin: 24px 0;
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
            align-items: center;
            justify-content: space-between;
        }
        .search-box {
            flex: 1;
            min-width: 250px;
            background: var(--bg-body);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 10px 14px;
            color: var(--text-main);
            font-family: inherit;
            font-size: 0.95rem;
            outline: none;
        }
        .search-box:focus {
            border-color: var(--accent-blue);
        }
        .filter-select {
            background: var(--bg-body);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 10px 14px;
            color: var(--text-main);
            font-family: inherit;
            font-size: 0.9rem;
            outline: none;
            cursor: pointer;
        }
        .view-toggles {
            display: flex;
            background: var(--bg-body);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 3px;
        }
        .btn-view {
            background: transparent;
            border: none;
            color: var(--text-sub);
            padding: 6px 12px;
            font-size: 0.85rem;
            font-weight: 600;
            border-radius: 6px;
            cursor: pointer;
            transition: all 0.2s;
        }
        .btn-view.active {
            background: var(--bg-card-alt);
            color: var(--text-main);
            border: 1px solid var(--border);
        }

        /* Repos Grid / List */
        .repo-list {
            display: flex;
            flex-direction: column;
            gap: 20px;
        }
        .repo-card {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 22px;
            transition: border-color 0.2s, box-shadow 0.2s;
        }
        .repo-card:hover {
            border-color: rgba(59, 130, 246, 0.6);
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
        }

        .card-top {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            flex-wrap: wrap;
            gap: 10px;
            margin-bottom: 10px;
        }
        .repo-header-info {
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .repo-num {
            font-family: var(--font-mono);
            font-size: 0.8rem;
            font-weight: 700;
            color: var(--accent-cyan);
            background: var(--bg-card-alt);
            padding: 3px 8px;
            border-radius: 6px;
            border: 1px solid var(--border);
        }
        .repo-name {
            font-size: 1.25rem;
            font-weight: 700;
        }
        .repo-name a {
            color: #60a5fa;
            text-decoration: none;
        }
        .repo-name a:hover {
            text-decoration: underline;
        }

        .badges-group {
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
        }
        .badge {
            font-size: 0.75rem;
            font-weight: 600;
            padding: 3px 8px;
            border-radius: 6px;
            border: 1px solid transparent;
        }
        .badge-star { background: rgba(245, 158, 11, 0.15); color: #fde047; border-color: rgba(245, 158, 11, 0.3); }
        .badge-lang { background: rgba(59, 130, 246, 0.15); color: #93c5fd; border-color: rgba(59, 130, 246, 0.3); }
        .badge-sec { background: rgba(16, 185, 129, 0.15); color: #6ee7b7; border-color: rgba(16, 185, 129, 0.3); }

        /* Pillars Content */
        .pillar {
            margin-top: 14px;
        }
        .pillar-title {
            font-size: 0.92rem;
            font-weight: 700;
            color: #e5e7eb;
            display: flex;
            align-items: center;
            gap: 6px;
            margin-bottom: 6px;
        }
        .pillar-text {
            color: #d1d5db;
            font-size: 0.9rem;
            line-height: 1.5;
        }

        .cases-ul {
            list-style: none;
            padding-left: 0;
            display: flex;
            flex-direction: column;
            gap: 4px;
        }
        .cases-ul li {
            position: relative;
            padding-left: 18px;
            color: #d1d5db;
            font-size: 0.88rem;
        }
        .cases-ul li::before {
            content: "▹";
            position: absolute;
            left: 0;
            color: var(--accent-blue);
        }

        /* Code Block with Copy */
        .code-box {
            background: #0d131f;
            border: 1px solid var(--border);
            border-radius: 8px;
            overflow: hidden;
            position: relative;
            margin-top: 6px;
        }
        .code-box pre {
            padding: 12px 14px;
            font-family: var(--font-mono);
            font-size: 0.84rem;
            color: #e2e8f0;
            overflow-x: auto;
        }
        .btn-copy {
            position: absolute;
            top: 6px;
            right: 8px;
            background: var(--bg-card-alt);
            border: 1px solid var(--border);
            color: var(--text-sub);
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.75rem;
            cursor: pointer;
            transition: all 0.2s;
        }
        .btn-copy:hover {
            color: #ffffff;
            border-color: var(--accent-blue);
        }

        /* Pro Tip Box */
        .tip-card {
            background: linear-gradient(135deg, rgba(245, 158, 11, 0.09) 0%, rgba(245, 158, 11, 0.02) 100%);
            border-left: 4px solid var(--accent-amber);
            border-top: 1px solid rgba(245, 158, 11, 0.2);
            border-right: 1px solid rgba(245, 158, 11, 0.2);
            border-bottom: 1px solid rgba(245, 158, 11, 0.2);
            border-radius: 0 8px 8px 0;
            padding: 10px 14px;
            color: #fef3c7;
            font-size: 0.88rem;
            margin-top: 12px;
        }

        /* Toast notifications */
        .toast {
            position: fixed;
            bottom: 24px;
            right: 24px;
            background: #1e293b;
            color: #ffffff;
            border: 1px solid var(--border-hover);
            padding: 12px 20px;
            border-radius: 8px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.5);
            font-size: 0.9rem;
            z-index: 1000;
            display: none;
        }

        /* Compact Mode Tweaks */
        body.mode-compact .full-only {
            display: none !important;
        }
    </style>
</head>
<body class="mode-compact">
    <nav class="navbar">
        <div class="container nav-content">
            <div class="brand">
                <span class="brand-logo">🌟</span>
                <div>
                    <h1 class="brand-title">GitHub Starred Hub</h1>
                    <span style="font-size: 0.75rem; color: var(--text-muted);">Curadoria técnica por @Jerixco</span>
                </div>
            </div>
            
            <div style="display: flex; align-items: center; gap: 12px;">
                <span id="syncStatusBadge" style="font-size: 0.8rem; color: var(--text-sub);">Carregando dados...</span>
                <button id="btnSync" class="btn-sync" onclick="triggerSync()">
                    <span>🔄</span>
                    <span>Sincronizar Agora</span>
                </button>
            </div>
        </div>
    </nav>

    <div class="container hero">
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-val" id="statTotal">--</div>
                <div class="stat-label">Favoritos Catalogados</div>
            </div>
            <div class="stat-card">
                <div class="stat-val" id="statStars">--</div>
                <div class="stat-label">Estrelas Combinadas</div>
            </div>
            <div class="stat-card">
                <div class="stat-val" id="statLangs">--</div>
                <div class="stat-label">Linguagens & Stacks</div>
            </div>
            <div class="stat-card">
                <div class="stat-val" id="statLastSync">--</div>
                <div class="stat-label">Última Sincronização</div>
            </div>
        </div>

        <div class="controls">
            <input type="text" id="searchInput" class="search-box" placeholder="🔍 Buscar por nome, tecnologia, caso de uso ou tags..." oninput="applyFilters()">
            
            <select id="langFilter" class="filter-select" onchange="applyFilters()">
                <option value="todos">🏷️ Todas as Linguagens</option>
            </select>

            <select id="sortSelect" class="filter-select" onchange="applyFilters()">
                <option value="index">🔢 Ordem do Catálogo</option>
                <option value="stars">⭐ Mais Estrelas</option>
                <option value="name">🔤 Alfabética (A-Z)</option>
            </select>

            <div class="view-toggles">
                <button id="btnCompact" class="btn-view active" onclick="setViewMode('compact')">Resumido</button>
                <button id="btnFull" class="btn-view" onclick="setViewMode('full')">Completo</button>
            </div>
        </div>

        <div id="repoList" class="repo-list">
            <!-- Cards carregados via JS -->
        </div>
    </div>

    <div id="toast" class="toast"></div>

    <script>
        let allRepos = [];
        let viewMode = 'compact';

        function showToast(msg) {
            const t = document.getElementById('toast');
            t.innerText = msg;
            t.style.display = 'block';
            setTimeout(() => { t.style.display = 'none'; }, 3000);
        }

        function setViewMode(mode) {
            viewMode = mode;
            document.body.className = mode === 'compact' ? 'mode-compact' : 'mode-full';
            document.getElementById('btnCompact').className = mode === 'compact' ? 'btn-view active' : 'btn-view';
            document.getElementById('btnFull').className = mode === 'full' ? 'btn-view active' : 'btn-view';
        }

        async function fetchStats() {
            try {
                const res = await fetch('/api/stats');
                const data = await res.json();
                document.getElementById('statTotal').innerText = data.total_repositories;
                document.getElementById('statStars').innerText = data.total_stars.toLocaleString('pt-BR') + ' ⭐';
                document.getElementById('statLangs').innerText = data.languages_count;
                document.getElementById('statLastSync').innerText = data.last_sync_time ? data.last_sync_time.split(' às ')[0] : 'Recente';
                
                const langSelect = document.getElementById('langFilter');
                const currentVal = langSelect.value;
                langSelect.innerHTML = '<option value="todos">🏷️ Todas as Linguagens</option>';
                data.languages.forEach(l => {
                    const opt = document.createElement('option');
                    opt.value = l.name.toLowerCase();
                    opt.innerText = `${l.name} (${l.count})`;
                    langSelect.appendChild(opt);
                });
                langSelect.value = currentVal;
            } catch (e) {
                console.error(e);
            }
        }

        async function fetchStars() {
            try {
                const res = await fetch('/api/stars');
                allRepos = await res.json();
                applyFilters();
            } catch (e) {
                console.error(e);
            }
        }

        function cleanCode(quickstart) {
            let s = (quickstart || '').trim();
            if (s.startsWith('```')) {
                const lines = s.split('\\n');
                if (lines[0].startsWith('```')) lines.shift();
                if (lines.length && lines[lines.length - 1].trim() === '```') lines.pop();
                return lines.join('\\n').trim();
            }
            return s;
        }

        function copyCode(id) {
            const el = document.getElementById(id);
            if (el) {
                navigator.clipboard.writeText(el.innerText);
                showToast('Comando copiado para a área de transferência!');
            }
        }

        function renderRepos(list) {
            const container = document.getElementById('repoList');
            if (!list.length) {
                container.innerHTML = '<div style="text-align:center; padding: 40px; color: var(--text-muted);">Nenhum repositório encontrado com os filtros atuais.</div>';
                return;
            }

            container.innerHTML = list.map(r => {
                const codeBody = cleanCode(r.quickstart);
                const codeId = 'code-' + r.id;
                
                // Formatação de casos de uso
                let cases = (r.use_cases || '').split(' | ').filter(x => x.trim());
                if (cases.length <= 1) cases = (r.use_cases || '').split('•').filter(x => x.trim());
                const casesHtml = cases.map(c => `<li>${c}</li>`).join('');

                return `
                <article class="repo-card">
                    <div class="card-top">
                        <div class="repo-header-info">
                            <span class="repo-num">#${String(r.index).padStart(2, '0')}</span>
                            <h2 class="repo-name"><a href="${r.html_url}" target="_blank" rel="noopener">${r.full_name}</a></h2>
                        </div>
                        <div class="badges-group">
                            <span class="badge badge-star">⭐ ${r.stars.toLocaleString('pt-BR')}</span>
                            <span class="badge badge-lang">🏷️ ${r.language}</span>
                            <span class="badge badge-sec">🛡️ Limpo</span>
                        </div>
                    </div>

                    <div class="pillar">
                        <h3 class="pillar-title"><span>🎯</span> O que é e para que serve</h3>
                        <p class="pillar-text">${r.what}</p>
                    </div>

                    <div class="pillar full-only">
                        <h3 class="pillar-title"><span>💡</span> Casos de uso reais no dia a dia</h3>
                        <ul class="cases-ul">${casesHtml}</ul>
                    </div>

                    <div class="pillar full-only">
                        <h3 class="pillar-title"><span>🚀</span> Como usar na prática com comandos prontos</h3>
                        <div class="code-box">
                            <button class="btn-copy" onclick="copyCode('${codeId}')">📋 Copiar</button>
                            <pre><code id="${codeId}">${codeBody}</code></pre>
                        </div>
                    </div>

                    <div class="tip-card">
                        <strong>⚡ Dica Pro:</strong> ${r.pro_tip}
                    </div>
                </article>
                `;
            }).join('');
        }

        function applyFilters() {
            const q = document.getElementById('searchInput').value.toLowerCase().trim();
            const lang = document.getElementById('langFilter').value.toLowerCase().trim();
            const sort = document.getElementById('sortSelect').value;

            let filtered = allRepos.filter(r => {
                const matchQ = !q || (
                    r.full_name.toLowerCase().includes(q) ||
                    r.what.toLowerCase().includes(q) ||
                    r.use_cases.toLowerCase().includes(q) ||
                    (r.pro_tip && r.pro_tip.toLowerCase().includes(q)) ||
                    (r.topics && r.topics.some(t => t.toLowerCase().includes(q)))
                );
                const matchLang = lang === 'todos' || r.language.toLowerCase() === lang;
                return matchQ && matchLang;
            });

            if (sort === 'stars') {
                filtered.sort((a, b) => b.stars - a.stars);
            } else if (sort === 'name') {
                filtered.sort((a, b) => a.full_name.localeCompare(b.full_name));
            } else {
                filtered.sort((a, b) => a.index - b.index);
            }

            renderRepos(filtered);
        }

        async function triggerSync() {
            const btn = document.getElementById('btnSync');
            btn.disabled = true;
            btn.innerHTML = '<span>⏳</span><span>Sincronizando...</span>';
            showToast('Sincronização iniciada com o GitHub!');

            try {
                await fetch('/api/sync', { method: 'POST' });
                pollSyncStatus();
            } catch (e) {
                console.error(e);
                btn.disabled = false;
                btn.innerHTML = '<span>🔄</span><span>Sincronizar Agora</span>';
            }
        }

        async function pollSyncStatus() {
            try {
                const res = await fetch('/api/sync/status');
                const data = await res.json();
                const badge = document.getElementById('syncStatusBadge');

                if (data.is_syncing) {
                    badge.innerText = '⚡ ' + data.progress_message;
                    setTimeout(pollSyncStatus, 2000);
                } else {
                    badge.innerText = data.last_sync_result ? `Status: ${data.last_sync_result}` : 'Pronto';
                    const btn = document.getElementById('btnSync');
                    btn.disabled = false;
                    btn.innerHTML = '<span>🔄</span><span>Sincronizar Agora</span>';
                    fetchStats();
                    fetchStars();
                    showToast('Catálogo sincronizado com sucesso!');
                }
            } catch (e) {
                console.error(e);
            }
        }

        // Inicialização
        fetchStats();
        fetchStars();
    </script>
</body>
</html>
"""

async def home_page(request):
    """Renderiza a página principal do Hub de Favoritos."""
    return HTMLResponse(HTML_TEMPLATE)

# ── Rotas e Inicialização da Aplicação ────────────────────────────────────────

routes = [
    Route("/", endpoint=home_page, methods=["GET"]),
    Route("/api/stars", endpoint=api_stars, methods=["GET"]),
    Route("/api/stats", endpoint=api_stats, methods=["GET"]),
    Route("/api/sync", endpoint=api_sync_start, methods=["POST"]),
    Route("/api/sync/status", endpoint=api_sync_status, methods=["GET"]),
]

app = Starlette(
    debug=True,
    routes=routes,
    middleware=[
        Middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
    ]
)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print("==================================================")
    print("   🌟 GITHUB STARRED HUB - WEB APP INICIANDO")
    print("==================================================")
    print(f"-> Servidor pronto em: http://127.0.0.1:{port}")
    print("-> Pressione Ctrl+C para encerrar.")
    print("==================================================")
    uvicorn.run("app:app", host="127.0.0.1", port=port, reload=False, log_level="info")
