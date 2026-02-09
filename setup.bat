@echo off
REM Slack TUI Setup for Windows

echo ============================================
echo   Slack TUI Setup
echo ============================================
echo.

REM Check Python
echo [1/3] Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found!
    echo Please install Python 3.11 or higher from python.org
    pause
    exit /b 1
)

python --version
echo.

REM Install dependencies
echo [2/3] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo.

REM Create config directory
echo [3/3] Creating config directory...
if not exist "%USERPROFILE%\.config\slack-tui-app" (
    mkdir "%USERPROFILE%\.config\slack-tui-app"
)
echo Config directory: %USERPROFILE%\.config\slack-tui-app
echo.

echo ============================================
echo   Setup Complete!
echo ============================================
echo.
echo Next steps:
echo 1. Get your Slack token from https://api.slack.com/apps
echo 2. Set environment variable:
echo    set SLACK_TUI_TOKEN=xoxp-your-token
echo.
echo 3. Run the app:
echo    python slack-tui.py --channels
echo.
pause
