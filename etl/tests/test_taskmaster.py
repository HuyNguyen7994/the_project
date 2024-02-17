import os
import pytest
from etl import taskmaster

@pytest.fixture(scope="package", autouse=True)
def os_env():
    os.environ["RABBITMQ_HOST"] = "localhost"
    os.environ["RABBITMQ_PORT"] = "5672"

def test_rabbitmq():
    consumer_channel = taskmaster.create_channel()
    assert consumer_channel


