Write-Host "正在创建Android SDK目录..."
$androidDir = "C:\Android"
if (!(Test-Path $androidDir)) {
    New-Item -ItemType Directory -Path $androidDir -Force
    Write-Host "创建目录: $androidDir"
}

Write-Host "正在下载Android SDK命令行工具..."
$url = "https://dl.google.com/android/repository/commandlinetools-win-11076708_latest.zip"
$output = "C:\Android\cmdline-tools.zip"

Write-Host "下载URL: $url"
Write-Host "输出文件: $output"

try {
    $webClient = New-Object System.Net.WebClient
    $webClient.Headers.Add("User-Agent", "Mozilla/5.0")
    $webClient.DownloadFile($url, $output)
    Write-Host "下载完成！"
} catch {
    Write-Host "下载失败: $($_.Exception.Message)"
}