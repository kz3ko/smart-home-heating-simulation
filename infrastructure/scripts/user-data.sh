Content-Type: multipart/mixed; boundary="//"
MIME-Version: 1.0

--//
Content-Type: text/cloud-config; charset="us-ascii"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit
Content-Disposition: attachment; filename="cloud-config.txt"

#cloud-config
cloud_final_modules:
- [scripts-user, always]

--//
Content-Type: text/x-shellscript; charset="us-ascii"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit
Content-Disposition: attachment; filename="userdata.txt"

#!/bin/bash
#sudo yum update
#sudo yum search docker
#sudo yum info docker
#sudo yum install docker
#
#USER="ssm-user"
#sudo usermod -aG docker $USER
#
#suwget https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)
#sudo mv docker-compose-$(uname -s)-$(uname -m) /usr/local/bin/docker-compose
#sudo chmod -v +x /usr/local/bin/docker-compose
#
#sudo systemctl enable docker.service
#sudo systemctl start docker.service

echo "Hello world" >> usr/bin/tmp/testfile.txt