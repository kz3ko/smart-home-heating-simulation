#! /bin/bash

# Download to machine with "aws s3 cp s3://smart-home-simulation-bucket-eu-west-1/setup_script.sh setup_script.sh".
# To be run on EC2 with "sudo bash setup_script.sh" command.

# Install docker.
yum update
yum install docker

usermod -aG docker ssm-user

# Install docker-compose.
rm /usr/local/bin/docker-compose
curl -L https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# Enable and start docker service.
systemctl enable docker.service
systemctl start docker.service

# Copy app code from S3.
cd
aws s3 cp s3://smart-home-simulation-bucket-eu-west-1/app.zip app.zip
unzip app.zip -d .
rm -rf app.zip

# Generate SSL certificates.
cd app
bash generate_certificates.sh

# Start app.
docker-compose up -d --build
