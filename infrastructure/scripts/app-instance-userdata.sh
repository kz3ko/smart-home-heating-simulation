##!/bin/sh
#
#sudo apt-get update
#sudo apt-get install \
#		 ca-certificates \
#		 curl \
#		 gnupg \
#		 lsb-release
#
#sudo mkdir -p /etc/apt/keyrings
#curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
#
#echo \
#"deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
#$(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
#
#sudo apt-get update
#sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin
#
#USER="ssm-user"
#
#sudo groupadd docker
#sudo usermod -aG docker $USER

# Configure SSM agent and environment
echo "Configuring SSM agent and environment ..."

#systemctl daemon-reload && systemctl restart amazon-ssm-agent

export STATUS="DONE"
