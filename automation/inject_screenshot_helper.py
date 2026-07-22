"""本地截图调试版 HTML：在 </body> 前加 query 强制显示所有 reveal"""
from pathlib import Path

INDEX = Path(r"D:\Learning\AI\面试\ai-portfolio\index.html")
html = INDEX.read_text(encoding="utf-8")

inject = """
<script>
  // 截图调试：把 URL 加 ?screenshot=1 时强制显示所有 reveal
  if (location.search.includes('screenshot=1')) {
    document.addEventListener('DOMContentLoaded', () => {
      setTimeout(() => {
        document.querySelectorAll('.reveal').forEach(el => {
          el.classList.add('is-visible');
          el.style.opacity = '1';
          el.style.transform = 'translateY(0)';
        });
        // 默认展示 hover 内容（模拟触屏）
        document.querySelectorAll('.project-hover-content').forEach(el => {
          el.style.maxHeight = '500px';
          el.style.opacity = '1';
          el.style.marginTop = '16px';
        });
      }, 200);
    });
  }
</script>
"""

if "screenshot=1" not in html:
    new_html = html.replace("</body>", inject + "</body>", 1)
    INDEX.write_text(new_html, encoding="utf-8")
    print("injected screenshot helper (visit ?screenshot=1 to use)")
else:
    print("already injected")
