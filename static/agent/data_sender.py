import threading, time, os, configparser, requests
from db_manager import get_unsent_dates, get_daily_send_data, save_send_result

SERVER_URL = ''
KIOSK_ID = ''
SEND_TIME = '08:00'
RETRY = 300

def load_config():
    global SERVER_URL, KIOSK_ID, SEND_TIME, RETRY
    config = configparser.ConfigParser()
    config.read(os.path.join(os.path.dirname(os.path.abspath(__file__)),'config.ini'), encoding='utf-8')
    SERVER_URL = config.get('SERVER','server_url',fallback='')
    KIOSK_ID = config.get('SERVER','kiosk_id',fallback='')
    SEND_TIME = config.get('SERVER','send_time',fallback='08:00')
    RETRY = config.getint('SERVER','retry_interval',fallback=300)
    print(f"[Sender] server: {SERVER_URL}")
    print(f"[Sender] kiosk: {KIOSK_ID}, time: {SEND_TIME}")

def send_one_date(work_date):
    data = get_daily_send_data(work_date)
    payload = {'kiosk_id': KIOSK_ID, 'work_date': work_date, 'summary': data['summary'], 'logs': data['logs']}
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
        print("[Sender] no unsent data")
        return
    for d in dates:
        send_one_date(d)
        time.sleep(1)

def sender_loop():
    load_config()
    if not SERVER_URL or not KIOSK_ID:
        print("[Sender] no config, disabled")
        return
    send_all()
    while True:
        now = time.strftime('%H:%M')
        if now == SEND_TIME:
            send_all()
            time.sleep(61)
        time.sleep(30)

def start_sender_thread():
    t = threading.Thread(target=sender_loop, daemon=True)
    t.start()
