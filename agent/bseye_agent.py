#!/usr/bin/env python3
"""BSEYE Agent v2.0.0 - Windows Service + Local DB + Usage Sync"""
import os, sys, time, json, socket, platform, subprocess, logging, sqlite3
import psutil, requests
import configparser
from datetime import datetime, timedelta

AGENT_VERSION = '2.0.0'

# ===== CONFIG =====
def load_config():
    base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    cfg_path = os.path.join(base_dir, 'agent_config.ini')
    defaults = {
        'server_url': 'https://monitor.blueswell.co.kr/api/agent/heartbeat',
        'usage_url': 'https://monitor.blueswell.co.kr/api/agent/usage',
        'agent_token': 'bseye-agent-2026',
        'hosp_cd': '000',
        'kiosk_id': 'TEST01',
        'interval': 30,
        'usage_sync_interval': 300,
        'log_file': 'agent.log',
        'local_db': 'bseye_local.db',
        'local_keep_days': 7,
        'local_max_mb': 500,
    }
    if os.path.exists(cfg_path):
        cfg = configparser.ConfigParser()
        cfg.read(cfg_path, encoding='utf-8')
        if cfg.has_section('settings'):
            for key in defaults:
                if isinstance(defaults[key], int):
                    defaults[key] = cfg.getint('settings', key, fallback=defaults[key])
                else:
                    defaults[key] = cfg.get('settings', key, fallback=defaults[key])
    return defaults

CONFIG = load_config()

# ===== LOGGING =====
log_path = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), CONFIG['log_file'])
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.FileHandler(log_path, encoding='utf-8'), logging.StreamHandler()]
)
log = logging.getLogger('bseye_agent')

# ===== LOCAL DB =====
def get_local_db():
    base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    db_path = os.path.join(base_dir, CONFIG['local_db'])
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute('''CREATE TABLE IF NOT EXISTS heartbeat_cache (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data TEXT NOT NULL,
        created_at TEXT DEFAULT (datetime('now','localtime')),
        sent INTEGER DEFAULT 0,
        sent_at TEXT
    )''')
    conn.execute('''CREATE TABLE IF NOT EXISTS usage_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        hosp_cd TEXT,
        kiosk_id TEXT,
        work_date TEXT,
        log_dt TEXT,
        proc_name TEXT,
        window_title TEXT,
        class_name TEXT,
        status TEXT,
        elapsed_sec REAL,
        created_at TEXT DEFAULT (datetime('now','localtime')),
        sent INTEGER DEFAULT 0,
        sent_at TEXT
    )''')
    conn.execute('''CREATE TABLE IF NOT EXISTS usage_session (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        hosp_cd TEXT,
        kiosk_id TEXT,
        work_date TEXT,
        session_id TEXT,
        menu_code TEXT,
        start_dt TEXT,
        end_dt TEXT,
        elapsed_sec REAL,
        result TEXT,
        cancel_step TEXT,
        created_at TEXT DEFAULT (datetime('now','localtime')),
        sent INTEGER DEFAULT 0,
        sent_at TEXT
    )''')
    conn.commit()
    return conn

def cleanup_local_db():
    """전송 완료된 오래된 데이터 삭제 + 용량 체크"""
    try:
        db = get_local_db()
        cutoff = (datetime.now() - timedelta(days=CONFIG['local_keep_days'])).strftime('%Y-%m-%d')
        
        for table in ['heartbeat_cache', 'usage_log', 'usage_session']:
            db.execute(f"DELETE FROM {table} WHERE sent=1 AND created_at < ?", (cutoff,))
        db.commit()
        
        # DB 용량 체크
        base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        db_path = os.path.join(base_dir, CONFIG['local_db'])
        size_mb = os.path.getsize(db_path) / (1024 * 1024)
        if size_mb > CONFIG['local_max_mb']:
            # 전송 완료된 가장 오래된 데이터부터 삭제
            for table in ['heartbeat_cache', 'usage_log', 'usage_session']:
                db.execute(f"DELETE FROM {table} WHERE sent=1")
            db.execute("VACUUM")
            db.commit()
            log.warning(f"DB 용량 초과 ({size_mb:.0f}MB), 전송완료 데이터 전체 삭제")
        
        db.close()
    except Exception as e:
        log.error(f"DB 정리 실패: {e}")

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

