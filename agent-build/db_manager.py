import sqlite3, os, sys, time, configparser

if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_PATH = os.path.join(BASE_DIR, 'monitor.db')

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn

def init_db():
    conn = get_conn()
    conn.executescript("""
    -- 윈도우 타이틀 이벤트 로그
    CREATE TABLE IF NOT EXISTS event_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        proc_name TEXT,
        window_title TEXT,
        class_name TEXT,
        status TEXT,
        elapsed_sec REAL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    CREATE INDEX IF NOT EXISTS idx_event_ts ON event_log(timestamp);

    -- 사용량 로그 (C#/PowerBuilder가 기록)
    CREATE TABLE IF NOT EXISTS usage_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        complete_dt TEXT NOT NULL,
        age_group TEXT,
        gender TEXT,
        created_at TEXT DEFAULT (datetime('now','localtime')),
        sent INTEGER DEFAULT 0
    );

    -- 하드웨어 모니터링 최신 상태 (1행)
    CREATE TABLE IF NOT EXISTS hw_status (
        id INTEGER PRIMARY KEY CHECK (id = 1),
        data_json TEXT,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );

    -- heartbeat 전송 실패 캐시
    CREATE TABLE IF NOT EXISTS heartbeat_cache (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data_json TEXT NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        sent INTEGER DEFAULT 0
    );

    -- 서버 전송 이력
    CREATE TABLE IF NOT EXISTS send_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        work_date TEXT NOT NULL,
        status TEXT DEFAULT 'pending',
        response TEXT,
        sent_at DATETIME,
        UNIQUE(work_date)
    );

    -- 세션 로그 (수납 플로우 단위)
    CREATE TABLE IF NOT EXISTS usage_session_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        kiosk_id TEXT NOT NULL,
        work_date TEXT NOT NULL,
        session_id TEXT NOT NULL UNIQUE,
        menu_code TEXT,
        start_dt TEXT,
        end_dt TEXT,
        elapsed_sec REAL,
        result TEXT,
        cancel_step TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        sent INTEGER DEFAULT 0
    );
    CREATE INDEX IF NOT EXISTS idx_session_date ON usage_session_log(work_date);

    -- 세션 내 단계별 로그
    CREATE TABLE IF NOT EXISTS usage_step_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        kiosk_id TEXT NOT NULL,
        session_id TEXT NOT NULL,
        step_order INTEGER,
        step_name TEXT,
        start_dt TEXT,
        end_dt TEXT,
        elapsed_sec REAL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        sent INTEGER DEFAULT 0
    );
    CREATE INDEX IF NOT EXISTS idx_step_session ON usage_step_log(session_id);

    -- A4 프린터 일별 사용량 (오늘사용량 계산용)
    CREATE TABLE IF NOT EXISTS printer_daily (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        work_date TEXT NOT NULL,
        page_count INTEGER DEFAULT 0,
        prev_total INTEGER DEFAULT 0,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(work_date)
    );

    -- 로컬 알람 로그
    CREATE TABLE IF NOT EXISTS alarm_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        alarm_type TEXT NOT NULL,
        severity TEXT DEFAULT 'warning',
        message TEXT,
        detail_json TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        sent INTEGER DEFAULT 0
    );
    """)
    conn.commit()

    # 기존 DB 마이그레이션: sent 컬럼 추가
    for tbl in ('usage_session_log', 'usage_step_log'):
        try:
            conn.execute(f"ALTER TABLE {tbl} ADD COLUMN sent INTEGER DEFAULT 0")
            conn.commit()
        except:
            pass  # 이미 존재하면 무시

    conn.close()
    print(f"[DB] initialized: {DB_PATH}")

# ─── 이벤트 로그 (hook_monitor용) ───
def insert_event(proc_name, window_title, class_name, status, elapsed_sec=None):
    conn = get_conn()
    conn.execute(
        "INSERT INTO event_log (timestamp,proc_name,window_title,class_name,status,elapsed_sec) VALUES (datetime('now','localtime'),?,?,?,?,?)",
        (proc_name, window_title, class_name, status, elapsed_sec))
    conn.commit()
    conn.close()

