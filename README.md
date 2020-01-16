# Arkive ... your pages forever

## Introduction
Arkive lets you choose two different ways of storing your webpages on the permaweb. You can store the page text on its own
as a readable version of the page or include images too. Or you can choose to compile the whole page into a bundle that can
be viewed in its current state including styling and javascript behaviours as well as images. As well as that Arkive will 
generate Open Graph Tags so that it will be displayed correctly when shared on social media sites.

As Arkive commits transactions to the Arweave permaweb please be aware that each page stored costs the price of the transaction 
to save it! So feel free to contribute to its upkeep with a small donation in ARWeave Coin to the address on the site. That way the service 
with be around for years to come!

Wallet Address Currently Used: ```h-Bgr13OWUOkRGWrnMT0LuUKfJhRss5pfTdxHmNcXyw```

Live service: ```http://www.arkive.online```

## Installation
To install ARkive you will need to have docker and docker-compose installed (https://docs.docker.com/compose/install/)

To build your own image:

```buildoutcfg
docker-compose build
```

To run:

```buildoutcfg
docker-compose up 
```

You can then visit http://localhost to run locally or you can setup using nginx using the hosting file contained in the config folder

###Hosting on a server
You can deploy this docker instance on a remote server by intalling docker-ce and docker-compose on the server then copy
the code below into a file ```docker-compose.yml``` to your servers home folder:

```buildoutcfg
version: '3'

services:
  arkive:
    image: mickeysofine1972/arkive
    command: gunicorn arkive.wsgi:application --bind 0.0.0.0:8000
    volumes:
      - static_volume:/code/arkive/staticfiles
      - media_volume:/code/arkive/media
    networks:
      - nginx_network
    restart: always

  nginx:
    image: mickeysofine1972/arkive-nginx
    ports:
      - 80:80
    volumes:
      - static_volume:/code/arkive/staticfiles
      - media_volume:/code/arkive/media
    depends_on:
      - arkive
    networks:
      - nginx_network
    restart: always

  redis:
    image: redis:latest
    hostname: redis
    restart: always
    networks:
      - redis
    environment:
      - ALLOW_EMPTY_PASSWORD=yes

  celery:
    image: mickeysofine1972/arkive-celery
    command: celery -A arkive worker --app=arkive.celery:app --loglevel=debug
    depends_on:
      - redis
    networks:
      - redis

networks:
  redis:
  nginx_network:
    driver: bridge

volumes:
  static_volume:
  media_volume:
```

Once you've saved your file you can simply run ```docker-compose up -d``` and the system will run!

#####Note:
If you change the domain name from arkive.online to something else you will need to edit the ```server_name``` option in the config/nginx/conf.d/arkive_nginx.conf file and rebuild your docker images