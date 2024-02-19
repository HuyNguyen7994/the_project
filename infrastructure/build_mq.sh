sudo yum update -y
sudo yum install htop -y

# Install Erlang
sudo yum install https://github.com/rabbitmq/erlang-rpm/releases/download/v21.3.4/erlang-21.3.4-1.el7.x86_64.rpm -y

# Install RabbitMQ
sudo yum install https://dl.bintray.com/rabbitmq/all/rabbitmq-server/3.7.14/rabbitmq-server-3.7.14-1.el7.noarch.rpm -y

# Allow remote connections
# @see: https://www.rabbitmq.com/access-control.html
echo 'loopback_users = none' | sudo tee -a /etc/rabbitmq/rabbitmq.conf

# Increase the maximum number of files for RabbitMQ
# @see: https://stackoverflow.com/questions/46240032/rabbitmq-file-descriptor-limit
sudo vim /usr/lib/systemd/system/rabbitmq-server.service
# set
# [Service]
# LimitNOFILE=65536

sudo systemctl daemon-reload

# Enable RabbitMQ Management Console
/usr/lib/rabbitmq/bin/rabbitmq-plugins enable rabbitmq_management

# Start as service and enable autostart
sudo service rabbitmq-server start
sudo chkconfig rabbitmq-server on