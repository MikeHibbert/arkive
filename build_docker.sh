#!/bin/bash

docker-compose build
docker-compose run web /code/manage.py collectstatic --no-input