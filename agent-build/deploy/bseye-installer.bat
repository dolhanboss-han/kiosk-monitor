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

:: ─── [1/6] 설치 디렉토리 생성 ───
echo [1/6] 설치 폴더 생성...
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"
if not exist "%INSTALL_DIR%\templates" mkdir "%INSTALL_DIR%\templates"
echo   %INSTALL_DIR% OK
echo.

:: ─── [2/6] 파일 다운로드 ───
echo [2/6] 파일 다운로드 중...
echo   - bseye-agent.exe
powershell -Command "Invoke-WebRequest -Uri '%DOWNLOAD_BASE%/bseye-agent.exe' -OutFile '%INSTALL_DIR%\bseye-agent.exe' -UseBasicParsing" 2>nul
if %ERRORLEVEL% neq 0 (
    echo   [WARN] bseye-agent.exe 다운로드 실패. USB에서 수동 복사하세요.
)

echo   - thermal_checker_32.exe
powershell -Command "Invoke-WebRequest -Uri '%DOWNLOAD_BASE%/thermal_checker_32.exe' -OutFile '%INSTALL_DIR%\thermal_checker_32.exe' -UseBasicParsing" 2>nul
if %ERRORLEVEL% neq 0 (
    echo   [WARN] thermal_checker_32.exe 다운로드 실패. USB에서 수동 복사하세요.
)

echo   - config_kiosk_sample.ini
powershell -Command "Invoke-WebRequest -Uri '%DOWNLOAD_BASE%/config_kiosk_sample.ini' -OutFile '%INSTALL_DIR%\config_kiosk_sample.ini' -UseBasicParsing" 2>nul

echo   - bseye-agent-viewer.html
powershell -Command "Invoke-WebRequest -Uri '%DOWNLOAD_BASE%/bseye-agent-viewer.html' -OutFile '%INSTALL_DIR%\templates\bseye-agent-viewer.html' -UseBasicParsing" 2>nul

echo   - INSTALL_GUIDE.html
powershell -Command "Invoke-WebRequest -Uri '%DOWNLOAD_BASE%/INSTALL_GUIDE.html' -OutFile '%INSTALL_DIR%\INSTALL_GUIDE.html' -UseBasicParsing" 2>nul
echo.

:: ─── [3/6] config.ini 설정 ───
echo [3/6] config.ini 설정...

if exist "%INSTALL_DIR%\config.ini" (
    echo   config.ini 파일이 이미 존재합니다.
    set /p "OVERWRITE=  덮어쓰시겠습니까? (Y/N) [N]: "
    if /i not "!OVERWRITE!"=="Y" (
        echo   기존 config.ini 유지. 설정 단계를 건너뜁니다.
        goto :skip_config
    )
)

if not exist "%INSTALL_DIR%\config_kiosk_sample.ini" (
    echo   [WARN] config_kiosk_sample.ini 없음. config.ini를 수동 생성하세요.
    goto :skip_config
)

:: 기본값 설정
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
:: server 전용
set "V_PROCESS_LIST=bs_number.exe"
set "V_DB_TYPE=mssql"
set "V_DB_HOST=localhost"
set "V_DB_PORT=1433"

:input_start
echo.
echo ========================================
echo   설정값 입력 (Enter = 기본값 사용)
echo ========================================
echo.

:: 기본 설정
set /p "V_HOSP_CD=  병원코드 (hosp_cd) [%V_HOSP_CD%]: " || set "V_HOSP_CD=%V_HOSP_CD%"
set /p "V_KIOSK_ID=  키오스크번호 (kiosk_id) [%V_KIOSK_ID%]: " || set "V_KIOSK_ID=%V_KIOSK_ID%"
set /p "V_KIOSK_NAME=  키오스크이름 (kiosk_name) [%V_KIOSK_NAME%]: " || set "V_KIOSK_NAME=%V_KIOSK_NAME%"
set /p "V_DEVICE_TYPE=  장비유형 kiosk/server (device_type) [%V_DEVICE_TYPE%]: " || set "V_DEVICE_TYPE=%V_DEVICE_TYPE%"
set /p "V_CATEGORY=  카테고리 (category) [%V_CATEGORY%]: " || set "V_CATEGORY=%V_CATEGORY%"
set /p "V_MONITOR_SIZE=  모니터크기 inch (monitor_size) [%V_MONITOR_SIZE%]: " || set "V_MONITOR_SIZE=%V_MONITOR_SIZE%"
set /p "V_USAGE_TYPE=  사용유형 receipt/payment/certificate (usage_type) [%V_USAGE_TYPE%]: " || set "V_USAGE_TYPE=%V_USAGE_TYPE%"

