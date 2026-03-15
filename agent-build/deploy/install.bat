@echo off
chcp 65001 >nul
echo ========================================
echo   BS-EYE Agent 설치
echo ========================================
echo.

:: 관리자 권한 확인
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo [오류] 관리자 권한으로 실행해주세요.
    echo 마우스 오른쪽 클릭 → 관리자 권한으로 실행
    pause
    exit /b 1
)

:: 폴더 생성
if not exist "C:\bseye-agent" mkdir "C:\bseye-agent"
cd /d "C:\bseye-agent"

echo [1/3] 설치 파일 다운로드 중...
powershell -Command "Invoke-WebRequest -Uri 'https://monitor.blueswell.co.kr/api/agent/download/bseye-installer.bat' -OutFile 'C:\bseye-agent\bseye-installer.bat'"

if not exist "C:\bseye-agent\bseye-installer.bat" (
    echo [오류] 다운로드 실패. 인터넷 연결을 확인하세요.
    pause
    exit /b 1
)

echo [2/3] 설치 시작...
call "C:\bseye-agent\bseye-installer.bat"

echo [3/3] 설치 완료
pause
