import sys
import urllib.request
import json
import base64

sys.stdout.reconfigure(encoding='utf-8')

repos = ['different-ai/openwork', 'deepseek-ai/deepseek-harness']

for repo in repos:
    try:
        url = f'https://api.github.com/repos/{repo}'
        req = urllib.request.Request(url, headers={'User-Agent': 'GitHub-Analyzer'})
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            print('='*60)
            print(f"REPO: {data.get('full_name')}")
            print(f"STARS: {data.get('stargazers_count')}")
            print(f"LANGUAGE: {data.get('language')}")
            print(f"DESCRIPTION: {data.get('description')}")
            print(f"TOPICS: {data.get('topics')}")
            
        url_readme = f'https://api.github.com/repos/{repo}/readme'
        req_r = urllib.request.Request(url_readme, headers={'User-Agent': 'GitHub-Analyzer'})
        with urllib.request.urlopen(req_r) as resp:
            r_data = json.loads(resp.read().decode('utf-8'))
            readme = base64.b64decode(r_data['content']).decode('utf-8', errors='ignore')
            print('--- README PREVIEW ---')
            print(readme[:3500])
    except Exception as e:
        print(f"Erro ao consultar {repo}: {e}")
