@echo off
REM Simple Git Push Script for WordMaster
REM Version 1.0 - Fixed encoding issues

REM Check if Git is installed
where git >nul 2>nul
if %errorlevel% neq 0 (
    echo ERROR: Git is not installed!
    echo Please download Git from https://git-scm.com/download/win
    pause
    exit /b 1
)

echo Git is installed.

REM Initialize Git if needed
if not exist ".git" (
    echo Initializing Git repository...
    git init
    if %errorlevel% neq 0 (
        echo ERROR: Git init failed!
        pause
        exit /b 1
    )
    
    echo Adding all files...
    git add .
    if %errorlevel% neq 0 (
        echo ERROR: Git add failed!
        pause
        exit /b 1
    )
    
    echo Creating commit...
    git commit -m "WordMaster - Prepare APK build"
    if %errorlevel% neq 0 (
        echo ERROR: Git commit failed!
        echo TIP: If in Vim, press ESC then type :wq to save
        pause
        exit /b 1
    )
    
    echo Git repository initialized.
) else (
    echo Git repository already exists.
)

REM Set GitHub info
set GITHUB_USER=wangzhou88
set REPO_URL=https://github.com/wangzhou88/wordmaster.git

REM Check if remote origin exists
set REMOTE_EXISTS=false
for /f "tokens=2" %%i in ('git remote -v ^| findstr "origin" ^| findstr "push"') do (
    set REMOTE_EXISTS=true
    set CURRENT_REMOTE=%%i
)

if %REMOTE_EXISTS% equ true (
    echo Remote origin exists.
    if "%CURRENT_REMOTE%" neq "%REPO_URL%" (
        echo Updating remote URL...
        git remote set-url origin %REPO_URL%
        if %errorlevel% neq 0 (
            echo ERROR: Remote URL update failed!
            pause
            exit /b 1
        )
        echo Remote URL updated.
    )
) else (
    echo Adding remote repository...
    git remote add origin %REPO_URL%
    if %errorlevel% neq 0 (
        echo ERROR: Remote add failed!
        pause
        exit /b 1
    )
    echo Remote repository added.
)

REM Set main branch
echo Setting main branch...
git branch -M main
if %errorlevel% neq 0 (
    echo ERROR: Branch set failed!
    pause
    exit /b 1
)
echo Main branch set.

REM Push to GitHub
echo Pushing to GitHub...
echo Username: %GITHUB_USER%
echo Repo: %REPO_URL%
git push -u origin main
if %errorlevel% neq 0 (
    echo ERROR: Push failed!
    echo Solutions:
    echo 1. Check GitHub credentials
    echo 2. Ensure repo exists on GitHub
    echo 3. Check network connection
    echo 4. Try manual push
    pause
    exit /b 1
)

echo Push successful!
echo Next steps:
echo 1. Visit: https://github.com/%GITHUB_USER%/wordmaster
echo 2. Go to Actions tab
echo 3. Enable "Build Android APK" workflow
echo 4. Click "Run workflow"
pause