from flask import Flask, render_template, jsonify, request, redirect, url_for, session, flash
from flask_socketio import SocketIO
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
import pyodbc
import sqlite3
from datetime import date, datetime
from config import get_connection_string

app = Flask(__name__)
app.config['SECRET_KEY'] = 'bseye-monitor-secret-2026'
socketio = SocketIO(app)

EXCLUDE_ISV = "('MCC','NSS')"
MONITOR_DB = '/home/ubuntu/kiosk-monitor/monitor.db'

def get_db():
    return pyodbc.connect(get_connection_string())



def get_user_filter():
    org_type = session.get('org_type', 'hq')
    org_code = session.get('org_code', '')
    return org_type, org_code

def is_hq():
    return session.get('org_type', 'hq') == 'hq'

def is_isv():
    return session.get('org_type', '') == 'isv'

def is_hospital():
    return session.get('org_type', '') == 'hospital'
def get_monitor_db():
    conn = sqlite3.connect(MONITOR_DB, timeout=10)
    conn.row_factory = sqlite3.Row
    return conn

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if session.get('user_role') != 'hq_admin':
            flash('관리자 권한이 필요합니다.')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated

def get_accessible_hospitals(cursor):
    org_type = session.get('org_type', '')
    org_code = session.get('org_code', '')
    if org_type == 'hq':
        cursor.execute(f"SELECT HOSP_CD, HOSP_NM FROM KIOSK_HOSP_INFO WHERE EMR_COMPANY NOT IN {EXCLUDE_ISV} ORDER BY HOSP_CD")
    elif org_type == 'isv':
        cursor.execute(f"SELECT HOSP_CD, HOSP_NM FROM KIOSK_HOSP_INFO WHERE EMR_COMPANY=? AND EMR_COMPANY NOT IN {EXCLUDE_ISV} ORDER BY HOSP_CD", org_code)
    elif org_type == 'hospital':
        cursor.execute("SELECT HOSP_CD, HOSP_NM FROM KIOSK_HOSP_INFO WHERE HOSP_CD=?", org_code)
    else:
        return []
    return cursor.fetchall()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        conn = get_monitor_db()
        user = conn.execute('SELECT * FROM users WHERE username=? AND is_active=1', (username,)).fetchone()
        success = 0
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['user_name'] = user['name']
            session['user_role'] = user['role']
            session['org_type'] = user['org_type']
            session['org_code'] = user['org_code']
            success = 1
            conn.execute('UPDATE users SET last_login=CURRENT_TIMESTAMP WHERE id=?', (user['id'],))
        conn.execute('INSERT INTO login_log (username, success, ip_address) VALUES (?,?,?)',
                     (username, success, request.headers.get('X-Real-IP', request.remote_addr)))
        conn.commit()
        conn.close()
        if success:
            return redirect(url_for('index'))
        else:
            flash('아이디 또는 비밀번호가 올바르지 않습니다.')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    try:
        conn = get_db()
        cursor = conn.cursor()
        today = date.today().strftime('%Y-%m-%d')
        org_type = session.get('org_type', '')
        org_code = session.get('org_code', '')

        # Tier별 WHERE 조건
        if org_type == 'isv':
            tier_filter = f"AND h.EMR_COMPANY = '{org_code}'"
            tier_filter_c = f"AND h.EMR_COMPANY = '{org_code}'"
        elif org_type == 'hospital':
            tier_filter = f"AND h.HOSP_CD = '{org_code}'"
            tier_filter_c = f"AND c.HOSP_CD = '{org_code}'"
        else:
            tier_filter = ""
            tier_filter_c = ""

        cursor.execute(f"SELECT COUNT(*), SUM(KIOSK_CNT) FROM KIOSK_HOSP_INFO h WHERE h.EMR_COMPANY NOT IN {EXCLUDE_ISV} {tier_filter}")
        summary = cursor.fetchone()

        cursor.execute(f"SELECT COUNT(*) FROM KIOSK_HOSP_INFO h WHERE h.USER_YN='Y' AND h.EMR_COMPANY NOT IN {EXCLUDE_ISV} {tier_filter}")
        active = cursor.fetchone()[0]

        cursor.execute(f"SELECT h.EMR_COMPANY, COUNT(*) as cnt FROM KIOSK_HOSP_INFO h WHERE h.EMR_COMPANY NOT IN {EXCLUDE_ISV} {tier_filter} GROUP BY h.EMR_COMPANY ORDER BY cnt DESC")
        isv_list = cursor.fetchall()

        cursor.execute(f"""
            SELECT COUNT(DISTINCT c.HOSP_CD), COUNT(*),
                   SUM(ISNULL(c.COUNT_01,0)+ISNULL(c.COUNT_02,0)+ISNULL(c.COUNT_03,0)+
                   ISNULL(c.COUNT_04,0)+ISNULL(c.COUNT_05,0)+ISNULL(c.COUNT_06,0)+
                   ISNULL(c.COUNT_07,0)+ISNULL(c.COUNT_08,0)+ISNULL(c.COUNT_09,0)+
                   ISNULL(c.COUNT_10,0)+ISNULL(c.COUNT_11,0)+ISNULL(c.COUNT_12,0)+
                   ISNULL(c.COUNT_13,0)),
                   SUM(ISNULL(c.TAMT,0))
            FROM KIOSK_HOSP_COUNT c
            JOIN KIOSK_HOSP_INFO h ON c.HOSP_CD = h.HOSP_CD
            WHERE c.COUNT_DATE = ? AND h.EMR_COMPANY NOT IN {EXCLUDE_ISV} {tier_filter_c}
        """, today)
        today_summary = cursor.fetchone()

        cursor.execute(f"""
            SELECT h.EMR_COMPANY, COUNT(DISTINCT c.HOSP_CD),
                   SUM(ISNULL(c.COUNT_01,0)+ISNULL(c.COUNT_02,0)+ISNULL(c.COUNT_03,0)+
                   ISNULL(c.COUNT_04,0)+ISNULL(c.COUNT_05,0)+ISNULL(c.COUNT_06,0)+
                   ISNULL(c.COUNT_07,0)+ISNULL(c.COUNT_08,0)+ISNULL(c.COUNT_09,0)+
                   ISNULL(c.COUNT_10,0)+ISNULL(c.COUNT_11,0)+ISNULL(c.COUNT_12,0)+
                   ISNULL(c.COUNT_13,0)),
                   SUM(ISNULL(c.TAMT,0))
            FROM KIOSK_HOSP_COUNT c
            JOIN KIOSK_HOSP_INFO h ON c.HOSP_CD = h.HOSP_CD
            WHERE c.COUNT_DATE = ? AND h.EMR_COMPANY NOT IN {EXCLUDE_ISV} {tier_filter_c}
            GROUP BY h.EMR_COMPANY ORDER BY 3 DESC
        """, today)
        isv_today = cursor.fetchall()

        cursor.execute(f"""
            SELECT TOP 7 c.COUNT_DATE, COUNT(DISTINCT c.HOSP_CD),
                   SUM(ISNULL(c.COUNT_01,0)+ISNULL(c.COUNT_02,0)+ISNULL(c.COUNT_03,0)+
                   ISNULL(c.COUNT_04,0)+ISNULL(c.COUNT_05,0)+ISNULL(c.COUNT_06,0)+
                   ISNULL(c.COUNT_07,0)+ISNULL(c.COUNT_08,0)+ISNULL(c.COUNT_09,0)+
                   ISNULL(c.COUNT_10,0)+ISNULL(c.COUNT_11,0)+ISNULL(c.COUNT_12,0)+
                   ISNULL(c.COUNT_13,0)),
                   SUM(ISNULL(c.TAMT,0))
            FROM KIOSK_HOSP_COUNT c
            JOIN KIOSK_HOSP_INFO h ON c.HOSP_CD = h.HOSP_CD
            WHERE h.EMR_COMPANY NOT IN {EXCLUDE_ISV} {tier_filter_c}
            GROUP BY c.COUNT_DATE ORDER BY c.COUNT_DATE DESC
        """)
        weekly = cursor.fetchall()

        cursor.execute(f"""
            SELECT TOP 10 c.HOSP_NM, c.KIOSK_ID, c.COUNT_DATE,
                   ISNULL(c.COUNT_01,0)+ISNULL(c.COUNT_02,0)+ISNULL(c.COUNT_03,0)+
                   ISNULL(c.COUNT_04,0)+ISNULL(c.COUNT_05,0)+ISNULL(c.COUNT_06,0)+
                   ISNULL(c.COUNT_07,0)+ISNULL(c.COUNT_08,0)+ISNULL(c.COUNT_09,0)+
                   ISNULL(c.COUNT_10,0)+ISNULL(c.COUNT_11,0)+ISNULL(c.COUNT_12,0)+
                   ISNULL(c.COUNT_13,0) as TOTAL_COUNT,
                   ISNULL(c.TAMT,0) as TAMT, c.HOSP_CD
            FROM KIOSK_HOSP_COUNT c
            JOIN KIOSK_HOSP_INFO h ON c.HOSP_CD = h.HOSP_CD
            WHERE h.EMR_COMPANY NOT IN {EXCLUDE_ISV} {tier_filter_c}
            ORDER BY c.COUNT_DATE DESC
        """)
        recent = cursor.fetchall()

        conn.close()

        return render_template('index.html',
            total_hosp=summary[0], total_kiosk=summary[1] or 0, active_hosp=active,
            isv_list=isv_list, today_summary=today_summary, isv_today=isv_today,
            weekly=weekly, recent=recent, today=today
        )
    except Exception as e:
        return f"DB Error: {e}", 500

@app.route('/hospitals')
@login_required
def hospitals():
    try:
        conn = get_db()
        cursor = conn.cursor()
        org_type = session.get('org_type', '')
        org_code = session.get('org_code', '')

        if org_type == 'isv':
            tier_filter = f"AND h.EMR_COMPANY = '{org_code}'"
        elif org_type == 'hospital':
            tier_filter = f"AND h.HOSP_CD = '{org_code}'"
        else:
            tier_filter = ""

        cursor.execute(f"""
            SELECT h.HOSP_CD, h.HOSP_NM, h.EMR_COMPANY, h.KIOSK_CNT,
                   h.USER_YN, h.ADDR1, h.OPEN_DATE, h.CARD_VAN
            FROM KIOSK_HOSP_INFO h
            WHERE h.EMR_COMPANY NOT IN {EXCLUDE_ISV} {tier_filter}
            ORDER BY h.HOSP_CD
        """)
        hospitals = cursor.fetchall()
        conn.close()
        return render_template('hospitals.html', hospitals=hospitals)
    except Exception as e:
        return f"DB Error: {e}", 500

@app.route('/hospital/<hosp_cd>')
@login_required
def hospital_detail(hosp_cd):
    org_type, org_code = get_user_filter()
    if org_type == 'hospital' and org_code != hosp_cd:
        return redirect('/hospitals')
    if org_type == 'isv':
        conn_chk = get_db()
        cur_chk = conn_chk.cursor()
        cur_chk.execute("SELECT EMR_COMPANY FROM KIOSK_HOSP_INFO WHERE HOSP_CD=?", (hosp_cd,))
        row_chk = cur_chk.fetchone()
        conn_chk.close()
        if not row_chk or row_chk[0] != org_code:
            return redirect('/hospitals')
    org_type = session.get('org_type', '')
    org_code = session.get('org_code', '')
    if org_type == 'hospital' and org_code != hosp_cd:
        flash('접근 권한이 없습니다.')
        return redirect(url_for('index'))

    try:
        conn = get_db()
        cursor = conn.cursor()

        if org_type == 'isv':
            cursor.execute("SELECT * FROM KIOSK_HOSP_INFO WHERE HOSP_CD=? AND EMR_COMPANY=?", hosp_cd, org_code)
        else:
            cursor.execute("SELECT * FROM KIOSK_HOSP_INFO WHERE HOSP_CD=?", hosp_cd)

        info = cursor.fetchone()
        if not info:
            flash('병원 정보를 찾을 수 없습니다.')
            return redirect(url_for('hospitals'))

        cols_info = [d[0] for d in cursor.description]

        cursor.execute("""
            SELECT KIOSK_ID, COUNT_DATE,
                   ISNULL(COUNT_01,0)+ISNULL(COUNT_02,0)+ISNULL(COUNT_03,0)+
                   ISNULL(COUNT_04,0)+ISNULL(COUNT_05,0)+ISNULL(COUNT_06,0)+
                   ISNULL(COUNT_07,0)+ISNULL(COUNT_08,0)+ISNULL(COUNT_09,0)+
                   ISNULL(COUNT_10,0)+ISNULL(COUNT_11,0)+ISNULL(COUNT_12,0)+
                   ISNULL(COUNT_13,0) as TOTAL_COUNT,
                   ISNULL(TAMT,0) as TAMT
            FROM KIOSK_HOSP_COUNT WHERE HOSP_CD=?
            ORDER BY COUNT_DATE DESC, KIOSK_ID
        """, hosp_cd)
        counts = cursor.fetchall()

        cursor.execute("""
            SELECT COUNT_DATE,
                   SUM(ISNULL(COUNT_01,0)+ISNULL(COUNT_02,0)+ISNULL(COUNT_03,0)+
                   ISNULL(COUNT_04,0)+ISNULL(COUNT_05,0)+ISNULL(COUNT_06,0)+
                   ISNULL(COUNT_07,0)+ISNULL(COUNT_08,0)+ISNULL(COUNT_09,0)+
                   ISNULL(COUNT_10,0)+ISNULL(COUNT_11,0)+ISNULL(COUNT_12,0)+
                   ISNULL(COUNT_13,0)) as DAILY_TOTAL,
                   SUM(ISNULL(TAMT,0)) as DAILY_AMT
            FROM KIOSK_HOSP_COUNT WHERE HOSP_CD=?
            GROUP BY COUNT_DATE ORDER BY COUNT_DATE DESC
        """, hosp_cd)
        daily = cursor.fetchall()

        conn.close()
        info_dict = dict(zip(cols_info, info)) if info else {}

        return render_template('hospital_detail.html',
            info=info_dict, counts=counts, daily=daily, hosp_cd=hosp_cd
        )
    except Exception as e:
        return f"DB Error: {e}", 500

# ===== 계정 관리 =====
@app.route('/admin/users')
@login_required
@admin_required
def admin_users():
    conn = get_monitor_db()
    users = conn.execute('SELECT * FROM users ORDER BY org_type, username').fetchall()
    conn.close()
    return render_template('admin_users.html', users=users)

