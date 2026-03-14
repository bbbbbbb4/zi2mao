import os
from PIL import Image, ImageDraw, ImageFont

# ================= 配置参数 =================
# 使用了 r"" 前缀来处理 Windows 路径，防止斜杠报错
# 请核对：确保最后的文件名就是你下载的字体文件名
FONT_PATH = r"C:\Users\高彬彬\Desktop\MaoZeDongShuFaZiTi\maozedong-1.ttf" 

# 输出文件夹也设置在桌面，生成完你可以直接在桌面看到
OUTPUT_DIR = r"C:\Users\高彬彬\Desktop\domain_B_mao"  
IMAGE_SIZE = 256             
FONT_SIZE = 200              

# 这里先放 100 个极其常用的汉字作为测试数据集
CHAR_LIST = (
    "的一是在不了有和人这中大为上个国我以要他时来用们生到作地于出就分对成会可主发年动"
    "同工也能下过子说产种面而方后多定行学法所民得经十三之进着等部度家电力里如水化高自"
    "二理起小物现实加量都两体制机当使点从业本去把性好应开它合还因由其些然前外天政四日"
)
# ============================================

def generate_dataset():
    # 创建输出文件夹
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # 尝试加载字体
    try:
        font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
    except IOError:
        print(f"❌ 找不到字体文件！请检查路径：'{FONT_PATH}' 是否正确。")
        return

    print(f"✅ 成功加载字体。开始渲染 {len(CHAR_LIST)} 个汉字...")

    # 遍历每个汉字并生成图片
    for i, char in enumerate(CHAR_LIST):
        img = Image.new('RGB', (IMAGE_SIZE, IMAGE_SIZE), color='white')
        draw = ImageDraw.Draw(img)
        
        # 精确计算文字的边界框，实现绝对居中
        bbox = draw.textbbox((0, 0), char, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        
        x = (IMAGE_SIZE - text_w) / 2 - bbox[0]
        y = (IMAGE_SIZE - text_h) / 2 - bbox[1]
        
        draw.text((x, y), char, font=font, fill='black')
        
        # 按照 "0001_的.jpg" 的格式统一命名保存
        filename = f"{i+1:04d}_{char}.jpg"
        save_path = os.path.join(OUTPUT_DIR, filename)
        img.save(save_path)
        
        if (i + 1) % 20 == 0:
            print(f"已生成 {i + 1} / {len(CHAR_LIST)} 张图片...")

    print(f"🎉 全部完成！去桌面的 '{OUTPUT_DIR}' 文件夹里看看吧！")

if __name__ == "__main__":
    generate_dataset()