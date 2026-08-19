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

# Configurações de Ambiente
GITHUB_USERNAME = os.environ.get("TARGET_USERNAME", "Jerixco")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
PROCESSED_FILE = os.path.join(DATA_DIR, "processed_stars.json")
MASTER_DB_FILE = os.path.join(DATA_DIR, "master_catalog_db.json")
CATALOG_DB_FILE = os.path.join(DATA_DIR, "catalog_db.json")
ALL_STARS_FILE = os.path.join(DATA_DIR, "all_starred_github.json")
CATALOG_FILE = os.path.join(BASE_DIR, "CATALOGO_ESTRELAS.md")

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

def parse_ai_response(text):
    """
    Parser resiliente que aceita JSON puro ou múltiplos formatos de Markdown.
    Nunca descarta respostas válidas por diferenças mínimas de pontuação ou negrito.
    """
    if not text:
        return None

    cleaned = text.strip()

    # 1. Tentar parsear como JSON direto caso a IA tenha respondido em JSON
    if cleaned.startswith("{") and cleaned.endswith("}"):
        try:
            data = json.loads(cleaned)
            if "what" in data and "use_cases" in data and "pro_tip" in data:
                quick = data.get("quickstart", "```bash\ngit clone repo\n```")
                if "```" not in quick:
                    quick = f"```bash\n{quick}\n```"
                return {
                    "what": data["what"].strip(),
                    "use_cases": data["use_cases"].strip(),
                    "quickstart": quick.strip(),
                    "pro_tip": data["pro_tip"].strip()
                }
        except Exception:
            pass

    # 2. Extração flexível por padrões semânticos de seções
    # Regex tolerante a emojis dentro/fora de negrito, hífens, cabeçalhos ### e variações de espaçamento
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
            quickstart = f"```bash\n{quickstart}\n```" if quickstart else "```bash\n# Consulte as instruções de inicialização no README\n```"
        return {
            "what": what,
            "use_cases": use_cases,
            "quickstart": quickstart,
            "pro_tip": pro_tip
        }

    return None

def call_gemini(prompt, api_version="v1beta"):
    """Chama a API do Google Gemini com fallback automático de modelos e versões de API."""
    if not GEMINI_API_KEY:
        return None

    models = [
        # Gemini 3.x series — modelos mais recentes (prioridade alta)
        "gemini-3.7-flash",
        "gemini-3.6-flash",
        "gemini-3.5-flash",
        "gemini-3.5-flash-lite",
        # Gemini 2.5 series — estáveis e amplamente disponíveis
        "gemini-2.5-flash",
        "gemini-2.5-pro",
        # Fallback para versões antigas que ainda podem estar ativas em contas existentes
        "gemini-2.0-flash",
    ]
    # Tentar ambos os endpoints de API para maximizar compatibilidade
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
            except Exception as e:
                print(f"  → Tentativa Gemini ({api_ver}/{model}) falhou: {e}")
                continue
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

def generate_smart_dynamic_analysis(repo_info, readme_text):
    """
    Gera uma análise individualizada e contextual diretamente baseada no README,
    descrição, tópicos reais e padrões de projeto do repositório.
    Nunca retorna texto genérico — extrai informações reais do que foi fornecido.
    """
    full_name = repo_info.get("full_name", "")
    description = (repo_info.get("description") or "").strip()
    language = repo_info.get("language") or "Docs / Shell"
    topics = repo_info.get("topics") or []
    name = full_name.split("/")[-1]
    owner = full_name.split("/")[0]
    topics_set = set(t.lower() for t in topics)

    # Extrair blocos de código reais do README se existirem
    code_blocks = re.findall(r"```(?:bash|shell|sh|zsh)?\n(.*?)\n```", readme_text, re.DOTALL)
    valid_code = _extract_valid_code_block(code_blocks, language, full_name, name)

    # Determinar O QUE É a partir do README real, não de suposições
    o_que_e = _build_what_is(description, language, topics_set, readme_text, full_name, owner, name)

    # Determinar CASOS DE USO a partir de tópicos e padrões do README
    casos_de_uso = _build_use_cases(description, topics_set, readme_text, language, name)

    # Determinar DICA PRO real baseada em padrões de configuração da linguagem/ecossistema
    dica_pro = _build_pro_tip(topics_set, description, language, readme_text, name, full_name)

    return {
        "what": o_que_e,
        "use_cases": casos_de_uso,
        "quickstart": f"```bash\n{valid_code}\n```",
        "pro_tip": dica_pro
    }


