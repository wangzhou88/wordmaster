Write-Host "Installing OpenJDK 17..."

# 创建Java安装目录
$javaDir = "C:\Java"
if (!(Test-Path $javaDir)) {
    New-Item -ItemType Directory -Path $javaDir -Force
    Write-Host "Created Java directory: $javaDir"
}

# OpenJDK 17下载链接 (Microsoft的构建版本)
$jdkUrl = "https://download.microsoft.com/download/6/e/0/6e04587b-100c-4c5b-bb90-1c73e8c6e6e1/microsoft-jdk-17.0.9.9-windows-x64.msi"
$jdkInstaller = "$javaDir\openjdk-17.msi"

Write-Host "Downloading OpenJDK 17..."
try {
    $webClient = New-Object System.Net.WebClient
    $webClient.Headers.Add("User-Agent", "Mozilla/5.0")
    $webClient.DownloadFile($jdkUrl, $jdkInstaller)
    
    if (Test-Path $jdkInstaller) {
        $fileSize = (Get-Item $jdkInstaller).Length
        Write-Host "Download completed! File size: $([math]::Round($fileSize/1MB, 2)) MB"
        
        Write-Host "Installing OpenJDK 17..."
        # 安装MSI包 (静默安装)
        $process = Start-Process -FilePath "msiexec.exe" -ArgumentList "/i", "`"$jdkInstaller`"", "/quiet", "INSTALLDIR=C:\Java\jdk-17" -Wait -PassThru
        
        if ($process.ExitCode -eq 0) {
            Write-Host "OpenJDK 17 installed successfully!"
            
            # 设置JAVA_HOME环境变量
            $javaHome = "C:\Java\jdk-17"
            [Environment]::SetEnvironmentVariable("JAVA_HOME", $javaHome, "User")
            
            # 更新PATH
            $currentPath = [Environment]::GetEnvironmentVariable("PATH", "User")
            $javaBinPath = "$javaHome\bin"
            
            if ($currentPath -notlike "*$javaBinPath*") {
                $newPath = "$currentPath;$javaBinPath"
                [Environment]::SetEnvironmentVariable("PATH", $newPath, "User")
                Write-Host "Environment variables updated!"
            }
            
            # 验证安装
            Write-Host "`nVerifying installation..."
            & "$javaHome\bin\java.exe" -version
            
        } else {
            Write-Host "Installation failed with exit code: $($process.ExitCode)"
        }
        
    } else {
        Write-Host "Download failed - file not created"
    }
} catch {
    Write-Host "Error: $($_.Exception.Message)"
    Write-Host "Trying alternative download method..."
    
    # 尝试使用其他下载源
    $altUrl = "https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17.0.9%2B9/OpenJDK17U-jdk_x64_windows_hotspot_17.0.9_9.msi"
    try {
        $webClient.DownloadFile($altUrl, $jdkInstaller)
        Write-Host "Downloaded from alternative source"
    } catch {
        Write-Host "Alternative download also failed: $($_.Exception.Message)"
    }
}