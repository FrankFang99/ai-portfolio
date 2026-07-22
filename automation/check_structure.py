"""验证 HTML 结构（6 个 project-card + hover-content 数量）"""
import re
import subprocess

c = subprocess.run(
    ["git", "show", "HEAD:index.html"],
    capture_output=True, text=True, encoding="utf-8"
).stdout

# 6 个 a.project-card
cards = re.findall(r'<a class="project-card"[^>]*href="([^"]+)"', c)
print(f"project cards: {len(cards)}")
for i, h in enumerate(cards, 1):
    print(f"  {i}. {h}")

# hover-content 块
hc = c.count("project-hover-content")
print(f"\nhover-content 块: {hc}")

# status 标签
statuses = re.findall(r'project-status[^"]*">([^<]+)<', c)
print(f"\nstatus 标签: {statuses}")

# title 文字
titles = re.findall(r'<h3 class="project-title">([^<]+)<', c)
print(f"\ntitle 文字（前缀）:")
for i, t in enumerate(titles, 1):
    print(f"  {i}. {t[:30]}")
