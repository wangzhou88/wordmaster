@echo off
chcp 65001
echo ==========================================
echo    WordMaster Git 推送脚本
echo ==========================================
echo.

REM 检查Git是否已安装
where git >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ Git未安装！
    echo 请先安装Git：https://git-scm.com/download/win
    pause
    exit /b 1
)

echo ✅ Git已安装

echo.

REM 检查是否已初始化Git
if not exist ".git" (
    echo 🔧 初始化Git仓库...
    git init
    if %errorlevel% neq 0 (
        echo ❌ Git初始化失败！
        pause
        exit /b 1
    )
    
    echo 🔧 添加所有文件...
    git add .
    if %errorlevel% neq 0 (
        echo ❌ 文件添加失败！
        pause
        exit /b 1
    )
    
    echo 🔧 创建提交...
    git commit -m "WordMaster - 准备APK构建"
    if %errorlevel% neq 0 (
        echo ❌ 提交创建失败！
        echo 提示：如果进入Vim编辑器，按ESC然后输入 :wq 保存
        pause
        exit /b 1
    )
    
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
echo 📝 仓库地址：https://github.com/wangzhou88/wordmaster.git
echo.

REM 设置GitHub用户名和仓库地址
set github_user=wangzhou88
set remote_url=https://github.com/wangzhou88/wordmaster.git

echo 🔧 GitHub用户名：%github_user%
echo 🔗 仓库地址：%remote_url%
echo.

REM 检查远程origin是否已存在
set remote_exists=false
for /f "tokens=2" %%i in ('git remote -v ^| findstr "origin" ^| findstr "push"') do (
    set remote_exists=true
    set current_remote=%%i
)

if %remote_exists% equ true (
    echo ⚠️  远程仓库origin已存在，当前地址：%current_remote%
    if "%current_remote%" neq "%remote_url%" (
        echo 🔄 更新远程仓库地址...
        git remote set-url origin %remote_url%
        if %errorlevel% neq 0 (
            echo ❌ 远程地址更新失败！
            pause
            exit /b 1
        )
        echo ✅ 远程仓库地址已更新
    ) else (
        echo ✅ 远程仓库地址已正确配置
    )
) else (
    echo 🔧 添加远程仓库...
    git remote add origin %remote_url%
    if %errorlevel% neq 0 (
        echo ❌ 远程仓库添加失败！
        pause
        exit /b 1
    )
    echo ✅ 远程仓库添加完成
)

echo.
echo 🏷️  设置主分支...
git branch -M main
if %errorlevel% neq 0 (
    echo ❌ 分支设置失败！
    pause
    exit /b 1
)
echo ✅ 主分支设置完成

echo.
echo 📤 推送代码到GitHub...
echo ⚠️  推送过程中可能需要输入GitHub凭据！
echo 用户名：%github_user%
echo 密码：GitHub密码或个人访问令牌

REM 执行推送
git push -u origin main
if %errorlevel% neq 0 (
    echo.
    echo ❌ 推送失败！
    echo.
    echo 📋 常见错误解决方案：
    echo 1. 认证失败：检查GitHub用户名和密码是否正确
    echo 2. 仓库不存在：先在GitHub创建仓库
    echo 3. 权限错误：确保有仓库推送权限
    echo 4. 网络问题：检查网络连接
    echo.
    echo 🆘 紧急备用方案：
    echo - 使用命令行手动推送
    echo - 使用GitHub Desktop
    pause
    exit /b 1
)

echo.
echo ✅ 推送成功！
echo.
echo ==========================================
echo 🎯 下一步：
echo 1. 访问 https://github.com/%github_user%/wordmaster
echo 2. 进入 Actions 页面
echo 3. 启用 "Build Android APK" 工作流
echo 4. 点击 "Run workflow" 开始构建APK
echo ==========================================
pause