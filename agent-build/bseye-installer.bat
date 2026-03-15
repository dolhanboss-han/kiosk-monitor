@echo off
chcp 65001 >nul
title BS-EYE Agent Installer

echo ============================================
echo   BS-EYE Agent Installer
echo ============================================
echo.

:: 설정
set "INSTALL_DIR=C:\bseye-agent"
set "SERVER=https://monitor.blueswell.co.kr"
set "DOWNLOAD_BASE=%SERVER%/downloads/agent"

:: 설치 디렉토리 생성
echo [1/6] Creating install directory...
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"
if not exist "%INSTALL_DIR%\templates" mkdir "%INSTALL_DIR%\templates"

:: 파일 다운로드
echo [2/6] Downloading files...
echo   - bseye-agent.exe
powershell -Command "Invoke-WebRequest -Uri '%DOWNLOAD_BASE%/bseye-agent.exe' -OutFile '%INSTALL_DIR%\bseye-agent.exe' -UseBasicParsing" 2>nul
if %ERRORLEVEL% neq 0 (
    echo   [WARN] bseye-agent.exe download failed. Copy manually from USB.
)

echo   - thermal_checker_32.exe
powershell -Command "Invoke-WebRequest -Uri '%DOWNLOAD_BASE%/thermal_checker_32.exe' -OutFile '%INSTALL_DIR%\thermal_checker_32.exe' -UseBasicParsing" 2>nul
if %ERRORLEVEL% neq 0 (
    echo   [WARN] thermal_checker_32.exe download failed. Copy manually from USB.
)

echo   - config_kiosk_sample.ini
powershell -Command "Invoke-WebRequest -Uri '%DOWNLOAD_BASE%/config_kiosk_sample.ini' -OutFile '%INSTALL_DIR%\config_kiosk_sample.ini' -UseBasicParsing" 2>nul

echo   - bseye-agent-viewer.html
powershell -Command "Invoke-WebRequest -Uri '%DOWNLOAD_BASE%/bseye-agent-viewer.html' -OutFile '%INSTALL_DIR%\templates\bseye-agent-viewer.html' -UseBasicParsing" 2>nul

:: config.ini 생성
echo [3/6] Setting up config.ini...
if not exist "%INSTALL_DIR%\config.ini" (
    if exist "%INSTALL_DIR%\config_kiosk_sample.ini" (
        copy "%INSTALL_DIR%\config_kiosk_sample.ini" "%INSTALL_DIR%\config.ini" >nul
        echo   config_kiosk_sample.ini copied to config.ini
    ) else (
        echo   [WARN] config_kiosk_sample.ini not found. Create config.ini manually.
        goto :skip_config
    )
) else (
    echo   config.ini already exists, skipping.
    goto :skip_config
)

:: 사용자 입력
echo.
echo [4/6] Enter kiosk settings:
set /p "HOSP_CD=  Hospital code (e.g. H001): "
set /p "KIOSK_ID=  Kiosk ID (e.g. KIOSK01): "
set /p "KIOSK_NAME=  Kiosk name (e.g. 1F Reception): "

if not "%HOSP_CD%"=="" (
    powershell -Command "(Get-Content '%INSTALL_DIR%\config.ini') -replace 'hosp_cd = .*', 'hosp_cd = %HOSP_CD%' | Set-Content '%INSTALL_DIR%\config.ini'"
)
if not "%KIOSK_ID%"=="" (
    powershell -Command "(Get-Content '%INSTALL_DIR%\config.ini') -replace 'kiosk_id = .*', 'kiosk_id = %KIOSK_ID%' | Set-Content '%INSTALL_DIR%\config.ini'"
)
if not "%KIOSK_NAME%"=="" (
    powershell -Command "(Get-Content '%INSTALL_DIR%\config.ini') -replace 'kiosk_name = .*', 'kiosk_name = %KIOSK_NAME%' | Set-Content '%INSTALL_DIR%\config.ini'"
)
echo   config.ini updated.

:skip_config

:: 작업 스케줄러 등록
echo [5/6] Registering startup task...
schtasks /query /tn "BSEYE Agent" >nul 2>&1
if %ERRORLEVEL% equ 0 (
    echo   Task already registered, skipping.
) else (
    schtasks /create /tn "BSEYE Agent" /tr "\"%INSTALL_DIR%\bseye-agent.exe\"" /sc onlogon /rl highest /f >nul 2>&1
    if %ERRORLEVEL% equ 0 (
        echo   Startup task registered.
    ) else (
        echo   [WARN] Failed to register task. Register manually.
    )
)

:: Agent 실행
echo [6/6] Starting agent...
if exist "%INSTALL_DIR%\bseye-agent.exe" (
    start "" "%INSTALL_DIR%\bseye-agent.exe"
    echo   Agent started.
) else (
    echo   [WARN] bseye-agent.exe not found. Copy files first.
)

echo.
echo ============================================
echo   Installation complete!
echo   Install dir: %INSTALL_DIR%
echo   Config: %INSTALL_DIR%\config.ini
echo ============================================
echo.
pause