echo.
echo --- 모니터링 설정 ---
set /p "V_TARGET_PROCESS=  감시프로세스 (target_process) [%V_TARGET_PROCESS%]: " || set "V_TARGET_PROCESS=%V_TARGET_PROCESS%"
set /p "V_RETENTION_DAYS=  데이터보관일 (retention_days) [%V_RETENTION_DAYS%]: " || set "V_RETENTION_DAYS=%V_RETENTION_DAYS%"
set /p "V_WEB_PORT=  웹포트 (web_port) [%V_WEB_PORT%]: " || set "V_WEB_PORT=%V_WEB_PORT%"
set /p "V_SEND_INTERVAL=  전송간격 초 (send_interval) [%V_SEND_INTERVAL%]: " || set "V_SEND_INTERVAL=%V_SEND_INTERVAL%"

echo.
echo --- 프린터 설정 ---
set /p "V_A4_IP=  A4 프린터 IP (printer_a4_ip) [%V_A4_IP%]: " || set "V_A4_IP=%V_A4_IP%"
set /p "V_SNMP_COMMUNITY=  SNMP 커뮤니티 (snmp_community) [%V_SNMP_COMMUNITY%]: " || set "V_SNMP_COMMUNITY=%V_SNMP_COMMUNITY%"
set /p "V_THERMAL_MODEL=  영수증 프린터 모델 (thermal_model) [%V_THERMAL_MODEL%]: " || set "V_THERMAL_MODEL=%V_THERMAL_MODEL%"

echo.
echo --- 주변장치 설정 ---
set /p "V_BARCODE_KEYWORD=  바코드스캐너 키워드 (barcode_keyword) [%V_BARCODE_KEYWORD%]: " || set "V_BARCODE_KEYWORD=%V_BARCODE_KEYWORD%"
set /p "V_VAN_PROCESS=  VAN 프로세스 (van_process) [%V_VAN_PROCESS%]: " || set "V_VAN_PROCESS=%V_VAN_PROCESS%"

echo.
echo --- EMR/네트워크 설정 ---
set /p "V_EMR_HOST=  EMR 서버 IP (emr_host) [%V_EMR_HOST%]: " || set "V_EMR_HOST=%V_EMR_HOST%"
set /p "V_EMR_PORT=  EMR 포트 (emr_port) [%V_EMR_PORT%]: " || set "V_EMR_PORT=%V_EMR_PORT%"
set /p "V_EMR_CHECK_TYPE=  EMR 체크방식 tcp/log_file (emr_check_type) [%V_EMR_CHECK_TYPE%]: " || set "V_EMR_CHECK_TYPE=%V_EMR_CHECK_TYPE%"
set /p "V_EMR_LOG_PATH=  EMR 로그경로 (emr_log_path) [%V_EMR_LOG_PATH%]: " || set "V_EMR_LOG_PATH=%V_EMR_LOG_PATH%"

:: server 전용 추가 입력
if /i "%V_DEVICE_TYPE%"=="server" (
    echo.
    echo --- 서버PC 전용 설정 ---
    set /p "V_PROCESS_LIST=  감시프로세스 목록 (process_list) [%V_PROCESS_LIST%]: " || set "V_PROCESS_LIST=%V_PROCESS_LIST%"
    set /p "V_DB_TYPE=  DB종류 (db_type) [%V_DB_TYPE%]: " || set "V_DB_TYPE=%V_DB_TYPE%"
    set /p "V_DB_HOST=  DB호스트 (db_host) [%V_DB_HOST%]: " || set "V_DB_HOST=%V_DB_HOST%"
    set /p "V_DB_PORT=  DB포트 (db_port) [%V_DB_PORT%]: " || set "V_DB_PORT=%V_DB_PORT%"
)

