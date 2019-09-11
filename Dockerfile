FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

LABEL maintainer "Jordan Bonser <jordan_bonser@live.co.uk>"

COPY requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

EXPOSE 80