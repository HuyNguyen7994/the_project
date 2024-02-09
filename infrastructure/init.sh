#!/bin/bash
sudo su
# Update package lists and install dependencies
yum update -y
yum install -y git

# Install Node.js 18
curl -fsSL https://rpm.nodesource.com/setup_18.x | bash -
yum install -y nodejs

# Install Pip
yum install python3-pip -y

# Clone the Project
git clone https://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@github.com/HuyNguyen7994/the_project.git