# ===== PRINTER =====
def check_printer(name='A4'):
    try:
        result = subprocess.run(['wmic', 'printer', 'get', 'name,status'],
            capture_output=True, text=True, timeout=5)
        if 'OK' in result.stdout or 'Idle' in result.stdout: return 'ok'
        return 'warning'
    except: return 'unknown'

def check_network_printer(ip, port=9100, timeout=3):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        s.connect((ip, port))
        s.close()
        return 'ok'
    except socket.timeout: return 'timeout'
    except ConnectionRefusedError: return 'refused'
    except: return 'offline'

def load_network_printers():
    base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    cfg_path = os.path.join(base_dir, 'agent_config.ini')
    printers = []
    if os.path.exists(cfg_path):
        cfg = configparser.ConfigParser()
        cfg.read(cfg_path, encoding='utf-8')
        if cfg.has_section('network_printer'):
            for name, val in cfg.items('network_printer'):
                parts = val.split(',')
                if len(parts) >= 2:
                    printers.append({
                        'name': name,
                        'ip': parts[0].strip(),
                        'port': int(parts[1].strip()),
                        'snmp': parts[2].strip().lower() == 'true' if len(parts) > 2 else False
                    })
    if not printers:
        printers = [
            {'ip': '192.168.0.6', 'name': 'Printer_A', 'port': 9100},
            {'ip': '192.168.0.20', 'name': 'Printer_B', 'port': 9100, 'snmp': True},
        ]
    return printers

NETWORK_PRINTERS = load_network_printers()

def check_all_network_printers():
    results = {}
    for p in NETWORK_PRINTERS:
        status = check_network_printer(p['ip'], p['port'])
        results[p['name']] = {'ip': p['ip'], 'status': status}
    return results

# ===== DEVICE =====
def check_device(keyword):
    try:
        result = subprocess.run(['wmic', 'path', 'Win32_PnPEntity', 'where',
            f"Name like '%{keyword}%'", 'get', 'status'],
            capture_output=True, text=True, timeout=5)
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

# ===== HARDWARE MONITORING =====
def check_monitor_hdmi():
    try:
        result = subprocess.run(
            ['wmic', 'path', 'Win32_DesktopMonitor', 'get', 'Availability,Status'],
            capture_output=True, text=True, timeout=5)
        if 'OK' in result.stdout or '3' in result.stdout:
            return 'connected'
        result2 = subprocess.run(
            ['wmic', 'path', 'Win32_PnPEntity', 'where', "PNPClass='Monitor'", 'get', 'Status'],
            capture_output=True, text=True, timeout=5)
        if 'OK' in result2.stdout:
            return 'connected'
        return 'disconnected'
    except: return 'unknown'

def check_monitor_touch():
    try:
        result = subprocess.run(
            ['wmic', 'path', 'Win32_PnPEntity', 'where', "Name like '%touch%'", 'get', 'Name,Status'],
            capture_output=True, text=True, timeout=5)
        lines = [l.strip() for l in result.stdout.strip().split('\n') if l.strip() and 'Name' not in l]
        if not lines: return 'not_found'
        for line in lines:
            if 'OK' in line: return 'ok'
            if 'Error' in line: return 'error'
        return 'unknown'
    except: return 'unknown'

def check_monitor_model():
    try:
        result = subprocess.run(
            ['wmic', 'desktopmonitor', 'get', 'Name,ScreenWidth,ScreenHeight'],
            capture_output=True, text=True, timeout=5)
        lines = [l.strip() for l in result.stdout.strip().split('\n') if l.strip() and 'Name' not in l]
        if lines: return lines[0].split()[0] if lines[0] else ''
        return ''
    except: return ''

def check_van_agents():
    config_path = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), 'agent_config.ini')
    van_processes = {}
    if os.path.exists(config_path):
        try:
            cfg = configparser.ConfigParser()
            cfg.read(config_path, encoding='utf-8')
            if cfg.has_section('watch_process'):
                for key, val in cfg.items('watch_process'):
                    for proc_name in val.split(','):
                        proc_name = proc_name.strip()
                        if proc_name:
                            van_processes[proc_name] = 'stopped'
        except: pass
    if not van_processes: return {}
    try:
        result = subprocess.run(['tasklist', '/FO', 'CSV', '/NH'],
            capture_output=True, text=True, timeout=5)
        running = result.stdout.lower()
        for proc_name in van_processes:
            if proc_name.lower() in running:
                van_processes[proc_name] = 'running'
    except: pass
    return van_processes

