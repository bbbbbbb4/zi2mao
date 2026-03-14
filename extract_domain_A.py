import os
import fitz  # PyMuPDF 库
from PIL import Image

# ================= 配置参数 =================
INPUT_PDF = r"C:\Users\高彬彬\Desktop\我的专属毛体字帖(1).pdf" # 确认文件名一致
OUTPUT_DIR = r"C:\Users\高彬彬\Desktop\domain_A_mine"

# 必须和之前生成字帖时的参数绝对一致
A4_WIDTH, A4_HEIGHT = 1240, 1754
CELL_SIZE = 256
COLS, ROWS = 4, 6
MARGIN_X = (A4_WIDTH - (COLS * CELL_SIZE)) // 2
MARGIN_Y = (A4_HEIGHT - (ROWS * CELL_SIZE)) // 2

# 必须和 Domain B 保持完全一样的字符顺序，以保证一一对应
CHAR_LIST = (
    "的一是在不了有和人这中大为上个国我以要他时来用们生到作地于出就分对成会可主发年动"
    "同工也能下过子说产种面而方后多定行学法所民得经十三之进着等部度家电力里如水化高自"
    "二理起小物现实加量都两体制机当使点从业本去把性好应开它合还因由其些然前外天政四日"
)
# ============================================

def extract_and_clean():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    try:
        doc = fitz.open(INPUT_PDF)
    except Exception as e:
        print(f"❌ 无法打开 PDF 文件: {e}")
        return

    print("✅ 成功加载 PDF，开始提取并过滤背景...")
    
    char_index = 0
    total_chars = len(CHAR_LIST)

    for page_num in range(len(doc)):
        page = doc[page_num]
        
        # 强制缩放页面到我们设定的 1240x1754 像素，保证裁剪坐标绝对准确
        zoom_x = A4_WIDTH / page.rect.width
        zoom_y = A4_HEIGHT / page.rect.height
        mat = fitz.Matrix(zoom_x, zoom_y)
        pix = page.get_pixmap(matrix=mat)
        
        # 将 PyMuPDF 图像转为 PIL 图像
        img_page = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        
        # 遍历这一页的 24 个格子
        for row in range(ROWS):
            for col in range(COLS):
                if char_index >= total_chars:
                    break
                
                # 计算裁剪坐标
                x0 = MARGIN_X + col * CELL_SIZE
                y0 = MARGIN_Y + row * CELL_SIZE
                x1 = x0 + CELL_SIZE
                y1 = y0 + CELL_SIZE
                
                # 裁剪出单个字
                cell_img = img_page.crop((x0, y0, x1, y1))
                
                # 【核心去噪魔法】: 转换为灰度图，并根据阈值二值化
                # 田字格外框是 120，内部十字是 200。你写的黑字接近 0。
                # 我们设定阈值为 100：颜色比 100 亮的（背景、格子、浅灰底字）全部变成纯白(255)
                # 颜色比 100 暗的（你的黑色笔迹）全部变成纯黑(0)
                gray_img = cell_img.convert('L')
                cleaned_img = gray_img.point(lambda p: 0 if p < 100 else 255, '1')
                
                # 保存图片
                char = CHAR_LIST[char_index]
                filename = f"{char_index+1:04d}_{char}.jpg"
                save_path = os.path.join(OUTPUT_DIR, filename)
                
                cleaned_img.save(save_path)
                char_index += 1

    print(f"🎉 提取大功告成！成功提取了 {char_index} 张纯净的手写图片。")
    print(f"请前往 {OUTPUT_DIR} 检查你的专属数据集！")

if __name__ == "__main__":
    extract_and_clean()