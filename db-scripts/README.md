This directory contains scripts regarding the database.

- **db-restore**: Collection of scripts to restore the database. For executing instructions, see the **README.md** in the directory.
- **db-init.sh**: Script to initialize the database - do not execute manually.
- **reset-app.sh**: Script to reset the application-database within the docker-container - run manually when switching between different environments (e.g. DEV => PROD). For running execute:
    ```bash
    docker compose exec timescaledb /docker-entrypoint-initdb.d/reset-app-db.sh
    ```
  or just with just:
    ```bash
    just reset-db
    ```
