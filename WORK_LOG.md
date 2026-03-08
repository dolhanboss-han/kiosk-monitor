# BSEYE Kiosk Monitor — Claude Code 작업 지시 이력
> 최종 업데이트: 2026-03-08

---

## Phase 1: 모바일 @media 반응형 추가 (5개 파일)

### 지시 1 — 모바일 반응형 신규/보강
- 대상: alarms.html, tickets.html, admin_users.html, ticket_detail.html, ticket_form.html
- 내용: @media(max-width:768px) 블록 추가/보강, 테이블 카드 변환, data-label 속성, 터치 타겟 36~44px
- 규칙: 데스크톱 CSS/HTML 변경 금지, executive.html 스타일 참조
- 커밋: 파일당 1커밋, "mobile: {파일명} 모바일 반응형 추가"

## Phase 2: 모바일 레이아웃 수정 (5개 파일)

### 지시 2 — 세부 모바일 레이아웃 문제 수정
- 대상: alarms.html, tickets.html, index.html, usage.html, setup_monitor.html
- alarms/tickets: 헤더 링크 숨김, thead 강제 숨김
- index: KPI 그리드 1열, 차트 max-width:100%
- usage: 탭 메뉴 가로 스크롤, 테이블 카드 변환
- setup_monitor: 스텝탭 텍스트 숨김

## Phase 3: 모바일 헤더 통일 (16개 파일)

### 지시 3 — 헤더 스타일 + 시계 통일
- 기준: executive.html (로고+한글메뉴명+햄버거+시계)
- 배경: linear-gradient(135deg,#0d1220,#131a2e), border #1a2340
- 시계: clk ID, tick() JS, YYYY.MM.DD 오후 HH:MM:SS
- 숨김: .user-info, 로그아웃, 비밀번호변경 링크

## Phase 4: 행동분석 3단계 뷰

### 지시 5 — app.py hosp_cd 필터 추가
- 수정 API: dashboard, daily, funnel, kiosks, receive (5개)
- 신규 API: /api/kiosk-usage/hospitals
- DB: usage_daily_summary, usage_event_log에 hosp_cd 컬럼 추가

### 지시 6 — usage.html 3단계 뷰
- 병원 드롭다운, 키오스크 드롭다운, 빵가루 내비게이션
- 병원 순위 테이블 클릭 드릴다운, 키오스크 클릭 드릴다운

## Phase 5: 행동분석 기능 강화

### 지시 7 — 기간선택 + 차트 개선
- 단일 날짜를 시작일/종료일로 변경 (기본 14일)
- 시간대 차트: 14일 평균 + 선택기간 이중 바
- 퍼널: 수평 스택 바, 이탈 히트맵: 색 농도

### 지시 8 — 퍼널 세션 파싱 + UI 6개 항목
- app.py: window_title '_' 기준 메뉴/단계 분리
- 날짜 입력 색상, 선택영역 위치, 키오스크 드롭다운 전체 유지
- 시간대 차트 연동, 퍼널 독립 카드, 이탈 바 차트

### 지시 9 — 깔때기 + 워터폴 2단계 차트
- 메인: CSS 깔때기 (사다리꼴, 위=넓고 아래=좁음)
- 상세: Chart.js 워터폴 (스택 막대)

## Phase 6: 최종 다듬기 (예정, 미실행)

### 지시 10 — 7개 항목
1. 퍼널 API 시스템 이벤트 제외 (기타, Bluswell)
2. 조회 필수 조건 (기간+병원 필수)
3. 키오스크 클릭 시 드롭다운 변경 안 함
4. 메뉴별 이탈율 깔때기형
5. 각 탭 KPI에 기간 표시 "YYYY.MM.DD ~ YYYY.MM.DD (N일간)"
6. 깔때기 색상 톤다운 (#0a7ea8, #0a8a5a, #cc3333)
7. 모바일 대응

---

## 서버 직접 수정 이력

| 날짜 | 파일 | 내용 | 커밋 |
|------|------|------|------|
| 03-08 | executive.html | 모바일 한글 메뉴명 유지 | cb9d161 |
| 03-08 | maintenance.html | 헤더 두께 통일 | f901bd8 |
| 03-08 | maintenance.html | 배경색+시계 경영진 통일 | 4fffb8f |
| 03-08 | app.py | hosp_cd 컬럼 추가 + receive API 수정 | d873d6b |

## 핵심 규칙

1. 데스크톱 CSS/HTML 변경 금지 — @media(max-width:768px)에서만 작업
2. </style> 바로 위에 @media 배치
3. 스타일 기준 executive.html
4. 파일 1개마다 git commit, push는 전체 완료 후 1회
5. nav.html 수정 시 22개 페이지 영향 주의
6. 문제 시 원복: git checkout HEAD~1 -- 파일명

## 데이터 구조 메모

### window_title: 메뉴명_단계명 형식
- 업무: 재진접수, 도착확인, 진료수납, 진료예약, 번호표발행
- 제외: 뒤로(&B), Bluswell_kiosk_app

### 퍼널 세션 규칙
- menu 변경 시 새 세션 시작
- 마지막 step에 완료 포함 시 completed=True