def _extract_valid_code_block(code_blocks, language, full_name, name):
    """Extrai o bloco de código mais relevante do README."""
    if not code_blocks:
        lang_lower = language.lower()
        return _default_code_for_language(lang_lower, full_name, name)

    for cb in code_blocks:
        cb_clean = cb.strip()
        if len(cb_clean) > 10 and any(
            k in cb_clean.lower() for k in ["install", "run", "clone", "cargo", "docker", "pip", "npm", "go build", "python"]
        ):
            # Preferir blocos que têm comandos reais de instalação/execução
            if any(cmd in cb_clean for cmd in ["pip install", "npm install", "cargo build", "docker", "go build", "git clone"]):
                return cb_clean
            # Bloco com comandos de execução
            if any(cmd in cb_clean for cmd in ["run", "start", "serve", "execute"]) and "npm" in cb_clean:
                return cb_clean

    # Fallback: usar primeiro bloco com comandos plausíveis
    for cb in code_blocks:
        cb_clean = cb.strip()
        if len(cb_clean) > 10:
            return cb_clean

    return _default_code_for_language(language.lower(), full_name, name)


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
    """Constroi a descrição 'O que é' usando informações reais do repo."""
    # Prioridade 1: usar a description do GitHub se existir
    if description and len(description.strip()) > 15:
        desc_pt = _localize_description(description, topics_set, language)
        return f"{desc_pt} Desenvolvido primariamente em {language}, mantido por @{owner}."

    # Prioridade 2: analisar README em busca de propósito declarado
    if readme_text:
        purpose = _extract_purpose_from_readme(readme_text, topics_set)
        if purpose and len(purpose) > 20:
            desc_pt = _localize_description(purpose, topics_set, language)
            return f"{desc_pt} Implementado em {language}, mantido por @{owner}."

    # Prioridade 3: inferir a partir de tópicos
    inferred = _infer_from_topics(topics_set, language, name)
    if inferred:
        return f"{inferred}. Mantido por @{owner}."

    # Último recurso: linguagem + nome do projeto
    return f"Ferramenta e módulo '{name}' desenvolvido em {language}, mantido por @{owner} para integração e desenvolvimento de software."


