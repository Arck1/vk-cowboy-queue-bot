FROM python:latest

ENV PYTHONUNBUFFERED 1
ENV LIBRARY_PATH=/lib:/usr/lib

WORKDIR /usr/src/app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY main.py /usr/src/app/main.py
COPY env.json /usr/src/app/env.json
COPY settings.py /usr/src/app/settings.py

