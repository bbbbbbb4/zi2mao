import os
import shutil
from PIL import Image

# ================= 配置参数 =================
# 输入文件夹（桌面上刚才提取的两个文件夹）
DIR_A = r"C:\Users\高彬彬\Desktop\domain_A_mine"
DIR_B = r"C:\Users\高彬彬\Desktop\domain_B_mao"

# 输出总文件夹（将作为 pix2pix 的 --dataroot 路径）
OUTPUT_DIR = r"C:\Users\高彬彬\Desktop\my_font_dataset"

# 单张图片的尺寸
IMG_SIZE = 256
# ============================================

def create_dataset():
    # 获取所有的文件名（两个文件夹里的文件名是一一对应的）
    files_A = [f for f in os.listdir(DIR_A) if f.endswith('.jpg')]
    files_A.sort()
    
    total_imgs = len(files_A)
    if total_imgs == 0:
        print("❌ 在 Domain A 找不到图片，请检查路径！")
        return
        
    print(f"✅ 找到 {total_imgs} 对图片，开始拼接并划分数据集...")

    # 创建标准目录结构
    for folder in ['train', 'val', 'test']:
        os.makedirs(os.path.join(OUTPUT_DIR, folder), exist_ok=True)

    # 简单划分比例：前 80% 训练，接下来 10% 验证，最后 10% 测试
    num_train = int(total_imgs * 0.8)
    num_val = int(total_imgs * 0.1)
    # 剩下的给 test

    for i, filename in enumerate(files_A):
        path_A = os.path.join(DIR_A, filename)
        path_B = os.path.join(DIR_B, filename)

        # 确保 B 文件夹里也有这个文件
        if not os.path.exists(path_B):
            print(f"⚠️ 警告: 找不到对应的 B 图片 {filename}，跳过该文件。")
            continue

        # 打开两张图片
        img_A = Image.open(path_A)
        img_B = Image.open(path_B)

        # 创建一张 512 x 256 的宽图
        paired_img = Image.new('RGB', (IMG_SIZE * 2, IMG_SIZE))
        
        # 将 A 贴在左边 (0, 0)，B 贴在右边 (256, 0)
        paired_img.paste(img_A, (0, 0))
        paired_img.paste(img_B, (IMG_SIZE, 0))

        # 决定这张图该去哪个文件夹
        if i < num_train:
            sub_folder = 'train'
        elif i < num_train + num_val:
            sub_folder = 'val'
        else:
            sub_folder = 'test'

        # 保存拼接后的图片
        save_path = os.path.join(OUTPUT_DIR, sub_folder, filename)
        paired_img.save(save_path)

        if (i + 1) % 20 == 0:
            print(f"已处理 {i + 1} / {total_imgs} 张...")

    print(f"🎉 拼接完成！最终数据集已保存在桌面的 '{OUTPUT_DIR}' 文件夹中。")
    print(f"   - Train: {num_train} 张")
    print(f"   - Val: {num_val} 张")
    print(f"   - Test: {total_imgs - num_train - num_val} 张")

if __name__ == "__main__":
    create_dataset()