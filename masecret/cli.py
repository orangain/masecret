import sys
import os
import re

from PIL import Image, ImageDraw
from pyocr.tesseract import image_to_string

from masecret.builders import ModifiedCharBoxBuilder
from masecret.position_utils import offset_rect, bounding_box, padding_box


def main():
    args = sys.argv[1:]

    if len(args) < 2:
        print('Usage: {0} INPUT... OUTPUT'.format(sys.argv[0]), file=sys.stderr)
        exit(1)

    input_paths = args[:-1]
    output_location = args[-1]

    if len(input_paths) >= 2 and not os.path.isdir(output_location):
        print('OUTPUT must be a directory when there are multiple INPUTs.', file=sys.stderr)
        exit(1)

    secret_res = get_secret_res('SECRETS.txt')

    for input_path in input_paths:
        if os.path.isdir(output_location):
            output_path = os.path.join(output_location, os.path.basename(input_path))
        else:
            output_path = output_location

        mask_secrets(input_path, output_path, secret_res, (96, 96, 96))


def get_secret_res(secret_path):
    """
    Read secret regexes from a file secret_path.

    param: str secret_path
    return: list of regexes
    rtype: list
    """

    res = []
    with open(secret_path) as f:
        for line in f:
            pattern = line.rstrip()
            res.append(re.compile(pattern))

    return res


def mask_secrets(input_path, output_path, secret_res, color):
    """
    Mask secret infomation in an image.

    param: str input_path
    param: str output_path
    param: list secret_res
    param: tuple color
    """

    print('Processing {0}...'.format(input_path), file=sys.stderr)

    image = Image.open(input_path)
    #offset = (0, 150)
    #cropped_image = image.crop((offset[0], offset[1], image.size[0], 220))
    offset = (0, 0)
    cropped_image = image

    builder = ModifiedCharBoxBuilder(image.size[1])
    boxes = image_to_string(cropped_image, lang='eng+jpn', builder=builder)

    if os.environ.get('DEBUG'):
        for box in boxes:
            print(box.content, box.position)

    content = ''.join(box.content for box in boxes)
    assert len(boxes) == len(content)

    secret_rects = []
    for secret_re in secret_res:
        for m in secret_re.finditer(content):
            matched_boxes = boxes[m.start():m.end()]
            rect = bounding_box([b.position for b in matched_boxes])
            rect = offset_rect(offset, padding_box(rect, 2))
            secret_rects.append(rect)

    print('Found {0} secrets at {1}'.format(len(secret_rects), secret_rects), file=sys.stderr)
    for rect in secret_rects:
        mask_rect(image, rect, color)

    image.save(output_path)
    print('Saved to {0}'.format(output_path), file=sys.stderr)


def mask_rect(image, rect, color):
    """
    Fill a rect in an image.

    param: Image image
    param: Rect rect
    param: tuple color
    """

    draw = ImageDraw.Draw(image)
    draw.rectangle(rect, fill=color)


if __name__ == '__main__':
    main()