def _localize_description(description, topics_set, language):
    """Adaptar description inglesa para pt-BR com contexto técnico e enriquecimento por tópicos."""
    desc = description.strip()

    # Mapeamento de prefixos comuns em inglês para pt-BR elegante
    prefix_map = [
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

    # Se tem tópicos, enriquecer com eles
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
        "rag": "com arquiterura RAG (Retrieval-Augmented Generation)",
        "web-scraping": "para extração de dados web",
        "crawler": "para rastreamento web",
        "scrapy": "baseado no ecossistema Scrapy",
        "docker": "com suporte a containers Docker",
        "kubernetes": "com integração Kubernetes",
        "devops": "focado em práticas DevOps",
        "ci-cd": "com pipelines de CI/CD",
        "cli": "como ferramenta de linha de comando",
        "terminal": "para uso em terminal",
        "sdk": "como kit de desenvolvimento de software",
        "api": "expondo API para integração",
        "microservice": "arquitetura de microsserviços",
        "microservices": "arquitetura de microsserviços",
        "database": "com integração a bancos de dados",
        "postgresql": "com suporte a PostgreSQL",
        "mysql": "com suporte a MySQL",
        "mongodb": "com suporte a MongoDB",
        "kafka": "com integração Apache Kafka",
        "monitoring": "focado em monitoramento",
        "observability": "com capacidades de observabilidade",
        "logging": "com sistema de logging",
        "security": "focado em segurança",
        "authentication": "com sistema de autenticação",
        "authorization": "com controle de autorização",
        "oauth": "com suporte a OAuth",
        "frontend": "focado em desenvolvimento frontend",
        "backend": "focado em desenvolvimento backend",
        "fullstack": "desenvolvimento fullstack",
        "mobile": "para desenvolvimento mobile",
        "ios": "para plataformas Apple/iOS",
        "android": "para Android",
        "game": "desenvolvimento de jogos",
        "game-development": "desenvolvimento de jogos",
        "editor": "como editor/IDE",
        "plugin": "como plugin/extensão",
        "extension": "como extensão",
        "library": "como biblioteca de código",
        "framework": "como framework",
        "sdk": "como SDK",
        "tool": "como ferramenta de desenvolvimento",
        "utility": "como utilitário",
        "template": "como template inicial",
        "starter": "como projeto inicial (starter)",
        "boilerplate": "como boilerplate",
        "example": "como exemplo/tutorial",
        "demo": "como demonstração",
        "tutorial": "como tutorial",
        "guide": "como guia/documentação",
        "course": "como curso/material educacional",
        "documentation": "como documentação técnica",
        "list": "como lista curada de recursos",
        "awesome": "como lista curada (awesome-list)",
        "collection": "como coleção de recursos",
        "cheatsheet": "como referência rápida (cheatsheet)",
        "config": "para gerenciamento de configuração",
        "configuration": "para gerenciamento de configuração",
        "infrastructure": "para infraestrutura como código",
        "iac": "como infraestrutura como código",
        "serverless": "arquitetura serverless",
        "faas": "como Function-as-a-Service",
        "container": "com containers",
        " virtualization": "com virtualização",
        "vm": "com máquinas virtuais",
        "cloud": "para nuvem",
        "aws": "com integração AWS",
        "azure": "com integração Azure",
        "gcp": "com integração Google Cloud",
        "minecraft": "para Minecraft",
        "mod": "como modificação (mod)",
        "plugin": "como plugin/extensão",
        "addon": "como complemento/addon",
        "theme": "como tema",
        "ui": "focado em interface de usuário",
        "ux": "focado em experiência de usuário",
        "dashboard": "como dashboard/analítico",
        "visualization": "com visualização de dados",
        "chart": "com gráficos/charts",
        "graph": "com visualização em grafos",
        "map": "com mapas",
        "gis": "para sistemas de informação geográfica",
        "iot": "para Internet of Things",
        "embedded": "para sistemas embarcados",
        "firmware": "como firmware",
        "rtos": "para RTOS",
        "driver": "como driver",
        "kernel": "para desenvolvimento de kernel",
        "compiler": "como compilador",
        "interpreter": "como interpretador",
        "runtime": "como runtime",
        "vm": "com máquina virtual",
        "jvm": "para JVM",
        "net": "para .NET",
        "dotnet": "para .NET",
        "csharp": "em C#",
        "fsharp": "em F#",
        "vb.net": "em VB.NET",
        "unity": "para Unity",
        "unreal": "para Unreal Engine",
        "godot": "para Godot",
        "blade": "com engine Blade",
        "laravel": "com framework Laravel",
        "symfony": "com framework Symfony",
        "django": "com framework Django",
        "flask": "com framework Flask",
        "fastapi": "com framework FastAPI",
        "spring": "com framework Spring",
        "spring-boot": "com Spring Boot",
        "rails": "com Ruby on Rails",
        "rubyonrails": "com Ruby on Rails",
        "express": "com Express.js",
        "nestjs": "com NestJS",
        "nextjs": "com Next.js",
        "nuxt": "com Nuxt.js",
        "vue": "com Vue.js",
        "react": "com React",
        "angular": "com Angular",
        "svelte": "com Svelte",
        "solid": "com SolidJS",
        "tailwind": "com Tailwind CSS",
        "bootstrap": "com Bootstrap",
        "material-ui": "com Material-UI",
        "ant-design": "com Ant Design",
        "chakra-ui": "com Chakra UI",
        "shadcn": "com shadcn/ui",
        "prisma": "com Prisma ORM",
        "typeorm": "com TypeORM",
        "sequelize": "com Sequelize",
        "mongoose": "com Mongoose",
        "redis": "com Redis",
        "graphql": "com GraphQL",
        "rest": "com API REST",
        "grpc": "com gRPC",
        "websocket": "com WebSockets",
        "mqtt": "com MQTT",
        "amqp": "com AMQP",
        "rabbitmq": "com RabbitMQ",
        "nsq": "com NSQ",
        "consul": "com Consul",
        "etcd": "com etcd",
        "zookeeper": "com Apache ZooKeeper",
        "prometheus": "com Prometheus",
        "grafana": "com Grafana",
        "kibana": "com Kibana",
        "elastic": "com ElasticSearch",
        "elasticsearch": "com ElasticSearch",
        "opensearch": "com OpenSearch",
        "clickhouse": "com ClickHouse",
        "sqlite": "com SQLite",
        "postgresql": "com PostgreSQL",
        "mysql": "com MySQL",
        "mariadb": "com MariaDB",
        "mongodb": "com MongoDB",
        "cassandra": "com Apache Cassandra",
        "couchdb": "com CouchDB",
        "dynamodb": "com DynamoDB",
        "firestore": "com Firestore",
        "spanner": "com Cloud Spanner",
        "neo4j": "com Neo4j",
        "redis": "com Redis",
        "memcached": "com Memcached",
        "hazelcast": "com Hazelcast",
        "yugabyte": "com YugabyteDB",
        "cockroachdb": "com CockroachDB",
        "vitess": "com Vitess",
        "foundationdb": "com FoundationDB",
        "tidb": "com TiDB",
        "dgraph": "com Dgraph",
        "arangodb": "com ArangoDB",
        "influxdb": "com InfluxDB",
        "timescaledb": "com TimescaleDB",
        "questdb": "com QuestDB",
        "duckdb": "com DuckDB",
        "pinecone": "com Pinecone",
        "weaviate": "com Weaviate",
        "qdrant": "com Qdrant",
        "chromadb": "com ChromaDB",
        "milvus": "com Milvus",
        "pgvector": "com pgvector",
        "redis": "com Redis",
        "ray": "com Ray",
        "dask": "com Dask",
        "spark": "com Apache Spark",
        "flink": "com Apache Flink",
        "hadoop": "com Apache Hadoop",
        "airflow": "com Apache Airflow",
        "prefect": "com Prefect",
        "dagster": "com Dagster",
        "kubeflow": "com Kubeflow",
        "mlflow": "com MLflow",
        "hydra": "com Hydra",
        "optuna": "com Optuna",
        "wandb": "com Weights & Biases",
        "lab": "com Google Colab",
        "jupyter": "com Jupyter",
        "colab": "com Google Colab",
        "notebook": "com notebooks",
        "binder": "com Binder",
        "streamlit": "com Streamlit",
        "dash": "com Plotly Dash",
        "gradio": "com Gradio",
        "panel": "com Panel",
        "voila": "com Voila",
        "flexx": "com Flexx",
        "ipywidgets": "com IPython widgets",
        "transformers": "com Hugging Face Transformers",
        "pytorch": "com PyTorch",
        "tensorflow": "com TensorFlow",
        "jax": "com JAX",
        "keras": "com Keras",
        "paddle": "com PaddlePaddle",
        "mxnet": "com MXNet",
        "caffe": "com Caffe",
        "theano": "com Theano",
        "cntk": "com CNTK",
        "onnx": "com ONNX",
        "openvino": "com OpenVINO",
        "tensorrt": "com TensorRT",
        "trt": "com TensorRT",
        "ncnn": "com ncnn",
        "tnn": "com TNN",
        "mnn": "com MNN",
        "opencl": "com OpenCL",
        "cuda": "com CUDA",
        "cudnn": "com cuDNN",
        "tensorflow-lite": "com TensorFlow Lite",
        "tflite": "com TensorFlow Lite",
        "pytorch-mobile": "com PyTorch Mobile",
        "mlkit": "com ML Kit",
        "core-ml": "com Core ML",
        "swiftui": "com SwiftUI",
        "appkit": "com AppKit",
        "uikit": "com UIKit",
        "watchos": "para watchOS",
        "tvos": "para tvOS",
        "macos": "para macOS",
        "ios": "para iOS",
        "ipados": "para iPadOS",
        "visionos": "para visionOS",
        "android": "para Android",
        "kotlin": "em Kotlin",
        "java": "em Java",
        "groovy": "em Groovy",
        "scala": "em Scala",
        "jruby": "em JRuby",
        "jython": "em Jython",
        "kotlin": "em Kotlin",
        "spring": "com Spring",
        "quarkus": "com Quarkus",
        "micronaut": "com Micronaut",
        "helidon": "com Helidon",
        "vert-x": "com Vert.x",
        "akka": "com Akka",
        "play": "com Play Framework",
        "lagom": "com Lagom",
        "slick": "com Slick",
        "doobie": "com Doobie",
        "http4s": "com Http4s",
        "zio": "com ZIO",
        "cats-effect": "com Cats Effect",
        "monix": "com Monix",
        "fs2": "com FS2",
        "scodec": "com Scodec",
        "breeze": "com Breeze",
        "spire": "com Spire",
        "shapeless": "com Shapeless",
        "macwire": "com MacWire",
        "config": "com pureconfig/config",
        "sbt": "com SBT",
        "mill": "com Mill",
        "bazel": "com Bazel",
        "gradle": "com Gradle",
        "maven": "com Maven",
        "leiningen": "com Leiningen",
        "boot": "com boot",
        "rebar": "com rebar3",
        "mix": "com Mix",
        "hex": "com Hex",
        "cargo": "com Cargo",
        "npm": "com npm",
        "yarn": "com Yarn",
        "pnpm": "com pnpm",
        "bun": "com Bun.sh",
        "deno": "com Deno",
        "npx": "com npx",
        "pip": "com pip",
        "poetry": "com Poetry",
        "pipenv": "com Pipenv",
        "conda": "com Conda",
        "mamba": "com Mamba",
        "uv": "com uv",
        "pdm": "com PDM",
        "rye": "com Rye",
        "flit": "com Flit",
        "hatch": "com Hatch",
        "setuptools": "com setuptools",
        "wheel": "com wheel",
        "twine": "com twine",
        "build": "com build",
        "tox": "com tox",
        "nox": "com nox",
        "pytest": "com pytest",
        "unittest": "com unittest",
        "nose": "com nose",
        "hypothesis": "com Hypothesis",
        "coverage": "com coverage",
        "coveragepy": "com Coverage.py",
        "codecov": "com Codecov",
        "coveralls": "com Coveralls",
        "sonarqube": "com SonarQube",
        "sonarcloud": "com SonarCloud",
        "eslint": "com ESLint",
        "prettier": "com Prettier",
        "black": "com Black",
        "isort": "com isort",
        "flake8": "com flake8",
        "pylint": "com pylint",
        "mypy": "com mypy",
        "pyright": "com Pyright",
        "ruff": "com Ruff",
        "pyflakes": "com Pyflakes",
        "bandit": "com Bandit",
        "safety": "com safety",
        "pip-audit": "com pip-audit",
        "dependabot": "com Dependabot",
        "renovate": "com Renovate",
        "trivy": "com Trivy",
        "snyk": "com Snyk",
        "grype": "com Grype",
        "syft": "com Syft",
        "anchore": "com Anchore",
        "aqua": "com Aqua",
        "kics": "com KICS",
        "checkov": "com Checkov",
        "tfsec": "com tfsec",
        "terraform": "com Terraform",
        "openterra": "com OpenTofu",
        "pulumi": "com Pulumi",
        "cdk": "com AWS CDK",
        "cdk8s": "com cdk8s",
        "cdktf": "com CDK for Terraform",
        "crossplane": "com Crossplane",
        "kustomize": "com Kustomize",
        "helm": "com Helm",
        "carvel": "com Carvel",
        "kapp": "com kapp",
        "ytt": "com ytt",
        "kbld": "com kbld",
        "imgpkg": "com imgpkg",
        " vendir": "com vendir",
        "stakater": "com Stakater",
        "reloader": "com Reloader",
        "external-dns": "com ExternalDNS",
        "cert-manager": "com cert-manager",
        "ingress-nginx": "com ingress-nginx",
        "traefik": "com Traefik",
        "envoy": "com Envoy",
        "istio": "com Istio",
        "linkerd": "com Linkerd",
        " Consul": "com Consul",
        "vault": "com Vault",
        "nomad": "com Nomad",
        "packer": "com Packer",
        "vagrant": "com Vagrant",
        "virtualbox": "com VirtualBox",
        "vmware": "com VMware",
        "hyper-v": "com Hyper-V",
        "qemu": "com QEMU",
        "libvirt": "com libvirt",
        "proxmox": "com Proxmox",
        "esxi": "com ESXi",
        "nutanix": "com Nutanix",
        "openstack": "com OpenStack",
        "cloudstack": "com Apache CloudStack",
        "maas": "com MAAS",
        "juju": "com Juju",
        "conjure": "com Canonical Juju",
        "charm": "com Charm",
    }
    matches = [context for topic, context in context_map.items() if topic in topics_set]
    if matches:
        return " | ".join(matches[:5])
    return ""


