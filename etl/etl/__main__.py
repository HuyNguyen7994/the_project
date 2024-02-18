from etl.taskmaster import create_channel, consume_message, execute_etl_script
from loguru import logger

if __name__ == "__main__":
    channel = create_channel()
    consume_message(channel, "run_etl", execute_etl_script)
    logger.info("Start listening for ETL command...")
    channel.start_consuming()
