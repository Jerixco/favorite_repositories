# -*- coding: utf-8 -*-
"""
Script de Rastreamento e Análise Automática de Estrelas do GitHub
Executado via GitHub Actions de forma 100% autônoma, resiliente e determinística.

Garante:
1. Sumário Completo SEMPRE no topo com 100% dos repositórios estrelados
2. Análise individualizada e técnica profunda para cada repositório (100% PT-BR)
3. Dica Pro técnica, rica, avançada e 100% exclusiva (sem repetições ou generalismos)
4. Módulo de Segurança e Auditoria de Malware (ScanRepo + Heurísticas Locais)
5. Zero dependência de constantes estáticas; suporte automático a novos favoritos.
"""

import os
import sys
import re
import json
import base64
import urllib.request
import urllib.error
from datetime import datetime, timezone

sys.stdout.reconfigure(encoding='utf-8')

# Importar o scanner de segurança
scripts_dir = os.path.dirname(os.path.abspath(__file__))
if scripts_dir not in sys.path:
    sys.path.append(scripts_dir)

from security_scanner import scan_repository_security
try:
    from knowledge_catalog import REPO_KNOWLEDGE_BASE
except ImportError:
    REPO_KNOWLEDGE_BASE = {}

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Carregador de variáveis de ambiente (.env)
def load_env_file():
    """Carrega variáveis de ambiente de arquivos .env locais se existirem."""
    candidate_paths = [
        os.path.join(BASE_DIR, ".env"),
        os.path.join(os.path.dirname(BASE_DIR), ".env"),
        os.path.join(os.path.dirname(os.path.dirname(BASE_DIR)), ".env"),
    ]
    for env_path in candidate_paths:
        if os.path.exists(env_path):
            try:
                with open(env_path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#") and "=" in line:
                            k, v = line.split("=", 1)
                            k = k.strip()
                            v = v.strip().strip("'\"")
                            if k not in os.environ:
                                os.environ[k] = v
            except Exception:
                pass

load_env_file()

# Configurações de Ambiente
GITHUB_USERNAME = os.environ.get("TARGET_USERNAME", "Jerixco")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY", "")
TOKENROUTER_API_KEY = os.environ.get("TOKENROUTER_API_KEY", "")
FORCE_RE_SCAN = os.environ.get("FORCE_RE_SCAN", "").lower() in ("true", "1", "yes") or "--force" in sys.argv

DATA_DIR = os.path.join(BASE_DIR, "data")
PROCESSED_FILE = os.path.join(DATA_DIR, "processed_stars.json")
MASTER_DB_FILE = os.path.join(DATA_DIR, "master_catalog_db.json")
CATALOG_DB_FILE = os.path.join(DATA_DIR, "catalog_db.json")
ALL_STARS_FILE = os.path.join(DATA_DIR, "all_starred_github.json")
CATALOG_FILE = os.path.join(BASE_DIR, "CATALOGO_ESTRELAS.md")

# ==============================================================================
# REGRAS E PADRÕES DE AUDITORIA DE QUALIDADE E IDIOMA
# ==============================================================================

BANNED_PHRASE_PATTERNS = [
    r"leia a documenta[çc][ãa]o",
    r"consulte (?:o|a)\s*(?:readme|documenta[çc][ãa]o|docs|guia)",
    r"para (?:saber|obter)\s*mais",
    r"see (?:the\s*)?(?:documentation|readme|docs|guide)",
    r"see:\s*",
    r"for more information",
    r"to learn more",
    r"read (?:the\s*)?docs",
    r"check the (?:docs|documentation)",
    r"refer to the (?:documentation|readme)",
    r"keep your requirements",
    r"keep your .* synchronized",
    r"desenvolvido para oferecer alto desempenho e facilidade de integra[çc][ãa]o em fluxos modernos de engenharia",
    r"implementa[çc][ãa]o de solu[çc][õo]es focadas em",
    r"automa[çc][ãa]o de rotinas de desenvolvimento e integra[çc][ãa]o cont[íi]nua",
    r"ao integrar o `.*?`, configure as vari[áa]veis de ambiente",
    r"to install the core",
    r"install python 3\.",
    r"install-python",
    r"1\.\s*install\s+",
    r"-\s*\[git\]",
    r"to get started",
    r"getting started",
    r"to begin",
    r"consulte as instru[çc][õo]es",
]

ENGLISH_START_PATTERNS = [
    r"^(?:A|An)\s+(?:open-source|framework|library|toolkit|tool|platform|CLI|web|Python|Rust|Go|TypeScript|agentic|autonomous|curated)\b",
    r"^The\s+(?:open-source|world|agent|most|definitive|easy|free|ultimate|fastest|context|Open|ZAP)\b",
    r"^Turn\s+",
    r"^Claude\s+Code\s+is\b",
    r"^Pretty\s+fancy\s+and\s+modern\b",
    r"^Semantic\s+Search\b",
    r"^This\s+(?:project|repository|tool|library|framework|is\s+list)\b",
    r"^(?:High-performance|Real-time|An?\s+agent-managed)\b",
    r"^aider\s+is\b",
]

def _is_portuguese(text):
    """Heurística robusta: texto tem proporção expressiva de palavras em pt-BR."""
    if not text or len(text.strip()) < 10:
        return False
    pt_indicators = {
        "é", "da", "do", "dos", "das", "um", "uma", "para", "com", "que",
        "este", "esta", "esse", "essa", "pode", "poder", "ter", "ser", "como",
        "no", "na", "nos", "nas", "por", "mais", "menos", "muito", "pouco",
        "em", "de", "não", "os", "as", "se", "sua", "seu", "suas", "seus",
        "ferramenta", "plataforma", "projeto", "desenvolvimento", "automação",
        "integração", "gerenciamento", "recursos", "suporte", "dados", "guia",
        "estúdio", "sistema", "biblioteca", "ambiente", "estrutura", "análise"
    }
    words = [w for w in re.findall(r"[a-záàâãéíóúç]+", text.lower()) if len(w) > 1]
    if not words:
        return False
    pt_count = sum(1 for w in words if w in pt_indicators)
    return pt_count >= max(2, len(words) * 0.12)

def _is_english_dominant(text):
    """Detecta se o trecho possui dominância de termos em inglês."""
    if not text or len(text.strip()) < 15:
        return False
    words = [w for w in re.findall(r"[a-z]+", text.lower()) if len(w) > 1]
    if not words:
        return False
    en_words = {
        "the", "a", "an", "is", "are", "was", "were", "be", "been",
        "have", "has", "had", "do", "does", "did", "will", "would",
        "can", "could", "should", "may", "might", "must", "shall",
        "to", "of", "in", "for", "on", "with", "at", "by", "from",
        "as", "into", "through", "during", "before", "after", "above",
        "below", "between", "under", "again", "further", "then", "once",
        "here", "there", "when", "where", "why", "how", "all", "each",
        "every", "both", "few", "more", "most", "other", "some", "such",
        "no", "nor", "not", "only", "own", "same", "so", "than", "too",
        "very", "just", "and", "but", "or", "if", "while", "although",
        "because", "this", "that", "these", "those", "it", "its",
        "use", "used", "using", "based", "instead", "also", "many",
        "much", "get", "gets", "getting", "make", "made", "making",
        "see", "seen", "know", "known", "think", "thought", "take",
        "takes", "taking", "give", "gives", "giving", "find", "found",
        "work", "works", "working", "need", "needs", "needed",
        "like", "want", "wants", "way", "thing", "things", "part",
        "place", "case", "cases", "type", "types", "example", "examples",
        "include", "includes", "including", "support", "supports",
        "supported", "help", "helps", "helping", "allow", "allows",
        "enabled", "enable", "providing", "provides", "provide"
    }
    en_count = sum(1 for w in words if w in en_words)
    return en_count >= max(3, len(words) * 0.25)

def _has_english_dominant_sentence(text):
    """Verifica se há qualquer sentença ou cláusula completa em inglês dentro do texto."""
    sentences = re.split(r'[.!?\n|]', text)
    for s in sentences:
        s_clean = s.strip()
        if len(s_clean) > 25 and _is_english_dominant(s_clean):
            return True
    return False

def _is_analysis_stale(existing_analysis, repo_info=None, strict_check=False, duplicate_tips=None):
    """Detecta se uma análise existente está estagnada (inglês, genérica, campos curtos/vazios, ou fora de padrão).
    Retorna True quando a análise precisa ser reexecutada.
    """
    if FORCE_RE_SCAN and not strict_check:
        return True

    if not existing_analysis:
        return True

    what = existing_analysis.get("what", "")
    use_cases = existing_analysis.get("use_cases", "")
    pro_tip = existing_analysis.get("pro_tip", "")

    # Critério 1: campos essenciais ausentes ou curtos demais
    for val, min_len in [(what, 35), (use_cases, 25), (pro_tip, 35)]:
        if not val or not val.strip() or len(val.strip()) < min_len:
            return True

    # Critério 2: Dica Pro repetida entre múltiplos repositórios
    if duplicate_tips and repo_info:
        name = repo_info.get("full_name", "")
        if name in duplicate_tips:
            return True

    full_text = f"{what} {use_cases} {pro_tip}"

    # Critério 3: Frases e padrões genéricos banidos
    for pattern in BANNED_PHRASE_PATTERNS:
        if re.search(pattern, full_text, re.IGNORECASE):
            return True

    # Critério 4: Aberturas de sentenças em inglês nos campos principais
    for pattern in ENGLISH_START_PATTERNS:
        if re.search(pattern, what.strip(), re.IGNORECASE):
            return True

    # Critério 5: Idioma pt-BR global
    if not _is_portuguese(full_text):
        return True

    # Critério 6: Detecção de qualquer sentença completa em inglês no texto
    if _has_english_dominant_sentence(full_text):
        return True

    return False

def check_duplicate_tips(master_db):
    """Retorna conjunto de repositórios que compartilham Dicas Pro idênticas para reanálise."""
    tip_to_repos = {}
    duplicates = set()
    for name, info in master_db.items():
        tip = info.get("pro_tip", "").strip()
        if tip:
            if tip in tip_to_repos:
                duplicates.add(name)
                duplicates.add(tip_to_repos[tip])
            else:
                tip_to_repos[tip] = name
    return duplicates

# ==============================================================================
# REQUISIÇÕES HTTP E INTEGRAÇÃO COM GITHUB
# ==============================================================================

def github_request(url):
    """Executa requisição autenticada ou anônima à API do GitHub."""
    req = urllib.request.Request(url)
    req.add_header("User-Agent", "GitHub-Star-Analyzer-Bot/2.0")
    req.add_header("Accept", "application/vnd.github.v3.star+json")
    if GITHUB_TOKEN:
        req.add_header("Authorization", f"Bearer {GITHUB_TOKEN}")
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print(f"Aviso na requisição GitHub ({url}): HTTP {e.code} - {e.reason}")
        return None
    except Exception as e:
        print(f"Erro na requisição GitHub ({url}): {e}")
        return None

def _detect_readme_language(readme_text):
    """
    Detecta se o README está em português, inglês ou outro idioma.
    Usa heurística de frequência de palavras-típicas de cada língua.
    Retorna 'pt-br', 'en' ou 'other'.
    """
    if not readme_text:
        return "other"

    pt_signals = [
        "o", "uma", "para", "com", "este", "essa", "nos", "nas", "do", "da",
        "que", "é", "se", "por", "em", "um", "mais", "como", "também", "isso",
        "pode", "são", "entre", "quando", "todo", "esse", "desde", "apenas",
        "durante", "sempre", "já", "ainda", "partir", "corpo", "cada", "mesmo",
    ]
    en_signals = [
        "the", "a", "an", "for", "with", "this", "that", "is", "are", "was",
        "were", "be", "to", "of", "in", "on", "and", "or", "but", "from",
        "by", "at", "as", "its", "can", "has", "have", "not", "will", "would",
        "you", "your", "we", "they", "their", "if", "then", "than", "because",
    ]
    pt_count = sum(1 for w in pt_signals if w in readme_text.lower())
    en_count = sum(1 for w in en_signals if w in readme_text.lower())

    if pt_count == 0 and en_count == 0:
        return "other"

    if pt_count > en_count * 1.4:
        return "pt-br"
    elif en_count > pt_count * 1.4:
        return "en"
    return "other"


def get_repo_readme(owner, repo):
    """Obtém o README do repositório decodificado."""
    url = f"https://api.github.com/repos/{owner}/{repo}/readme"
    data = github_request(url)
    if data and isinstance(data, dict) and "content" in data:
        try:
            return base64.b64decode(data["content"]).decode("utf-8", errors="ignore")[:7000]
        except Exception:
            return ""
    return ""

# ==============================================================================
# PARSER DE RESPOSTAS DE IA
# ==============================================================================

def parse_ai_response(text):
    """
    Parser resiliente que aceita JSON puro ou múltiplos formatos de Markdown.
    Valida obrigatoriamente que a resposta é em pt-BR e livre de generalismos.
    """
    if not text:
        return None

    cleaned = text.strip()
    result = None

    # 1. Tentar parsear como JSON direto caso a IA tenha respondido em JSON
    if cleaned.startswith("{") and cleaned.endswith("}"):
        try:
            data = json.loads(cleaned)
            if "what" in data and "use_cases" in data and "pro_tip" in data:
                quick = data.get("quickstart", "```bash\ngit clone repo\n```")
                if "```" not in quick:
                    quick = f"```bash\n{quick}\n```"
                result = {
                    "what": data["what"].strip(),
                    "use_cases": data["use_cases"].strip(),
                    "quickstart": quick.strip(),
                    "pro_tip": data["pro_tip"].strip()
                }
        except Exception:
            pass

    # 2. Extração flexível por padrões semânticos de seções
    if not result:
        what_pattern = r"(?:🎯|\*\*🎯|###\s*🎯)?\s*(?:\*\*)?O que é e para que serve:?(?:\*\*)?:?\s*(.*?)(?=(?:💡|\*\*💡|###\s*💡|-?\s*💡|\*\*Casos de uso)|\Z)"
        use_pattern = r"(?:💡|\*\*💡|###\s*💡)?\s*(?:\*\*)?Casos de uso reais(?: no dia a dia)?:?(?:\*\*)?:?\s*(.*?)(?=(?:🚀|\*\*🚀|###\s*🚀|-?\s*🚀|\*\*Como usar)|\Z)"
        quick_pattern = r"(?:🚀|\*\*🚀|###\s*🚀)?\s*(?:\*\*)?Como usar na prática(?: com comandos prontos)?:?(?:\*\*)?:?\s*(.*?)(?=(?:⚡|\*\*⚡|###\s*⚡|-?\s*⚡|\*\*Dica Pro)|\Z)"
        tip_pattern = r"(?:⚡|\*\*⚡|###\s*⚡)?\s*(?:\*\*)?Dica Pro(?: de produtividade)?:?(?:\*\*)?:?\s*(.*)"

        what_match = re.search(what_pattern, cleaned, re.DOTALL | re.IGNORECASE)
        use_match = re.search(use_pattern, cleaned, re.DOTALL | re.IGNORECASE)
        quick_match = re.search(quick_pattern, cleaned, re.DOTALL | re.IGNORECASE)
        tip_match = re.search(tip_pattern, cleaned, re.DOTALL | re.IGNORECASE)

        what = what_match.group(1).strip() if what_match else ""
        use_cases = use_match.group(1).strip() if use_match else ""
        quickstart = quick_match.group(1).strip() if quick_match else ""
        pro_tip = tip_match.group(1).strip() if tip_match else ""

        # Limpeza de prefixos residuais
        what = re.sub(r"^[-*•]\s*", "", what).strip()
        use_cases = re.sub(r"^[-*•]\s*", "", use_cases).strip()
        pro_tip = re.sub(r"^[-*•]\s*", "", pro_tip).strip()

        if what and use_cases and pro_tip:
            if "```" not in quickstart:
                quickstart = f"```bash\n{quickstart}\n```" if quickstart else "```bash\n# Inicialize o projeto conforme o guia de instalacao\n```"
            result = {
                "what": what,
                "use_cases": use_cases,
                "quickstart": quickstart,
                "pro_tip": pro_tip
            }

    # Validação estrita de qualidade e idioma da resposta da IA
    if result:
        # Se a resposta gerada contiver frases banidas ou for em inglês, descartar para tentar outro provedor
        if _is_analysis_stale(result, None, strict_check=True):
            return None
        return result

    return None

# ==============================================================================
# PROVEDORES DE IA E FALLBACKS
# ==============================================================================

def call_gemini(prompt, api_version="v1beta"):
    """Chama a API do Google Gemini com fallback automático de modelos e versões de API."""
    if not GEMINI_API_KEY:
        return None

    models = [
        "gemini-3.7-flash",
        "gemini-3.6-flash",
        "gemini-3.5-flash",
        "gemini-3.5-flash-lite",
        "gemini-2.5-flash",
        "gemini-2.5-pro",
        "gemini-2.0-flash",
    ]
    api_versions = [api_version, "v1"] if api_version == "v1beta" else [api_version]

    for api_ver in api_versions:
        for model in models:
            try:
                api_url = f"https://generativelanguage.googleapis.com/{api_ver}/models/{model}:generateContent?key={GEMINI_API_KEY}"
                payload = {
                    "contents": [{"parts": [{"text": prompt}]}],
                    "generationConfig": {
                        "temperature": 0.2,
                        "maxOutputTokens": 1500,
                    }
                }
                req = urllib.request.Request(
                    api_url,
                    data=json.dumps(payload).encode("utf-8"),
                    headers={"Content-Type": "application/json"},
                )
                with urllib.request.urlopen(req, timeout=45) as resp:
                    res_data = json.loads(resp.read().decode("utf-8"))
                    text = res_data["candidates"][0]["content"]["parts"][0]["text"].strip()
                    parsed = parse_ai_response(text)
                    if parsed:
                        print(f"  → Gemini ({api_ver}/{model}) gerou análise com sucesso.")
                        return parsed
            except Exception:
                continue
    return None

def call_deepseek(prompt):
    """Chama a API do DeepSeek como fallback com modelos avançados."""
    if not DEEPSEEK_API_KEY:
        return None

    try:
        api_url = "https://api.deepseek.com/v1/chat/completions"
        payload = {
            "model": "deepseek-chat",
            "messages": [
                {
                    "role": "system",
                    "content": "Você é um arquiteto de software sênior brasileiro especializado em open-source. Responda exclusivamente em Português do Brasil com termos técnicos precisos e dicas práticas aprofundadas."
                },
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.2,
            "max_tokens": 1500,
        }
        req = urllib.request.Request(
            api_url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            },
        )
        with urllib.request.urlopen(req, timeout=45) as resp:
            res_data = json.loads(resp.read().decode("utf-8"))
            text = res_data["choices"][0]["message"]["content"].strip()
            parsed = parse_ai_response(text)
            if parsed:
                print("  → DeepSeek (deepseek-chat) gerou análise com sucesso.")
                return parsed
    except Exception as e:
        print(f"Aviso: Tentativa DeepSeek falhou ({e})")
    return None

def call_tokenrouter(prompt):
    """Chama a API do TokenRouter como fallback com painel de modelos gratuitos."""
    if not TOKENROUTER_API_KEY:
        return None

    try:
        api_url = "https://api.tokenrouter.com/v1/chat/completions"
        payload = {
            "model": "moonshotai/kimi-k3",
            "messages": [
                {"role": "system", "content": "Você é um arquiteto de software sênior brasileiro especializado em open-source. Responda exclusivamente em Português do Brasil com termos técnicos precisos e dicas práticas aprofundadas."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.2,
            "max_tokens": 1500,
        }
        req = urllib.request.Request(api_url, data=json.dumps(payload).encode("utf-8"), headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {TOKENROUTER_API_KEY}",
        })
        with urllib.request.urlopen(req, timeout=45) as resp:
            res_data = json.loads(resp.read().decode("utf-8"))
            text = res_data["choices"][0]["message"]["content"].strip()
            parsed = parse_ai_response(text)
            if parsed:
                print("  → TokenRouter (moonshotai/kimi-k3) gerou análise com sucesso.")
                return parsed
    except Exception as e:
        print(f"Aviso: Tentativa TokenRouter falhou ({e})")
    return None

def call_openai(prompt):
    """Chama a API da OpenAI como fallback secundário."""
    if not OPENAI_API_KEY:
        return None

    try:
        api_url = "https://api.openai.com/v1/chat/completions"
        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {
                    "role": "system",
                    "content": "Você é um arquiteto de software sênior brasileiro especializado em open-source. Responda exclusivamente em Português do Brasil com termos técnicos precisos e dicas práticas aprofundadas."
                },
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.2,
            "max_tokens": 1500,
        }
        req = urllib.request.Request(
            api_url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {OPENAI_API_KEY}",
            },
        )
        with urllib.request.urlopen(req, timeout=35) as resp:
            res_data = json.loads(resp.read().decode("utf-8"))
            text = res_data["choices"][0]["message"]["content"].strip()
            parsed = parse_ai_response(text)
            if parsed:
                print("  → OpenAI (gpt-4o-mini) gerou análise com sucesso.")
                return parsed
    except Exception as e:
        print(f"Aviso: Tentativa OpenAI falhou ({e})")
    return None

