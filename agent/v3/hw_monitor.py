import time, json, os, sys, subprocess, ctypes, ctypes.wintypes, configparser, socket, requests, psutil
from db_manager import save_hw_status, save_heartbeat_cache, save_printer_daily, get_printer_daily

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
        try:
            out = subprocess.check_output(
                'powershell -Command "[Console]::OutputEncoding=[System.Text.Encoding]::UTF8; Get-CimInstance Win32_DesktopMonitor | Select-Object Name,MonitorType,ScreenWidth | ConvertTo-Json"',
                shell=True, timeout=10).decode('utf-8', errors='replace')
            monitors = json.loads(out)
            if isinstance(monitors, dict):
                monitors = [monitors]
            if monitors:
                result['monitor_model'] = monitors[0].get('Name', 'unknown')
                try:
                    vout = subprocess.check_output(
                        'powershell -Command "[Console]::OutputEncoding=[System.Text.Encoding]::UTF8; Get-WmiObject Win32_VideoController | Select-Object VideoModeDescription | ConvertTo-Json"',
                        shell=True, timeout=10).decode('utf-8', errors='replace')
                    vdata = json.loads(vout)
                    if isinstance(vdata, dict):
                        vdata = [vdata]
                    result['monitor_hdmi'] = 'connected' if vdata and vdata[0].get('VideoModeDescription') else 'disconnected'
                except:
                    result['monitor_hdmi'] = 'connected' if monitors[0].get('ScreenWidth') else 'disconnected'
            else:
                result['monitor_model'] = 'unknown'
        except:
            result['monitor_hdmi'] = 'unknown'
            result['monitor_model'] = 'unknown'

        # ?곗튂?⑤꼸
        try:
            out = subprocess.check_output(
                'powershell -Command "[Console]::OutputEncoding=[System.Text.Encoding]::UTF8; Get-PnpDevice -Class HIDClass -Status OK | Where-Object {.FriendlyName -like ''*touch*''} | Select-Object FriendlyName | ConvertTo-Json"',
                shell=True, timeout=10).decode('utf-8', errors='replace')
            if out.strip() and out.strip() != 'null':
                result['monitor_touch'] = 'ok'
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

        except ImportError:
            result['printer_a4'] = 'snmp_not_installed'
        except Exception as e:
            result['printer_a4'] = 'error'
            result['printer_a4_error'] = str(e)

        return result

    # ??? [PRINTER THERMAL] HwaUSB.DLL ???
    def _check_printer_thermal(self):
        result = {}
        dll_path = self.config.get('PRINTER_THERMAL', 'dll_path', fallback='HwaUSB.DLL')
        model = self.config.get('PRINTER_THERMAL', 'model', fallback='HMK-825')

        try:
            dll = ctypes.cdll.LoadLibrary(dll_path)
            open_result = dll.UsbOpen(model.encode('ascii'))
            if open_result != 0:
                result['printer_thermal'] = 'disconnected'
                return result

            status = dll.NewRealRead()
            if status < 0:
                result['printer_thermal'] = 'read_error'
            else:
                # ESC/POS ?명솚 ?곹깭 鍮꾪듃 遺꾩꽍
                result['printer_thermal'] = 'ok'
                result['thermal_cover'] = 'open' if (status & 0x04) else 'closed'
                result['thermal_paper'] = 'empty' if (status & 0x20) else 'ok'
                result['thermal_error'] = 'yes' if (status & 0x40) else 'no'
                if result['thermal_paper'] == 'empty' or result['thermal_error'] == 'yes':
                    result['printer_thermal'] = 'error'
        except OSError:
            result['printer_thermal'] = 'dll_not_found'
        except Exception as e:
            result['printer_thermal'] = 'error'
            result['thermal_error_msg'] = str(e)

        return result

    # ??? [CARD READER] USB ?μ튂 媛먯? ???
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

