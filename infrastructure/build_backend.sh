#!/bin/bash
sudo yum install -y nginx

# Start Nginx
sudo systemctl start nginx

# Configure Nginx as a reverse proxy for port 8080
sudo tee /etc/nginx/conf.d/reverse-proxy.conf > /dev/null <<EOF
server {
    listen 80;

    location /api/ {
        proxy_pass http://127.0.0.1:8000/api/;
    }

    location / {
        root /var/www/html;
    }
}
EOF

# Test Nginx configuration and reload
sudo nginx -t && sudo systemctl reload nginx

# Build Backend
cd /the_project/backend/app
pip install .
nohup python3 -m backend
nohup python3 -m etl
