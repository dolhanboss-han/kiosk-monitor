# WORK LOG

## 2026-03-13 (Supabase DB 통합)

### 완료
- Supabase 프로젝트 연동 (xzozycbrkdqoztcxbtwa)
- 병원코드 마이그레이션: MSSQL → Supabase hospitals 테이블
  - 정확 매칭: 123건
  - 유사 매칭: 33건
  - 총 156건 완료, 미배정 24건 (신규 코드 필요)
- 중복 병원 정리: 6건 삭제 (180건 → 180건)
- kiosk_records에 hosp_cd 컬럼 추가 및 매핑 (209건)
- Supabase 모니터링 테이블 11개 생성
  - mst_kiosk_devices, mon_kiosk_status, mon_heartbeat_log
  - mon_alarms, mon_tickets, mon_ticket_comments, mon_notification_log
  - sys_users, sys_login_log
  - usg_daily_summary, usg_event_log
- 인덱스 설계: hosp_cd 기반 유니크/인덱스 적용
- RLS(Row Level Security) 전체 테이블 활성화
- SQLite → Supabase 데이터 이전 완료 (총 2,383건)
- Flask heartbeat API: SQLite + Supabase 이중 저장
- Supabase 키 환경변수화 (.env + systemd EnvironmentFile)
- Git push 완료

### 미완료
- 미배정 병원 24건 코드 발급
- MSSQL 사용량 데이터(27,744건) Supabase 이전
- Flask API 전체를 Supabase로 전환 (현재 heartbeat만)
- Next.js(v0) 대시보드 제작 (고정 레이아웃)
- 키오스크 C# 프로그램 로컬 SQLite 연동
- Agent 사용량 전송 기능 추가
- 카카오 알림톡 연동

## 2026-03-12
- 서버 이전 (Lightsail 4GB), DNS/SSL
- v0 디자인 배포, Nginx 설정
- DB 컬럼 확장, heartbeat API 수정
- Agent v1.1.0 (HDMI/터치/VAN/Thermal)
- agent_config.ini 동적 로딩
- COMMON_RULES.md 정리

## 2026-03-11
- 위젯 공통 파일, UI 개선, 차트 수정