def call_openrouter(prompt):
    """Chama a API do OpenRouter como fallback gratuito agnóstico."""
    if not OPENROUTER_API_KEY:
        return None

    try:
        api_url = "https://openrouter.ai/api/v1/chat/completions"
        payload = {
            "model": "openrouter/free",
            "messages": [
                {
                    "role": "system",
                    "content": "Você é um arquiteto de software sênior brasileiro especializado em open-source. Responda exclusivamente em Português do Brasil com termos técnicos precisos e dicas práticas aprofundadas."
                },
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.2,
            "max_tokens": 1500,
        }
        req = urllib.request.Request(
            api_url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "HTTP-Referer": "https://github.com/Jerixco/favorite_repositories",
                "X-Title": "GitHub Star Analyzer",
            },
        )
        with urllib.request.urlopen(req, timeout=45) as resp:
            res_data = json.loads(resp.read().decode("utf-8"))
            text = res_data["choices"][0]["message"]["content"].strip()
            parsed = parse_ai_response(text)
            if parsed:
                print("  → OpenRouter (openrouter/free) gerou análise com sucesso.")
                return parsed
    except Exception as e:
        print(f"Aviso: Tentativa OpenRouter falhou ({e})")
    return None

# ==============================================================================
# ANALISADOR DINÂMICO CONTEXTUAL (FALLBACK OFFLINE/RESILIENTE)
# ==============================================================================

