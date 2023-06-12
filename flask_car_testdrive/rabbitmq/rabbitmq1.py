import json
import os.path

import pika

credentials = pika.PlainCredentials(username=os.environ.get('RABBIT_USER'), password=os.environ.get('RABBIT_PASSWORD'))
connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq', credentials=credentials))
channel = connection.channel()
channel.queue_declare(queue='hello')


def callback(ch, method, properties, body):
    body = json.loads(body)

    print(body['subject'], body['sender'], body['recipients'], body['body'], body['attachments'])


channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
