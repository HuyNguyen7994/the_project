#!/bin/bash
sudo su
sudo yum install -y nginx

# Start Nginx and enable it to start on boot
sudo systemctl start nginx
sudo systemctl enable nginx

# Configure Nginx as a reverse proxy for port 8080
sudo tee /etc/nginx/conf.d/reverse-proxy.conf > /dev/null <<EOF
server {
    listen 8080;

    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

# Test Nginx configuration and reload
sudo nginx -t && sudo systemctl reload nginx

echo "Nginx installation and reverse proxy configuration completed."

# Build Backend
cd /the_project/backend/app
pip install .
screen -dmS AppBackEnd uvicorn app.main:app --port 8080