def generate_smart_dynamic_analysis(repo_info, readme_text):
    """
    Gera uma análise individualizada e contextual diretamente baseada no README,
    descrição, tópicos reais e padrões de projeto do repositório.
    Garante 100% PT-BR e unicidade absoluta.
    """
    full_name = repo_info.get("full_name", "")
    if full_name in REPO_KNOWLEDGE_BASE:
        kb = REPO_KNOWLEDGE_BASE[full_name]
        return {
            "what": kb["what"],
            "use_cases": kb["use_cases"],
            "quickstart": kb["quickstart"],
            "pro_tip": kb["pro_tip"]
        }

    description = (repo_info.get("description") or "").strip()
    language = repo_info.get("language") or "Docs / Shell"
    topics = repo_info.get("topics") or []
    name = full_name.split("/")[-1]
    owner = full_name.split("/")[0]
    topics_set = set(t.lower() for t in topics)

    code_blocks = re.findall(r"```(?:bash|shell|sh|zsh)?\n(.*?)\n```", readme_text, re.DOTALL)
    valid_code = _extract_valid_code_block(code_blocks, language, full_name, name)

    o_que_e = _build_what_is(description, language, topics_set, readme_text, full_name, owner, name)
    casos_de_uso = _build_use_cases(description, topics_set, readme_text, language, name)
    dica_pro = _build_pro_tip(topics_set, description, language, readme_text, name, full_name)

    return {
        "what": o_que_e,
        "use_cases": casos_de_uso,
        "quickstart": f"```bash\n{valid_code}\n```",
        "pro_tip": dica_pro
    }

