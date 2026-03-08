# BSEYE Agent 설치 가이드
> 최종 업데이트: 2026-03-08

---

## 사전 준비

### 설치 대상 PC 요구사항
- Windows 10 이상
- 인터넷 연결 가능 (HTTPS 443 포트)
- Python 설치 불필요 (EXE 단독 실행)

### 설치 전 확인 정보
- 병원코드 (hosp_cd) — 예: H001
- 키오스크ID (kiosk_id) — 예: KIOSK_01
- 병원명 — 예: 강남세브란스
- 설치위치 — 예: 1층 로비
- 키오스크 프로그램 프로세스명 — 예: hospital_kiosk_app.exe
- 설치자 이름

---

## 설치 순서

### 1단계 — 백신 예외 등록 (필수, 설치 전 먼저 수행)

EXE 파일이 백신에 의해 차단될 수 있습니다. 설치 전에 예외 폴더를 등록하세요.

**Windows Defender:**
1. 시작 → "Windows 보안" 검색 → 열기
2. "바이러스 및 위협 방지" 클릭
3. "바이러스 및 위협 방지 설정" 아래 "설정 관리" 클릭
4. 아래로 스크롤 → "제외" 항목 → "제외 추가 또는 제거" 클릭
5. "제외 사항 추가" → "폴더" 선택
6. C:\bseye-agent 입력 (폴더가 없으면 먼저 생성)
7. "폴더 선택" 클릭

**V3, 알약 등 타사 백신:**
- 해당 백신의 실시간 감시 → 예외 설정에서 C:\bseye-agent 폴더 추가
- 또는 설치 중 일시적으로 실시간 감시 해제 후 설치 완료 뒤 재활성화

### 2단계 — 설치마법사에서 정보 입력

1. https://monitor.blueswell.co.kr/setup-monitor 접속 (로그인 필요)
2. 1단계 "키오스크 정보 입력"에서 병원코드, 키오스크ID, 병원명, 위치, 프로세스명, 설치자 입력
3. "다음" 클릭

### 3단계 — 설치 명령어 복사 및 실행

1. 2단계에서 "설치 명령어 생성" 클릭
2. "명령어 복사" 버튼 클릭
3. 키오스크 PC에서 PowerShell을 관리자 모드로 실행
   (시작 → PowerShell 우클릭 → 관리자로 실행)
4. 복사한 명령어를 붙여넣고 Enter

자동으로 수행되는 작업:
- C:\bseye-agent 폴더 생성
- 서버에서 에이전트 파일 다운로드
- config.ini 자동 생성 (입력한 정보 반영)
- 에이전트 실행

### 4단계 — 설치 확인

1. 설치마법사 3단계 "설치 확인"에서 "에이전트 연결됨" 표시 확인
2. 브라우저에서 http://localhost:8080 접속 → 로컬 대시보드 확인
3. https://monitor.blueswell.co.kr/usage 에서 해당 키오스크 데이터 수신 확인

---

## 수동 설치 (설치마법사 사용 불가 시)

### 1단계 — 다운로드

아래 URL에서 EXE 다운로드:
https://monitor.blueswell.co.kr/static/agent/bseye-agent.exe

다운로드 시 브라우저 경고가 나오면:
- Chrome: "계속" 또는 "유지" 클릭
- Edge: "..." → "유지" → "자세한 정보" → "계속 유지"

### 2단계 — 폴더 생성 및 배치

C:\bseye-agent 폴더를 만들고 EXE를 이동합니다.

### 3단계 — config.ini 작성

C:\bseye-agent\config.ini 파일을 메모장으로 만들고 아래 내용 입력:

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

각 항목을 실제 값으로 수정합니다.

### 4단계 — 실행

C:\bseye-agent\bseye-agent.exe 더블클릭
또는 CMD에서: C:\bseye-agent\bseye-agent.exe

---

## config.ini 항목 설명

| 항목 | 설명 | 예시 |
|------|------|------|
| web_port | 로컬 대시보드 포트 | 8080 |
| refresh_interval | 화면 갱신 주기(초) | 5 |
| retention_days | 로컬 DB 보관 일수 | 30 |
| target_process | 감시할 키오스크 프로세스명 | hospital_kiosk_app.exe |
| server_url | 서버 수신 API | https://monitor.blueswell.co.kr/api/kiosk-usage/receive |
| kiosk_id | 키오스크 고유ID | KIOSK_01 |
| hosp_cd | 병원코드 | H001 |
| hosp_name | 병원명 | 강남세브란스 |
| send_time | 일일 전송 시각 | 08:00 |
| retry_interval | 전송 실패 재시도 간격(초) | 300 |

---

## 문제 해결

### 백신이 EXE를 삭제함
→ 1단계 백신 예외 등록을 먼저 수행하세요. 이미 삭제된 경우 예외 등록 후 다시 다운로드하세요.

### 다운로드 시 브라우저가 차단
→ Chrome: 다운로드 바에서 "^" → "유지". Edge: "..." → "유지"

### Windows SmartScreen 경고
→ "추가 정보" 클릭 → "실행" 클릭 (코드 서명 미적용 시 정상 표시)

### 에이전트 실행 후 서버에 데이터 안 올라옴
→ config.ini의 server_url 확인, 인터넷 연결 확인, 방화벽 443 포트 확인

### 로컬 대시보드(localhost:8080) 접속 안 됨
→ 에이전트가 실행 중인지 확인, 다른 프로그램이 8080 포트를 사용 중인지 확인

---

## Windows 시작 시 자동 실행 설정

1. Win+R → shell:startup 입력 → Enter
2. 시작프로그램 폴더가 열림
3. C:\bseye-agent\bseye-agent.exe의 바로가기를 이 폴더에 복사
4. PC 재시작 시 자동 실행됨

---

## 파일 구조

C:\bseye-agent\
├── bseye-agent.exe    — 에이전트 실행 파일
├── config.ini         — 설정 파일
└── monitor.db         — 로컬 DB (자동 생성)
