# arkive ... your pages forever

## Introduction

## Installation
To install ARkive you will need to have docker and docker compose installed (https://docs.docker.com/compose/install/)

To build your own image:

```buildoutcfg
docker build -t arkive . Dockerfile
```

To run:

```buildoutcfg
docker run arkive
```

You can then visit http://localhost:8000 to run locally or you can setup using nginx using the hosting file contained in the config folder