def _extract_valid_code_block(code_blocks, language, full_name, name):
    """Extrai o bloco de código mais relevante do README, limpando placeholders de chave e guias textuais."""
    clean_code = ""
    if code_blocks:
        for cb in code_blocks:
            cb_clean = cb.strip()
            if len(cb_clean) > 10 and any(
                k in cb_clean.lower() for k in ["install", "run", "clone", "cargo", "docker", "pip", "npm", "go build", "python"]
            ):
                # Descartar blocos com texto explicativo misturado
                if "getting started" in cb_clean.lower() or "visit http" in cb_clean.lower() or "see docs" in cb_clean.lower():
                    continue
                if any(cmd in cb_clean for cmd in ["pip install", "npm install", "cargo build", "docker", "go build", "git clone"]):
                    clean_code = cb_clean
                    break
                if any(cmd in cb_clean for cmd in ["run", "start", "serve", "execute"]) and "npm" in cb_clean:
                    clean_code = cb_clean
                    break
        if not clean_code:
            for cb in code_blocks:
                cb_clean = cb.strip()
                if len(cb_clean) > 10 and "getting started" not in cb_clean.lower():
                    clean_code = cb_clean
                    break

    if not clean_code:
        clean_code = _default_code_for_language(language.lower(), full_name, name)

    # Sanitização de placeholders de chaves para evitar falsos positivos
    clean_code = re.sub(r'--api-key\s+\w+=<key>', '# Configure a chave de API necessaria via variavel de ambiente', clean_code)
    clean_code = re.sub(r'export\s+[A-Z_]+_API_KEY=.*', '# Defina suas chaves de API no ambiente ou arquivo .env', clean_code)
    return clean_code

def _default_code_for_language(lang_lower, full_name, name):
    """Gera comando de instalação padrão baseado na linguagem detectada."""
    base = f"git clone https://github.com/{full_name}.git\ncd {name}"
    if "python" in lang_lower:
        return f"{base}\npip install -r requirements.txt"
    if "typescript" in lang_lower or "javascript" in lang_lower:
        return f"{base}\nnpm install\nnpm run dev"
    if "rust" in lang_lower:
        return f"{base}\ncargo build --release"
    if "go" in lang_lower:
        return f"{base}\ngo build"
    if "java" in lang_lower:
        return f"{base}\n./gradlew build"
    if "ruby" in lang_lower:
        return f"{base}\nbundle install"
    if "php" in lang_lower:
        return f"{base}\ncomposer install"
    return base

def _build_what_is(description, language, topics_set, readme_text, full_name, owner, name):
    """Constroi a descrição 'O que é' usando informações reais do repo em pt-BR."""
    if description and len(description.strip()) > 15:
        desc_pt = _localize_description(description, topics_set, language)
        return f"{desc_pt} Desenvolvido primariamente em {language}, mantido por @{owner}."

    if readme_text:
        purpose = _extract_purpose_from_readme(readme_text, topics_set)
        if purpose and len(purpose) > 20:
            desc_pt = _localize_description(purpose, topics_set, language)
            return f"{desc_pt} Implementado em {language}, mantido por @{owner}."

    inferred = _infer_from_topics(topics_set, language, name)
    if inferred:
        return f"{inferred}. Mantido por @{owner}."

    return f"Ferramenta e módulo '{name}' desenvolvido em {language}, mantido por @{owner} para integração e desenvolvimento de software."

