FROM python:3.11

WORKDIR /usr/src/app/
COPY rabbitmq1.py /usr/src/app/

RUN pip install --no-cache-dir pika
CMD ["python", "rabbitmq1.py"]
