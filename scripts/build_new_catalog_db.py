# -*- coding: utf-8 -*-
"""
Catalog builder dinâmico para repositórios estrelados.
Gera catalog_db.json chamando analyze_repository do star_tracker para cada repo.
Substitui qualquer dicionário hardcoded por análise dinâmica contextual via star_tracker.

Nunca usa texto genérico — cada repo é analisado individualmente usando:
- Descrição do GitHub + tópicos + README real
- IA (Gemini/OpenAI) quando disponível
- Fallback contextual avançado baseado em README e tópicos
"""

import json
import sys
import os
import subprocess
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
ALL_STARS_FILE = DATA_DIR / "all_starred_github.json"
CATALOG_DB_FILE = DATA_DIR / "catalog_db.json"
MASTER_DB_FILE = DATA_DIR / "master_catalog_db.json"

scripts_dir = BASE_DIR / "scripts"
if str(scripts_dir) not in sys.path:
    sys.path.insert(0, str(scripts_dir))


def get_all_starred():
    """Obtém lista de repositórios estrelados via gh CLI ou cache local."""
    try:
        res = subprocess.check_output(
            ['gh', 'api', 'users/Jerixco/starred', '--paginate'],
            stderr=subprocess.DEVNULL
        ).decode('utf-8', errors='replace')
        data = json.loads(res)
        if data and isinstance(data, list):
            # Salvar cache atualizado
            with open(ALL_STARS_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return data
    except Exception:
        pass

    if ALL_STARS_FILE.exists():
        with open(ALL_STARS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    print(f"ERRO: Não foi possível obter repositórios e {ALL_STARS_FILE} não existe.")
    sys.exit(1)


def load_star_tracker_analyzer():
    """Carrega analyze_repository do star_tracker dinamicamente."""
    import importlib.util
    star_tracker_path = scripts_dir / "star_tracker.py"
    spec = importlib.util.spec_from_file_location("star_tracker", star_tracker_path)
    star_tracker = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(star_tracker)
    return star_tracker.analyze_repository


def build_dynamic_catalog():
    """Gera catalog_db.json chamando analyze_repository para cada repo estrelado."""
    repos = get_all_starred()
    print(f"Total de repositórios carregados: {len(repos)}")

    # Carregar banco existente para preservar análises prévias
    catalog_db = {}
    if CATALOG_DB_FILE.exists():
        try:
            with open(CATALOG_DB_FILE, "r", encoding="utf-8") as f:
                catalog_db = json.load(f)
        except Exception:
            catalog_db = {}
    elif MASTER_DB_FILE.exists():
        try:
            with open(MASTER_DB_FILE, "r", encoding="utf-8") as f:
                catalog_db = json.load(f)
        except Exception:
            catalog_db = {}

    analyze_repo = load_star_tracker_analyzer()
    
    analyzed_count = 0
    for repo in repos:
        full_name = repo.get("full_name", "")
        if not full_name:
            continue
        if full_name in catalog_db and catalog_db[full_name].get("what"):
            continue
        print(f"Analisando: {full_name}...")
        analysis = analyze_repo(repo)
        catalog_db[full_name] = analysis
        analyzed_count += 1

    print(f"Novas análises realizadas: {analyzed_count}")

    with open(CATALOG_DB_FILE, "w", encoding="utf-8") as f:
        json.dump(catalog_db, f, indent=2, ensure_ascii=False)

    with open(MASTER_DB_FILE, "w", encoding="utf-8") as f:
        json.dump(catalog_db, f, indent=2, ensure_ascii=False)
    
    print(f"Salvas {len(catalog_db)} entradas detalhadas em {CATALOG_DB_FILE}")


if __name__ == "__main__":
    build_dynamic_catalog()
