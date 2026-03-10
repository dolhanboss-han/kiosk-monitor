import sys, time, os, configparser, ctypes, ctypes.wintypes
from db_manager import insert_event

class HookMonitor:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read(os.path.join(os.path.dirname(sys.executable) if getattr(sys,"frozen",False) else os.path.dirname(os.path.abspath(__file__)),'config.ini'), encoding='utf-8')
        raw = config.get('MONITOR','target_process',fallback='')
        self.targets = [x.strip().lower() for x in raw.split(',') if x.strip()]
        self.exclude_procs = [x.strip().lower() for x in config.get('MONITOR','exclude_process',fallback='').split(',') if x.strip()]
        self.exclude_titles = [x.strip().lower() for x in config.get('MONITOR','exclude_title',fallback='').split(',') if x.strip()]
        self.last_title = None
        self.last_proc = None
        self.last_start = None
        print(f"[Hook] targets: {self.targets if self.targets else 'ALL'}")

    def start(self):
        while True:
            try:
                self._poll()
            except:
                pass
            time.sleep(0.5)

    def _is_target(self, proc_name):
        if not self.targets:
            return True
        pn = proc_name.lower()
        return any(t in pn for t in self.targets)

    def _is_excluded(self, proc_name, title):
        pn = proc_name.lower()
        tl = (title or '').lower()
        return any(ep in pn for ep in self.exclude_procs) or any(et in tl for et in self.exclude_titles)

    def _get_child_titles(self, hwnd):
        titles = []
        EnumChildWindows = ctypes.windll.user32.EnumChildWindows
        WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.wintypes.HWND, ctypes.wintypes.LPARAM)
        def callback(child_hwnd, lparam):
            buf = ctypes.create_unicode_buffer(512)
            ctypes.windll.user32.GetWindowTextW(child_hwnd, buf, 512)
            if buf.value.strip():
                titles.append(buf.value.strip())
            return True
        EnumChildWindows(hwnd, WNDENUMPROC(callback), 0)
        return titles

    def _poll(self):
        import psutil
        hwnd = ctypes.windll.user32.GetForegroundWindow()
        pid = ctypes.wintypes.DWORD()
        ctypes.windll.user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
        try:
            proc = psutil.Process(pid.value)
            proc_name = proc.name()
        except:
            return

        if not self._is_target(proc_name):
            if self.last_title and self.last_proc:
                elapsed = round(time.time() - self.last_start, 1) if self.last_start else None
                insert_event(self.last_proc, self.last_title, '', 'END', elapsed)
                self.last_title = self.last_proc = self.last_start = None
            return

        buf = ctypes.create_unicode_buffer(512)
        ctypes.windll.user32.GetWindowTextW(hwnd, buf, 512)
        title = buf.value

        if not title:
            child_titles = self._get_child_titles(hwnd)
            if child_titles:
                title = child_titles[0]
            else:
                title = proc_name

        if self._is_excluded(proc_name, title):
            return

        if title != self.last_title:
            now = time.time()
            if self.last_title and self.last_proc:
                elapsed = round(now - self.last_start, 1) if self.last_start else None
                insert_event(self.last_proc, self.last_title, '', 'END', elapsed)
            insert_event(proc_name, title, '', 'START', None)
            self.last_title = title
            self.last_proc = proc_name
            self.last_start = now
