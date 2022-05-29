# Put this on S3 and download to machine with aws s3 cp s3://smart-home-simulation-bucket-eu-west-1/setup_script.sh setup_script.sh
# then run with "sudo source setup_script.sh".

# Install docker
yum update
yum install docker

usermod -aG docker ssm-user

# Install docker-compose
rm /usr/local/bin/docker-compose
curl -L https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# Enable and start docker service
systemctl enable docker.service
systemctl start docker.service


cd
aws s3 cp s3://smart-home-simulation-bucket-eu-west-1/app.zip app.zip
unzip app.zip -d .
rm -rf app.zip

cd app
aws s3 cp s3://smart-home-simulation-bucket-eu-west-1/ssl_certificates.zip ssl_certificates.zip
unzip ssl_certificates.zip -d .cert
rm -rf ssl_certificates.zip

docker-compose up -d --build
