# BSEYE Kiosk Monitor - Server Setup Log
# 최종 업데이트: 2026-03-06

---

## 1. 서버 정보
- 클라우드: AWS Lightsail (Seoul ap-northeast-2a)
- 인스턴스: bseye-monitor
- 고정 IP: 43.202.240.118
- 도메인: https://monitor.blueswell.co.kr (SSL 적용)
- OS: Ubuntu 22.04 LTS
- 사양: 512 MB RAM, 2 vCPU, 20 GB SSD ($5/mo)
- 시간대: Asia/Seoul (KST)

---

## 2. 설치 소프트웨어
- Python 3.10, pip, venv
- Nginx 1.18 + Certbot (SSL 자동갱신)
- Gunicorn + Eventlet
- MSSQL ODBC Driver 18, pyodbc 5.3.0
- Flask 3.1.3 (SocketIO 5.6.1, Login 0.6.3, JWT-Extended 4.7.1)
- Chart.js (CDN)
- PyInstaller 6.19.0 (에이전트 EXE 빌드)

---

## 3. 프로젝트 구조
/home/ubuntu/kiosk-monitor/
- app.py (메인 Flask 앱)
- config.py (DB 설정)
- init_db.py (초기 DB 생성)
- init_layout_db.py (레이아웃 테이블 생성)
- monitor.db (SQLite DB)
- venv/ (가상환경)
- templates/ (HTML 템플릿 19개)
  - index.html, hospitals.html, hospital_detail.html, isv_detail.html
  - monitoring.html, alarms.html, tickets.html, ticket_form.html, ticket_detail.html
  - editor.html, dashboard_preview.html
  - login.html, change_password.html
  - admin_users.html, admin_user_form.html, admin_login_log.html
- agent/ (키오스크 에이전트)
  - bseye_agent.py, INSTALL_GUIDE.md
- static/ (CSS, JS, 이미지)
- routes/, models/, services/
- SERVER_SETUP_LOG.md

---

## 4. 서비스 명령어
- 재시작: sudo systemctl restart kiosk-monitor
- 상태: sudo systemctl status kiosk-monitor
- 로그: sudo journalctl -u kiosk-monitor -f
- Nginx: sudo systemctl restart nginx
- 가상환경: cd ~/kiosk-monitor && source venv/bin/activate

---

## 5. 방화벽
- UFW: 22(SSH), 80(HTTP), 443(HTTPS)
- Lightsail: 22, 80, 443, 5000(테스트)

---

## 6. DB 연결

### MSSQL (읽기전용)
- 서버: 121.141.174.121:1433
- DB: KIOSK / 사용자: nssdb
- 테이블: KIOSK_HOSP_INFO, KIOSK_HOSP_COUNT

### SQLite (관제용)
- 경로: /home/ubuntu/kiosk-monitor/monitor.db
- 테이블: users, login_log, dashboard_layouts, widgets, kiosk_devices, kiosk_status, device_components, alarms, tickets, ticket_comments, notification_log, heartbeat_log

---

## 7. 접속 URL
- https://monitor.blueswell.co.kr (메인 대시보드)
- /dashboard-preview (위젯 미리보기 30개)
- /editor (대시보드 에디터)
- /monitoring (실시간 모니터링)
- /hospitals (병원 목록)
- /hospital/{code} (병원 상세)
- /isv/{name} (ISV 상세)
- /alarms (알람 관리)
- /tickets (티켓 목록)
- /admin/users (계정 관리, HQ만)
- /admin/login-log (로그인 이력)
- /change-password (비밀번호 변경)
- /api/health (서버 상태)
- /api/agent/heartbeat (에이전트 수신 POST)
- /executive (경영진 대시보드)
- /hospital-view (병원 뷰 대시보드)
- /api/executive/overview (경영진 KPI)
- /api/executive/monthly (월별 사용량)
- /api/executive/isv-performance (ISV별 실적)
- /api/executive/top-hospitals (사용량 상위 병원)
- /api/executive/risk-hospitals (이탈 위험 병원)
- /api/executive/scale-distribution (규모별 사용량)
- /api/executive/weekday-heatmap (요일별 히트맵)
- /api/hospital-list (병원 목록)
- /api/hospital-view/summary/{cd} (병원 요약)
- /api/hospital-view/daily/{cd} (일별 사용량)
- /api/hospital-view/hourly/{cd} (시간대별 사용량)
- /api/hospital-view/compare/{cd} (동급 비교)

