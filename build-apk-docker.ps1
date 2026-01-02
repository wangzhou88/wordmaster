# WordMaster Docker APK构建脚本 (PowerShell版本)
# 需要以管理员权限运行

param(
    [switch]$Clean,
    [switch]$Help
)

# 设置控制台编码
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

function Show-Help {
    Write-Host @"
🐳 WordMaster Docker APK构建器 (PowerShell版本)

用法:
  .\build-apk-docker.ps1 [选项]

选项:
  -Clean     清理之前的构建文件
  -Help      显示此帮助信息

示例:
  .\build-apk-docker.ps1          # 标准构建
  .\build-apk-docker.ps1 -Clean   # 清理后构建

要求:
  - Docker Desktop已安装并运行
  - 项目根目录包含main.py和buildozer.spec
  - 网络连接正常（用于下载依赖）

"@
}

function Test-DockerEnvironment {
    Write-Host "🔍 检查Docker环境..." -ForegroundColor Cyan
    
    # 检查Docker是否安装
    try {
        $dockerVersion = docker --version
        Write-Host "✅ Docker已安装: $dockerVersion" -ForegroundColor Green
    }
    catch {
        Write-Host "❌ 错误: Docker未安装" -ForegroundColor Red
        Write-Host "请访问 https://www.docker.com/products/docker-desktop 下载安装" -ForegroundColor Yellow
        return $false
    }
    
    # 检查Docker服务是否运行
    try {
        docker info | Out-Null
        Write-Host "✅ Docker服务运行正常" -ForegroundColor Green
    }
    catch {
        Write-Host "❌ 错误: Docker服务未运行" -ForegroundColor Red
        Write-Host "请启动Docker Desktop并等待初始化完成" -ForegroundColor Yellow
        return $false
    }
    
    return $true
}

function Test-ProjectFiles {
    Write-Host "📁 检查项目文件..." -ForegroundColor Cyan
    
    # 检查必需文件
    if (-not (Test-Path "main.py")) {
        Write-Host "❌ 错误: 未找到main.py文件" -ForegroundColor Red
        Write-Host "请确保在WordMaster项目根目录中运行此脚本" -ForegroundColor Yellow
        return $false
    }
    
    if (-not (Test-Path "buildozer.spec")) {
        Write-Host "⚠️  警告: 未找到buildozer.spec文件" -ForegroundColor Yellow
        Write-Host "将使用默认构建参数" -ForegroundColor Yellow
    }
    
    Write-Host "✅ 项目文件检查通过" -ForegroundColor Green
    return $true
}

function Clear-BuildFiles {
    Write-Host "🧹 清理构建文件..." -ForegroundColor Cyan
    
    $cleanupPaths = @(
        "bin",
        "build",
        "dist",
        ".android",
        "*.pyc",
        "__pycache__"
    )
    
    foreach ($path in $cleanupPaths) {
        if (Test-Path $path) {
            try {
                Remove-Item $path -Recurse -Force -ErrorAction SilentlyContinue
                Write-Host "  ✅ 已清理: $path" -ForegroundColor Green
            }
            catch {
                Write-Host "  ⚠️  无法清理: $path" -ForegroundColor Yellow
            }
        }
    }
}

