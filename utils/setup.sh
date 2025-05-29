#!/bin/bash

echo "INSTALLATION"
sudo apt-get update && \
	sudo apt-get upgrade -y && \
	sudo apt-get install git -y && \
	sudo apt-get install nginx -y && \
	sudo apt-get install docker.io -y

sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

echo "CLONING GIT"
git clone https://$1:$2@github.com//gabriGutiz/room-guard.git

echo "BUILDING DOCKER"
sudo docker-compose up -d

#echo "NGINX"
#sudo systemctl restart nginx
#nginx -t
