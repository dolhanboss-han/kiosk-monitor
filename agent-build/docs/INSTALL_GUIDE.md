# BSEYE Agent 설치 가이드

## 1. 개요

BSEYE Agent는 키오스크 및 서버PC의 하드웨어 상태를 모니터링하여
중앙 서버로 heartbeat 데이터를 전송하는 Windows 에이전트입니다.

### 지원 장치 타입
- **kiosk** : 키오스크 PC (프린터, 바코드, 카드리더, 모니터 등 체크)
- **server** : 서버 PC (프로세스 실행 여부, DB 연결 체크)

---

## 2. 배포 파일 구성

```
deploy/
  bseye-agent.exe          # 메인 에이전트 EXE
  thermal_checker_32.exe   # 감열 프린터 체크 (32비트)
  config.ini               # 설정 파일
  templates/               # 웹 템플릿
  config_kiosk_sample.ini  # 키오스크 설정 예시
  config_server_sample.ini # 서버PC 설정 예시
```

---

## 3. 설치 방법

### 3.1 키오스크 설치

1. deploy 폴더를 USB에 복사
2. 키오스크 PC의 원하는 경로에 복사 (예: `C:\BSEYE\`)
3. `config.ini`를 `config_kiosk_sample.ini` 참고하여 편집
4. 필수 설정:
   ```ini
   [KIOSK_INFO]
   device_type = kiosk

   [SERVER]
   hosp_cd = H001          # 병원코드
   kiosk_id = KIOSK01      # 키오스크 고유 ID
   kiosk_name = 1층 접수    # 표시명
   ```
5. 장치별 on/off:
   ```ini
   [DEVICE_CHECK]
   pc = true
   monitor = true
   printer_a4 = true       # A4 프린터 (SNMP)
   printer_thermal = true  # 감열 프린터 (DLL)
   card_reader = false
   barcode_scanner = true
   ```
6. `bseye-agent.exe` 실행

### 3.2 서버PC 설치

1. deploy 폴더를 서버PC에 복사
2. `config.ini`를 `config_server_sample.ini` 참고하여 편집
3. 필수 설정:
   ```ini
   [KIOSK_INFO]
   device_type = server

   [SERVER]
   hosp_cd = H001
   kiosk_id = SVR01
   kiosk_name = 번호발급서버
   ```
4. 서버 모니터링 설정:
   ```ini
   [SERVER_MONITOR]
   ; 감시할 프로세스 (쉼표 구분, 여러 개 가능)
   process_list = bs_number.exe
   ; DB 연결 체크
   db_type = mssql
   db_host = localhost
   db_port = 1433
   db_check = true
   ```
5. `bseye-agent.exe` 실행

---

## 4. config.ini 섹션별 설명

### [KIOSK_INFO]
| 키 | 설명 | 예시 |
|---|---|---|
| device_type | 장치 타입 (kiosk/server) | kiosk |
| category | 카테고리 | standard |
| monitor_size | 모니터 크기 (인치) | 27 |
| usage_type | 용도 (receipt/payment/certificate/server) | receipt |

### [SERVER]
| 키 | 설명 | 예시 |
|---|---|---|
| server_url | heartbeat API URL | https://monitor.blueswell.co.kr/api/agent/heartbeat |
| usage_url | 이벤트 API URL | https://monitor.blueswell.co.kr/api/agent/events |
| agent_token | 인증 토큰 | bseye-agent-2026 |
| hosp_cd | 병원코드 | H001 |
| kiosk_id | 장치 ID | KIOSK01 |
| heartbeat_interval | 전송 간격 (초) | 30 |

### [DEVICE_CHECK] (키오스크 전용)
| 키 | 설명 | 기본값 |
|---|---|---|
| pc | CPU/메모리/디스크/네트워크 | true |
| monitor | HDMI/터치스크린 | true |
| printer_a4 | A4 프린터 (SNMP) | false |
| printer_thermal | 감열 프린터 (DLL) | false |
| card_reader | 카드리더기 | false |
| barcode_scanner | 바코드 스캐너 | false |

### [PRINTER_A4]
| 키 | 설명 | 예시 |
|---|---|---|
| ip | 프린터 IP | 192.168.0.25 |
| snmp_community | SNMP community | public |

### [PRINTER_THERMAL]
| 키 | 설명 | 예시 |
|---|---|---|
| dll_path | HwaUSB.DLL 경로 | C:\Windows\SysWOW64\HwaUSB.DLL |
| model | 프린터 모델 | HMK-072 |

### [SERVER_MONITOR] (서버PC 전용)
| 키 | 설명 | 예시 |
|---|---|---|
| process_list | 감시 프로세스 (쉼표 구분) | bs_number.exe |
| db_type | DB 종류 (참고용) | mssql |
| db_host | DB 호스트 | localhost |
| db_port | DB 포트 | 1433 |
| db_check | DB 포트 체크 on/off | true |

---

## 5. heartbeat 데이터 필드

### 공통 필드
- `hosp_cd`, `kiosk_id`, `agent_version`, `device_type`
- `cpu_usage`, `memory_usage`, `disk_usage`, `os_version`, `local_ip`
- `network_latency`, `emr_status`

### 키오스크 전용 필드
- `monitor_model`, `monitor_hdmi`, `monitor_touch`
- `printer_a4`, `printer_a4_toner`, `printer_a4_errors`
- `printer_thermal`, `thermal_cover`, `thermal_paper`
- `card_reader`, `barcode_scanner`
- `van_agent_status`

### 서버PC 전용 필드
- `server_processes` : `{"bs_number.exe": "running"}` 형태
- `server_db_status` : `"connected"` 또는 `"disconnected"`

---

## 6. 자동 시작 설정

Windows 작업 스케줄러에 등록하여 부팅 시 자동 실행:

```
schtasks /create /tn "BSEYE Agent" /tr "C:\BSEYE\bseye-agent.exe" /sc onlogon /rl highest
```

---

## 7. 문제 해결

| 증상 | 원인 | 해결 |
|---|---|---|
| thermal: checker_not_found | thermal_checker_32.exe 없음 | deploy 폴더에서 복사 |
| thermal: dll_load_failed | HwaUSB.DLL 로드 실패 | dll_path 확인, 32비트 DLL 설치 |
| printer_a4: offline | SNMP 통신 실패 | 프린터 IP, 네트워크 확인 |
| server_db_status: disconnected | DB 포트 연결 실패 | MSSQL 서비스 상태, 포트 확인 |
| server_processes: stopped | 프로세스 미실행 | 해당 프로그램 시작 |