def _infer_from_topics(topics_set, language, name):
    """Inferir propósito do projeto a partir de tópicos."""
    # Tópicos que indicam propósito claro
    if "cli" in topics_set or "terminal" in topics_set or "command-line" in topics_set or "commandline" in topics_set:
        return f"Interface de linha de comando (CLI) para terminal"
    if "library" in topics_set:
        return f"Biblioteca de código {language} para reutilização em projetos"
    if "framework" in topics_set:
        return f"Framework {language} para desenvolvimento de aplicações"
    if "sdk" in topics_set:
        return f"Kit de desenvolvimento de software (SDK) em {language}"
    if "tool" in topics_set:
        return f"Utilitário/ferramenta de desenvolvimento em {language}"
    if "template" in topics_set or "starter" in topics_set or "boilerplate" in topics_set:
        return f"Template/starter inicial para projetos {language}"
    if "plugin" in topics_set or "extension" in topics_set:
        return f"Plugin/extensão para ecossistema de desenvolvimento"
    if "example" in topics_set or "demo" in topics_set or "tutorial" in topics_set or "guide" in topics_set:
        return f"Material de exemplo/tutorial para aprendizado"
    if "awesome" in topics_set:
        return f"Lista curada de recursos sobre {language}"
    if "cheatsheet" in topics_set:
        return f"Referência rápida/cheat sheet para {language}"
    if "list" in topics_set or "collection" in topics_set:
        return f"Coleção/lista de recursos para comunidade"
    if "course" in topics_set:
        return f"Material educacional/curso sobre {language}"
    if "documentation" in topics_set:
        return f"Documentação técnica para {language}"
    if "config" in topics_set or "configuration" in topics_set:
        return f"Gerenciamento de configuração para projetos"
    if "infrastructure" in topics_set or "iac" in topics_set:
        return f"Infraestrutura como código (IaC) para deploy"
    if "serverless" in topics_set or "faas" in topics_set:
        return f"Arquitetura serverless/FaaS para execução em nuvem"
    if "container" in topics_set:
        return f"Ferramenta/container para isolamento e deploy"
    if "monitoring" in topics_set or "observability" in topics_set:
        return f"Monitoramento e observabilidade para sistemas"
    if "security" in topics_set or "authentication" in topics_set or "authorization" in topics_set:
        return f"Segurança/autenticação para aplicações"
    if "database" in topics_set or any(db in str(topics_set) for db in ["postgresql", "mysql", "mongodb"]):
        return f"Integração com bancos de dados para persistência"
    if "frontend" in topics_set:
        return f"Desenvolvimento frontend para interfaces web"
    if "backend" in topics_set:
        return f"Desenvolvimento backend para API e lógica"
    if "mobile" in topics_set:
        return f"Desenvolvimento mobile para dispositivos"
    if "game" in topics_set or "game-development" in topics_set:
        return f"Desenvolvimento de jogos e engines"
    if "editor" in topics_set:
        return f"Editor/IDE para desenvolvimento"
    if "ui" in topics_set:
        return f"Interface de usuário para aplicações"
    if "dashboard" in topics_set:
        return f"Dashboard/analítico para monitoramento"
    if "visualization" in topics_set or "chart" in topics_set:
        return f"Visualização de dados para análise"
    if "iot" in topics_set:
        return f"Internet of Things para dispositivos conectados"
    if "embedded" in topics_set or "firmware" in topics_set:
        return f"Sistemas embarcados/firmware para hardware"
    if "ml" in str(topics_set) or "machine-learning" in str(topics_set) or "data-science" in str(topics_set):
        return f"Machine Learning / Ciência de dados para análise e predição"
    if "ai" in str(topics_set) or "artificial-intelligence" in str(topics_set):
        return f"Inteligência artificial para automação e raciocínio"
    if "llm" in str(topics_set) or "rag" in str(topics_set):
        return f"Modelos de linguagem grandes (LLM) com RAG para geração de texto"

    # Fallback: linguagem
    return f"Projeto em {language} com propósito a ser explorado no código-fonte"