@app.route('/admin/user/add', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_user_add():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        name = request.form.get('name', '').strip()
        role = request.form.get('role', '')
        org_type = request.form.get('org_type', '')
        org_code = request.form.get('org_code', '').strip()
        phone = request.form.get('phone', '').strip()

        if not username or not password or not name:
            flash('필수 항목을 모두 입력하세요.')
            return redirect(url_for('admin_user_add'))

        conn = get_monitor_db()
        exists = conn.execute('SELECT id FROM users WHERE username=?', (username,)).fetchone()
        if exists:
            flash('이미 존재하는 아이디입니다.')
            conn.close()
            return redirect(url_for('admin_user_add'))

        conn.execute('''INSERT INTO users (username, password_hash, name, role, org_type, org_code, phone)
                        VALUES (?,?,?,?,?,?,?)''',
                     (username, generate_password_hash(password), name, role, org_type, org_code, phone))
        conn.commit()
        conn.close()
        flash(f'계정 [{username}] 생성 완료')
        return redirect(url_for('admin_users'))

    # ISV 목록 가져오기
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(f"SELECT DISTINCT EMR_COMPANY FROM KIOSK_HOSP_INFO WHERE EMR_COMPANY NOT IN {EXCLUDE_ISV} AND EMR_COMPANY IS NOT NULL ORDER BY EMR_COMPANY")
        isv_list = [r[0] for r in cursor.fetchall()]
        cursor.execute(f"SELECT HOSP_CD, HOSP_NM FROM KIOSK_HOSP_INFO WHERE EMR_COMPANY NOT IN {EXCLUDE_ISV} ORDER BY HOSP_CD")
        hosp_list = cursor.fetchall()
        conn.close()
    except:
        isv_list = []
        hosp_list = []

    return render_template('admin_user_form.html', isv_list=isv_list, hosp_list=hosp_list, user=None)

@app.route('/admin/user/edit/<int:user_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_user_edit(user_id):
    conn = get_monitor_db()

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        role = request.form.get('role', '')
        org_type = request.form.get('org_type', '')
        org_code = request.form.get('org_code', '').strip()
        phone = request.form.get('phone', '').strip()
        is_active = 1 if request.form.get('is_active') else 0
        new_password = request.form.get('password', '').strip()

        if new_password:
            conn.execute('UPDATE users SET name=?, role=?, org_type=?, org_code=?, phone=?, is_active=?, password_hash=? WHERE id=?',
                         (name, role, org_type, org_code, phone, is_active, generate_password_hash(new_password), user_id))
        else:
            conn.execute('UPDATE users SET name=?, role=?, org_type=?, org_code=?, phone=?, is_active=? WHERE id=?',
                         (name, role, org_type, org_code, phone, is_active, user_id))
        conn.commit()
        conn.close()
        flash('계정 수정 완료')
        return redirect(url_for('admin_users'))

    user = conn.execute('SELECT * FROM users WHERE id=?', (user_id,)).fetchone()
    conn.close()

    try:
        mconn = get_db()
        cursor = mconn.cursor()
        cursor.execute(f"SELECT DISTINCT EMR_COMPANY FROM KIOSK_HOSP_INFO WHERE EMR_COMPANY NOT IN {EXCLUDE_ISV} AND EMR_COMPANY IS NOT NULL ORDER BY EMR_COMPANY")
        isv_list = [r[0] for r in cursor.fetchall()]
        cursor.execute(f"SELECT HOSP_CD, HOSP_NM FROM KIOSK_HOSP_INFO WHERE EMR_COMPANY NOT IN {EXCLUDE_ISV} ORDER BY HOSP_CD")
        hosp_list = cursor.fetchall()
        mconn.close()
    except:
        isv_list = []
        hosp_list = []

    return render_template('admin_user_form.html', user=user, isv_list=isv_list, hosp_list=hosp_list)

@app.route('/admin/user/delete/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def admin_user_delete(user_id):
    if user_id == session.get('user_id'):
        flash('자기 자신은 삭제할 수 없습니다.')
        return redirect(url_for('admin_users'))
    conn = get_monitor_db()
    conn.execute('DELETE FROM users WHERE id=?', (user_id,))
    conn.commit()
    conn.close()
    flash('계정 삭제 완료')
    return redirect(url_for('admin_users'))

@app.route('/api/health')
def health():
    return jsonify({'status': 'ok', 'server': 'bseye-monitor', 'version': '0.1.0'})



# ═══════════════════════════════════════════════════

@app.route('/usage')
@login_required
def usage_page():
    return render_template('usage.html')

# 키오스크 사용자 행동 분석 (진입/이탈 추적)
# ═══════════════════════════════════════════════════

@app.route('/api/kiosk-usage/receive', methods=['POST'])
def usage_receive():
    """에이전트에서 일별 사용 데이터 수신"""
    try:
        data = request.get_json()
        kiosk_id = data['kiosk_id']
        hosp_cd = data.get("hosp_cd", "")
        work_date = data['work_date']
        hosp_cd = data.get('hosp_cd', '')
        summary = data.get('summary', {})
        logs = data.get('logs', [])
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        db = get_monitor_db()

        # 중복 체크
        existing = db.execute('SELECT 1 FROM usage_daily_summary WHERE kiosk_id=? AND work_date=?',
                              (kiosk_id, work_date)).fetchone()
        if existing:
            db.close()
            return jsonify({'result': 'DUPLICATE', 'message': 'already received'})

        # 요약 저장
        db.execute("""
            INSERT INTO usage_daily_summary
                (kiosk_id, work_date, hosp_cd, first_use_time, last_use_time,
                 total_entry, total_complete, total_cancel, complete_rate, received_dt)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (kiosk_id, work_date, hosp_cd,
              summary.get('first_use_time', ''),
              summary.get('last_use_time', ''),
              summary.get('total_entry', 0),
              summary.get('total_complete', 0),
              summary.get('total_cancel', 0),
              summary.get('complete_rate', 0),
              now, hosp_cd))

        # 이벤트 로그 저장
        for log in logs:
            db.execute("""
                INSERT INTO usage_event_log
                    (kiosk_id, work_date, hosp_cd, log_dt, proc_name, window_title,
                     class_name, status, elapsed_sec, received_dt)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (kiosk_id, work_date, hosp_cd,
                  log.get('log_dt', ''),
                  log.get('proc_name', ''),
                  log.get('window_title', ''),
                  log.get('class_name', ''),
                  log.get('status', ''),
                  log.get('elapsed_sec'),
                  now, hosp_cd))

        # 키오스크 마스터 업데이트
        db.execute("""
            INSERT OR REPLACE INTO usage_kiosk_master
                (kiosk_id, kiosk_name, location, hosp_cd, last_received_dt)
            VALUES (?, COALESCE((SELECT kiosk_name FROM usage_kiosk_master WHERE kiosk_id=?), ?),
                    COALESCE((SELECT location FROM usage_kiosk_master WHERE kiosk_id=?), ''),
                    ?, ?)
        """, (kiosk_id, kiosk_id, kiosk_id, kiosk_id, hosp_cd, now))

        db.commit()
        db.close()
        return jsonify({'result': 'OK', 'received': len(logs)})

    except Exception as e:
        return jsonify({'result': 'ERROR', 'message': str(e)})


@app.route('/api/kiosk-usage/dashboard')
@login_required
def usage_dashboard_api():
    """사용 현황 대시보드 API"""
    today = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))
    hosp_cd = request.args.get('hosp_cd', 'all')
    # TODO: hosp_admin은 session['org_code']로 자기 병원만
    # TODO: isv_admin은 소속 병원 목록으로 필터
    db = get_monitor_db()

    if hosp_cd and hosp_cd != 'all':
        summary = db.execute("""
            SELECT d.*, k.kiosk_name, k.location, d.hosp_cd
            FROM usage_daily_summary d
            LEFT JOIN usage_kiosk_master k ON d.kiosk_id = k.kiosk_id
            WHERE d.work_date = ? AND d.hosp_cd = ?
            ORDER BY d.kiosk_id
        """, (today, hosp_cd)).fetchall()
    else:
        summary = db.execute("""
            SELECT d.*, k.kiosk_name, k.location, d.hosp_cd
            FROM usage_daily_summary d
            LEFT JOIN usage_kiosk_master k ON d.kiosk_id = k.kiosk_id
            WHERE d.work_date = ?
            ORDER BY d.kiosk_id
        """, (today,)).fetchall()
    summary = [dict(r) for r in summary]

    total_entry = sum(s.get('total_entry', 0) for s in summary)
    total_complete = sum(s.get('total_complete', 0) for s in summary)
    total_cancel = sum(s.get('total_cancel', 0) for s in summary)

    # 전체 통계
    stats = db.execute("""
        SELECT COUNT(DISTINCT kiosk_id) as kiosk_count,
               COUNT(DISTINCT work_date) as day_count,
               SUM(total_entry) as total_entry,
               SUM(total_complete) as total_complete,
               SUM(total_cancel) as total_cancel
        FROM usage_daily_summary
    """).fetchone()
    stats = dict(stats) if stats else {}

    # 병원별 순위 (1단계 전체 뷰용)
    hospital_ranking = []
    if not hosp_cd or hosp_cd == 'all':
        ranking_rows = db.execute("""
            SELECT d.hosp_cd,
                   COUNT(DISTINCT d.kiosk_id) as kiosk_count,
                   SUM(d.total_entry) as total_entry,
                   SUM(d.total_complete) as total_complete,
                   SUM(d.total_cancel) as total_cancel
            FROM usage_daily_summary d
            WHERE d.work_date = ? AND d.hosp_cd IS NOT NULL AND d.hosp_cd != ''
            GROUP BY d.hosp_cd
            ORDER BY total_entry DESC
        """, (today,)).fetchall()
        hospital_ranking = [dict(r) for r in ranking_rows]
        for h in hospital_ranking:
            e = h.get('total_entry', 0) or 0
            c = h.get('total_complete', 0) or 0
            h['complete_rate'] = round(c / e * 100, 1) if e > 0 else 0

    db.close()
    return jsonify({
        'today': today,
        'active_kiosks': len(summary),
        'total_entry': total_entry,
        'total_complete': total_complete,
        'total_cancel': total_cancel,
        'complete_rate': round(total_complete / total_entry * 100, 1) if total_entry > 0 else 0,
        'summary': summary,
        'all_stats': stats,
        'hospital_ranking': hospital_ranking
    })


@app.route('/api/kiosk-usage/daily')
@login_required
def usage_daily_api():
    """일별 현황 API"""
    start_date = request.args.get('start_date', datetime.now().strftime('%Y-%m-%d'))
    end_date = request.args.get('end_date', start_date)
    kiosk_id = request.args.get('kiosk_id', 'all')
    hosp_cd = request.args.get('hosp_cd', 'all')
    db = get_monitor_db()

    where = 'WHERE work_date >= ? AND work_date <= ?'
    params = [start_date, end_date]

    if kiosk_id and kiosk_id != 'all':
        where += ' AND kiosk_id = ?'
        params.append(kiosk_id)
    if hosp_cd and hosp_cd != 'all':
        where += ' AND hosp_cd = ?'
        params.append(hosp_cd)

    rows = db.execute(f"""
        SELECT * FROM usage_daily_summary
        {where}
        ORDER BY work_date DESC, kiosk_id
    """, params).fetchall()

    db.close()
    return jsonify({'data': [dict(r) for r in rows], 'count': len(rows)})


@app.route('/api/kiosk-usage/detail')
@login_required
def usage_detail_api():
    """상세 이벤트 로그 API"""
    kiosk_id = request.args.get('kiosk_id', '')
    work_date = request.args.get('work_date', datetime.now().strftime('%Y-%m-%d'))
    db = get_monitor_db()

    rows = db.execute("""
        SELECT * FROM usage_event_log
        WHERE kiosk_id = ? AND work_date = ?
        ORDER BY log_dt
    """, (kiosk_id, work_date)).fetchall()
    logs = [dict(r) for r in rows]

    for log in logs:
        if log.get('elapsed_sec') and log['elapsed_sec'] > 0:
            m = log['elapsed_sec'] // 60
            s = log['elapsed_sec'] % 60
            log['elapsed_str'] = f'{m}m {s}s'
        else:
            log['elapsed_str'] = '-'

    db.close()
    return jsonify({'logs': logs, 'count': len(logs)})




@app.route('/api/kiosk-usage/funnel')
@login_required
def usage_funnel_api():
    """메뉴별 퍼널 분석 API"""
    work_date = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))
    kiosk_id = request.args.get('kiosk_id', '')
    hosp_cd = request.args.get('hosp_cd', '')
    db = get_monitor_db()

    where = 'WHERE work_date = ?'
    params = [work_date]

    if kiosk_id and kiosk_id != 'all':
        where += ' AND kiosk_id = ?'
        params.append(kiosk_id)
    if hosp_cd and hosp_cd != 'all' and hosp_cd:
        where += ' AND hosp_cd = ?'
        params.append(hosp_cd)

    rows = db.execute(f"""
        SELECT window_title, status, elapsed_sec, log_dt
        FROM usage_event_log
        {where}
        ORDER BY log_dt
    """, params).fetchall()

    logs = [dict(r) for r in rows]
    db.close()

    # 메뉴별 세션 파싱
    menus = {}
    sessions = []
    cur_session = None

    for log in logs:
        title = log.get('window_title', '') or ''
        status = log.get('status', '')
        elapsed = log.get('elapsed_sec') or 0

        if '_' in title:
            parts = title.split('_', 1)
            menu = parts[0]
            step = parts[1] if len(parts) > 1 else ''
        else:
            menu = title
            step = ''

        if status == 'START' and (cur_session is None or cur_session['menu'] != menu or step in ('메인', '')):
            if cur_session:
                last_step = cur_session['steps'][-1] if cur_session['steps'] else ''
                cur_session['completed'] = '완료' in last_step
                sessions.append(cur_session)
            cur_session = {'menu': menu, 'steps': [step], 'times': {step: 0}, 'total_sec': 0}
        elif cur_session:
            if step and step not in cur_session['steps']:
                cur_session['steps'].append(step)
            if status == 'END' and elapsed:
                cur_session['times'][step] = cur_session['times'].get(step, 0) + elapsed
                cur_session['total_sec'] += elapsed

    if cur_session:
        last_step = cur_session['steps'][-1] if cur_session['steps'] else ''
        cur_session['completed'] = '완료' in last_step
        sessions.append(cur_session)

    # 메뉴별 집계
    for s in sessions:
        menu = s['menu']
        if menu not in menus:
            menus[menu] = {'menu': menu, 'total': 0, 'completed': 0, 'cancelled': 0,
                           'steps': {}, 'step_order': [], 'step_times': {}, 'cancel_at': {}}
        m = menus[menu]
        m['total'] += 1
        if s['completed']:
            m['completed'] += 1
        else:
            m['cancelled'] += 1
            if s['steps']:
                last = s['steps'][-1]
                m['cancel_at'][last] = m['cancel_at'].get(last, 0) + 1

        for i, step in enumerate(s['steps']):
            if step not in m['steps']:
                m['steps'][step] = 0
            m['steps'][step] += 1
            if step not in m['step_order']:
                m['step_order'].append(step)
            if step not in m['step_times']:
                m['step_times'][step] = []
            if step in s['times']:
                m['step_times'][step].append(s['times'][step])

    # 결과 정리
    result = []
    for menu, m in menus.items():
        funnel = []
        for step in m['step_order']:
            count = m['steps'].get(step, 0)
            times = m['step_times'].get(step, [])
            avg_time = round(sum(times) / len(times), 1) if times else 0
            cancel = m['cancel_at'].get(step, 0)
            funnel.append({
                'step': step,
                'count': count,
                'pct': round(count / m['total'] * 100, 1) if m['total'] > 0 else 0,
                'avg_sec': avg_time,
                'cancel_count': cancel
            })
        result.append({
            'menu': menu,
            'total': m['total'],
            'completed': m['completed'],
            'cancelled': m['cancelled'],
            'rate': round(m['completed'] / m['total'] * 100, 1) if m['total'] > 0 else 0,
            'funnel': funnel
        })

    result.sort(key=lambda x: x['total'], reverse=True)
    return jsonify({'menus': result, 'date': work_date})

@app.route('/api/kiosk-usage/kiosks')
@login_required
def usage_kiosk_list_api():
    """등록된 키오스크 목록"""
    hosp_cd = request.args.get('hosp_cd', 'all')
    db = get_monitor_db()

    if hosp_cd and hosp_cd != 'all':
        rows = db.execute('SELECT * FROM usage_kiosk_master WHERE hosp_cd = ? ORDER BY kiosk_id', (hosp_cd,)).fetchall()
    else:
        rows = db.execute('SELECT * FROM usage_kiosk_master ORDER BY kiosk_id').fetchall()

    db.close()
    return jsonify({'kiosks': [dict(r) for r in rows]})

