#Configurar swarm con aws

#Crear instancias de EC2
export MACHINE_DRIVER=amazonec2
export AWS_ACCESS_KEY_ID=
export AWS_SECRET_ACCESS_KEY=
export AWS_DEFAULT_REGION=us-west-2
# export AWS_INSTANCE_TYE=m3.large
for N in $(seq 1 5); do
	docker-machine create aws-node$N                            
	docker-machine ssh aws-node$N sudo usermod -aG docker ubuntu
done   


# Abrir puertos
aws ec2 authorize-security-group-ingress --group-name docker-machine --protocol -1 --cidr 0.0.0.0/0 


## Iniciar SWARM
eval $(docker-machine env aws-node1)

docker swarm init --advertise-addr $(docker-machine ip aws-node1)

TOKEN=$(docker swarm join-token -q manager)
for N in $(seq 2 5); do
  eval $(docker-machine env aws-node$N)
  docker swarm join --token $TOKEN $(docker-machine  ip aws-node1):2377
done
eval $(docker-machine env aws-node1)

## iniciar servicio 
# docker service create --name registry --publish 5000:5000 registry:2


