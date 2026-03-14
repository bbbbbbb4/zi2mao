import os
from PIL import Image, ImageDraw

# ================= 配置参数 =================
# 读取你刚才生成的毛体字文件夹
INPUT_DIR = r"C:\Users\高彬彬\Desktop\domain_B_mao"
# 导出的 PDF 字帖文件路径
OUTPUT_PDF = r"C:\Users\高彬彬\Desktop\我的专属毛体字帖.pdf"

# A4 纸张尺寸设定 (150 DPI)
A4_WIDTH, A4_HEIGHT = 1240, 1754
CELL_SIZE = 256  # 保持 256x256 的核心尺寸
COLS, ROWS = 4, 6  # 每页排版：4列 × 6行 = 24个字

# 计算居中边距
MARGIN_X = (A4_WIDTH - (COLS * CELL_SIZE)) // 2
MARGIN_Y = (A4_HEIGHT - (ROWS * CELL_SIZE)) // 2
# ============================================

def create_copybook():
    # 获取所有的 jpg 图片并排序
    image_files = [f for f in os.listdir(INPUT_DIR) if f.endswith('.jpg')]
    image_files.sort()

    if not image_files:
        print("❌ 没有找到图片，请确认 INPUT_DIR 文件夹路径！")
        return

    print(f"✅ 找到 {len(image_files)} 张图片，正在排版生成 PDF 字帖...")
    pages = []
    current_page = None
    draw = None

    for index, filename in enumerate(image_files):
        # 每满 24 个字，新建一页 A4 纸
        if index % (COLS * ROWS) == 0:
            if current_page:
                pages.append(current_page)
            # 创建白底 A4 画布
            current_page = Image.new('RGB', (A4_WIDTH, A4_HEIGHT), 'white')
            draw = ImageDraw.Draw(current_page)

        # 计算当前字在 A4 纸上的 X, Y 坐标
        pos_index = index % (COLS * ROWS)
        col = pos_index % COLS
        row = pos_index // COLS
        x = MARGIN_X + col * CELL_SIZE
        y = MARGIN_Y + row * CELL_SIZE

        # 1. 读取原图
        img_path = os.path.join(INPUT_DIR, filename)
        char_img = Image.open(img_path).convert('RGB')

        # 2. 将纯黑色的毛体字变淡 (变为浅灰水印，方便你覆盖书写)
        white_bg = Image.new('RGB', (CELL_SIZE, CELL_SIZE), 'white')
        # alpha=0.82 意味着 82% 是白色，18% 是原字，形成极淡的底印
        faint_img = Image.blend(char_img, white_bg, alpha=0.82) 
        
        # 将水印底字贴到画布上
        current_page.paste(faint_img, (x, y))

        # 3. 绘制带有基准线的“田字格”
        # 画外边框 (深灰色)
        draw.rectangle([x, y, x + CELL_SIZE, y + CELL_SIZE], outline=(120, 120, 120), width=2)
        # 画内部十字交叉线 (浅灰色)
        draw.line([x, y + CELL_SIZE // 2, x + CELL_SIZE, y + CELL_SIZE // 2], fill=(200, 200, 200), width=1)
        draw.line([x + CELL_SIZE // 2, y, x + CELL_SIZE // 2, y + CELL_SIZE], fill=(200, 200, 200), width=1)

    # 把最后一页加进去
    if current_page:
        pages.append(current_page)

    # 导出保存为 PDF
    if pages:
        pages[0].save(OUTPUT_PDF, save_all=True, append_images=pages[1:])
        print(f"🎉 字帖生成成功！共 {len(pages)} 页。")
        print(f"请在桌面查看：{OUTPUT_PDF}")

if __name__ == "__main__":
    create_copybook()