# .-= The part for Django =-.\
FROM python:3.6

ENV PYTHONBUFFERED 1
ENV DJANGO_ENV dev
ENV DOCKER_CONTAINER 1

COPY ./web/calories/back-end/requirements.txt /web/requirements.txt
RUN pip3 install -U pip
RUN pip3 install -r /web/requirements.txt
COPY ./config/postgres/ /

COPY . /web/
WORKDIR /web/

#Add the library for compiling the translations
#RUN apt-get update && apt-get install -y gettext \
#    vim \
#    python-pip python-dev build-essential \
#    gunicorn

RUN adduser --disabled-password --gecos '' myuser
#
## Install NPM for React
#RUN apt-get install -y curl xvfb libgtk2.0-0 libnotify-dev libgconf-2-4 libnss3 libxss1 libasound2
#RUN curl -sL https://deb.nodesource.com/setup_10.x | bash -
#RUN curl -sL https://deb.nodesource.com/setup_8.x | bash -
#RUN apt install nodejs
#RUN node -v
#RUN npm -v
#RUN npm i webpack @babel/core babel-loader @babel/preset-env @babel/preset-react \
#          babel-plugin-transform-class-properties react react-dom prop-types weak-key --save-dev


EXPOSE 8000