FROM --platform=linux/x86_64 python:3.9.16-bullseye

ENV PYTHONIOENCODING utf-8

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --upgrade pip && pip install --no-cache-dir -r ./requirements.txt

COPY ./app ./