@echo off
chcp 65001
echo ==========================================
echo    WordMaster Git 推送脚本
echo ==========================================
echo.

REM 检查是否已初始化Git
if not exist ".git" (
    echo 🔧 初始化Git仓库...
    git init
    git add .
    git commit -m "WordMaster - 准备APK构建"
    echo ✅ Git仓库初始化完成
) else (
    echo ✅ Git仓库已存在
)

echo.
echo 📋 当前状态检查:
git status

echo.
echo 🚀 准备推送到GitHub...
echo.
echo ⚠️  请确保您已创建GitHub仓库！
echo 📝 仓库信息格式：https://github.com/您的用户名/wordmaster.git
echo.
echo 🔧 请修改下面的命令中的"您的用户名"为实际的GitHub用户名
echo.

set /p github_user="请输入您的GitHub用户名: "

if "%github_user%"=="" (
    echo ❌ GitHub用户名不能为空
    pause
    exit /b 1
)

set remote_url=https://github.com/%github_user%/wordmaster.git

echo.
echo 🔗 添加远程仓库: %remote_url%
git remote add origin %remote_url%

echo.
echo 🏷️  设置主分支
git branch -M main

echo.
echo 📤 推送代码到GitHub...
git push -u origin main

echo.
echo ==========================================
echo ✅ 推送完成！
echo.
echo 🎯 下一步：
echo 1. 访问 https://github.com/%github_user%/wordmaster
echo 2. 进入 Actions 页面
echo 3. 启用 "Build Android APK" 工作流
echo 4. 点击 "Run workflow" 开始构建APK
echo ==========================================
pause