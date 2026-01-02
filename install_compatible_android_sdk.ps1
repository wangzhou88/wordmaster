Write-Host "Installing Java 11 compatible Android SDK..."

# 删除旧版本
$androidDir = "C:\Android"
$oldZip = "$androidDir\cmdline-tools.zip"

if (Test-Path $oldZip) {
    Remove-Item $oldZip -Force
    Write-Host "Removed old SDK zip file"
}

# 下载Java 11兼容的Android SDK版本
# 使用2022年的版本，应该与Java 11兼容
$compatibleSdkUrl = "https://dl.google.com/android/repository/commandlinetools-win-9477386_latest.zip"
$newZip = "$androidDir\cmdline-tools-compatible.zip"

Write-Host "Downloading Java 11 compatible Android SDK..."
try {
    $webClient = New-Object System.Net.WebClient
    $webClient.Headers.Add("User-Agent", "Mozilla/5.0")
    $webClient.DownloadFile($compatibleSdkUrl, $newZip)
    
    if (Test-Path $newZip) {
        $fileSize = (Get-Item $newZip).Length
        Write-Host "Download completed! File size: $([math]::Round($fileSize/1MB, 2)) MB"
        
        # 删除旧解压文件
        $oldToolsDir = "$androidDir\cmdline-tools"
        if (Test-Path $oldToolsDir) {
            Remove-Item $oldToolsDir -Recurse -Force
            Write-Host "Removed old SDK tools directory"
        }
        
        # 解压新版本
        Write-Host "Extracting compatible SDK..."
        Expand-Archive -Path $newZip -DestinationPath $androidDir -Force
        
        # 设置环境变量
        Write-Host "Setting environment variables..."
        [Environment]::SetEnvironmentVariable("ANDROID_HOME", $androidDir, "User")
        
        $currentPath = [Environment]::GetEnvironmentVariable("PATH", "User")
        $androidToolsPath = "$androidDir\cmdline-tools\latest\bin"
        $androidPlatformToolsPath = "$androidDir\platform-tools"
        
        $newPath = $currentPath
        if ($currentPath -notlike "*$androidToolsPath*") {
            $newPath = "$newPath;$androidToolsPath;$androidPlatformToolsPath"
            [Environment]::SetEnvironmentVariable("PATH", $newPath, "User")
        }
        
        # 测试SDK
        Write-Host "`nTesting Android SDK with Java 11..."
        $sdkmanagerPath = "$androidDir\cmdline-tools\latest\bin\sdkmanager.bat"
        
        if (Test-Path $sdkmanagerPath) {
            Write-Host "SDK Manager found at: $sdkmanagerPath"
            & $sdkmanagerPath --version
        } else {
            Write-Host "SDK Manager not found"
        }
        
    } else {
        Write-Host "Download failed"
    }
} catch {
    Write-Host "Error: $($_.Exception.Message)"
}