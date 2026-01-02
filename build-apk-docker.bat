@echo off
chcp 65001 >nul
title WordMaster Docker APK构建器

echo.
echo ===============================================
echo         🐳 WordMaster Docker APK构建器
echo ===============================================
echo.

:: 检查Docker是否安装
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 错误: Docker未安装或未在PATH中
    echo.
    echo 请按照以下步骤安装Docker Desktop:
    echo 1. 访问 https://www.docker.com/products/docker-desktop
    echo 2. 下载并安装Docker Desktop for Windows
    echo 3. 重启计算机
    echo 4. 启动Docker Desktop并等待初始化完成
    echo.
    echo 或者查看 DOCKER_SETUP_GUIDE.md 获取详细说明
    echo.
    pause
    exit /b 1
)

:: 检查Docker服务是否运行
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 错误: Docker服务未运行
    echo.
    echo 请确保:
    echo 1. Docker Desktop正在运行
    echo 2. Docker服务已启动
    echo.
    pause
    exit /b 1
)

echo ✅ Docker环境检查通过
echo.

:: 设置变量
set PROJECT_NAME=wordmaster
set PACKAGE_NAME=com.wordmaster.app
set DOCKER_IMAGE=python:3.11-slim
set PROJECT_PATH=%cd%

echo 📁 项目路径: %PROJECT_PATH%
echo 📦 项目名称: %PROJECT_NAME%
echo 📱 包名: %PACKAGE_NAME%
echo 🐳 Docker镜像: %DOCKER_IMAGE%
echo.

:: 检查项目文件
if not exist "main.py" (
    echo ❌ 错误: 未找到main.py文件
    echo 请确保在WordMaster项目根目录中运行此脚本
    pause
    exit /b 1
)

if not exist "buildozer.spec" (
    echo ⚠️  警告: 未找到buildozer.spec文件
    echo 将使用默认构建参数
)

echo 🚀 开始Docker APK构建...
echo 这可能需要几分钟时间，请耐心等待...
echo.

:: 运行Docker构建容器
docker run --rm ^
  -v "%PROJECT_PATH%:/app" ^
  -w /app ^
  %DOCKER_IMAGE% ^
  bash -c "
    echo '📦 正在安装系统依赖...'
    apt-get update && apt-get install -y openjdk-11-jdk git wget unzip
    
    echo '☕ 配置Java环境...'
    export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
    export ANDROID_HOME=/opt/android-sdk
    export PATH=\$PATH:\$ANDROID_HOME/cmdline-tools/latest/bin:\$ANDROID_HOME/platform-tools
    
    echo '📱 设置Android SDK...'
    mkdir -p \$ANDROID_HOME
    
    echo '⬇️  下载Android命令行工具...'
    cd /tmp
    wget -q https://dl.google.com/android/repository/commandlinetools-win-11076708_latest.zip
    unzip -q commandlinetools-win-11076708_latest.zip
    
    echo '📁 配置SDK目录结构...'
    mkdir -p \$ANDROID_HOME/cmdline-tools
    mv cmdline-tools \$ANDROID_HOME/cmdline-tools/latest
    rm commandlinetools-win-11076708_latest.zip
    
    echo '✅ 接受Android SDK许可证...'
    yes | \$ANDROID_HOME/cmdline-tools/latest/bin/sdkmanager --licenses
    
    echo '🔧 安装Android SDK组件...'
    \$ANDROID_HOME/cmdline-tools/latest/bin/sdkmanager \
      'platform-tools' \
      'platforms;android-31' \
      'build-tools;31.0.0' \
      'system-images;android-31;google_apis;x86_64'
    
    echo '🐍 升级Python工具...'
    pip install --upgrade setuptools wheel
    
    echo '⚡ 安装python-for-android...'
    pip install python-for-android
    
    echo '🔨 开始构建APK...'
    p4a apk --private /app --name %PROJECT_NAME% --package %PACKAGE_NAME% --android-api 31
    
    echo '✅ 构建完成！'
    ls -la bin/
  "

:: 检查构建结果
if %errorlevel% equ 0 (
    echo.
    echo ===============================================
    echo               🎉 构建成功！
    echo ===============================================
    echo.
    echo 📁 APK文件位置:
    dir bin\*.apk /b 2>nul
    if %errorlevel% equ 0 (
        echo ✅ APK文件已生成在 bin\ 目录中
    ) else (
        echo ⚠️  警告: 未找到APK文件
    )
    echo.
    echo 📋 后续步骤:
    echo 1. 检查 bin\ 目录中的APK文件
    echo 2. 将APK文件传输到Android设备
    echo 3. 在设备上安装APK（需要启用"未知来源"）
    echo.
) else (
    echo.
    echo ===============================================
    echo               ❌ 构建失败！
    echo ===============================================
    echo.
    echo 请检查:
    echo 1. 网络连接是否正常
    echo 2. 磁盘空间是否充足
    echo 3. Docker是否正常运行
    echo 4. 项目文件是否完整
    echo.
    echo 如需帮助，请查看:
    echo - DOCKER_SETUP_GUIDE.md
    echo - ANDROID_ENVIRONMENT_SETUP_COMPLETE.md
    echo.
)

echo 按任意键退出...
pause >nul