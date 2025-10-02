import ctypes
from ctypes.wintypes import BOOL, DWORD, HWND, INT, LPARAM, UINT

HWND_NOTOPMOST = HWND(-2)
HWND_TOP = HWND(0)
HWND_TOPMOST = HWND(-1)
SW_MINIMIZE = 6
SW_RESTORE = 9
SW_SHOWNOACTIVATE = 4
SWP_NOMOVE = 2
SWP_NOSIZE = 1
SWP_SHOWWINDOW = 64
WDA_EXCLUDEFROMCAPTURE = 17
WDA_NONE = 0

user32 = ctypes.WinDLL('user32', use_last_error=True)

AttachThreadInput = user32.AttachThreadInput
AttachThreadInput.argtypes = [DWORD, DWORD, BOOL]
AttachThreadInput.restype = BOOL
EnumWindows = user32.EnumWindows
EnumWindowsProc = ctypes.WINFUNCTYPE(BOOL, HWND, LPARAM)
GetCurrentThreadId = ctypes.windll.kernel32.GetCurrentThreadId
GetCurrentThreadId.restype = DWORD
GetFocus = user32.GetFocus
GetFocus.restype = HWND
GetForegroundWindow = user32.GetForegroundWindow
GetForegroundWindow.restype = HWND
GetSystemMetrics = user32.GetSystemMetrics
GetSystemMetrics.argtypes = [INT]
GetSystemMetrics.restype = INT
GetWindowThreadProcessId = user32.GetWindowThreadProcessId
IsIconic = user32.IsIconic
IsWindowVisible = user32.IsWindowVisible
SetFocus = user32.SetFocus
SetForegroundWindow = user32.SetForegroundWindow
SetParent = user32.SetParent
SetParent.argtypes = [HWND, HWND]
SetParent.restype = HWND
SetWindowDisplayAffinity = user32.SetWindowDisplayAffinity
SetWindowDisplayAffinity.argtypes = [HWND, DWORD]
SetWindowDisplayAffinity.restype = BOOL
SetWindowPos = user32.SetWindowPos
SetWindowPos.argtypes = [HWND, HWND, INT, INT, INT, INT, UINT]
SetWindowPos.restype = BOOL
ShowWindow = user32.ShowWindow
