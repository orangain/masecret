import re

from setuptools import setup


with open('masecret/__init__.py') as f:
    init_content = f.read()

version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                    init_content, re.MULTILINE).group(1)

long_description = """
masecret
========

masecret is a command to mask secret information in image files using OCR.

Prerequisite
------------

-  Python 3.3+
-  `Tesseract <https://github.com/tesseract-ocr/tesseract>`__

  -  Language data for OCR (can be specified with ``--lang``, default is ``eng``)
     must be available.

Installation
------------

::

    $ pip3 install masecret

You may need ``sudo``.

masecret depends on `pyocr <https://github.com/jflesch/pyocr>`__ and
`Pillow <https://pillow.readthedocs.io/>`__. If you fail to install
Pillow, please see the installation instruction of Pillow.

Usage
-----

Mask a single file:

::

    $ masecret -r '[-\d]{12,}' original.png -o masked.png

Mask multiple files (output directory must exist):

::

    $ masecret -r '[-\d]{12,}' original1.png original2.png ... -o masked_images/

With ``-i`` option, image files are masked in-place.

::

    $ masecret -r '[-\d]{12,}' -i original1.png original2.png ...

SECRETS.txt
~~~~~~~~~~~

If you don't specify ``-r`` option, regular expression are read from a file named
``SECRETS.txt`` in a current directory.
Content of the file is regular expression patterns which match secret information
you want to mask. You can include multiple patterns line by line.

Example content of ``SECRETS.txt`` to mask AWS account number:

::

    [-\d]{12,}

"""

setup(
    name="masecret",
    version=version,
    author="orangain",
    author_email="orangain@gmail.com",
    description="A command to mask secret information of images using OCR",
    long_description=long_description,
    license="MIT",
    keywords="ocr image screenshot secret mask",
    url="https://github.com/orangain/masecret",
    packages=['masecret'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Utilities",
    ],
    install_requires=['Pillow', 'pyocr>=0.4.3'],
    entry_points={
        'console_scripts': [
            'masecret = masecret.cli:main'
        ]
    }
)
