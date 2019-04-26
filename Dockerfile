FROM python:3.7-alpine
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY main.py main.py
COPY templates templates
COPY ./posts /app/posts/
CMD FLASK_APP=main.py FLASK_DEBUG=1 python -m flask run \
    --host=0.0.0.0 --port=8000

