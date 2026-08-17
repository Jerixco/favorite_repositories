import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("data/all_starred_github.json", "r", encoding="utf-8") as f:
    all_stars = json.load(f)

print(f"Total: {len(all_stars)}")
for i, r in enumerate(all_stars[:45], 1):
    print(f"[{i:02d}] {r['full_name']} (⭐ {r['stargazers_count']}) [{r['language']}]")
    print(f"     Desc: {r['description']}")
    print(f"     Topics: {r.get('topics', [])}")
    print("-" * 60)
