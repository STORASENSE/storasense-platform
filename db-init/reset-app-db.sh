#!/bin/bash
set -e

APP_DB_NAME=${POSTGRES_DB:-storasense_app_data}

echo "INFO: Resetting application database '$APP_DB_NAME'..."

# Connect to psql and execute the SQL commands
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "postgres" <<-EOSQL
    -- Terminate all active connections to the app DB, BUT NOT THE OWN CONNECTION
    SELECT pg_terminate_backend(pid)
    FROM pg_stat_activity
    WHERE datname = '$APP_DB_NAME'
      AND pid <> pg_backend_pid(); -- This is the crucial addition

    -- Drop the database
    DROP DATABASE IF EXISTS $APP_DB_NAME;

    -- Recreate the database
    CREATE DATABASE $APP_DB_NAME WITH OWNER = ${POSTGRES_USER};
EOSQL

echo "SUCCESS: Database '$APP_DB_NAME' has been successfully reset."
