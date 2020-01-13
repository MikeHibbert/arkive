#!/bin/bash

docker-compose build
docker-compose run arkive /code/manage.py collectstatic --no-input