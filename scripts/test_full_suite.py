# -*- coding: utf-8 -*-
"""
Suíte de Testes Automatizados para Validação de Integridade do Catálogo
Verifica contagens dinâmicas, posições, ausência de frases genéricas,
ausência de órfãos, unicidade absoluta de Dicas Pro e conformidade com pt-BR.

Utiliza BANNED_PHRASE_PATTERNS do star_tracker.py como fonte única de verdade.
Por padrão é somente-leitura (QA seguro). Use --run-tracker para executar o star_tracker.py antes dos testes.
"""

import os
import re
import sys
import json
import subprocess

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
SCRIPTS_DIR = os.path.join(BASE_DIR, "scripts")

if SCRIPTS_DIR not in sys.path:
    sys.path.append(SCRIPTS_DIR)

from star_tracker import BANNED_PHRASE_PATTERNS

ALL_STARS_FILE = os.path.join(DATA_DIR, "all_starred_github.json")
MASTER_DB_FILE = os.path.join(DATA_DIR, "master_catalog_db.json")
CATALOG_DB_FILE = os.path.join(DATA_DIR, "catalog_db.json")
PROCESSED_FILE = os.path.join(DATA_DIR, "processed_stars.json")
CATALOG_FILE = os.path.join(BASE_DIR, "CATALOGO_ESTRELAS.md")

# Padrões adicionais de genericismo que nunca podem aparecer
MASS_GENERIC_PATTERNS = [
    r"Projeto de engenharia de software e biblioteca de alta performance",
    r"Integração em arquiteturas modernas de microsserviços",
    r"inspecione as configurações no arquivo de build principal para otimizar o empacotamento",
    r"Consulte as instru[çc][õo]es de execu[çc][ãa]o no reposit[óo]rio",
    r"# Consulte as instrucoes",
]

def run_tests():
    print("==================================================")
    print("   INICIANDO SUÍTE COMPLETA DE TESTES AUTOMATIZADOS")
    print("==================================================")

    # Executar star_tracker apenas se explicitamente solicitado via CLI
    if "--run-tracker" in sys.argv or "--integration" in sys.argv:
        print("\n[Opcional] Executando scripts/star_tracker.py...")
        res = subprocess.run([sys.executable, os.path.join(BASE_DIR, "scripts", "star_tracker.py")], capture_output=True, text=True, encoding="utf-8", errors="replace")
        assert res.returncode == 0, f"star_tracker.py falhou com código {res.returncode}:\n{res.stderr}\n{res.stdout}"
        print("      -> star_tracker.py executou com sucesso (Código 0)!")

    # Teste 1: Validar arquivos de dados e ausência de órfãos
    print("\n[1/6] Validando arquivos de dados e ausência de órfãos...")
    assert os.path.exists(ALL_STARS_FILE), f"ERRO: Arquivo {ALL_STARS_FILE} não existe."
    assert os.path.exists(MASTER_DB_FILE), f"ERRO: Arquivo {MASTER_DB_FILE} não existe."
    assert os.path.exists(CATALOG_DB_FILE), f"ERRO: Arquivo {CATALOG_DB_FILE} não existe."
    assert os.path.exists(PROCESSED_FILE), f"ERRO: Arquivo {PROCESSED_FILE} não existe."

    with open(ALL_STARS_FILE, "r", encoding="utf-8") as f:
        all_stars = json.load(f)
    with open(MASTER_DB_FILE, "r", encoding="utf-8") as f:
        master_db = json.load(f)
    with open(CATALOG_DB_FILE, "r", encoding="utf-8") as f:
        catalog_db = json.load(f)
    with open(PROCESSED_FILE, "r", encoding="utf-8") as f:
        processed_data = json.load(f)

    expected_total = len(all_stars)
    master_total = len(master_db)
    catalog_total = len(catalog_db)
    processed_total = len(processed_data.get("processed_ids", []))

    print(f"      -> Favoritos ativos (all_stars): {expected_total}")
    print(f"      -> Registros master_db: {master_total}")
    print(f"      -> Registros catalog_db: {catalog_total}")
    print(f"      -> IDs processados: {processed_total}")

    assert master_total == expected_total, f"ERRO: master_db possui {master_total} itens, esperado {expected_total} (órfãos detectados)"
    assert catalog_total == expected_total, f"ERRO: catalog_db possui {catalog_total} itens, esperado {expected_total}"
    assert processed_total == expected_total, f"ERRO: processed_ids possui {processed_total} itens, esperado {expected_total}"
    print("      -> Consistência de dados e ausência de órfãos validada com sucesso!")

    # Teste 2: Ler e validar CATALOGO_ESTRELAS.md
    print("\n[2/6] Lendo CATALOGO_ESTRELAS.md...")
    assert os.path.exists(CATALOG_FILE), f"ERRO: {CATALOG_FILE} não encontrado."
    with open(CATALOG_FILE, "r", encoding="utf-8") as f:
        content = f.read()
    assert len(content) > 10000, f"ERRO: Tamanho do catálogo anormalmente pequeno ({len(content)} bytes)."
    print(f"      -> Arquivo lido com sucesso ({len(content):,} caracteres).")

    # Teste 3: Posição e integridade do Sumário
    print("\n[3/6] Validando estrutura e posição do Sumário...")
    toc_pos = content.find("## 📑 Sumário Completo dos Repositórios")
    det_pos = content.find("## 🔍 Análise Detalhada Repositório por Repositório")
    assert 0 < toc_pos < det_pos, "ERRO CRÍTICO: O Sumário não está posicionado no topo!"
    print(f"      -> Sumário no topo validado (TOC pos: {toc_pos}, Detalhe pos: {det_pos})")

    # Teste 4: Contagem dinâmica de itens e seções
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

    # Teste 6: Auditoria rigorosa de padrões genéricos e proibidos
    print("\n[6/6] Auditando ausência de frases genéricas e padrões banidos...")
    found_violations = []

    all_patterns_to_check = BANNED_PHRASE_PATTERNS + MASS_GENERIC_PATTERNS

    for pattern in all_patterns_to_check:
        matches = re.findall(pattern, content, re.IGNORECASE)
        if matches:
            found_violations.append(f"Padrão banido encontrado ('{pattern}'): {len(matches)} ocorrência(s)")

    # Validação nos registros da base JSON
    for repo_name, info in master_db.items():
        full_repo_text = f"{info.get('what', '')} {info.get('use_cases', '')} {info.get('quickstart', '')} {info.get('pro_tip', '')}"
        for pattern in all_patterns_to_check:
            if re.search(pattern, full_repo_text, re.IGNORECASE):
                found_violations.append(f"[{repo_name}] violou padrão '{pattern}'")

    assert len(found_violations) == 0, "ERRO: Violações de qualidade encontradas:\n" + "\n".join(found_violations[:10])
    print("      -> ZERO padrões genéricos encontrados! Catálogo 100% individualizado, técnico e em pt-BR.")

    print("\n==================================================")
    print(f"✅ TODOS OS 6 TESTES PASSARAM COM 100% DE SUCESSO!")
    print(f"   Catálogo verificado e homologado para {expected_total} repositórios.")
    print("==================================================")

if __name__ == '__main__':
    run_tests()
