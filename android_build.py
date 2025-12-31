#!/usr/bin/env python3
"""
Android APK构建脚本 - 使用python-for-android直接构建
"""

import os
import sys
import subprocess
import shutil

# 配置参数
APP_NAME = "WordMaster英语学习助手"
PACKAGE_NAME = "org.wordmaster.wordmaster"
VERSION = "1.0"
SOURCE_DIR = "."
OUTPUT_DIR = "bin"

# 依赖列表
REQUIREMENTS = [
    "python3",
    "kivy==2.2.1",
    "kivymd==1.1.1",
    "gtts==2.3.2",
    "pygame==2.5.2",
    "speechrecognition==3.10.1",
    "pydub==0.25.1",
    "matplotlib==3.8.0",
    "numpy==1.26.0",
    "pandas==2.1.1"
]

# Android权限
ANDROID_PERMISSIONS = [
    "android.permission.INTERNET",
    "android.permission.WRITE_EXTERNAL_STORAGE",
    "android.permission.READ_EXTERNAL_STORAGE",
    "android.permission.RECORD_AUDIO",
    "android.permission.MODIFY_AUDIO_SETTINGS"
]

def run_command(cmd, cwd=None):
    """运行命令并返回结果"""
    print(f"执行命令: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    print(f"退出码: {result.returncode}")
    if result.stdout:
        print(f"输出:\n{result.stdout}")
    if result.stderr:
        print(f"错误:\n{result.stderr}")
    return result

def install_p4a():
    """安装python-for-android"""
    print("=== 安装python-for-android ===")
    cmd = [sys.executable, "-m", "pip", "install", "python-for-android"]
    result = run_command(cmd)
    if result.returncode != 0:
        print("安装python-for-android失败，尝试使用Buildozer的p4a")
        cmd = [sys.executable, "-m", "pip", "install", "buildozer[android]"]
        return run_command(cmd)
    return result

def build_apk():
    """构建APK"""
    print("=== 构建APK ===")
    
    # 确保输出目录存在
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # 构建命令
    cmd = [
        "p4a", "apk",
        "--private", SOURCE_DIR,
        "--package", PACKAGE_NAME,
        "--name", APP_NAME,
        "--version", VERSION,
        "--bootstrap", "sdl2",
        "--requirements", ",".join(REQUIREMENTS),
        "--permission", ",".join(ANDROID_PERMISSIONS),
        "--orientation", "portrait",
        "--arch", "armeabi-v7a",
        "--arch", "arm64-v8a",
        "--dist-name", f"wordmaster-{VERSION}",
        "--output-dir", OUTPUT_DIR,
        "--debug"
    ]
    
    return run_command(cmd)

def build_with_buildozer():
    """使用Buildozer构建"""
    print("=== 使用Buildozer构建 ===")
    
    # 清理之前的构建
    cmd_clean = ["buildozer", "android", "clean"]
    run_command(cmd_clean)
    
    # 构建APK
    cmd_build = ["buildozer", "android", "debug", "-v"]
    return run_command(cmd_build)

def main():
    """主函数"""
    print("🚀 Android APK构建脚本")
    print(f"应用名称: {APP_NAME}")
    print(f"包名: {PACKAGE_NAME}")
    print(f"版本: {VERSION}")
    print()
    
    # 安装依赖
    if install_p4a().returncode != 0:
        print("❌ 依赖安装失败")
        return 1
    
    # 尝试使用python-for-android构建
    print("\n尝试方法1: 使用python-for-android直接构建")
    result = build_apk()
    
    if result.returncode != 0:
        print("\n❌ python-for-android构建失败，尝试方法2: 使用Buildozer")
        result = build_with_buildozer()
    
    # 检查构建结果
    if result.returncode == 0:
        print("\n✅ 构建成功！")
        # 列出构建产物
        if os.path.exists(OUTPUT_DIR):
            print("\n构建产物:")
            for file in os.listdir(OUTPUT_DIR):
                if file.endswith(".apk"):
                    file_path = os.path.join(OUTPUT_DIR, file)
                    size = os.path.getsize(file_path) / (1024 * 1024)
                    print(f"  - {file} ({size:.2f} MB)")
        return 0
    else:
        print("\n❌ 构建失败！")
        return 1

if __name__ == "__main__":
    sys.exit(main())
