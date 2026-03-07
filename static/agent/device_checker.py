import psutil, subprocess, os, json, time, configparser

def check_cpu():
    u = psutil.cpu_percent(interval=1)
    return {'item':'CPU','status':'ok' if u<80 else 'warn' if u<95 else 'error','value':f'{u}%',
            'detail':{'usage':u,'cores':psutil.cpu_count(),'threshold':'<80% 정상, 80-95% 주의, >95% 오류'}}

def check_memory():
    m = psutil.virtual_memory()
    return {'item':'메모리','status':'ok' if m.percent<80 else 'warn' if m.percent<95 else 'error','value':f'{m.percent}%',
            'detail':{'total_gb':round(m.total/1024**3,1),'used_gb':round(m.used/1024**3,1),'threshold':'<80% 정상'}}

def check_disk():
    d = psutil.disk_usage('C:\\')
    return {'item':'디스크','status':'ok' if d.percent<85 else 'warn' if d.percent<95 else 'error','value':f'{d.percent}%',
            'detail':{'total_gb':round(d.total/1024**3,1),'free_gb':round(d.free/1024**3,1),'threshold':'<85% 정상'}}

def check_os():
    import platform
    return {'item':'OS','status':'ok','value':platform.platform(),'detail':{}}

def check_network():
    config = configparser.ConfigParser()
    config.read('config.ini', encoding='utf-8')
    url = config.get('SERVER','server_url',fallback='https://monitor.blueswell.co.kr/api/kiosk-usage/receive')
    try:
        import requests
        s = time.time()
        r = requests.get(url.rsplit('/api',1)[0]+'/login', timeout=10)
        ms = round((time.time()-s)*1000)
        return {'item':'네트워크','status':'ok' if ms<1000 else 'warn' if ms<3000 else 'error','value':f'{ms}ms',
                'detail':{'http':r.status_code,'threshold':'<1초 정상'}}
    except Exception as e:
        return {'item':'네트워크','status':'error','value':'연결실패','detail':{'error':str(e)}}

def check_printers():
    results = []
    try:
        out = subprocess.check_output('powershell -Command "Get-Printer | Select Name,PrinterStatus,PortName | ConvertTo-Json"',
                                      shell=True, timeout=10).decode('utf-8',errors='replace')
        printers = json.loads(out)
        if isinstance(printers,dict): printers=[printers]
        for p in printers:
            nm = p.get('Name','')
            st = p.get('PrinterStatus',0)
            stxt = {0:'정상',1:'일시중지',2:'오류',4:'용지걸림',5:'용지부족',6:'토너부족'}.get(st,f'상태:{st}')
            is_th = any(k in nm.lower() for k in ['thermal','receipt','pos','bixolon','sam4s','sewoo'])
            results.append({'item':('영수증' if is_th else 'A4')+f'프린터: {nm}',
                           'status':'ok' if st==0 else 'error','value':stxt,'detail':{'port':p.get('PortName','')}})
    except Exception as e:
        results.append({'item':'프린터','status':'error','value':'점검실패','detail':{'error':str(e)}})
    return results or [{'item':'프린터','status':'warn','value':'없음','detail':{}}]

def check_usb():
    results = []
    try:
        out = subprocess.check_output('powershell -Command "Get-PnpDevice -Class USB -Status OK | Select FriendlyName | ConvertTo-Json"',
                                      shell=True, timeout=10).decode('utf-8',errors='replace')
        devs = json.loads(out)
        if isinstance(devs,dict): devs=[devs]
        bc = cd = False
        for d in devs:
            nm = (d.get('FriendlyName') or '').lower()
            if any(k in nm for k in ['barcode','scanner','honeywell','zebra','datalogic']):
                bc = True; results.append({'item':'바코드리더기','status':'ok','value':d.get('FriendlyName',''),'detail':{}})
            if any(k in nm for k in ['card','reader','smart']):
                cd = True; results.append({'item':'카드리더기','status':'ok','value':d.get('FriendlyName',''),'detail':{}})
        if not bc: results.append({'item':'바코드리더기','status':'warn','value':'미감지(수동확인)','detail':{}})
        if not cd: results.append({'item':'카드리더기','status':'warn','value':'미감지(수동확인)','detail':{}})
    except Exception as e:
        results.append({'item':'USB장치','status':'error','value':str(e),'detail':{}})
    return results

def check_process():
    config = configparser.ConfigParser()
    config.read('config.ini', encoding='utf-8')
    raw = config.get('MONITOR','target_process',fallback='')
    targets = [x.strip().lower() for x in raw.split(',') if x.strip()]
    results = []
    for t in targets:
        found = False
        for p in psutil.process_iter(['name','pid']):
            if p.info['name'] and t in p.info['name'].lower():
                found = True; results.append({'item':f'프로세스: {t}','status':'ok','value':f'PID:{p.info["pid"]}','detail':{}})
                break
        if not found:
            results.append({'item':f'프로세스: {t}','status':'warn','value':'미실행','detail':{'note':'프로그램을 실행하세요'}})
    return results or [{'item':'프로세스','status':'warn','value':'대상 미설정','detail':{}}]

def check_server():
    config = configparser.ConfigParser()
    config.read('config.ini', encoding='utf-8')
    url = config.get('SERVER','server_url',fallback='')
    kid = config.get('SERVER','kiosk_id',fallback='')
    if not url: return [{'item':'서버전송','status':'error','value':'URL 미설정','detail':{}}]
    try:
        import requests
        s = time.time()
        r = requests.post(url, json={'kiosk_id':kid,'work_date':'TEST','summary':{'first_use_time':'00:00','last_use_time':'00:00','total_entry':0,'total_complete':0,'total_cancel':0,'complete_rate':0},'logs':[]}, timeout=15)
        ms = round((time.time()-s)*1000)
        return [{'item':'서버전송','status':'ok' if r.status_code==200 else 'error','value':f'{r.json().get("result","?")} ({ms}ms)','detail':{'url':url}}]
    except Exception as e:
        return [{'item':'서버전송','status':'error','value':'전송실패','detail':{'error':str(e)}}]

def check_monitor():
    import sqlite3
    db = os.path.join(os.path.dirname(os.path.abspath(__file__)),'monitor.db')
    if not os.path.exists(db): return [{'item':'수집현황','status':'error','value':'DB없음','detail':{}}]
    conn = sqlite3.connect(db)
    today = time.strftime('%Y-%m-%d')
    t = conn.execute("SELECT count(*) FROM event_log WHERE date(timestamp)=?",(today,)).fetchone()[0]
    s = conn.execute("SELECT count(*) FROM event_log WHERE date(timestamp)=? AND status='START'",(today,)).fetchone()[0]
    conn.close()
    return [{'item':'수집현황','status':'ok' if t>0 else 'warn','value':f'총{t}건 (진입:{s})','detail':{'date':today}}]

def run_all():
    r = [check_cpu(),check_memory(),check_disk(),check_os(),check_network()]
    r.extend(check_printers()); r.extend(check_usb()); r.extend(check_process())
    r.extend(check_server()); r.extend(check_monitor())
    return r

def run_category(cat):
    m = {'pc':lambda:[check_cpu(),check_memory(),check_disk(),check_os()],'network':lambda:[check_network()],
         'printer':check_printers,'usb':check_usb,'process':check_process,'server':check_server,'monitor':check_monitor}
    return m.get(cat,run_all)()
