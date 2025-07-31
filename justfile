#!/usr/bin/env just --justfile

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