def check_thermal_printer():
    result = {'paper': 'unknown', 'detail': {}}
    try:
        r = subprocess.run(
            ['wmic', 'printer', 'where',
             "Name like '%thermal%' or Name like '%receipt%' or Name like '%POS%'",
             'get', 'Name,PrinterStatus,WorkOffline'],
            capture_output=True, text=True, timeout=5)
        lines = [l.strip() for l in r.stdout.strip().split('\n') if l.strip() and 'Name' not in l]
        if lines:
            result['detail']['name'] = lines[0].split('  ')[0] if lines[0] else ''
            if 'TRUE' in r.stdout.upper():
                result['paper'] = 'offline'
            else:
                result['paper'] = 'ok'
        else:
            result['paper'] = 'not_found'
    except:
        result['paper'] = 'unknown'
    return result

# ===== COLLECT & SEND =====
def collect_status():
    thermal = check_thermal_printer()  # 1회만 호출
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
        'agent_version': AGENT_VERSION,
        'monitor_hdmi': check_monitor_hdmi(),
        'monitor_touch': check_monitor_touch(),
        'monitor_model': check_monitor_model(),
        'van_agent_status': check_van_agents(),
        'thermal_paper': thermal['paper'],
        'thermal_detail': thermal['detail'],
        'os_version': get_os_version(),
        'ip_local': get_local_ip()
    }

def send_heartbeat():
    """상태 수집 → 로컬 DB 저장 → 서버 전송"""
    data = collect_status()
    
    # 로컬 DB에 항상 저장
    try:
        db = get_local_db()
        db.execute("INSERT INTO heartbeat_cache (data) VALUES (?)", (json.dumps(data, ensure_ascii=False),))
        db.commit()
        db.close()
    except Exception as e:
        log.error(f"로컬 DB 저장 실패: {e}")
    
    # 서버 전송 시도
    try:
        r = requests.post(CONFIG['server_url'], json=data,
            headers={'X-Agent-Token': CONFIG['agent_token']}, timeout=10)
        result = r.json()
        log.info(f"OK CPU:{data['cpu']}% MEM:{data['memory']}% DISK:{data['disk']}% alerts:{result.get('alerts',0)}")
        
        # 전송 성공 → 로컬 캐시 최신 1건 sent 처리
        try:
            db = get_local_db()
            db.execute("UPDATE heartbeat_cache SET sent=1, sent_at=datetime('now','localtime') WHERE sent=0 ORDER BY id DESC LIMIT 1")
            db.commit()
            db.close()
        except: pass
        
        return True
    except Exception as e:
        log.error(f"전송 실패 (로컬 저장됨): {e}")
        return False

def retry_unsent():
    """미전송 데이터 재전송"""
    try:
        db = get_local_db()
        rows = db.execute("SELECT id, data FROM heartbeat_cache WHERE sent=0 ORDER BY id ASC LIMIT 10").fetchall()
        if not rows:
            db.close()
            return
        
        sent_ids = []
        for row in rows:
            try:
                data = json.loads(row['data'])
                r = requests.post(CONFIG['server_url'], json=data,
                    headers={'X-Agent-Token': CONFIG['agent_token']}, timeout=10)
                if r.status_code == 200:
                    sent_ids.append(row['id'])
            except:
                break  # 서버 연결 안 되면 중단
        
        if sent_ids:
            placeholders = ','.join(['?'] * len(sent_ids))
            db.execute(f"UPDATE heartbeat_cache SET sent=1, sent_at=datetime('now','localtime') WHERE id IN ({placeholders})", sent_ids)
            db.commit()
            log.info(f"미전송 재전송: {len(sent_ids)}건 성공")
        
        db.close()
    except Exception as e:
        log.error(f"재전송 실패: {e}")

