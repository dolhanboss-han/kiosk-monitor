import os, sys, json
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse

if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = FastAPI(title="BS-EYE Kiosk Agent")

@app.get("/", response_class=HTMLResponse)
async def index():
    html_path = os.path.join(BASE_DIR, 'templates', 'bseye-agent-viewer.html')
    if os.path.exists(html_path):
        return open(html_path, encoding='utf-8', errors='replace').read()
    return '<h1>BS-EYE Agent Running</h1><p>bseye-agent-viewer.html not found</p>'

@app.get("/api/status")
async def api_status():
    from db_manager import get_today_summary, get_today_events, get_hw_status
    summary = get_today_summary()
    events = get_today_events(limit=50)
    hw = get_hw_status()
    hw_data = json.loads(hw['data_json']) if hw and hw.get('data_json') else {}
    return {
        'summary': summary,
        'events': events,
        'hw': hw_data,
        'hw_updated': hw.get('updated_at', '') if hw else ''
    }

@app.get("/api/check/{category}")
async def api_check(category: str):
    try:
        from device_checker import run_category
        return {'results': run_category(category)}
    except Exception as e:
        return {'results': [{'item': category, 'status': 'error', 'value': str(e)}]}

@app.get("/api/check-all")
async def api_check_all():
    try:
        from device_checker import run_all
        return {'results': run_all()}
    except Exception as e:
        return {'results': [{'item': 'all', 'status': 'error', 'value': str(e)}]}

@app.get("/api/printer-status")
async def api_printer_status():
    from hw_monitor import _read_status_file, STATUS_DIR
    a4 = _read_status_file(os.path.join(STATUS_DIR, 'printer_status.txt'))
    thermal = _read_status_file(os.path.join(STATUS_DIR, 'thermal_status.txt'))
    return {'a4': a4, 'thermal': thermal}

@app.get("/api/emr-status")
async def api_emr_status():
    from hw_monitor import _read_status_file, STATUS_DIR
    return _read_status_file(os.path.join(STATUS_DIR, 'emr_status.txt'))

@app.get("/api/print-result")
async def api_print_result():
    from hw_monitor import _read_status_file, STATUS_DIR
    return _read_status_file(os.path.join(STATUS_DIR, 'print_result.txt'))
