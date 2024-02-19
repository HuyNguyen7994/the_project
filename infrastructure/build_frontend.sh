#!/bin/bash
sudo su
yum install httpd -y

# Build Frontend
export VITE_BACKEND_URL=http://3.82.212.198/
cd /the_project/frontend/frontend
npm i
npm run build
mkdir -p /var/www/html
cp -a /the_project/frontend/frontend/dist/. /var/www/html