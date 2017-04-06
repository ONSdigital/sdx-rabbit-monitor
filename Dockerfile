FROM onsdigital/flask-crypto-queue

ADD rabbit_monitor /app/rabbit_monitor
ADD rabbit_monitor.py /app/rabbit_monitor.py
ADD requirements.txt /app/requirements.txt
ADD startup.sh /app/startup.sh

# set working directory to /app/
WORKDIR /app/

EXPOSE 5000

RUN pip3 install --no-cache-dir -U -r /app/requirements.txt

ENTRYPOINT ./startup.sh
