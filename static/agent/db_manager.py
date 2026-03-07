import sqlite3, os, time, configparser

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'monitor.db')

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_conn()
    conn.executescript("""
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
    CREATE TABLE IF NOT EXISTS send_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        work_date TEXT NOT NULL,
        status TEXT DEFAULT 'pending',
        response TEXT,
        sent_at DATETIME,
        UNIQUE(work_date)
    );
    CREATE INDEX IF NOT EXISTS idx_event_ts ON event_log(timestamp);
    """)
    conn.commit()
    conn.close()

def cleanup_old_data():
    config = configparser.ConfigParser()
    config.read(os.path.join(os.path.dirname(os.path.abspath(__file__)),'config.ini'), encoding='utf-8')
    days = config.getint('MONITOR','retention_days',fallback=30)
    conn = get_conn()
    conn.execute("DELETE FROM event_log WHERE date(timestamp) < date('now',?)", (f'-{days} days',))
    conn.commit()
    conn.close()

def insert_event(proc_name, window_title, class_name, status, elapsed_sec=None):
    conn = get_conn()
    conn.execute("INSERT INTO event_log (timestamp,proc_name,window_title,class_name,status,elapsed_sec) VALUES (datetime('now','localtime'),?,?,?,?,?)",
                 (proc_name, window_title, class_name, status, elapsed_sec))
    conn.commit()
    conn.close()

def get_today_events():
    conn = get_conn()
    rows = conn.execute("SELECT * FROM event_log WHERE date(timestamp)=date('now','localtime') ORDER BY id DESC").fetchall()
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

def get_unsent_dates():
    conn = get_conn()
    rows = conn.execute("""
        SELECT DISTINCT date(timestamp) as d FROM event_log
        WHERE date(timestamp) < date('now','localtime')
        AND date(timestamp) NOT IN (SELECT work_date FROM send_history WHERE status='OK')
        ORDER BY d
    """).fetchall()
    conn.close()
    return [r['d'] for r in rows]

def get_daily_send_data(work_date):
    conn = get_conn()
    logs = conn.execute("SELECT timestamp as log_dt, proc_name, window_title, class_name, status, elapsed_sec FROM event_log WHERE date(timestamp)=? ORDER BY id", (work_date,)).fetchall()
    logs = [dict(r) for r in logs]
    starts = sum(1 for l in logs if l['status']=='START')
    ends = sum(1 for l in logs if l['status']=='END')
    first = logs[0]['log_dt'] if logs else None
    last = logs[-1]['log_dt'] if logs else None
    rate = round(ends/starts*100,1) if starts>0 else 0
    conn.close()
    return {
        'summary': {
            'first_use_time': (first or '')[-8:],
            'last_use_time': (last or '')[-8:],
            'total_entry': starts, 'total_complete': ends,
            'total_cancel': max(0, starts-ends), 'complete_rate': rate
        },
        'logs': logs
    }

def save_send_result(work_date, status, response=''):
    conn = get_conn()
    conn.execute("INSERT OR REPLACE INTO send_history (work_date,status,response,sent_at) VALUES (?,?,?,datetime('now','localtime'))",
                 (work_date, status, response))
    conn.commit()
    conn.close()