:: 설정 요약 표시
echo.
echo ========================================
echo   설정값 확인
echo ========================================
echo   병원코드       : %V_HOSP_CD%
echo   키오스크번호   : %V_KIOSK_ID%
echo   키오스크이름   : %V_KIOSK_NAME%
echo   장비유형       : %V_DEVICE_TYPE%
echo   카테고리       : %V_CATEGORY%
echo   모니터크기     : %V_MONITOR_SIZE%
echo   사용유형       : %V_USAGE_TYPE%
echo   감시프로세스   : %V_TARGET_PROCESS%
echo   데이터보관일   : %V_RETENTION_DAYS%
echo   웹포트         : %V_WEB_PORT%
echo   전송간격       : %V_SEND_INTERVAL%초
echo   A4 프린터 IP   : %V_A4_IP%
echo   SNMP 커뮤니티  : %V_SNMP_COMMUNITY%
echo   영수증 모델    : %V_THERMAL_MODEL%
echo   바코드 키워드  : %V_BARCODE_KEYWORD%
echo   VAN 프로세스   : %V_VAN_PROCESS%
echo   EMR 서버       : %V_EMR_HOST%:%V_EMR_PORT%
echo   EMR 체크방식   : %V_EMR_CHECK_TYPE%
echo   EMR 로그경로   : %V_EMR_LOG_PATH%
if /i "%V_DEVICE_TYPE%"=="server" (
    echo   --- 서버 전용 ---
    echo   감시 프로세스  : %V_PROCESS_LIST%
    echo   DB 종류        : %V_DB_TYPE%
    echo   DB 호스트      : %V_DB_HOST%:%V_DB_PORT%
)
echo ========================================
echo.

set /p "CONFIRM=  설정을 확인하세요 (Y/N) [Y]: " || set "CONFIRM=Y"
if /i not "%CONFIRM%"=="Y" (
    if /i "%CONFIRM%"=="N" (
        echo   다시 입력합니다...
        goto :input_start
    )
)

:: config_kiosk_sample.ini → config.ini 복사
copy "%INSTALL_DIR%\config_kiosk_sample.ini" "%INSTALL_DIR%\config.ini" >nul
echo   config.ini 생성 완료.

:: powershell로 각 값 치환
set "CFG=%INSTALL_DIR%\config.ini"

powershell -Command "(Get-Content '%CFG%') -replace 'hosp_cd = .*', 'hosp_cd = %V_HOSP_CD%' | Set-Content '%CFG%'"
powershell -Command "(Get-Content '%CFG%') -replace 'kiosk_id = .*', 'kiosk_id = %V_KIOSK_ID%' | Set-Content '%CFG%'"
powershell -Command "(Get-Content '%CFG%') -replace 'kiosk_name = .*', 'kiosk_name = %V_KIOSK_NAME%' | Set-Content '%CFG%'"
powershell -Command "(Get-Content '%CFG%') -replace 'device_type = .*', 'device_type = %V_DEVICE_TYPE%' | Set-Content '%CFG%'"
powershell -Command "(Get-Content '%CFG%') -replace 'category = .*', 'category = %V_CATEGORY%' | Set-Content '%CFG%'"
powershell -Command "(Get-Content '%CFG%') -replace 'monitor_size = .*', 'monitor_size = %V_MONITOR_SIZE%' | Set-Content '%CFG%'"
powershell -Command "(Get-Content '%CFG%') -replace 'usage_type = .*', 'usage_type = %V_USAGE_TYPE%' | Set-Content '%CFG%'"
powershell -Command "(Get-Content '%CFG%') -replace 'target_process = .*', 'target_process = %V_TARGET_PROCESS%' | Set-Content '%CFG%'"
powershell -Command "(Get-Content '%CFG%') -replace 'retention_days = .*', 'retention_days = %V_RETENTION_DAYS%' | Set-Content '%CFG%'"
powershell -Command "(Get-Content '%CFG%') -replace 'web_port = .*', 'web_port = %V_WEB_PORT%' | Set-Content '%CFG%'"
powershell -Command "(Get-Content '%CFG%') -replace 'send_interval = .*', 'send_interval = %V_SEND_INTERVAL%' | Set-Content '%CFG%'"
powershell -Command "(Get-Content '%CFG%') -replace 'ip = .*', 'ip = %V_A4_IP%' | Set-Content '%CFG%'"
powershell -Command "(Get-Content '%CFG%') -replace 'snmp_community = .*', 'snmp_community = %V_SNMP_COMMUNITY%' | Set-Content '%CFG%'"
powershell -Command "(Get-Content '%CFG%') -replace 'model = .*', 'model = %V_THERMAL_MODEL%' | Set-Content '%CFG%'"
powershell -Command "(Get-Content '%CFG%') -replace 'device_keyword = barcode.*', 'device_keyword = %V_BARCODE_KEYWORD%' | Set-Content '%CFG%'"
powershell -Command "(Get-Content '%CFG%') -replace 'process = .*', 'process = %V_VAN_PROCESS%' | Set-Content '%CFG%'"
powershell -Command "(Get-Content '%CFG%') -replace 'emr_host = .*', 'emr_host = %V_EMR_HOST%' | Set-Content '%CFG%'"
powershell -Command "(Get-Content '%CFG%') -replace 'emr_port = .*', 'emr_port = %V_EMR_PORT%' | Set-Content '%CFG%'"
powershell -Command "(Get-Content '%CFG%') -replace 'emr_check_type = .*', 'emr_check_type = %V_EMR_CHECK_TYPE%' | Set-Content '%CFG%'"
powershell -Command "(Get-Content '%CFG%') -replace 'emr_log_path = .*', 'emr_log_path = %V_EMR_LOG_PATH%' | Set-Content '%CFG%'"

