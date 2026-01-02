Write-Host "Building APK using GitHub Actions workflow configuration..."

# 清理之前的构建
Write-Host "Cleaning previous build..."
try {
    buildozer android clean
} catch {
    Write-Host "Clean failed or not needed"
}

# 设置环境变量（使用Java 11）
$env:ANDROID_HOME = "C:\Android"
$env:JAVA_HOME = (Get-Command java).Source.Replace("\bin\java.exe", "")
Write-Host "Set environment variables:"
Write-Host "ANDROID_HOME: $env:ANDROID_HOME"
Write-Host "JAVA_HOME: $env:JAVA_HOME"

# 验证环境
Write-Host "`nEnvironment verification:"
java -version
Write-Host "Buildozer version:"
buildozer --version

# 检查Android SDK
Write-Host "`nChecking Android SDK..."
$sdkManagerPath = "$env:ANDROID_HOME\cmdline-tools\latest\bin\sdkmanager.bat"
if (Test-Path $sdkManagerPath) {
    Write-Host "SDK Manager found"
    try {
        & $sdkManagerPath --version
    } catch {
        Write-Host "SDK Manager version check failed"
    }
} else {
    Write-Host "SDK Manager not found, will rely on buildozer to set up"
}

# 尝试使用buildozer初始化android target
Write-Host "`nInitializing android target..."
try {
    buildozer android init
    Write-Host "Android target initialized successfully"
} catch {
    Write-Host "Android init failed: $($_.Exception.Message)"
}

# 尝试构建debug APK
Write-Host "`nBuilding debug APK..."
try {
    Write-Host "Running: buildozer android debug"
    & buildozer android debug --verbose
} catch {
    Write-Host "Debug build failed: $($_.Exception.Message)"
    
    # 如果debug失败，尝试简单的buildozer build
    Write-Host "`nTrying simple buildozer command..."
    try {
        & buildozer android build
    } catch {
        Write-Host "Build also failed: $($_.Exception.Message)"
    }
}

# 检查构建结果
Write-Host "`nChecking build results..."
if (Test-Path "bin") {
    Write-Host "Found bin directory, contents:"
    Get-ChildItem "bin"
} else {
    Write-Host "No bin directory found"
}

# 查找APK文件
Write-Host "`nSearching for APK files..."
$apkFiles = Get-ChildItem -Recurse -Filter "*.apk" -ErrorAction SilentlyContinue
if ($apkFiles) {
    Write-Host "Found APK files:"
    foreach ($apk in $apkFiles) {
        Write-Host "📱 $($apk.FullName) - Size: $([math]::Round($apk.Length/1MB, 2)) MB"
    }
} else {
    Write-Host "No APK files found"
}