---

## 8. 계정 및 역할
- admin / bseye2026! (hq_admin, HQ)
- dolhan (hq_admin, HQ)
- test (hq_monitor, HQ)
- isv_jw / test1234! (isv_admin, JW)
- isv_metro / test1234! (isv_admin, METRO)
- hosp_002 / test1234! (hosp_admin, 002)

### 역할 체계
- hq_admin: 전체 관리
- hq_monitor: HQ 모니터링(읽기)
- hq_engineer: HQ 엔지니어(알람/티켓)
- isv_admin: ISV 관리자(소속 병원만)
- isv_tech: ISV 기술자(소속 병원만)
- hosp_admin: 병원 관리자(자기 병원만)
- hosp_user: 병원 사용자(자기 병원만)

---

## 9. 에이전트 API
- POST /api/agent/heartbeat
- 헤더: X-Agent-Token: bseye-agent-2026
- 자동 알람: CPU/MEM/DISK >90% (warning), 프린터/카드리더/EMR 오류 (critical)
- EXE: D:\BSEYE\dist\bseye_agent.exe (Python 불필요)

---

## 10. 위젯 시스템 (30개)
- KPI 15개: 전체병원, 가동병원, 전체키오스크, 오늘이용건수, 오늘가동병원, 오늘가동키오스크, 전체에이전트, 온라인에이전트, 장애에이전트, 오프라인에이전트, 미처리알람, 미처리티켓, 오늘장애건수, 평균응답시간, 이번달누적
- 테이블 8개: ISV목록, 최근사용현황, 알람목록, 티켓목록, 에이전트상태, 장애키오스크, 미응답키오스크, 오늘이용TOP10
- 차트 5개: 주간이용추이, ISV분포도넛, 월별이용추이, 시간대별이용, ISV별오늘이용
- 유틸 2개: 시계, 텍스트블록

---

## 11. 현재 데이터 (2026-03-06)
- 전체 병원: 203개
- 활성 병원: 184개 (USER_YN=Y)
- 서비스 활성: 150개 (SERVICE=Y)
- 이탈 위험: 18개 (USER_YN=N)
- 전체 키오스크: 349대
- ISV 파트너: 14개사
- 등록 에이전트: 3대 (TEST01, KIOSK01, KIOSK02)

---

## 12. 완료 작업

### Phase 1 (2026-03-04)
- [x] AWS 계정 + MFA, Lightsail 인스턴스 + 고정IP
- [x] 서버 환경 (Python, Nginx, Gunicorn, MSSQL 드라이버)
- [x] Flask 프로젝트, 메인 대시보드, 병원/ISV 페이지
- [x] 로그인/인증/계정관리/비밀번호변경/로그인이력
- [x] 모바일 반응형, DNS + SSL, HTTP->HTTPS
- [x] 대시보드 에디터 (위젯, 다중선택, 글자크기 연동)
- [x] 관제 SQLite 8개 테이블, 알람/티켓 관리
- [x] 에이전트 API + Python 코드, 모니터링 페이지
- [x] 서버 시간대 KST

### Phase 2 (2026-03-05)
- [x] 에이전트 PC 테스트
- [x] 역할별 접근 제어 (ISV/병원 필터링)
- [x] 위젯 9개 추가 (총 30개)
- [x] 미리보기 전체 재생성 + API 필드명 수정
- [x] 에디터-미리보기 레이아웃 일치
- [x] 추천 레이아웃 버튼
- [x] 에이전트 EXE 변환 (PyInstaller)
- [x] SERVER_SETUP_LOG.md 업데이트


### Phase 3 (2026-03-06)

