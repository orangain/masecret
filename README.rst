masecret
========

|pypiBadge| |testBadge| |coverageBadge|

.. |pypiBadge| image:: https://badge.fury.io/py/masecret.svg
    :target: https://pypi.python.org/pypi/masecret
.. |testBadge| image:: https://api.shippable.com/projects/5895dc346e5b460f005d7aaa/badge?branch=master
    :target: https://app.shippable.com/projects/5895dc346e5b460f005d7aaa
.. |coverageBadge| image:: https://api.shippable.com/projects/5895dc346e5b460f005d7aaa/coverageBadge?branch=master
    :target: https://app.shippable.com/projects/5895dc346e5b460f005d7aaa

masecret is a command to mask secret information in image files using OCR.

**DISCLAIMER**: There is no guarantee that all the secret information is successfully masked. You must make sure that all the secret information is masked.

Before:

.. figure:: docs/original.png
   :alt: Before

After:

.. figure:: docs/masked.png
   :alt: After

Prerequisite
------------

- Python 3.3+
- `Tesseract <https://github.com/tesseract-ocr/tesseract>`__

  - Language data for OCR (can be specified with ``--lang``, default is ``eng``)
    must be available.

Installation
------------

::

    $ pip3 install masecret

You may need ``sudo``.

masecret depends on `pyocr <https://github.com/jflesch/pyocr>`__ and
`Pillow <https://pillow.readthedocs.io/>`__. If you fail to install
Pillow, please see `the installation instruction of Pillow <http://pillow.readthedocs.io/en/latest/installation.html>`__.

Usage
-----

Mask a single image file with a regular expression pattern that match AWS account number::

    $ masecret -r '[-\d]{12,}' original.png -o masked.png

Mask multiple image files (output directory must exist)::

    $ masecret -r '[-\d]{12,}' original1.png original2.png ... -o masked_images/

Mask image files in-place with ``-i`` option::

    $ masecret -i -r '[-\d]{12,}' original1.png original2.png ...

WARNING: No backup files will be saved.

SECRETS.txt
~~~~~~~~~~~

If ``-r`` option is not specified, regular expression will be read from a file named
``SECRETS.txt`` in a current directory.
Content of the file is regular expression patterns that match secret information
you want to mask. You can include multiple patterns line by line.

Full Usage
~~~~~~~~~~

::

    usage:
        masecret [options] INPUT -o OUTPUT
        masecret [options] INPUT... -o OUTPUT
        masecret -i [options] INPUT...

    Mask secret information in image files using OCR. Put regular expression
    matches secret information into a file named SECRETS.txt or -r option.

    positional arguments:
      INPUT                 input files

    optional arguments:
      -h, --help            show this help message and exit
      -V, --version         show program's version number and exit
      -o OUTPUT, --output OUTPUT
                            output file or directory (default: None)
      -r REGEX, --regex REGEX
                            regular expression matches secret information
                            (default: None)
      -s SECRET_PATH, --secret SECRET_PATH
                            path to file containing regexes line by line that
                            match secret information (default: ./SECRETS.txt)
      -l LANG, --lang LANG  language for OCR, can be multiple languages joined by
                            + sign, e.g. eng+jpn (default: eng)
      -c COLOR, --color COLOR
                            color to fill secrets (default: #666)
      -i, --in-place        mask image files in-place. WARNING: No backup files
                            will be saved (default: False)
      --tesseract-params PARAMS
                            (Advanced Option) additional parameters passed to
                            tesseract (default: -psm 6 makebox)

Debug
-----

If images are not masked as expected, the environment variable ``DEBUG``
will help you. If ``DEBUG`` is set, all the characters tesseract
recognized are printed with position.

::

    $ DEBUG=1 masecret original.png -o masked.png
    Processing original.png...
    . ((136, 90), (160, 114))
    . ((176, 90), (200, 114))
    . ((216, 90), (240, 114))
    I ((292, 104), (304, 126))
    I ((308, 104), (320, 126))
    A ((326, 104), (340, 120))
    W ((341, 104), (361, 120))
    S ((362, 103), (375, 120))
    M ((385, 104), (401, 120))
    a ((404, 108), (415, 120))
    n ((417, 108), (427, 120))
    a ((430, 108), (440, 120))
    g ((443, 108), (453, 125))
    e ((456, 108), (467, 120))
    m ((469, 108), (485, 120))
    e ((488, 108), (499, 120))
    n ((501, 108), (511, 120))
    t ((513, 105), (519, 120))
    C ((528, 103), (542, 120))
    o ((545, 108), (556, 120))
    n ((559, 108), (569, 120))
    ...

License
-------

MIT License. See: ``LICENSE``.

Packaging
---------

::

    (venv) $ pip install -r dev-requirements.txt
    (venv) $ nosetests
    (venv) $ python setup.py sdist bdist_wheel upload
