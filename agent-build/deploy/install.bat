@echo off
echo ========================================
echo   BS-EYE Agent Install
echo ========================================
echo.

:: Check administrator privileges
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Run as Administrator.
    echo Right-click and select Run as Administrator.
    pause
    exit /b 1
)

:: Create directory
if not exist "C:\bseye-agent" mkdir "C:\bseye-agent"
cd /d "C:\bseye-agent"

echo [1/3] Downloading installer...
powershell -Command "Invoke-WebRequest -Uri 'https://monitor.blueswell.co.kr/api/agent/download/bseye-installer.bat' -OutFile 'C:\bseye-agent\bseye-installer.bat'"

if not exist "C:\bseye-agent\bseye-installer.bat" (
    echo [ERROR] Download failed. Check internet connection.
    pause
    exit /b 1
)

echo [2/3] Starting installation...
call "C:\bseye-agent\bseye-installer.bat"

echo [3/3] Installation complete
pause
