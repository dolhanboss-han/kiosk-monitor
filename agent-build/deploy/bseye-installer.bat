@echo off
setlocal enabledelayedexpansion
title BS-EYE Agent Installer

echo ============================================
echo   BS-EYE Agent Installer
echo ============================================
echo.

:: Settings
set "INSTALL_DIR=C:\bseye-agent"
set "SERVER=https://monitor.blueswell.co.kr"
set "DOWNLOAD_BASE=%SERVER%/api/agent/download"

:: --- [1/6] Create install directory ---
echo [1/6] Creating install directory...
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"
if not exist "%INSTALL_DIR%\templates" mkdir "%INSTALL_DIR%\templates"
echo   %INSTALL_DIR% OK
echo.

:: --- [2/6] Download files ---
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

echo   - INSTALL_GUIDE.html
powershell -Command "Invoke-WebRequest -Uri '%DOWNLOAD_BASE%/INSTALL_GUIDE.html' -OutFile '%INSTALL_DIR%\INSTALL_GUIDE.html' -UseBasicParsing" 2>nul
echo.

:: --- [3/6] config.ini setup ---
echo [3/6] config.ini setup...

if exist "%INSTALL_DIR%\config.ini" (
    echo   config.ini already exists.
    set /p "OVERWRITE=  Overwrite? (Y/N) [N]: "
    if /i not "!OVERWRITE!"=="Y" (
        echo   Keeping existing config.ini. Skipping setup.
        goto :skip_config
    )
)

:: Default values
set "V_HOSP_CD=000"
set "V_KIOSK_ID=TEST01"
set "V_KIOSK_NAME=TEST"
set "V_DEVICE_TYPE=kiosk"
set "V_CATEGORY=standard"
set "V_MONITOR_SIZE=27"
set "V_USAGE_TYPE=receipt"
set "V_TARGET_PROCESS=kiosk_msys.exe"
set "V_RETENTION_DAYS=30"
set "V_WEB_PORT=8080"
set "V_SEND_INTERVAL=60"
set "V_A4_IP=192.168.0.25"
set "V_SNMP_COMMUNITY=public"
set "V_THERMAL_MODEL=HMK-072"
set "V_BARCODE_KEYWORD=barcode,POS HID,0C2E"
set "V_VAN_PROCESS=KocesICPos.exe"
set "V_EMR_HOST=127.0.0.1"
set "V_EMR_PORT=7000"
set "V_EMR_CHECK_TYPE=log_file"
set "V_EMR_LOG_PATH=C:\MsystechHIS_Ver.2\KIOSK_NSS\LOG"
:: server only
set "V_PROCESS_LIST=bs_number.exe"
set "V_DB_TYPE=mssql"
set "V_DB_HOST=localhost"
set "V_DB_PORT=1433"

:input_start
echo.
echo ========================================
echo   Enter settings (press Enter for default)
echo ========================================
echo.

:: Basic settings
set /p "V_HOSP_CD=  Hospital code (hosp_cd) [%V_HOSP_CD%]: "
set /p "V_KIOSK_ID=  Kiosk ID (kiosk_id) [%V_KIOSK_ID%]: "
set /p "V_KIOSK_NAME=  Kiosk name (kiosk_name) [%V_KIOSK_NAME%]: "
set /p "V_DEVICE_TYPE=  Device type kiosk/server (device_type) [%V_DEVICE_TYPE%]: "
set /p "V_CATEGORY=  Category (category) [%V_CATEGORY%]: "
set /p "V_MONITOR_SIZE=  Monitor size inch (monitor_size) [%V_MONITOR_SIZE%]: "
set /p "V_USAGE_TYPE=  Usage type receipt/payment/certificate (usage_type) [%V_USAGE_TYPE%]: "

echo.
echo --- Monitoring ---
set /p "V_TARGET_PROCESS=  Target process (target_process) [%V_TARGET_PROCESS%]: "
set /p "V_RETENTION_DAYS=  Retention days (retention_days) [%V_RETENTION_DAYS%]: "
set /p "V_WEB_PORT=  Web port (web_port) [%V_WEB_PORT%]: "
set /p "V_SEND_INTERVAL=  Send interval sec (send_interval) [%V_SEND_INTERVAL%]: "

