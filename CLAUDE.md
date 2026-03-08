# BSEYE Kiosk Monitoring System — Claude Code 작업 지침서
> 최종 업데이트: 2026-03-08

---

## 1. 프로젝트 개요

| 항목 | 값 |
|------|-----|
| 서비스 URL | https://monitor.blueswell.co.kr |
| 서버 | AWS Lightsail, Ubuntu 22.04 LTS, Seoul (43.202.240.118) |
| 기술스택 | Python 3.10 + Flask 3.1.3 + Gunicorn + Nginx |
| DB | SQLite (monitor.db) + MSSQL (읽기전용, 121.141.174.121:1433) |
| 템플릿 엔진 | Jinja2 |
| 차트 | Chart.js (CDN) |
| Git | https://github.com/dolhanboss-han/kiosk-monitor (private) |
| 서비스 재시작 | sudo systemctl restart kiosk-monitor |

---

## 2. 프로젝트 구조

/home/ubuntu/kiosk-monitor/
- app.py — Flask 메인 (모든 라우트 포함)
- config.py — DB 연결 설정
- monitor.db — SQLite DB
- templates/ — HTML 27개
- static/ — CSS/JS/이미지 (대부분 비어있음)
- static/agent/ — 에이전트 배포 파일
- agent/ — 에이전트 소스
- SERVER_SETUP_LOG.md — 서버 설정 + 작업 이력
- PROJECT_STATUS.md — 자동 생성 현황 문서
- PREDICTION_SPEC.md — 예측 분석 기획서
- CLAUDE.md — 이 파일

---

## 3. 템플릿 파일 (templates/ 27개)

### nav.html include 적용 (22개)

index.html — 대시보드 (/)
monitoring.html — 모니터링 (/monitoring)
monitoring3.html — 모니터링 대체뷰 (/monitoring3, 비활성)
hospitals.html — 병원목록 (/hospitals)
hospital_detail.html — 병원상세 (/hospital/{code})
isv_detail.html — ISV상세 (/isv/{name})
usage.html — 행동분석 (/usage)
usage_verify.html — 현장검증 (/usage-verify)
maintenance.html — 유지보수 (/maintenance)
alarms.html — 알람관리 (/alarms)
tickets.html — 티켓관리 (/tickets)
ticket_detail.html — 티켓상세 (/ticket/{id})
ticket_form.html — 티켓등록 (/ticket/new)
executive.html — 경영진 대시보드 (/executive)
hospital_view.html — 병원 대시보드 (/hospital-view)
setup_monitor.html — 설치마법사 (/setup-monitor)
admin_users.html — 사용자관리 (/admin/users)
admin_user_form.html — 사용자등록 (/admin/users/new)
admin_login_log.html — 로그인이력 (/admin/login-log)
change_password.html — 비밀번호변경 (/change-password)
editor.html — 에디터 (/editor, 메뉴에서 제거됨, URL 직접접근만 가능)
kiosk_editor.html — 키오스크 에디터 (/kiosk-editor)

### nav.html 미적용 (5개) — 수정 불필요

login.html — 로그인
nav.html — 공통 네비게이션 (자기 자신)
index_old.html — 미사용 구버전
dashboard_preview.html — 위젯 미리보기 전용
kiosk_preview.html — 키오스크 미리보기 전용

---

## 4. 네비게이션 (nav.html)

### PC (768px 초과)
- 상단 가로 메뉴바, 중앙정렬
- 역할(session role, ot)에 따라 메뉴 동적 표시

### 모바일 (768px 이하)
- 가로 메뉴 숨김
- 좌측 고정 햄버거(☰) 버튼 표시
- 클릭 시 우측에서 슬라이드 패널 열림
- 오버레이 클릭으로 닫기

### 권한별 메뉴

hq_admin: 대시보드, 모니터링, 병원목록, 행동분석, 현장검증, 경영진, 병원뷰, 유지보수, 알람관리, 티켓관리, 설치마법사, 사용자관리
hosp_admin: 대시보드, 모니터링, 행동분석, 알람관리, 티켓관리
isv_admin: 대시보드, 모니터링, 행동분석, 현장검증, 유지보수, 알람관리, 티켓관리, 설치마법사

에디터는 메뉴에서 제거됨. URL 직접 접근만 가능.

---

## 5. CSS 스타일 규칙

### 구조적 특징
- 외부 CSS 파일 없음. 각 HTML 파일 내 <style> 블록에 CSS 포함
- 인라인 style 속성 많이 사용됨. 이 패턴을 유지할 것
- 헤더 클래스가 파일마다 다름: .header(index), .hdr(monitoring, usage), .hd(setup, verify, executive)
- 일괄 클래스명 치환 금지. 각 파일의 기존 패턴을 따를 것

### 로고 규격 (전체 통일 완료)

PC: font-size 1.26rem, font-weight 700
모바일: font-size 0.95rem (nav.html @media에서 일괄 적용)
BS 색상: #00d4ff (파랑)
EYE 색상: #eee (흰색)
메뉴명 색상: #a0b0c0 (회색), font-size 0.82rem

로고 HTML 예시:
<span style="font-size:1.26rem;font-weight:700;color:#eee;white-space:nowrap"><em style="color:#00d4ff;font-style:normal">BS</em>EYE</span>
<span style="font-size:0.82rem;font-weight:400;color:#a0b0c0;margin-left:6px">한글메뉴명</span>

