#!/bin/bash
set -e

# Initialize the database with a user and a database for Keycloak
psql --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE USER ${POSTGRES_KC_DB_USER} WITH PASSWORD '${POSTGRES_KC_DB_PASSWORD}';
    CREATE DATABASE ${POSTGRES_KC_DB_NAME} WITH OWNER = ${POSTGRES_KC_DB_USER};
EOSQL

# Connects to application database and actovates TimescaleDB extension
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE EXTENSION IF NOT EXISTS timescaledb;
EOSQL
