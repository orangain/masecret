import unittest

from masecret.position_utils import add_positions, offset_rect, bounding_box, padding_box


class TestPositionUtils(unittest.TestCase):

    def test_add_positions(self):
        a = (10, 20)
        b = (30, 40)
        self.assertEqual(add_positions(a, b), (40, 60))

    def test_offset_rect(self):
        rect = ((10, 20), (40, 60))
        offset = (15, 20)
        self.assertEqual(offset_rect(offset, rect),
                         ((25, 40), (55, 80)))

    def test_bounding_box_single_box(self):
        rects = [
            ((10, 20), (40, 60)),
        ]
        self.assertEqual(bounding_box(rects),
                         ((10, 20), (40, 60)))

    def test_bounding_box_multiple_boxes(self):
        rects = [
            ((10, 20), (40, 60)),
            ((100, 30), (120, 90)),
        ]
        self.assertEqual(bounding_box(rects),
                         ((10, 20), (120, 90)))

    def test_padding_box(self):
        rect = ((10, 20), (40, 60))
        self.assertEqual(padding_box(rect, 5),
                         ((5, 15), (45, 65)))

if __name__ == '__main__':
    unittest.main()
