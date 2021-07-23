FROM python:3.9

ENV APP_CODE=/usr/src/app
RUN mkdir $APP_CODE
WORKDIR $APP_CODE

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY Pipfile Pipfile.lock $APP_CODE/
RUN pip install pipenv && pipenv install --system

COPY . $APP_CODE/
