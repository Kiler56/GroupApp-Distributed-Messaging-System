import pika
import json

def publish_event(queue, message):
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='127.0.0.1')
        )

        channel = connection.channel()

        channel.queue_declare(queue=queue)

        channel.basic_publish(
            exchange='',
            routing_key=queue,
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2  
            )
        )

        print("Evento enviado a RabbitMQ")

        connection.close()

    except Exception as e:
        print("Error RabbitMQ:", e)

def consume_messages():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='127.0.0.1')
    )

    channel = connection.channel()

    channel.queue_declare(queue="messages")

    def callback(ch, method, properties, body):
        message = json.loads(body)
        print("📩 Evento recibido:", message)

        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(
        queue="messages",
        on_message_callback=callback
    )

    print("🟢 Esperando mensajes...")
    channel.start_consuming()