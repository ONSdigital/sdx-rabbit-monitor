FROM onsdigital/flask-crypto-queue

COPY rabbit_monitor.py /app/rabbit_monitor.py
COPY requirements.txt /app/requirements.txt
COPY settings.py /app/settings.py
COPY wsgi.py /app/wsgi.py
COPY startup.sh /app/startup.sh

WORKDIR /app/

EXPOSE 5000

RUN pip3 install --no-cache-dir -U -r /app/requirements.txt

ENTRYPOINT ./startup.sh