@app.route('/api/kiosk-usage/hospitals')
@login_required
def usage_hospital_list_api():
    """행동분석용 병원 목록 API"""
    db = get_monitor_db()
    rows = db.execute("""
        SELECT DISTINCT hosp_cd FROM usage_kiosk_master
        WHERE hosp_cd IS NOT NULL AND hosp_cd != ''
        ORDER BY hosp_cd
    """).fetchall()
    db.close()

    hospitals = [{'hosp_cd': r[0], 'hosp_nm': r[0]} for r in rows]

    # MSSQL에서 병원명 매핑 시도
    try:
        conn = get_db()
        cursor = conn.cursor()
        codes = [h['hosp_cd'] for h in hospitals]
        if codes:
            placeholders = ','.join(['?' for _ in codes])
            cursor.execute(f"SELECT HOSP_CD, HOSP_NM FROM KIOSK_HOSP_INFO WHERE HOSP_CD IN ({placeholders})", codes)
            name_map = {str(row[0]): str(row[1]) for row in cursor.fetchall()}
            for h in hospitals:
                if h['hosp_cd'] in name_map:
                    h['hosp_nm'] = name_map[h['hosp_cd']]
        conn.close()
    except:
        pass

    return jsonify({'hospitals': hospitals})



# ============================================================
# 통합 검증 페이지 & API
# ============================================================
@app.route('/usage-verify')
@login_required
def usage_verify():
    return render_template('usage_verify.html')

@app.route('/api/verify/devices')
@login_required
def verify_devices():
    conn = get_monitor_db()
    rows = conn.execute("""
        SELECT hosp_cd, kiosk_id, status, cpu_usage, memory_usage, disk_usage,
               printer_a4, printer_thermal, card_reader, barcode_reader,
               network_speed, emr_connection, agent_version, last_heartbeat
        FROM kiosk_status ORDER BY hosp_cd, kiosk_id
    """).fetchall()
    conn.close()
    return jsonify(devices=[dict(r) for r in rows])

@app.route('/api/verify/alarms')
@login_required
def verify_alarms():
    conn = get_monitor_db()
    rows = conn.execute("""
        SELECT hosp_cd, kiosk_id, alarm_type, severity, title, message, status, created_at
        FROM alarms ORDER BY created_at DESC LIMIT 20
    """).fetchall()
    conn.close()
    return jsonify(alarms=[dict(r) for r in rows])

@app.route('/api/verify/send-status')
@login_required
def verify_send_status():
    conn = get_monitor_db()
    rows = conn.execute("SELECT * FROM usage_kiosk_master").fetchall()
    conn.close()
    from datetime import datetime
    result = []
    for r in rows:
        d = dict(r)
        try:
            last = datetime.strptime(d['last_received_dt'], '%Y-%m-%d %H:%M:%S')
            d['hours_ago'] = round((datetime.now() - last).total_seconds() / 3600, 1)
        except:
            d['hours_ago'] = 9999
        result.append(d)
    return jsonify(kiosks=result)



# ============================================================
# 키오스크 설치 체크리스트 API
# ============================================================
SETUP_CHECKLIST_TEMPLATE = [
    (1, 'basic', '병원코드 입력', 'manual'),
    (1, 'basic', '병원명 입력', 'manual'),
    (1, 'basic', '키오스크ID 설정', 'manual'),
    (1, 'basic', '설치위치 입력', 'manual'),
    (1, 'basic', '설치자명 입력', 'manual'),
    (2, 'pc', 'CPU 상태', 'auto'),
    (2, 'pc', '메모리 상태', 'auto'),
    (2, 'pc', '디스크 상태', 'auto'),
    (2, 'pc', 'OS 버전', 'auto'),
    (2, 'device', '모니터 출력', 'manual'),
    (2, 'device', '바코드리더기', 'manual'),
    (2, 'device', '영수증프린터', 'manual'),
    (2, 'device', 'A4프린터', 'manual'),
    (2, 'device', 'A4프린터 토너', 'manual'),
    (2, 'device', 'A4프린터 용지', 'manual'),
    (2, 'device', '카드리더기', 'manual'),
    (2, 'device', '스마트플러그', 'manual'),
    (3, 'network', '서버 통신 확인', 'auto'),
    (3, 'network', '등록 요청 전송', 'auto'),
    (3, 'network', '서버 응답 확인', 'auto'),
    (4, 'data', '샘플 이벤트 전송', 'auto'),
    (4, 'data', '서버 수신 확인', 'auto'),
    (4, 'data', '데이터 정합성', 'auto'),
    (5, 'program', '대상 프로세스 감지', 'auto'),
    (5, 'program', '메뉴 진입 감지', 'manual'),
    (5, 'program', '메뉴 완료 감지', 'manual'),
    (5, 'program', '메뉴 이탈 감지', 'manual'),
]

@app.route('/setup-monitor')
@login_required
def setup_monitor():
    return render_template('setup_monitor.html')

@app.route('/api/setup/start', methods=['POST'])
def api_setup_start():
    data = request.get_json() or {}
    kiosk_id = data.get('kiosk_id','').strip()
    if not kiosk_id:
        return jsonify(result='ERROR', message='kiosk_id required')
    conn = get_monitor_db()
    cur = conn.execute(
        "INSERT INTO setup_session (kiosk_id, hosp_cd, hosp_name, location, installer) VALUES (?,?,?,?,?)",
        (kiosk_id, data.get('hosp_cd',''), data.get('hosp_name',''), data.get('location',''), data.get('installer',''))
    )
    sid = cur.lastrowid
    for step, cat, item, ctype in SETUP_CHECKLIST_TEMPLATE:
        conn.execute(
            "INSERT INTO setup_checklist (session_id, step, category, item, check_type, status) VALUES (?,?,?,?,?,?)",
            (sid, step, cat, item, ctype, 'pending')
        )
    conn.commit()
    conn.close()
    return jsonify(result='OK', session_id=sid)

@app.route('/api/setup/update', methods=['POST'])
def api_setup_update():
    data = request.get_json() or {}
    sid = data.get('session_id')
    item = data.get('item','')
    status = data.get('status','ok')
    value = data.get('value','')
    if not sid or not item:
        return jsonify(result='ERROR', message='session_id and item required')
    conn = get_monitor_db()
    conn.execute(
        "UPDATE setup_checklist SET status=?, value=?, checked_at=CURRENT_TIMESTAMP WHERE session_id=? AND item=?",
        (status, value, sid, item)
    )
    conn.commit()
    # 전체 완료 체크
    pending = conn.execute("SELECT count(*) FROM setup_checklist WHERE session_id=? AND status='pending'", (sid,)).fetchone()[0]
    if pending == 0:
        conn.execute("UPDATE setup_session SET status='completed', completed_at=CURRENT_TIMESTAMP WHERE id=?", (sid,))
        conn.commit()
    conn.close()
    return jsonify(result='OK', remaining=pending)

@app.route('/api/setup/update-info', methods=['POST'])
def api_setup_update_info():
    data = request.get_json() or {}
    sid = data.get('session_id')
    if not sid:
        return jsonify(result='ERROR')
    conn = get_monitor_db()
    conn.execute(
        "UPDATE setup_session SET hosp_cd=?, hosp_name=?, location=?, installer=? WHERE id=?",
        (data.get('hosp_cd',''), data.get('hosp_name',''), data.get('location',''), data.get('installer',''), sid)
    )
    conn.commit()
    conn.close()
    return jsonify(result='OK')

@app.route('/api/setup/status')
def api_setup_status():
    sid = request.args.get('session_id')
    conn = get_monitor_db()
    if sid:
        sess = conn.execute("SELECT * FROM setup_session WHERE id=?", (sid,)).fetchone()
        checks = conn.execute("SELECT * FROM setup_checklist WHERE session_id=? ORDER BY step, id", (sid,)).fetchall()
        conn.close()
        if not sess:
            return jsonify(result='ERROR', message='not found')
        return jsonify(session=dict(sess), checks=[dict(c) for c in checks])
    else:
        sessions = conn.execute("SELECT * FROM setup_session ORDER BY started_at DESC LIMIT 20").fetchall()
        result = []
        for s in sessions:
            total = conn.execute("SELECT count(*) FROM setup_checklist WHERE session_id=?", (s['id'],)).fetchone()[0]
            done = conn.execute("SELECT count(*) FROM setup_checklist WHERE session_id=? AND status!='pending'", (s['id'],)).fetchone()[0]
            d = dict(s)
            d['total'] = total
            d['done'] = done
            d['progress'] = round(done/total*100) if total>0 else 0
            result.append(d)
        conn.close()
        return jsonify(sessions=result)

@app.route('/api/setup/sessions')
@login_required
def api_setup_sessions():
    conn = get_monitor_db()
    sessions = conn.execute("SELECT * FROM setup_session ORDER BY started_at DESC").fetchall()
    result = []
    for s in sessions:
        total = conn.execute("SELECT count(*) FROM setup_checklist WHERE session_id=?", (s['id'],)).fetchone()[0]
        done = conn.execute("SELECT count(*) FROM setup_checklist WHERE session_id=? AND status!='pending'", (s['id'],)).fetchone()[0]
        d = dict(s)
        d['total'] = total
        d['done'] = done
        d['progress'] = round(done/total*100) if total>0 else 0
        result.append(d)
    conn.close()
    return jsonify(sessions=result)



@app.route('/api/setup/check')
@login_required
def api_setup_check():
    """에이전트에 점검 명령을 전달하는 프록시 (추후 에이전트 직접 연결 시 사용)"""
    kiosk_id = request.args.get('kiosk_id','')
    category = request.args.get('category','all')
    conn = get_monitor_db()
    # 현재는 kiosk_status 테이블에서 데이터 조회
    dev = conn.execute("SELECT * FROM kiosk_status WHERE kiosk_id=? ORDER BY id DESC LIMIT 1", (kiosk_id,)).fetchone()
    conn.close()
    results = []
    if category in ('pc','all'):
        if dev:
            cpu = dev['cpu_usage'] or 0
            results.append({'item':'CPU','status':'ok' if cpu<80 else 'warn' if cpu<95 else 'error','value':f'{cpu}%',
                           'detail':{'usage_pct':cpu,'threshold':'<80% 정상, 80-95% 주의, >95% 오류'}})
            mem = dev['memory_usage'] or 0
            results.append({'item':'메모리','status':'ok' if mem<80 else 'warn' if mem<95 else 'error','value':f'{mem}%',
                           'detail':{'usage_pct':mem,'threshold':'<80% 정상, 80-95% 주의, >95% 오류'}})
            disk = dev['disk_usage'] or 0
            results.append({'item':'디스크','status':'ok' if disk<85 else 'warn' if disk<95 else 'error','value':f'{disk}%' if disk else '미수집',
                           'detail':{'usage_pct':disk,'threshold':'<85% 정상, 85-95% 주의, >95% 오류'}})
        else:
            results.append({'item':'PC','status':'warn','value':'에이전트 데이터 없음','detail':{'note':'에이전트를 실행하세요'}})
    if category in ('printer','all'):
        if dev:
            pa = dev['printer_a4'] or 'unknown'
            results.append({'item':'A4프린터','status':'ok' if pa=='ok' else 'error' if pa=='error' else 'warn','value':pa,'detail':{}})
            pt = dev['printer_thermal'] or 'unknown'
            results.append({'item':'영수증프린터','status':'ok' if pt=='ok' else 'error' if pt=='error' else 'warn','value':pt,'detail':{}})
        else:
            results.append({'item':'프린터','status':'warn','value':'에이전트 데이터 없음','detail':{}})
    if category in ('usb','all'):
        if dev:
            br = dev['barcode_reader'] or 'unknown'
            results.append({'item':'바코드리더기','status':'ok' if br=='ok' else 'error' if br=='error' else 'warn','value':br,'detail':{}})
            cr = dev['card_reader'] or 'unknown'
            results.append({'item':'카드리더기','status':'ok' if cr=='ok' else 'error' if cr=='error' else 'warn','value':cr,'detail':{}})
        else:
            results.append({'item':'USB장치','status':'warn','value':'에이전트 데이터 없음','detail':{}})
    if category in ('network','all'):
        if dev:
            ns = dev['network_speed'] or 0
            results.append({'item':'네트워크','status':'ok' if ns>10 else 'warn' if ns>2 else 'error','value':f'{ns}Mbps' if ns else '미수집',
                           'detail':{'threshold':'>10Mbps 정상, 2-10Mbps 주의, <2Mbps 오류'}})
            emr = dev['emr_connection'] or 'unknown'
            results.append({'item':'EMR연결','status':'ok' if emr=='ok' else 'error' if emr=='error' else 'warn','value':emr,'detail':{}})
        else:
            results.append({'item':'네트워크','status':'warn','value':'에이전트 데이터 없음','detail':{}})
    if category in ('server','all'):
        conn2 = get_monitor_db()
        master = conn2.execute("SELECT * FROM usage_kiosk_master WHERE kiosk_id=?", (kiosk_id,)).fetchone()
        conn2.close()
        if master:
            results.append({'item':'서버전송','status':'ok','value':f'마지막 수신: {master["last_received_dt"]}','detail':{}})
        else:
            results.append({'item':'서버전송','status':'warn','value':'수신 이력 없음','detail':{'note':'에이전트에서 데이터를 전송하세요'}})
    if category in ('process','all'):
        results.append({'item':'프로세스감지','status':'warn','value':'에이전트에서 직접 확인','detail':{'note':'키오스크 PC의 localhost:8080에서 확인'}})
    if category in ('monitor','all'):
        conn3 = get_monitor_db()
        today_str = date.today().isoformat()
        cnt = conn3.execute("SELECT count(*) FROM usage_event_log WHERE kiosk_id=? AND work_date=?", (kiosk_id, today_str)).fetchone()[0]
        conn3.close()
        results.append({'item':'오늘수집','status':'ok' if cnt>0 else 'warn','value':f'{cnt}건','detail':{'date':today_str}})
    return jsonify(results=results)



@app.route('/api/setup/install-bat', methods=['POST'])
def api_setup_install_bat():
    """기본정보를 받아 install.bat를 동적 생성하여 다운로드"""
    data = request.get_json() or {}
    hosp_cd = data.get('hosp_cd','')
    hosp_name = data.get('hosp_name','')
    kiosk_id = data.get('kiosk_id','')
    location = data.get('location','')
    installer = data.get('installer','')
    target_process = data.get('target_process','hospital_kiosk_app.exe')
    server_url = data.get('server_url','https://monitor.blueswell.co.kr/api/kiosk-usage/receive')

    config_ini = f"""[MONITOR]
web_port = 8080
refresh_interval = 5
retention_days = 30
target_process = {target_process}
exclude_process =
exclude_title =

[SERVER]
server_url = {server_url}
kiosk_id = {kiosk_id}
kiosk_name = {hosp_name}_{kiosk_id}
location = {location}
hosp_cd = {hosp_cd}
hosp_name = {hosp_name}
installer = {installer}
send_time = 08:00
retry_interval = 300"""

    bat_content = f"""@echo off
chcp 65001 >nul
echo ============================================
echo   BSEYE Kiosk Agent Installer
echo   {hosp_name} / {kiosk_id}
echo ============================================
echo.

echo [1/5] 폴더 생성...
if not exist "C:\\bseye-agent" mkdir "C:\\bseye-agent"
cd /d "C:\\bseye-agent"
echo     OK

echo [2/5] 에이전트 다운로드...
powershell -Command "Invoke-WebRequest -Uri 'https://monitor.blueswell.co.kr/static/agent/bseye-agent.zip' -OutFile 'agent.zip'"
if errorlevel 1 (
    echo     실패! 인터넷 연결을 확인하세요
    pause
    exit /b 1
)
echo     OK

echo [3/5] 압축 해제...
powershell -Command "Expand-Archive -Path 'agent.zip' -DestinationPath '.' -Force"
if exist "bseye-agent" (
    powershell -Command "Copy-Item 'bseye-agent\*' '.' -Recurse -Force"
    powershell -Command "Remove-Item 'bseye-agent' -Recurse -Force -ErrorAction SilentlyContinue"
)
del agent.zip 2>nul
echo     OK

echo [4/5] config.ini 생성...
(
echo {config_ini.replace(chr(10), chr(10) + 'echo ')}
) > config.ini.tmp
powershell -Command "$c = @'
{config_ini}
'@; $c | Out-File -FilePath 'config.ini' -Encoding utf8NoBOM"
del config.ini.tmp 2>nul
echo     OK

echo [5/5] 필수 패키지 설치...
pip install psutil requests uvicorn fastapi -q 2>nul
if errorlevel 1 (
    python -m pip install psutil requests uvicorn fastapi -q 2>nul
)
echo     OK

echo.
echo ============================================
echo   설치 완료!
echo   에이전트를 시작합니다...
echo ============================================
echo.

start "BSEYE Agent" python main.py

echo 에이전트가 백그라운드에서 실행 중입니다.
echo 브라우저에서 http://localhost:8080 으로 확인하세요.
echo.
echo 이 창은 닫아도 됩니다.
pause
"""

    from flask import Response
    return Response(
        bat_content,
        mimetype='application/x-bat',
        headers={'Content-Disposition': f'attachment; filename=bseye-install-{kiosk_id}.bat'}
    )

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)

