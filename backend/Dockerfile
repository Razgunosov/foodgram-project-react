FROM python:3.8

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

COPY . .

CMD [ "gunicorn", "config.wsgi", "--bind", "0:8000" ]