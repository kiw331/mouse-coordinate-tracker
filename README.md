# mouse-coordinate-tracker

마우스 좌표를 실시간으로 보여주는 Python GUI 프로그램 (tkinter, 외부 의존성 없음).

## 기능

- **실시간 좌표**: 마우스 커서의 현재 화면(스크린) 좌표를 표시
- **드래그 추적**: 왼쪽 버튼을 누르고 드래그하면
  - 드래그 시작 좌표 (클릭한 위치)
  - 드래그 현재 좌표
  - 상대 변화량 `(dx, dy)` = 현재 − 시작
- 버튼을 떼면 마지막 드래그 값이 유지됨
- Windows에서는 창 밖(화면 전체)의 드래그도 감지. 다른 OS에서는 창 안에서만 감지

## 실행

```bash
python -m mouse_tracker
```

## 테스트

```bash
python -m unittest discover -s tests
```

## 구조

```
mouse_tracker/
  app.py       # tkinter GUI, 좌표 폴링(약 60fps)
  tracker.py   # 드래그 상태 계산 로직 (GUI 독립)
  __main__.py  # python -m 진입점
tests/
  test_tracker.py
```

## exe 빌드

```bash
pip install pyinstaller
python -m PyInstaller --onefile --windowed --name MouseCoordinateTracker mouse_tracker/__main__.py
```