#### 경영진 대시보드 (/executive)
- [x] 경영진 대시보드 신규 구축 (executive.html 전체 재작성)
- [x] 3단 레이아웃: 좌측 KPI + 가운데 차트 + 우측 순위
- [x] 좌측 패널: KPI 5개 (활성병원, 총키오스크, 이번달사용량, 이탈위험, 서비스활성) + ISV 분포 바
- [x] 가운데 8개 차트 (4x2 그리드):
  - 월별 사용량 + 성장률 (Bar+Line 이중축)
  - ISV 파트너 성과 (수평 Stacked Bar: 활성/비활성)
  - 키오스크당 월평균 사용량 (Area Line, Unit Economics)
  - 병원 규모별 사용량 분포 (Bar+Line, 키오스크 대수별)
  - 병원 활성화율 추이 (Area Line + 70% 기준선)
  - 일별 트렌드 + 7일 이동평균 (Dual Line)
  - 신규 개통 vs 이탈 순증 (쌍방향 Bar + Line)
  - 요일별 사용 패턴 히트맵 (커스텀 Canvas, 요일×시간대)
- [x] 우측 패널: 사용량 TOP 15 (금/은/동 아이콘) + 이탈 위험 병원 (점멸 경고)
- [x] 차트 호버 시 경영적 인사이트 툴팁 8개
- [x] 글자색 시인성 개선 (밝기 조정), 차트 내 글자 흰색 bold

#### 경영진 대시보드 API 신규/수정
- [x] 기존 API 엔드포인트 매칭 수정 (overview, monthly, isv-performance, top-hospitals, risk-hospitals)
- [x] /api/executive/scale-distribution 신규 (키오스크 대수별 병원 평균 사용량)
- [x] /api/executive/weekday-heatmap 신규 (요일×시간대 히트맵, 최근 4주)

#### 병원 뷰 대시보드 (/hospital-view)
- [x] 병원 뷰 대시보드 전면 재구축 (hospital_view.html 전체 재작성)
- [x] 2단 레이아웃: 좌측 병원정보+KPI + 가운데 차트 8개
- [x] 좌측 패널: 병원 헤더 (이름, 주소, ISV, 개통일, 활성/서비스 뱃지) + KPI 4개 (이번달, 전월, 오늘, 키오스크)
- [x] 가운데 8개 차트 (4x2 그리드):
  - 일별 사용량 + 7일 이동평균 (Dual Line)
  - 시간대별 사용 패턴 (Bar, 피크시간 강조색)
  - 주간 사용량 추이 (Bar+Line, daily→주간 그룹핑)
  - 동급 병원 내 순위 (수평 Bar, 본인 강조+타 병원 마스킹)
  - 요일별 사용 패턴 (Radar/Spider, daily→요일 그룹핑)
  - 키오스크 대당 효율 (Doughnut Gauge, 동급 평균 대비 %)
  - 3개월 성장 트렌드 (Bar, 전전월/전월/이번달)
  - 상위 사례 벤치마크 (수평 Bar + ISV 태그, TOP 5)
- [x] 차트 호버 시 경영적 인사이트 툴팁 8개
- [x] 첫 화면 병원 검색창 (가운데 + 좌측 패널 이중 배치)
- [x] 동급 병원 비교: 본인 병원만 실명, 타 병원 마스킹 처리
- [x] 상위 사례: 본인 포함 시 실명+강조, 타 병원 마스킹

#### 병원 뷰 API 수정
- [x] /api/hospital-view/hourly 쿼리 7일→30일 변경
- [x] /api/hospital-view/compare 응답 키 매칭 수정 (kiosks, month_total)
- [x] top_cases에 hosp_cd, is_me 필드 추가 (본인 병원 식별)

#### 메인 대시보드 연결
- [x] index.html 네비게이션에 '경영진', '병원뷰' 링크 추가
- [x] executive.html에 '◀ 메인', '병원뷰' 이동 버튼
- [x] hospital_view.html에 '◀ 메인', '경영진' 이동 버튼

#### 키오스크 에디터 점검
- [x] kiosk_editor.html 이벤트 리스너 중복 확인 (12개 매치)
- [x] globalResizing 변수 중복 수정

#### 문서
- [x] 경영진 대시보드 사용설명서 작성 (목차별 상세)
- [x] SERVER_SETUP_LOG.md 업데이트

---

## 13. 다음 작업---

## 13. 다음 작업

