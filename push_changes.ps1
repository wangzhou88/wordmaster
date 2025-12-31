# PowerShell Script to push Git changes
# Created to resolve GitHub Actions build issues

Write-Host "=== WordMaster Git Push Script ===" -ForegroundColor Green

# Navigate to project directory
Set-Location "C:\Users\admin\Downloads\wordmaster"

# Check git status
Write-Host "Checking Git status..." -ForegroundColor Yellow
git status

# Show recent commits
Write-Host "Recent commits:" -ForegroundColor Yellow
git log --oneline -n 3

# Try to push changes
Write-Host "Pushing changes to GitHub..." -ForegroundColor Yellow
git push origin main

# Check final status
Write-Host "Final Git status:" -ForegroundColor Yellow
git status

Write-Host "=== Script completed ===" -ForegroundColor Green