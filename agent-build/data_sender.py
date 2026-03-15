import sys, threading, time, os, json, configparser, requests, urllib.request, urllib.error
from db_manager import (
    get_unsent_dates, get_daily_send_data, save_send_result,
    get_unsent_usage, mark_usage_sent,
    get_unsent_heartbeats, mark_heartbeat_sent,
    get_unsent_sessions, get_session_steps, mark_sessions_sent
)

SUPABASE_URL = os.environ.get('SUPABASE_URL', 'https://xzozycbrkdqoztcxbtwa.supabase.co')
SUPABASE_KEY = os.environ.get('SUPABASE_SERVICE_KEY', '')

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
        self.supabase_headers = {
            'Content-Type': 'application/json',
            'apikey': SUPABASE_KEY,
            'Authorization': f'Bearer {SUPABASE_KEY}',
            'Prefer': 'resolution=merge-duplicates',
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
        self._send_sessions()
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

    # ─── 세션 데이터 전송 ───
    def _send_sessions(self):
        unsent = get_unsent_sessions(limit=50)
        if not unsent:
            return

        # 각 세션에 step 데이터 포함
        sessions_payload = []
        for sess in unsent:
            steps = get_session_steps(sess['session_id'])
            sessions_payload.append({
                'kiosk_id': sess['kiosk_id'],
                'hosp_cd': self.hosp_cd,
                'work_date': sess['work_date'],
                'session_id': sess['session_id'],
                'menu_code': sess['menu_code'],
                'start_dt': sess['start_dt'],
                'end_dt': sess['end_dt'],
                'elapsed_sec': sess['elapsed_sec'],
                'result': sess['result'],
                'cancel_step': sess['cancel_step'],
                'steps': [{
                    'step_order': st['step_order'],
                    'step_name': st['step_name'],
                    'start_dt': st['start_dt'],
                    'end_dt': st['end_dt'],
                    'elapsed_sec': st['elapsed_sec'],
                } for st in steps]
            })

        ok_ids = []

        # 1) 서버 API로 전송
        if self.server_url:
            try:
                session_api = self.server_url.rsplit('/', 1)[0] + '/sessions'
                payload = {
                    'hosp_cd': self.hosp_cd,
                    'kiosk_id': self.kiosk_id,
                    'sessions': sessions_payload,
                }
                resp = requests.post(session_api, json=payload, headers=self.headers, timeout=30)
                if resp.status_code == 200:
                    print(f"[Sender] sessions → server: {len(unsent)}건 OK")
                else:
                    print(f"[Sender] sessions → server: FAIL {resp.status_code}")
            except Exception as e:
                print(f"[Sender] sessions → server: FAIL {e}")

        # 2) Supabase 직접 전송
        try:
            supabase_ok = self._send_sessions_to_supabase(unsent)
            if supabase_ok:
                ok_ids = [s['id'] for s in unsent]
        except Exception as e:
            print(f"[Sender] sessions → supabase: FAIL {e}")

        if ok_ids:
            mark_sessions_sent(ok_ids)
            print(f"[Sender] sessions: {len(ok_ids)}건 sent 마킹 완료")

    def _send_sessions_to_supabase(self, sessions):
        """Supabase에 세션 및 스텝 데이터 upsert"""
        # 세션 upsert
        session_rows = [{
            'kiosk_id': s['kiosk_id'],
            'hosp_cd': self.hosp_cd,
            'work_date': s['work_date'],
            'session_id': s['session_id'],
            'menu_code': s['menu_code'],
            'start_dt': s['start_dt'],
            'end_dt': s['end_dt'],
            'elapsed_sec': s['elapsed_sec'],
            'result': s['result'],
            'cancel_step': s['cancel_step'],
        } for s in sessions]

        if not self._supabase_upsert('usg_session_log', session_rows):
            return False

        # 스텝 upsert
        all_steps = []
        for sess in sessions:
            steps = get_session_steps(sess['session_id'])
            for st in steps:
                all_steps.append({
                    'kiosk_id': st['kiosk_id'],
                    'hosp_cd': self.hosp_cd,
                    'session_id': st['session_id'],
                    'step_order': st['step_order'],
                    'step_name': st['step_name'],
                    'start_dt': st['start_dt'],
                    'end_dt': st['end_dt'],
                    'elapsed_sec': st['elapsed_sec'],
                })

        if all_steps:
            if not self._supabase_upsert('usg_step_log', all_steps):
                return False

        print(f"[Sender] sessions → supabase: {len(sessions)}세션, {len(all_steps)}스텝 OK")
        return True

    def _supabase_upsert(self, table, rows):
        """Supabase REST API로 upsert (urllib 사용, requests 의존 최소화)"""
        if not rows:
            return True
        url = f"{SUPABASE_URL}/rest/v1/{table}"
        data = json.dumps(rows, ensure_ascii=False).encode('utf-8')
        req = urllib.request.Request(url, data=data, method='POST')
        for k, v in self.supabase_headers.items():
            req.add_header(k, v)
        try:
            resp = urllib.request.urlopen(req, timeout=30)
            return resp.status in (200, 201)
        except urllib.error.HTTPError as e:
            body = e.read().decode('utf-8', errors='replace')
            print(f"[Sender] supabase {table}: HTTP {e.code} - {body[:200]}")
            return False

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
