import time, json, os, sys, subprocess, configparser, socket, requests, psutil, threading
from db_manager import save_hw_status, save_heartbeat_cache, save_printer_daily, get_printer_daily, insert_alarm

if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class HWMonitor:
    def __init__(self, config):
        self.config = config
        self.server_url = config.get('SERVER', 'server_url', fallback='')
        self.agent_token = config.get('SERVER', 'agent_token', fallback='')
        self.hosp_cd = config.get('SERVER', 'hosp_cd', fallback='')
        self.kiosk_id = config.get('SERVER', 'kiosk_id', fallback='')
        self.interval = config.getint('SERVER', 'heartbeat_interval', fallback=30)
        self.version = '3.0.0'

        # DEVICE_CHECK on/off
        self.chk_pc = config.getboolean('DEVICE_CHECK', 'pc', fallback=True)
        self.chk_monitor = config.getboolean('DEVICE_CHECK', 'monitor', fallback=True)
        self.chk_printer_a4 = config.getboolean('DEVICE_CHECK', 'printer_a4', fallback=False)
        self.chk_printer_thermal = config.getboolean('DEVICE_CHECK', 'printer_thermal', fallback=False)
        self.chk_card_reader = config.getboolean('DEVICE_CHECK', 'card_reader', fallback=False)
        self.chk_barcode = config.getboolean('DEVICE_CHECK', 'barcode_scanner', fallback=False)

    def run(self):
        print(f"[HW] started (interval={self.interval}s)")
        # A4 프린터 폴링 스레드 시작 (별도 스레드)
        if self.chk_printer_a4:
            t = threading.Thread(target=self._monitor_print_job, daemon=True)
            t.start()
        while True:
            try:
                data = self.collect_all()
                save_hw_status(json.dumps(data, ensure_ascii=False))
                self.send_heartbeat(data)
            except Exception as e:
                print(f"[HW] error: {e}")
            time.sleep(self.interval)

    # ??? ?섏쭛 ???
    def collect_all(self):
        data = {
            'hosp_cd': self.hosp_cd,
            'kiosk_id': self.kiosk_id,
            'agent_version': self.version
        }
        if self.chk_pc:
            data.update(self._check_pc())
        if self.chk_monitor:
            data.update(self._check_monitor())
        if self.chk_printer_a4:
            data.update(self._check_printer_a4())
        if self.chk_printer_thermal:
            data.update(self._check_printer_thermal())
        if self.chk_card_reader:
            data.update(self._check_card_reader())
        if self.chk_barcode:
            data.update(self._check_barcode())
        # VAN Agent
        data['van_agent_status'] = self._check_van_agent()
        return data

    # ??? [PC] CPU, 硫붾え由? ?붿뒪?? OS, IP, ?ㅽ듃?뚰겕 ???
    def _check_pc(self):
        result = {}
        try:
            result['cpu_usage'] = psutil.cpu_percent(interval=1)
            result['memory_usage'] = psutil.virtual_memory().percent
            result['disk_usage'] = psutil.disk_usage('C:\\').percent
            import platform
            result['os_version'] = platform.platform()
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            try:
                s.connect(('8.8.8.8', 80))
                result['local_ip'] = s.getsockname()[0]
            finally:
                s.close()
        except Exception as e:
            result['pc_error'] = str(e)

        # ?ㅽ듃?뚰겕 ?묐떟?띾룄
        try:
            start = time.time()
            requests.get(self.server_url.rsplit('/api', 1)[0] + '/login', timeout=10)
            result['network_latency'] = f"{round((time.time() - start) * 1000)}ms"
        except:
            result['network_latency'] = 'timeout'

        # EMR ?곌껐
        emr_host = self.config.get('NETWORK', 'emr_host', fallback='127.0.0.1')
        emr_port = self.config.getint('NETWORK', 'emr_port', fallback=7000)
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(3)
            s.connect((emr_host, emr_port))
            s.close()
            result['emr_status'] = 'connected'
        except:
            result['emr_status'] = 'disconnected'

        return result

    # ??? [MONITOR] HDMI, ?곗튂, 紐⑤뜽紐????
    def _check_monitor(self):
        result = {}

        # 모니터 모델명
        try:
            out = subprocess.check_output(
                'powershell -Command "[Console]::OutputEncoding=[System.Text.Encoding]::UTF8; Get-CimInstance Win32_DesktopMonitor | Select-Object Name,MonitorType | ConvertTo-Json"',
                shell=True, timeout=10).decode('utf-8', errors='replace')
            monitors = json.loads(out)
            if isinstance(monitors, dict):
                monitors = [monitors]
            if monitors:
                result['monitor_model'] = monitors[0].get('Name', 'unknown')
            else:
                result['monitor_model'] = 'unknown'
        except:
            result['monitor_model'] = 'unknown'

        # HDMI 감지: Win32_VideoController의 VideoModeDescription으로 판단
        try:
            vout = subprocess.check_output(
                'powershell -Command "[Console]::OutputEncoding=[System.Text.Encoding]::UTF8; Get-WmiObject Win32_VideoController | Select-Object VideoModeDescription | ConvertTo-Json"',
                shell=True, timeout=10).decode('utf-8', errors='replace')
            vdata = json.loads(vout)
            if isinstance(vdata, dict):
                vdata = [vdata]
            result['monitor_hdmi'] = 'connected' if vdata and vdata[0].get('VideoModeDescription') else 'disconnected'
        except:
            result['monitor_hdmi'] = 'unknown'

        # 터치스크린 감지: HID 터치 장치 ("HID 규격 터치 스크린" 포함)
        try:
            out = subprocess.check_output(
                'powershell -Command "[Console]::OutputEncoding=[System.Text.Encoding]::UTF8;'
                " Get-PnpDevice -Class HIDClass -Status OK"
                " | Where-Object {$_.FriendlyName -like '*touch*' -or $_.FriendlyName -like '*터치*'}"
                ' | Select-Object FriendlyName | ConvertTo-Json"',
                shell=True, timeout=10).decode('utf-8', errors='replace')
            if out.strip() and out.strip() != 'null':
                touch_data = json.loads(out)
                if isinstance(touch_data, dict):
                    touch_data = [touch_data]
                result['monitor_touch'] = 'ok'
                result['monitor_touch_name'] = touch_data[0].get('FriendlyName', '') if touch_data else ''
            else:
                result['monitor_touch'] = 'not_detected'
        except:
            result['monitor_touch'] = 'unknown'

        return result

    # ??? [PRINTER A4] SNMP - 援먯꽭??P3045DN ???
    def _check_printer_a4(self):
        result = {}
        ip = self.config.get('PRINTER_A4', 'ip', fallback='')
        community = self.config.get('PRINTER_A4', 'snmp_community', fallback='public')
        if not ip:
            result['printer_a4'] = 'not_configured'
            return result

        try:
            from pysnmp.hlapi import (
                getCmd, SnmpEngine, CommunityData, UdpTransportTarget,
                ContextData, ObjectType, ObjectIdentity
            )

            def snmp_get(oid):
                iterator = getCmd(
                    SnmpEngine(), CommunityData(community),
                    UdpTransportTarget((ip, 161), timeout=5, retries=1),
                    ContextData(), ObjectType(ObjectIdentity(oid))
                )
                error_indication, error_status, error_index, var_binds = next(iterator)
                if error_indication or error_status:
                    return None
                return var_binds[0][1]

            # ?꾨┛???곹깭
            status_val = snmp_get('1.3.6.1.2.1.25.3.5.1.1.1')
            status_map = {1: 'other', 2: 'unknown', 3: 'idle', 4: 'printing', 5: 'warmup'}
            result['printer_a4'] = status_map.get(int(status_val), 'error') if status_val else 'offline'

            # ?좊꼫 ?붾웾
            toner_max = snmp_get('1.3.6.1.2.1.43.11.1.1.8.1.1')
            toner_cur = snmp_get('1.3.6.1.2.1.43.11.1.1.9.1.1')
            if toner_max and toner_cur and int(toner_max) > 0:
                result['printer_a4_toner'] = round(int(toner_cur) / int(toner_max) * 100)
            else:
                result['printer_a4_toner'] = -1

            # 移댁꽭?? ?⑹?
            cas1_max = snmp_get('1.3.6.1.2.1.43.8.2.1.9.1.2')
            cas1_cur = snmp_get('1.3.6.1.2.1.43.8.2.1.10.1.2')
            # 移댁꽭?? ?꾩옱??OID媛 ?ㅻ? ???덉쓬, ?곗꽑 ?숈씪 OID ?ъ슜
            if cas1_max and int(cas1_max) > 0:
                result['printer_a4_cassette_upper'] = round(int(cas1_cur) / int(cas1_max) * 100)
            else:
                result['printer_a4_cassette_upper'] = -1

            # 移댁꽭?? ?⑹?
            cas2_max = snmp_get('1.3.6.1.2.1.43.8.2.1.9.1.3')
            cas2_cur = snmp_get('1.3.6.1.2.1.43.8.2.1.10.1.3')
            if cas2_max and int(cas2_max) > 0:
                result['printer_a4_cassette_lower'] = round(int(cas2_cur) / int(cas2_max) * 100)
            else:
                result['printer_a4_cassette_lower'] = -1

            # ?꾩쟻 留ㅼ닔
            total_pages = snmp_get('1.3.6.1.2.1.43.10.2.1.4.1.1')
            result['printer_a4_total_pages'] = int(total_pages) if total_pages else 0

            # ?ㅻ뒛 ?ъ슜??怨꾩궛
            today = time.strftime('%Y-%m-%d')
            total_now = result['printer_a4_total_pages']
            daily = get_printer_daily(today)
            if daily:
                result['printer_a4_today'] = max(0, total_now - daily['prev_total'])
            else:
                save_printer_daily(today, 0, total_now)
                result['printer_a4_today'] = 0
            save_printer_daily(today, result.get('printer_a4_today', 0), total_now)

            # hrPrinterDetectedErrorState 비트마스크 파싱
            error_state = snmp_get('1.3.6.1.2.1.25.3.5.1.2.1')
            if error_state is not None:
                try:
                    if isinstance(error_state, bytes):
                        err_byte = int.from_bytes(error_state, 'big')
                    elif isinstance(error_state, int):
                        err_byte = error_state
                    else:
                        # pysnmp OctetString 등 → bytes 변환
                        err_byte = int.from_bytes(bytes(error_state), 'big')
                    error_bits = [
                        (0, 'lowPaper'), (1, 'noPaper'), (2, 'lowToner'), (3, 'noToner'),
                        (4, 'doorOpen'), (5, 'jammed'), (6, 'offline'), (7, 'serviceRequested'),
                    ]
                    detected = [name for bit, name in error_bits if err_byte & (1 << bit)]
                    result['printer_a4_errors'] = detected
                    result['printer_a4_jammed'] = 'jammed' in detected
                except Exception as e:
                    print(f"[HW] errorState parse failed: {type(error_state).__name__}={error_state!r} err={e}")
                    result['printer_a4_errors'] = []
                    result['printer_a4_jammed'] = False
            else:
                result['printer_a4_errors'] = []
                result['printer_a4_jammed'] = False

        except ImportError:
            result['printer_a4'] = 'snmp_not_installed'
        except Exception as e:
            result['printer_a4'] = 'error'
            result['printer_a4_error'] = str(e)

        return result

    # ─── [PRINTER THERMAL] subprocess → thermal_checker_32.exe ───
    def _check_printer_thermal(self):
        result = {}
        exe_path = os.path.join(BASE_DIR, 'thermal_checker_32.exe')

        proc = None
        if os.path.exists(exe_path):
            try:
                proc = subprocess.run(
                    [exe_path], capture_output=True, timeout=10, text=True, cwd=BASE_DIR
                )
            except (subprocess.TimeoutExpired, OSError) as e:
                print(f"[HW] thermal_checker_32.exe failed: {e}")
                proc = None

        if proc is None:
            result['printer_thermal'] = 'checker_not_found'
            result['thermal_error_msg'] = f'thermal_checker_32.exe not found: {exe_path}'
            print("[HW] thermal: checker_not_found")
            return result

        # subprocess 결과 처리
        try:
            if proc.returncode != 0:
                result['printer_thermal'] = 'checker_error'
                result['thermal_error_msg'] = proc.stderr.strip() if proc.stderr else f'exit code {proc.returncode}'
                return result

            data = json.loads(proc.stdout.strip())
            status = data.get('status', 'error')

            if status == 'ok':
                result['printer_thermal'] = 'ok'
                result['thermal_cover'] = data.get('cover', 'unknown')
                result['thermal_paper'] = data.get('paper', 'unknown')
                result['thermal_error'] = data.get('error', 'unknown')
            elif status == 'dll_load_failed':
                result['printer_thermal'] = 'dll_load_failed'
                result['thermal_error_msg'] = data.get('message', 'unknown')
                result['thermal_bit'] = data.get('bit', 'unknown')
            elif status == 'error':
                msg = data.get('message', 'unknown')
                if msg == 'disconnected':
                    result['printer_thermal'] = 'disconnected'
                else:
                    result['printer_thermal'] = 'error'
                    result['thermal_error_msg'] = msg
            else:
                result['printer_thermal'] = status
                result['thermal_cover'] = data.get('cover', 'unknown')
                result['thermal_paper'] = data.get('paper', 'unknown')
                result['thermal_error'] = data.get('error', 'unknown')

        except json.JSONDecodeError as e:
            result['printer_thermal'] = 'parse_error'
            result['thermal_error_msg'] = f'JSON parse error: {e}'
        except Exception as e:
            result['printer_thermal'] = 'error'
            result['thermal_error_msg'] = str(e)

        return result

    # ??? [CARD READER] USB ?μ튂 媛먯? ???
    # ─── [PRINTER A4] SNMP 폴링: 인쇄 감지 + 잼 알람 ───
    def _get_snmp_fn(self):
        """pysnmp 기반 snmp_get 함수 반환 (import 1회)"""
        ip = self.config.get('PRINTER_A4', 'ip', fallback='')
        community = self.config.get('PRINTER_A4', 'snmp_community', fallback='public')
        if not ip:
            return None

        try:
            from pysnmp.hlapi import (
                getCmd, SnmpEngine, CommunityData, UdpTransportTarget,
                ContextData, ObjectType, ObjectIdentity
            )
        except ImportError:
            return None

        engine = SnmpEngine()

        def snmp_get(oid):
            iterator = getCmd(
                engine, CommunityData(community),
                UdpTransportTarget((ip, 161), timeout=5, retries=1),
                ContextData(), ObjectType(ObjectIdentity(oid))
            )
            error_indication, error_status, _, var_binds = next(iterator)
            if error_indication or error_status:
                return None
            return var_binds[0][1]

        return snmp_get

    def _monitor_print_job(self):
        """별도 스레드: 프린터 상태 폴링 (idle=30s, printing=2s)"""
        OID_STATUS = '1.3.6.1.2.1.25.3.5.1.1.1'
        OID_ERROR = '1.3.6.1.2.1.25.3.5.1.2.1'
        OID_PAGES = '1.3.6.1.2.1.43.10.2.1.4.1.1'
        STATUS_MAP = {1: 'other', 2: 'unknown', 3: 'idle', 4: 'printing', 5: 'warmup'}

        print("[HW] print job monitor started")

        snmp_get = self._get_snmp_fn()
        if not snmp_get:
            print("[HW] print job monitor: SNMP not available, exiting")
            return

        poll_interval = 30
        was_printing = False
        pages_before = None

        while True:
            try:
                status_val = snmp_get(OID_STATUS)
                status = int(status_val) if status_val else 0
                status_name = STATUS_MAP.get(status, 'unknown')

                if status == 4 and not was_printing:
                    # printing 시작 감지
                    was_printing = True
                    poll_interval = 2
                    p = snmp_get(OID_PAGES)
                    pages_before = int(p) if p else None
                    print(f"[HW] print job: PRINTING started (pages={pages_before})")

                elif status == 4 and was_printing:
                    # printing 중 - 잼 체크
                    err_val = snmp_get(OID_ERROR)
                    if err_val is not None:
                        err_byte = int(err_val)
                        if err_byte & (1 << 5):  # bit5 = jammed
                            print("[HW] print job: JAMMED detected!")
                            insert_alarm(
                                alarm_type='printer_a4_jammed',
                                severity='critical',
                                message='A4 프린터 용지 걸림 감지',
                                detail_json=json.dumps({
                                    'kiosk_id': self.kiosk_id,
                                    'hosp_cd': self.hosp_cd,
                                    'pages_before': pages_before,
                                }, ensure_ascii=False),
                            )

                elif status != 4 and was_printing:
                    # printing -> idle 복귀
                    was_printing = False
                    poll_interval = 30
                    p = snmp_get(OID_PAGES)
                    pages_after = int(p) if p else None
                    printed = (pages_after - pages_before) if pages_after and pages_before else 0
                    print(f"[HW] print job: IDLE (printed={printed} pages)")

                    # 오늘 사용량 갱신
                    if pages_after:
                        today = time.strftime('%Y-%m-%d')
                        daily = get_printer_daily(today)
                        if daily:
                            today_pages = max(0, pages_after - daily['prev_total'])
                            save_printer_daily(today, today_pages, pages_after)

            except Exception as e:
                print(f"[HW] print job monitor error: {e}")
                poll_interval = 30
                was_printing = False

            time.sleep(poll_interval)

    # ─── [CARD READER] USB 장치 감지 ───
    def _check_card_reader(self):
        result = {}
        keywords = self.config.get('CARD_READER', 'device_keyword', fallback='card,reader,smart')
        keywords = [k.strip().lower() for k in keywords.split(',')]
        try:
            out = subprocess.check_output(
                'powershell -Command "Get-PnpDevice -Status OK | Select-Object FriendlyName,Class | ConvertTo-Json"',
                shell=True, timeout=10).decode('utf-8', errors='replace')
            devs = json.loads(out)
            if isinstance(devs, dict):
                devs = [devs]
            found = False
            for d in devs:
                nm = (d.get('FriendlyName') or '').lower()
                if any(k in nm for k in keywords):
                    result['card_reader'] = 'ok'
                    result['card_reader_name'] = d.get('FriendlyName', '')
                    found = True
                    break
            if not found:
                result['card_reader'] = 'not_detected'
        except Exception as e:
            result['card_reader'] = 'error'
            result['card_reader_error'] = str(e)
        return result

    # ??? [BARCODE SCANNER] USB ?μ튂 媛먯? ???
    def _check_barcode(self):
        result = {}
        keywords = self.config.get('BARCODE_SCANNER', 'device_keyword', fallback='barcode,scanner')
        keywords = [k.strip().lower() for k in keywords.split(',')]
        try:
            out = subprocess.check_output(
                'powershell -Command "Get-PnpDevice -Status OK | Select-Object FriendlyName,Class | ConvertTo-Json"',
                shell=True, timeout=10).decode('utf-8', errors='replace')
            devs = json.loads(out)
            if isinstance(devs, dict):
                devs = [devs]
            found = False
            for d in devs:
                nm = (d.get('FriendlyName') or '').lower()
                if any(k in nm for k in keywords):
                    result['barcode_scanner'] = 'ok'
                    result['barcode_scanner_name'] = d.get('FriendlyName', '')
                    found = True
                    break
            if not found:
                result['barcode_scanner'] = 'not_detected'
        except Exception as e:
            result['barcode_scanner'] = 'error'
            result['barcode_error'] = str(e)
        return result

    # ??? [VAN AGENT] ?꾨줈?몄뒪 媛먯떆 ???
    def _check_van_agent(self):
        processes = self.config.get('VAN_AGENT', 'process', fallback='')
        targets = [p.strip() for p in processes.split(',') if p.strip()]
        if not targets:
            return {}
        result = {}
        for target in targets:
            found = False
            for proc in psutil.process_iter(['name']):
                if proc.info['name'] and target.lower() in proc.info['name'].lower():
                    found = True
                    break
            result[target] = 'running' if found else 'stopped'
        return result

    # ??? heartbeat ?꾩넚 ???
    def send_heartbeat(self, data):
        if not self.server_url:
            return
        try:
            headers = {
                'Content-Type': 'application/json',
                'X-Agent-Token': self.agent_token
            }
            resp = requests.post(self.server_url, json=data, headers=headers, timeout=15)
            if resp.status_code == 200:
                print(f"[HW] heartbeat sent OK")
            else:
                print(f"[HW] heartbeat failed: {resp.status_code}")
                save_heartbeat_cache(json.dumps(data, ensure_ascii=False))
        except Exception as e:
            print(f"[HW] heartbeat error: {e}")
            save_heartbeat_cache(json.dumps(data, ensure_ascii=False))

