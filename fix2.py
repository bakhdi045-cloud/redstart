import re

with open('part1.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Ensure we get the correct lines: we want the @app.cell starting with mo.md("### Validation Summary")
start_idx = -1
end_idx = -1
for i, line in enumerate(lines):
    if 'def _(K_oc, K_pp, mo, np, pi, sol_oc_nl, sol_pp_nl):' in line:
        start_idx = i - 1  # Get the @app.cell
        break

for i in range(start_idx, len(lines)):
    if 'if __name__ == "__main__":' in lines[i]:
        end_idx = i
        break

to_add = ''.join(lines[start_idx:end_idx])

with open('notebook-day-2.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace trailing block logic
text = re.sub(r'(@app\.cell\ndef _\(\):\n    return\n\n\n)+if __name__ == "__main__":\n    app\.run\(\)\n*', '', text) 
text = text.replace('if __name__ == "__main__":\n    app.run()\n', '')

# Append
if 'Validation Summary' not in text:
    text = text.rstrip() + '\n\n\n' + to_add + 'if __name__ == "__main__":\n    app.run()\n'

# Fix variables
text = text.replace('def check(sol, K):', 'def check(sol_val, K):')
text = text.replace('xi = sol.y', 'xi = sol_val.y')
text = text.replace('np.abs(sol.y', 'np.abs(sol_val.y')

with open('notebook-day-2.py', 'w', encoding='utf-8') as f:
    f.write(text)