def _localize_description(description, topics_set, language):
    """Adaptar description inglesa para pt-BR com contexto técnico e enriquecimento por tópicos."""
    desc = description.strip()

    prefix_map = [
        (r"^The\s+open-source\s+communication\s+infrastructure\b.*", "Infraestrutura open-source de comunicação e notificações multicanal para agentes e produtos modernos."),
        (r"^The\s+world's\s+most\s+flexible\s+commerce\s+platform\b.*", "Plataforma de comércio eletrônico flexível e modular para desenvolvedores e agentes autônomos."),
        (r"^The\s+open-source\s+alternative\s+to\s+Claude\s+Cowork\b.*", "Alternativa open-source e auto-hospedável ao Claude Cowork para colaboração inteligente."),
        (r"^The\s+agent\s+that\s+grows\s+with\s+you\b.*", "Agente de inteligência artificial adaptativo com aprendizado contínuo e autonomia operacional."),
        (r"^The\s+ZAP\s+by\s+Checkmarx\s+Core\s+project\b.*", "Projeto principal do OWASP ZAP para análise dinâmica de segurança e testes de intrusão em aplicações web."),
        (r"^Turn\s+any\s+codebase\b.*", "Transforma qualquer repositório de código, documentação e schemas em um grafo de conhecimento consultável via IA."),
        (r"^(?:A|An)\s+curated\s+collection\s+of\s+1000\+\s+agent\s+skills\b.*", "Coleção com curadoria de mais de 1000 habilidades e ferramentas para agentes de inteligência artificial."),
        (r"^The\s+most\s+powerful\s+and\s+modular\b.*", "Interface gráfica modular baseada em nós e API avançada para modelos de difusão e IA gerativa."),
        (r"^This\s+is\s+list\s+of\s+discounts\b.*", "Guia com curadoria de descontos e benefícios em ferramentas SaaS, Cloud e infraestrutura para estudantes e desenvolvedores."),
        (r"^The\s+open-source\s+AI\s+voice\s+studio\b.*", "Estúdio open-source de voz com inteligência artificial para clonagem, síntese e criação em tempo real."),
        (r"^The\s+agent\s+harness\s+performance\s+optimization\s+system\b.*", "Sistema de otimização e controle de desempenho para execução segura e orquestração de agentes."),
        (r"^(?:A|An)\s+agentic\s+skills\s+framework\b.*", "Framework de habilidades agênticas e metodologia robusta para desenvolvimento assistido por IA."),
        (r"^The\s+definitive\s+list\b.*", "Lista definitiva com curadoria das melhores ferramentas e bibliotecas para desenvolvimento."),
        (r"^The\s+easy-to-use\s+open\s+source\b.*", "Ferramenta open-source intuitiva de Business Intelligence e análise de dados para geração de dashboards e métricas."),
        (r"^The\s+free\s+coding\s+agent\b.*", "Agente autônomo e gratuito de programação para assistência e automação de código no editor."),
        (r"^Turn\s+any\s+PDF\s+or\s+image\s+document\b.*", "Transforma qualquer PDF ou documento de imagem em dados estruturados para pipelines de IA via OCR de alta precisão."),
        (r"^The\s+ultimate\s+RAG\s+for\s+your\s+monorepo\b.*", "Sistema avançado de RAG para monorepositórios com consultas semânticas e edição de bases de código multilíngues."),
        (r"^The\s+fastest\s+knowledge\s+base\b.*", "Base de conhecimento rápida e colaborativa para equipes de desenvolvimento e engenharia."),
        (r"^The\s+context\s+API\s+to\s+search,\s+scrape\b.*", "API de contexto para busca, extração e interação com a web em grande escala para modelos de IA."),
        (r"^The\s+Open\s+Source\s+DocuSign\s+Alternative\b.*", "Plataforma open-source de assinatura eletrônica e gestão de documentos com foco em privacidade."),
        (r"^The\s+fastest,\s+litest\s+AI\s+Gateway\b.*", "Gateway de IA leve e de alta velocidade com núcleo em Rust para unificar chamadas a múltiplos provedores de LLM."),
        (r"^Turn\s+your\s+PC,\s+Mac,\s+or\s+Linux\s+box\s+into\s+an\s+AI\s+server\b.*", "Transforma seu computador (PC, Mac ou Linux) em um servidor local completo de IA com suporte a LLM, RAG e agentes."),
        (r"^Turn\s+Claude\s+Code\s+into\s+a\s+full\s+game\s+dev\s+studio\b.*", "Transforma o Claude Code em um estúdio completo de desenvolvimento de jogos com dezenas de agentes especializados e fluxos coordenados."),
        (r"^Claude\s+Code\s+is\s+an\s+agentic\s+coding\s+tool\b.*", "Ferramenta de codificação agêntica que opera no terminal, compreende bases de código complexas e automatiza rotinas e fluxos Git via comandos em linguagem natural."),
        (r"^An\s+agent-managed\s+museum\s+exhibit\b.*", "Ambiente e exibição de software desenvolvida e mantida de forma 100% autônoma por agentes inteligentes em Rust sem intervenção humana."),
        (r"^Pretty\s+fancy\s+and\s+modern\s+terminal\s+file\s+manager\b.*", "Gerenciador de arquivos para terminal moderno, elegante e de alta performance com interface rica em Go."),
        (r"^Semantic\s+Search\s+&\s+Call\s+Graphs\s+for\s+AI\s+Agents\b.*", "Motor de busca semântica e grafos de chamadas para agentes de inteligência artificial com execução 100% local e privada."),
        (r"^High-performance\s+code\s+intelligence\s+MCP\s+server\b.*", "Servidor MCP de inteligência de código e alta performance, indexando bases de código em grafos de conhecimento persistentes em milissegundos."),
        (r"^An\s+autonomous\s+agent\s+that\s+conducts\s+deep\s+research\b.*", "Agente autônomo projetado para realizar pesquisas profundas e estruturadas em qualquer fonte de dados utilizando múltiplos provedores de LLM."),
        (r"^A\s+framework\s+for\s+building\s+realtime\s+voice\s+AI\s+agents\b.*", "Framework completo e otimizado para construção e orquestração de agentes conversacionais de voz com IA em tempo real."),
        (r"^aider\s+is\s+AI\s+pair\s+programming\s+in\s+your\s+terminal\b.*", "Assistente e programador em par com inteligência artificial para operação direta na linha de comando."),
        (r"^Turn\s+(.*?)\s+into\s+(.*)", r"Transforma \1 em \2."),
        (r"^(?:A |An )?open[\s-]source (?:framework|library|toolkit|tool|platform) for\b", "Framework e plataforma open-source para"),
        (r"^(?:A |An )?open[\s-]source\b", "Projeto open-source de"),
        (r"^(?:A |An )?curated list of\b", "Acervo curado e lista de referências sobre"),
        (r"^(?:A |An )?modern (?:and fast )?(?:web )?(?:framework|tool|library|platform)\b", "Ferramenta moderna e de alta performance de"),
        (r"^(?:A |An )?fast and lightweight\b", "Solução leve e de alta velocidade para"),
        (r"^Official (?:repository|Python library|Go client|SDK) for\b", "SDK e biblioteca oficial para"),
        (r"^The official\b", "Repositório oficial do"),
        (r"^A collection of\b", "Coleção abrangente e utilitários de"),
        (r"^A simple and\b", "Solução simplificada e"),
        (r"^A powerful (?:and flexible )?\b", "Solução robusta e flexível de"),
    ]
    for pattern, replacement in prefix_map:
        if re.search(pattern, desc, re.IGNORECASE):
            desc = re.sub(pattern, replacement, desc, flags=re.IGNORECASE).strip()
            break

    if topics_set:
        tech_context = _tech_context_from_topics(topics_set)
        if tech_context and tech_context.lower() not in desc.lower():
            desc = f"{desc} ({tech_context})"

    return desc

def _tech_context_from_topics(topics_set):
    """Gera contexto técnico a partir de tópicos relevantes."""
    context_map = {
        "ai": "focado em inteligência artificial",
        "machine-learning": "com capacidades de machine learning",
        "deep-learning": "com suporte a deep learning",
        "llm": "otimizado para modelos de linguagem grandes",
        "rag": "com arquitetura RAG (Retrieval-Augmented Generation)",
        "web-scraping": "para extração de dados web",
        "crawler": "para rastreamento web",
        "docker": "com suporte a containers Docker",
        "kubernetes": "com integração Kubernetes",
        "devops": "focado em práticas DevOps",
        "ci-cd": "com pipelines de CI/CD",
        "cli": "como ferramenta de linha de comando",
        "terminal": "para uso em terminal",
        "database": "com integração a bancos de dados",
        "postgresql": "com suporte a PostgreSQL",
        "security": "focado em segurança",
        "frontend": "focado em desenvolvimento frontend",
        "backend": "focado em desenvolvimento backend",
        "game": "desenvolvimento de jogos",
    }
    for topic, text in context_map.items():
        if topic in topics_set:
            return text
    return ""

def _build_use_cases(description, topics_set, readme_text, language, name):
    """Gera casos de uso práticos e reais em pt-BR."""
    cases = []

    if any(t in topics_set for t in ["ai", "llm", "rag", "langchain", "agents"]):
        cases.append(f"Orquestração e integração de fluxos com modelos de linguagem e agentes inteligentes em '{name}'")
    if any(t in topics_set for t in ["cli", "terminal", "tool"]):
        cases.append(f"Execução ágil via linha de comando em scripts de automação e terminais de desenvolvimento")
    if any(t in topics_set for t in ["docker", "devops", "kubernetes", "ci-cd"]):
        cases.append(f"Automação de pipelines de CI/CD, empacotamento em containers e orquestração de infraestrutura")
    if any(t in topics_set for t in ["database", "sql", "postgresql", "mysql", "mongodb", "redis"]):
        cases.append(f"Persistência estruturada, indexação de dados e consultas de alta performance no backend")
    if any(t in topics_set for t in ["frontend", "react", "vue", "ui", "web"]):
        cases.append(f"Construção de interfaces de usuário reativas, modulares e focadas em usabilidade")
    if any(t in topics_set for t in ["security", "malware", "vulnerability"]):
        cases.append(f"Auditoria contínua de código, detecção de segredos e prevenção de vulnerabilidades")
    if any(t in topics_set for t in ["game", "game-development", "unity", "godot"]):
        cases.append(f"Desenvolvimento e prototipagem de mecânicas de jogos e automação de assets criativos")
    if any(t in topics_set for t in ["testing", "quality"]):
        cases.append(f"Execução de testes automatizados para validação de regressões e garantia de qualidade")

    if not cases:
        cases.append(f"Desenvolvimento de soluções em {language} com integração em pipelines modernos de engenharia")
        cases.append(f"Automação de rotinas operacionais e aceleração de entrega de software")

    unique_cases = list(dict.fromkeys(cases))
    return " | ".join(unique_cases[:3])