### 긴급 (Phase 3 후속)
- [ ] 데이터 정합성 체크: 이번달 사용량 월초 -81% 표시 원인 확인 (당월 누적 vs 전월 전체 비교)
- [ ] 데이터 정합성 체크: 병원 규모별 4대+ 그룹(696)이 3대(3,617)보다 낮은 원인 분석
- [ ] 데이터 정합성 체크: 요일별 히트맵 DATEPART(WEEKDAY) 서버 설정별 요일 매칭 확인
- [ ] 데이터 정합성 체크: 활성화율 분모(전체 병원) 시점 기준 보정
- [ ] 병원뷰 첫 화면 검색창 시인성 추가 개선
- [ ] kiosk_editor.html 이벤트 리스너 중복 완전 정리 (mousemove/mouseup/resize/drag)

### 예정
- [ ] 카카오 알림톡 연동
- [ ] 일별 사용량 스냅샷 수집
- [ ] 에이전트 자동업데이트 / Windows 서비스 등록
- [ ] 역할별 대시보드 레이아웃
- [ ] 대시보드 PDF/이미지 내보내기
- [ ] 키오스크 UI 에디터 (Phase 2)
- [ ] Supabase 마스터 DB 연동
- [ ] DB 백업 자동화, 보안 강화
- [ ] SLA 관리, 보고서 자동생성, 엔지니어 배차
- [ ] 병원 뷰 대시보드 사용설명서 작성
- [ ] 경영진/병원뷰 대시보드 모바일 반응형

---

## 14. 다음 세션
1. SERVER_SETUP_LOG.md 로컬 백업
2. 다음 대화 시 이 파일 첨부
3. "첨부 파일 읽고 계속 진행" 전송

## 2026-03-06 작업 내역

### 1. 에이전트(bseye_agent.py) SNMP 프린터 모니터링 추가
- `check_printer_snmp()` 함수 추가 (pysnmp-lextudio 사용)
- KYOCERA ECOSYS P3045dn (192.168.0.20) SNMP 조회: 모델, 시리얼, 토너잔량, 용지잔량(트레이3개), 인쇄매수
- `NETWORK_PRINTERS` 에 `snmp: True` 플래그 추가
- `check_all_network_printers()` 에서 SNMP 상세 데이터를 `detail` 키로 포함

### 2. 서버 app.py 수정
- heartbeat API: `network_printers` 필드 UPDATE/INSERT 추가
- SQLite WAL 모드 + timeout=10 적용 (database locked 해결)
- `printer_daily_count` 테이블 생성 (일별 인쇄량 자동 기록)
- heartbeat 수신 시 SNMP 프린터 page_count 기준으로 일별 인쇄량 자동 계산/저장
- `/api/printer-daily/<hosp_cd>/<kiosk_id>` API 추가
- `/api/printer-summary` API 추가
- `/api/kiosk-monitor` 에 today_print, avg7_print 포함

### 3. 모니터링 페이지(monitoring.html) 재구성
- 병원별 그룹핑 → 키오스크 타일 뷰 (한 화면에 30대 표시)
- 타일: PC상태(CPU/MEM/DISK), 장치5개 상태점, 토너게이지, 인쇄매수
- 호버 툴팁: 프린터 SNMP 상세 (토너/용지4게이지 + 오늘/7일avg/누적 인쇄량)
- 모바일 터치 상세보기 지원
- 글자크기 확대, 반응형 레이아웃

### 4. 테스트 데이터
- 15개 병원, 30대 키오스크 테스트 데이터 INSERT (실 운영 시 삭제 필요)

### 5. 인코딩 수정
- bseye_agent.py 한글 깨짐 → 영문 로그 메시지로 교체

### 현재 상태
- TEST01 (000): 에이전트 정상 연결, SNMP 프린터 데이터 수집 중
- Printer_A (192.168.0.6): TCP OK
- Printer_B (192.168.0.20): SNMP OK (토너49%, MP트레이0%, 카세트1 30%, 카세트2 70%, 누적 1,149매)
- 모니터링 URL: https://monitor.blueswell.co.kr/monitoring

## 2026-03-06 최종 목표 아키텍처 확정

### 현재 완료된 것 (Phase 0)
- bseye_agent.py: CPU/메모리/디스크 수집 + SNMP 프린터 읽기 (토너/용지/인쇄매수)
- 서버: heartbeat 수신 → SQLite 저장 → 모니터링 대시보드 표시
- 대시보드: 병원별 키오스크 타일 뷰, 프린터 SNMP 상세, 일별 인쇄량 기록
- 구조: 단방향 (에이전트 → 서버)

