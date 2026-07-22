"""用 GitHub API 更新 index.html，绕过 git push 网络问题。"""
import base64
import json
import subprocess
import sys
from pathlib import Path

REPO = "FrankFang99/ai-portfolio"
BRANCH = "main"
FILE_PATH = "index.html"
LOCAL_PATH = Path(r"D:\Learning\AI\面试\ai-portfolio\index.html")
COMMIT_MESSAGE = """feat: 加入小传项目 + 升级招商银行智能客服至 v3.12.1 final

- 新增：小传 - AI 传记助手（React + TS + Vite）
- 升级：AI 智能客服 - 招商银行 从 Coming Soon 到 v3.12.1 final
  - 9 轮迭代：对抗性 39% 到 95%（+56pp）
  - P0 召回 97.91% / 业务权重 91.86% / 多轮 66.7%
  - 链接到 GitHub Page Live Demo
- 更新：Stats + About 中项目数 5 到 6
- 保留：联系方式 frank-fangyz@139.com

🤖 Generated with Mavis"""


def get_current_sha():
    result = subprocess.run(
        ["gh", "api", f"/repos/{REPO}/contents/{FILE_PATH}", "--jq", ".sha"],
        capture_output=True, text=True, encoding="utf-8"
    )
    if result.returncode != 0:
        print(f"ERROR get_sha: {result.stderr}", file=sys.stderr)
        sys.exit(1)
    return result.stdout.strip()


def update_file(sha, content_b64, message):
    body = {
        "message": message,
        "branch": BRANCH,
        "sha": sha,
        "content": content_b64,
    }
    result = subprocess.run(
        ["gh", "api", f"/repos/{REPO}/contents/{FILE_PATH}",
         "-X", "PUT", "--input", "-"],
        input=json.dumps(body, ensure_ascii=False),
        capture_output=True, text=True, encoding="utf-8"
    )
    if result.returncode != 0:
        print(f"ERROR update: {result.stderr}", file=sys.stderr)
        print(f"stdout: {result.stdout[:500]}", file=sys.stderr)
        sys.exit(1)
    return result.stdout


def main():
    print(f"[1/3] 读取本地文件: {LOCAL_PATH}")
    raw = LOCAL_PATH.read_bytes()
    print(f"      字节数: {len(raw)}")
    content_b64 = base64.b64encode(raw).decode("ascii")
    print(f"      base64 长度: {len(content_b64)}")

    print(f"[2/3] 取远程文件 sha ...")
    sha = get_current_sha()
    print(f"      sha: {sha}")

    print(f"[3/3] PUT 更新文件 ...")
    resp = update_file(sha, content_b64, COMMIT_MESSAGE)
    print(f"      响应: {resp[:200]}")
    print("\n✅ 更新成功")


if __name__ == "__main__":
    main()
