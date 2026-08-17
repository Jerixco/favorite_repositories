import sys, json, subprocess

sys.stdout.reconfigure(encoding='utf-8')

res = subprocess.check_output(['gh', 'api', 'users/Jerixco/starred', '--paginate']).decode('utf-8')
data = json.loads(res)
print(f"Total current starred repos on GitHub: {len(data)}")
for i, r in enumerate(data, 1):
    print(f"{i:02d}. {r['full_name']} (⭐ {r['stargazers_count']}) [{r['language']}]")
