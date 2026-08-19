# -*- coding: utf-8 -*-
"""
Script de Extração de Repositórios Estrelados do GitHub
Atualiza data/all_starred_github.json de forma dinâmica e resiliente.
"""

import sys
import json
import subprocess
import os

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
ALL_STARS_FILE = os.path.join(DATA_DIR, "all_starred_github.json")

def get_all_starred():
    try:
        res = subprocess.check_output(
            ['gh', 'api', 'users/Jerixco/starred', '--paginate'],
            stderr=subprocess.DEVNULL
        ).decode('utf-8', errors='replace')
        return json.loads(res)
    except Exception as e:
        print(f"Aviso ao consultar gh CLI: {e}")
        if os.path.exists(ALL_STARS_FILE):
            with open(ALL_STARS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

if __name__ == '__main__':
    repos = get_all_starred()
    print(f"Total de repositórios carregados: {len(repos)}")
    if repos:
        os.makedirs(DATA_DIR, exist_ok=True)
        with open(ALL_STARS_FILE, "w", encoding="utf-8") as f:
            json.dump(repos, f, indent=2, ensure_ascii=False)
        print(f"Salvo com sucesso em: {ALL_STARS_FILE}")
