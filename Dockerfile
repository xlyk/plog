FROM python:3.7-alpine

ARG IS_DEBUG=false

WORKDIR /app

COPY ./requirements.txt requirements.txt

RUN pip install -q --upgrade pip && \
    pip install -q -r requirements.txt

COPY ./src /app

CMD if [[ "$IS_DEBUG" = "true" ]]; then \
        FLASK_APP=/app/src/main.py FLASK_DEBUG=1 \
            python -m flask run --host=0.0.0.0 --port=8000 ; \
    else \
        gunicorn -w 4 -b 0.0.0.0:8000 src.main:app ; \
    fi
