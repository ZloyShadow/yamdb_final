FROM python:3.7-slim

WORKDIR /app

RUN apt-get update -y
RUN apt-get upgrade -y

COPY requirements.txt /app

RUN pip3 install -r requirements.txt --no-cache-dir

COPY ./ .

CMD ["gunicorn", "api_yamdb.wsgi:application", "--bind", "0:8000"]