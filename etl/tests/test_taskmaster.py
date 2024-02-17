import os
import pytest
from etl import taskmaster
import pika
from pika.spec import Basic
from pika.spec import BasicProperties
from pika.channel import Channel
from logging import getLogger

logger = getLogger(__name__)


def get_message(
    channel: Channel, method: Basic.Deliver, properties: BasicProperties, body: bytes
) -> str:
    message = body.decode("utf-8")
    return message


@pytest.fixture(scope="package", autouse=True)
def os_env():
    os.environ["RABBITMQ_HOST"] = "localhost"
    os.environ["RABBITMQ_PORT"] = "5672"


def test_rabbitmq():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=os.getenv("RABBITMQ_HOST"),
            port=os.getenv("RABBITMQ_PORT"),
        )
    )
    producer_channel = connection.channel()
    producer_channel.queue_declare(queue="run_etl")
    producer_channel.basic_publish(exchange="", routing_key="etl_run", body="abc")

    # consumer_channel = taskmaster.create_channel()
    # message = taskmaster.consume_message(consumer_channel, "run_etl", get_message)
    # assert message
