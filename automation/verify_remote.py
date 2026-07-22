"""verify 远程仓库 index.html 的关键内容"""
import base64
import json
import subprocess

REPO = "FrankFang99/ai-portfolio"

# 拉取远程 index.html
result = subprocess.run(
    ["gh", "api", f"/repos/{REPO}/contents/index.html"],
    capture_output=True, text=True, encoding="utf-8"
)
if result.returncode != 0:
    print(f"ERROR: {result.stderr}")
    raise SystemExit(1)

data = json.loads(result.stdout)
b64_content = data["content"]
size = data["size"]

# decode
content = base64.b64decode(b64_content).decode("utf-8")

# checks
checks = {
    "小传": "小传" in content,
    "v3.12.1": "v3.12.1" in content,
    "frank-fangyz@139.com": "frank-fangyz@139.com" in content,
    "方逸之": "方逸之" in content,
    "Coming Soon 残留": "Coming Soon" in content,
    "方意智 残留": "方意智" in content,
    "项目数 6": "GitHub Pages 已部署" in content and ">6<" in content,
}

print(f"Remote index.html size: {size} bytes")
print("=" * 50)
for k, v in checks.items():
    icon = "[OK]" if v else "[FAIL]"
    print(f"{icon} {k}: {v}")

# 列出项目标题
print("\n=== 项目卡片标题 ===")
import re
titles = re.findall(r'<h3 class="project-title">([^<]+)', content)
for i, t in enumerate(titles, 1):
    print(f"  {i}. {t}")

print(f"\n共 {len(titles)} 个项目卡片")
