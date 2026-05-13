import pika
import json
import os
from dotenv import load_dotenv

load_dotenv()

RABBITMQ_HOST = os.getenv("RABBITMQ_URL", "localhost")

def publish_event(queue, message):
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=RABBITMQ_HOST)
        )

        channel = connection.channel()

        channel.queue_declare(queue=queue, durable=True)

        channel.basic_publish(
            exchange='',
            routing_key=queue,
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2  
            )
        )

        connection.close()

    except Exception as e:
        pass

def consume_messages():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST)
    )

    channel = connection.channel()

    channel.queue_declare(queue="messages", durable=True)

    def callback(ch, method, properties, body):
        message = json.loads(body)

        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(
        queue="messages",
        on_message_callback=callback
    )

    channel.start_consuming()
