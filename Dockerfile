From python:3.7

LABEL maintainer="samuel.joaquim@gmail.com"

RUN apt-get update -y

RUN pip install pipenv

EXPOSE 5000/tcp

RUN mkdir /app

COPY ./app/ /app/

WORKDIR /app

RUN pipenv install

ENTRYPOINT pipenv run python3 api.py