def _extract_purpose_from_readme(readme_text, topics_set):
    """Extrai a declaração de propósito do README."""
    text_only = re.sub(r"```.*?```", "", readme_text, flags=re.DOTALL)
    text_only = re.sub(r"\[.*?\]\(.*?\)", "", text_only)
    text_only = re.sub(r"#{1,6}\s+", "", text_only)
    text_only = re.sub(r"[-*•]\s+", "", text_only)

    lines = [l.strip() for l in text_only.split("\n") if l.strip() and len(l.strip()) > 20]
    for line in lines[:10]:
        if any(kw in line.lower() for kw in ["is ", "this ", "provides", "allows", "enables", "helps", "built to", "designed"]):
            return line
        if len(line) > 80 and not line.startswith("http"):
            return line
    return ""

def _infer_from_topics(topics_set, language, name):
    """Inferência baseada nos tópicos."""
    if "ai" in topics_set or "machine-learning" in topics_set:
        return f"Plataforma inteligente focada em inteligência artificial e aprendizado de máquina desenvolvida em {language}"
    if "cli" in topics_set:
        return f"Ferramenta de terminal e linha de comando de alta produtividade construída em {language}"
    return ""

def _build_pro_tip(topics_set, description, language, readme_text, name, full_name):
    """Gera uma Dica Pro real, altamente individualizada e única para cada repositório."""
    lang_lower = language.lower()
    desc_lower = (description or "").lower()

    if "vagas" in name.lower() or "jobs" in name.lower() or "vagas" in full_name.lower():
        return f"No repositório '{full_name}', configure notificações por webhook ou feeds RSS filtrando por stack e nível de experiência para acompanhar novas oportunidades em tempo real."
    if any(t in ["voice", "audio", "realtime"] for t in topics_set) or "voice" in name.lower() or "voice" in desc_lower or "audio" in desc_lower or "realtime" in desc_lower:
        return f"Para comunicação em tempo real com '{full_name}', configure buffers de streaming entre 20ms e 50ms e ative supressão de ruído com VAD adaptativo para reduzir a latência percebida."
    if "research" in name.lower() or "researcher" in name.lower() or "research" in desc_lower:
        return f"Ao executar pesquisas aprofundadas com '{full_name}', estruture as consultas em múltiplos sub-tópicos paralelos e limite a profundidade de scraping para equilibrar precisão e tempo de resposta."
    if any(t in ["agent", "agents", "swarm", "subagents"] for t in topics_set) or "agent" in name.lower():
        return f"No '{full_name}', modularize os agentes por responsabilidade única e isole o contexto de execução de cada worker para evitar dispersão de tokens e alucinações em tarefas longas."
    if any(t in ["search", "semantic", "graph", "mcp"] for t in topics_set) or "search" in name.lower() or "grep" in name.lower():
        return f"No '{full_name}', combine indexação vetorial com re-ranking baseado em BM25 e ajuste os limites de chunk com overlap para maximizar a relevância na recuperação de contexto."
    if "docker" in topics_set or "container" in topics_set:
        return f"Adicione `.dockerignore` detalhado e utilize multi-stage builds no Dockerfile de '{full_name}' para reduzir expressivamente a imagem de produção e acelerar o deploy."
    if "kubernetes" in topics_set or "k8s" in topics_set or "helm" in topics_set:
        return f"Defina resource requests e limits com base em benchmarks de consumo real para '{full_name}', prevenindo despejos de pods (OOMKilled) sob picos de tráfego."
    if "ci-cd" in topics_set or "github-actions" in topics_set:
        return f"Configure cache de dependências e execute matrizes de teste em paralelo nos workflows de CI de '{full_name}' para reduzir o tempo de feedback nos pull requests."
    if "security" in topics_set or "malware" in topics_set or "vulnerability" in topics_set:
        return f"Integre verificações automatizadas de dependências e análise estática (SAST) no pipeline de '{full_name}' para mitigar riscos de segurança antes do merge."
    if any(t in topics_set for t in ["llm", "rag", "ai", "langchain", "ollama", "vllm"]):
        return f"Ao integrar '{full_name}' com modelos de linguagem, utilize streaming de respostas e ajuste parâmetros de chunking com overlap de 10-15% para maximizar relevância de contexto sem estourar limites de tokens."
    if any(t in topics_set for t in ["web-scraping", "crawler", "scrapy", "playwright", "puppeteer"]):
        return f"Configure rotação de User-Agents e limites de taxa de download ao executar '{full_name}' para evitar bloqueios por rate limiting em requisições concorrentes."
    if "fastapi" in topics_set or "fastapi" in desc_lower:
        return f"Utilize `response_model` com Pydantic v2 em '{full_name}' para serialização em Rust com ganho expressivo de velocidade em endpoints com grandes volumes de dados."
    if "django" in topics_set or "django" in desc_lower:
        return f"Utilize `select_related` e `prefetch_related` nas consultas ORM de '{full_name}' para mitigar o problema clássico de N+1 queries em views com relacionamentos."
    if "react" in topics_set or "nextjs" in topics_set or "next" in topics_set:
        return f"Utilize dynamic imports com Suspense no projeto '{full_name}' para lazy loading de componentes pesados, otimizando as métricas de Core Web Vitals (LCP/FCP)."
    if "vue" in topics_set or "nuxt" in topics_set:
        return f"Aproveite a Composition API e modularize composables reutilizáveis no projeto '{full_name}' para desacoplar regras de negócio da camada visual."
    if "redis" in topics_set or "redis" in desc_lower:
        return f"Defina políticas explícitas de TTL e eviction (como `allkeys-lru`) ao usar '{full_name}' com Redis para impedir esgotamento de memória em picos de escrita."
    if "postgres" in topics_set or "postgresql" in topics_set or "postgres" in desc_lower:
        return f"Crie índices parciais e utilize connection pooling com '{full_name}' para manter baixas latências de consulta e economizar conexões abertas no banco de dados."
    if "graphql" in topics_set or "graphql" in desc_lower:
        return f"Implemente `DataLoader` nas camadas de resolver de '{full_name}' para agrupar consultas ao banco e eliminar requisições redundantes."
    if "cli" in topics_set or "terminal" in topics_set:
        return f"Adicione suporte a flags `--help` autoexplicativas e auto-completar de shell (Bash/Zsh/Fish) nas ferramentas CLI de '{full_name}' para melhorar a experiência do usuário."
    if "tauri" in topics_set or "electron" in topics_set:
        return f"Isole a comunicação IPC entre frontend e backend em '{full_name}' com validação rigorosa de payload para prevenir vulnerabilidades de execução remota de código."
    if "testing" in topics_set or "pytest" in topics_set or "jest" in topics_set:
        return f"Configure testes com cobertura de branches no projeto '{full_name}' para assegurar que fluxos de exceção e fallbacks estejam 100% validados."

    # Regras por linguagem principal
    if "typescript" in lang_lower:
        return f"Ative `strict: true` no `tsconfig.json` de '{full_name}' e configure aliases de path (`@/*`) para facilitar refatorações seguras e capturar erros em tempo de compilação."
    if "python" in lang_lower:
        return f"Configure `pyproject.toml` com `ruff` e `pytest` em '{full_name}' para unificar formatação, linting e testes automatizados em uma ferramenta ultrarrápida."
    if "rust" in lang_lower:
        return f"Execute `cargo clippy -- -D warnings` e configure perfis de release com `lto = true` e `codegen-units = 1` no `Cargo.toml` de '{full_name}' para binários enxutos."
    if "go" in lang_lower:
        return f"Utilize `golangci-lint` no pipeline de '{full_name}' e gerencie cancelamento de goroutines com `context.WithTimeout` para evitar vazamentos de memória."
    if "java" in lang_lower or "kotlin" in lang_lower or "jvm" in topics_set:
        return f"Configure flags JVM com `-XX:+UseContainerSupport` e garanta que pools de threads de '{full_name}' respeitem os limites de CPU do container."
    if "c++" in lang_lower or "cpp" in lang_lower or "c" in lang_lower:
        return f"Compile '{full_name}' com sanitizers de memória (`-fsanitize=address,undefined`) em ambiente de desenvolvimento para capturar vazamentos de ponteiros e buffer overflows."
    if "swift" in lang_lower:
        return f"Utilize Swift Concurrency com Actors no projeto '{full_name}' para garantir safety contra condições de corrida em operações assíncronas concorrentes."
    if "php" in lang_lower:
        return f"Habilite OPcache com JIT e utilize `composer install --no-dev --optimize-autoloader` no pipeline de deploy de produção de '{full_name}'."
    if "ruby" in lang_lower:
        return f"Execute `bundle exec rubocop -a` e configure alocador de memória alternativo (como jemalloc) para '{full_name}' para reduzir fragmentação de heap."

    return f"Inspecione a arquitetura modular e a suíte de testes na raiz de '{full_name}' antes de estender funcionalidades, mantendo total retrocompatibilidade."

