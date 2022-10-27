import json
import logging
import os

import pika
import redis
from rich.logging import RichHandler


redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    decode_responses=True,
)

logging.basicConfig(
    level="INFO",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler()],
)


log = logging.getLogger(__name__)


def callback(ch, method, properties, body):
    """
    Callback function for RabbitMQ.

    Args:
        ch: Channel.
        method: Method.
        properties: Properties.
        body: Body.

    Returns:
        None.
    """

    data = json.loads(body.decode())
    log.info(
        f"Received data from RabbitMQ: {json.dumps(data, indent=4)}"
    )

    for key, value in data.items():
        redis_client.set(key, value)
        log.info(f"Stock {key} is saved to Redis!")

    ch.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == "__main__":
    host = os.getenv("RABBITMQ_HOST", "localhost")
    port = int(os.getenv("RABBITMQ_PORT", 5672))
    queue = os.getenv("RABBITMQ_QUEUE", "stocks")

    log.info(f"Connecting to RabbitMQ {host}:{port}")

    rabbit_connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=host, port=port)
    )

    log.info(f"Connected to RabbitMQ {host}:{port}")

    rabbit_channel = rabbit_connection.channel()
    rabbit_channel.queue_declare(queue=queue, durable=True)

    log.info(f"Queue {queue} is declared")

    rabbit_channel.basic_qos(prefetch_count=1)
    rabbit_channel.basic_consume(
        queue=queue, on_message_callback=callback
    )

    log.info(f"Waiting for messages from RabbitMQ")
    rabbit_channel.start_consuming()
