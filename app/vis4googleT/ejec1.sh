#!/bin/bash

. ./vamb.sh

docker-machine create awsn00                            
docker-machine ssh awsn00 sudo usermod -aG docker ubuntu

aws ec2 authorize-security-group-ingress --group-name docker-machine --protocol -1 --cidr 0.0.0.0/0 

#eval $(docker-machine env awsn00)
docker info | grep ^Name

docker-machine ssh awsn00 git clone https://github.com/adfmb/vis4googleT.git
docker-machine scp -r vamb.sh awsn00:/home/ubuntu/vis4googleT/ambiente/app/vamb.sh
docker-machine ssh awsn00 chmod u+x vis4googleT/execn1_01.sh
docker-machine ssh awsn00 ./vis4googleT/execn1_01.sh #Este script termina con el swarm inicializado

eval $(docker-machine env awsn00)
docker info | grep ^Name
docker network create --driver overlay vis4g
docker info | grep ^Name
docker network ls

eval $(docker-machine env -u)
docker info | grep ^Name
docker-machine ssh awsn00 docker stack deploy -c vis4googleT/swarm-docker-compose.yml vis4g


echo "vistar $(docker-machine  ip awsn00):3838"