echo.
echo --- Printer ---
set /p "V_A4_IP=  A4 printer IP (printer_a4_ip) [%V_A4_IP%]: "
set /p "V_SNMP_COMMUNITY=  SNMP community (snmp_community) [%V_SNMP_COMMUNITY%]: "
set /p "V_THERMAL_MODEL=  Thermal printer model (thermal_model) [%V_THERMAL_MODEL%]: "

echo.
echo --- Peripherals ---
set /p "V_BARCODE_KEYWORD=  Barcode scanner keyword (barcode_keyword) [%V_BARCODE_KEYWORD%]: "
set /p "V_VAN_PROCESS=  VAN process (van_process) [%V_VAN_PROCESS%]: "

echo.
echo --- EMR / Network ---
set /p "V_EMR_HOST=  EMR host IP (emr_host) [%V_EMR_HOST%]: "
set /p "V_EMR_PORT=  EMR port (emr_port) [%V_EMR_PORT%]: "
set /p "V_EMR_CHECK_TYPE=  EMR check type tcp/log_file (emr_check_type) [%V_EMR_CHECK_TYPE%]: "
set /p "V_EMR_LOG_PATH=  EMR log path (emr_log_path) [%V_EMR_LOG_PATH%]: "

:: Server-only settings
if /i "%V_DEVICE_TYPE%"=="server" (
    echo.
    echo --- Server PC only ---
    set /p "V_PROCESS_LIST=  Process list (process_list) [!V_PROCESS_LIST!]: "
    set /p "V_DB_TYPE=  DB type (db_type) [!V_DB_TYPE!]: "
    set /p "V_DB_HOST=  DB host (db_host) [!V_DB_HOST!]: "
    set /p "V_DB_PORT=  DB port (db_port) [!V_DB_PORT!]: "
)

:: Summary
echo.
echo ========================================
echo   Configuration Summary
echo ========================================
echo   hosp_cd        : %V_HOSP_CD%
echo   kiosk_id       : %V_KIOSK_ID%
echo   kiosk_name     : %V_KIOSK_NAME%
echo   device_type    : %V_DEVICE_TYPE%
echo   category       : %V_CATEGORY%
echo   monitor_size   : %V_MONITOR_SIZE%
echo   usage_type     : %V_USAGE_TYPE%
echo   target_process : %V_TARGET_PROCESS%
echo   retention_days : %V_RETENTION_DAYS%
echo   web_port       : %V_WEB_PORT%
echo   send_interval  : %V_SEND_INTERVAL%s
echo   A4 printer IP  : %V_A4_IP%
echo   SNMP community : %V_SNMP_COMMUNITY%
echo   thermal model  : %V_THERMAL_MODEL%
echo   barcode keyword: %V_BARCODE_KEYWORD%
echo   VAN process    : %V_VAN_PROCESS%
echo   EMR host       : %V_EMR_HOST%:%V_EMR_PORT%
echo   EMR check type : %V_EMR_CHECK_TYPE%
echo   EMR log path   : %V_EMR_LOG_PATH%
if /i "%V_DEVICE_TYPE%"=="server" (
    echo   --- Server only ---
    echo   process_list   : !V_PROCESS_LIST!
    echo   db_type        : !V_DB_TYPE!
    echo   db_host        : !V_DB_HOST!:!V_DB_PORT!
)
echo ========================================
echo.

set /p "CONFIRM=  Confirm settings? (Y/N) [Y]: "
if not defined CONFIRM set "CONFIRM=Y"
if /i "%CONFIRM%"=="N" (
    echo   Re-entering settings...
    goto :input_start
)

