from scripts.extract_from_gsheet import main as extract_from_gsheet
import pika
from pika.channel import Channel
from pika.spec import Basic
from pika.spec import BasicProperties
from loguru import logger
from time import sleep

commands_map = {
    "gsheet": extract_from_gsheet,
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


with pika.BlockingConnection(
    pika.ConnectionParameters(
        host="localhost",
        port="5672",
    )
) as connection:
    channel = connection.channel()
    channel.queue_declare(queue="run_etl")
    channel.basic_consume(
        queue="run_etl", auto_ack=True, on_message_callback=execute_etl_script
    )
    channel.start_consuming()
