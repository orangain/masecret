import unittest
from unittest.mock import MagicMock

import re
import os
import tempfile

from PIL import Image

from masecret.cli import parser, parse_args, get_secret_res, input_output_pairs, find_secret_rects

FIXTURES_DIR = os.path.join(os.path.dirname(__file__), 'fixtures')


class TestParseArgs(unittest.TestCase):

    def setUp(self):
        self.original_error = parser.error
        parser.error = MagicMock(side_effect=SystemExit())

    def tearDown(self):
        parser.error = self.original_error

    def test_no_argument(self):
        with self.assertRaises(SystemExit):
            parse_args([])
        parser.error.assert_called_once_with('the following arguments are required: INPUT')

    def test_one_argument(self):
        with self.assertRaises(SystemExit):
            parse_args(['original.png'])
        parser.error.assert_called_once_with('-o OUTPUT is required unless -i is specified.')

    def test_two_arguments(self):
        with self.assertRaises(SystemExit):
            parse_args(['original1.png', 'original2.png'])
        parser.error.assert_called_once_with('-o OUTPUT is required unless -i is specified.')

    def test_two_arguments_with_output_file(self):
        with self.assertRaises(SystemExit):
            parse_args(['original1.png', 'original2.png', '-o', 'masked.png'])
        parser.error.assert_called_once_with('OUTPUT must be a directory when there are multiple INPUTs.')

    def test_two_arguments_with_output_dir(self):
        with tempfile.TemporaryDirectory() as tempdir:
            args = parse_args(['original1.png', 'original2.png', '-o', tempdir])
            self.assertEqual(args.input_paths, ['original1.png', 'original2.png'])
            self.assertEqual(args.output_location, tempdir)

    def test_one_argument_with_in_place(self):
        args = parse_args(['-i', 'original.png'])
        self.assertTrue(args.in_place)
        self.assertEqual(args.input_paths, ['original.png'])

    def test_both_in_place_and_output(self):
        with self.assertRaises(SystemExit):
            parse_args(['-i', 'original.png', '-o', 'masked.png'])
        parser.error.assert_called_once_with('You MUST NOT specify both -i and -o options.')

    def test_both_regex_and_secret(self):
        with self.assertRaises(SystemExit):
            parse_args(['-s', 'mysecret.txt', '-r', 'PA.*RD',
                        'original.png', '-o', 'masked.png'])
        parser.error.assert_called_once_with('You MUST NOT specify both -r and -s options.')


class TestGetSecretRes(unittest.TestCase):

    def test_secret_file(self):
        secrets_path = os.path.join(FIXTURES_DIR, 'secrets_for_test.txt')
        args = parse_args(['-s', secrets_path, 'original.png', '-o', 'masked.png'])
        patterns = [r.pattern for r in get_secret_res(args)]
        self.assertEqual(patterns, [r'[-\d]+', r'PA.*RD'])

    def test_regex_option(self):
        args = parse_args(['-r', 'PA.*RD', 'original.png', '-o', 'masked.png'])
        patterns = [r.pattern for r in get_secret_res(args)]
        self.assertEqual(patterns, ['PA.*RD'])


class TestInputOutputPairs(unittest.TestCase):

    def test_output_file(self):
        args = parse_args(['-o', 'masked.png', 'original.png'])
        self.assertEqual(list(input_output_pairs(args)), [('original.png', 'masked.png')])

    def test_output_dir(self):
        with tempfile.TemporaryDirectory() as tempdir:
            args = parse_args(['-o', tempdir, 'original.png'])
            self.assertEqual(list(input_output_pairs(args)), [
                ('original.png', os.path.join(tempdir, 'original.png'))
            ])

    def test_output_dir_multiple_files(self):
        with tempfile.TemporaryDirectory() as tempdir:
            args = parse_args(['-o', tempdir, 'original1.png', 'original2.png'])
            self.assertEqual(list(input_output_pairs(args)), [
                ('original1.png', os.path.join(tempdir, 'original1.png')),
                ('original2.png', os.path.join(tempdir, 'original2.png')),
            ])

    def test_in_place(self):
        args = parse_args(['-i', 'original.png'])
        self.assertEqual(list(input_output_pairs(args)), [('original.png', 'original.png')])

    def test_in_place_multiple_files(self):
        args = parse_args(['-i', 'original1.png', 'original2.png'])
        self.assertEqual(list(input_output_pairs(args)), [
            ('original1.png', 'original1.png'),
            ('original2.png', 'original2.png'),
        ])


class TestFindSecretRects(unittest.TestCase):

    def test_find_secret_rects(self):
        image = Image.open(os.path.join(FIXTURES_DIR, 'original_eng.png'))
        secret_res = [re.compile(r'[-\d]{12,}')]

        secret_rects = find_secret_rects(image, secret_res, 'eng')

        self.assertEquals(secret_rects, [((1460, 235), (1665, 258))])

    def test_find_secret_rects_jpn(self):
        image = Image.open(os.path.join(FIXTURES_DIR, 'original_jpn.png'))
        secret_res = [re.compile(r'[-—\d]{12,}')]  # include dash sign

        secret_rects = find_secret_rects(image, secret_res, 'eng+jpn')

        self.assertEquals(secret_rects, [((1500, 235), (1705, 258))])


if __name__ == '__main__':
    unittest.main()
