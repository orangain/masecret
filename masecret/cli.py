import sys
import os
import re
import argparse

from PIL import Image, ImageDraw, ImageColor
from pyocr.tesseract import image_to_string

from masecret import __version__
from masecret.builders import ModifiedCharBoxBuilder
from masecret.position_utils import offset_rect, bounding_box, padding_box


def main():
    parser = argparse.ArgumentParser(
        description='Mask secret information of images using OCR.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('input_paths', metavar='INPUT', nargs='+',
                        help='input files')
    parser.add_argument('output_location', metavar='OUTPUT',
                        help='output file or directory')
    parser.add_argument('-V', '--version', action='version',
                        version='%(prog)s {0}'.format(__version__))
    parser.add_argument('-s', '--secret', dest='secret_path', default='./SECRETS.txt',
                        help='path to secret regex file')
    parser.add_argument('-l', '--lang', dest='lang', default='eng',
                        help='language for OCR, can be multiple languages joined by + sign')
    parser.add_argument('-c', '--color', dest='color', default='#666',
                        help='color to fill secrets')
    parser.add_argument('--tesseract-configs', dest='tesseract_configs', metavar='CONFIGS',
                        default=','.join(ModifiedCharBoxBuilder.tesseract_configs),
                        help='(Advanced Option) comma-separated configs to be passed to tesseract')

    args = parser.parse_args()

    if len(args.input_paths) >= 2 and not os.path.isdir(args.output_location):
        print('OUTPUT must be a directory when there are multiple INPUTs.', file=sys.stderr)
        exit(1)

    secret_res = get_secret_res(args.secret_path)
    options = {
        'lang': args.lang,
        'fill_color': ImageColor.getrgb(args.color),
        'tesseract_configs': args.tesseract_configs.split(','),
    }

    for input_path in args.input_paths:
        if os.path.isdir(args.output_location):
            output_path = os.path.join(args.output_location, os.path.basename(input_path))
        else:
            output_path = args.output_location

        mask_secrets(input_path, output_path, secret_res, **options)


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


def mask_secrets(input_path, output_path, secret_res, lang, fill_color, tesseract_configs=None):
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
    if tesseract_configs:
        builder.tesseract_configs = tesseract_configs

    boxes = image_to_string(cropped_image, lang=lang, builder=builder)

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
        mask_rect(image, rect, fill_color)

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
