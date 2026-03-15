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

## 2026-03-14 작업

### 완료
1. V0 대시보드 완성 (Next.js 16 + Supabase) - 6단계 + 세션 퍼널
2. API Routes 8개 (dashboard, kiosks, hospitals, alerts, stats, isv-summary, events, settings)
3. ISV 공급현황 차트 + 진입/이탈 퍼널 차트
4. Supabase Pro 업그레이드, usg_session_log/usg_step_log 테이블 생성
5. Agent hook_monitor.py 세션 로직 추가, EXE 빌드 완료
6. SQLite→Supabase 이벤트 이관 (usg_event_log)

### 오후 추가 완료
7. app.py Supabase upsert 필드 매핑 수정 (v3 8컬럼 추가) - 완료
8. mon_kiosk_status 컬럼 8개 추가 (printer_a4_toner 등) - 완료
9. 키오스크 EXE 배포 및 테스트 - 완료
   - HDMI: connected (정상)
   - 터치스크린: ok - HID-compliant touch screen (정상)
   - A4 프린터: idle, 토너44%, 상단30%, 하단70% (정상)
   - 바코드: POS HID Barcode scanner (정상)
   - VAN Agent: KocesICPos.exe running (정상)
   - Thermal: dll_load_failed (미해결 - 32bit DLL + 64bit EXE 문제)
   - EMR: disconnected (COM DLL 방식이라 TCP 체크 부정확)
10. hw_monitor.py HDMI/터치/Thermal DLL 로드 로직 수정 + EXE 재빌드
11. data_sender.py 세션 전송 로직 추가 (_send_sessions, _supabase_upsert)
12. config.ini VAN Agent = KocesICPos.exe 변경
13. SNMP 용지걸림 감지 방법 확인 (hrPrinterDetectedErrorState 비트5)
14. PowerBuilder EMR COM DLL 연동 구조 파악 (prjAUTORCPTK.clsAUTORCPTK)

### 미완료 (향후)
- [ ] Thermal DLL 문제 해결 (32bit 별도 프로세스 또는 별도 EXE 방안)
- [ ] EMR 상태 모니터링 방식 결정 (COM DLL 체크 vs 로그 모니터링, 협의 필요)
- [ ] 세션 로직 실사용 테스트 (수납 진행 시 session_log 기록 확인)
- [ ] SNMP 용지걸림 감지 + 알람 + 키오스크 차단 연동
- [ ] Vercel 대시보드 배포
- [ ] 미배정 병원 24건 코드 발급
- [ ] Agent 자동 업데이트 기능 검증
- [ ] C#/PowerBuilder usage_log 연동
- [ ] 카카오 알림톡 연동
- [ ] 전체 병원 450대 순차 배포


### 2026-03-14 오후 추가 완료
7. app.py Supabase upsert 필드 매핑 수정 (v3 8컬럼 추가)
8. mon_kiosk_status 컬럼 8개 추가 (printer_a4_toner, cassette_upper/lower, total/today_pages, os_version, local_ip, barcode_scanner)
9. /api/agent/events 엔드포인트 추가 (이벤트 수신 + SQLite + Supabase 동기화)
10. /api/agent/sessions 엔드포인트 추가 (세션 수신 + Supabase upsert)
11. 키오스크 EXE 배포 및 테스트 결과:
    - HDMI: connected (정상)
    - 터치스크린: ok - HID-compliant touch screen (정상)
    - A4 프린터: idle, 토너44%, 상단30%, 하단70%, 누적4193매 (정상)
    - 바코드: POS HID Barcode scanner (정상)
    - VAN Agent: KocesICPos.exe running (정상)
    - Thermal: dll_load_failed (미해결 - PyInstaller frozen 환경)
    - EMR: disconnected (COM DLL 방식이라 TCP 체크 부정확)
