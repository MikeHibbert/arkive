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
You can deploy this docker instance on a remote server by intalling docker-ce and docker-compose on the server then copy
the contents of ```docker-compose.yml``` to your home folder then:

Remove the build lines:
```buildoutcfg
build:
      context: .
      dockerfile: ./images/arkive/Dockerfile

... and the later build lines too ...

build:
      context: .
      dockerfile: ./images/nginx/Dockerfile
```

Once they are removed you can simply run ```docker-compose up -d``` and the system will run!

#####Note:
If you change the domain name from arkive.online to something else you will need to edit the ```server_name``` option in the config/nginx/conf.d/arkive_nginx.conf file and rebuild your docker images