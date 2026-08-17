# -*- coding: utf-8 -*-
"""
Suíte de Testes Automatizados para Validação de Integridade do Catálogo
"""

import os
import re
import sys
import subprocess

sys.stdout.reconfigure(encoding='utf-8')

def run_tests():
    print("--- INICIANDO TESTES DE VALIDAÇÃO ---")
    
    # Teste 1: Executar star_tracker.py
    print("[1/5] Executando star_tracker.py...")
    res = subprocess.run([sys.executable, "scripts/star_tracker.py"], capture_output=True, text=True, encoding="utf-8")
    assert res.returncode == 0, f"star_tracker.py falhou:\n{res.stderr}"
    print("      -> star_tracker.py executou com sucesso!")

    # Teste 2: Ler CATALOGO_ESTRELAS.md
    print("[2/5] Lendo CATALOGO_ESTRELAS.md...")
    with open("CATALOGO_ESTRELAS.md", "r", encoding="utf-8") as f:
        content = f.read()

    # Teste 3: Posição do Sumário (deve estar antes das análises)
    print("[3/5] Validando posição do Sumário...")
    toc_pos = content.find("## 📑 Sumário Completo dos Repositórios")
    det_pos = content.find("## 🔍 Análise Detalhada Repositório por Repositório")
    assert 0 < toc_pos < det_pos, "ERRO: O sumário não está no topo!"
    print(f"      -> Sumário no topo confirmado (pos: {toc_pos}, detalhe: {det_pos})")

    # Teste 4: Contagem de itens e links
    print("[4/5] Validando contagem de repositórios e links de segurança...")
    toc_items = re.findall(r"^\d+\.\s+\[([^\]]+)\]\(#([^\)]+)\)", content, re.MULTILINE)
    det_items = re.findall(r"^### \d+\.\s+\[([^\]]+)\]\(([^)]+)\)", content, re.MULTILINE)
    sec_badges = re.findall(r"- 🛡️ \*\*Segurança & Malware:\*\* (.*)", content)
    dicas = re.findall(r"- ⚡ \*\*Dica Pro de produtividade:\*\* (.*)", content)

    print(f"      -> Total no Sumário: {len(toc_items)}")
    print(f"      -> Total no Detalhamento: {len(det_items)}")
    print(f"      -> Total de Badges ScanRepo: {len(sec_badges)}")
    print(f"      -> Total de Dicas Pro: {len(dicas)}")

    assert len(toc_items) == len(det_items) == len(sec_badges) == len(dicas) == 118, "ERRO na contagem de itens!"
    
    # Teste 5: Unicidade das Dicas Pro
    print("[5/5] Validando unicidade das Dicas Pro...")
    unique_dicas = set(dicas)
    assert len(unique_dicas) == len(dicas), f"ERRO: Existem {len(dicas) - len(unique_dicas)} dicas repetidas!"
    print(f"      -> Todas as {len(unique_dicas)} Dicas Pro são 100% exclusivas e personalizadas!")

    print("\n✅ TODOS OS 5 TESTES PASSARAM COM 100% DE SUCESSO!")

if __name__ == '__main__':
    run_tests()
