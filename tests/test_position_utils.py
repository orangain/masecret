import unittest

from masecret.position_utils import (add_positions, offset_rect, bounding_box,
                                     padding_box, bounding_boxes_by_line)


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

    def test_bounding_boxes_by_line_one_line(self):
        rects = [
            ((0, 0), (10, 20)),
            ((10, 0), (20, 20)),
            ((25, 0), (35, 15)),
        ]
        self.assertEqual(list(bounding_boxes_by_line(rects)), [((0, 0), (35, 20))])

    def test_bounding_boxes_by_line_multiple_lines(self):
        rects = [
            ((100, 0), (110, 20)),
            ((110, 0), (120, 20)),
            ((125, 0), (135, 15)),
            ((0, 20), (10, 40)),
            ((10, 20), (20, 40)),
            ((25, 20), (35, 35)),
        ]
        self.assertEqual(list(bounding_boxes_by_line(rects)),
                         [((100, 0), (135, 20)), ((0, 20), (35, 40))])


if __name__ == '__main__':
    unittest.main()
