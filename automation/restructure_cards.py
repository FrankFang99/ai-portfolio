"""把 6 个项目卡片从 <article> 改成 <a> 包裹结构，hover 展开"""
import re
from pathlib import Path

INDEX = Path(r"D:\Learning\AI\面试\ai-portfolio\index.html")

content = INDEX.read_text(encoding="utf-8")

# 正则：匹配 <article class="project-card">...</article>
# 关键改造：
# 1) <article class="project-card"> → <a class="project-card" href="URL" target="_blank" rel="noopener">
# 2) 末尾的 <a class="project-link">...</a> → <span class="project-link">...</span>
# 3) 把 tagline + tech + link 全部包到 <div class="project-hover-content"> 里

pattern = re.compile(
    r'<article class="project-card">\s*'
    r'(<div class="project-icon">.*?</div>)\s*'
    r'(<h3 class="project-title">.*?</h3>)\s*'
    r'(<p class="project-tagline">.*?</p>)\s*'
    r'(<div class="project-tech">.*?</div>)\s*'
    r'(<a href="([^"]+)"[^>]*class="project-link">.*?</a>)\s*'
    r'</article>',
    re.DOTALL
)

def repl(m):
    icon = m.group(1)
    title = m.group(2)
    tagline = m.group(3)
    tech = m.group(4)
    link_tag = m.group(5)
    url = m.group(6)
    # 把 link 的 <a ... class="project-link">...</a> 换成 <span class="project-link">...</span>
    inner_link = re.sub(r'<a [^>]*class="project-link">(.*?)</a>',
                        r'<span class="project-link">\1</span>',
                        link_tag, flags=re.DOTALL)
    return (
        f'<a class="project-card" href="{url}" target="_blank" rel="noopener">\n'
        f'        {icon}\n'
        f'        {title}\n'
        f'        <div class="project-hover-content">\n'
        f'          {tagline}\n'
        f'          {tech}\n'
        f'          {inner_link}\n'
        f'        </div>\n'
        f'      </a>'
    )

new_content, n = pattern.subn(repl, content)
print(f"Replaced {n} project cards")

INDEX.write_text(new_content, encoding="utf-8")
print(f"Written: {INDEX}")
