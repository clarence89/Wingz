FROM python:3.9-alpine
LABEL maintainer="Clarence Advincula Baluyot <akingprincess@gmail.com> https://www.linkedin.com/in/clarencebaluyot/"
WORKDIR /usr/src/app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apk update && apk add --no-cache \
    build-base \
    libpq \
    libpq-dev \
    libffi-dev \
    cups \
    rm -rf /var/cache/apk/*

RUN pip install --upgrade pip pipenv flake8 black

COPY Pipfile* ./
RUN pipenv install --system --ignore-pipfile

COPY . .

RUN pipenv run black .
EXPOSE 8000
EXPOSE 8081
RUN flake8 --ignore=E501,F401,W503 --exclude=node_modules .
