import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="Kiosk Monitor Agent")

@app.get("/", response_class=HTMLResponse)
async def index():
    return open(os.path.join(os.path.dirname(__file__),"templates","dashboard.html")).read()

@app.get("/api/status")
async def api_status():
    from db_manager import get_today_summary, get_today_events
    summary = get_today_summary()
    events = get_today_events()[:50]
    return {"summary": summary, "events": events}

@app.get("/api/check/{category}")
async def api_check(category: str):
    try:
        from device_checker import run_category
        return {"results": run_category(category)}
    except Exception as e:
        return {"results": [{"item": category, "status": "error", "value": str(e), "detail": {}}]}

@app.get("/api/check-all")
async def api_check_all():
    try:
        from device_checker import run_all
        return {"results": run_all()}
    except Exception as e:
        return {"results": [{"item": "all", "status": "error", "value": str(e), "detail": {}}]}
