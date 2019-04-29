FROM python:3.7-alpine

WORKDIR /app

COPY src/requirements.txt requirements.txt

RUN pip install -q --upgrade pip && pip install -q -r requirements.txt

COPY ./src /app

WORKDIR src

CMD gunicorn -w 4 -b 0.0.0.0:8000 main:app