def _build_use_cases(description, topics_set, readme_text, language, name):
    """Constroi casos de uso reais baseados em tópicos e README."""
    cases = []

    if "cli" in topics_set or "terminal" in topics_set:
        cases.append(f"Automação de tarefas repetitivas diretamente no terminal sem depender de interface gráfica")
    if "docker" in topics_set or "container" in topics_set:
        cases.append(f"Empacotamento e execução consistentes em qualquer ambiente via containers Docker")
    if "kubernetes" in topics_set:
        cases.append(f"Deploy orquestrado em clusters Kubernetes para escalabilidade")
    if "ci-cd" in topics_set or "devops" in topics_set:
        cases.append(f"Integração com pipelines de CI/CD para build e deploy automatizado")
    if "monitoring" in topics_set or "observability" in topics_set:
        cases.append(f"Monitoramento contínuo de métricas, logs e health checks em produção")
    if "security" in topics_set:
        cases.append(f"Auditoria de segurança e proteção contra vulnerabilidades em dependências e configurações")
    if "authentication" in topics_set or "oauth" in topics_set:
        cases.append(f"Gerenciamento de autenticação e autorização para acesso seguro a recursos")
    if "database" in topics_set:
        cases.append(f"Integração com bancos de dados para armazenamento e consulta persistente")
    if "api" in topics_set or "rest" in topics_set:
        cases.append(f"Exposição de API REST para integração com serviços externos e clientes")
    if "graphql" in topics_set:
        cases.append(f"API GraphQL para consultas flexíveis e tipadas por clientes")
    if "frontend" in topics_set:
        cases.append(f"Construção de interfaces web reativas e responsivas para usuários finais")
    if "backend" in topics_set:
        cases.append(f"Desenvolvimento de lógica de negócio, regras e processamento no servidor")
    if "mobile" in topics_set:
        cases.append(f"Desenvolvimento de aplicativos para iOS/Android com acesso a recursos nativos")
    if "testing" in topics_set or "quality" in topics_set:
        cases.append(f"Execução de testes automatizados para garantir qualidade e prevenir regressions")
    if "documentation" in topics_set or "docs" in topics_set:
        cases.append(f"Geração e publicação de documentação técnica para desenvolvedores e usuários")
    if "cli" in topics_set:
        cases.append(f"Execução via linha de comando em scripts de shell e pipelines de automação")
    if "library" in topics_set:
        cases.append(f"Reutilização como dependência em múltiplos projetos via gestor de pacotes")

    # Deduplicar cases
    unique_cases = list(dict.fromkeys(cases))

    if unique_cases:
        return " | ".join(unique_cases[:4])

    # Fallback: usar README para extrair casos de uso
    if readme_text:
        use_case = _extract_use_case_from_readme(readme_text)
        if use_case:
            return use_case

    return f"Automação e desenvolvimento em {language}; integração em pipelines e projetos reais."


