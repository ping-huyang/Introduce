from PIL import Image
import os

# 获取当前目录
current_dir = os.getcwd()

# 遍历当前目录下的所有png图片
for filename in os.listdir(current_dir):
    if filename.endswith('.png'):
        # 打开图片
        img = Image.open(filename)
        
        # 获取原始尺寸和长宽比
        width, height = img.size
        aspect_ratio = width / height
        
        # 计算新的高度
        new_height = int(800 / aspect_ratio)
        
        # 调整图片尺寸
        img = img.resize((800, new_height))
        
        # 保存图片
        img.save(filename)