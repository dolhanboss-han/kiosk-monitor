import sys, threading, time, os, configparser, requests
from db_manager import get_unsent_dates, get_daily_send_data, save_send_result

SERVER_URL = ''
KIOSK_ID = ''
HOSP_CD = ''
KIOSK_NAME = ''
SEND_INTERVAL = 60
RETRY = 300

def load_config():
    global SERVER_URL, KIOSK_ID, HOSP_CD, KIOSK_NAME, SEND_INTERVAL, RETRY
    config = configparser.ConfigParser()
    config.read(os.path.join(os.path.dirname(sys.executable) if getattr(sys,"frozen",False) else os.path.dirname(os.path.abspath(__file__)),'config.ini'), encoding='utf-8')
    SERVER_URL = config.get('SERVER','server_url',fallback='')
    KIOSK_ID = config.get('SERVER','kiosk_id',fallback='')
    HOSP_CD = config.get("SERVER","hosp_cd",fallback="")
    KIOSK_NAME = config.get("SERVER","kiosk_name",fallback="")
    SEND_INTERVAL = config.getint('SERVER','send_interval',fallback=60)
    RETRY = config.getint('SERVER','retry_interval',fallback=300)
    print(f"[Sender] server: {SERVER_URL}")
    print(f"[Sender] kiosk: {KIOSK_ID}, interval: {SEND_INTERVAL}s")

def send_one_date(work_date):
    data = get_daily_send_data(work_date)
    payload = {'kiosk_id': KIOSK_ID, 'hosp_cd': HOSP_CD, 'kiosk_name': KIOSK_NAME, 'work_date': work_date, 'summary': data['summary'], 'logs': data['logs']}
    try:
        resp = requests.post(SERVER_URL, json=payload, timeout=30)
        result = resp.json().get('result','ERROR')
        save_send_result(work_date, result, resp.text[:200])
        print(f"[Sender] {work_date}: {result}")
        return result
    except Exception as e:
        save_send_result(work_date, 'FAIL', str(e)[:200])
        print(f"[Sender] {work_date}: FAIL - {e}")
        return 'FAIL'

def send_all():
    dates = get_unsent_dates()
    if not dates:
        return False
    for d in dates:
        send_one_date(d)
        time.sleep(1)
    return True

def sender_loop():
    load_config()
    if not SERVER_URL or not KIOSK_ID:
        print("[Sender] no config, disabled")
        return
    send_all()
    while True:
        time.sleep(SEND_INTERVAL)
        send_all()

def start_sender_thread():
    t = threading.Thread(target=sender_loop, daemon=True)
    t.start()
