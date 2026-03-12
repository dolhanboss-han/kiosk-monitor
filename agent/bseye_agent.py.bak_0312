#!/usr/bin/env python3
"""BSEYE Agent - Windows Service Version"""
import os, sys, time, json, socket, platform, subprocess, logging
import psutil, requests

# ===== CONFIG =====
CONFIG = {
    'server_url': 'https://monitor.blueswell.co.kr/api/agent/heartbeat',
    'agent_token': 'bseye-agent-2026',
    'hosp_cd': '000',
    'kiosk_id': 'TEST01',
    'interval': 30,
    'log_file': 'agent.log'
}

# ===== LOGGING =====
log_path = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), CONFIG['log_file'])
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.FileHandler(log_path, encoding='utf-8'), logging.StreamHandler()]
)
log = logging.getLogger('bseye_agent')

# ===== SYSTEM INFO =====
def get_cpu(): return psutil.cpu_percent(interval=1)
def get_memory(): return psutil.virtual_memory().percent
def get_disk():
    try: return psutil.disk_usage('C:\\').percent
    except: return 0
def get_os_version(): return f"{platform.system()} {platform.release()} {platform.machine()}"
def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except: return '0.0.0.0'

def check_printer(name='A4'):
    try:
        result = subprocess.run(['wmic', 'printer', 'get', 'name,status'], capture_output=True, text=True, timeout=5)
        if 'OK' in result.stdout or 'Idle' in result.stdout: return 'ok'
        return 'warning'
    except: return 'unknown'

def check_network_printer(ip, port=9100, timeout=3):
    """네트워크 프린터 상태 체크 (TCP 포트 연결)"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        s.connect((ip, port))
        s.close()
        return 'ok'
    except socket.timeout:
        return 'timeout'
    except ConnectionRefusedError:
        return 'refused'
    except:
        return 'offline'

# 네트워크 프린터 목록 (IP, 이름)
NETWORK_PRINTERS = [
    {'ip': '192.168.0.6', 'name': 'Printer_A', 'port': 9100},
    {'ip': '192.168.0.20', 'name': 'Printer_B', 'port': 9100},
]

def check_all_network_printers():
    """모든 네트워크 프린터 상태 반환"""
    results = {}
    for p in NETWORK_PRINTERS:
        status = check_network_printer(p['ip'], p['port'])
        results[p['name']] = {'ip': p['ip'], 'status': status}
    return results

def check_device(keyword):
    try:
        result = subprocess.run(['wmic', 'path', 'Win32_PnPEntity', 'where', f"Name like '%{keyword}%'", 'get', 'status'], capture_output=True, text=True, timeout=5)
        if 'OK' in result.stdout: return 'ok'
        return 'unknown'
    except: return 'unknown'

def check_network():
    try:
        start = time.time()
        requests.get('https://monitor.blueswell.co.kr/api/health', timeout=5)
        ms = round((time.time() - start) * 1000, 1)
        return ms
    except: return 0

def check_emr():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(3)
        s.connect(('127.0.0.1', 7000))
        s.close()
        return 'ok'
    except: return 'unknown'

def collect_status():
    return {
        'hosp_cd': CONFIG['hosp_cd'],
        'kiosk_id': CONFIG['kiosk_id'],
        'status': 'online',
        'cpu': get_cpu(),
        'memory': get_memory(),
        'disk': get_disk(),
        'printer_a4': check_printer('A4'),
        'printer_thermal': check_printer('Thermal'),
        'network_printers': check_all_network_printers(),
        'card_reader': check_device('Card Reader'),
        'barcode_reader': check_device('Barcode'),
        'network_speed': check_network(),
        'emr_connection': check_emr(),
        'agent_version': '1.0.0',
        'os_version': get_os_version(),
        'ip_local': get_local_ip()
    }

def send_heartbeat():
    try:
        data = collect_status()
        r = requests.post(CONFIG['server_url'], json=data,
            headers={'X-Agent-Token': CONFIG['agent_token']}, timeout=10)
        result = r.json()
        log.info(f"OK CPU:{data['cpu']}% MEM:{data['memory']}% DISK:{data['disk']}% alerts:{result.get('alerts',0)}")
    except Exception as e:
        log.error(f"전송 실패: {e}")

# ===== WINDOWS SERVICE =====
try:
    import win32serviceutil
    import win32service
    import win32event
    import servicemanager
    HAS_WIN32 = True
except ImportError:
    HAS_WIN32 = False

if HAS_WIN32:
    class BSEYEAgentService(win32serviceutil.ServiceFramework):
        _svc_name_ = 'BSEYEAgent'
        _svc_display_name_ = 'BSEYE Kiosk Monitor Agent'
        _svc_description_ = 'BSEYE 키오스크 모니터링 에이전트 - 상태 수집 및 서버 전송'

        def __init__(self, args):
            win32serviceutil.ServiceFramework.__init__(self, args)
            self.stop_event = win32event.CreateEvent(None, 0, 0, None)
            self.running = True

        def SvcStop(self):
            self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
            win32event.SetEvent(self.stop_event)
            self.running = False

        def SvcDoRun(self):
            servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                servicemanager.PYS_SERVICE_STARTED, (self._svc_name_, ''))
            log.info('=== BSEYE Agent 서비스 시작 ===')
            while self.running:
                send_heartbeat()
                rc = win32event.WaitForSingleObject(self.stop_event, CONFIG['interval'] * 1000)
                if rc == win32event.WAIT_OBJECT_0:
                    break
            log.info('=== BSEYE Agent 서비스 종료 ===')

# ===== MAIN =====
def main():
    log.info(f'=== BSEYE Agent v1.0.0 시작 ===')
    log.info(f"병원: {CONFIG['hosp_cd']}, 키오스크: {CONFIG['kiosk_id']}")
    log.info(f"서버: {CONFIG['server_url']}")
    log.info(f"주기: {CONFIG['interval']}초")
    while True:
        send_heartbeat()
        time.sleep(CONFIG['interval'])

if __name__ == '__main__':
    if len(sys.argv) > 1 and HAS_WIN32:
        win32serviceutil.HandleCommandLine(BSEYEAgentService)
    else:
        main()