:: Generate config.ini using CMD echo
echo   Generating config.ini...
set "CFG=%INSTALL_DIR%\config.ini"
del "%CFG%" 2>nul
echo [KIOSK_INFO]>"%CFG%"
echo device_type = %V_DEVICE_TYPE%>>"%CFG%"
echo category = %V_CATEGORY%>>"%CFG%"
echo monitor_size = %V_MONITOR_SIZE%>>"%CFG%"
echo usage_type = %V_USAGE_TYPE%>>"%CFG%"
echo.>>"%CFG%"
echo [MONITOR_SETTING]>>"%CFG%"
echo target_process = %V_TARGET_PROCESS%>>"%CFG%"
echo exclude_process =>>"%CFG%"
echo exclude_title =>>"%CFG%"
echo retention_days = %V_RETENTION_DAYS%>>"%CFG%"
echo web_port = %V_WEB_PORT%>>"%CFG%"
echo.>>"%CFG%"
echo [SERVER]>>"%CFG%"
echo server_url = https://monitor.blueswell.co.kr/api/agent/heartbeat>>"%CFG%"
echo usage_url = https://monitor.blueswell.co.kr/api/agent/events>>"%CFG%"
echo agent_token = bseye-agent-2026>>"%CFG%"
echo hosp_cd = %V_HOSP_CD%>>"%CFG%"
echo kiosk_id = %V_KIOSK_ID%>>"%CFG%"
echo kiosk_name = %V_KIOSK_NAME%>>"%CFG%"
echo send_interval = %V_SEND_INTERVAL%>>"%CFG%"
echo heartbeat_interval = 30>>"%CFG%"
echo.>>"%CFG%"
echo [DEVICE_CHECK]>>"%CFG%"
echo pc = true>>"%CFG%"
if /i "%V_DEVICE_TYPE%"=="server" (
    echo monitor = false>>"%CFG%"
    echo printer_a4 = false>>"%CFG%"
    echo printer_thermal = false>>"%CFG%"
    echo card_reader = false>>"%CFG%"
    echo barcode_scanner = false>>"%CFG%"
) else (
    echo monitor = true>>"%CFG%"
    echo printer_a4 = true>>"%CFG%"
    echo printer_thermal = true>>"%CFG%"
    echo card_reader = false>>"%CFG%"
    echo barcode_scanner = true>>"%CFG%"
)
echo.>>"%CFG%"
echo [PRINTER_A4]>>"%CFG%"
echo ip = %V_A4_IP%>>"%CFG%"
echo snmp_community = %V_SNMP_COMMUNITY%>>"%CFG%"
echo.>>"%CFG%"
echo [PRINTER_THERMAL]>>"%CFG%"
echo dll_path = C:\Windows\SysWOW64\HwaUSB.DLL>>"%CFG%"
echo model = %V_THERMAL_MODEL%>>"%CFG%"
echo.>>"%CFG%"
echo [CARD_READER]>>"%CFG%"
echo device_keyword = card,reader,smart>>"%CFG%"
echo.>>"%CFG%"
echo [BARCODE_SCANNER]>>"%CFG%"
echo device_keyword = %V_BARCODE_KEYWORD%>>"%CFG%"
echo.>>"%CFG%"
echo [VAN_AGENT]>>"%CFG%"
echo process = %V_VAN_PROCESS%>>"%CFG%"
echo.>>"%CFG%"
echo [NETWORK]>>"%CFG%"
echo emr_host = %V_EMR_HOST%>>"%CFG%"
echo emr_port = %V_EMR_PORT%>>"%CFG%"
echo emr_check_type = %V_EMR_CHECK_TYPE%>>"%CFG%"
echo emr_log_path = %V_EMR_LOG_PATH%>>"%CFG%"
echo emr_success_keyword = OCS/EMR>>"%CFG%"
echo.>>"%CFG%"
echo [SERVER_MONITOR]>>"%CFG%"
echo process_list = !V_PROCESS_LIST!>>"%CFG%"
echo db_type = !V_DB_TYPE!>>"%CFG%"
echo db_host = !V_DB_HOST!>>"%CFG%"
echo db_port = !V_DB_PORT!>>"%CFG%"
echo db_check = true>>"%CFG%"
echo   config.ini created.

:skip_config

echo.
echo ============================================
echo   Installation complete
echo   Install dir : %INSTALL_DIR%
echo   Config      : %INSTALL_DIR%\config.ini
echo   Guide       : %INSTALL_DIR%\INSTALL_GUIDE.html
echo ============================================
echo.
echo   Next steps:
echo     1. Open INSTALL_GUIDE.html for instructions
echo     2. cd C:\bseye-agent
echo     3. bseye-agent.exe debug
echo     4. Check http://localhost:8080
echo     5. If all OK, register as service
echo ============================================
echo.
pause
