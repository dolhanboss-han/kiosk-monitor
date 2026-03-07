import os, sys, threading, configparser, uvicorn
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    config = configparser.ConfigParser()
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini')
    config.read(config_path, encoding='utf-8')
    port = config.getint('MONITOR', 'web_port', fallback=8080)

    from db_manager import init_db, cleanup_old_data
    init_db()
    cleanup_old_data()

    from hook_monitor import HookMonitor
    monitor = HookMonitor()
    t = threading.Thread(target=monitor.start, daemon=True)
    t.start()
    targets = config.get('MONITOR','target_process',fallback='')
    print(f"[Monitor] DB: {os.path.join(os.path.dirname(os.path.abspath(__file__)),'monitor.db')}")
    print(f"[Monitor] target: {targets}")

    if config.has_section('SERVER') and config.get('SERVER','server_url',fallback=''):
        from data_sender import start_sender_thread
        start_sender_thread()

    from web_server import app
    print(f"[Web] http://localhost:{port}")
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="warning")

if __name__ == "__main__":
    main()
