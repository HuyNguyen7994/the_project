#!/bin/bash
sudo su
yum install ngnix

# Build Backend
cd /the_project/backend/app
pip install .
screen -dmS AppBackEnd uvicorn app.main:app --port 8080