### 최종 목표 아키텍처
- 구조: 양방향 (에이전트 ↔ 서버)
- 에이전트: 수집 + 명령 수신/실행 (폴링 방식)
- 서버: 모니터링 + 명령 발행 + 자동 진단 + 알림
- 제어: SNMP SET (프린터 리셋/온라인전환), PC 원격 재부팅, 스마트멀티탭 전원제어
- 4단계 에스컬레이션: 소프트리셋 → 전원리셋 → 물리적전원차단 → 현장출동

### 구현 로드맵

#### Phase 1 — 양방향 전환 (설치 후 1주차)
- [ ] command_queue 테이블 생성
- [ ] heartbeat 응답에 pending 명령 포함
- [ ] 에이전트: 명령 수신 → 실행 → 결과 전송
- [ ] SNMP SET 구현 (소프트리셋, 온라인전환)
- [ ] 대시보드: 프린터 리셋 버튼

#### Phase 2 — 자동 진단 + 알림 (2주차)
- [ ] 토너/용지 임계값 자동 체크
- [ ] 에러 비트맵 해석 + 자동 조치 판단
- [ ] 알림 채널 연동 (카카오톡/슬랙)
- [ ] 일별/월별 인쇄량 통계 화면

#### Phase 3 — 물리적 제어 (3주차~)
- [ ] 스마트 멀티탭 선정/구매/테스트
- [ ] 4단계 자동 에스컬레이션 구현
- [ ] 에이전트 자동 업데이트 메커니즘

### 3월 9일 현장 설치 시 필수 확인 사항
- [ ] 프린터 SNMP Write Community String 확인/설정
- [ ] 프린터 고정 IP 확인
- [ ] SNMP Walk 전체 실행 (교세라 전용 OID 검증)
- [ ] 에이전트(bseye_agent.py) 설치/정상동작 확인
- [ ] 방화벽 포트 확인 (UDP 161)

### 참조 설계문서
- 키오스크 원격 관리 시스템 마크다운 (사용자 제공)
- 파일: snmp_utils.py, printer_manager.py, pc_manager.py, smart_plug.py, agent.py, monitor.py
- config.json 구조 확정

---

## Phase 4 (2026-03-07)

### 1. GitHub 이력 관리 체계 구축
- [x] Git 초기화 + .gitignore 생성 (DB, 캐시, 로그 제외)
- [x] GitHub private 저장소 생성: https://github.com/dolhanboss-han/kiosk-monitor
- [x] 초기 백업 커밋 + push 완료 (commit c03a808)
- [x] 모든 작업 단위별 커밋/푸시 규칙 적용

### 2. 사용현황 분석 (usage.html) 기능 구현
- [x] /usage 페이지 전체 탭 구현 (KPI, 키오스크별, 시간대별, 일별추이, 완료율)
- [x] /usage-verify 현장 검증 페이지 배포
- [x] 퍼널 분석 탭 기본 구현 (메뉴별/단계별 드롭오프)
- [x] usage_event_log 18,407건, usage_daily_summary 43건 데이터 확인

### 3. 설치 마법사 (setup_monitor.html) 수정
- [x] downloadInstaller() 함수 누락 → 추가 (PowerShell 명령어 생성 방식)
- [x] checkInstall() 함수 누락 → 추가 (에이전트 연결 확인)
- [x] bat 다운로드 → 복사/붙여넣기 방식으로 전환 (Windows Defender 차단 우회)
- [x] /api/setup/install-bat 라우트 경로 확인 (app.py line 990)
- [x] install.bat 내 C:\bseye-agent 경로 백슬래시 이스케이프 수정

### 4. 공통 네비게이션 통합 (nav.html)
- [x] templates/nav.html 신규 생성 — 권한별 메뉴 동적 표시
- [x] 역할 분기: hq(전체), hosp(제한), isv(제한)
- [x] 22개 HTML 파일에 {% include 'nav.html' %} 적용 완료
- [x] 적용 제외 5개: login.html, nav.html, index_old.html, dashboard_preview.html, kiosk_preview.html
- [x] 메뉴 중앙정렬 통일 (justify-content:center)
- [x] usage_verify.html 중앙정렬 별도 수정
- [x] 에디터 링크를 hq_admin 관리 영역으로 이동 (일반 메뉴에서 분리)
- [x] 관리 영역 구분선(|) 추가, "관리" → "사용자관리" 라벨 변경