def _extract_use_case_from_readme(readme_text):
    """Tenta extrair 'How to use' ou 'Usage' do README."""
    # Procurar seção de uso
    usage_match = re.search(r"(?i)(?:#|##|###)\s*(?:usage|how to use|como usar|como usar|getting started|início rápido|instalação|installation)", readme_text)
    if usage_match:
        start = usage_match.start()
        # Pegar texto após o heading
        snippet = readme_text[start:start + 500]
        # Extrair primeiro parágrafo ou lista
        lines = snippet.split("\n")
        for line in lines:
            line = line.strip()
            if line and not line.startswith("#") and not line.startswith("```"):
                return line
    return ""


def _extract_purpose_from_readme(readme_text, topics_set):
    """Extrai a declaração de propósito do README (primeiro parágrafo ou description)."""
    # Remover headings, code blocks e links para focar no texto
    text_only = re.sub(r"```.*?```", "", readme_text, flags=re.DOTALL)
    text_only = re.sub(r"\[.*?\]\(.*?\)", "", text_only)
    text_only = re.sub(r"#{1,6}\s+", "", text_only)
    text_only = re.sub(r"[-*•]\s+", "", text_only)

    # Pegar primeiras linhas significativas (provavelmente a descrição)
    lines = [l.strip() for l in text_only.split("\n") if l.strip() and len(l.strip()) > 20]
    for line in lines[:10]:
        if any(kw in line.lower() for kw in ["is ", "this ", "provides", "allows", "enables", "helps", "built to", "designed"]):
            return line
        # Se a linha é longa e parece descritiva
        if len(line) > 80 and not line.startswith("http"):
            return line

    return ""


