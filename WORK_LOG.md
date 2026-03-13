# BS-EYE 키오스크 모니터링 시스템 - 작업 기록

## 시스템 구조
- **DB**: Supabase (PostgreSQL) - 프로젝트 ID: xzozycbrkdqoztcxbtwa
- **Backend**: Flask API (Lightsail ubuntu@monitor.blueswell.co.kr)
- **Frontend**: Next.js v0 (예정)
- **Agent**: Python EXE (키오스크 PC에 설치)
- **키오스크 프로그램**: C# / PowerBuilder -> 로컬 SQLite -> Agent -> Supabase

## Supabase 테이블 (17개)
| 테이블 | 용도 | 건수 |
|---|---|---|
| hospitals | 병원 마스터 | 180 |
| kiosk_records | 키오스크 장비 이력 | 241 |
| mst_kiosk_devices | 키오스크 장비 마스터 | 4 |
| mst_agent_version | Agent 버전 관리 | 1 |
| mon_kiosk_status | 키오스크 실시간 상태 | 29 |
| mon_heartbeat_log | heartbeat 로그 | 1,748 |
| mon_alarms | 알람 | 6 |
| mon_tickets | 티켓 | 1 |
| mon_ticket_comments | 티켓 댓글 | 4 |
| mon_notification_log | 알림 로그 | 0 |
| sys_users | 사용자 | 8 |
| sys_login_log | 로그인 로그 | 149 |
| usg_daily_summary | 사용량 일별 요약 | 2 |
| usg_event_log | 사용량 이벤트 | 11 |
| usg_kiosk_daily | MSSQL 사용량 (이전) | 27,756 |

## Agent v3.0.0 구조

### 파일 구성 (D:\BSEYE\agent-build)
| 파일 | 크기 | 역할 |
|---|---|---|
| bseye_agent.py | 3KB | 진입점 - config, DB초기화, 스레드, Windows 서비스 |
| hw_monitor.py | 14KB | 하드웨어 모니터링 + heartbeat 전송 |
| hook_monitor.py | 3.4KB | 윈도우 타이틀 감시 (0.5초 폴링) |
| data_sender.py | 4.5KB | 사용량/이벤트/heartbeat캐시 서버 전송 |
| device_checker.py | 5.1KB | 장치 상태 점검 (로컬 웹 API용) |
| db_manager.py | 8.3KB | 로컬 SQLite DB 관리 (6개 테이블) |
| web_server.py | 1.6KB | 로컬 대시보드 FastAPI (localhost:8080) |
| config.ini | 0.9KB | 설정 파일 |

### 모니터링 체크 항목 (6개 카테고리)
| 카테고리 | 체크 방법 | 상세 항목 |
|---|---|---|
| PC | psutil + WMI | CPU, 메모리, 디스크, OS, IP, 네트워크 응답속도, EMR 연결 |
| MONITOR | PowerShell WMI | HDMI 신호, 터치패널, 모델명 |
| PRINTER(A4) | SNMP (네트워크) | 상태, 토너잔량, 카세트1/2 용지, 누적매수, 오늘사용량 |
| PRINTER(THERMAL) | HwaUSB.DLL (USB) | 상태, 용지유무, 커버열림, 에러 |
| CARD READER | Get-PnpDevice | USB 장치 연결 상태 |
| BARCODE SCANNER | Get-PnpDevice | USB 장치 연결 상태 |

### config.ini 섹션
- KIOSK_INFO: 키오스크 분류 (대/중/소분류)
- MONITOR_SETTING: 윈도우 감시 설정
- SERVER: 서버 연결 정보
- DEVICE_CHECK: 체크 항목 ON/OFF
- PRINTER_A4: A4 프린터 (IP, SNMP)
- PRINTER_THERMAL: 영수증 프린터 (DLL, 모델)
- CARD_READER: 카드리더 키워드
- BARCODE_SCANNER: 바코드스캐너 키워드
- VAN_AGENT: VAN Agent 프로세스
- NETWORK: EMR 호스트/포트

### 키오스크 분류 체계
- 대분류: barrier_free / standard
- 중분류: 모니터 사이즈 (27 / 32)
- 소분류: 용도 (receipt/register/cert/payment)

### 프린터 정보
- A4: 교세라 ECOSYS P3045DN (네트워크, SNMP)
- Thermal: 화성 HMK-825 (USB, HwaUSB.DLL)

### Agent heartbeat 필드
Copy
hosp_cd, kiosk_id, agent_version, cpu_usage, memory_usage, disk_usage, os_version, local_ip, network_latency, emr_status, monitor_model, monitor_hdmi, monitor_touch, van_agent_status, printer_a4, printer_a4_toner, printer_a4_cassette1, printer_a4_cassette2, printer_a4_total_pages, printer_a4_today, printer_thermal, thermal_cover, thermal_paper, card_reader, barcode_scanner


## 작업 이력

### 2026-03-13 (Supabase 통합 + Agent v3.0.0)

