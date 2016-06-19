import re

from setuptools import setup


with open('masecret/__init__.py') as f:
    init_content = f.read()

version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                    init_content, re.MULTILINE).group(1)

long_description = """
masecret
========

A command to mask secret information of images using OCR.

Prerequisite
------------

-  Python 3.3+
-  `Tesseract <https://github.com/tesseract-ocr/tesseract>`__
-  Languages for OCR (can be set by ``--lang``, default is ``eng+jpn``)
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

Preparation
~~~~~~~~~~~

Create a ``SECRETS.txt`` in a current directory. Content of the file is
regular expression patterns which match secret information you want to
mask. You can includes multiple patterns using multi lines.

Example content of ``SECRETS.txt`` to mask AWS account number:

::

    [-\d]{12,}

Mask Secret
~~~~~~~~~~~

Mask a single file:

::

    $ masecret original.png masked.png

Mask multiple files (output directory must exist):

::

    $ masecret original1.png original2.png ... masked_images/

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
    install_requires=['Pillow', 'pyocr'],
    entry_points={
        'console_scripts': [
            'masecret = masecret.cli:main'
        ]
    }
)
