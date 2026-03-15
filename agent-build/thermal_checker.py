"""
thermal_checker.py - 감열 프린터 상태 체크 (독립 실행)
HwaUSB.DLL을 ctypes로 로드하여 프린터 상태를 JSON으로 stdout에 출력한다.
PyInstaller --onefile로 EXE 빌드하여 배포한다.
"""
import sys, os, json, struct, ctypes, configparser


def _get_base_dir():
    """PyInstaller frozen이면 exe 디렉토리, 아니면 스크립트 디렉토리"""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


def _get_bit_label():
    return '64bit' if struct.calcsize('P') * 8 == 64 else '32bit'


def _add_dll_search_path(dll_dir):
    """DLL 디렉토리를 검색 경로에 추가"""
    if hasattr(os, 'add_dll_directory'):
        try:
            os.add_dll_directory(dll_dir)
        except OSError:
            pass
    os.environ['PATH'] = dll_dir + os.pathsep + os.environ.get('PATH', '')


def _try_load_dll(dll_path):
    """CDLL → WinDLL → windll.LoadLibrary 순서로 DLL 로드 시도"""
    errors = []
    for loader_name, loader_fn in [
        ('CDLL',   lambda p: ctypes.CDLL(p, winmode=0)),
        ('WinDLL', lambda p: ctypes.WinDLL(p, winmode=0)),
        ('windll', lambda p: ctypes.windll.LoadLibrary(p)),
    ]:
        try:
            dll = loader_fn(dll_path)
            return dll, errors
        except OSError as e:
            errors.append(f"{loader_name}: {e}")
    return None, errors


def main():
    try:
        base_dir = _get_base_dir()
        config_path = os.path.join(base_dir, 'config.ini')

        if not os.path.exists(config_path):
            print(json.dumps({"status": "error", "message": "config_not_found"}))
            return

        config = configparser.ConfigParser()
        config.read(config_path, encoding='utf-8')

        cfg_dll_path = config.get('PRINTER_THERMAL', 'dll_path', fallback='HwaUSB.DLL')
        model = config.get('PRINTER_THERMAL', 'model', fallback='HMK-825')

        # 상대경로이면 base_dir 기준 절대경로 변환
        if not os.path.isabs(cfg_dll_path):
            cfg_dll_path = os.path.join(base_dir, cfg_dll_path)

        # DLL 탐색 순서 (32/64비트 모두 처리)
        candidate_paths = [
            cfg_dll_path,                                        # 1) config.ini의 dll_path
            os.path.join(base_dir, 'HwaUSB.DLL'),               # 2) 같은 폴더
            r'C:\Windows\SysWOW64\HwaUSB.DLL',                  # 3) 32비트
            r'C:\Windows\System32\HwaUSB.DLL',                  # 4) 64비트
        ]
        # 중복 제거 (순서 유지)
        seen = set()
        unique_paths = []
        for p in candidate_paths:
            norm = os.path.normcase(os.path.abspath(p))
            if norm not in seen:
                seen.add(norm)
                unique_paths.append(p)

        dll = None
        all_errors = []

        for dll_path in unique_paths:
            if not os.path.exists(dll_path):
                all_errors.append(f"[{dll_path}] not found")
                continue

            _add_dll_search_path(os.path.dirname(os.path.abspath(dll_path)))
            dll, errors = _try_load_dll(dll_path)
            if dll is not None:
                break
            all_errors.extend(f"[{dll_path}] {e}" for e in errors)

        if dll is None:
            print(json.dumps({
                "status": "dll_load_failed",
                "message": '; '.join(all_errors),
                "bit": _get_bit_label()
            }))
            return

        # 프린터 연결
        open_result = dll.UsbOpen(model.encode('ascii'))
        if open_result != 0:
            print(json.dumps({"status": "error", "message": "disconnected"}))
            return

        # 상태 읽기
        status = dll.NewRealRead()
        if status < 0:
            print(json.dumps({"status": "error", "message": "read_error"}))
            return

        cover = 'open' if (status & 0x04) else 'closed'
        paper = 'empty' if (status & 0x20) else 'normal'
        error = 'yes' if (status & 0x40) else 'no'

        if paper == 'empty' or error == 'yes':
            overall = 'error'
        else:
            overall = 'ok'

        print(json.dumps({
            "status": overall,
            "paper": paper,
            "cover": cover,
            "error": error
        }))

    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}))


if __name__ == '__main__':
    main()
