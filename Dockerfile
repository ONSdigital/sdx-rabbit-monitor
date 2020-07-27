# TODO: switch to FROM onsdigital/flask-crypto-queue, py 3.8 version
FROM python:3.8

ENV BUILD_PACKAGES="curl build-essential python3-dev ca-certificates libssl-dev libffi-dev"
ENV PACKAGES="git gcc make build-essential python3-dev python3-reportlab"

ADD requirements.txt /crypto/requirements.txt

RUN apt-get update && apt-get install -y $BUILD_PACKAGES $PACKAGES \
    && pip3 install --no-cache-dir -U -I -r /crypto/requirements.txt \
	&& rm -rf /var/lib/apt/lists/*

COPY rabbit_monitor.py /app/rabbit_monitor.py
COPY requirements.txt /app/requirements.txt
COPY settings.py /app/settings.py
COPY wsgi.py /app/wsgi.py
COPY startup.sh /app/startup.sh

WORKDIR /app/

EXPOSE 5000

RUN pip3 install --no-cache-dir -U -r /app/requirements.txt

ENTRYPOINT ./startup.sh
