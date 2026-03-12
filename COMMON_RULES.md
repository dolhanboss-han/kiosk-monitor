# 공통 적용 원칙

## 기본 원칙
1. **파일 수정 전 반드시 백업** - `cp 파일명 파일명.bak` 후 작업
2. **요청한 작업만 수행** - 관련 없는 코드 절대 건드리지 않음, 기존 기능 깨뜨리지 않음
3. **코드 중복 금지** - 한 곳 수정하면 양쪽 반영
4. **작업 종료 시 Git Push** - `git add -A && git commit && git push`, .bak 파일 제외
5. **작업 전 WORK_LOG.md, COMMON_RULES.md 확인 필수**

## 프로젝트 구조
- **프론트엔드**: Next.js (v0 디자인) → `/home/ubuntu/v0_design/` (포트 3000)
- **백엔드 API**: Flask (app.py) → `/home/ubuntu/kiosk-monitor/` (포트 5000)
- **Agent**: `/home/ubuntu/kiosk-monitor/agent/bseye_agent.py` (Windows 키오스크에 설치)
- **Nginx**: HTTPS → Flask(/), Next.js(/v0/), 정적파일(/_next/)

## 키오스크 하드웨어 구성
- PC, 모니터(27/32인치 터치), 카드리더, Thermal Printer, A4 프린터
- Agent 수집 항목: CPU, 메모리, 디스크, HDMI신호, 터치상태, 모니터모델, VAN Agent 프로세스, Thermal Printer(용지/상태), A4 프린터(SNMP), 네트워크, EMR연결

## 프로젝트 방향
- **1축**: 중소병원 클라우드 (Supabase + AWS)
- **2축**: 대형병원 온프레미스 (병원당 30~150대, 80개 병원)
- 하드웨어 모니터링은 양쪽 공통

---
마지막 업데이트: 2026-03-12
