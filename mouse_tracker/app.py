"""tkinter 기반 마우스 좌표 트래커 GUI."""

import sys
import tkinter as tk
from tkinter import font as tkfont

from mouse_tracker.tracker import DragState

POLL_MS = 16  # 약 60fps


def _make_button_reader():
    """화면 어디서든 왼쪽 버튼 상태를 읽는 함수를 반환한다 (Windows 전용).

    Windows가 아니면 None을 반환하고, 그 경우 창 내부 이벤트로 대체한다.
    """
    if sys.platform != "win32":
        return None
    import ctypes

    user32 = ctypes.windll.user32
    VK_LBUTTON = 0x01
    VK_RBUTTON = 0x02
    SM_SWAPBUTTON = 23

    def is_left_pressed() -> bool:
        # 마우스 좌우 버튼이 바뀐 설정도 고려
        vk = VK_RBUTTON if user32.GetSystemMetrics(SM_SWAPBUTTON) else VK_LBUTTON
        return bool(user32.GetAsyncKeyState(vk) & 0x8000)

    return is_left_pressed


def _fmt(point) -> str:
    return "-" if point is None else f"({point[0]:>5}, {point[1]:>5})"


def _fmt_delta(point) -> str:
    return "-" if point is None else f"({point[0]:>+5}, {point[1]:>+5})"


class MouseTrackerApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.state = DragState()
        self.read_button = _make_button_reader()
        self._window_pressed = False  # 비 Windows 환경용

        root.title("Mouse Coordinate Tracker")
        root.geometry("420x260")
        root.resizable(False, False)
        root.attributes("-topmost", True)

        mono = tkfont.Font(family="Consolas", size=12)
        bold = tkfont.Font(family="Consolas", size=12, weight="bold")

        frame = tk.Frame(root, padx=16, pady=12)
        frame.pack(fill="both", expand=True)

        rows = [
            ("현재 좌표", "current"),
            ("드래그 시작 좌표", "start"),
            ("드래그 현재 좌표", "drag_current"),
            ("변화량 (dx, dy)", "delta"),
        ]
        self.vars = {}
        for i, (label, key) in enumerate(rows):
            tk.Label(frame, text=label, font=bold, anchor="w").grid(
                row=i, column=0, sticky="w", pady=4
            )
            var = tk.StringVar(value="-")
            tk.Label(frame, textvariable=var, font=mono, anchor="e", width=16).grid(
                row=i, column=1, sticky="e", pady=4
            )
            self.vars[key] = var

        self.status = tk.StringVar(value="대기 중")
        self.status_label = tk.Label(frame, textvariable=self.status, font=bold, fg="gray")
        self.status_label.grid(row=len(rows), column=0, columnspan=2, pady=(12, 0))

        scope = "화면 전체" if self.read_button else "이 창 안"
        tk.Label(
            frame,
            text=f"좌표 기준: 화면(스크린) 좌표 · 드래그 감지: {scope}",
            fg="gray",
        ).grid(row=len(rows) + 1, column=0, columnspan=2, pady=(6, 0))

        if self.read_button is None:
            root.bind("<ButtonPress-1>", lambda e: self._set_window_pressed(True))
            root.bind("<ButtonRelease-1>", lambda e: self._set_window_pressed(False))

        self._poll()

    def _set_window_pressed(self, value: bool) -> None:
        self._window_pressed = value

    def _poll(self) -> None:
        pos = self.root.winfo_pointerxy()
        pressed = self.read_button() if self.read_button else self._window_pressed
        self.state.update(pos, pressed)

        self.vars["current"].set(_fmt(pos))
        self.vars["start"].set(_fmt(self.state.start))
        self.vars["drag_current"].set(_fmt(self.state.current))
        self.vars["delta"].set(_fmt_delta(self.state.delta))

        if self.state.dragging:
            self.status.set("드래그 중")
            self.status_label.config(fg="#d9480f")
        elif self.state.start is not None:
            self.status.set("드래그 종료 (마지막 값 표시)")
            self.status_label.config(fg="#2b8a3e")

        self.root.after(POLL_MS, self._poll)


def main() -> None:
    root = tk.Tk()
    MouseTrackerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
