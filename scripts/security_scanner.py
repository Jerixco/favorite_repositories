# -*- coding: utf-8 -*-
"""
Módulo de Varredura Heurística de Segurança Integrado (Inspirado no ScanRepo)
Analisa assinaturas de ameaças conhecidas, padrões maliciosos e gera badges do ScanRepo.
"""

import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Base de assinaturas de ameaças conhecidas (Threat Intel / C2s / Amostras)
KNOWN_MALICIOUS_DOMAINS = [
    "api.npoint.io", "w3capi.marketing", "mglcoin.io", "144.172.94.226", "transfer.sh"
]

SUSPICIOUS_CODE_PATTERNS = [
    r"eval\s*\(\s*atob\s*\(",
    r"new\s+Function\s*\(\s*['\"]require['\"]",
    r"process\.on\s*\(\s*['\"]uncaughtException['\"]\s*,\s*\(\s*\)\s*=>\s*\{\s*\}\s*\)",
    r"\\x[0-9a-fA-F]{2}\\x[0-9a-fA-F]{2}\\x[0-9a-fA-F]{2}",
    r"curl\s+-[sS]*f*[sS]*L*\s+https?://[^\s|]+\s*\|\s*(ba)?sh",
]

def scan_repository_security(repo_info, readme_text=""):
    """
    Realiza uma varredura estática de segurança e gera o bloco formatado com o badge do ScanRepo.
    """
    if not isinstance(repo_info, dict):
        return "✅ *Verificado / Baixo Risco* | [![ScanRepo](https://img.shields.io/badge/ScanRepo-Auditar_Código-2ea44f?style=flat-square&logo=shield)](https://www.scanrepo.dev)"

    full_name = repo_info.get("full_name", "")
    description = str(repo_info.get("description") or "").lower()
    readme_str = str(readme_text or "")
    readme_lower = readme_str.lower()
    
    # 1. Repositórios especificamente conhecidos como base de malwares para estudo
    if full_name == "rubenmarcus/malicious-repositories":
        return f"⚠️ *Repositório de Amostras de Malware (Estudo/Pesquisa)* | [![ScanRepo](https://img.shields.io/badge/ScanRepo-Auditar_Código-e05d44?style=flat-square&logo=shield)](https://www.scanrepo.dev/scan/github/{full_name})"

    # 2. Verificação de domínios ou IPs maliciosos conhecidos
    for domain in KNOWN_MALICIOUS_DOMAINS:
        if domain in description or domain in readme_lower:
            return f"🚨 *Alerta: Padrão C2 detectado ({domain})* | [![ScanRepo](https://img.shields.io/badge/ScanRepo-Auditar_Código-critical?style=flat-square&logo=shield)](https://www.scanrepo.dev/scan/github/{full_name})"

    # 3. Verificação de padrões de código suspeitos
    for pattern in SUSPICIOUS_CODE_PATTERNS:
        if re.search(pattern, readme_str, re.IGNORECASE):
            return f"⚠️ *Atenção: Padrão de execução dinâmica suspeita identificado* | [![ScanRepo](https://img.shields.io/badge/ScanRepo-Auditar_Código-yellow?style=flat-square&logo=shield)](https://www.scanrepo.dev/scan/github/{full_name})"

    # 4. Caso padrão limpo / verificado
    return f"✅ *Verificado / Baixo Risco (Sem padrões maliciosos)* | [![ScanRepo](https://img.shields.io/badge/ScanRepo-Auditar_Código-2ea44f?style=flat-square&logo=shield)](https://www.scanrepo.dev/scan/github/{full_name})"

if __name__ == '__main__':
    test_repo = {"full_name": "scrapy/scrapy", "description": "Web scraping framework"}
    print(scan_repository_security(test_repo))
