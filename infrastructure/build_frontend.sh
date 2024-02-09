#!/bin/bash
sudo su
yum install httpd -y

# Build Frontend
export VITE_BACKEND_URL=http://127.0.0.1:8080/
cd /the_project/frontend/frontend
npm i
npm run build
cp -a /the_project/frontend/frontend/dist/. /var/www/html
service httpd start