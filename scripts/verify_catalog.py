# -*- coding: utf-8 -*-
"""
Script Rápido de Verificação da Estrutura do Catálogo Markdown
"""

import os
import re
import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
ALL_STARS_FILE = os.path.join(DATA_DIR, "all_starred_github.json")
CATALOG_FILE = os.path.join(BASE_DIR, "CATALOGO_ESTRELAS.md")

with open(ALL_STARS_FILE, "r", encoding="utf-8") as f:
    stars = json.load(f)
expected_total = len(stars)

with open(CATALOG_FILE, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Verificar sumário no topo
toc_pos = content.find("## 📑 Sumário Completo dos Repositórios")
det_pos = content.find("## 🔍 Análise Detalhada Repositório por Repositório")

print(f"Posição do Sumário: {toc_pos}")
print(f"Posição da Análise Detalhada: {det_pos}")
assert 0 < toc_pos < det_pos, "O sumário DEVE vir antes das análises detalhadas!"

# 2. Contar itens no sumário
toc_items = re.findall(r"^\d+\.\s+\[([^\]]+)\]\(#([^\)]+)\)", content, re.MULTILINE)
print(f"Total de itens no Sumário: {len(toc_items)} (Esperado: {expected_total})")
assert len(toc_items) == expected_total

# 3. Contar seções detalhadas
det_items = re.findall(r"^### \d+\.\s+\[([^\]]+)\]\(([^)]+)\)", content, re.MULTILINE)
print(f"Total de seções detalhadas: {len(det_items)} (Esperado: {expected_total})")
assert len(det_items) == expected_total

# 4. Verificar se há dicas repetidas
dicas = re.findall(r"- ⚡ \*\*Dica Pro de produtividade:\*\* (.*)", content)
print(f"Total de Dicas Pro encontradas: {len(dicas)}")
unique_dicas = set(dicas)
print(f"Total de Dicas Pro únicas: {len(unique_dicas)}")
assert len(dicas) == len(unique_dicas), f"Existem {len(dicas) - len(unique_dicas)} dicas repetidas!"

print("\nVerificação concluída com 100% de sucesso!")
