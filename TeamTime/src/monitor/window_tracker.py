import platform
import psutil

class WindowTracker:
    def __init__(self):
        self.os_type = platform.system()

    def get_active_window(self):
        try:
            if self.os_type == "Windows":
                return self._get_windows_active_window()
            elif self.os_type == "Darwin":
                return self._get_mac_active_window()
            elif self.os_type == "Linux":
                return self._get_linux_active_window()
            else:
                return None, None
        except Exception as e:
            print(f"Error getting active window: {e}")
            return None, None

    def _get_windows_active_window(self):
        try:
            import pygetwindow as gw
            window = gw.getActiveWindow()
            if window:
                return window.title, self._get_process_name_from_title(window.title)
            return None, None
        except Exception as e:
            print(f"Windows tracking error: {e}")
            return None, None

    def _get_mac_active_window(self):
        try:
            from AppKit import NSWorkspace
            active_app = NSWorkspace.sharedWorkspace().activeApplication()
            app_name = active_app['NSApplicationName']
            window_title = active_app.get('NSApplicationPath', app_name)
            return window_title, app_name
        except ImportError:
            print("AppKit not available. Install with: pip install pyobjc-framework-Cocoa")
            return None, None
        except Exception as e:
            print(f"Mac tracking error: {e}")
            return None, None

    def _get_linux_active_window(self):
        try:
            import subprocess
            window_id = subprocess.check_output(['xdotool', 'getactivewindow']).decode().strip()
            window_title = subprocess.check_output(['xdotool', 'getwindowname', window_id]).decode().strip()
            pid = subprocess.check_output(['xdotool', 'getwindowpid', window_id]).decode().strip()
            process = psutil.Process(int(pid))
            app_name = process.name()
            return window_title, app_name
        except Exception as e:
            print(f"Linux tracking error: {e}")
            return None, None

    def _get_process_name_from_title(self, title):
        for proc in psutil.process_iter(['name', 'pid']):
            try:
                if proc.info['name']:
                    return proc.info['name'].lower().replace('.exe', '')
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return "unknown"
