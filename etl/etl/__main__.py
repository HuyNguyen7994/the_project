from etl.taskmaster import create_channel, consume_message, execute_etl_script

if __name__ == "__main__":
    channel = create_channel()
    consume_message(channel, "run_etl", execute_etl_script)
    channel.start_consuming()
