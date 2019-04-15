FROM python:3.7-alpine
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY main.py main.py
COPY templates templates
COPY pages pages
CMD python main.py
