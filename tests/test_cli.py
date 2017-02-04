import unittest

import re
import os
from PIL import Image

from masecret.cli import find_secret_rects


class TestCli(unittest.TestCase):

    def test_find_secret_rects(self):
        image = Image.open(os.path.join(os.path.dirname(__file__), 'fixture_eng.png'))
        secret_res = [re.compile(r'[-\d]{12,}')]

        secret_rects = find_secret_rects(image, secret_res, 'eng')

        self.assertEquals(secret_rects, [((1460, 235), (1665, 259))])

    def test_find_secret_rects_jpn(self):
        image = Image.open(os.path.join(os.path.dirname(__file__), 'fixture_jpn.png'))
        secret_res = [re.compile(r'[-—\d]{12,}')]  # include dash sign

        secret_rects = find_secret_rects(image, secret_res, 'eng+jpn')

        self.assertEquals(secret_rects, [((1500, 235), (1705, 259))])


if __name__ == '__main__':
    unittest.main()
