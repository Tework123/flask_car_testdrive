import json
from app import create_app
from app.user.email import send_email
from config import DevelopmentConfig
import pika

# this module must turn on determine from main flask app, this it rabbitmq worker for listen message
app = create_app(DevelopmentConfig)
app.app_context().push()

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='hello')


def callback(ch, method, properties, body):
    body = json.loads(body)
    send_email(body['subject'], body['sender'], body['recipients'], body['body'], body['attachments'])


channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
