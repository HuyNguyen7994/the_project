sudo yum update -y
sudo yum install htop -y

# Install Erlang
sudo yum install https://github.com/rabbitmq/erlang-rpm/releases/download/v26.2.2/erlang-26.2.2-1.el7.x86_64.rpm -y

# Install RabbitMQ
sudo yum install https://github.com/rabbitmq/rabbitmq-server/releases/download/v3.12.13/rabbitmq-server-3.12.13-1.el8.noarch.rpm -y

# Start as service and enable autostart
sudo service rabbitmq-server start
sudo chkconfig rabbitmq-server on