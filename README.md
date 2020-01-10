# arkive ... your pages forever

## Introduction

## Installation
To install ARkive you will need to have docker and docker-compose installed (https://docs.docker.com/compose/install/)

To build your own image:

```buildoutcfg
./build_docker.sh
```

To run:

```buildoutcfg
docker-compose up
```

You can then visit http://localhost to run locally or you can setup using nginx using the hosting file contained in the config folder

###Hosting on a server
You can deploy this docker instance on a remote server in the same way you deploy any docker instance.

If you want to change the domain name used You will need to edit the Dockerfile and change the DJANGO_ALLOWED_HOSTS to a string containing all the domains you want this app to respond to. If you have multiple domains you can separte each on with a space character and they will be included.

You will also need to add the domain to the ```config/nginx/conf.d/arkive_nginx.conf``` file and finally run the ```build_docker.sh``` script again before you run docker-compose again