function Build-APK {
    param(
        [string]$ProjectName = "wordmaster",
        [string]$PackageName = "com.wordmaster.app",
        [string]$DockerImage = "python:3.11-slim"
    )
    
    Write-Host "🚀 开始Docker APK构建..." -ForegroundColor Cyan
    Write-Host "这可能需要10-30分钟，请耐心等待..." -ForegroundColor Yellow
    Write-Host ""
    
    # 设置构建参数
    $buildParams = @(
        "docker", "run", "--rm",
        "-v", "$(Resolve-Path .):/app",
        "-w", "/app",
        $DockerImage,
        "bash", "-c", @"

echo '📦 正在安装系统依赖...'
export DEBIAN_FRONTEND=noninteractive
apt-get update && apt-get install -y openjdk-11-jdk git wget unzip curl

echo '☕ 配置Java环境...'
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
export ANDROID_HOME=/opt/android-sdk
export PATH=`$PATH:`$ANDROID_HOME/cmdline-tools/latest/bin:`$ANDROID_HOME/platform-tools

echo '📱 设置Android SDK...'
mkdir -p `$ANDROID_HOME

echo '⬇️  下载Android命令行工具...'
cd /tmp
wget -q https://dl.google.com/android/repository/commandlinetools-win-11076708_latest.zip
unzip -q commandlinetools-win-11076708_latest.zip

echo '📁 配置SDK目录结构...'
mkdir -p `$ANDROID_HOME/cmdline-tools
mv cmdline-tools `$ANDROID_HOME/cmdline-tools/latest
rm commandlinetools-win-11076708_latest.zip

echo '✅ 接受Android SDK许可证...'
yes | `$ANDROID_HOME/cmdline-tools/latest/bin/sdkmanager --licenses

echo '🔧 安装Android SDK组件...'
`$ANDROID_HOME/cmdline-tools/latest/bin/sdkmanager `
  'platform-tools' `
  'platforms;android-31' `
  'build-tools;31.0.0'

echo '🐍 升级Python工具...'
pip install --upgrade setuptools wheel

echo '⚡ 安装python-for-android...'
pip install python-for-android

echo '🔨 开始构建APK...'
p4a apk --private /app --name $ProjectName --package $PackageName --android-api 31

echo '✅ 构建完成！'
ls -la bin/ 2>/dev/null || echo 'APK生成完成，请检查bin目录'

"@)
    
    try {
        & @buildParams
        return $LASTEXITCODE -eq 0
    }
    catch {
        Write-Host "❌ 构建过程中出现错误" -ForegroundColor Red
        return $false
    }
}

function Show-BuildResult {
    param([bool]$Success)
    
    Write-Host ""
    Write-Host "===============================================" -ForegroundColor Cyan
    if ($Success) {
        Write-Host "               🎉 构建成功！" -ForegroundColor Green
        Write-Host "===============================================" -ForegroundColor Green
        Write-Host ""
        Write-Host "📁 APK文件位置:" -ForegroundColor Cyan
        
        $apkFiles = Get-ChildItem -Path "bin" -Filter "*.apk" -ErrorAction SilentlyContinue
        if ($apkFiles) {
            foreach ($apk in $apkFiles) {
                $size = [math]::Round($apk.Length / 1MB, 2)
                Write-Host "  ✅ $($apk.Name) ($size MB)" -ForegroundColor Green
            }
        } else {
            Write-Host "  ⚠️  未在bin目录找到APK文件" -ForegroundColor Yellow
        }
        
        Write-Host ""
        Write-Host "📋 后续步骤:" -ForegroundColor Cyan
        Write-Host "1. 检查 bin\ 目录中的APK文件" -ForegroundColor White
        Write-Host "2. 将APK文件传输到Android设备" -ForegroundColor White
        Write-Host "3. 在设备上安装APK（需要启用"未知来源"）" -ForegroundColor White
    } else {
        Write-Host "               ❌ 构建失败！" -ForegroundColor Red
        Write-Host "===============================================" -ForegroundColor Red
        Write-Host ""
        Write-Host "请检查:" -ForegroundColor Cyan
        Write-Host "1. 网络连接是否正常" -ForegroundColor White
        Write-Host "2. 磁盘空间是否充足" -ForegroundColor White
        Write-Host "3. Docker是否正常运行" -ForegroundColor White
        Write-Host "4. 项目文件是否完整" -ForegroundColor White
        Write-Host ""
        Write-Host "如需帮助，请查看:" -ForegroundColor Cyan
        Write-Host "- DOCKER_SETUP_GUIDE.md" -ForegroundColor White
        Write-Host "- ANDROID_ENVIRONMENT_SETUP_COMPLETE.md" -ForegroundColor White
    }
}

# 主程序开始
Write-Host ""
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host "         🐳 WordMaster Docker APK构建器" -ForegroundColor Cyan
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host ""

# 处理参数
if ($Help) {
    Show-Help
    exit 0
}

if ($Clean) {
    Clear-BuildFiles
    Write-Host ""
}

# 执行检查
if (-not (Test-DockerEnvironment)) {
    Write-Host ""
    Write-Host "按任意键退出..." -ForegroundColor Gray
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 1
}

if (-not (Test-ProjectFiles)) {
    Write-Host ""
    Write-Host "按任意键退出..." -ForegroundColor Gray
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 1
}

# 执行构建
$success = Build-APK

# 显示结果
Show-BuildResult -Success $success

Write-Host ""
Write-Host "按任意键退出..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")