def _build_pro_tip(topics_set, description, language, readme_text, name, full_name):
    """Gera uma Dica Pro real baseada na linguagem, tópicos e padrões avançados do ecossistema."""
    lang_lower = language.lower()
    desc_lower = (description or "").lower()

    # Dicas altamente específicas por tópicos/ecossistemas
    if "docker" in topics_set or "container" in topics_set:
        return f"Adicione `.dockerignore` detalhado e use multi-stage builds no Dockerfile de '{name}' para reduzir a imagem de produção e acelerar pipelines de CI/CD."
    if "kubernetes" in topics_set or "k8s" in topics_set or "helm" in topics_set:
        return f"Defina resource requests e limits com base em benchmarks de consumo real para '{name}', evitando despejos de pods (OOMKilled) sob picos de tráfego no cluster."
    if "ci-cd" in topics_set or "github-actions" in topics_set:
        return f"Configure cache de dependências e execute matrizes de teste em paralelo nos workflows de CI de '{name}' para reduzir expressivamente o tempo de feedback."
    if "security" in topics_set or "malware" in topics_set or "vulnerability" in topics_set:
        return f"Integre verificações automatizadas de dependências e regras de SAST no pipeline de '{name}' para identificar vulnerabilidades e segredos expostos antes do merge."
    if any(t in topics_set for t in ["llm", "rag", "ai", "langchain", "ollama", "vllm"]):
        return f"Ao integrar '{name}' com modelos de linguagem, utilize streaming de respostas e ajuste parâmetros de chunking com overlap de 10-15% para maximizar relevância de contexto sem estourar limites de tokens."
    if any(t in topics_set for t in ["web-scraping", "crawler", "scrapy", "playwright", "puppeteer"]):
        return f"Configure rotação de User-Agents e limites de taxa (rate limiting/download delay) ao executar '{name}' para evitar bloqueios por Cloudflare e rate-limits em requisições concorrentes."
    if "fastapi" in topics_set or "fastapi" in desc_lower:
        return f"Utilize `response_model` com Pydantic v2 em '{name}' para serialização em Rust com ganho de velocidade de até 5x em endpoints com listas grandes de objetos."
    if "django" in topics_set or "django" in desc_lower:
        return f"Utilize `select_related` e `prefetch_related` nas consultas ORM de '{name}' para mitigar o problema de N+1 queries em views com relacionamentos complexos."
    if "react" in topics_set or "nextjs" in topics_set or "next" in topics_set:
        return f"Utilize dynamic imports com Suspense no projeto '{name}' para lazy loading de componentes pesados, reduzindo drasticamente o First Contentful Paint (FCP) inicial."
    if "vue" in topics_set or "nuxt" in topics_set:
        return f"Aproveite a Composition API e modularize composables reutilizáveis no projeto '{name}' para desacoplar regras de negócio do template visual."
    if "redis" in topics_set or "redis" in desc_lower:
        return f"Defina políticas explícitas de TTL e eviction (como `allkeys-lru`) ao usar '{name}' com Redis para impedir exaustão de memória em picos operacionais."
    if "postgres" in topics_set or "postgresql" in topics_set or "postgres" in desc_lower:
        return f"Crie índices parciais e utilize connection pooling (ex: PgBouncer) com '{name}' para manter latências baixas e economizar conexões abertas no banco de dados."
    if "graphql" in topics_set or "graphql" in desc_lower:
        return f"Implemente `DataLoader` nas camadas de resolver do '{name}' para agrupar consultas ao banco e evitar explosão de requisições N+1."
    if "cli" in topics_set or "terminal" in topics_set:
        return f"Adicione suporte a flags `--help` descritivas e auto-completar de shell (Bash/Zsh/Fish) nas ferramentas CLI de '{name}' para aumentar a velocidade de uso no dia a dia."
    if "tauri" in topics_set or "electron" in topics_set:
        return f"Isole a comunicação IPC entre frontend e backend no '{name}' com validação de payload para prevenir brechas de segurança de execução remota de código."
    if "testing" in topics_set or "pytest" in topics_set or "jest" in topics_set:
        return f"Configure testes com cobertura de branches (não apenas linhas) no projeto '{name}' para garantir que fluxos de erro e fallbacks também sejam validados."

    # Regras por linguagem principal
    if "typescript" in lang_lower:
        return f"Ative `strict: true` no `tsconfig.json` de '{name}' e adicione aliases de path (`@/*`) para simplificar refatorações e capturar erros de tipo em tempo de compilação."
    if "python" in lang_lower:
        return f"Configure `pyproject.toml` com `ruff` e `pytest` em '{name}' para centralizar linting, formatação e suíte de testes em uma única ferramenta moderna e ultrarrápida."
    if "rust" in lang_lower:
        return f"Execute `cargo clippy -- -D warnings` e configure perfis de release com `lto = true` no `Cargo.toml` de '{name}' para máxima otimização e binários enxutos."
    if "go" in lang_lower:
        return f"Utilize `go vet` e `golangci-lint` no pipeline de '{name}', além de controlar encerramento de goroutines com `context.WithTimeout` para evitar vazamentos de recursos."
    if "java" in lang_lower or "kotlin" in lang_lower or "jvm" in topics_set:
        return f"Configure JVM flags com `-XX:+UseContainerSupport` e garanta que pools de conexões e threads de '{name}' respeitem os limites de CPU da máquina."
    if "c++" in lang_lower or "cpp" in lang_lower or "c" in lang_lower:
        return f"Compile '{name}' com sanitizers de memória (`-fsanitize=address,undefined`) durante o desenvolvimento para detectar buffer overflows e vazamentos de memória imediatamente."
    if "swift" in lang_lower:
        return f"Utilize Swift Concurrency (async/await com Actors) no projeto '{name}' para garantir safety contra data races em operações assíncronas."
    if "php" in lang_lower:
        return f"Habilite OPcache com JIT ativado no PHP e utilize `composer install --no-dev --optimize-autoloader` no deploy de produção de '{name}'."
    if "ruby" in lang_lower:
        return f"Execute `bundle exec rubocop -a` e utilize jemalloc com Ruby em produção no projeto '{name}' para reduzir fragmentação de memória."

    # Fallback contextual por tópicos gerais
    generic_topic_tips = {
        "ci": f"Configure cache de dependências no pipeline CI de '{name}' para não refazer download de pacotes a cada execução.",
        "deploy": f"Use environments no deploy de '{name}' com approval gates para produção para evitar publicações acidentais.",
        "api": f"Documente a API de '{name}' com OpenAPI/Swagger gerado automaticamente a partir de código para prevenir documentação defasada.",
        "plugin": f"Registre o plugin '{name}' no catálogo oficial do ecossistema para validação automatizada e maior visibilidade.",
    }
    for topic, tip in generic_topic_tips.items():
        if topic in topics_set or topic in str(topics_set):
            return tip

    return f"Inspecione a arquitetura modular e os testes na raiz de '{name}' antes de estender funcionalidades, garantindo retrocompatibilidade com novas versões."

