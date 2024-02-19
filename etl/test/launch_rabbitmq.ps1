docker pull rabbitmq:3.12-management
docker run -p 5672:5672 -p 15672:15672 -e RABBITMQ_DEFAULT_USER=guest -e RABBITMQ_DEFAULT_PASS=guest --rm -d rabbitmq:3.12-management