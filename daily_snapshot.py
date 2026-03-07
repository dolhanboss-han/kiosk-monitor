#!/usr/bin/env python3
"""매일 자정 실행 - MSSQL에서 당일 사용량을 SQLite에 저장"""
import sys, os
sys.path.insert(0, '/home/ubuntu/kiosk-monitor')
import pyodbc, sqlite3
from datetime import datetime, timedelta

MSSQL = {
    'server': '121.141.174.121,1433',
    'database': 'KIOSK',
    'username': 'nssdb',
    'password': 'nss2109',
    'driver': '{ODBC Driver 18 for SQL Server}',
    'TrustServerCertificate': 'yes'
}

SQLITE_PATH = '/home/ubuntu/kiosk-monitor/monitor.db'

def get_mssql():
    conn_str = f"DRIVER={MSSQL['driver']};SERVER={MSSQL['server']};DATABASE={MSSQL['database']};UID={MSSQL['username']};PWD={MSSQL['password']};TrustServerCertificate={MSSQL['TrustServerCertificate']}"
    return pyodbc.connect(conn_str)

def snapshot(target_date=None):
    if not target_date:
        target_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    
    print(f'[{datetime.now()}] 스냅샷 시작: {target_date}')
    
    mssql = get_mssql()
    cursor = mssql.cursor()
    
    # 키오스크별 사용량
    cursor.execute("""
        SELECT c.HOSP_CD, c.HOSP_NM, c.KIOSK_ID,
            ISNULL(c.COUNT_01,0)+ISNULL(c.COUNT_02,0)+ISNULL(c.COUNT_03,0)+ISNULL(c.COUNT_04,0)+
            ISNULL(c.COUNT_05,0)+ISNULL(c.COUNT_06,0)+ISNULL(c.COUNT_07,0)+ISNULL(c.COUNT_08,0)+
            ISNULL(c.COUNT_09,0)+ISNULL(c.COUNT_10,0)+ISNULL(c.COUNT_11,0)+ISNULL(c.COUNT_12,0)+
            ISNULL(c.COUNT_13,0) AS DAY_TOTAL,
            ISNULL(h.EMR_COMPANY,'')
        FROM KIOSK_HOSP_COUNT c
        LEFT JOIN KIOSK_HOSP_INFO h ON c.HOSP_CD = h.HOSP_CD
        WHERE c.COUNT_DATE = ? AND c.HOSP_CD NOT IN ('MCC','NSS')
    """, target_date)
    rows = cursor.fetchall()
    
    lite = sqlite3.connect(SQLITE_PATH)
    count = 0
    for r in rows:
        try:
            lite.execute("""INSERT OR REPLACE INTO daily_usage_snapshot 
                (snap_date, hosp_cd, hosp_name, kiosk_id, total_count, isv_name)
                VALUES (?,?,?,?,?,?)""",
                (str(target_date), str(r[0]), str(r[1]), str(r[2]), int(r[3] or 0), str(r[4] or '')))
            count += 1
        except Exception as e:
            print(f'  오류: {r[0]}/{r[2]} - {e}')
    
    # 일별 요약
    total_hosp = len(set(r[0] for r in rows))
    active_hosp = len(set(r[0] for r in rows if (r[3] or 0) > 0))
    total_kiosk = len(rows)
    active_kiosk = len([r for r in rows if (r[3] or 0) > 0])
    total_count = sum(r[3] or 0 for r in rows)
    
    lite.execute("""INSERT OR REPLACE INTO daily_summary
        (snap_date, total_hospitals, active_hospitals, total_kiosks, active_kiosks, total_count)
        VALUES (?,?,?,?,?,?)""",
        (str(target_date), int(total_hosp), int(active_hosp), int(total_kiosk), int(active_kiosk), int(total_count)))
    
    lite.commit()
    lite.close()
    mssql.close()
    
    print(f'[{datetime.now()}] 완료: {target_date} - {count}건, 병원 {total_hosp}개, 키오스크 {total_kiosk}대, 총 {total_count}건')

if __name__ == '__main__':
    if len(sys.argv) > 1:
        snapshot(sys.argv[1])
    else:
        snapshot()