def get_today_events(limit=50):
    conn = get_conn()
    rows = conn.execute(
        "SELECT * FROM event_log WHERE date(timestamp)=date('now','localtime') ORDER BY id DESC LIMIT ?",
        (limit,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_today_summary():
    conn = get_conn()
    today = time.strftime('%Y-%m-%d')
    total = conn.execute("SELECT count(*) FROM event_log WHERE date(timestamp)=?", (today,)).fetchone()[0]
    starts = conn.execute("SELECT count(*) FROM event_log WHERE date(timestamp)=? AND status='START'", (today,)).fetchone()[0]
    ends = conn.execute("SELECT count(*) FROM event_log WHERE date(timestamp)=? AND status='END'", (today,)).fetchone()[0]
    conn.close()
    return {'date': today, 'total': total, 'starts': starts, 'ends': ends}

# ─── 사용량 로그 (C#/PowerBuilder용) ───
def save_usage(complete_dt, age_group, gender):
    conn = get_conn()
    conn.execute(
        "INSERT INTO usage_log (complete_dt, age_group, gender) VALUES (?,?,?)",
        (complete_dt, age_group, gender))
    conn.commit()
    conn.close()

def get_unsent_usage(limit=100):
    conn = get_conn()
    rows = conn.execute(
        "SELECT id, complete_dt, age_group, gender FROM usage_log WHERE sent=0 ORDER BY id LIMIT ?",
        (limit,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def mark_usage_sent(ids):
    if not ids:
        return
    conn = get_conn()
    placeholders = ','.join(['?'] * len(ids))
    conn.execute(f"UPDATE usage_log SET sent=1 WHERE id IN ({placeholders})", ids)
    conn.commit()
    conn.close()

# ─── 하드웨어 상태 ───
def save_hw_status(data_json):
    conn = get_conn()
    conn.execute(
        "INSERT OR REPLACE INTO hw_status (id, data_json, updated_at) VALUES (1, ?, datetime('now','localtime'))",
        (data_json,))
    conn.commit()
    conn.close()

def get_hw_status():
    conn = get_conn()
    row = conn.execute("SELECT data_json, updated_at FROM hw_status WHERE id=1").fetchone()
    conn.close()
    return dict(row) if row else None

# ─── heartbeat 캐시 ───
def save_heartbeat_cache(data_json):
    conn = get_conn()
    conn.execute("INSERT INTO heartbeat_cache (data_json) VALUES (?)", (data_json,))
    conn.commit()
    conn.close()

def get_unsent_heartbeats(limit=10):
    conn = get_conn()
    rows = conn.execute(
        "SELECT id, data_json FROM heartbeat_cache WHERE sent=0 ORDER BY id LIMIT ?",
        (limit,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def mark_heartbeat_sent(ids):
    if not ids:
        return
    conn = get_conn()
    placeholders = ','.join(['?'] * len(ids))
    conn.execute(f"UPDATE heartbeat_cache SET sent=1 WHERE id IN ({placeholders})", ids)
    conn.commit()
    conn.close()

# ─── 서버 전송 이력 ───
def get_unsent_dates():
    conn = get_conn()
    rows = conn.execute("""
        SELECT DISTINCT date(timestamp) as d FROM event_log
        WHERE date(timestamp) <= date('now','localtime')
        AND date(timestamp) NOT IN (SELECT work_date FROM send_history WHERE status='OK')
        ORDER BY d
    """).fetchall()
    conn.close()
    return [r['d'] for r in rows]

def get_daily_send_data(work_date):
    conn = get_conn()
    logs = conn.execute(
        "SELECT timestamp as log_dt, proc_name, window_title, class_name, status, elapsed_sec FROM event_log WHERE date(timestamp)=? ORDER BY id",
        (work_date,)).fetchall()
    logs = [dict(r) for r in logs]
    starts = sum(1 for l in logs if l['status'] == 'START')
    ends = sum(1 for l in logs if l['status'] == 'END')
    first = logs[0]['log_dt'] if logs else None
    last = logs[-1]['log_dt'] if logs else None
    rate = round(ends / starts * 100, 1) if starts > 0 else 0
    conn.close()
    return {
        'summary': {
            'first_use_time': (first or '')[-8:],
            'last_use_time': (last or '')[-8:],
            'total_entry': starts, 'total_complete': ends,
            'total_cancel': max(0, starts - ends), 'complete_rate': rate
        },
        'logs': logs
    }

def save_send_result(work_date, status, response=''):
    conn = get_conn()
    conn.execute(
        "INSERT OR REPLACE INTO send_history (work_date,status,response,sent_at) VALUES (?,?,?,datetime('now','localtime'))",
        (work_date, status, response))
    conn.commit()
    conn.close()

# ─── 프린터 일별 사용량 ───
def save_printer_daily(work_date, page_count, prev_total):
    conn = get_conn()
    conn.execute(
        "INSERT OR REPLACE INTO printer_daily (work_date, page_count, prev_total) VALUES (?,?,?)",
        (work_date, page_count, prev_total))
    conn.commit()
    conn.close()

def get_printer_daily(work_date):
    conn = get_conn()
    row = conn.execute("SELECT * FROM printer_daily WHERE work_date=?", (work_date,)).fetchone()
    conn.close()
    return dict(row) if row else None

# ─── 세션 / 스텝 로그 ───
def insert_session(kiosk_id, work_date, session_id, menu_code, start_dt,
                   end_dt=None, elapsed_sec=None, result=None, cancel_step=None):
    conn = get_conn()
    conn.execute(
        """INSERT OR REPLACE INTO usage_session_log
           (kiosk_id, work_date, session_id, menu_code, start_dt, end_dt, elapsed_sec, result, cancel_step)
           VALUES (?,?,?,?,?,?,?,?,?)""",
        (kiosk_id, work_date, session_id, menu_code, start_dt,
         end_dt, elapsed_sec, result, cancel_step))
    conn.commit()
    conn.close()

def insert_step(kiosk_id, session_id, step_order, step_name, start_dt,
                end_dt=None, elapsed_sec=None):
    conn = get_conn()
    conn.execute(
        """INSERT INTO usage_step_log
           (kiosk_id, session_id, step_order, step_name, start_dt, end_dt, elapsed_sec)
           VALUES (?,?,?,?,?,?,?)""",
        (kiosk_id, session_id, step_order, step_name, start_dt, end_dt, elapsed_sec))
    conn.commit()
    conn.close()

def update_step_end(session_id, step_name, end_dt, elapsed_sec):
    conn = get_conn()
    conn.execute(
        """UPDATE usage_step_log SET end_dt=?, elapsed_sec=?
           WHERE session_id=? AND step_name=? AND end_dt IS NULL""",
        (end_dt, elapsed_sec, session_id, step_name))
    conn.commit()
    conn.close()

def get_unsent_sessions(limit=50):
    conn = get_conn()
    rows = conn.execute(
        """SELECT * FROM usage_session_log
           WHERE sent=0 AND result IS NOT NULL
           ORDER BY id LIMIT ?""",
        (limit,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_session_steps(session_id):
    conn = get_conn()
    rows = conn.execute(
        """SELECT * FROM usage_step_log
           WHERE session_id=?
           ORDER BY step_order""",
        (session_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def mark_sessions_sent(ids):
    if not ids:
        return
    conn = get_conn()
    placeholders = ','.join(['?'] * len(ids))
    conn.execute(f"UPDATE usage_session_log SET sent=1 WHERE id IN ({placeholders})", ids)
    # 해당 세션의 step도 sent=1로 마킹
    conn.execute(
        f"""UPDATE usage_step_log SET sent=1
            WHERE session_id IN (
                SELECT session_id FROM usage_session_log WHERE id IN ({placeholders})
            )""", ids)
    conn.commit()
    conn.close()

def get_today_sessions(kiosk_id, limit=50):
    conn = get_conn()
    rows = conn.execute(
        """SELECT * FROM usage_session_log
           WHERE kiosk_id=? AND work_date=date('now','localtime')
           ORDER BY id DESC LIMIT ?""",
        (kiosk_id, limit)).fetchall()
    conn.close()
    return [dict(r) for r in rows]

# ─── 알람 로그 ───
def insert_alarm(alarm_type, severity, message, detail_json=None):
    conn = get_conn()
    conn.execute(
        "INSERT INTO alarm_log (alarm_type, severity, message, detail_json) VALUES (?,?,?,?)",
        (alarm_type, severity, message, detail_json))
    conn.commit()
    conn.close()

# ─── 정리 ───
def cleanup_old_data(days=30):
    conn = get_conn()
    conn.execute("DELETE FROM event_log WHERE date(timestamp) < date('now',?)", (f'-{days} days',))
    conn.execute("DELETE FROM heartbeat_cache WHERE sent=1 AND date(created_at) < date('now',?)", (f'-{days} days',))
    conn.execute("DELETE FROM usage_log WHERE sent=1 AND date(created_at) < date('now',?)", (f'-{days} days',))
    conn.execute("DELETE FROM printer_daily WHERE date(work_date) < date('now',?)", (f'-{days} days',))
    conn.execute("DELETE FROM usage_session_log WHERE date(work_date) < date('now',?)", (f'-{days} days',))
    conn.execute("DELETE FROM usage_step_log WHERE date(created_at) < date('now',?)", (f'-{days} days',))
    conn.commit()
    conn.close()
