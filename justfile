#!/usr/bin/env just --justfile

build:
    echo "Building the application..."
    docker-compose up --build

start:
    echo "Starting the application..."
    docker-compose up -d

start-scaled:
    echo "Starting the application with scaling..."
    docker-compose up -d --scale app=3

stop:
    echo "Stopping the application..."
    docker-compose down

restart:
    echo "Restarting the application..."
    just stop
    just start

reset-all:
    just stop
    docker system prune
    docker image prune -a

reset-db:
    docker compose exec timescaledb /docker-entrypoint-initdb.d/reset-app-db.sh

logs:
    echo "Displaying logs..."
    docker-compose logs -f
