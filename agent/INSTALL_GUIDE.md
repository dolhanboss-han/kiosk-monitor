# BSEYE Agent 설치 가이드

## 1. 요구사항
- Windows 10/11 64bit
- Python 3.8 이상

## 2. 패키지 설치
pip install psutil requests pyserial

## 3. 설정
bseye_agent.py의 CONFIG 부분 수정:
- hosp_cd: 병원코드 (예: 002)
- kiosk_id: 키오스크ID (예: KIOSK01)
- interval: 전송 주기 (기본 60초)

## 4. 실행
python bseye_agent.py

## 5. EXE 변환 (배포용)
pip install pyinstaller
pyinstaller --onefile --name bseye_agent bseye_agent.py

## 6. Windows 시작프로그램 등록
dist/bseye_agent.exe를 시작프로그램 폴더에 복사
