import sys
import os
import re
import argparse

from PIL import Image, ImageDraw, ImageColor
from pyocr.tesseract import image_to_string

from masecret import __version__
from masecret.builders import ModifiedCharBoxBuilder
from masecret.position_utils import offset_rect, bounding_box, padding_box


parser = argparse.ArgumentParser(
    usage='''
    %(prog)s [options] INPUT -o OUTPUT
    %(prog)s [options] INPUT... -o OUTPUT
    %(prog)s -i [options] INPUT...''',
    description='''
        Mask secret information in image files using OCR.
        Put regular expression matches secret information
        into a file named SECRETS.txt or -r option.''',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('input_paths', metavar='INPUT', nargs='+',
                    help='input files')
parser.add_argument('-V', '--version', action='version',
                    version='%(prog)s {0}'.format(__version__))
parser.add_argument('-o', '--output', dest='output_location', metavar='OUTPUT',
                    help='output file or directory')
parser.add_argument('-r', '--regex', dest='regex', default=None,
                    help='regular expression matches secret information')
parser.add_argument('-s', '--secret', dest='secret_path', default='./SECRETS.txt',
                    help='path to file containing regexes line by line that match secret information')
parser.add_argument('-l', '--lang', dest='lang', default='eng',
                    help='language for OCR, can be multiple languages joined by + sign, e.g. eng+jpn')
parser.add_argument('-c', '--color', dest='color', default='#666',
                    help='color to fill secrets')
parser.add_argument('-i', '--in-place', dest='in_place', action='store_true', default=False,
                    help='mask image files in-place. WARNING: No backup files will be saved')
parser.add_argument('--tesseract-configs', dest='tesseract_configs', metavar='CONFIGS',
                    default=','.join(ModifiedCharBoxBuilder.tesseract_configs),
                    help='(Advanced Option) comma-separated configs to be passed to tesseract')


def main():
    args = parse_args()

    secret_res = get_secret_res(args)
    options = {
        'lang': args.lang,
        'fill_color': ImageColor.getrgb(args.color),
        'tesseract_configs': args.tesseract_configs.split(','),
    }

    for input_path, output_path in input_output_pairs(args):
        mask_secrets(input_path, output_path, secret_res, **options)


def parse_args(args=None):
    """
    Parse command line arguments and convert to a Namespace object.

    param: list args
    return: parsed arguments
    rtype: Namespace
    """

    args = parser.parse_args(args)

    if args.in_place and args.output_location:
        parser.error('You MUST NOT specify both -i and -o options.')

    if not args.in_place:
        if not args.output_location:
            parser.error('-o OUTPUT is required unless -i is specified.')

        if len(args.input_paths) >= 2 and not os.path.isdir(args.output_location):
            parser.error('OUTPUT must be a directory when there are multiple INPUTs.')

    if args.regex and args.secret_path != './SECRETS.txt':
        parser.error('You MUST NOT specify both -r and -s options.')

    return args


def get_secret_res(args):
    """
    Get secret regexes from a Namespace object.

    param: Namespace args
    return: list of regexes
    rtype: list
    """

    if args.regex:
        return [re.compile(args.regex)]
    else:
        return read_secret_res_from_file(args.secret_path)


def read_secret_res_from_file(secret_path):
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


def input_output_pairs(args):
    """
    Yield pairs of input path and output path.

    param: Namespace args
    return: generator of tuple (input_path, output_path)
    rtype: generator
    """

    for input_path in args.input_paths:
        if args.in_place:
            yield (input_path, input_path)
        elif os.path.isdir(args.output_location):
            yield (input_path, os.path.join(args.output_location, os.path.basename(input_path)))
        else:
            yield (input_path, args.output_location)


def mask_secrets(input_path, output_path, secret_res, lang, fill_color, tesseract_configs=None):
    """
    Mask secret infomation in an image.

    param: str input_path
    param: str output_path
    param: list secret_res
    param: str lang
    param: str tesseract_configs
    param: tuple fill_color
    """

    print('Processing {0}...'.format(input_path), file=sys.stderr)

    image = Image.open(input_path)
    secret_rects = find_secret_rects(image, secret_res, lang, tesseract_configs)
    print('Found {0} secrets at {1}'.format(len(secret_rects), secret_rects), file=sys.stderr)
    for rect in secret_rects:
        mask_rect(image, rect, fill_color)

    image.save(output_path)
    print('Saved to {0}'.format(output_path), file=sys.stderr)


def find_secret_rects(image, secret_res, lang, tesseract_configs=None):
    """
    Find secret rects in an image.

    param: Image image
    param: list secret_res
    param: str lang
    param: str tesseract_configs
    return: list of rects
    rtype: list
    """

    # offset = (0, 150)
    # cropped_image = image.crop((offset[0], offset[1], image.size[0], 220))
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

    return secret_rects


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
