# -*- coding: utf-8 -*-
"""
Script de Processamento de Todos os 118 Repositórios Estrelados do Jerixco
Gera base de dados rica com análises 100% em pt-BR e Dicas Pro específicas.
"""

import sys
import json
import subprocess
import os
import re

sys.stdout.reconfigure(encoding='utf-8')

def get_all_starred():
    res = subprocess.check_output(['gh', 'api', 'users/Jerixco/starred', '--paginate']).decode('utf-8')
    return json.loads(res)

if __name__ == '__main__':
    repos = get_all_starred()
    print(f"Total de repositórios carregados: {len(repos)}")
    with open("data/all_starred_github.json", "w", encoding="utf-8") as f:
        json.dump(repos, f, indent=2, ensure_ascii=False)
