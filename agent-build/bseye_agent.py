import os, sys, threading, configparser, time

if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(0, BASE_DIR)
os.chdir(BASE_DIR)

VERSION = '3.0.2'

def load_config():
    config = configparser.ConfigParser()
    config.read(os.path.join(BASE_DIR, 'config.ini'), encoding='utf-8')
    return config

def main():
    print(f'[Agent] BS-EYE Agent v{VERSION} starting...')
    config = load_config()
    port = config.getint('MONITOR_SETTING', 'web_port', fallback=8080)

    # 1. DB 초기화
    from db_manager import init_db, cleanup_old_data
    init_db()
    cleanup_old_data(config.getint('MONITOR_SETTING', 'retention_days', fallback=30))

    # 2. 윈도우 타이틀 감시 스레드
    from hook_monitor import HookMonitor
    hook = HookMonitor(config)
    t1 = threading.Thread(target=hook.start, daemon=True)
    t1.start()

    # 3. 하드웨어 모니터링 스레드
    from hw_monitor import HWMonitor
    hw = HWMonitor(config)
    t2 = threading.Thread(target=hw.run, daemon=True)
    t2.start()

    # 4. 데이터 전송 스레드
    if config.get('SERVER', 'server_url', fallback=''):
        from data_sender import start_sender_thread
        start_sender_thread(config, version=VERSION)

    # 5. 로컬 웹서버
    print(f'[Web] http://localhost:{port}')
    import uvicorn
    from web_server import app
    uvicorn.run(app, host='0.0.0.0', port=port, log_level='warning')

# ─── Windows 서비스 ───
try:
    import win32serviceutil, win32service, win32event, servicemanager

    class BseyeService(win32serviceutil.ServiceFramework):
        _svc_name_ = 'BseyeAgent'
        _svc_display_name_ = 'BS-EYE Kiosk Agent'
        _svc_description_ = 'BS-EYE Kiosk Monitoring Agent v3.0.2'

        def __init__(self, args):
            win32serviceutil.ServiceFramework.__init__(self, args)
            self.stop_event = win32event.CreateEvent(None, 0, 0, None)
            self.running = True

        def SvcStop(self):
            self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
            self.running = False
            win32event.SetEvent(self.stop_event)

        def SvcDoRun(self):
            servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                                 servicemanager.PYS_SERVICE_STARTED, (self._svc_name_, ''))
            self.main_func()

        def main_func(self):
            try:
                main()
            except Exception as e:
                servicemanager.LogErrorMsg(f'BseyeAgent error: {e}')

    if __name__ == '__main__':
        if len(sys.argv) == 1:
            servicemanager.Initialize()
            servicemanager.PrepareToHostSingle(BseyeService)
            servicemanager.StartServiceCtrlDispatcher()
        elif sys.argv[1] == 'debug':
            main()
        else:
            win32serviceutil.HandleCommandLine(BseyeService)

except ImportError:
    if __name__ == '__main__':
        main()
