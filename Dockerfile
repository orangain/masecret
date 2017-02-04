FROM python:3.6
MAINTAINER orangain@gmail.com

RUN apt-get update && apt-get install -y \
	tesseract-ocr \
	tesseract-ocr-eng \
	tesseract-ocr-jpn \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /work

COPY dev-requirements.txt ./
RUN pip3 install -r dev-requirements.txt

COPY . ./
RUN pip3 install -e .