### 5. UI 레이아웃 수정
- [x] alarms.html stat-card 가로배치 수정 (div.stats 래핑 추가)
- [x] tickets.html stat-card 가로배치 수정 (div.stats 래핑 추가)
- [x] editor.html 캔버스 왼쪽 빈공간 제거 (margin-left:260px 삭제)
- [x] maintenance.html 모바일 최적화 (헤더 한줄, 세로 알림 행)

### 6. 문서 생성
- [x] PROJECT_STATUS.md 자동 생성 (파일구조, 템플릿 현황, 라우트, DB 테이블, 권한 매트릭스, 사용자 목록)
- [x] SERVER_SETUP_LOG.md Phase 4 업데이트

### 7. 권한별 메뉴 접근 매트릭스 (nav.html 기준)

| 메뉴 | 경로 | hq_admin | hosp_admin | isv_admin |
|------|------|:--------:|:----------:|:---------:|
| 대시보드 | / | ✅ | ✅ | ✅ |
| 모니터링 | /monitoring | ✅ | ✅ | ✅ |
| 병원 | /hospitals | ✅ | ❌ | ❌ |
| 행동분석 | /usage | ✅ | ✅ | ✅ |
| 유지보수 | /maintenance | ✅ | ❌ | ✅ |
| 알람 | /alarms | ✅ | ✅ | ✅ |
| 티켓 | /tickets | ✅ | ✅ | ✅ |
| 경영진 | /executive | ✅ | ❌ | ❌ |
| 병원뷰 | /hospital-view | ✅ | ❌ | ❌ |
| 검증 | /usage-verify | ✅ | ❌ | ✅ |
| 설치 | /setup-monitor | ✅ | ❌ | ✅ |
| 에디터 | /editor | ✅ (관리) | ❌ | ❌ |
| 사용자관리 | /admin/users | ✅ (관리) | ❌ | ❌ |

### 8. 프로젝트 구조 업데이트
- templates/ 26개 HTML (기존 19개 → 7개 추가)
  - 추가: executive.html, hospital_view.html, monitoring3.html, setup_monitor.html, usage.html, usage_verify.html, nav.html
- Git 커밋 이력 관리 시작 (GitHub private repo)
- PROJECT_STATUS.md 자동 생성 스크립트

---

## 13. 다음 작업 (업데이트)

### 긴급
- [ ] setup-monitor: saveInfo/downloadInstaller 버튼 동작 최종 확인 (스크린샷 필요)
- [ ] 퍼널 분석 탭 스크린샷 검증 (메뉴별/단계별 드롭오프)
- [ ] maintenance.html JavaScript 오류 수정 ('현장출동' 정의, showTab 누락)
- [ ] f-string 문법 오류 잔여건 확인

### 보류 (기존 유지)
- [ ] 데이터 정합성 체크: 이번달 사용량 월초 -81% 표시 원인
- [ ] 데이터 정합성 체크: 병원 규모별 4대+ 그룹 이상치
- [ ] 데이터 정합성 체크: 요일별 히트맵 DATEPART(WEEKDAY) 매칭
- [ ] 데이터 정합성 체크: 활성화율 분모 시점 기준 보정
- [ ] kiosk_editor.html 이벤트 리스너 중복 완전 정리

### 예정 (기존 유지 + 추가)
- [ ] 권한별 백엔드 필터링 강화 (app.py 라우트별 hosp_cd 필터)
- [ ] hosp_admin / isv_admin 전용 대시보드 레이아웃
- [ ] executive.html, hospital_view.html 모바일 반응형 CSS (@media queries)
- [ ] Supabase 마스터 DB 연동 + 병원코드 마이그레이션
- [ ] 에이전트 MSSQL 데이터 수집 확장 (진입탈 상세정보)
- [ ] 카카오 알림톡 연동
- [ ] 에이전트 자동업데이트 / Windows 서비스 등록
- [ ] DB 백업 자동화, 보안 강화
- [ ] 에디터 독립 모듈 분리 (관리 전용)

---

## 14. 다음 세션
1. SERVER_SETUP_LOG.md 로컬 백업
2. 다음 대화 시 이 파일 첨부
3. "첨부 파일 읽고 계속 진행" 전송
