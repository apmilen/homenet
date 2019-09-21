FROM node:8-buster-slim

RUN apt-get update && apt-get install -y python3.7\
    python3-pip \
    gcc \
    python3.7-dev \
    libpq-dev \
    locales \
    libpango1.0-0 \
    libcairo2

RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales && \
    update-locale LANG=en_US.UTF-8

ENV LANG en_US.UTF-8 

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

WORKDIR /opt/monadical.homenet/pennydjango/
# RUN adduser www-data
USER www-data
RUN echo $USER