**완료:**
1. Supabase 프로젝트 연동 (xzozycbrkdqoztcxbtwa)
2. 병원코드 마이그레이션 (정확 123 + 유사 33 = 156건, 미배정 24건)
3. 중복 병원 6건 삭제
4. kiosk_records에 hosp_cd 컬럼 추가 (209건 매핑)
5. Supabase 모니터링 테이블 11개 생성 + 인덱스 + RLS
6. SQLite -> Supabase 데이터 이전 (2,383건)
7. MSSQL 사용량 27,756건 Supabase 이전 (usg_kiosk_daily)
8. Flask heartbeat API 이중저장 (SQLite + Supabase)
9. Supabase 키 환경변수화 (.env + systemd)
10. Agent v3.0.0 통합 완성 (7개 모듈)
11. Agent -> 서버 -> Supabase heartbeat 전송 성공
12. 자동 업데이트 기능 (update-check API + Nginx /downloads/)
13. mst_agent_version 테이블 생성

**미완료 (다음 작업):**
- [ ] 서버 app.py Supabase upsert 필드 매핑 수정 (2114행)
      Agent: cpu_usage, memory_usage, disk_usage, network_latency, emr_status
      서버: cpu, memory, disk, network_speed, emr_connection
- [ ] Agent v3.0.0 EXE 빌드 + 서버 업로드 + 버전 등록
- [ ] 미배정 병원 24건 코드 발급
- [ ] Next.js v0 대시보드 (고정 레이아웃)
- [ ] C#/PowerBuilder usage_log 연동
- [ ] 카카오 알림톡 연동
- [ ] 카드리더/바코드스캐너 기종 확인

### 2026-03-12
- 서버 Lightsail 4GB 이전, DNS/SSL 설정
- Nginx 설정, DB 컬럼 확장
- Agent v1.1.0 (HDMI/Touch/VAN/Thermal)

### 2026-03-11
- Widget 공통 파일, UI 개선

## Git
- https://github.com/dolhanboss-han/kiosk-monitor.git (main)

## 2026-03-13 오후 작업 (Agent v3.0.0 테스트 및 수정)

### 완료 항목
1. A4 프린터 SNMP 모니터링 완성
   - 프린터 IP: 192.168.0.25 (Kyocera ECOSYS P3145dn)
   - 토너(TK-3165KS): 44%, 시리얼: RTN1Z06537
   - 카세트 OID 수정: tray1=MP트레이(사용안함), tray2=상단, tray3=하단
   - 용지 잔량은 프린터 펌웨어 추정치 (용지 보충 시 꽉 채워야 정확)

2. 바코드 스캐너 감지 완성
   - POS HID 바코드 스캐너 (VID_0C2E, Honeywell)
   - USB + HIDClass 모두 검색하도록 수정

3. 대시보드(bseye-agent-viewer.html) 수정
   - 카세트 표기: Upper(상단) / Lower(하단)
   - 게이지 색상 역전: 토너/카세트는 낮을수록 빨강 (gaugeColorReverse, setGaugeR)
   - 한글 깨짐 수정

4. 터치스크린 감지 수정 (PowerShell $_ 누락 수정)
5. config.ini 프린터 IP 설정 (192.168.0.25)
6. 전체 장치 활성화 (pc, monitor, printer_a4, printer_thermal, card_reader, barcode_scanner)
7. EMR 체크 비활성화 (불필요)

### 미완료 (다음 작업)
1. HDMI 감지 로직 수정 (Win32_DesktopMonitor ScreenWidth → Win32_VideoController)
2. Thermal 프린터 DLL 로드 문제 (64bit EXE ↔ 32bit DLL 호환성)
3. 서버 app.py Supabase upsert 필드 매핑 수정 (v3 필드 반영)
4. 구버전 에이전트 중지 후 v3 Supabase 검증
5. EXE 자동 업데이트 기능
6. Next.js 서버 대시보드
7. C#/PowerBuilder 연동
8. 카카오 알림톡

### 키오스크 테스트 결과
- PC: CPU 0.5%, 메모리 52.1%, 디스크 19.2% - 정상
- A4 프린터: idle, 토너 44%, 상단 30%, 하단 70% - 정상
- 바코드: POS HID Barcode scanner - 정상
- VAN Agent: KocesICPos.exe running - 정상
- 윈도우 타이틀 감시: kiosk_msys.exe 전체 흐름 기록 완벽
  (Main→수납KeyPad→환자정보→수납방법선택→할부개월선택→수납확인및결제→영수증및처방전출력→Main)
- monitor_hdmi: disconnected (수정 필요)
- monitor_touch: unknown (수정 완료, 재테스트 필요)
- printer_thermal: dll_not_found (수정 필요)

### 파일 현황 (D:\BSEYE\agent-build)
- bseye_agent.py: 진입점 + Windows 서비스
- hw_monitor.py: 하드웨어 모니터링 (SNMP, DLL, PowerShell)
- hook_monitor.py: 윈도우 타이틀 감시
- data_sender.py: 서버 데이터 전송
- device_checker.py: 장치 점검 (웹 API용)
- db_manager.py: 로컬 SQLite 관리
- web_server.py: FastAPI 로컬 대시보드
- config.ini: 설정 파일
- templates/bseye-agent-viewer.html: 대시보드 HTML
