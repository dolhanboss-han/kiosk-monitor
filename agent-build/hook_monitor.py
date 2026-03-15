import sys, time, os, configparser, ctypes, ctypes.wintypes
from db_manager import insert_event, insert_session, insert_step, update_step_end

# 수납 플로우 단계 순서 (KIOSK_Main 제외, 업무 단계만)
FLOW_STEPS = [
    'KIOSK_수납방법선택',
    'KIOSK_할부개월선택',
    'KIOSK_수납(KeyPad)',
    'KIOSK_수납확인 및 결제',
    'KIOSK_영수증 및 처방전 출력',
]

FLOW_MAIN = 'KIOSK_Main'
FLOW_FINAL = 'KIOSK_영수증 및 처방전 출력'


class HookMonitor:
    def __init__(self, config):
        raw = config.get('MONITOR_SETTING', 'target_process', fallback='')
        self.targets = [x.strip().lower() for x in raw.split(',') if x.strip()]
        self.exclude_procs = [x.strip().lower() for x in config.get('MONITOR_SETTING', 'exclude_process', fallback='').split(',') if x.strip()]
        self.exclude_titles = [x.strip().lower() for x in config.get('MONITOR_SETTING', 'exclude_title', fallback='').split(',') if x.strip()]
        self.kiosk_id = config.get('SERVER', 'kiosk_id', fallback='UNKNOWN')
        self.last_title = None
        self.last_proc = None
        self.last_start = None

        # 세션 상태
        self._session_id = None
        self._session_start = None     # time.time()
        self._session_start_dt = None  # datetime 문자열
        self._session_steps = []       # 완료된 step 목록
        self._current_step = None      # 현재 진행 중인 step 이름
        self._current_step_start = None
        self._step_order = 0
        self._final_ended = False      # 최종 단계(영수증출력) END 감지 여부

        print(f"[Hook] targets: {self.targets if self.targets else 'ALL'}")
        print(f"[Hook] kiosk_id: {self.kiosk_id}")

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
        WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.wintypes.HWND, ctypes.wintypes.LPARAM)
        def callback(child_hwnd, lparam):
            buf = ctypes.create_unicode_buffer(512)
            ctypes.windll.user32.GetWindowTextW(child_hwnd, buf, 512)
            if buf.value.strip():
                titles.append(buf.value.strip())
            return True
        ctypes.windll.user32.EnumChildWindows(hwnd, WNDENUMPROC(callback), 0)
        return titles

    # ─── 세션 관리 ───

    def _now_dt(self):
        return time.strftime('%Y-%m-%d %H:%M:%S')

    def _today(self):
        return time.strftime('%Y-%m-%d')

    def _new_session_id(self):
        return f"{self.kiosk_id}_{time.strftime('%Y%m%d%H%M%S')}_{int(time.time()*1000)%10000}"

    def _close_current_step(self):
        """현재 진행 중인 step을 END 처리"""
        if self._current_step and self._session_id:
            now = time.time()
            now_dt = self._now_dt()
            elapsed = round(now - self._current_step_start, 1) if self._current_step_start else None
            update_step_end(self._session_id, self._current_step, now_dt, elapsed)
            self._current_step = None
            self._current_step_start = None

    def _close_session(self, result, cancel_step=None):
        """세션 종료: complete 또는 cancel"""
        if not self._session_id:
            return

        now = time.time()
        now_dt = self._now_dt()
        elapsed = round(now - self._session_start, 1) if self._session_start else None

        # 현재 step이 있으면 먼저 닫기
        self._close_current_step()

        insert_session(
            kiosk_id=self.kiosk_id,
            work_date=self._today(),
            session_id=self._session_id,
            menu_code='receipt',
            start_dt=self._session_start_dt,
            end_dt=now_dt,
            elapsed_sec=elapsed,
            result=result,
            cancel_step=cancel_step,
        )
        print(f"[Session] {result}: {self._session_id} ({elapsed}s) steps={len(self._session_steps)}"
              + (f" cancel_at={cancel_step}" if cancel_step else ""))

        self._session_id = None
        self._session_start = None
        self._session_start_dt = None
        self._session_steps = []
        self._step_order = 0
        self._final_ended = False

    def _start_session(self):
        """새 세션 시작"""
        self._session_id = self._new_session_id()
        self._session_start = time.time()
        self._session_start_dt = self._now_dt()
        self._session_steps = []
        self._current_step = None
        self._current_step_start = None
        self._step_order = 0
        self._final_ended = False

        # 세션 레코드 생성 (result=NULL, 진행 중)
        insert_session(
            kiosk_id=self.kiosk_id,
            work_date=self._today(),
            session_id=self._session_id,
            menu_code='receipt',
            start_dt=self._session_start_dt,
        )
        print(f"[Session] START: {self._session_id}")

    def _start_step(self, step_name):
        """새 step 시작"""
        self._close_current_step()

        self._step_order += 1
        self._current_step = step_name
        self._current_step_start = time.time()
        now_dt = self._now_dt()

        insert_step(
            kiosk_id=self.kiosk_id,
            session_id=self._session_id,
            step_order=self._step_order,
            step_name=step_name,
            start_dt=now_dt,
        )
        self._session_steps.append(step_name)

    def _handle_session_event(self, title, status):
        """세션 이벤트 처리 (KIOSK_ 접두사 타이틀만 호출됨)"""

        is_main = (title == FLOW_MAIN)
        is_flow_step = (title in FLOW_STEPS)
        is_final = (title == FLOW_FINAL)

        if is_main and status == 'START':
            if self._session_id is None:
                # 첫 진입: 새 세션 시작
                self._start_session()
            elif self._final_ended:
                # 영수증 출력 END 이후 KIOSK_Main → complete
                self._close_session('complete')
                self._start_session()
            else:
                # 중간에 KIOSK_Main으로 돌아옴 → cancel
                last_step = self._session_steps[-1] if self._session_steps else None
                self._close_session('cancel', cancel_step=last_step)
                self._start_session()

        elif is_flow_step and status == 'START' and self._session_id:
            self._start_step(title)

        elif is_final and status == 'END' and self._session_id:
            self._final_ended = True
            self._close_current_step()

    # ─── 메인 폴링 ───

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

            # 기존 event_log INSERT (하위 호환)
            if self.last_title and self.last_proc:
                elapsed = round(now - self.last_start, 1) if self.last_start else None
                insert_event(self.last_proc, self.last_title, '', 'END', elapsed)

                # 이전 타이틀의 END 세션 이벤트
                if self.last_title.startswith('KIOSK_'):
                    self._handle_session_event(self.last_title, 'END')

            insert_event(proc_name, title, '', 'START', None)

            # 새 타이틀의 START 세션 이벤트
            if title.startswith('KIOSK_'):
                self._handle_session_event(title, 'START')

            self.last_title = title
            self.last_proc = proc_name
            self.last_start = now