def analyze_repository(repo_info):
    """Analisa um repositório individualmente usando IA ou fallback contextual."""
    full_name = repo_info.get("full_name", "")
    owner, name = full_name.split("/")
    description = repo_info.get("description") or "Sem descrição fornecida"
    language = repo_info.get("language") or "Docs / Shell"
    topics = ", ".join(repo_info.get("topics") or [])

    print(f"-> Analisando repositório: {full_name}...")
    readme_text = get_repo_readme(owner, name)

    # Detecção de idioma do README para instrução de tradução obrigatória
    readme_lang = _detect_readme_language(readme_text)
    translate_instruction = ""
    if readme_lang == "en":
        translate_instruction = (
            "\n⚠️ ATENÇÃO: O README deste repositório está em INGLÊS. "
            "TODOS os trechos do README, descrição e qualquer conteúdo em inglês "
            "devem ser TRADUZIDOS para Português do Brasil antes de compor a análise. "
            "NUNCA inclua sentenças ou trechos em inglês na resposta — traduza tudo.\n"
        )
    elif readme_lang == "other":
        translate_instruction = (
            "\n⚠️ ATENÇÃO: O README deste repositório está em outro idioma (não é inglês nem português). "
            "TODOS os trechos do README devem ser TRADUZIDOS para Português do Brasil antes de compor a análise. "
            "NUNCA inclua trechos no idioma original na resposta.\n"
        )

    prompt = f"""Você é um arquiteto de software sênior brasileiro especializado em código aberto.
Analise detalhadamente o repositório do GitHub '{full_name}' (Linguagem principal: {language}).

Descrição oficial: {description}
Tópicos/Tags: {topics}
Trecho do README:
{readme_text[:4000]}
{translate_instruction}
Gere EXATAMENTE a estrutura abaixo em Português do Brasil (pt-BR) com alto nível técnico e sem superficialidades:

- 🎯 **O que é e para que serve:** (Explique com precisão técnica em 2 a 3 frases o propósito real da ferramenta, sua arquitetura e seu principal diferencial competitivo em português)
- 💡 **Casos de uso reais no dia a dia:** (Apresente 2 a 3 cenários práticos e objetivos de aplicação em projetos reais de engenharia de software, dados, segurança ou infraestrutura em português)
- 🚀 **Como usar na prática com comandos prontos:**
```bash
(Forneça comandos exatos, funcionais e corretos de instalação e execução rápida em Docker, pip, npm, cargo, go ou clone)
```
- ⚡ **Dica Pro de produtividade:** (Forneça uma dica técnica única, avançada e exclusiva para '{name}', citando flags reais de CLI, parâmetros de configuração, variáveis de ambiente ou decisões arquiteturais. NUNCA use frases genéricas como 'leia a documentação' ou 'consulte o readme')

REGRAS OBRIGATÓRIAS:
1. Responda 100% em Português do Brasil (pt-BR). É expressamente proibido responder em inglês ou misturar sentenças em inglês.
2. Seja profundo, específico para '{name}' e técnico.
3. Não use dicas genéricas ou de preenchimento."""

    # 1. Tentar Gemini
    res = call_gemini(prompt)
    if res:
        return res

    # 2. Tentar DeepSeek
    res = call_deepseek(prompt)
    if res:
        return res

    # 3. Tentar TokenRouter
    res = call_tokenrouter(prompt)
    if res:
        return res

    # 4. Tentar OpenAI
    res = call_openai(prompt)
    if res:
        return res

    # 5. Tentar OpenRouter
    res = call_openrouter(prompt)
    if res:
        return res

    # 6. Fallback contextual dinâmico inteligente
    print("  → Usando analisador contextual dinâmico baseado no README")
    return generate_smart_dynamic_analysis(repo_info, readme_text)

# ==============================================================================
# CONSTRUÇÃO DO CATÁLOGO MARKDOWN
# ==============================================================================

def rebuild_catalog_markdown(all_stars, master_db):
    """Reconstrói o arquivo CATALOGO_ESTRELAS.md determinística e perfeitamente.
    Função pura de renderização sem efeitos colaterais de I/O na base de dados.
    """
    total = len(all_stars)
    doc = []

    # 1. CABEÇALHO OFICIAL
    doc.append("# 🌟 Dossiê Completo: Análise Minuciosa das Estrelas do GitHub")
    doc.append("")
    doc.append(f"> **Perfil:** [@{GITHUB_USERNAME}](https://github.com/{GITHUB_USERNAME}) (Matheus Salustiano)")
    doc.append(f"> **Total de Repositórios Analisados:** {total}")
    doc.append("> **Estrutura Obrigatória por Item:**")
    doc.append("> 🛡️ *Segurança & Malware (ScanRepo)* | 🎯 *O que é e para que serve* | 💡 *Casos de uso reais no dia a dia* | 🚀 *Como usar na prática* | ⚡ *Dica Pro de produtividade*")
    doc.append("")
    doc.append("---")
    doc.append("")

    # 2. SUMÁRIO COMPLETO SEMPRE NO TOPO (100% dos repositórios)
    doc.append("## 📑 Sumário Completo dos Repositórios")
    doc.append("")
    for i, r in enumerate(all_stars, 1):
        name = r["full_name"]
        anchor = re.sub(r"[^a-z0-9]", "", name.lower())
        stars = r.get("stargazers_count", 0)
        lang = r.get("language") or "Docs / Shell"
        doc.append(f"{i:02d}. [{name}](#{anchor}) — ⭐ {stars:,} (`{lang}`)")
    doc.append("")
    doc.append("---")
    doc.append("")

    # 3. ANÁLISE DETALHADA REPOSITÓRIO POR REPOSITÓRIO
    doc.append("## 🔍 Análise Detalhada Repositório por Repositório")
    doc.append("")

    for i, r in enumerate(all_stars, 1):
        name = r["full_name"]
        url = r.get("html_url") or f"https://github.com/{name}"
        stars = r.get("stargazers_count", 0)
        lang = r.get("language") or "Docs / Shell"
        anchor = re.sub(r"[^a-z0-9]", "", name.lower())

        info = master_db.get(name, {})
        security_badge = scan_repository_security(r)

        doc.append(f"<a id=\"{anchor}\"></a>")
        doc.append(f"### {i:02d}. [{name}]({url})")
        doc.append(f"- **⭐ Stars:** {stars:,} | **💻 Linguagem:** `{lang}`")
        doc.append(f"- 🛡️ **Segurança & Malware:** {security_badge}")
        doc.append(f"- 🎯 **O que é e para que serve:** {info.get('what', '')}")
        doc.append(f"- 💡 **Casos de uso reais no dia a dia:** {info.get('use_cases', '')}")
        doc.append(f"- 🚀 **Como usar na prática com comandos prontos:**")
        quickstart_default = "```bash\n# Consulte as instrucoes no README\n```"
        doc.append(f"{info.get('quickstart', quickstart_default)}")
        doc.append(f"- ⚡ **Dica Pro de produtividade:** {info.get('pro_tip', '')}")
        doc.append("")
        doc.append("---")
        doc.append("")

    return "\n".join(doc)