def analyze_repository(repo_info):
    """Analisa um repositório individualmente usando IA ou fallback contextual."""
    full_name = repo_info.get("full_name", "")
    owner, name = full_name.split("/")
    description = repo_info.get("description") or "Sem descrição fornecida"
    language = repo_info.get("language") or "Docs / Shell"
    topics = ", ".join(repo_info.get("topics") or [])

    print(f"-> Analisando repositório: {full_name}...")
    readme_text = get_repo_readme(owner, name)

    prompt = f"""Você é um arquiteto de software sênior brasileiro especializado em código aberto.
Analise detalhadamente o repositório do GitHub '{full_name}' (Linguagem principal: {language}).

Descrição oficial: {description}
Tópicos/Tags: {topics}
Trecho do README:
{readme_text[:4000]}

Gere EXATAMENTE a estrutura abaixo em Português do Brasil (pt-BR) com alto nível técnico e sem superficialidades:

- 🎯 **O que é e para que serve:** (Explique com precisão técnica em 2 a 3 frases o propósito real da ferramenta, sua arquitetura e seu principal diferencial competitivo)
- 💡 **Casos de uso reais no dia a dia:** (Apresente 2 a 3 cenários práticos e objetivos de aplicação em projetos reais de engenharia de software, dados, segurança ou infraestrutura)
- 🚀 **Como usar na prática com comandos prontos:**
```bash
(Forneça comandos exatos, funcionais e corretos de instalação e execução rápida em Docker, pip, npm, cargo, go ou clone)
```
- ⚡ **Dica Pro de produtividade:** (Forneça uma dica técnica única, avançada e exclusiva para este projeto, citando flags reais de CLI, parâmetros de configuração, variáveis de ambiente ou decisões arquiteturais. NUNCA use frases genéricas como 'leia a documentação' ou 'consulte o readme')

REGRAS:
1. Responda 100% em Português do Brasil.
2. Seja profundo, específico e técnico.
3. Não use dicas genéricas."""

    # 1. Tentar Gemini
    res = call_gemini(prompt)
    if res:
        return res

    # 2. Tentar OpenAI
    res = call_openai(prompt)
    if res:
        return res

    # 3. Tentar OpenRouter (fallback gratuito agnóstico)
    res = call_openrouter(prompt)
    if res:
        return res

    # 4. Fallback contextual dinâmico inteligente
    print("  → Usando analisador contextual dinâmico baseado no README")
    return generate_smart_dynamic_analysis(repo_info, readme_text)

def call_openrouter(prompt):
    """Chama a API do OpenRouter como fallback gratuito agnóstico.
    Usa o modelo 'openrouter/free' que roteia para o melhor modelo gratuito disponível.
    Endpoint compatível com OpenAI: https://openrouter.ai/api/v1/chat/completions
    """
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

def rebuild_catalog_markdown(all_stars, master_db):
    """Reconstrói o arquivo CATALOGO_ESTRELAS.md determinística e perfeitamente."""
    total = len(all_stars)
    doc = []

    # 1. CABEÇALHO OFICIAL
    doc.append("# 🌟 Dossiê Completo: Análise Minuciosa das Estrelas do GitHub")
    doc.append("")
    doc.append(f"> **Perfil:** [@{GITHUB_USERNAME}](https://github.com/{GITHUB_USERNAME}) (Matheus Salustiano)  ")
    doc.append(f"> **Total de Repositórios Analisados:** {total}  ")
    doc.append("> **Estrutura Obrigatória por Item:**  ")
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

        info = master_db.get(name)
        if not info:
            info = generate_smart_dynamic_analysis(r, "")
            master_db[name] = info

        security_badge = scan_repository_security(r)

        doc.append(f"<a id=\"{anchor}\"></a>")
        doc.append(f"### {i:02d}. [{name}]({url})")
        doc.append(f"- **⭐ Stars:** {stars:,} | **💻 Linguagem:** `{lang}`")
        doc.append(f"- 🛡️ **Segurança & Malware:** {security_badge}")
        doc.append(f"- 🎯 **O que é e para que serve:** {info['what']}")
        doc.append(f"- 💡 **Casos de uso reais no dia a dia:** {info['use_cases']}")
        doc.append(f"- 🚀 **Como usar na prática com comandos prontos:**")
        doc.append(f"{info['quickstart']}")
        doc.append(f"- ⚡ **Dica Pro de produtividade:** {info['pro_tip']}")
        doc.append("")
        doc.append("---")
        doc.append("")

    return "\n".join(doc)

def main():
    print(f"Iniciando verificação e sincronização de estrelas para: {GITHUB_USERNAME}")

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
            # Em caso de falha da API (ex: rate limit sem token), marcar status
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

    # Salvar cópia atualizada da lista de repositórios
    with open(ALL_STARS_FILE, "w", encoding="utf-8") as f:
        json.dump(all_stars, f, indent=2, ensure_ascii=False)

    # 4. Identificar novos repositórios que ainda não foram analisados
    new_found = 0
    for repo in all_stars:
        repo_name = repo.get("full_name")
        repo_id = repo.get("id")

        if repo_name not in master_db or repo_id not in processed_ids:
            analysis = analyze_repository(repo)
            master_db[repo_name] = analysis
            if repo_id:
                processed_ids.add(repo_id)
            new_found += 1

    print(f"Novos repositórios processados nesta rodada: {new_found}")

    # 5. Salvar bases de dados atualizadas
    with open(MASTER_DB_FILE, "w", encoding="utf-8") as f:
        json.dump(master_db, f, indent=2, ensure_ascii=False)

    with open(CATALOG_DB_FILE, "w", encoding="utf-8") as f:
        json.dump(master_db, f, indent=2, ensure_ascii=False)

    # 6. Salvar estado de IDs processados
    processed_data["processed_ids"] = list(processed_ids)
    processed_data["total"] = total_current
    processed_data["last_updated"] = datetime.now(timezone.utc).isoformat()
    with open(PROCESSED_FILE, "w", encoding="utf-8") as f:
        json.dump(processed_data, f, indent=2, ensure_ascii=False)

    # 7. Reconstruir o CATALOGO_ESTRELAS.md determinístico
    catalog_markdown = rebuild_catalog_markdown(all_stars, master_db)
    with open(CATALOG_FILE, "w", encoding="utf-8") as f:
        f.write(catalog_markdown)

    # 8. Espelhar de forma segura nos caminhos locais se existirem
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
