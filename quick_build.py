#!/usr/bin/env python3
"""
WordMaster APK 快速构建助手
"""
import os
import subprocess
import sys

def check_git_status():
    """检查 Git 状态"""
    try:
        result = subprocess.run(['git', 'status'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Git 仓库状态正常")
            return True
        else:
            print("❌ Git 仓库状态异常")
            return False
    except FileNotFoundError:
        print("❌ 未找到 Git，请先安装 Git")
        return False

def init_git_if_needed():
    """初始化 Git 仓库（如果需要）"""
    if not os.path.exists('.git'):
        print("📂 初始化 Git 仓库...")
        subprocess.run(['git', 'init'], check=True)
        subprocess.run(['git', 'add', '.'], check=True)
        subprocess.run(['git', 'commit', '-m', 'WordMaster - 初始化 APK 构建配置'], check=True)
        print("✅ Git 仓库初始化完成")

def get_build_status():
    """获取构建状态"""
    files = [
        'buildozer.spec',
        '.github/workflows/build-android.yml',
        'data/icon_bg.png',
        'data/icon_fg.png'
    ]
    
    missing_files = []
    for file in files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("❌ 缺少必要文件:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    else:
        print("✅ 所有构建文件都已准备就绪")
        return True

def show_next_steps():
    """显示下一步操作"""
    print("\n🚀 下一步操作:")
    print("1. 创建 GitHub 仓库:")
    print("   - 访问 https://github.com/new")
    print("   - 仓库名称: wordmaster")
    print("   - 设置为 Public")
    
    print("\n2. 推送代码到 GitHub:")
    print("   git remote add origin https://github.com/你的用户名/wordmaster.git")
    print("   git push -u origin main")
    
    print("\n3. 启用 GitHub Actions:")
    print("   - 进入 GitHub 仓库的 Actions 页面")
    print("   - 启用 'Build Android APK' 工作流")
    
    print("\n4. 等待构建完成 (约 10-15 分钟)")
    print("5. 在 Actions 页面下载生成的 APK 文件")

def main():
    print("📱 WordMaster APK 构建助手")
    print("=" * 50)
    
    # 检查构建文件
    if not get_build_status():
        print("\n请确保所有构建文件都已创建")
        return
    
    # 检查 Git 状态
    if check_git_status():
        # 初始化 Git（如果需要）
        init_git_if_needed()
    else:
        print("请先安装 Git 或手动初始化仓库")
        return
    
    print("\n📋 构建准备状态:")
    print("✅ Buildozer 配置文件已创建")
    print("✅ 应用图标已生成")
    print("✅ GitHub Actions 工作流已配置")
    print("✅ 构建指南已准备")
    
    show_next_steps()
    
    print("\n📚 详细文档:")
    print("   - 完整指南: README_APK.md")
    print("   - 详细步骤: APK_BUILD_GUIDE.md")

if __name__ == "__main__":
    main()