import os
import pika
from etl.source import aqicn_main
from pika.channel import Channel
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic
from pika.spec import BasicProperties
from loguru import logger
from time import sleep

commands_map = {
    "aqicn": aqicn_main,
}


def execute_etl_script(
    channel: Channel, method: Basic.Deliver, properties: BasicProperties, body: bytes
):
    command = body.decode("utf-8")
    if command not in commands_map:
        logger.error(f"Command {command} is invalid. Skipped.")
        return
    logger.info(f"Executing {command} job")
    commands_map[command]()
    sleep(5)
    logger.info(f"Finished execution of {command} job")
    return


def create_channel() -> BlockingChannel:
    with pika.BlockingConnection(
        pika.ConnectionParameters(
            host=os.getenv("RABBITMQ_HOST"),
            port=os.getenv("RABBITMQ_PORT"),
        )
    ) as connection:
        channel = connection.channel()
        channel.queue_declare(queue="run_etl")
        channel.basic_consume(
            queue="run_etl", auto_ack=True, on_message_callback=execute_etl_script
        )
        return channel


if __name__ == "__main__":
    channel = create_channel()
    channel.start_consuming()
