@echo off
title GitHub One-Click Team Project Upload
echo =======================================================================
echo   India Nutrient Deficiency & Hidden Hunger Analytics Team Uploader
echo =======================================================================
echo.
echo Step 1: Create a new empty repository on your GitHub:
echo         1. Open https://github.com/new
echo         2. Name it: india-nutrient-deficiency-analytics
echo         3. Make it PUBLIC
echo         4. Leave README, .gitignore, license UNCHECKED
echo         5. Click "Create repository"
echo.
set /p REPO_URL="Enter your new GitHub repository URL (e.g. https://github.com/YOUR_USERNAME/india-nutrient-deficiency-analytics.git): "

if "%REPO_URL%"=="" (
    echo [ERROR] No URL provided. Exiting.
    pause
    exit /b
)

echo.
echo Initializing Git repository...
if exist .git (
    echo Cleaning existing local git cache...
    rmdir /s /q .git
)

git init
git checkout -b main
git add .
git commit -m "Initial release: India Nutrient Deficiency & Hidden Hunger Paradox Analytics"
git remote add origin %REPO_URL%

echo.
echo Pushing to your GitHub repository...
git push -u origin main

if %ERRORLEVEL% equ 0 (
    echo.
    echo =======================================================================
    echo [SUCCESS] Your project has been uploaded to your GitHub!
    echo.
    echo Next: Enable GitHub Pages to make your website live!
    echo   1. Go to your repo on GitHub: Settings -> Pages
    echo   2. Under "Build and deployment" -> Source: Deploy from a branch
    echo   3. Select Branch: "main", Folder: "/ (root)"
    echo   4. Click Save!
    echo =======================================================================
) else (
    echo.
    echo [NOTE] Push failed. Make sure you are signed into Git or have access to the repository.
)

echo.
pause
