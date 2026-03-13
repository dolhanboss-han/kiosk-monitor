import sys, threading, time, os, json, configparser, requests
from db_manager import (
    get_unsent_dates, get_daily_send_data, save_send_result,
    get_unsent_usage, mark_usage_sent,
    get_unsent_heartbeats, mark_heartbeat_sent
)

class DataSender:
    def __init__(self, config):
        self.server_url = config.get('SERVER', 'server_url', fallback='')
        self.usage_url = config.get('SERVER', 'usage_url', fallback='')
        self.agent_token = config.get('SERVER', 'agent_token', fallback='')
        self.hosp_cd = config.get('SERVER', 'hosp_cd', fallback='')
        self.kiosk_id = config.get('SERVER', 'kiosk_id', fallback='')
        self.kiosk_name = config.get('SERVER', 'kiosk_name', fallback='')
        self.send_interval = config.getint('SERVER', 'send_interval', fallback=60)
        self.headers = {
            'Content-Type': 'application/json',
            'X-Agent-Token': self.agent_token
        }
        print(f"[Sender] server: {self.server_url}")
        print(f"[Sender] kiosk: {self.kiosk_id}, interval: {self.send_interval}s")

    def run(self):
        if not self.server_url:
            print("[Sender] no server_url, disabled")
            return
        # 시작 시 미전송 데이터 즉시 전송
        self._send_all()
        while True:
            time.sleep(self.send_interval)
            self._send_all()

    def _send_all(self):
        self._send_events()
        self._send_usage()
        self._retry_heartbeats()

    # ─── 이벤트 로그 (윈도우 타이틀) 전송 ───
    def _send_events(self):
        dates = get_unsent_dates()
        if not dates:
            return
        for work_date in dates:
            try:
                data = get_daily_send_data(work_date)
                payload = {
                    'kiosk_id': self.kiosk_id,
                    'hosp_cd': self.hosp_cd,
                    'kiosk_name': self.kiosk_name,
                    'work_date': work_date,
                    'summary': data['summary'],
                    'logs': data['logs']
                }
                resp = requests.post(self.usage_url, json=payload, headers=self.headers, timeout=30)
                if resp.status_code == 200:
                    result = resp.json().get('result', 'OK')
                    save_send_result(work_date, result, resp.text[:200])
                    print(f"[Sender] events {work_date}: {result}")
                else:
                    save_send_result(work_date, 'FAIL', f"HTTP {resp.status_code}")
                    print(f"[Sender] events {work_date}: FAIL {resp.status_code}")
            except Exception as e:
                save_send_result(work_date, 'FAIL', str(e)[:200])
                print(f"[Sender] events {work_date}: FAIL {e}")
            time.sleep(1)

    # ─── 사용량 로그 (C#/PowerBuilder) 전송 ───
    def _send_usage(self):
        unsent = get_unsent_usage(limit=100)
        if not unsent:
            return
        payload = {
            'hosp_cd': self.hosp_cd,
            'kiosk_id': self.kiosk_id,
            'events': [{
                'complete_dt': r['complete_dt'],
                'age_group': r['age_group'],
                'gender': r['gender']
            } for r in unsent]
        }
        try:
            resp = requests.post(self.usage_url, json=payload, headers=self.headers, timeout=30)
            if resp.status_code == 200:
                ids = [r['id'] for r in unsent]
                mark_usage_sent(ids)
                print(f"[Sender] usage: {len(unsent)}건 전송 OK")
            else:
                print(f"[Sender] usage: FAIL {resp.status_code}")
        except Exception as e:
            print(f"[Sender] usage: FAIL {e}")

    # ─── 실패한 heartbeat 재전송 ───
    def _retry_heartbeats(self):
        unsent = get_unsent_heartbeats(limit=10)
        if not unsent:
            return
        ok_ids = []
        for item in unsent:
            try:
                data = json.loads(item['data_json'])
                resp = requests.post(self.server_url, json=data, headers=self.headers, timeout=15)
                if resp.status_code == 200:
                    ok_ids.append(item['id'])
            except:
                pass
        if ok_ids:
            mark_heartbeat_sent(ok_ids)
            print(f"[Sender] heartbeat retry: {len(ok_ids)}건 성공")

def start_sender_thread(config):
    sender = DataSender(config)
    t = threading.Thread(target=sender.run, daemon=True)
    t.start()
