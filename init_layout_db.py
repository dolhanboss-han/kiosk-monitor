import sqlite3

conn = sqlite3.connect('/home/ubuntu/kiosk-monitor/monitor.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS dashboard_layouts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    user_id INTEGER,
    role TEXT,
    layout_json TEXT NOT NULL,
    is_default INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)''')

c.execute('''INSERT OR IGNORE INTO dashboard_layouts 
    (id, name, user_id, role, layout_json, is_default)
    VALUES (1, '기본 레이아웃', 1, 'hq_admin', '[]', 1)''')

conn.commit()
conn.close()
print("=== 레이아웃 테이블 생성 완료 ===")
