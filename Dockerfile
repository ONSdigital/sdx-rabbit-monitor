FROM onsdigital/flask-crypto-queue

COPY rabbit_monitor.py /app/rabbit_monitor.py
COPY requirements.txt /app/requirements.txt
COPY settings.py /app/settings.py
COPY wsgi.py /app/wsgi.py
COPY startup.sh /app/startup.sh

WORKDIR /app/


EXPOSE 5000

RUN apt-get update -y
RUN apt-get upgrade -y
RUN apt-get install -yq git gcc make build-essential python3-dev python3-reportlab
RUN git clone -b 0.7.0 https://github.com/ONSdigital/sdx-common.git
RUN pip3 install ./sdx-common

RUN pip3 install --no-cache-dir -U -r /app/requirements.txt

ENTRYPOINT ./startup.sh
