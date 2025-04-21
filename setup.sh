#!/bin/bash

echo "INSTALLATION"
sudo apt-get update && \
	sudo apt-get upgrade -y && \
	sudo apt-get install git -y && \
	sudo apt-get install nginx -y && \
	sudo apt-get install docker.io -y

echo "CLONING GIT"
git clone https://$1:$2@github.com//gabriGutiz/url-shortener.git

mv layers-case/api .
mv layers-case/site .

echo "BUILDING DOCKER"
sudo docker build \
    --build-arg EKS_ENV=prd \
    --build-arg MONGO_CONN=$3 \
    --build-arg PORT=8000 \
    -t api ./api
sudo docker build -t site ./site

echo "RUNNING DOCKER"
sudo docker run -d -p 8001:8000 api
sudo docker run -d -p 8000:80/tcp site

sudo mv -f layers-case/nginx.conf /etc/nginx/sites-available/default
sudo rm -rf layer-case

echo "NGINX"
sudo systemctl restart nginx
nginx -t
