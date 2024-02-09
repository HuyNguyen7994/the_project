#!/bin/bash
sudo su
yum install -y nginx

# Start Nginx and enable it to start on boot
systemctl start nginx
systemctl enable nginx

# Configure Nginx as a reverse proxy for port 8080
tee /etc/nginx/conf.d/reverse-proxy.conf > /dev/null <<EOF
server {
    listen 80;

    location /api/ {
        proxy_pass http://127.0.0.1:8080/;
    }

    location / {
        root /var/www/html;
    }
}
EOF

# Test Nginx configuration and reload
nginx -t && systemctl reload nginx

echo "Nginx installation and reverse proxy configuration completed."

# Build Backend
cd /the_project/backend/app
pip install .
screen -dmS AppBackEnd uvicorn app.main:app --port 8080