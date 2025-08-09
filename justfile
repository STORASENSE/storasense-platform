#!/usr/bin/env just --justfile

build:
    echo "Building the application..."
    docker-compose up --build

start:
    echo "Starting the application..."
    docker-compose up -d

stop:
    echo "Stopping the application..."
    docker-compose down

softreset:
    just stop
    docker system prune

prune-builds:
    echo "Pruning old builds..."
    docker container prune

prune-images:
    echo "Pruning old images..."
    docker image prune -a

restart:
    echo "Restarting the application..."
    just stop
    just start

logs:
    echo "Displaying logs..."
    docker-compose logs -f

delete-volume:
    echo "Deleting the database..."
    docker volume rm timescaledb_data

logs-app:
    docker-compose logs -f app
