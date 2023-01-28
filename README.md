# api.frankwiles.com

## Overview

A Django project starter kit

## Local Development Setup

This project will use Python 3.11, Docker, and Docker Compose.

Make a Python 3.11.x virtualenv.

Copy .env-dist to .env and adjust values to match your local environment:

```shell
$ cp .env-dist .env
$ cp docker-compose.override.yml-dist docker-compose.override.yml
```

Then run:

```shell
# rebuild our services
$ docker compose build

# start our services
$ docker compose up

# start our services with daemon mode
$ docker compose up -d

# to run database migrations
$ docker compose run --rm web python manage.py migrate

# to create a superuser
$ docker compose run --rm web python manage.py createsuperuser

# to create database migrations
$ docker compose run --rm web python manage.py makemigrations
```

This will create the Docker image, install dependencies, start the services defined in `docker-compose.yml`, and start the web server.

### Cleaning up

To shut down our database and any long-running services, we shut everyone down using:

```shell
$ docker compose down
```

### Running with Celery and Redis

AlphaKit ships with Celery and Redis support, but they are off by default. To rebuild our image with support, we need to pass the `--profile celery` option to Docker Compose via:

```shell
# rebuild our services
$ docker compose --profile celery build

# start our services
$ docker compose --profile celery up

# start our services with daemon mode
$ docker compose --profile celery up -d

# stop and unregister all of our services
$ docker compose --profile celery down
```

## Running the tests

To run the tests, execute:

```shell
$ docker compose run --rm web pytest
```

## Deploying

TDB

## Production Environment Considerations

TDB
