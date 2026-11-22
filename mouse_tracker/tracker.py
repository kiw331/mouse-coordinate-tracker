"""GUI와 독립적인 드래그 상태 로직."""

from dataclasses import dataclass
from typing import Optional, Tuple

Point = Tuple[int, int]


@dataclass
class DragState:
    """마우스 버튼 상태 변화를 받아 드래그 시작점/현재점/변화량을 계산한다."""

    start: Optional[Point] = None
    current: Optional[Point] = None
    dragging: bool = False

    def update(self, pos: Point, pressed: bool) -> None:
        if pressed and not self.dragging:
            # 버튼이 막 눌림 -> 드래그 시작
            self.dragging = True
            self.start = pos
        if self.dragging:
            self.current = pos
        if not pressed and self.dragging:
            # 버튼을 뗌 -> 드래그 종료 (마지막 값은 유지)
            self.dragging = False

    @property
    def delta(self) -> Optional[Point]:
        if self.start is None or self.current is None:
            return None
        return (self.current[0] - self.start[0], self.current[1] - self.start[1])
