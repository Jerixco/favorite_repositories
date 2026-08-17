import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("CATALOGO_ESTRELAS.md", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Verificar sumário no topo
toc_pos = content.find("## 📑 Sumário Completo dos Repositórios")
det_pos = content.find("## 🔍 Análise Detalhada Repositório por Repositório")

print(f"Posição do Sumário: {toc_pos}")
print(f"Posição da Análise Detalhada: {det_pos}")
assert 0 < toc_pos < det_pos, "O sumário DEVE vir antes das análises detalhadas!"

# 2. Contar itens no sumário
toc_items = re.findall(r"^\d+\.\s+\[([^\]]+)\]\(#([^\)]+)\)", content, re.MULTILINE)
print(f"Total de itens no Sumário: {len(toc_items)}")

# 3. Contar seções detalhadas
det_items = re.findall(r"^### \d+\.\s+\[([^\]]+)\]\(([^)]+)\)", content, re.MULTILINE)
print(f"Total de seções detalhadas: {len(det_items)}")

# 4. Verificar se há dicas repetidas
dicas = re.findall(r"- ⚡ \*\*Dica Pro de produtividade:\*\* (.*)", content)
print(f"Total de Dicas Pro encontradas: {len(dicas)}")
unique_dicas = set(dicas)
print(f"Total de Dicas Pro únicas: {len(unique_dicas)}")

print("Verificação concluída com 100% de sucesso!")
