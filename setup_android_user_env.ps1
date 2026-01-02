Write-Host "Setting up Android SDK with user-level environment variables..."

# 设置用户级环境变量
$androidDir = "C:\Android"
$androidHomePath = $androidDir

Write-Host "Setting user-level ANDROID_HOME..."
[Environment]::SetEnvironmentVariable("ANDROID_HOME", $androidHomePath, "User")

# 设置工具路径
$androidToolsPath = "$androidHomePath\cmdline-tools\latest\bin"
$androidPlatformToolsPath = "$androidHomePath\platform-tools"

# 获取当前用户PATH
$currentPath = [Environment]::GetEnvironmentVariable("PATH", "User")

# 检查并添加Android工具路径
$pathsToAdd = @($androidToolsPath, $androidPlatformToolsPath)
$newPath = $currentPath

foreach ($path in $pathsToAdd) {
    if ($currentPath -notlike "*$path*") {
        $newPath = "$newPath;$path"
        Write-Host "Added to PATH: $path"
    }
}

if ($newPath -ne $currentPath) {
    [Environment]::SetEnvironmentVariable("PATH", $newPath, "User")
    Write-Host "User PATH updated successfully!"
} else {
    Write-Host "Android tools already in PATH"
}

# 验证设置
Write-Host "`nEnvironment verification:"
Write-Host "ANDROID_HOME: $([Environment]::GetEnvironmentVariable('ANDROID_HOME', 'User'))"

# 测试Android SDK工具
Write-Host "`nTesting Android SDK tools..."
$testCmd = "sdkmanager --version"
Write-Host "Running: $testCmd"

try {
    $result = & cmd.exe /c "$env:ANDROID_HOME\cmdline-tools\latest\bin\sdkmanager.bat --version"
    Write-Host "SDK Manager version: $result"
} catch {
    Write-Host "Error testing sdkmanager: $($_.Exception.Message)"
}

Write-Host "`nSetup completed! Please restart your terminal or log out/in for environment changes to take effect."