12. hw_monitor.py 수정:
    - HDMI: Win32_VideoController VideoModeDescription 사용
    - 터치: *touch*/*터치* 매칭
    - Thermal: os.add_dll_directory + winmode=0 (여전히 실패)
    - SNMP 용지걸림 감지 추가 (hrPrinterDetectedErrorState 비트마스크 파싱)
    - 프린터 상태 폴링 스레드 (printing 시 2초간격, jammed 즉시 알람)
13. data_sender.py 세션 전송 로직 추가 (_send_sessions, _supabase_upsert)
14. config.ini VAN Agent = KocesICPos.exe 변경
15. 수납 플로우 완벽 기록 확인:
    Main→수납KeyPad→환자정보→수납KeyPad→할부개월→수납확인결제(19초)→영수증출력(15초)→Main
16. PowerBuilder EMR COM DLL 구조 파악 (prjAUTORCPTK.clsAUTORCPTK / GetChargeInfo)

### 새로 확인된 요구사항
- Windows Server PC 모니터링: 자동순번(bs_number.exe) + 전자처방전
  - device_type=server, MSSQL TCP 1433 체크
  - 대형병원 100%, 중소병원 15% (전자처방전 의무화로 확대 중)
- 프린터 출력 매수 검증 (방안B): PowerBuilder→Agent API에 출력장수 전달, 전후 누적매수 비교

### 미완료 (향후 우선순위)
- [ ] 키오스크 Agent 재시작 → [Sender] events OK 확인
- [ ] Thermal DLL 해결 (별도 subprocess 또는 32bit EXE 분리)
- [ ] Vercel 대시보드 배포
- [ ] 세션 로직 실사용 테스트 (session_log 완료/이탈 기록 확인)
- [ ] Windows Server PC Agent 모드 구현 (device_type=server)
- [ ] SNMP 용지걸림 → 카카오 알림톡 연동
- [ ] 프린터 출력 매수 검증 (방안B, PowerBuilder 연동)
- [ ] 미배정 병원 24건 코드 발급
- [ ] Agent 자동 업데이트 기능 검증
- [ ] C#/PowerBuilder usage_log 직접 연동
- [ ] 전체 병원 450대 순차 배포

## 프린터 출력 매수 검증 설계

### 문제
- 키오스크 수납 시 영수증/처방전 등 3장 출력 요청
- 2장만 나오고 1장이 걸리면 고객이 모르고 계속 진행 -> 부작용 발생
- 가장 빈번한 유지보수 이슈

### SNMP로 확인 가능한 정보
- 누적 출력 매수: prtMarkerLifeCount (OID 1.3.6.1.2.1.43.10.2.1.4.1.1)
- 프린터 상태: hrPrinterStatus (1=other, 2=unknown, 3=idle, 4=printing, 5=warmup)
- 에러 상태: hrPrinterDetectedErrorState (비트마스크)
  - Bit 0: lowPaper, Bit 1: noPaper, Bit 2: lowToner, Bit 3: noToner
  - Bit 4: doorOpen, Bit 5: jammed, Bit 6: offline, Bit 7: serviceRequested

### 방안 A: 프린터 상태 폴링 (현재 구현됨)
- 키오스크 프로그램 연동 불필요
- Agent가 hrPrinterStatus를 평시 30초, printing 감지 시 2초 간격 폴링
- printing(4) 시작 -> 누적매수 기록 -> idle(3) 복귀 -> 누적매수 재조회 -> 증가분 기록
- 중간에 jammed 감지 시 즉시 알람 생성
- 한계: 원래 몇 장이어야 하는지 모름 -> 부족분 감지 불가
- 용지 걸림(jammed)만 즉시 감지 가능

### 방안 B: 키오스크 프로그램 연동 (정확한 감지, 향후 구현)
- PowerBuilder/C#에서 출력 시 Agent 로컬 API에 출력 정보 전달
- API: POST http://localhost:8080/api/print-job
- 요청 본문 예시:
  job_type: receipt
  expected_pages: 3
  patient_id: 12345
  timestamp: 2026-03-14 18:34:21
- Agent 처리 흐름:
  1. 요청 수신 -> SNMP로 현재 누적매수 기록 (예: 4193)
  2. 프린터 상태 2초 간격 폴링 시작
  3. idle 복귀 -> 누적매수 재조회 (예: 4195)
  4. 증가분(2) vs 요청(3) 비교 -> 1장 부족 감지
  5. 부족 시 알람 생성 + 카카오 알림톡 발송
  6. 결과 저장: print_job_log 테이블
- 필요 작업: PowerBuilder에 HTTP POST 호출 코드 추가
- PowerBuilder 예시: OLEObject MSXML2.XMLHTTP -> Open POST localhost:8080/api/print-job -> Send JSON

### 현재 상태
- 방안 A 구현 완료 (hw_monitor.py _monitor_print_job 스레드)
- 방안 B는 C#/PowerBuilder 연동 시 구현 예정
- 병원 전산실/ISV와 협의 필요

### 관련 테이블 (향후 추가)
- print_job_log: job_id, kiosk_id, job_type, expected_pages, actual_pages, result(ok/shortage/jammed), timestamp

### 2026-03-15 오전 작업

### 완료
1. [Sender] events 404 해결 - config.ini usage_url을 /api/agent/events로 수정
2. Thermal 프린터 DLL 완전 해결
   - thermal_checker_32.exe (32비트 별도 EXE) 빌드
   - 32비트 Python 3.12.9 설치 (C:\Python312-32)
   - DLL 로드 성공, 프린터 상태: ok, paper: normal, cover: closed
3. A4 프린터 SNMP 에러 파싱 수정 (bytes 타입 처리)
   - printer_a4: idle, errors: [], jammed: false
4. 프린터 모델 수정: HMK-825 -> HMK-072 (실제 장비 확인)
5. 64비트 thermal_checker.exe 제거, 32비트만 사용
6. config.ini 동기화 (usage_url, model)
7. 로컬 대시보드 색상 수정 (thermal paper normal -> 초록색)
8. /api/agent/events, /api/agent/sessions 엔드포인트 추가 (어제)
9. EMR 로그 경로 확인: C:\MsystechHIS_Ver.2\KIOSK_NSS\LOG   - 성공 키워드: OCS/EMR[msys] 사용가능
   - 향후 로그 파일 모니터링 방식으로 EMR 체크 구현 예정

### 키오스크 최종 상태 (192.168.0.11)
- HDMI: connected
- 터치스크린: ok (HID-compliant touch screen)
- A4 프린터: idle, 토너44%, 상단30%, 하단70%, errors:[], jammed:false
- 영수증 프린터: ok, paper:normal, cover:closed
- 바코드: ok (POS HID Barcode scanner)
- VAN Agent: KocesICPos.exe running
- 이벤트 전송: OK
- EMR: disconnected (개발 키오스크, 정상)

### deploy 폴더 구성
- bseye-agent.exe (22.7MB)
- thermal_checker_32.exe (6.5MB)
- config.ini
- templates/bseye-agent-viewer.html

### 미완료
- [ ] 프린터 jammed 시 키오스크 화면 차단 구현
- [ ] Vercel 대시보드 배포
- [ ] EMR 로그 모니터링 구현 (실제 병원 배포 시)
- [ ] Windows Server PC Agent 모드 (device_type=server)
- [ ] 카카오 알림톡 연동
- [ ] 전체 병원 450대 순차 배포


## 2026-03-15 (2차 작업)

### 완료
1. events 404 해결: config.ini usage_url → /api/agent/events 변경
2. Thermal DLL 32bit 해결: thermal_checker_32.exe 빌드, 64bit 제거
3. A4 프린터 SNMP 파싱 수정: bytes→int 변환 (printer_a4: idle, errors:[], jammed:false)
4. 프린터 모델 수정: HMK-825 → HMK-072
5. 로컬 대시보드 한글 깨짐 수정: 이모지→텍스트, UTF-8 BOM
6. 프린터 잼 화면차단: printer_status.txt, thermal_status.txt 자동 갱신
7. 출력 매수 검증: print_request.txt 감지 확인 (실출력 테스트 내일)
8. EMR 로그 모니터링: log_file 방식 구현, emr_status.txt 생성
9. 서버 PC Agent 모드: device_type=server, process/DB 체크 구현
10. 자동 업데이트: update-check API, download API, 3.0.0→3.0.2 자동 업데이트 검증 완료
11. 설치 스크립트: bseye-installer.bat (서버에서 파일 다운로드+config 설정+서비스 등록)
12. 서버 API: /api/agent/update-check, /api/agent/download/<filename> 추가
13. API 추가: /api/printer-status, /api/emr-status, /api/print-result

### Agent v3.0.2 deploy 파일
- bseye-agent.exe: 22.68 MB
- thermal_checker_32.exe: 6.49 MB
- config.ini, config_kiosk_sample.ini, config_server_sample.ini
- bseye-installer.bat
- templates/bseye-agent-viewer.html

### 키오스크 최종 상태 (192.168.0.11)
- Agent: v3.0.2, 자동 업데이트 동작 확인
- HDMI: connected, 터치: ok
- A4 프린터: idle, 토너44%, 상단30%, 하단70%, jammed:false
- 영수증 프린터: ok, paper:normal, cover:closed
- 바코드: ok, VAN: running
- EMR: unknown (개발 키오스크)
- 이벤트 전송: OK
- 프린터 상태 파일: printer_status.txt=OK, thermal_status.txt=OK

### 내일 작업
1. 출력 매수 검증 실출력 테스트
2. Vercel 대시보드 배포
3. 카카오 알림톡 연동
4. 미배정 병원 24건 코드 발급
5. 전체 병원 450대 순차 배포


## 2026-03-15 (3차 작업 - 설치 자동화)

### 완료
1. install.bat 생성: 더블클릭 한 번으로 전체 설치 (서버에서 파일 다운로드)
2. bseye-installer.bat 완성: 20개 설정 항목 입력, CMD echo 방식 config.ini 생성 (BOM 없는 UTF-8)
3. 서버 API 추가: /api/agent/update-check, /api/agent/download (하위폴더 검색 포함)
4. 자동 업데이트 검증: 3.0.0 → 3.0.2 자동 다운로드+교체+재시작 성공
5. data_sender.py: 버전 하드코딩 제거, bseye_agent.py에서 VERSION 전달
6. 파일명 버그 수정: bseye-agent.exe_new.exe → bseye-agent_new.exe
7. schtasks 등록: "bseye-agent.exe debug" 파라미터 포함
8. INSTALL_GUIDE.html 전체 재작성: Step 1~6, 서버PC, 자동업데이트, 문제해결, 파일구성
9. config 주석 영문 전환 (CMD 인코딩 호환)
10. install.bat 영문 전환 (CMD 한글 깨짐 해결)
11. 서버 download API: templates 하위폴더 파일 검색 지원

### 설치 흐름 (최종)
1. install.bat 더블클릭 (관리자 권한)
2. 서버에서 파일 자동 다운로드
3. 20개 설정 입력 (기본값 Enter)
4. config.ini 자동 생성
5. schtasks 자동 등록
6. INSTALL_GUIDE.html 보면서 config 확인
7. bseye-agent.exe debug 실행
8. http://localhost:8080 대시보드 확인
9. 모든 항목 초록색 확인 후 Ctrl+C
10. PC 재부팅 → 자동 시작 확인

### 배포 파일 목록 (서버 deploy)
- bseye-agent.exe: 22.68 MB
- thermal_checker_32.exe: 6.49 MB
- config.ini, config_kiosk_sample.ini, config_server_sample.ini
- bseye-installer.bat, install.bat
- INSTALL_GUIDE.html, INSTALL_GUIDE.md
- templates/bseye-agent-viewer.html

### 내일 작업
1. 출력 매수 검증 실출력 테스트
2. Vercel 대시보드 배포
3. 카카오 알림톡 연동
4. 미배정 병원 24건 코드 발급
5. 전체 병원 450대 순차 배포


### 결정사항
- Vercel 대시보드 작업을 Claude Code로 통합 (토큰 효율화)
- v0에서 만든 디자인 스타일(Next.js 16 + shadcn/ui + Recharts 6)을 Claude Code에서 유지하며 개발
- 프로젝트 경로: D:\BSEYE\ZIP\20260314_DASHBOARD
- 대시보드 추가 반영 항목:
  1. device_type (kiosk/server) 구분 표시
  2. printer_a4_errors, printer_a4_jammed 표시
  3. thermal_cover, thermal_paper, thermal_error 표시
  4. emr_status 표시
  5. server_processes, server_db_status (서버PC)
  6. 출력 매수 검증 결과
  7. 알림 목록 페이지 (jammed, shortage 등)
  8. 서버PC 현황 페이지
  9. 설치 현황 (병원별 Agent 버전, 마지막 heartbeat)
  10. 출력 매수 검증 로그 페이지
