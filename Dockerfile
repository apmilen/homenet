FROM node:8-buster-slim

RUN apt-get update && apt-get install -y python3.7\
    python3-pip \
    gcc \
    python3.7-dev \
    libpq-dev

RUN python3.7 -m pip install -U pip \
    pipenv 



ENV PYTHONUNBUFFERED 1

ADD ./pennydjango /opt/monadical.homenet/pennydjango
ADD ./env /opt/monadical.homenet/env
ADD ./Pipfile  /opt/monadical.homenet/pennydjango/Pipfile
ADD ./Pipfile.lock  /opt/monadical.homenet/pennydjango/Pipfile.lock


WORKDIR /opt/monadical.homenet/pennydjango

RUN pipenv install --system --deploy --ignore-pipfile --dev
RUN pipenv clean
RUN pipenv lock --clear
RUN pipenv check

RUN apt-get update && apt-get install -y --no-install-recommends \
    gdal-bin \
    npm

RUN npm install --global npm
RUN npm install --upgrade --global yarn

WORKDIR /opt/monadical.homenet/pennydjango/js
RUN yarn install


WORKDIR /opt/monadical.homenet/pennydjango
RUN python3 ./manage.py migrate