def sync_usage():
    """로컬 사용량 데이터 서버 전송"""
    try:
        db = get_local_db()
        
        # usage_log 미전송 데이터
        rows = db.execute("SELECT * FROM usage_log WHERE sent=0 ORDER BY id ASC LIMIT 100").fetchall()
        if not rows:
            db.close()
            return
        
        payload = []
        ids = []
        for row in rows:
            ids.append(row['id'])
            payload.append({
                'hosp_cd': row['hosp_cd'],
                'kiosk_id': row['kiosk_id'],
                'work_date': row['work_date'],
                'log_dt': row['log_dt'],
                'proc_name': row['proc_name'],
                'window_title': row['window_title'],
                'class_name': row['class_name'],
                'status': row['status'],
                'elapsed_sec': row['elapsed_sec'],
            })
        
        r = requests.post(CONFIG['usage_url'], json={
            'hosp_cd': CONFIG['hosp_cd'],
            'kiosk_id': CONFIG['kiosk_id'],
            'events': payload
        }, headers={'X-Agent-Token': CONFIG['agent_token']}, timeout=15)
        
        if r.status_code == 200:
            placeholders = ','.join(['?'] * len(ids))
            db.execute(f"UPDATE usage_log SET sent=1, sent_at=datetime('now','localtime') WHERE id IN ({placeholders})", ids)
            db.commit()
            log.info(f"사용량 전송: {len(ids)}건 성공")
        
        db.close()
    except Exception as e:
        log.error(f"사용량 전송 실패: {e}")

# ===== WINDOWS SERVICE =====
try:
    import win32serviceutil, win32service, win32event, servicemanager
    HAS_WIN32 = True
except ImportError:
    HAS_WIN32 = False

if HAS_WIN32:
    class BSEYEAgentService(win32serviceutil.ServiceFramework):
        _svc_name_ = 'BSEYEAgent'
        _svc_display_name_ = 'BSEYE Kiosk Monitor Agent'
        _svc_description_ = 'BSEYE 키오스크 모니터링 에이전트 v2.0 - 상태 수집, 사용량 전송, 로컬 DB 캐시'

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
            log.info(f'=== BSEYE Agent v{AGENT_VERSION} 서비스 시작 ===')
            loop_count = 0
            usage_interval = CONFIG['usage_sync_interval'] // CONFIG['interval']
            cleanup_interval = 3600 // CONFIG['interval']  # 1시간마다
            
            while self.running:
                send_heartbeat()
                loop_count += 1
                
                # 미전송 재전송 (매 5회)
                if loop_count % 5 == 0:
                    retry_unsent()
                
                # 사용량 전송 (주기적)
                if loop_count % usage_interval == 0:
                    sync_usage()
                
                # DB 정리 (1시간마다)
                if loop_count % cleanup_interval == 0:
                    cleanup_local_db()
                
                rc = win32event.WaitForSingleObject(self.stop_event, CONFIG['interval'] * 1000)
                if rc == win32event.WAIT_OBJECT_0:
                    break
            log.info(f'=== BSEYE Agent v{AGENT_VERSION} 서비스 종료 ===')

# ===== MAIN =====
def main():
    log.info(f'=== BSEYE Agent v{AGENT_VERSION} 시작 ===')
    log.info(f"병원: {CONFIG['hosp_cd']}, 키오스크: {CONFIG['kiosk_id']}")
    log.info(f"서버: {CONFIG['server_url']}")
    log.info(f"주기: {CONFIG['interval']}초, 사용량전송: {CONFIG['usage_sync_interval']}초")
    log.info(f"로컬DB: {CONFIG['local_db']}, 보관: {CONFIG['local_keep_days']}일, 최대: {CONFIG['local_max_mb']}MB")
    
    loop_count = 0
    usage_interval = max(1, CONFIG['usage_sync_interval'] // CONFIG['interval'])
    cleanup_interval = max(1, 3600 // CONFIG['interval'])
    
    while True:
        send_heartbeat()
        loop_count += 1
        
        if loop_count % 5 == 0:
            retry_unsent()
        
        if loop_count % usage_interval == 0:
            sync_usage()
        
        if loop_count % cleanup_interval == 0:
            cleanup_local_db()
        
        time.sleep(CONFIG['interval'])

if __name__ == '__main__':
    if len(sys.argv) > 1 and HAS_WIN32:
        win32serviceutil.HandleCommandLine(BSEYEAgentService)
    else:
        main()
