import os
import json
import pika
from etl.source import aqicn_main
from pika.spec import Basic
from pika.spec import BasicProperties
from pika.channel import Channel
from pika.adapters.blocking_connection import BlockingChannel
from loguru import logger
from typing import Callable

commands_map = {
    "aqicn": aqicn_main,
}


def execute_etl_script(
    channel: Channel, method: Basic.Deliver, properties: BasicProperties, body: bytes
):
    body = json.loads(body)
    command = body["command"]
    payload = body["payload"]
    if command not in commands_map:
        logger.error(f"Command {command} is invalid. Skipped.")
        return
    logger.info(f"Executing {command} job")
    commands_map[command](payload)
    logger.info(f"Finished execution of {command} job")
    return


def create_channel() -> BlockingChannel:
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=os.getenv("RABBITMQ_HOST"),
            port=os.getenv("RABBITMQ_PORT"),
        )
    )
    channel = connection.channel()
    channel.queue_declare(queue="run_etl")
    return channel


def consume_message(
    channel: Channel,
    queue_name: str,
    on_message_callback: Callable[
        [Channel, Basic.Deliver, BasicProperties, bytes], None
    ],
):
    channel.basic_consume(
        queue=queue_name, auto_ack=True, on_message_callback=on_message_callback
    )
