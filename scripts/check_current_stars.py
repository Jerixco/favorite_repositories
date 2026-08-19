import sys, json, subprocess

sys.stdout.reconfigure(encoding='utf-8')

try:
    res = subprocess.check_output(
        ['gh', 'api', 'users/Jerixco/starred', '--paginate'],
        stderr=subprocess.DEVNULL
    ).decode('utf-8', errors='replace')
    data = json.loads(res)
    print(f"Total current starred repos on GitHub: {len(data)}")
    for i, r in enumerate(data, 1):
        print(f"{i:02d}. {r.get('full_name')} (⭐ {r.get('stargazers_count', 0)}) [{r.get('language') or 'N/A'}]")
except Exception as e:
    print(f"Erro ao verificar estrelas atuais via gh CLI: {e}")
