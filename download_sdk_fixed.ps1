Write-Host "Creating Android SDK directory..."
$androidDir = "C:\Android"

if (!(Test-Path $androidDir)) {
    New-Item -ItemType Directory -Path $androidDir -Force
    Write-Host "Created directory: $androidDir"
} else {
    Write-Host "Directory already exists: $androidDir"
}

Write-Host "Downloading Android SDK command line tools..."
$url = "https://dl.google.com/android/repository/commandlinetools-win-11076708_latest.zip"
$output = "C:\Android\cmdline-tools.zip"

Write-Host "Download URL: $url"
Write-Host "Output file: $output"

try {
    Write-Host "Starting download..."
    $webClient = New-Object System.Net.WebClient
    $webClient.Headers.Add("User-Agent", "Mozilla/5.0")
    $webClient.DownloadFile($url, $output)
    
    if (Test-Path $output) {
        $fileSize = (Get-Item $output).Length
        Write-Host "Download completed! File size: $([math]::Round($fileSize/1MB, 2)) MB"
    } else {
        Write-Host "Download failed - file not created"
    }
} catch {
    Write-Host "Download failed: $($_.Exception.Message)"
}