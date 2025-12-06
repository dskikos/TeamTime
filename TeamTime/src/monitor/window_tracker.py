import platform
import psutil
import os
import subprocess

class WindowTracker:
    def __init__(self):
        self.os_type = platform.system()
        # Detect if we're running in WSL
        self.is_wsl = self._detect_wsl()
        if self.is_wsl:
            print("WSL environment detected - will monitor Windows applications")

    def _detect_wsl(self):
        """Detect if we're running in WSL"""
        try:
            # Check for WSL-specific indicators
            if os.path.exists('/proc/version'):
                with open('/proc/version', 'r') as f:
                    version_info = f.read().lower()
                    if 'microsoft' in version_info or 'wsl' in version_info:
                        return True
            # Also check if we can execute Windows commands
            if os.path.exists('/mnt/c/Windows'):
                return True
        except:
            pass
        return False

    def get_active_window(self):
        try:
            # If we're in WSL, use Windows tracking
            if self.is_wsl:
                return self._get_wsl_windows_active_window()
            elif self.os_type == "Windows":
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
            import win32process
            import win32gui

            hwnd = win32gui.GetForegroundWindow()
            window_title = win32gui.GetWindowText(hwnd)
            _, pid = win32process.GetWindowThreadProcessId(hwnd)

            try:
                process = psutil.Process(pid)
                app_name = process.name().lower().replace('.exe', '')

                # If TeamTime is the active window, get the window behind it
                if 'python' in app_name and 'teamtime' in window_title.lower():
                    # Get all windows
                    windows = gw.getAllWindows()
                    # Filter out TeamTime windows and invisible windows
                    for window in windows:
                        if window.title and 'teamtime' not in window.title.lower() and window.visible:
                            try:
                                # Get process info for this window
                                hwnd_behind = win32gui.FindWindow(None, window.title)
                                if hwnd_behind:
                                    _, pid_behind = win32process.GetWindowThreadProcessId(hwnd_behind)
                                    process_behind = psutil.Process(pid_behind)
                                    app_name_behind = process_behind.name().lower().replace('.exe', '')
                                    return window.title, app_name_behind
                            except:
                                continue

                return window_title, app_name
            except:
                return window_title, "unknown"
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

    def _get_wsl_windows_active_window(self):
        """Get active window from Windows while running in WSL"""
        try:
            # PowerShell script to get active window info
            ps_script = """
            Add-Type @"
                using System;
                using System.Runtime.InteropServices;
                using System.Text;
                public class WindowHelper {
                    [DllImport("user32.dll")]
                    public static extern IntPtr GetForegroundWindow();
                    [DllImport("user32.dll")]
                    public static extern int GetWindowText(IntPtr hWnd, StringBuilder text, int count);
                    [DllImport("user32.dll")]
                    public static extern uint GetWindowThreadProcessId(IntPtr hWnd, out uint processId);
                }
"@
            $hwnd = [WindowHelper]::GetForegroundWindow()
            $title = New-Object System.Text.StringBuilder 256
            [void][WindowHelper]::GetWindowText($hwnd, $title, 256)
            $processId = 0
            [void][WindowHelper]::GetWindowThreadProcessId($hwnd, [ref]$processId)
            $process = Get-Process -Id $processId -ErrorAction SilentlyContinue
            if ($process) {
                Write-Output "$($title.ToString())|$($process.ProcessName)"
            } else {
                Write-Output "$($title.ToString())|unknown"
            }
            """

            # Execute PowerShell through WSL interop
            result = subprocess.check_output(
                ['powershell.exe', '-NoProfile', '-NonInteractive', '-Command', ps_script],
                stderr=subprocess.DEVNULL,
                timeout=5
            ).decode('utf-8', errors='ignore').strip()

            if '|' in result:
                window_title, app_name = result.split('|', 1)
                window_title = window_title.strip()
                app_name = app_name.strip().lower().replace('.exe', '')

                # Filter out TeamTime itself (only if it's actually the TeamTime Python app)
                if window_title and app_name:
                    # Only filter if it's python AND has TeamTime Dashboard in the title
                    if 'python' in app_name and 'teamtime dashboard' in window_title.lower():
                        return None, None
                    return window_title, app_name

            return None, None

        except subprocess.TimeoutExpired:
            print("PowerShell timeout - Windows may be slow to respond")
            return None, None
        except FileNotFoundError:
            print("PowerShell not found. Make sure Windows interop is enabled in WSL.")
            return None, None
        except Exception as e:
            print(f"WSL Windows tracking error: {e}")
            return None, None

    def _get_linux_active_window(self):
        try:
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
