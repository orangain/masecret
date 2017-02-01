from pyocr.tesseract import CharBoxBuilder
from pyocr.builders import Box


class ModifiedCharBoxBuilder(CharBoxBuilder):

    # Though CharBoxBuilder's tesseract_configs includes 'batch.nochop',
    # this cause misrecognition. So it is removed.
    tesseract_configs = ['makebox']

    def __init__(self, image_height):
        """
        param: int image_height
        """

        super().__init__()
        self.image_height = image_height

    def read_file(self, file_descriptor):
        boxes = CharBoxBuilder.read_file(file_descriptor)

        # Though CharBoxBuilder's base position (0, 0) is top left,
        # box file's base position (0, 0) is bottom left.
        # Therefore position must be reflected.
        # See: https://github.com/tesseract-ocr/tesseract/wiki/TrainingTesseract
        for box in boxes:
            box.position = self._reflect_rect_vertically(box.position)

        def _ensure_one_char_per_box(boxes):
            """
            Occasionally, a Box contains two characters.
            So, ensure that all the boxes contains only one characters.
            """

            char_boxes = []
            for box in boxes:
                if len(box.content) == 1:
                    char_boxes.append(box)
                else:
                    assert len(box.content) >= 2
                    for c in box.content:
                        char_boxes.append(Box(c, box.position))

            return char_boxes

        return _ensure_one_char_per_box(boxes)

    def _reflect_rect_vertically(self, rect):
        """
        Get a new Rect where rect is reflected vertically.

        param: Rect rect
        return: vertically reflected Rect
        rtype: Rect
        """

        top_left, bottom_right = rect
        bottom_left = self._reflect_pos_vertically(top_left)
        top_right = self._reflect_pos_vertically(bottom_right)

        left, bottom = bottom_left
        right, top = top_right

        return ((left, top), (right, bottom))

    def _reflect_pos_vertically(self, pos):
        """
        Get a new Position where pos is reflected vertically.

        param: Position pos
        return: vertically reflected Position
        rtype: Position
        """

        return pos[0], self.image_height - pos[1]
