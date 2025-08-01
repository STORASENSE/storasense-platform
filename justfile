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

restart:
    echo "Restarting the application..."
    just stop
    just start

logs:
    echo "Displaying logs..."
    docker-compose logs -f

enter-db:
    docker exec -it timescaledb psql -U postgres -W

logs-app:
    docker-compose logs -f app