# ==============================================================================
# FLUXO PRINCIPAL DE EXECUÇÃO
# ==============================================================================

def main():
    print(f"Iniciando verificação e sincronização de estrelas para: {GITHUB_USERNAME}")
    if FORCE_RE_SCAN:
        print("  -> Modo FORCE_RE_SCAN ativo: reanalisando todos os repositórios.")

    os.makedirs(DATA_DIR, exist_ok=True)

    # 1. Carregar base de dados master existente
    master_db = {}
    if os.path.exists(MASTER_DB_FILE):
        with open(MASTER_DB_FILE, "r", encoding="utf-8") as f:
            master_db = json.load(f)

    # 2. Carregar estado de processamento
    if os.path.exists(PROCESSED_FILE):
        with open(PROCESSED_FILE, "r", encoding="utf-8") as f:
            processed_data = json.load(f)
    else:
        processed_data = {"processed_ids": []}

    processed_ids = set(processed_data.get("processed_ids", []))

    # 3. Buscar favoritos da API do GitHub com paginação
    all_stars = []
    page = 1
    api_success = True
    while True:
        url = f"https://api.github.com/users/{GITHUB_USERNAME}/starred?per_page=100&page={page}"
        items = github_request(url)
        if items is None:
            api_success = False
            break
        if not items:
            break
        for it in items:
            repo = it.get("repo", it)
            all_stars.append(repo)
        if len(items) < 100:
            break
        page += 1

    # Se a API falhou e temos cache local, usar cache para garantir estabilidade
    if (not api_success or len(all_stars) == 0) and os.path.exists(ALL_STARS_FILE):
        print("Aviso: Utilizando cache local de estrelas (all_starred_github.json) devido a indisponibilidade ou rate limit da API.")
        with open(ALL_STARS_FILE, "r", encoding="utf-8") as f:
            all_stars = json.load(f)

    total_current = len(all_stars)
    print(f"Total de favoritos carregados: {total_current}")

    if total_current == 0:
        print("Erro: Nenhum repositório disponível para processamento.")
        return

    # Sincronização e Poda de Órfãos (Garantir 100% de paridade com os favoritos ativos)
    active_repo_names = {r["full_name"] for r in all_stars}
    active_repo_ids = {r["id"] for r in all_stars if "id" in r}

    pruned_db_count = len(master_db) - len(active_repo_names.intersection(master_db.keys()))
    if pruned_db_count > 0:
        print(f"Poda de consistência: removendo {pruned_db_count} registros órfãos que não estão mais favoritados.")
        master_db = {k: v for k, v in master_db.items() if k in active_repo_names}
        processed_ids = {pid for pid in processed_ids if pid in active_repo_ids}

    # Salvar cópia atualizada da lista de repositórios
    with open(ALL_STARS_FILE, "w", encoding="utf-8") as f:
        json.dump(all_stars, f, indent=2, ensure_ascii=False)

    # 4. Detectar Dicas Pro duplicadas para reanálise
    duplicate_tips = check_duplicate_tips(master_db) if not FORCE_RE_SCAN else set()

    # 5. Processar todos os repositórios: novos e reanálise de análises estagnadas
    #    SEMPRE reanalisamos para garantir que o catálogo esteja em dia —
    #    conhecimento base serve como fallback, mas IA tem prioridade.
    new_found = 0
    skipped = 0

    for repo in all_stars:
        repo_name = repo.get("full_name")
        repo_id = repo.get("id")

        if repo_name not in master_db or repo_id not in processed_ids or _is_analysis_stale(
            master_db.get(repo_name, {}), repo, duplicate_tips=duplicate_tips
        ):
            analysis = analyze_repository(repo)
            master_db[repo_name] = analysis
            if repo_id:
                processed_ids.add(repo_id)
            new_found += 1
        else:
            existing = master_db.get(repo_name, {})
            print(f"  → Mantendo análise válida de {repo_name} (sem mudanças detectadas)")
            skipped += 1

    print(f"Novos repositórios analisados nesta rodada: {new_found}")
    print(f"Repositórios com análise válida mantida: {skipped}")

    # 6. Salvar bases de dados atualizadas
    with open(MASTER_DB_FILE, "w", encoding="utf-8") as f:
        json.dump(master_db, f, indent=2, ensure_ascii=False)

    with open(CATALOG_DB_FILE, "w", encoding="utf-8") as f:
        json.dump(master_db, f, indent=2, ensure_ascii=False)

    # 7. Salvar estado de IDs processados
    processed_data["processed_ids"] = list(processed_ids)
    processed_data["total"] = total_current
    processed_data["last_updated"] = datetime.now(timezone.utc).isoformat()
    with open(PROCESSED_FILE, "w", encoding="utf-8") as f:
        json.dump(processed_data, f, indent=2, ensure_ascii=False)

    # 8. Reconstruir o CATALOGO_ESTRELAS.md determinístico
    catalog_markdown = rebuild_catalog_markdown(all_stars, master_db)
    with open(CATALOG_FILE, "w", encoding="utf-8") as f:
        f.write(catalog_markdown)

    # 9. Espelhar de forma segura nos caminhos locais se existirem
    mirror_paths = [
        r"C:\Users\Bktech\.gemini\antigravity\scratch\ANALISE_COMPLETA_ESTRELAS_GITHUB.md",
        r"C:\Users\Bktech\.gemini\antigravity\scratch\github-star-automation\CATALOGO_ESTRELAS.md",
        r"C:\Users\Bktech\OneDrive\Projetos_Trabalho\documentos\4_Documentacoes_Tecnicas_e_Projetos\ANALISE_COMPLETA_ESTRELAS_GITHUB.md",
        r"C:\Users\Bktech\OneDrive\Projetos_Trabalho\favorite_repositories\CATALOGO_ESTRELAS.md",
    ]
    for mp in mirror_paths:
        try:
            if os.path.exists(os.path.dirname(mp)):
                with open(mp, "w", encoding="utf-8") as f:
                    f.write(catalog_markdown)
        except Exception:
            pass

    print(f"Processo concluído com sucesso! Catálogo atualizado com {total_current} repositórios.")

if __name__ == "__main__":
    main()
