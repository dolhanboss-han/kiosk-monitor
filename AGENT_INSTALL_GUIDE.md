# BSEYE Agent 설치 가이드
> 최종 업데이트: 2026-03-08

---

## 사전 준비

### 설치 대상 PC 요구사항
- Windows 10 이상
- 인터넷 연결 가능 (HTTPS 443 포트)
- Python 설치 불필요 (EXE 단독 실행)

### 설치 전 확인 정보
- 병원코드 (hosp_cd)
- 키오스크ID (kiosk_id)
- 병원명
- 설치위치
- 키오스크 프로그램 프로세스명
- 설치자 이름

---

## 설치 순서

### 1단계 — 백신 예외 등록 (필수)

EXE 파일이 백신에 의해 차단될 수 있습니다.

Windows Defender:
1. 시작 > Windows 보안 > 바이러스 및 위협 방지
2. 설정 관리 > 제외 > 제외 추가 또는 제거
3. 폴더 추가 > C:\bseye-agent

타사 백신(V3, 알약 등):
실시간 감시 예외에 C:\bseye-agent 폴더 추가

### 2단계 — 설치마법사에서 정보 입력

1. https://monitor.blueswell.co.kr/setup-monitor 접속
2. 병원코드, 키오스크ID, 병원명, 위치, 프로세스명, 설치자 입력
3. 다음 클릭

### 3단계 — 설치 명령어 복사 및 실행

1. 설치 명령어 생성 클릭
2. 명령어 복사 클릭
3. 키오스크 PC에서 PowerShell 관리자 모드로 실행
4. 붙여넣고 Enter

### 4단계 — 설치 확인

1. 설치마법사에서 에이전트 연결됨 표시 확인
2. http://localhost:8080 로컬 대시보드 확인
3. https://monitor.blueswell.co.kr/usage 에서 데이터 수신 확인

---

## 수동 설치 (설치마법사 불가 시 / USB 설치)

### 방법 A — 인터넷 가능한 경우
1. https://monitor.blueswell.co.kr/static/agent/bseye-agent.exe 다운로드
2. C:\bseye-agent 폴더 생성 후 EXE 이동
3. config.ini 작성 (아래 참조)
4. bseye-agent.exe 더블클릭

### 방법 B — USB 설치 (인터넷 불가)
1. 다른 PC에서 bseye-agent.exe 다운로드
2. USB에 복사
3. 키오스크 PC에 C:\bseye-agent 폴더 생성
4. USB에서 EXE 복사
5. config.ini 작성
6. bseye-agent.exe 더블클릭

### config.ini 예시

[MONITOR]
web_port = 8080
refresh_interval = 5
retention_days = 30
target_process = hospital_kiosk_app.exe
exclude_process =
exclude_title =

[SERVER]
server_url = https://monitor.blueswell.co.kr/api/kiosk-usage/receive
kiosk_id = KIOSK_01
kiosk_name = 강남세브란스_KIOSK_01
location = 1층 로비
hosp_cd = H001
hosp_name = 강남세브란스
installer = 홍길동
send_time = 08:00
retry_interval = 300

---

## config.ini 항목 설명

| 항목 | 설명 | 예시 |
|------|------|------|
| web_port | 로컬 대시보드 포트 | 8080 |
| target_process | 감시할 프로세스명 | hospital_kiosk_app.exe |
| server_url | 서버 수신 API | https://monitor.blueswell.co.kr/api/kiosk-usage/receive |
| kiosk_id | 키오스크 고유ID | KIOSK_01 |
| hosp_cd | 병원코드 | H001 |
| hosp_name | 병원명 | 강남세브란스 |
| send_time | 일일 전송 시각 | 08:00 |
| retry_interval | 재시도 간격(초) | 300 |

---

## 문제 해결

### 백신이 EXE 삭제
-> 1단계 예외 등록 후 다시 다운로드

### 브라우저 다운로드 차단
-> Chrome: 유지 클릭 / Edge: ... > 유지

### Windows SmartScreen 경고
-> 추가 정보 > 실행

### 서버에 데이터 안 올라옴
-> config.ini server_url 확인, 인터넷 연결 확인, 443 포트 확인

### 로컬 대시보드 접속 안 됨
-> 에이전트 실행 여부 확인, 8080 포트 충돌 확인

---

## 자동 실행 설정

1. Win+R > shell:startup > Enter
2. C:\bseye-agent\bseye-agent.exe 바로가기를 시작프로그램 폴더에 복사
3. PC 재시작 시 자동 실행

---

## 파일 구조

C:\bseye-agent\
- bseye-agent.exe (에이전트 실행 파일)
- config.ini (설정 파일)
- monitor.db (로컬 DB, 자동 생성)
