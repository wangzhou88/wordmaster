# Android SDK下载和配置脚本
Write-Host "正在下载Android SDK命令行工具..." -ForegroundColor Green

# 创建Android SDK目录
$androidDir = "C:\Android"
if (!(Test-Path $androidDir)) {
    New-Item -ItemType Directory -Path $androidDir -Force
}

# Android命令行工具下载链接
$cmdlineToolsUrl = "https://dl.google.com/android/repository/commandlinetools-win-11076708_latest.zip"
$cmdlineToolsZip = "$androidDir\cmdline-tools.zip"

try {
    Write-Host "尝试从官方源下载..." -ForegroundColor Yellow
    
    # 使用WebClient下载
    $webClient = New-Object System.Net.WebClient
    $webClient.Headers.Add("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    $webClient.DownloadFile($cmdlineToolsUrl, $cmdlineToolsZip)
    
    if (Test-Path $cmdlineToolsZip) {
        $fileSize = (Get-Item $cmdlineToolsZip).Length
        if ($fileSize -gt 1000000) {  # 大于1MB
            Write-Host "下载成功！文件大小: $([math]::Round($fileSize/1MB, 2)) MB" -ForegroundColor Green
            
            # 解压文件
            Write-Host "正在解压Android SDK命令行工具..." -ForegroundColor Green
            
            # 创建cmdline-tools目录
            $cmdlineToolsDir = "$androidDir\cmdline-tools"
            if (!(Test-Path $cmdlineToolsDir)) {
                New-Item -ItemType Directory -Path $cmdlineToolsDir -Force
            }
            
            # 使用PowerShell展开压缩文件
            Expand-Archive -Path $cmdlineToolsZip -DestinationPath $cmdlineToolsDir -Force
            
            # 移动cmdline-tools到正确位置
            $extractedDir = "$cmdlineToolsDir\cmdline-tools"
            if (Test-Path $extractedDir) {
                Get-ChildItem -Path $extractedDir -Recurse | Move-Item -Destination $cmdlineToolsDir
                Remove-Item -Path $extractedDir -Recurse -Force
            }
            
            Write-Host "Android SDK命令行工具解压完成！" -ForegroundColor Green
            Write-Host "安装路径: $cmdlineToolsDir" -ForegroundColor Cyan
            
            # 设置环境变量提示
            Write-Host "`n请设置以下环境变量:" -ForegroundColor Yellow
            Write-Host "ANDROID_HOME = $androidDir" -ForegroundColor Cyan
            Write-Host "PATH += $androidDir\cmdline-tools\latest\bin;$androidDir\platform-tools" -ForegroundColor Cyan
            
        } else {
            Write-Host "下载的文件太小，可能下载失败" -ForegroundColor Red
        }
    } else {
        Write-Host "下载文件不存在" -ForegroundColor Red
    }
} catch {
    Write-Host "下载失败: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "请检查网络连接或手动下载Android SDK命令行工具" -ForegroundColor Yellow
}