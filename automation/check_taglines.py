"""检查最新 commit 的 6 个 tagline 内容"""
import subprocess
import re

c = subprocess.run(
    ["git", "show", "HEAD:index.html"],
    capture_output=True, text=True, encoding="utf-8"
).stdout

taglines = re.findall(
    r'<p class="project-tagline">\s*(.+?)\s*</p>',
    c, re.DOTALL
)

print(f"Found {len(taglines)} taglines\n")
for i, t in enumerate(taglines, 1):
    # 整理空白
    clean = " ".join(t.split())
    print(f"=== Tagline {i} ===")
    print(clean)
    print()
