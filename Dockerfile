FROM python:3.6.3

RUN apt-get update && \
        apt-get install -y libreoffice

RUN mkdir /psalms

WORKDIR /psalms

RUN python -m venv venv

COPY ./requirements.txt requirements.txt
RUN venv/bin/pip install -r requirements.txt

COPY ./tools /psalms/tools
COPY ./masters /psalms/masters
COPY ./scripts /psalms/scripts