@app.route('/isv/<isv_name>')
@login_required
def isv_detail(isv_name):
    org_type = session.get('org_type', '')
    org_code = session.get('org_code', '')
    if org_type == 'isv' and org_code != isv_name:
        flash('접근 권한이 없습니다.')
        return redirect(url_for('index'))
    if org_type == 'hospital':
        flash('접근 권한이 없습니다.')
        return redirect(url_for('index'))

    try:
        conn = get_db()
        cursor = conn.cursor()
        today = date.today().strftime('%Y-%m-%d')

        cursor.execute("SELECT COUNT(*), SUM(KIOSK_CNT) FROM KIOSK_HOSP_INFO WHERE EMR_COMPANY=?", isv_name)
        summary = cursor.fetchone()

        cursor.execute("SELECT COUNT(*) FROM KIOSK_HOSP_INFO WHERE EMR_COMPANY=? AND USER_YN='Y'", isv_name)
        active = cursor.fetchone()[0]

        cursor.execute("""
            SELECT HOSP_CD, HOSP_NM, KIOSK_CNT, USER_YN, ADDR1, OPEN_DATE
            FROM KIOSK_HOSP_INFO WHERE EMR_COMPANY=? ORDER BY HOSP_CD
        """, isv_name)
        hosp_list = cursor.fetchall()

        cursor.execute("""
            SELECT COUNT(DISTINCT c.HOSP_CD), COUNT(*),
                   SUM(ISNULL(c.COUNT_01,0)+ISNULL(c.COUNT_02,0)+ISNULL(c.COUNT_03,0)+
                   ISNULL(c.COUNT_04,0)+ISNULL(c.COUNT_05,0)+ISNULL(c.COUNT_06,0)+
                   ISNULL(c.COUNT_07,0)+ISNULL(c.COUNT_08,0)+ISNULL(c.COUNT_09,0)+
                   ISNULL(c.COUNT_10,0)+ISNULL(c.COUNT_11,0)+ISNULL(c.COUNT_12,0)+
                   ISNULL(c.COUNT_13,0))
            FROM KIOSK_HOSP_COUNT c
            JOIN KIOSK_HOSP_INFO h ON c.HOSP_CD = h.HOSP_CD
            WHERE h.EMR_COMPANY=? AND c.COUNT_DATE=?
        """, isv_name, today)
        today_stat = cursor.fetchone()

        cursor.execute("""
            SELECT TOP 14 c.COUNT_DATE, COUNT(DISTINCT c.HOSP_CD),
                   SUM(ISNULL(c.COUNT_01,0)+ISNULL(c.COUNT_02,0)+ISNULL(c.COUNT_03,0)+
                   ISNULL(c.COUNT_04,0)+ISNULL(c.COUNT_05,0)+ISNULL(c.COUNT_06,0)+
                   ISNULL(c.COUNT_07,0)+ISNULL(c.COUNT_08,0)+ISNULL(c.COUNT_09,0)+
                   ISNULL(c.COUNT_10,0)+ISNULL(c.COUNT_11,0)+ISNULL(c.COUNT_12,0)+
                   ISNULL(c.COUNT_13,0))
            FROM KIOSK_HOSP_COUNT c
            JOIN KIOSK_HOSP_INFO h ON c.HOSP_CD = h.HOSP_CD
            WHERE h.EMR_COMPANY=?
            GROUP BY c.COUNT_DATE ORDER BY c.COUNT_DATE DESC
        """, isv_name)
        daily = cursor.fetchall()

        conn.close()

        return render_template('isv_detail.html',
            isv_name=isv_name, total_hosp=summary[0], total_kiosk=summary[1] or 0,
            active=active, hosp_list=hosp_list, today_stat=today_stat,
            daily=daily, today=today
        )
    except Exception as e:
        return f"DB Error: {e}", 500

@app.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        current = request.form.get('current_password', '')
        new_pw = request.form.get('new_password', '')
        confirm = request.form.get('confirm_password', '')

        if not current or not new_pw:
            flash('모든 항목을 입력하세요.')
            return redirect(url_for('change_password'))

        if new_pw != confirm:
            flash('새 비밀번호가 일치하지 않습니다.')
            return redirect(url_for('change_password'))

        if len(new_pw) < 6:
            flash('비밀번호는 6자 이상이어야 합니다.')
            return redirect(url_for('change_password'))

        conn = get_monitor_db()
        user = conn.execute('SELECT * FROM users WHERE id=?', (session['user_id'],)).fetchone()

        if not check_password_hash(user['password_hash'], current):
            flash('현재 비밀번호가 올바르지 않습니다.')
            conn.close()
            return redirect(url_for('change_password'))

        conn.execute('UPDATE users SET password_hash=? WHERE id=?',
                     (generate_password_hash(new_pw), session['user_id']))
        conn.commit()
        conn.close()
        flash('비밀번호가 변경되었습니다.')
        return redirect(url_for('index'))

    return render_template('change_password.html')

@app.route('/admin/login-log')
@login_required
@admin_required
def admin_login_log():
    conn = get_monitor_db()
    logs = conn.execute('SELECT * FROM login_log ORDER BY created_at DESC LIMIT 100').fetchall()
    conn.close()
    return render_template('admin_login_log.html', logs=logs)

@app.route('/editor')
@login_required
def editor():
    return render_template('editor.html')

import json

@app.route('/api/layout', methods=['GET'])
@login_required
def get_layout():
    db = get_monitor_db()
    row = db.execute('SELECT layout_json FROM dashboard_layouts WHERE is_default=1').fetchone()
    db.close()
    return jsonify({'layout': json.loads(row[0]) if row else []})

@app.route('/api/layout', methods=['POST'])
@login_required
def save_layout():
    data = request.get_json()
    layout = json.dumps(data.get('layout', []))
    db = get_monitor_db()
    db.execute('UPDATE dashboard_layouts SET layout_json=?, updated_at=CURRENT_TIMESTAMP WHERE is_default=1',
               (layout,))
    db.commit()
    db.close()
    return jsonify({'status': 'saved'})



@app.route('/api/kiosk-monitor')
@login_required
def api_kiosk_monitor():
    """병원별 키오스크 통합 모니터링 API"""
    import json as _json
    db = get_monitor_db()
    rows = db.execute("""SELECT hosp_cd, kiosk_id, status, cpu_usage, memory_usage, disk_usage,
        printer_a4, printer_thermal, card_reader, barcode_reader,
        network_speed, emr_connection, network_printers, agent_version, last_heartbeat
        FROM kiosk_status ORDER BY hosp_cd, kiosk_id""").fetchall()
    
    hospitals = {}
    for r in rows:
        hc = r[0]
        np = {}
        try:
            if r[12]: np = _json.loads(r[12])
        except: pass
        
        kiosk = {
            'kiosk_id': r[1], 'status': r[2],
            'pc': {'cpu': r[3] or 0, 'memory': r[4] or 0, 'disk': r[5] or 0},
            'printer_a4': r[6] or 'unknown',
            'printer_thermal': r[7] or 'unknown',
            'card_reader': r[8] or 'unknown',
            'barcode_reader': r[9] or 'unknown',
            'network_speed': r[10] or 0,
            'emr_connection': r[11] or 'unknown',
            'network_printers': np,
            'agent_version': r[13] or '',
            'last_heartbeat': r[14] or ''
        }
        
        # SNMP 프린터 상세 추출
        for pname, pinfo in np.items():
            if 'detail' in pinfo:
                kiosk['printer_detail'] = pinfo['detail']
                break
        
        # 일별 인쇄량 조회
        try:
            today_row = db.execute(
                "SELECT daily_count FROM printer_daily_count WHERE hosp_cd=? AND kiosk_id=? AND date=date('now')",
                (hc, kiosk['kiosk_id'])).fetchone()
            kiosk['today_print'] = today_row[0] if today_row else 0
            
            avg_row = db.execute(
                "SELECT AVG(daily_count) FROM printer_daily_count WHERE hosp_cd=? AND kiosk_id=? AND date >= date('now','-7 days') AND daily_count > 0",
                (hc, kiosk['kiosk_id'])).fetchone()
            kiosk['avg7_print'] = round(avg_row[0]) if avg_row and avg_row[0] else 0
        except:
            kiosk['today_print'] = 0
            kiosk['avg7_print'] = 0
        
        if hc not in hospitals:
            hospitals[hc] = {'hosp_cd': hc, 'kiosks': []}
        hospitals[hc]['kiosks'].append(kiosk)
    
    # 병원명 매핑 (MSSQL에서)
    try:
        conn = get_mssql_connection()
        cursor = conn.cursor()
        codes = list(hospitals.keys())
        if codes:
            placeholders = ','.join(['?' for _ in codes])
            cursor.execute(f"SELECT HOSP_CD, HOSP_NAME FROM KIOSK_HOSP_INFO WHERE HOSP_CD IN ({placeholders})", codes)
            for row in cursor.fetchall():
                if row[0] in hospitals:
                    hospitals[row[0]]['hosp_name'] = row[1]
        conn.close()
    except:
        pass
    
    # 기본 매핑
    default_names = {'000': '테스트센터', '002': '강남베드로병원',
        '038': '가자연세병원', '165': '강남힐병원', '050': '고운세상병원',
        '077': '나무병원', '088': '다나병원', '091': '대림성모병원',
        '100': '동탄시티병원', '110': '명지병원', '115': '봄빛병원',
        '120': '삼성미래병원', '130': '서울나우병원', '140': '아주좋은병원',
        '150': '연세한마음병원'}
    result = list(hospitals.values())
    for h in result:
        if 'hosp_name' not in h:
            h['hosp_name'] = default_names.get(h['hosp_cd'], h['hosp_cd'])
    
    # 통계
    total_kiosks = sum(len(h['kiosks']) for h in result)
    online = sum(1 for h in result for k in h['kiosks'] if k['status'] == 'online')
    printer_warn = sum(1 for h in result for k in h['kiosks'] 
                       if k.get('printer_detail',{}).get('toner_black',{}).get('pct',100) <= 20
                       or any(k.get('printer_detail',{}).get(t,{}).get('pct',100) <= 0 for t in ['tray1_mp','tray2','tray3']))
    
    return jsonify({
        'hospitals': result,
        'stats': {
            'total_hospitals': len(result),
            'total_kiosks': total_kiosks,
            'online': online,
            'offline': total_kiosks - online,
            'printer_warnings': printer_warn
        }
    })


@app.route('/api/printer-daily/<hosp_cd>/<kiosk_id>')
@login_required
def api_printer_daily(hosp_cd, kiosk_id):
    """프린터 일별 인쇄량 조회 (최근 30일)"""
    db = get_monitor_db()
    rows = db.execute(
        "SELECT date, daily_count, total_count, toner_pct, tray1_pct, tray2_pct, tray3_pct FROM printer_daily_count WHERE hosp_cd=? AND kiosk_id=? ORDER BY date DESC LIMIT 30",
        (hosp_cd, kiosk_id)).fetchall()
    result = []
    for r in rows:
        result.append({
            'date': r[0], 'daily': r[1], 'total': r[2],
            'toner': r[3], 'tray1': r[4], 'tray2': r[5], 'tray3': r[6]
        })
    return jsonify({'daily': list(reversed(result))})

@app.route('/api/printer-summary')
@login_required
def api_printer_summary():
    """전체 프린터 일별 인쇄량 요약"""
    db = get_monitor_db()
    # 오늘
    today_rows = db.execute(
        "SELECT SUM(daily_count) FROM printer_daily_count WHERE date=date('now')").fetchone()
    today_total = today_rows[0] if today_rows and today_rows[0] else 0
    
    # 최근 7일
    week_rows = db.execute(
        "SELECT date, SUM(daily_count) FROM printer_daily_count WHERE date >= date('now','-7 days') GROUP BY date ORDER BY date").fetchall()
    weekly = [{'date': r[0], 'count': r[1]} for r in week_rows]
    
    # 최근 30일
    month_rows = db.execute(
        "SELECT date, SUM(daily_count) FROM printer_daily_count WHERE date >= date('now','-30 days') GROUP BY date ORDER BY date").fetchall()
    monthly = [{'date': r[0], 'count': r[1]} for r in month_rows]
    
    return jsonify({'today': today_total, 'weekly': weekly, 'monthly': monthly})

@app.route('/api/printer-status')
@login_required
def api_printer_status():
    db = get_monitor_db()
    rows = db.execute("SELECT hosp_cd, kiosk_id, network_printers, last_heartbeat FROM kiosk_status WHERE network_printers IS NOT NULL AND network_printers != '' AND network_printers != '{}'").fetchall()
    result = []
    import json
    for r in rows:
        try:
            printers = json.loads(r[2])
            for name, info in printers.items():
                entry = {
                    'hosp_cd': r[0],
                    'kiosk_id': r[1],
                    'printer_name': name,
                    'ip': info.get('ip',''),
                    'status': info.get('status','unknown'),
                    'last_heartbeat': r[3]
                }
                if 'detail' in info:
                    entry['detail'] = info['detail']
                result.append(entry)
        except:
            pass
    return jsonify({'printers': result})

