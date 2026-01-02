Write-Host "Building APK with buildozer..."

# 设置环境变量
$androidDir = "C:\Android"
$env:ANDROID_HOME = $androidDir
$env:JAVA_HOME = "C:\Program Files\Eclipse Adoptium\jdk-17.0.17.10-hotspot"

# 检查环境变量
Write-Host "ANDROID_HOME: $env:ANDROID_HOME"
Write-Host "JAVA_HOME: $env:JAVA_HOME"
Write-Host "Java version:"
java -version

# 检查Android SDK
Write-Host "`nChecking Android SDK..."
$sdkmanagerPath = "$androidDir\cmdline-tools\latest\bin\sdkmanager.bat"
if (Test-Path $sdkmanagerPath) {
    Write-Host "Found SDK Manager: $sdkmanagerPath"
    try {
        & $sdkmanagerPath --version
    } catch {
        Write-Host "SDK Manager version check failed, but continuing..."
    }
} else {
    Write-Host "SDK Manager not found, but buildozer might download it automatically"
}

# 尝试构建APK
Write-Host "`nStarting buildozer build process..."
try {
    Write-Host "Running: buildozer android debug"
    & buildozer android debug
    
} catch {
    Write-Host "Build failed with error: $($_.Exception.Message)"
    
    # 如果失败，尝试清理并重新构建
    Write-Host "`nTrying clean build..."
    try {
        & buildozer android clean
        Write-Host "Clean completed, retrying build..."
        & buildozer android debug
    } catch {
        Write-Host "Clean build also failed: $($_.Exception.Message)"
    }
}