if /i "%V_DEVICE_TYPE%"=="server" (
    powershell -Command "(Get-Content '%CFG%') -replace 'process_list = .*', 'process_list = %V_PROCESS_LIST%' | Set-Content '%CFG%'"
    powershell -Command "(Get-Content '%CFG%') -replace 'db_type = .*', 'db_type = %V_DB_TYPE%' | Set-Content '%CFG%'"
    powershell -Command "(Get-Content '%CFG%') -replace 'db_host = .*', 'db_host = %V_DB_HOST%' | Set-Content '%CFG%'"
    powershell -Command "(Get-Content '%CFG%') -replace 'db_port = .*', 'db_port = %V_DB_PORT%' | Set-Content '%CFG%'"
)

echo   config.ini 설정 완료.

:skip_config

:: ─── [4/6] DEVICE_CHECK 자동 설정 (server면 주변장치 off) ───
echo.
echo [4/6] 장치 체크 설정...
if /i "%V_DEVICE_TYPE%"=="server" (
    powershell -Command "(Get-Content '%CFG%') -replace 'monitor = .*', 'monitor = false' | Set-Content '%CFG%'"
    powershell -Command "(Get-Content '%CFG%') -replace 'printer_a4 = .*', 'printer_a4 = false' | Set-Content '%CFG%'"
    powershell -Command "(Get-Content '%CFG%') -replace 'printer_thermal = .*', 'printer_thermal = false' | Set-Content '%CFG%'"
    powershell -Command "(Get-Content '%CFG%') -replace 'card_reader = .*', 'card_reader = false' | Set-Content '%CFG%'"
    powershell -Command "(Get-Content '%CFG%') -replace 'barcode_scanner = .*', 'barcode_scanner = false' | Set-Content '%CFG%'"
    echo   서버PC 모드: 주변장치 체크 비활성화
) else (
    echo   키오스크 모드: 기본 장치 체크 유지
)

:: ─── [5/6] 작업 스케줄러 등록 ───
echo.
echo [5/6] 시작프로그램 등록...
schtasks /query /tn "BSEYE Agent" >nul 2>&1
if %ERRORLEVEL% equ 0 (
    echo   이미 등록되어 있습니다.
) else (
    schtasks /create /tn "BSEYE Agent" /tr "\"%INSTALL_DIR%\bseye-agent.exe\"" /sc onlogon /rl highest /f >nul 2>&1
    if %ERRORLEVEL% equ 0 (
        echo   시작프로그램 등록 완료.
    ) else (
        echo   [WARN] 등록 실패. 수동으로 등록하세요.
    )
)

:: ─── [6/6] Agent 실행 ───
echo.
echo [6/6] Agent 시작...
if exist "%INSTALL_DIR%\bseye-agent.exe" (
    start "" "%INSTALL_DIR%\bseye-agent.exe"
    echo   Agent가 시작되었습니다.
) else (
    echo   [WARN] bseye-agent.exe 파일이 없습니다. 파일을 먼저 복사하세요.
)

echo.
echo ============================================
echo   설치 완료!
echo   설치 경로 : %INSTALL_DIR%
echo   설정 파일 : %INSTALL_DIR%\config.ini
echo   웹 주소   : http://localhost:%V_WEB_PORT%
echo ============================================
echo.
pause
