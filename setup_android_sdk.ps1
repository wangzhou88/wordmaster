Write-Host "Setting up Android SDK environment..."

# 解压cmdline-tools
$androidDir = "C:\Android"
$zipFile = "$androidDir\cmdline-tools.zip"
$extractPath = "$androidDir\cmdline-tools"

Write-Host "Extracting Android SDK command line tools..."
if (Test-Path $zipFile) {
    try {
        Expand-Archive -Path $zipFile -DestinationPath $androidDir -Force
        Write-Host "Extraction completed!"
    } catch {
        Write-Host "Extraction failed: $($_.Exception.Message)"
        exit 1
    }
} else {
    Write-Host "Zip file not found: $zipFile"
    exit 1
}

# 检查提取的内容
Write-Host "Checking extracted contents:"
Get-ChildItem -Path $extractPath -Recurse

# 设置环境变量
Write-Host "Setting up environment variables..."

# 设置ANDROID_HOME
$androidHomePath = $androidDir
[Environment]::SetEnvironmentVariable("ANDROID_HOME", $androidHomePath, "Machine")

# 将Android SDK工具添加到PATH
$androidToolsPath = "$androidHomePath\cmdline-tools\latest\bin"
$androidPlatformToolsPath = "$androidHomePath\platform-tools"

# 获取当前PATH
$currentPath = [Environment]::GetEnvironmentVariable("PATH", "Machine")

# 检查是否已经添加，避免重复
if ($currentPath -notlike "*$androidToolsPath*") {
    $newPath = "$currentPath;$androidToolsPath;$androidPlatformToolsPath"
    [Environment]::SetEnvironmentVariable("PATH", $newPath, "Machine")
    Write-Host "Environment variables updated!"
} else {
    Write-Host "Environment variables already configured"
}

# 显示当前环境变量
Write-Host "Current ANDROID_HOME: $([Environment]::GetEnvironmentVariable('ANDROID_HOME', 'Machine'))"
Write-Host "PATH contains Android tools: $(if ($currentPath -like '*cmdline-tools*') {'Yes'} else {'No'})"

Write-Host "Android SDK setup completed!"