### 색상 테마
- 배경: #0a0e1a ~ #111130
- 카드: #1a1a3e ~ #12122a
- 테두리: #333
- 텍스트: #eee(주), #888 ~ #a0b0c0(보조)
- 포인트: #00d4ff(파랑), #00ff88(녹), #ff4444(빨), #ffaa00(노)

---

## 6. 반응형(모바일) 작업 규칙

### 필수 원칙
1. 브레이크포인트는 768px 하나만 사용. 다른 브레이크포인트 추가 금지
2. @media(max-width:768px){} 블록을 </style> 바로 위에 추가
3. 데스크톱 CSS와 HTML 구조는 절대 변경하지 않음
4. 터치 대상 최소 44px x 44px
5. 수정 전 반드시 git commit으로 백업

### @media 적용 현황

모바일 레이아웃 완료:
index.html, monitoring.html, usage.html, maintenance.html, executive.html,
hospital_view.html, hospitals.html, hospital_detail.html, isv_detail.html,
admin_login_log.html, change_password.html, setup_monitor.html, usage_verify.html

@media 존재하나 모바일 레이아웃 불완전 (보강 필요):
alarms.html, tickets.html

@media 없음 (추가 필요):
admin_users.html, ticket_detail.html, ticket_form.html

PC 전용 — 모바일 작업 불필요:
editor.html, kiosk_editor.html, dashboard_preview.html, kiosk_preview.html,
login.html, index_old.html, admin_user_form.html, monitoring3.html

### 테이블 카드 변환 패턴

@media(max-width:768px){
    table thead{display:none}
    table tr{display:block;background:#1a1a3e;margin-bottom:8px;padding:10px;border-radius:8px}
    table td{display:block;padding:4px 0;border:none;font-size:0.85rem}
    table td::before{content:attr(data-label);font-weight:bold;color:#888;margin-right:8px}
}

---

## 7. SQLite DB 주요 테이블 (monitor.db)

users — 사용자 계정 (username, role, org_type, org_code)
login_log — 로그인 이력
dashboard_layouts — 대시보드 레이아웃
widgets — 위젯 설정
kiosk_devices — 키오스크 등록 정보
kiosk_status — 키오스크 실시간 상태 (heartbeat)
device_components — 장치 구성요소 상태
alarms — 알람
tickets — 티켓
ticket_comments — 티켓 댓글
notification_log — 알림 이력
heartbeat_log — 하트비트 이력
printer_daily_count — 일별 인쇄량 (SNMP 기반)
usage_event_log — 사용 이벤트 로그
usage_daily_summary — 일별 사용 요약

---

## 8. Git 작업 규칙

### 커밋
- 파일 1개 수정할 때마다 커밋
- 메시지 형식: "mobile: alarms.html 모바일 반응형 추가"
- 작업 시작 전: git add -A && git commit -m "작업 전 백업"

### 배포 흐름
로컬(C:\bseye\kiosk-monitor) -> git push -> GitHub -> 서버에서 git pull -> 서버 반영
- Claude Code는 로컬 파일만 수정 (서버 직접 접근 불가)
- git push 후 사용자가 서버 반영 요청하면 서버에서 처리
- 서버 재시작은 서버 세션에서만 가능

---

## 9. 현재 상태 (2026-03-08)

### 완료
- 로고 전체 통일 (BS파랑 EYE흰색, PC 1.26rem, 모바일 0.95rem)
- 로고 옆 한글 메뉴명 전체 적용
- 햄버거 모바일 메뉴 (좌측 고정, 슬라이드 패널)
- PC/모바일 메뉴명 통일
- 에디터 메뉴에서 제거
- monitoring.html 유지보수 이동 버튼 제거
- GitHub private repo 연동

### 진행중
- 모바일 @media 보강: alarms.html, tickets.html
- 모바일 @media 신규: admin_users.html, ticket_detail.html, ticket_form.html

### 미해결
- setup-monitor: saveInfo/downloadInstaller/next 버튼 동작 불량
- maintenance.html: JavaScript 오류
- app.py: f-string 문법 오류 잔여건
- kiosk_editor.html: 이벤트 리스너 중복

### 예정
- 토너/용지 소진 예측 (PREDICTION_SPEC.md)
- 데이터 정합성 체크
- 카카오 알림톡 연동
- 에이전트 양방향 전환

---

## 10. 주의사항

1. nav.html 수정하면 22개 페이지에 영향. PC와 모바일 모두 확인 필수
2. executive.html이 스타일 기준. 새 페이지나 수정 시 참조
3. .hd a 같은 광범위 셀렉터는 nav-mobile 링크까지 영향. :not(#nav-mobile a) 처리 필요
4. 각 페이지 헤더 클래스 다름 (.header, .hdr, .hd). 일괄 치환 금지
5. monitor.db는 gitignore됨. DB 스키마 변경은 init_db.py 또는 app.py에서 처리
6. venv/, __pycache__/, *.pyc, *.db, *.log 는 gitignore됨

---

## 11. 참조 문서

- SERVER_SETUP_LOG.md — 서버 설정 전체 이력 (Phase 1~4)
- PROJECT_STATUS.md — 파일 구조, 라우트, DB 테이블, 권한 매트릭스
- PREDICTION_SPEC.md — 토너/용지 소진 예측 등 7개 예측 항목 기획서
