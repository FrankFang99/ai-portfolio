"""把 6 张图标拼成 3x2 预览图，方便用户一眼看效果"""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

ICONS_DIR = Path(r"D:\Learning\AI\面试\ai-portfolio\assets\icons")
OUTPUT = Path(r"D:\Learning\AI\面试\ai-portfolio\preview-icons-grid.png")

# 项目列表（按作品集顺序）
projects = [
    ("cmb-customer-service.png", "AI 智能客服 - 招商银行"),
    ("ai-landing-research.png",  "AI 行业落地研究"),
    ("ggti-16-type.png",         "GGTI 股格测试"),
    ("xiaozhuan-biography.png",  "小传 - AI 传记助手"),
    ("buffett-letters.png",      "巴菲特股东信"),
    ("empty-the-cart.png",       "免费清空购物车"),
]

# 布局参数
TILE = 480        # 每张 tile 大小
COLS = 3
ROWS = 2
PAD = 24          # tile 之间间距
LABEL_H = 56      # 标签区高度
BG = (10, 14, 39) # 跟作品集背景同色 #0a0e27
TEXT = (255, 255, 255)
SUB = (255, 255, 255, 180)

W = COLS * TILE + (COLS + 1) * PAD
H = ROWS * (TILE + LABEL_H) + (ROWS + 1) * PAD

canvas = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(canvas)

# 字体（尝试用系统字体，回退 default）
try:
    font_label = ImageFont.truetype("msyh.ttc", 22)
except OSError:
    font_label = ImageFont.load_default()

for i, (fname, label) in enumerate(projects):
    col = i % COLS
    row = i // COLS
    x = PAD + col * (TILE + PAD)
    y = PAD + row * (TILE + LABEL_H + PAD)

    # 加载并缩放图标
    img_path = ICONS_DIR / fname
    if not img_path.exists():
        print(f"missing: {img_path}")
        continue
    img = Image.open(img_path).convert("RGB")
    img = img.resize((TILE, TILE), Image.LANCZOS)

    # 圆角 mask（用 alpha）
    mask = Image.new("L", (TILE, TILE), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, TILE, TILE), radius=24, fill=255)
    img_rounded = Image.new("RGB", (TILE, TILE), BG)
    img_rounded.paste(img, (0, 0), mask)
    canvas.paste(img_rounded, (x, y))

    # 标签
    bbox = draw.textbbox((0, 0), label, font=font_label)
    tw = bbox[2] - bbox[0]
    tx = x + (TILE - tw) // 2
    ty = y + TILE + 14
    draw.text((tx, ty), label, fill=TEXT, font=font_label)

canvas.save(OUTPUT, "PNG", optimize=True)
print(f"saved: {OUTPUT} ({OUTPUT.stat().st_size // 1024} KB)")
