FROM python:3.10-slim-buster as prod

RUN apt-get update && apt-get install -y
RUN apt-get install -y gcc
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools

COPY requirements.txt requirements.txt
RUN pip install \
    --no-warn-script-location \
    --ignore-installed \
    --requirement requirements.txt

RUN groupadd --gid 1000 app \
 && useradd --create-home --home /app --gid 1000 --uid 1000 app


USER app
WORKDIR /app
