# -*- coding: utf-8 -*-
"""
Suíte de Testes Automatizados para Validação de Integridade do Catálogo
Verifica contagens dinâmicas, posições, ausência de frases genéricas,
unicidade absoluta de Dicas Pro e validade de badges de segurança.
"""

import os
import re
import sys
import json
import subprocess

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
ALL_STARS_FILE = os.path.join(DATA_DIR, "all_starred_github.json")
CATALOG_FILE = os.path.join(BASE_DIR, "CATALOGO_ESTRELAS.md")

GENERIC_BANNED_PHRASES = [
    "Projeto open-source em",
    "Consulte as issues e discussões do repositório no GitHub",
    "Consulte os exemplos no README para acelerar",
    "Isole as permissões de terminal de cada agente em um container",
    "Teste diferentes tamanhos de chunk (ex: 500 vs 1000",
    "Padronize a validação dos schemas de entrada",
    "Integre as regras de auditoria como pre-commit hook no Git local para barrar",
    "Configure variáveis de ambiente no arquivo .env antes da primeira inicialização para manter a persistência",
]

def run_tests():
    print("==================================================")
    print("   INICIANDO SUÍTE COMPLETA DE TESTES AUTOMATIZADOS")
    print("==================================================")

    assert os.path.exists(ALL_STARS_FILE), f"ERRO: Arquivo {ALL_STARS_FILE} não existe."

    # Teste 1: Executar star_tracker.py (gera/atualiza all_starred_github.json e CATALOGO_ESTRELAS.md)
    print("\n[1/6] Executando scripts/star_tracker.py...")
    res = subprocess.run([sys.executable, os.path.join(BASE_DIR, "scripts", "star_tracker.py")], capture_output=True, text=True, encoding="utf-8", errors="replace")
    assert res.returncode == 0, f"star_tracker.py falhou com código {res.returncode}:\n{res.stderr}\n{res.stdout}"
    print("      -> star_tracker.py executou com sucesso (Código 0)!")

    # 2. Carregar contagem esperada DINAMICAMENTE a partir do JSON atualizado pelo star_tracker
    with open(ALL_STARS_FILE, "r", encoding="utf-8") as f:
        all_stars = json.load(f)
    expected_total = len(all_stars)
    print(f"\n[Info] Total esperado de repositórios (dinâmico, após star_tracker): {expected_total}")

    # Teste 2: Ler CATALOGO_ESTRELAS.md
    print("\n[2/6] Lendo CATALOGO_ESTRELAS.md...")
    assert os.path.exists(CATALOG_FILE), f"ERRO: {CATALOG_FILE} não encontrado."
    with open(CATALOG_FILE, "r", encoding="utf-8") as f:
        content = f.read()
    assert len(content) > 10000, f"ERRO: Tamanho do catálogo anormalmente pequeno ({len(content)} bytes)."
    print(f"      -> Arquivo lido com sucesso ({len(content):,} caracteres).")

    # Teste 3: Posição do Sumário (deve estar antes das análises)
    print("\n[3/6] Validando estrutura e posição do Sumário...")
    toc_pos = content.find("## 📑 Sumário Completo dos Repositórios")
    det_pos = content.find("## 🔍 Análise Detalhada Repositório por Repositório")
    assert 0 < toc_pos < det_pos, "ERRO CRÍTICO: O Sumário não está posicionado no topo!"
    print(f"      -> Sumário no topo validado (TOC pos: {toc_pos}, Detalhe pos: {det_pos})")

    # Teste 4: Contagem dinâmica de itens e links
    print("\n[4/6] Validando contagem dinâmica de repositórios...")
    toc_items = re.findall(r"^\d+\.\s+\[([^\]]+)\]\(#([^\)]+)\)", content, re.MULTILINE)
    det_items = re.findall(r"^### \d+\.\s+\[([^\]]+)\]\(([^)]+)\)", content, re.MULTILINE)
    sec_badges = re.findall(r"- 🛡️ \*\*Segurança & Malware:\*\* (.*)", content)
    dicas = re.findall(r"- ⚡ \*\*Dica Pro de produtividade:\*\* (.*)", content)
    whats = re.findall(r"- 🎯 \*\*O que é e para que serve:\*\* (.*)", content)
    cases = re.findall(r"- 💡 \*\*Casos de uso reais no dia a dia:\*\* (.*)", content)

    print(f"      -> Itens no Sumário: {len(toc_items)} / {expected_total}")
    print(f"      -> Seções Detalhadas: {len(det_items)} / {expected_total}")
    print(f"      -> Badges ScanRepo: {len(sec_badges)} / {expected_total}")
    print(f"      -> Dicas Pro: {len(dicas)} / {expected_total}")
    print(f"      -> O que é e para que serve: {len(whats)} / {expected_total}")
    print(f"      -> Casos de uso: {len(cases)} / {expected_total}")

    assert len(toc_items) == expected_total, f"ERRO: Sumário contém {len(toc_items)}, esperado {expected_total}"
    assert len(det_items) == expected_total, f"ERRO: Detalhamento contém {len(det_items)}, esperado {expected_total}"
    assert len(sec_badges) == expected_total, f"ERRO: Badges de segurança contém {len(sec_badges)}, esperado {expected_total}"
    assert len(dicas) == expected_total, f"ERRO: Dicas Pro contém {len(dicas)}, esperado {expected_total}"
    assert len(whats) == expected_total, f"ERRO: 'O que é' contém {len(whats)}, esperado {expected_total}"
    assert len(cases) == expected_total, f"ERRO: 'Casos de uso' contém {len(cases)}, esperado {expected_total}"

    # Teste 5: Unicidade absoluta das Dicas Pro
    print("\n[5/6] Validando unicidade absoluta das Dicas Pro...")
    unique_dicas = set(dicas)
    duplicates = len(dicas) - len(unique_dicas)
    assert duplicates == 0, f"ERRO: Existem {duplicates} Dicas Pro repetidas!"
    print(f"      -> Todas as {len(unique_dicas)} Dicas Pro são 100% EXCLUSIVAS e personalizadas!")

    # Teste 6: Auditoria de frases genéricas banidas
    print("\n[6/6] Auditando ausência de frases genéricas banidas...")
    found_generic = []
    for phrase in GENERIC_BANNED_PHRASES:
        if phrase in content:
            found_generic.append(phrase)

    assert len(found_generic) == 0, f"ERRO: Frases genéricas encontradas no catálogo:\n" + "\n".join(found_generic)
    print("      -> ZERO frases genéricas encontradas! Catálogo 100% individualizado e técnico.")

    print("\n==================================================")
    print(f"✅ TODOS OS 6 TESTES PASSARAM COM 100% DE SUCESSO!")
    print(f"   Catálogo verificado e homologado para {expected_total} repositórios.")
    print("==================================================")

if __name__ == '__main__':
    run_tests()
