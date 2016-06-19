import re

from setuptools import setup


with open('masecret/__init__.py') as f:
    init_content = f.read()

version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                    init_content, re.MULTILINE).group(1)

setup(
    name="masecret",
    version=version,
    author="orangain",
    author_email="orangain@gmail.com",
    description="A command to mask secret information from images using OCR",
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
