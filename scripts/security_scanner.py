# -*- coding: utf-8 -*-
"""
Módulo de Varredura Heurística de Segurança Integrado (Inspirado no ScanRepo)
"""

import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Base de assinaturas de ameaças conhecidas (Threat Intel do ScanRepo / Ruben Marcus)
KNOWN_MALICIOUS_DOMAINS = [
    "api.npoint.io", "w3capi.marketing", "mglcoin.io", "144.172.94.226"
]

SUSPICIOUS_CODE_PATTERNS = [
    r"eval\s*\(\s*atob\s*\(",
    r"new\s+Function\s*\(\s*['\"]require['\"]",
    r"process\.on\s*\(\s*['\"]uncaughtException['\"]\s*,\s*\(\s*\)\s*=>\s*\{\s*\}\s*\)",
    r"\\x[0-9a-fA-F]{2}\\x[0-9a-fA-F]{2}\\x[0-9a-fA-F]{2}",
]

def scan_repository_security(repo_info, readme_text=""):
    """
    Realiza uma varredura estática de segurança e gera o bloco com o badge do ScanRepo.
    """
    full_name = repo_info.get("full_name", "")
    description = (repo_info.get("description") or "").lower()
    readme_lower = (readme_text or "").lower()
    
    # 1. Repositórios especificamente conhecidos como base de malwares para estudo
    if full_name == "rubenmarcus/malicious-repositories":
        return f"⚠️ *Repositório de Amostras de Malware (Estudo/Pesquisa)* | [![ScanRepo](https://img.shields.io/badge/ScanRepo-Auditar_Código-e05d44?style=flat-square&logo=shield)](https://www.scanrepo.dev/scan/github/{full_name})"

    # 2. Verificação de domínios ou IPs maliciosos conhecidos
    for domain in KNOWN_MALICIOUS_DOMAINS:
        if domain in description or domain in readme_lower:
            return f"🚨 *Alerta: Padrão C2 detectado ({domain})* | [![ScanRepo](https://img.shields.io/badge/ScanRepo-Auditar_Código-critical?style=flat-square&logo=shield)](https://www.scanrepo.dev/scan/github/{full_name})"

    # 3. Verificação de padrões de código suspeitos
    for pattern in SUSPICIOUS_CODE_PATTERNS:
        if re.search(pattern, readme_text):
            return f"⚠️ *Atenção: Padrão de execução dinâmica suspeita identificado* | [![ScanRepo](https://img.shields.io/badge/ScanRepo-Auditar_Código-yellow?style=flat-square&logo=shield)](https://www.scanrepo.dev/scan/github/{full_name})"

    # 4. Caso padrão limpo
    return f"✅ *Verificado / Baixo Risco (Sem padrões maliciosos)* | [![ScanRepo](https://img.shields.io/badge/ScanRepo-Auditar_Código-2ea44f?style=flat-square&logo=shield)](https://www.scanrepo.dev/scan/github/{full_name})"

if __name__ == '__main__':
    # Teste rápido
    test_repo = {"full_name": "scrapy/scrapy", "description": "Web scraping framework"}
    print(scan_repository_security(test_repo))
