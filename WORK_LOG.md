# 작업 로그

## 2026-03-11 완료
- 공통 위젯 파일 구축 (widget-render.js, widget-common.css)
- 에디터/대시보드 UI 개선 (팔레트, 툴바, 헤더, KPI, 차트, 테이블)
- 장비이상현황 위젯 (숫자 3개, 깜박임)
- 미응답 키오스크 위젯 (10개 제한, 스크롤)
- 시계 위젯 스케일링

## 2026-03-12 완료
- 서버 이전: Lightsail 4GB RAM 인스턴스 (bseye-monitor-4gb)
- DNS 변경: monitor.blueswell.co.kr → 43.200.102.115
- SSL 인증서 재발급 (Let's Encrypt)
- v0 디자인 배포: Next.js 빌드 → /v0/ 경로로 서빙
- Nginx 설정: Flask(/), Next.js(/v0/), 정적파일(/_next/)
- 하드웨어 모니터링 DB 확장: kiosk_status에 6개 컬럼 추가 (monitor_hdmi, monitor_touch, monitor_model, van_agent_status, thermal_paper, thermal_detail)
- heartbeat API 수정: 새 하드웨어 필드 수신/저장
- Agent 업데이트 (v1.1.0): HDMI신호, 터치상태, 모니터모델, VAN Agent 프로세스 감시, Thermal Printer 상태 수집 함수 추가
- config.ini 샘플 생성 (VAN Agent 감시 목록)
- COMMON_RULES.md 정리 (중복 제거, 프로젝트 구조 추가)

## 미해결
- 차트 x축 라벨 안 보임 (에디터)
- 장비이상현황 리사이즈 시 제목 크기 미연동
- v0 디자인 → Flask 대시보드 완전 전환 (진행중)
- Supabase 마스터 DB 연동
- 카카오 알림톡 연동

---
마지막 업데이트: 2026-03-12
