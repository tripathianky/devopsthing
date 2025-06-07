# Docker Learning Guide

## Projects
- Hello World - Java, JavaScript and Python
- 2 Microservices - Currency Exchange and Currency Conversion

## Steps
1. Docker and DevOps - Installation and Introduction
2. Your First Docker Usecase
3. Important Docker Concepts - Registry, Repository, Tag, Image and Container
4. Playing with Docker Images - Java, JavaScript and Python
5. Playing with Docker - Detached Mode and Logs
6. Playing with Docker Images and Containers
7. Understanding Docker Architecture - Docker Client, Docker Engine
8. Understanding Docker Popularity - My 3 Top Reasons
9. Learning Docker Images - Commands
10. Learning Docker Containers - Commands
11. Learning Docker Commands - system and stats
12. Building Docker Images for Python Application
13. Understanding creation of Docker Images in Depth
14. Pushing Python App Docker Image to Docker Hub
15. Building and Pushing Docker Image for Node JavaScript App
16. Building and Pushing Docker Image for Java Application
17. Building Efficient Docker Images - Improving Layer Caching
18. Understanding ENTRYPOINT vs CMD
19. Docker and Microservices - Quick Start
20. Introduction to Microservices - CE and CC
21. Running Microservices as Docker Containers
22. Using Docker Link to Connect Microservices
23. Using Custom Networking to Connect Microservices
24. Using Docker Compose to Simplify Microservices Launch
25. Understanding Docker Compose further

## Docker Hub Repositories
- https://hub.docker.com/u/in28min
- https://hub.docker.com/r/in28min/hello-world-java
- https://hub.docker.com/r/in28min/hello-world-python
- https://hub.docker.com/r/in28min/hello-world-nodejs

## Common Docker Commands
```bash
docker --version
docker run -p 5000:5000 in28min/hello-world-python:0.0.1.RELEASE
docker run -d -p 5000:5000 in28min/hello-world-nodejs:0.0.1.RELEASE
docker logs <container_id>
docker images
docker container ls -a
docker container stop <container_id>
docker pull mysql
docker search mysql
docker image history <image_id>
docker image inspect <image_id>
docker image remove <image_name:tag>
docker container rm <container_id>
docker container pause <container_id>
docker container unpause <container_id>
docker container inspect <container_id>
docker container prune
docker system
docker system df
docker system info
docker system prune -a
docker top <container_id>
docker stats <container_id>
docker container run -p 5000:5000 -d -m 512m in28min/hello-world-java:0.0.1.RELEASE
docker container run -p 5000:5000 -d -m 512m --cpu-quota=50000 in28min/hello-world-java:0.0.1.RELEASE
docker system events
```

## Build and Push Docker Images
```bash
# Python
cd /path/to/hello-world-python
docker build -t in28min/hello-world-python:0.0.2.RELEASE .
docker push in28min/hello-world-python:0.0.2.RELEASE

# Node.js
cd ../hello-world-nodejs/
docker build -t in28min/hello-world-nodejs:0.0.2.RELEASE .
docker push in28min/hello-world-nodejs:0.0.2.RELEASE

# Java
cd ../hello-world-java/
docker build -t in28min/hello-world-java:0.0.2.RELEASE .
docker push in28min/hello-world-java:0.0.2.RELEASE
```

## Microservices Containers
```bash
docker run -d -p 8000:8000 --name=currency-exchange in28min/currency-exchange:0.0.1-RELEASE
docker run -d -p 8100:8100 --name=currency-conversion in28min/currency-conversion:0.0.1-RELEASE
```

## Docker Networking
```bash
docker network ls
docker network inspect bridge
docker network create currency-network
docker run -d -p 8000:8000 --name=currency-exchange --network=currency-network in28min/currency-exchange:0.0.1-RELEASE
docker run -d -p 8100:8100 --env CURRENCY_EXCHANGE_SERVICE_HOST=http://currency-exchange --name=currency-conversion --network=currency-network in28min/currency-conversion:0.0.1-RELEASE
```

## Docker Compose
```bash
docker-compose --version
cd /path/to/microservices
docker-compose up
docker-compose up -d
docker-compose down
docker-compose config
docker-compose images
docker-compose ps
docker-compose top
```

## Host Networking on Docker (Linux only)
- https://docs.docker.com/network/host/
