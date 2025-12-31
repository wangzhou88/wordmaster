# GitHub Actions Build Status Checker
# Created to monitor WordMaster APK build progress

Write-Host "=== WordMaster GitHub Actions Build Status ===" -ForegroundColor Green
Write-Host "Repository: https://github.com/wangzhou88/wordmaster" -ForegroundColor Yellow
Write-Host "Build Target: Android APK" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Green

# Navigate to project directory
Set-Location "C:\Users\admin\Downloads\wordmaster"

# Show recent commits
Write-Host "`nRecent commits:" -ForegroundColor Cyan
git log --oneline -n 5

# Show git status
Write-Host "`nCurrent git status:" -ForegroundColor Cyan
git status --porcelain

# Check for any generated artifacts locally
Write-Host "`nChecking for local build artifacts:" -ForegroundColor Cyan
if (Test-Path "*.apk") {
    Write-Host "Found APK files:" -ForegroundColor Green
    Get-ChildItem *.apk | ForEach-Object {
        Write-Host "  - $($_.Name) ($([math]::Round($_.Length/1MB, 2)) MB)" -ForegroundColor Green
    }
} else {
    Write-Host "No local APK files found." -ForegroundColor Yellow
}

# Check if GitHub Actions workflow file exists
Write-Host "`nGitHub Actions workflow status:" -ForegroundColor Cyan
if (Test-Path ".github/workflows/build-android.yml") {
    Write-Host "Build workflow file exists: .github/workflows/build-android.yml" -ForegroundColor Green
} else {
    Write-Host "Build workflow file not found!" -ForegroundColor Red
}

# Show the URL to check GitHub Actions manually
Write-Host "`nTo check build status manually:" -ForegroundColor Yellow
Write-Host "1. Open browser and go to: https://github.com/wangzhou88/wordmaster/actions" -ForegroundColor White
Write-Host "2. Click on the latest workflow run" -ForegroundColor White
Write-Host "3. Wait for the build to complete" -ForegroundColor White
Write-Host "4. Download the APK from the 'Artifacts' section" -ForegroundColor White

Write-Host "`nBuild monitoring script completed." -ForegroundColor Green