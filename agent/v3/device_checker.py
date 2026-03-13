import psutil, subprocess, os, json, time, configparser, sys

if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def _load_config():
    config = configparser.ConfigParser()
    config.read(os.path.join(BASE_DIR, 'config.ini'), encoding='utf-8')
    return config

def check_cpu():
    u = psutil.cpu_percent(interval=1)
    return {'item': 'CPU', 'status': 'ok' if u < 80 else 'warn' if u < 95 else 'error', 'value': f'{u}%'}

def check_memory():
    m = psutil.virtual_memory()
    return {'item': 'Memory', 'status': 'ok' if m.percent < 80 else 'warn' if m.percent < 95 else 'error', 'value': f'{m.percent}%'}

def check_disk():
    d = psutil.disk_usage('C:\\')
    return {'item': 'Disk', 'status': 'ok' if d.percent < 85 else 'warn' if d.percent < 95 else 'error', 'value': f'{d.percent}%'}

def check_os_info():
    import platform
    return {'item': 'OS', 'status': 'ok', 'value': platform.platform()}

def check_network():
    config = _load_config()
    url = config.get('SERVER', 'server_url', fallback='')
    if not url:
        return {'item': 'Network', 'status': 'error', 'value': 'URL not set'}
    try:
        import requests
        s = time.time()
        requests.get(url.rsplit('/api', 1)[0] + '/login', timeout=10)
        ms = round((time.time() - s) * 1000)
        return {'item': 'Network', 'status': 'ok' if ms < 1000 else 'warn', 'value': f'{ms}ms'}
    except:
        return {'item': 'Network', 'status': 'error', 'value': 'Failed'}

def check_printers():
    results = []
    try:
        out = subprocess.check_output(
            'powershell -Command "Get-Printer | Select Name,PrinterStatus | ConvertTo-Json"',
            shell=True, timeout=10).decode('utf-8', errors='replace')
        printers = json.loads(out)
        if isinstance(printers, dict):
            printers = [printers]
        for p in printers:
            nm = p.get('Name', '')
            st = p.get('PrinterStatus', 0)
            results.append({'item': f'Printer: {nm}', 'status': 'ok' if st == 0 else 'error', 'value': f'status:{st}'})
    except Exception as e:
        results.append({'item': 'Printer', 'status': 'error', 'value': str(e)})
    return results or [{'item': 'Printer', 'status': 'warn', 'value': 'None'}]

def check_usb():
    results = []
    config = _load_config()
    card_kw = [k.strip().lower() for k in config.get('CARD_READER', 'device_keyword', fallback='card,reader').split(',')]
    barcode_kw = [k.strip().lower() for k in config.get('BARCODE_SCANNER', 'device_keyword', fallback='barcode,scanner').split(',')]
    try:
        out = subprocess.check_output(
            'powershell -Command "Get-PnpDevice -Class USB -Status OK | Select FriendlyName | ConvertTo-Json"',
            shell=True, timeout=10).decode('utf-8', errors='replace')
        devs = json.loads(out)
        if isinstance(devs, dict):
            devs = [devs]
        bc = cd = False
        for d in devs:
            nm = (d.get('FriendlyName') or '').lower()
            if any(k in nm for k in barcode_kw):
                bc = True
                results.append({'item': 'Barcode', 'status': 'ok', 'value': d.get('FriendlyName', '')})
            if any(k in nm for k in card_kw):
                cd = True
                results.append({'item': 'Card Reader', 'status': 'ok', 'value': d.get('FriendlyName', '')})
        if not bc:
            results.append({'item': 'Barcode', 'status': 'warn', 'value': 'Not detected'})
        if not cd:
            results.append({'item': 'Card Reader', 'status': 'warn', 'value': 'Not detected'})
    except Exception as e:
        results.append({'item': 'USB', 'status': 'error', 'value': str(e)})
    return results

def check_process():
    config = _load_config()
    raw = config.get('MONITOR_SETTING', 'target_process', fallback='')
    targets = [x.strip().lower() for x in raw.split(',') if x.strip()]
    results = []
    for t in targets:
        found = any(t in (p.info['name'] or '').lower() for p in psutil.process_iter(['name']))
        results.append({'item': f'Process: {t}', 'status': 'ok' if found else 'warn', 'value': 'Running' if found else 'Not found'})
    return results or [{'item': 'Process', 'status': 'warn', 'value': 'No target'}]

def check_monitor_log():
    from db_manager import get_today_summary
    s = get_today_summary()
    total = s.get('total', 0)
    return [{'item': 'Monitor Log', 'status': 'ok' if total > 0 else 'warn', 'value': f'Total:{total} Start:{s.get("starts",0)}'}]

def run_all():
    r = [check_cpu(), check_memory(), check_disk(), check_os_info(), check_network()]
    r.extend(check_printers())
    r.extend(check_usb())
    r.extend(check_process())
    r.extend(check_monitor_log())
    return r

def run_category(cat):
    m = {
        'pc': lambda: [check_cpu(), check_memory(), check_disk(), check_os_info()],
        'network': lambda: [check_network()],
        'printer': check_printers,
        'usb': check_usb,
        'process': check_process,
        'monitor': check_monitor_log
    }
    return m.get(cat, run_all)()
