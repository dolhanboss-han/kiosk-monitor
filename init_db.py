import sqlite3

conn = sqlite3.connect('/home/ubuntu/kiosk-monitor/monitor.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    name TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'hosp_user',
    org_type TEXT NOT NULL DEFAULT 'hospital',
    org_code TEXT,
    phone TEXT,
    is_active INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
)''')

c.execute('''CREATE TABLE IF NOT EXISTS login_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    success INTEGER,
    ip_address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)''')

# 기본 관리자 계정 생성
from werkzeug.security import generate_password_hash
admin_pw = generate_password_hash('bseye2026!')

c.execute('''INSERT OR IGNORE INTO users 
    (username, password_hash, name, role, org_type, org_code)
    VALUES (?, ?, ?, ?, ?, ?)''',
    ('admin', admin_pw, '시스템관리자', 'hq_admin', 'hq', 'HQ'))

conn.commit()
conn.close()
print("=== DB 초기화 완료 ===")
print("관리자 계정: admin / bseye2026!")
