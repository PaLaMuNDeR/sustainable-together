# .-= The part for Django =-.\
FROM python:3.6

ENV PYTHONBUFFERED 1
ENV DJANGO_ENV dev
ENV DOCKER_CONTAINER 1

COPY web/st/back-end/requirements.txt /web/requirements.txt
RUN pip3 install -U pip
RUN pip3 install -r /web/requirements.txt
COPY config/postgres /

COPY web/st/back-end /web/
WORKDIR /web/

#Add the library for compiling the translations
#RUN apt-get update && apt-get install -y gettext \
#    vim \
#    python-pip python-dev build-essential \
#    gunicorn

RUN adduser --disabled-password --gecos '' myuser


EXPOSE 8000