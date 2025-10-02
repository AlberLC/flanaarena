import ctypes
from ctypes.wintypes import DWORD, HWND
from typing import Any

import psutil

from windows_api import constants as win_constants


def _get_hwnd(hwnd: int | HWND | psutil.Process) -> HWND | None:
    match hwnd:
        case int():
            return HWND(hwnd)
        case HWND():
            return hwnd
        case _:
            return get_hwnd_of_pid(hwnd.info['pid'])


def force_foreground(hwnd: int | HWND | psutil.Process) -> None:
    if hwnd := _get_hwnd(hwnd):
        flags = win_constants.SWP_NOMOVE | win_constants.SWP_NOSIZE | win_constants.SWP_SHOWWINDOW
        win_constants.SetWindowPos(hwnd, win_constants.HWND_TOPMOST, 0, 0, 0, 0, flags)
        win_constants.SetWindowPos(hwnd, win_constants.HWND_NOTOPMOST, 0, 0, 0, 0, flags)


def get_focused_hwnd() -> HWND | None:
    if not (foreground_hwnd := win_constants.GetForegroundWindow()):
        return

    current_thread_id = win_constants.GetCurrentThreadId()
    target_thread_id = win_constants.GetWindowThreadProcessId(foreground_hwnd, None)

    if win_constants.AttachThreadInput(target_thread_id, current_thread_id, True):
        focused_hwnd = win_constants.GetFocus()
        win_constants.AttachThreadInput(target_thread_id, current_thread_id, False)

        return focused_hwnd


def get_hwnd_of_pid(pid: int) -> HWND | None:
    hwnd = None

    @win_constants.EnumWindowsProc
    def enum_proc(hwnd_: HWND, _: Any) -> bool:
        nonlocal hwnd

        if win_constants.IsWindowVisible(hwnd_):
            pid_ = DWORD()
            win_constants.GetWindowThreadProcessId(hwnd_, ctypes.byref(pid_))

            if pid_.value == pid:
                hwnd = hwnd_
                return False

        return True

    win_constants.EnumWindows(enum_proc, None)
    return hwnd


def get_screen_size() -> tuple[int, int]:
    return win_constants.GetSystemMetrics(0), win_constants.GetSystemMetrics(1)


def is_focused(hwnd: int | HWND | psutil.Process) -> bool:
    if hwnd := _get_hwnd(hwnd):
        return hwnd == get_focused_hwnd()

    return False


def is_foreground(hwnd: int | HWND | psutil.Process) -> bool:
    if hwnd := _get_hwnd(hwnd):
        return hwnd == win_constants.GetForegroundWindow()

    return False


def is_minimized(hwnd: int | HWND | psutil.Process) -> bool:
    if hwnd := _get_hwnd(hwnd):
        return bool(win_constants.IsIconic(hwnd))

    return False


def minimize(hwnd: int | HWND | psutil.Process) -> None:
    if hwnd := _get_hwnd(hwnd):
        win_constants.ShowWindow(hwnd, win_constants.SW_MINIMIZE)


def show_with_focus(hwnd: int | HWND | psutil.Process) -> None:
    if not (hwnd := _get_hwnd(hwnd)):
        return

    if win_constants.IsIconic(hwnd):
        win_constants.ShowWindow(hwnd, win_constants.SW_RESTORE)

    win_constants.SetForegroundWindow(hwnd)
    win_constants.SetFocus(hwnd)


def show_without_focus(hwnd: int | HWND | psutil.Process) -> None:
    if hwnd := _get_hwnd(hwnd):
        win_constants.ShowWindow(hwnd, win_constants.SW_SHOWNOACTIVATE)


def set_capturable(hwnd: int | HWND | psutil.Process, allow_capture: bool) -> None:
    if hwnd := _get_hwnd(hwnd):
        win_constants.SetWindowDisplayAffinity(
            hwnd,
            win_constants.WDA_NONE if allow_capture else win_constants.WDA_EXCLUDEFROMCAPTURE
        )


def set_parent(parent_hwnd: int | HWND, hwnd: int | HWND | psutil.Process) -> None:
    if hwnd := _get_hwnd(hwnd):
        win_constants.SetParent(_get_hwnd(parent_hwnd), hwnd)
