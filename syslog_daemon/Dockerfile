FROM python:3.12-slim
RUN apt-get update && \
    apt-get install -y freetds-dev && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir pymssql

COPY syslog_server.py /app/

WORKDIR /app

CMD ["python","-u","syslog_server.py"]
