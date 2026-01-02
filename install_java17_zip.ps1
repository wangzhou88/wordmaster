Write-Host "Installing OpenJDK 17 from zip archive..."

# 创建Java安装目录
$javaDir = "C:\Java"
if (!(Test-Path $javaDir)) {
    New-Item -ItemType Directory -Path $javaDir -Force
    Write-Host "Created Java directory: $javaDir"
}

# OpenJDK 17 zip下载链接 (Temurin)
$jdkUrl = "https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17.0.9%2B9/OpenJDK17U-jdk_x64_windows_hotspot_17.0.9_9.zip"
$jdkZip = "$javaDir\openjdk-17.zip"

Write-Host "Downloading OpenJDK 17..."
try {
    Write-Host "Download URL: $jdkUrl"
    $webClient = New-Object System.Net.WebClient
    $webClient.Headers.Add("User-Agent", "Mozilla/5.0")
    $webClient.DownloadFile($jdkUrl, $jdkZip)
    
    if (Test-Path $jdkZip) {
        $fileSize = (Get-Item $jdkZip).Length
        Write-Host "Download completed! File size: $([math]::Round($fileSize/1MB, 2)) MB"
        
        Write-Host "Extracting OpenJDK 17..."
        try {
            Expand-Archive -Path $jdkZip -DestinationPath $javaDir -Force
            Write-Host "Extraction completed!"
            
            # 查找解压后的目录
            $extractedDirs = Get-ChildItem -Path $javaDir -Directory | Where-Object { $_.Name -like "jdk-*" }
            if ($extractedDirs) {
                $jdkDir = $extractedDirs[0].FullName
                Write-Host "JDK extracted to: $jdkDir"
                
                # 设置JAVA_HOME环境变量
                [Environment]::SetEnvironmentVariable("JAVA_HOME", $jdkDir, "User")
                
                # 更新PATH
                $currentPath = [Environment]::GetEnvironmentVariable("PATH", "User")
                $javaBinPath = "$jdkDir\bin"
                
                if ($currentPath -notlike "*$javaBinPath*") {
                    $newPath = "$currentPath;$javaBinPath"
                    [Environment]::SetEnvironmentVariable("PATH", $newPath, "User")
                    Write-Host "Environment variables updated!"
                }
                
                # 验证安装
                Write-Host "`nVerifying installation..."
                & "$javaBinPath\java.exe" -version
                
            } else {
                Write-Host "Could not find extracted JDK directory"
            }
            
        } catch {
            Write-Host "Extraction failed: $($_.Exception.Message)"
        }
        
    } else {
        Write-Host "Download failed - file not created"
    }
} catch {
    Write-Host "Download failed: $($_.Exception.Message)"
    Write-Host "Trying alternative mirror..."
    
    # 尝试华为镜像
    $altUrl = "https://repo.huaweicloud.com/java/jdk/17.0.9+9/jdk-17.0.9+9_windows-x64_bin.zip"
    try {
        Write-Host "Trying Huawei mirror..."
        $webClient.DownloadFile($altUrl, $jdkZip)
        Write-Host "Downloaded from Huawei mirror"
        
        if (Test-Path $jdkZip) {
            Expand-Archive -Path $jdkZip -DestinationPath $javaDir -Force
            Write-Host "Extraction completed!"
        }
    } catch {
        Write-Host "Alternative download failed: $($_.Exception.Message)"
    }
}