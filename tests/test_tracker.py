import unittest

from mouse_tracker.tracker import DragState


class DragStateTest(unittest.TestCase):
    def test_initial_state(self):
        s = DragState()
        self.assertIsNone(s.start)
        self.assertIsNone(s.delta)
        self.assertFalse(s.dragging)

    def test_drag_computes_delta(self):
        s = DragState()
        s.update((100, 200), pressed=True)
        s.update((130, 150), pressed=True)
        self.assertTrue(s.dragging)
        self.assertEqual(s.start, (100, 200))
        self.assertEqual(s.current, (130, 150))
        self.assertEqual(s.delta, (30, -50))

    def test_release_keeps_last_values(self):
        s = DragState()
        s.update((0, 0), pressed=True)
        s.update((10, 10), pressed=True)
        s.update((10, 10), pressed=False)
        s.update((500, 500), pressed=False)  # 놓은 뒤 이동은 반영 안 됨
        self.assertFalse(s.dragging)
        self.assertEqual(s.delta, (10, 10))

    def test_new_drag_resets_start(self):
        s = DragState()
        s.update((0, 0), pressed=True)
        s.update((5, 5), pressed=False)
        s.update((50, 60), pressed=True)
        self.assertEqual(s.start, (50, 60))
        self.assertEqual(s.delta, (0, 0))


if __name__ == "__main__":
    unittest.main()
