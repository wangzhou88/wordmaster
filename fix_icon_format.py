#!/usr/bin/env python3
"""
修复图标格式问题
解决 libpng 警告：tRNS: invalid with alpha channel
"""
from PIL import Image
import os

def fix_icon_format():
    """修复图标文件格式，确保兼容性和避免 libpng 警告"""
    print("🔧 开始修复图标格式...")
    
    # 修复 icon_bg.png (RGB -> RGBA)
    bg_path = 'data/icon_bg.png'
    if os.path.exists(bg_path):
        try:
            # 打开背景图标
            bg_img = Image.open(bg_path)
            print(f"icon_bg.png - 原始格式: {bg_img.mode}, 尺寸: {bg_img.size}")
            
            # 如果不是RGBA模式，转换为RGBA
            if bg_img.mode != 'RGBA':
                # 创建RGBA图像，白色背景
                new_bg = Image.new('RGBA', bg_img.size, (255, 255, 255, 255))
                if bg_img.mode == 'RGB':
                    # 将RGB图像粘贴到RGBA背景上
                    new_bg.paste(bg_img, (0, 0))
                else:
                    # 对于其他模式，直接转换
                    new_bg = bg_img.convert('RGBA')
                bg_img = new_bg
            
            # 保存修复后的图像
            bg_img.save(bg_path, 'PNG', optimize=True)
            print(f"✅ icon_bg.png 格式已修复为: {bg_img.mode}")
        except Exception as e:
            print(f"❌ 修复 icon_bg.png 时出错: {e}")
    
    # 修复 icon_fg.png (确保RGBA格式正确)
    fg_path = 'data/icon_fg.png'
    if os.path.exists(fg_path):
        try:
            # 打开前景图标
            fg_img = Image.open(fg_path)
            print(f"icon_fg.png - 原始格式: {fg_img.mode}, 尺寸: {fg_img.size}")
            
            # 确保是RGBA模式
            if fg_img.mode != 'RGBA':
                fg_img = fg_img.convert('RGBA')
            
            # 清理可能的透明通道问题
            # 确保所有像素的alpha值都正确设置
            pixels = fg_img.load()
            width, height = fg_img.size
            
            # 检查并修复可能的alpha通道问题
            has_transparency = False
            for x in range(width):
                for y in range(height):
                    r, g, b, a = pixels[x, y]
                    # 如果alpha值异常，设为255（不透明）
                    if a > 255 or a < 0:
                        pixels[x, y] = (r, g, b, 255)
                        has_transparency = True
            
            if has_transparency:
                print("🔧 清理了异常alpha值")
            
            # 保存修复后的图像
            fg_img.save(fg_path, 'PNG', optimize=True)
            print(f"✅ icon_fg.png 格式已验证: {fg_img.mode}")
        except Exception as e:
            print(f"❌ 修复 icon_fg.png 时出错: {e}")
    
    print("🎉 图标格式修复完成！")

def verify_icons():
    """验证修复后的图标"""
    print("\n🔍 验证图标格式...")
    
    files = ['data/icon_bg.png', 'data/icon_fg.png']
    for file in files:
        if os.path.exists(file):
            try:
                img = Image.open(file)
                print(f"{file} - 格式: {img.mode}, 尺寸: {img.size}")
            except Exception as e:
                print(f"❌ 验证 {file} 时出错: {e}")
        else:
            print(f"❌ 文件不存在: {file}")

if __name__ == "__main__":
    fix_icon_format()
    verify_icons()