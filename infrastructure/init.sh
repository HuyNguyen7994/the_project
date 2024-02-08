#!/bin/bash
# Update package lists and install dependencies
sudo yum update -y
sudo yum install -y git

# Install Node.js 18
curl -fsSL https://rpm.nodesource.com/setup_18.x | sudo bash -
sudo yum install -y nodejs

# Install Pip
sudo yum install python3-pip -y