@app.route('/api/widget-data/<widget_type>')
@login_required
def widget_data(widget_type):
    try:
        conn = get_db()
        cur = conn.cursor()
        if widget_type == 'kpi_summary':
            cur.execute("SELECT COUNT(*), SUM(KIOSK_CNT) FROM KIOSK_HOSP_INFO WHERE EMR_COMPANY NOT IN ('MCC','NSS')")
            s = cur.fetchone()
            cur.execute("SELECT COUNT(*) FROM KIOSK_HOSP_INFO WHERE USER_YN='Y' AND EMR_COMPANY NOT IN ('MCC','NSS')")
            a = cur.fetchone()[0]
            conn.close()
            return jsonify({'total_hosp': s[0], 'total_kiosk': s[1] or 0, 'active_hosp': a})
        elif widget_type == 'today_usage':
            from datetime import date, datetime
            today = date.today().strftime('%Y-%m-%d')
            cur.execute("SELECT COUNT(DISTINCT c.HOSP_CD), COUNT(DISTINCT c.KIOSK_ID), SUM(ISNULL(c.COUNT_01,0)+ISNULL(c.COUNT_02,0)+ISNULL(c.COUNT_03,0)+ISNULL(c.COUNT_04,0)+ISNULL(c.COUNT_05,0)+ISNULL(c.COUNT_06,0)+ISNULL(c.COUNT_07,0)+ISNULL(c.COUNT_08,0)+ISNULL(c.COUNT_09,0)+ISNULL(c.COUNT_10,0)+ISNULL(c.COUNT_11,0)+ISNULL(c.COUNT_12,0)+ISNULL(c.COUNT_13,0)) FROM KIOSK_HOSP_COUNT c INNER JOIN KIOSK_HOSP_INFO i ON c.HOSP_CD=i.HOSP_CD WHERE c.COUNT_DATE='" + today + "' AND i.EMR_COMPANY NOT IN ('MCC','NSS')")
            r = cur.fetchone()
            conn.close()
            return jsonify({'hosp_count': r[0] or 0, 'kiosk_count': r[1] or 0, 'total_count': r[2] or 0})
        elif widget_type == 'isv_list':
            cur.execute("SELECT EMR_COMPANY, COUNT(*) as cnt FROM KIOSK_HOSP_INFO WHERE EMR_COMPANY NOT IN ('MCC','NSS') GROUP BY EMR_COMPANY ORDER BY cnt DESC")
            rows = cur.fetchall()
            conn.close()
            return jsonify({'isv': [{'name': r[0], 'count': r[1]} for r in rows]})
        elif widget_type == 'recent_usage':
            cur.execute("SELECT TOP 10 c.HOSP_NM, c.KIOSK_ID, c.COUNT_DATE, ISNULL(c.COUNT_01,0)+ISNULL(c.COUNT_02,0)+ISNULL(c.COUNT_03,0)+ISNULL(c.COUNT_04,0)+ISNULL(c.COUNT_05,0)+ISNULL(c.COUNT_06,0)+ISNULL(c.COUNT_07,0)+ISNULL(c.COUNT_08,0)+ISNULL(c.COUNT_09,0)+ISNULL(c.COUNT_10,0)+ISNULL(c.COUNT_11,0)+ISNULL(c.COUNT_12,0)+ISNULL(c.COUNT_13,0) as tc, c.HOSP_CD FROM KIOSK_HOSP_COUNT c INNER JOIN KIOSK_HOSP_INFO i ON c.HOSP_CD=i.HOSP_CD WHERE i.EMR_COMPANY NOT IN ('MCC','NSS') ORDER BY c.COUNT_DATE DESC, tc DESC")
            rows = cur.fetchall()
            conn.close()
            return jsonify({'data': [{'name': r[0], 'kiosk': r[1], 'date': r[2], 'count': r[3], 'code': r[4]} for r in rows]})
        else:
            conn.close()
            return jsonify({'error': 'unknown widget'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/dashboard-preview')
@login_required
def dashboard_preview():
    return render_template('dashboard_preview.html')


@app.route('/alarms')
@login_required
def alarm_list():
    db = get_monitor_db()
    status_filter = request.args.get('status', 'all')
    org_type, org_code = get_user_filter()
    extra_where = ''
    params = []
    if org_type == 'hospital':
        extra_where = ' AND a.hosp_cd=?'
        params = [org_code]
    elif org_type == 'isv':
        conn_tmp = get_db()
        cur_tmp = conn_tmp.cursor()
        cur_tmp.execute("SELECT HOSP_CD FROM KIOSK_HOSP_INFO WHERE EMR_COMPANY=?", (org_code,))
        my_hosps = [r[0] for r in cur_tmp.fetchall()]
        conn_tmp.close()
        if my_hosps:
            extra_where = ' AND a.hosp_cd IN (' + ','.join(['?' for _ in my_hosps]) + ')'
            params = my_hosps
        else:
            extra_where = ' AND 1=0'
    if status_filter == 'all':
        alarms = db.execute("""SELECT a.*, 
            (SELECT COUNT(*) FROM tickets t WHERE t.alarm_id=a.id) as ticket_count
            FROM alarms a WHERE 1=1""" + extra_where + " ORDER BY a.created_at DESC LIMIT 100", params).fetchall()
    else:
        alarms = db.execute("""SELECT a.*,
            (SELECT COUNT(*) FROM tickets t WHERE t.alarm_id=a.id) as ticket_count
            FROM alarms a WHERE a.status=?""" + extra_where + " ORDER BY a.created_at DESC LIMIT 100", [status_filter] + params).fetchall()
    stats = {
        'total': db.execute("SELECT COUNT(*) FROM alarms").fetchone()[0],
        'open': db.execute("SELECT COUNT(*) FROM alarms WHERE status='open'").fetchone()[0],
        'acknowledged': db.execute("SELECT COUNT(*) FROM alarms WHERE status='acknowledged'").fetchone()[0],
        'resolved': db.execute("SELECT COUNT(*) FROM alarms WHERE status='resolved'").fetchone()[0]
    }
    db.close()
    return render_template('alarms.html', alarms=alarms, stats=stats, current_filter=status_filter)

@app.route('/alarm/<int:alarm_id>/acknowledge', methods=['POST'])
@login_required
def acknowledge_alarm(alarm_id):
    db = get_monitor_db()
    db.execute("UPDATE alarms SET status='acknowledged', acknowledged_by=?, acknowledged_at=CURRENT_TIMESTAMP WHERE id=?",
               (session.get('username'), alarm_id))
    db.commit()
    db.close()
    return redirect('/alarms')

@app.route('/alarm/<int:alarm_id>/resolve', methods=['POST'])
@login_required
def resolve_alarm(alarm_id):
    db = get_monitor_db()
    db.execute("UPDATE alarms SET status='resolved', resolved_by=?, resolved_at=CURRENT_TIMESTAMP WHERE id=?",
               (session.get('username'), alarm_id))
    db.commit()
    db.close()
    return redirect('/alarms')

@app.route('/tickets')
@login_required
def ticket_list():
    db = get_monitor_db()
    status_filter = request.args.get('status', 'all')
    org_type, org_code = get_user_filter()
    extra_where = ''
    params = []
    if org_type == 'hospital':
        extra_where = ' AND hosp_cd=?'
        params = [org_code]
    elif org_type == 'isv':
        conn_tmp = get_db()
        cur_tmp = conn_tmp.cursor()
        cur_tmp.execute("SELECT HOSP_CD FROM KIOSK_HOSP_INFO WHERE EMR_COMPANY=?", (org_code,))
        my_hosps = [r[0] for r in cur_tmp.fetchall()]
        conn_tmp.close()
        if my_hosps:
            extra_where = ' AND hosp_cd IN (' + ','.join(['?' for _ in my_hosps]) + ')'
            params = my_hosps
        else:
            extra_where = ' AND 1=0'
    if status_filter == 'all':
        tickets = db.execute("SELECT * FROM tickets WHERE 1=1" + extra_where + " ORDER BY created_at DESC LIMIT 100", params).fetchall()
    else:
        tickets = db.execute("SELECT * FROM tickets WHERE status=?" + extra_where + " ORDER BY created_at DESC LIMIT 100", [status_filter] + params).fetchall()
    stats = {
        'total': db.execute("SELECT COUNT(*) FROM tickets").fetchone()[0],
        'open': db.execute("SELECT COUNT(*) FROM tickets WHERE status='open'").fetchone()[0],
        'in_progress': db.execute("SELECT COUNT(*) FROM tickets WHERE status='in_progress'").fetchone()[0],
        'closed': db.execute("SELECT COUNT(*) FROM tickets WHERE status='closed'").fetchone()[0]
    }
    db.close()
    return render_template('tickets.html', tickets=tickets, stats=stats, current_filter=status_filter)

@app.route('/ticket/new', methods=['GET','POST'])
@login_required
def ticket_new():
    if request.method == 'POST':
        db = get_monitor_db()
        db.execute("INSERT INTO tickets (hosp_cd, kiosk_id, title, description, priority, category, created_by) VALUES (?,?,?,?,?,?,?)",
                   (request.form.get('hosp_cd',''), request.form.get('kiosk_id',''),
                    request.form['title'], request.form.get('description',''),
                    request.form.get('priority','medium'), request.form.get('category',''),
                    session.get('username')))
        db.commit()
        db.close()
        return redirect('/tickets')
    return render_template('ticket_form.html', ticket=None)

@app.route('/ticket/<int:ticket_id>')
@login_required
def ticket_detail(ticket_id):
    db = get_monitor_db()
    ticket = db.execute("SELECT * FROM tickets WHERE id=?", (ticket_id,)).fetchone()
    comments = db.execute("SELECT * FROM ticket_comments WHERE ticket_id=? ORDER BY created_at", (ticket_id,)).fetchall()
    db.close()
    if not ticket:
        return redirect('/tickets')
    return render_template('ticket_detail.html', ticket=ticket, comments=comments)

@app.route('/ticket/<int:ticket_id>/comment', methods=['POST'])
@login_required
def ticket_comment(ticket_id):
    db = get_monitor_db()
    db.execute("INSERT INTO ticket_comments (ticket_id, author, comment) VALUES (?,?,?)",
               (ticket_id, session.get('username'), request.form['comment']))
    db.execute("UPDATE tickets SET updated_at=CURRENT_TIMESTAMP WHERE id=?", (ticket_id,))
    db.commit()
    db.close()
    return redirect(f'/ticket/{ticket_id}')

@app.route('/ticket/<int:ticket_id>/status', methods=['POST'])
@login_required
def ticket_status(ticket_id):
    new_status = request.form['status']
    db = get_monitor_db()
    if new_status == 'closed':
        db.execute("UPDATE tickets SET status=?, closed_at=CURRENT_TIMESTAMP, updated_at=CURRENT_TIMESTAMP WHERE id=?", (new_status, ticket_id))
    else:
        db.execute("UPDATE tickets SET status=?, updated_at=CURRENT_TIMESTAMP WHERE id=?", (new_status, ticket_id))
    db.commit()
    db.close()
    return redirect(f'/ticket/{ticket_id}')


@app.route('/api/agent/heartbeat', methods=['POST'])
def agent_heartbeat():
    data = request.get_json()
    if not data or not data.get('hosp_cd') or not data.get('kiosk_id'):
        return jsonify({'error': 'missing fields'}), 400

    token = request.headers.get('X-Agent-Token', '')
    if token != 'bseye-agent-2026':
        return jsonify({'error': 'unauthorized'}), 401

    db = get_monitor_db()

    # 하트비트 로그
    db.execute("INSERT INTO heartbeat_log (hosp_cd, kiosk_id, agent_version, ip_address) VALUES (?,?,?,?)",
               (data['hosp_cd'], data['kiosk_id'], data.get('agent_version',''), request.headers.get('X-Real-IP', request.remote_addr)))

    # 키오스크 상태 업데이트 (최신 1건만 유지)
    existing = db.execute("SELECT id FROM kiosk_status WHERE hosp_cd=? AND kiosk_id=?",
                          (data['hosp_cd'], data['kiosk_id'])).fetchone()
    if existing:
        db.execute("""UPDATE kiosk_status SET
            status=?, cpu_usage=?, memory_usage=?, disk_usage=?,
            printer_a4=?, printer_thermal=?, card_reader=?, barcode_reader=?,
            network_speed=?, emr_connection=?, network_printers=?, agent_version=?, last_heartbeat=CURRENT_TIMESTAMP
            WHERE hosp_cd=? AND kiosk_id=?""",
            (data.get('status','online'), data.get('cpu',0), data.get('memory',0), data.get('disk',0),
             data.get('printer_a4','unknown'), data.get('printer_thermal','unknown'),
             data.get('card_reader','unknown'), data.get('barcode_reader','unknown'),
             data.get('network_speed',0), data.get('emr_connection','unknown'),
             json.dumps(data.get('network_printers',{})), data.get('agent_version',''), data['hosp_cd'], data['kiosk_id']))
    else:
        db.execute("""INSERT INTO kiosk_status
            (hosp_cd, kiosk_id, status, cpu_usage, memory_usage, disk_usage,
             printer_a4, printer_thermal, card_reader, barcode_reader,
             network_speed, emr_connection, network_printers, agent_version, last_heartbeat)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,CURRENT_TIMESTAMP)""",
            (data['hosp_cd'], data['kiosk_id'], data.get('status','online'),
             data.get('cpu',0), data.get('memory',0), data.get('disk',0),
             data.get('printer_a4','unknown'), data.get('printer_thermal','unknown'),
             data.get('card_reader','unknown'), data.get('barcode_reader','unknown'),
             data.get('network_speed',0), data.get('emr_connection','unknown'),
             json.dumps(data.get('network_printers',{})), data.get('agent_version','')))

    # 장비 마스터 자동 등록/업데이트
    dev = db.execute("SELECT id FROM kiosk_devices WHERE hosp_cd=? AND kiosk_id=?",
                     (data['hosp_cd'], data['kiosk_id'])).fetchone()
    if dev:
        db.execute("UPDATE kiosk_devices SET os_version=?, ip_local=?, ip_public=?, updated_at=CURRENT_TIMESTAMP WHERE hosp_cd=? AND kiosk_id=?",
                   (data.get('os_version',''), data.get('ip_local',''), request.headers.get('X-Real-IP',''),
                    data['hosp_cd'], data['kiosk_id']))
    else:
        db.execute("INSERT INTO kiosk_devices (hosp_cd, kiosk_id, os_version, ip_local, ip_public) VALUES (?,?,?,?,?)",
                   (data['hosp_cd'], data['kiosk_id'], data.get('os_version',''),
                    data.get('ip_local',''), request.headers.get('X-Real-IP','')))

    # 자동 알람 체크
    alerts = []
    if data.get('cpu', 0) > 90:
        alerts.append(('cpu_high', 'warning', 'CPU 사용률 높음', f"CPU {data['cpu']}%"))
    if data.get('memory', 0) > 90:
        alerts.append(('memory_high', 'warning', '메모리 사용률 높음', f"메모리 {data['memory']}%"))
    if data.get('disk', 0) > 90:
        alerts.append(('disk_high', 'warning', '디스크 사용률 높음', f"디스크 {data['disk']}%"))
    if data.get('printer_a4') == 'error':
        alerts.append(('printer_a4_error', 'critical', 'A4 프린터 오류', 'A4 프린터 응답 없음'))
    if data.get('printer_thermal') == 'error':
        alerts.append(('printer_thermal_error', 'critical', '영수증 프린터 오류', '영수증 프린터 응답 없음'))
    if data.get('card_reader') == 'error':
        alerts.append(('card_reader_error', 'critical', '카드리더기 오류', '카드리더기 응답 없음'))
    if data.get('emr_connection') == 'error':
        alerts.append(('emr_error', 'critical', 'EMR 연결 실패', 'EMR 서버 연결 불가'))

    for atype, severity, title, msg in alerts:
        existing_alarm = db.execute(
            "SELECT id FROM alarms WHERE hosp_cd=? AND kiosk_id=? AND alarm_type=? AND status!='resolved' ORDER BY created_at DESC LIMIT 1",
            (data['hosp_cd'], data['kiosk_id'], atype)).fetchone()
        if not existing_alarm:
            db.execute("INSERT INTO alarms (hosp_cd, kiosk_id, alarm_type, severity, title, message) VALUES (?,?,?,?,?,?)",
                       (data['hosp_cd'], data['kiosk_id'], atype, severity, title, msg))

    db.commit()
    db.close()

    # === 일별 인쇄량 기록 ===
    try:
        import json as _pjson
        np_raw = data.get('network_printers', {})
        if isinstance(np_raw, str):
            np_raw = _pjson.loads(np_raw) if np_raw else {}
        for pname, pinfo in np_raw.items():
            detail = pinfo.get('detail', {})
            if not detail or not detail.get('page_count'):
                continue
            today = datetime.now().strftime('%Y-%m-%d')
            total = detail['page_count']
            toner = (detail.get('toner_black') or {}).get('pct', 0)
            t1 = (detail.get('tray1_mp') or {}).get('pct', 0)
            t2 = (detail.get('tray2') or {}).get('pct', 0)
            t3 = (detail.get('tray3') or {}).get('pct', 0)
            prev = db.execute(
                "SELECT total_count FROM printer_daily_count WHERE hosp_cd=? AND kiosk_id=? AND printer_name=? AND date<? ORDER BY date DESC LIMIT 1",
                (data['hosp_cd'], data['kiosk_id'], pname, today)).fetchone()
            prev_total = prev[0] if prev else 0
            daily = total - prev_total if prev_total > 0 else 0
            if daily < 0:
                daily = 0
            existing = db.execute(
                "SELECT id FROM printer_daily_count WHERE hosp_cd=? AND kiosk_id=? AND printer_name=? AND date=?",
                (data['hosp_cd'], data['kiosk_id'], pname, today)).fetchone()
            if existing:
                db.execute(
                    "UPDATE printer_daily_count SET total_count=?, daily_count=?, toner_pct=?, tray1_pct=?, tray2_pct=?, tray3_pct=? WHERE id=?",
                    (total, daily, toner, t1, t2, t3, existing[0]))
            else:
                db.execute(
                    "INSERT INTO printer_daily_count (hosp_cd, kiosk_id, printer_name, date, total_count, daily_count, toner_pct, tray1_pct, tray2_pct, tray3_pct) VALUES (?,?,?,?,?,?,?,?,?,?)",
                    (data['hosp_cd'], data['kiosk_id'], pname, today, total, daily, toner, t1, t2, t3))
            db.commit()
    except:
        pass

    return jsonify({'status': 'ok', 'alerts': len(alerts)})

@app.route('/api/agent/status')
@login_required
def agent_status_list():
    db = get_monitor_db()
    statuses = db.execute("""SELECT s.*, d.teamviewer_id, d.model
        FROM kiosk_status s
        LEFT JOIN kiosk_devices d ON s.hosp_cd=d.hosp_cd AND s.kiosk_id=d.kiosk_id
        ORDER BY s.last_heartbeat DESC""").fetchall()
    db.close()
    return jsonify({'data': [dict(zip(
        ['id','hosp_cd','kiosk_id','status','cpu','memory','disk',
         'printer_a4','printer_thermal','card_reader','barcode_reader',
         'network_speed','emr_connection','agent_version','last_heartbeat','created_at',
         'teamviewer_id','model'], r)) for r in statuses]})



@app.route('/maintenance')
def maintenance():
    return render_template('maintenance.html')

@app.route('/monitoring')
@login_required
def monitoring():
    db = get_monitor_db()
    org_type, org_code = get_user_filter()
    if org_type == 'isv':
        conn_tmp = get_db()
        cur_tmp = conn_tmp.cursor()
        cur_tmp.execute("SELECT HOSP_CD FROM KIOSK_HOSP_INFO WHERE EMR_COMPANY=?", (org_code,))
        my_hosps = [r[0] for r in cur_tmp.fetchall()]
        conn_tmp.close()
        if my_hosps:
            placeholders = ','.join(['?' for _ in my_hosps])
            statuses = db.execute("""SELECT s.hosp_cd, s.kiosk_id, s.status, s.cpu_usage, s.memory_usage, s.disk_usage,
                s.printer_a4, s.printer_thermal, s.card_reader, s.barcode_reader,
                s.network_speed, s.emr_connection, s.agent_version, s.last_heartbeat,
                d.teamviewer_id, d.model, d.os_version, d.ip_local
                FROM kiosk_status s
                LEFT JOIN kiosk_devices d ON s.hosp_cd=d.hosp_cd AND s.kiosk_id=d.kiosk_id
                WHERE s.hosp_cd IN (""" + placeholders + """)
                ORDER BY s.last_heartbeat DESC""", my_hosps).fetchall()
        else:
            statuses = []
    elif org_type == 'hospital':
        statuses = db.execute("""SELECT s.hosp_cd, s.kiosk_id, s.status, s.cpu_usage, s.memory_usage, s.disk_usage,
            s.printer_a4, s.printer_thermal, s.card_reader, s.barcode_reader,
            s.network_speed, s.emr_connection, s.agent_version, s.last_heartbeat,
            d.teamviewer_id, d.model, d.os_version, d.ip_local
            FROM kiosk_status s
            LEFT JOIN kiosk_devices d ON s.hosp_cd=d.hosp_cd AND s.kiosk_id=d.kiosk_id
            WHERE s.hosp_cd=?
            ORDER BY s.last_heartbeat DESC""", (org_code,)).fetchall()
    else:
        statuses = db.execute("""SELECT s.hosp_cd, s.kiosk_id, s.status, s.cpu_usage, s.memory_usage, s.disk_usage,
            s.printer_a4, s.printer_thermal, s.card_reader, s.barcode_reader,
            s.network_speed, s.emr_connection, s.agent_version, s.last_heartbeat,
            d.teamviewer_id, d.model, d.os_version, d.ip_local
            FROM kiosk_status s
            LEFT JOIN kiosk_devices d ON s.hosp_cd=d.hosp_cd AND s.kiosk_id=d.kiosk_id
            ORDER BY s.last_heartbeat DESC""").fetchall()
    stats = {
        'total': len(statuses),
        'online': sum(1 for s in statuses if s[2]=='online'),
        'error': sum(1 for s in statuses if s[2]=='error'),
        'offline': sum(1 for s in statuses if s[2] not in ('online','error'))
    }
    db.close()
    return render_template('monitoring.html', statuses=statuses, stats=stats)



@login_required
def monitoring2():
    return render_template('monitoring2.html')

@app.route('/monitoring3')
@login_required
def monitoring3():
    return render_template('monitoring3.html')

@app.route('/api/widget-data/alarm_summary')
@login_required
def widget_alarm_summary():
    db = get_monitor_db()
    o = db.execute("SELECT COUNT(*) FROM alarms WHERE status='open'").fetchone()[0]
    a = db.execute("SELECT COUNT(*) FROM alarms WHERE status='acknowledged'").fetchone()[0]
    db.close()
    return jsonify({'open': o, 'acknowledged': a})

@app.route('/api/widget-data/ticket_summary')
@login_required
def widget_ticket_summary():
    db = get_monitor_db()
    o = db.execute("SELECT COUNT(*) FROM tickets WHERE status='open'").fetchone()[0]
    p = db.execute("SELECT COUNT(*) FROM tickets WHERE status='in_progress'").fetchone()[0]
    db.close()
    return jsonify({'open': o, 'in_progress': p})

@app.route('/api/widget-data/agent_summary')
@login_required
def widget_agent_summary():
    db = get_monitor_db()
    total = db.execute("SELECT COUNT(*) FROM kiosk_status").fetchone()[0]
    online = db.execute("SELECT COUNT(*) FROM kiosk_status WHERE status='online'").fetchone()[0]
    error = db.execute("SELECT COUNT(*) FROM kiosk_status WHERE status='error'").fetchone()[0]
    db.close()
    return jsonify({'total': total, 'online': online, 'error': error, 'offline': total - online - error})

@app.route('/api/widget-data/alarm_list')
@login_required
def widget_alarm_list():
    db = get_monitor_db()
    rows = db.execute("SELECT hosp_cd, kiosk_id, alarm_type, severity, title, status, created_at FROM alarms ORDER BY created_at DESC LIMIT 10").fetchall()
    db.close()
    return jsonify({'data': [{'hosp': r[0], 'kiosk': r[1], 'type': r[2], 'severity': r[3], 'title': r[4], 'status': r[5], 'time': r[6][:16] if r[6] else ''} for r in rows]})

@app.route('/api/widget-data/ticket_list')
@login_required
def widget_ticket_list():
    db = get_monitor_db()
    rows = db.execute("SELECT id, hosp_cd, title, priority, status, created_by, created_at FROM tickets ORDER BY created_at DESC LIMIT 10").fetchall()
    db.close()
    return jsonify({'data': [{'id': r[0], 'hosp': r[1], 'title': r[2], 'priority': r[3], 'status': r[4], 'author': r[5], 'time': r[6][:16] if r[6] else ''} for r in rows]})

@app.route('/api/widget-data/agent_status')
@login_required
def widget_agent_status():
    db = get_monitor_db()
    rows = db.execute("SELECT hosp_cd, kiosk_id, status, cpu_usage, memory_usage, disk_usage, printer_a4, card_reader, emr_connection, last_heartbeat FROM kiosk_status ORDER BY last_heartbeat DESC LIMIT 10").fetchall()
    db.close()
    return jsonify({'data': [{'hosp': r[0], 'kiosk': r[1], 'status': r[2], 'cpu': r[3], 'mem': r[4], 'disk': r[5], 'printer': r[6], 'card': r[7], 'emr': r[8], 'time': r[9][:16] if r[9] else ''} for r in rows]})

@app.route('/api/widget-data/weekly_trend')
@login_required
def widget_weekly_trend():
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT TOP 7 c.COUNT_DATE, SUM(ISNULL(c.COUNT_01,0)+ISNULL(c.COUNT_02,0)+ISNULL(c.COUNT_03,0)+ISNULL(c.COUNT_04,0)+ISNULL(c.COUNT_05,0)+ISNULL(c.COUNT_06,0)+ISNULL(c.COUNT_07,0)+ISNULL(c.COUNT_08,0)+ISNULL(c.COUNT_09,0)+ISNULL(c.COUNT_10,0)+ISNULL(c.COUNT_11,0)+ISNULL(c.COUNT_12,0)+ISNULL(c.COUNT_13,0)), COUNT(DISTINCT c.HOSP_CD) FROM KIOSK_HOSP_COUNT c INNER JOIN KIOSK_HOSP_INFO i ON c.HOSP_CD=i.HOSP_CD WHERE i.EMR_COMPANY NOT IN ('MCC','NSS') GROUP BY c.COUNT_DATE ORDER BY c.COUNT_DATE DESC")
        rows = cur.fetchall()
        conn.close()
        return jsonify({'data': [{'date': r[0], 'count': r[1] or 0, 'hosps': r[2] or 0} for r in reversed(rows)]})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/widgets')
@login_required
def get_widgets():
    db = get_monitor_db()
    rows = db.execute("SELECT widget_key, name, category, description, default_width, default_height, data_source, is_system FROM widgets WHERE is_active=1 ORDER BY category, name").fetchall()
    db.close()
    return jsonify({'widgets': [{'key': r[0], 'name': r[1], 'category': r[2], 'desc': r[3], 'w': r[4], 'h': r[5], 'source': r[6], 'system': r[7]} for r in rows]})

@app.route('/api/widgets/add', methods=['POST'])
@login_required
def add_custom_widget():
    data = request.get_json()
    db = get_monitor_db()
    try:
        db.execute("INSERT INTO widgets (widget_key, name, category, description, default_width, default_height, data_source, is_system) VALUES (?,?,?,?,?,?,?,0)",
            (data['key'], data['name'], data.get('category','custom'), data.get('desc',''), data.get('w',200), data.get('h',120), data.get('source','none')))
        db.commit()
        db.close()
    
        return jsonify({'ok': True})
    except Exception as e:
        db.close()
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        db.close()
        return jsonify({'error': str(e)}), 400


@app.route('/api/widget-data/monthly_trend')
@login_required
def widget_monthly_trend():
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT LEFT(c.COUNT_DATE,7) as month, SUM(ISNULL(c.COUNT_01,0)+ISNULL(c.COUNT_02,0)+ISNULL(c.COUNT_03,0)+ISNULL(c.COUNT_04,0)+ISNULL(c.COUNT_05,0)+ISNULL(c.COUNT_06,0)+ISNULL(c.COUNT_07,0)+ISNULL(c.COUNT_08,0)+ISNULL(c.COUNT_09,0)+ISNULL(c.COUNT_10,0)+ISNULL(c.COUNT_11,0)+ISNULL(c.COUNT_12,0)+ISNULL(c.COUNT_13,0)) as total, COUNT(DISTINCT c.HOSP_CD) as hosps FROM KIOSK_HOSP_COUNT c INNER JOIN KIOSK_HOSP_INFO i ON c.HOSP_CD=i.HOSP_CD WHERE i.EMR_COMPANY NOT IN ('MCC','NSS') GROUP BY LEFT(c.COUNT_DATE,7) ORDER BY month DESC")
        rows = cur.fetchall()[:12]
        conn.close()
        return jsonify({'data': [{'month': r[0], 'count': r[1] or 0, 'hosps': r[2] or 0} for r in reversed(rows)]})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/widget-data/hourly_usage')
@login_required
def widget_hourly_usage():
    try:
        conn = get_db()
        cur = conn.cursor()
        from datetime import date, datetime
        today = date.today().strftime('%Y-%m-%d')
        cur.execute("SELECT c.COUNT_DATE, ISNULL(c.COUNT_01,0) as h1, ISNULL(c.COUNT_02,0) as h2, ISNULL(c.COUNT_03,0) as h3, ISNULL(c.COUNT_04,0) as h4, ISNULL(c.COUNT_05,0) as h5, ISNULL(c.COUNT_06,0) as h6, ISNULL(c.COUNT_07,0) as h7, ISNULL(c.COUNT_08,0) as h8, ISNULL(c.COUNT_09,0) as h9, ISNULL(c.COUNT_10,0) as h10, ISNULL(c.COUNT_11,0) as h11, ISNULL(c.COUNT_12,0) as h12, ISNULL(c.COUNT_13,0) as h13 FROM KIOSK_HOSP_COUNT c INNER JOIN KIOSK_HOSP_INFO i ON c.HOSP_CD=i.HOSP_CD WHERE c.COUNT_DATE='" + today + "' AND i.EMR_COMPANY NOT IN ('MCC','NSS')")
        rows = cur.fetchall()
        conn.close()
        totals = [0]*13
        for r in rows:
            for i in range(13):
                totals[i] += r[i+1] or 0
        labels = ['구간1','구간2','구간3','구간4','구간5','구간6','구간7','구간8','구간9','구간10','구간11','구간12','구간13']
        return jsonify({'labels': labels, 'data': totals})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/widget-data/isv_today')
@login_required
def widget_isv_today():
    try:
        conn = get_db()
        cur = conn.cursor()
        from datetime import date, datetime
        today = date.today().strftime('%Y-%m-%d')
        cur.execute("SELECT i.EMR_COMPANY, SUM(ISNULL(c.COUNT_01,0)+ISNULL(c.COUNT_02,0)+ISNULL(c.COUNT_03,0)+ISNULL(c.COUNT_04,0)+ISNULL(c.COUNT_05,0)+ISNULL(c.COUNT_06,0)+ISNULL(c.COUNT_07,0)+ISNULL(c.COUNT_08,0)+ISNULL(c.COUNT_09,0)+ISNULL(c.COUNT_10,0)+ISNULL(c.COUNT_11,0)+ISNULL(c.COUNT_12,0)+ISNULL(c.COUNT_13,0)) as total FROM KIOSK_HOSP_COUNT c INNER JOIN KIOSK_HOSP_INFO i ON c.HOSP_CD=i.HOSP_CD WHERE c.COUNT_DATE='" + today + "' AND i.EMR_COMPANY NOT IN ('MCC','NSS') GROUP BY i.EMR_COMPANY ORDER BY total DESC")
        rows = cur.fetchall()
        conn.close()
        return jsonify({'data': [{'isv': r[0], 'count': r[1] or 0} for r in rows]})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/widget-data/today_alarm')
@login_required
def widget_today_alarm():
    db = get_monitor_db()
    from datetime import date, datetime
    today = date.today().strftime('%Y-%m-%d')
    count = db.execute("SELECT COUNT(*) FROM alarms WHERE created_at >= ?", (today,)).fetchone()[0]
    db.close()
    return jsonify({'count': count})

@app.route('/api/widget-data/avg_response')
@login_required
def widget_avg_response():
    db = get_monitor_db()
    row = db.execute("SELECT AVG(network_speed) FROM kiosk_status WHERE status='online'").fetchone()
    db.close()
    return jsonify({'avg_ms': round(row[0] or 0, 1)})

@app.route('/api/widget-data/month_count')
@login_required
def widget_month_count():
    try:
        conn = get_db()
        cur = conn.cursor()
        from datetime import date, datetime
        month_prefix = date.today().strftime('%Y-%m')
        cur.execute("SELECT SUM(ISNULL(c.COUNT_01,0)+ISNULL(c.COUNT_02,0)+ISNULL(c.COUNT_03,0)+ISNULL(c.COUNT_04,0)+ISNULL(c.COUNT_05,0)+ISNULL(c.COUNT_06,0)+ISNULL(c.COUNT_07,0)+ISNULL(c.COUNT_08,0)+ISNULL(c.COUNT_09,0)+ISNULL(c.COUNT_10,0)+ISNULL(c.COUNT_11,0)+ISNULL(c.COUNT_12,0)+ISNULL(c.COUNT_13,0)) FROM KIOSK_HOSP_COUNT c INNER JOIN KIOSK_HOSP_INFO i ON c.HOSP_CD=i.HOSP_CD WHERE c.COUNT_DATE LIKE '" + month_prefix + "%' AND i.EMR_COMPANY NOT IN ('MCC','NSS')")
        row = cur.fetchone()
        conn.close()
        return jsonify({'count': row[0] or 0})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/widget-data/error_kiosks')
@login_required
def widget_error_kiosks():
    db = get_monitor_db()
    rows = db.execute("SELECT hosp_cd, kiosk_id, cpu_usage, memory_usage, printer_a4, card_reader, emr_connection, last_heartbeat FROM kiosk_status WHERE status='error' ORDER BY last_heartbeat DESC").fetchall()
    db.close()
    return jsonify({'data': [{'hosp': r[0], 'kiosk': r[1], 'cpu': r[2], 'mem': r[3], 'printer': r[4], 'card': r[5], 'emr': r[6], 'time': r[7][:16] if r[7] else ''} for r in rows]})

@app.route('/api/widget-data/no_heartbeat')
@login_required
def widget_no_heartbeat():
    db = get_monitor_db()
    rows = db.execute("SELECT hosp_cd, kiosk_id, status, agent_version, last_heartbeat FROM kiosk_status WHERE last_heartbeat < datetime('now','-1 hour') ORDER BY last_heartbeat").fetchall()
    db.close()
    return jsonify({'data': [{'hosp': r[0], 'kiosk': r[1], 'status': r[2], 'version': r[3], 'time': r[4][:16] if r[4] else ''} for r in rows]})

@app.route('/api/widget-data/top10_today')
@login_required
def widget_top10_today():
    try:
        conn = get_db()
        cur = conn.cursor()
        from datetime import date, datetime
        today = date.today().strftime('%Y-%m-%d')
        cur.execute("SELECT TOP 10 c.HOSP_NM, c.HOSP_CD, SUM(ISNULL(c.COUNT_01,0)+ISNULL(c.COUNT_02,0)+ISNULL(c.COUNT_03,0)+ISNULL(c.COUNT_04,0)+ISNULL(c.COUNT_05,0)+ISNULL(c.COUNT_06,0)+ISNULL(c.COUNT_07,0)+ISNULL(c.COUNT_08,0)+ISNULL(c.COUNT_09,0)+ISNULL(c.COUNT_10,0)+ISNULL(c.COUNT_11,0)+ISNULL(c.COUNT_12,0)+ISNULL(c.COUNT_13,0)) as total, COUNT(DISTINCT c.KIOSK_ID) as kiosks FROM KIOSK_HOSP_COUNT c INNER JOIN KIOSK_HOSP_INFO i ON c.HOSP_CD=i.HOSP_CD WHERE c.COUNT_DATE='" + today + "' AND i.EMR_COMPANY NOT IN ('MCC','NSS') GROUP BY c.HOSP_NM, c.HOSP_CD ORDER BY total DESC")
        rows = cur.fetchall()
        conn.close()
        return jsonify({'data': [{'name': r[0], 'code': r[1], 'count': r[2] or 0, 'kiosks': r[3] or 0} for r in rows]})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/widget-data/daily_trend')
@login_required
def widget_daily_trend():
    try:
        db = get_monitor_db()
        rows = db.execute("SELECT snap_date, total_count, active_hospitals FROM daily_summary ORDER BY snap_date DESC LIMIT 30").fetchall()
        db.close()
        rows = list(reversed(rows))
        return jsonify({
            'labels': [r[0][5:] for r in rows],
            'counts': [r[1] for r in rows],
            'hospitals': [r[2] for r in rows]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/widget-data/daily_hospital_trend')
@login_required
def widget_daily_hospital_trend():
    try:
        db = get_monitor_db()
        rows = db.execute("SELECT snap_date, total_hospitals, active_hospitals FROM daily_summary ORDER BY snap_date DESC LIMIT 30").fetchall()
        db.close()
        rows = list(reversed(rows))
        return jsonify({
            'labels': [r[0][5:] for r in rows],
            'total': [r[1] for r in rows],
            'active': [r[2] for r in rows]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/widget-data/snapshot_detail')
@login_required
def widget_snapshot_detail():
    try:
        db = get_monitor_db()
        rows = db.execute("""SELECT hosp_cd, hosp_name, SUM(total_count) as total, COUNT(DISTINCT kiosk_id) as kiosks
            FROM daily_usage_snapshot
            WHERE snap_date = (SELECT MAX(snap_date) FROM daily_summary)
            GROUP BY hosp_cd ORDER BY total DESC LIMIT 15""").fetchall()
        db.close()
        return jsonify({
            'items': [{'code': r[0], 'name': r[1], 'count': r[2], 'kiosks': r[3]} for r in rows]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/kiosk-editor')
@login_required
def kiosk_editor():
    return render_template('kiosk_editor.html')

@app.route('/api/kiosk-components')
@login_required
def get_kiosk_components():
    db = get_monitor_db()
    rows = db.execute("SELECT comp_key, name, category, icon, default_width, default_height, default_color, default_text_color FROM kiosk_components ORDER BY category, name").fetchall()
    db.close()
    return jsonify({'components': [{'key':r[0],'name':r[1],'category':r[2],'icon':r[3],'width':r[4],'height':r[5],'color':r[6],'textColor':r[7]} for r in rows]})

@app.route('/api/kiosk-design/<hosp_cd>')
@login_required
def get_kiosk_design(hosp_cd):
    db = get_monitor_db()
    row = db.execute("SELECT id, design_name, design_json, screen_width, screen_height FROM kiosk_designs WHERE hosp_cd=? AND is_active=1", (hosp_cd,)).fetchone()
    db.close()
    if row:
        return jsonify({'id':row[0],'name':row[1],'design':json.loads(row[2]),'width':row[3],'height':row[4]})
    return jsonify({'design':[],'width':1080,'height':1920})

@app.route('/api/kiosk-design/<hosp_cd>', methods=['POST'])
@login_required
def save_kiosk_design(hosp_cd):
    data = request.get_json()
    design_json = json.dumps(data.get('design', []))
    name = data.get('name', '기본 디자인')
    width = data.get('width', 1080)
    height = data.get('height', 1920)
    user = session.get('user_name', 'admin')
    db = get_monitor_db()
    existing = db.execute("SELECT id FROM kiosk_designs WHERE hosp_cd=? AND design_name=?", (hosp_cd, name)).fetchone()
    if existing:
        db.execute("UPDATE kiosk_designs SET design_json=?, screen_width=?, screen_height=?, updated_at=CURRENT_TIMESTAMP WHERE id=?", (design_json, width, height, existing[0]))
    else:
        db.execute("UPDATE kiosk_designs SET is_active=0 WHERE hosp_cd=?", (hosp_cd,))
        db.execute("INSERT INTO kiosk_designs (hosp_cd, design_name, design_json, screen_width, screen_height, is_active, created_by) VALUES (?,?,?,?,?,1,?)", (hosp_cd, name, design_json, width, height, user))
    db.commit()
    db.close()
    return jsonify({'status':'saved'})

@app.route('/api/kiosk-design-list/<hosp_cd>')
@login_required
def list_kiosk_designs(hosp_cd):
    db = get_monitor_db()
    rows = db.execute("SELECT id, design_name, is_active, created_by, updated_at FROM kiosk_designs WHERE hosp_cd=? ORDER BY updated_at DESC", (hosp_cd,)).fetchall()
    db.close()
    return jsonify({'designs': [{'id':r[0],'name':r[1],'active':r[2],'author':r[3],'updated':r[4]} for r in rows]})

@app.route('/api/kiosk-design-activate/<int:design_id>', methods=['POST'])
@login_required
def activate_kiosk_design(design_id):
    db = get_monitor_db()
    row = db.execute("SELECT hosp_cd FROM kiosk_designs WHERE id=?", (design_id,)).fetchone()
    if row:
        db.execute("UPDATE kiosk_designs SET is_active=0 WHERE hosp_cd=?", (row[0],))
        db.execute("UPDATE kiosk_designs SET is_active=1 WHERE id=?", (design_id,))
        db.commit()
    db.close()
    return jsonify({'status':'ok'})

@app.route('/api/kiosk-preview/<hosp_cd>')
@login_required
def kiosk_preview(hosp_cd):
    return render_template('kiosk_preview.html', hosp_cd=hosp_cd)


# ========== 경영진 대시보드 API ==========

@app.route('/executive')
@login_required
def executive_dashboard():
    return render_template('executive.html')

@app.route('/api/executive/overview')
@login_required
def api_exec_overview():
    """경영진 핵심 KPI"""
    import pyodbc
    from config import get_connection_string
    conn = pyodbc.connect(get_connection_string())
    cur = conn.cursor()
    
    # 전체 병원 수
    cur.execute("SELECT COUNT(*) FROM KIOSK_HOSP_INFO")
    total_hosp = cur.fetchone()[0]
    
    # 활성 병원 (USER_YN=Y)
    cur.execute("SELECT COUNT(*) FROM KIOSK_HOSP_INFO WHERE USER_YN='Y'")
    active_hosp = cur.fetchone()[0]
    
    # 서비스 활성
    cur.execute("SELECT COUNT(*) FROM KIOSK_HOSP_INFO WHERE SERVICE='Y'")
    service_hosp = cur.fetchone()[0]
    
    # 총 키오스크 대수
    cur.execute("SELECT ISNULL(SUM(CAST(KIOSK_CNT AS INT)),0) FROM KIOSK_HOSP_INFO WHERE KIOSK_CNT IS NOT NULL")
    total_kiosk = cur.fetchone()[0]
    
    # ISV별 병원 수
    cur.execute("SELECT EMR_COMPANY, COUNT(*) cnt FROM KIOSK_HOSP_INFO WHERE EMR_COMPANY IS NOT NULL AND EMR_COMPANY!=\'\'  GROUP BY EMR_COMPANY ORDER BY cnt DESC")
    isv_list = [{"name":str(r[0]),"count":r[1]} for r in cur.fetchall()]
    
    # 미사용 병원 (이탈 위험)
    cur.execute("SELECT COUNT(*) FROM KIOSK_HOSP_INFO WHERE USER_YN='N'")
    inactive_hosp = cur.fetchone()[0]
    
    conn.close()
    
    # SQLite에서 일일 트렌드
    import sqlite3
    lite = sqlite3.connect('monitor.db')
    lc = lite.cursor()
    lc.execute("SELECT snap_date, total_count, active_hospitals, active_kiosks FROM daily_summary ORDER BY snap_date DESC LIMIT 30")
    daily = [{"date":r[0],"count":r[1],"hospitals":r[2],"kiosks":r[3]} for r in lc.fetchall()]
    daily.reverse()
    lite.close()
    
    return jsonify({
        "total_hosp": total_hosp,
        "active_hosp": active_hosp,
        "service_hosp": service_hosp,
        "inactive_hosp": inactive_hosp,
        "total_kiosk": total_kiosk,
        "isv_list": isv_list,
        "daily_trend": daily
    })

@app.route('/api/executive/monthly')
@login_required
def api_exec_monthly():
    """월별 사용량 트렌드"""
    import pyodbc
    from config import get_connection_string
    conn = pyodbc.connect(get_connection_string())
    cur = conn.cursor()
    
    cur.execute("""
        SELECT LEFT(CONVERT(VARCHAR,COUNT_DATE,23),7) mon,
               COUNT(DISTINCT HOSP_CD) hospitals,
               COUNT(DISTINCT HOSP_CD+\'-\'+KIOSK_ID) kiosks,
               SUM(COUNT_01+COUNT_02+COUNT_03+COUNT_04+COUNT_05+COUNT_06+
                   COUNT_07+COUNT_08+COUNT_09+COUNT_10+COUNT_11+COUNT_12+COUNT_13) total
        FROM KIOSK_HOSP_COUNT
        WHERE COUNT_DATE >= DATEADD(MONTH,-12,GETDATE())
        GROUP BY LEFT(CONVERT(VARCHAR,COUNT_DATE,23),7)
        ORDER BY mon
    """)
    data = [{"month":str(r[0]),"hospitals":r[1],"kiosks":r[2],"count":int(r[3] or 0)} for r in cur.fetchall()]
    
    # 월별 성장률 계산
    for i in range(1, len(data)):
        prev = data[i-1]["count"]
        curr = data[i]["count"]
        data[i]["growth"] = round(((curr-prev)/prev*100),1) if prev > 0 else 0
    if data:
        data[0]["growth"] = 0
    
    conn.close()
    return jsonify({"monthly": data})

@app.route('/api/executive/isv-performance')
@login_required
def api_exec_isv():
    """ISV별 실적"""
    import pyodbc
    from config import get_connection_string
    conn = pyodbc.connect(get_connection_string())
    cur = conn.cursor()
    
    cur.execute("""
        SELECT i.EMR_COMPANY,
               COUNT(DISTINCT i.HOSP_CD) hosp_cnt,
               ISNULL(SUM(CAST(i.KIOSK_CNT AS INT)),0) kiosk_cnt,
               SUM(CASE WHEN i.USER_YN='Y' THEN 1 ELSE 0 END) active_cnt,
               SUM(CASE WHEN i.USER_YN='N' THEN 1 ELSE 0 END) inactive_cnt
        FROM KIOSK_HOSP_INFO i
        WHERE i.EMR_COMPANY IS NOT NULL AND i.EMR_COMPANY!='' AND i.EMR_COMPANY NOT IN ('MCC','NSS')
        GROUP BY i.EMR_COMPANY
        ORDER BY hosp_cnt DESC
    """)
    data = [{"isv":str(r[0]),"hospitals":r[1],"kiosks":r[2],"active":r[3],"inactive":r[4]} for r in cur.fetchall()]
    conn.close()
    return jsonify({"isv": data})

@app.route('/api/executive/risk-hospitals')
@login_required
def api_exec_risk():
    """이탈 위험 병원"""
    import sqlite3
    lite = sqlite3.connect('monitor.db')
    lc = lite.cursor()
    
    # 최근 7일 사용량이 0인 병원 (활성 병원 중)
    lc.execute("""
        SELECT hosp_cd, hosp_name, SUM(total_count) total
        FROM daily_usage_snapshot
        WHERE snap_date >= date('now','-7 days')
        GROUP BY hosp_cd
        HAVING total = 0
    """)
    zero_usage = [{"hosp_cd":r[0],"hosp_name":r[1],"total":r[2]} for r in lc.fetchall()]
    
    # 사용량 하위 10개 병원
    lc.execute("""
        SELECT hosp_cd, hosp_name, SUM(total_count) total
        FROM daily_usage_snapshot
        WHERE snap_date >= date('now','-7 days')
        GROUP BY hosp_cd
        ORDER BY total ASC
        LIMIT 10
    """)
    low_usage = [{"hosp_cd":r[0],"hosp_name":r[1],"total":r[2]} for r in lc.fetchall()]
    
    lite.close()
    # ISV 정보 매핑
    try:
        import pyodbc
        from config import get_connection_string
        mconn = pyodbc.connect(get_connection_string())
        mcur = mconn.cursor()
        mcur.execute("SELECT HOSP_CD, EMR_COMPANY FROM KIOSK_HOSP_INFO")
        isv_map = {r[0]: r[1] for r in mcur.fetchall()}
        mconn.close()
        for item in low_usage:
            item['isv'] = isv_map.get(item['hosp_cd'], '')
    except:
        for item in low_usage:
            item['isv'] = ''
    return jsonify({"zero_usage": zero_usage, "low_usage": low_usage})

@app.route('/api/executive/top-hospitals')
@login_required
def api_exec_top():
    """사용량 상위 병원"""
    import sqlite3
    lite = sqlite3.connect('monitor.db')
    lc = lite.cursor()
    
    lc.execute("""
        SELECT hosp_cd, hosp_name, SUM(total_count) total, COUNT(DISTINCT kiosk_id) kiosks
        FROM daily_usage_snapshot
        WHERE snap_date >= date('now','-7 days')
        GROUP BY hosp_cd
        ORDER BY total DESC
        LIMIT 15
    """)
    data = [{"hosp_cd":r[0],"hosp_name":r[1],"total":r[2],"kiosks":r[3]} for r in lc.fetchall()]
    lite.close()
    return jsonify({"top": data})



@app.route('/api/executive/scale-distribution')
@login_required
def api_exec_scale():
    """키오스크 대수별 병원 평균 사용량"""
    import pyodbc
    from config import get_connection_string
    conn = pyodbc.connect(get_connection_string())
    cur = conn.cursor()
    cur.execute("""
        SELECT grp, COUNT(*) hosp_cnt, AVG(total) avg_usage
        FROM (
            SELECT h.HOSP_CD,
                CASE
                    WHEN CAST(h.KIOSK_CNT AS INT)=1 THEN '1대'
                    WHEN CAST(h.KIOSK_CNT AS INT)=2 THEN '2대'
                    WHEN CAST(h.KIOSK_CNT AS INT)=3 THEN '3대'
                    ELSE '4대+'
                END grp,
                ISNULL((SELECT SUM(c.COUNT_01+c.COUNT_02+c.COUNT_03+c.COUNT_04+c.COUNT_05+c.COUNT_06+
                                    c.COUNT_07+c.COUNT_08+c.COUNT_09+c.COUNT_10+c.COUNT_11+c.COUNT_12+c.COUNT_13)
                        FROM KIOSK_HOSP_COUNT c
                        WHERE c.HOSP_CD=h.HOSP_CD AND c.COUNT_DATE >= DATEADD(DAY,-30,GETDATE())),0) total
            FROM KIOSK_HOSP_INFO h
            WHERE h.USER_YN='Y' AND h.KIOSK_CNT IS NOT NULL AND CAST(h.KIOSK_CNT AS INT)>0
        ) sub
        GROUP BY grp
        ORDER BY grp
    """)
    data = [{"group":str(r[0]),"hospitals":r[1],"avg_usage":int(r[2] or 0)} for r in cur.fetchall()]
    conn.close()
    return jsonify({"scale": data})


@app.route('/api/executive/weekday-heatmap')
@login_required
def api_exec_heatmap():
    """요일별 시간대 사용 히트맵 (최근 4주)"""
    import pyodbc
    from config import get_connection_string
    conn = pyodbc.connect(get_connection_string())
    cur = conn.cursor()
    cur.execute("""
        SELECT DATEPART(WEEKDAY, COUNT_DATE) wd,
               AVG(COUNT_01) h08, AVG(COUNT_02) h09, AVG(COUNT_03) h10,
               AVG(COUNT_04) h11, AVG(COUNT_05) h12, AVG(COUNT_06) h13,
               AVG(COUNT_07) h14, AVG(COUNT_08) h15, AVG(COUNT_09) h16,
               AVG(COUNT_10) h17, AVG(COUNT_11) h18, AVG(COUNT_12) h19,
               AVG(COUNT_13) h20
        FROM KIOSK_HOSP_COUNT
        WHERE COUNT_DATE >= DATEADD(DAY,-28,GETDATE())
        GROUP BY DATEPART(WEEKDAY, COUNT_DATE)
        ORDER BY wd
    """)
    days_map = {2:'월',3:'화',4:'수',5:'목',6:'금',7:'토',1:'일'}
    hours = ['08','09','10','11','12','13','14','15','16','17','18','19','20']
    result = []
    for r in cur.fetchall():
        wd = int(r[0])
        day_name = days_map.get(wd, str(wd))
        vals = [int(r[i+1] or 0) for i in range(13)]
        result.append({"day":day_name,"hours":vals})
    conn.close()
    return jsonify({"heatmap":result,"hours":hours})

# ========== 병원 뷰 대시보드 API ==========

@app.route('/hospital-view')
@login_required
def hospital_view():
    hosp_cd = request.args.get('hosp_cd', '')
    role = session.get('user_role','')
    if role.startswith('hosp_'):
        hosp_cd = session.get('hosp_cd','')
    return render_template('hospital_view.html', hosp_cd=hosp_cd)

@app.route('/api/hospital-view/summary/<hosp_cd>')
@login_required
def api_hosp_summary(hosp_cd):
    import pyodbc
    from config import get_connection_string
    conn = pyodbc.connect(get_connection_string())
    cur = conn.cursor()
    
    # 병원 기본 정보
    cur.execute("SELECT HOSP_NM, ADDR1, EMR_COMPANY, KIOSK_CNT, IPGO_DATE, OPEN_DATE, USER_YN, SERVICE FROM KIOSK_HOSP_INFO WHERE HOSP_CD=?", hosp_cd)
    row = cur.fetchone()
    if not row:
        conn.close()
        return jsonify({"error":"병원 없음"})
    
    info = {
        "hosp_cd": hosp_cd,
        "hosp_name": str(row[0] or ''),
        "addr": str(row[1] or ''),
        "isv": str(row[2] or ''),
        "kiosk_cnt": int(row[3] or 0),
        "ipgo_date": str(row[4] or ''),
        "open_date": str(row[5] or ''),
        "user_yn": str(row[6] or ''),
        "service": str(row[7] or '')
    }
    
    # 이번달 사용량
    cur.execute("""
        SELECT SUM(COUNT_01+COUNT_02+COUNT_03+COUNT_04+COUNT_05+COUNT_06+
                    COUNT_07+COUNT_08+COUNT_09+COUNT_10+COUNT_11+COUNT_12+COUNT_13) total
        FROM KIOSK_HOSP_COUNT
        WHERE HOSP_CD=? AND COUNT_DATE >= DATEADD(DAY,1-DAY(GETDATE()),CAST(GETDATE() AS DATE))
    """, hosp_cd)
    r = cur.fetchone()
    info["month_count"] = int(r[0] or 0) if r else 0
    
    # 전월 사용량
    cur.execute("""
        SELECT SUM(COUNT_01+COUNT_02+COUNT_03+COUNT_04+COUNT_05+COUNT_06+
                    COUNT_07+COUNT_08+COUNT_09+COUNT_10+COUNT_11+COUNT_12+COUNT_13) total
        FROM KIOSK_HOSP_COUNT
        WHERE HOSP_CD=? AND COUNT_DATE >= DATEADD(MONTH,-1,DATEADD(DAY,1-DAY(GETDATE()),CAST(GETDATE() AS DATE)))
              AND COUNT_DATE < DATEADD(DAY,1-DAY(GETDATE()),CAST(GETDATE() AS DATE))
    """, hosp_cd)
    r = cur.fetchone()
    info["prev_month_count"] = int(r[0] or 0) if r else 0
    
    # 전전월 사용량
    cur.execute("""
        SELECT SUM(COUNT_01+COUNT_02+COUNT_03+COUNT_04+COUNT_05+COUNT_06+
                    COUNT_07+COUNT_08+COUNT_09+COUNT_10+COUNT_11+COUNT_12+COUNT_13) total
        FROM KIOSK_HOSP_COUNT
        WHERE HOSP_CD=? AND COUNT_DATE >= DATEADD(MONTH,-2,DATEADD(DAY,1-DAY(GETDATE()),CAST(GETDATE() AS DATE)))
              AND COUNT_DATE < DATEADD(MONTH,-1,DATEADD(DAY,1-DAY(GETDATE()),CAST(GETDATE() AS DATE)))
    """, hosp_cd)
    r = cur.fetchone()
    info["prev2_month_count"] = int(r[0] or 0) if r else 0
    
    # 성장률 (전전월 대비 전월)
    if info["prev2_month_count"] > 0:
        info["growth"] = round((info["prev_month_count"] - info["prev2_month_count"]) / info["prev2_month_count"] * 100, 1)
    else:
        info["growth"] = 0
    
    # 오늘 사용량
    cur.execute("""
        SELECT SUM(COUNT_01+COUNT_02+COUNT_03+COUNT_04+COUNT_05+COUNT_06+
                    COUNT_07+COUNT_08+COUNT_09+COUNT_10+COUNT_11+COUNT_12+COUNT_13) total
        FROM KIOSK_HOSP_COUNT
        WHERE HOSP_CD=? AND COUNT_DATE=CAST(GETDATE() AS DATE)
    """, hosp_cd)
    r = cur.fetchone()
    info["today_count"] = int(r[0] or 0) if r else 0
    
    conn.close()
    return jsonify(info)

@app.route('/api/hospital-view/daily/<hosp_cd>')
@login_required
def api_hosp_daily(hosp_cd):
    import pyodbc
    from config import get_connection_string
    conn = pyodbc.connect(get_connection_string())
    cur = conn.cursor()
    
    cur.execute("""
        SELECT CONVERT(VARCHAR,COUNT_DATE,23) dt,
               SUM(COUNT_01+COUNT_02+COUNT_03+COUNT_04+COUNT_05+COUNT_06+
                   COUNT_07+COUNT_08+COUNT_09+COUNT_10+COUNT_11+COUNT_12+COUNT_13) total
        FROM KIOSK_HOSP_COUNT
        WHERE HOSP_CD=? AND COUNT_DATE >= DATEADD(DAY,-30,GETDATE())
        GROUP BY COUNT_DATE
        ORDER BY COUNT_DATE
    """, hosp_cd)
    data = [{"date":str(r[0]),"count":int(r[1] or 0)} for r in cur.fetchall()]
    conn.close()
    return jsonify({"daily": data})

@app.route('/api/hospital-view/hourly/<hosp_cd>')
@login_required
def api_hosp_hourly(hosp_cd):
    import pyodbc
    from config import get_connection_string
    conn = pyodbc.connect(get_connection_string())
    cur = conn.cursor()
    
    # 최근 30일 시간대별 평균
    cur.execute("""
        SELECT AVG(COUNT_01),AVG(COUNT_02),AVG(COUNT_03),AVG(COUNT_04),AVG(COUNT_05),
               AVG(COUNT_06),AVG(COUNT_07),AVG(COUNT_08),AVG(COUNT_09),AVG(COUNT_10),
               AVG(COUNT_11),AVG(COUNT_12),AVG(COUNT_13)
        FROM KIOSK_HOSP_COUNT
        WHERE HOSP_CD=? AND COUNT_DATE >= DATEADD(DAY,-30,GETDATE())
    """, hosp_cd)
    r = cur.fetchone()
    labels = ['08시','09시','10시','11시','12시','13시','14시','15시','16시','17시','18시','19시','20시']
    counts = [int(r[i] or 0) for i in range(13)] if r else [0]*13
    conn.close()
    return jsonify({"labels": labels, "counts": counts})

@app.route('/api/hospital-view/compare/<hosp_cd>')
@login_required
def api_hosp_compare(hosp_cd):
    import pyodbc
    from config import get_connection_string
    conn = pyodbc.connect(get_connection_string())
    cur = conn.cursor()
    
    # 이 병원의 키오스크 대수
    cur.execute("SELECT KIOSK_CNT FROM KIOSK_HOSP_INFO WHERE HOSP_CD=?", hosp_cd)
    r = cur.fetchone()
    my_kiosk = int(r[0] or 1) if r else 1
    
    # 동급 병원 (같은 키오스크 대수 +-1)
    cur.execute("""
        SELECT h.HOSP_CD, h.HOSP_NM, h.KIOSK_CNT,
               ISNULL((SELECT SUM(c.COUNT_01+c.COUNT_02+c.COUNT_03+c.COUNT_04+c.COUNT_05+c.COUNT_06+
                                   c.COUNT_07+c.COUNT_08+c.COUNT_09+c.COUNT_10+c.COUNT_11+c.COUNT_12+c.COUNT_13)
                       FROM KIOSK_HOSP_COUNT c
                       WHERE c.HOSP_CD=h.HOSP_CD AND c.COUNT_DATE >= DATEADD(DAY,-30,GETDATE())),0) month_total
        FROM KIOSK_HOSP_INFO h
        WHERE h.USER_YN='Y' AND h.KIOSK_CNT IS NOT NULL
              AND CAST(h.KIOSK_CNT AS INT) BETWEEN ? AND ?
        ORDER BY month_total DESC
    """, max(1,my_kiosk-1), my_kiosk+1)
    
    peers = []
    my_rank = 0
    for i, r in enumerate(cur.fetchall()):
        is_me = str(r[0]) == hosp_cd
        peers.append({
            "hosp_cd": str(r[0]),
            "hosp_name": str(r[1] or ''),
            "kiosks": int(r[2] or 0),
            "month_total": int(r[3] or 0),
            "is_me": is_me
        })
        if is_me:
            my_rank = i + 1
    
    # 동급 평균
    avg_total = sum(p["month_total"] for p in peers) / len(peers) if peers else 0
    
    # 전체 상위 활용 병원 (성공 사례) - 병원명 일부 마스킹
    cur.execute("""
        SELECT TOP 5 h.HOSP_CD, h.HOSP_NM, h.KIOSK_CNT, h.EMR_COMPANY,
               ISNULL((SELECT SUM(c.COUNT_01+c.COUNT_02+c.COUNT_03+c.COUNT_04+c.COUNT_05+c.COUNT_06+
                                   c.COUNT_07+c.COUNT_08+c.COUNT_09+c.COUNT_10+c.COUNT_11+c.COUNT_12+c.COUNT_13)
                       FROM KIOSK_HOSP_COUNT c
                       WHERE c.HOSP_CD=h.HOSP_CD AND c.COUNT_DATE >= DATEADD(DAY,-30,GETDATE())),0) month_total
        FROM KIOSK_HOSP_INFO h
        WHERE h.USER_YN='Y' AND h.EMR_COMPANY NOT IN ('MCC','NSS')
        ORDER BY month_total DESC
    """)
    
    top_cases = []
    for r in cur.fetchall():
        tc_cd = str(r[0] or '')
        name = str(r[1] or '')
        is_me = tc_cd == hosp_cd
        masked = name if is_me else (name[0] + 'O' * (len(name)-1) if len(name) > 1 else name)
        top_cases.append({
            "hosp_cd": tc_cd,
            "hosp_name": masked,
            "kiosks": int(r[2] or 0),
            "isv": str(r[3] or ''),
            "month_total": int(r[4] or 0),
            "is_me": is_me
        })
    
    conn.close()
    return jsonify({
        "my_rank": my_rank,
        "peer_count": len(peers),
        "peer_avg": round(avg_total),
        "peers": peers[:10],
        "top_cases": top_cases
    })


@app.route('/api/hospital-list')
@login_required
def api_hospital_list():
    import pyodbc
    from config import get_connection_string
    conn = pyodbc.connect(get_connection_string())
    cur = conn.cursor()
    cur.execute("SELECT HOSP_CD, HOSP_NM FROM KIOSK_HOSP_INFO WHERE USER_YN='Y' AND EMR_COMPANY NOT IN ('MCC','NSS') ORDER BY HOSP_NM")
    data = [{"hosp_cd":str(r[0]),"hosp_name":str(r[1] or '')} for r in cur.fetchall()]
    conn.close()
    return jsonify({"hospitals": data})
