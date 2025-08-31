#!/bin/bash

# Check if backup file parameter is provided
if [ $# -eq 0 ]; then
    echo "Error: Backup file parameter is required"
    echo "Usage: $0 <backup_file>"
    exit 1
fi

BACKUP_FILE="$1"
VOLUME_NAME="storasense-platform_storasense_data_volume"
DB_SERVICE_NAME="timescaledb"
BACKUP_DIR="./storasense_data_volume_backup"

BACKUP_FILE_PATH="$BACKUP_DIR/$BACKUP_FILE"

if [ ! -f "$BACKUP_FILE_PATH" ]; then
    echo "Error: The backup file '$BACKUP_FILE_PATH' was not found."
    exit 1
fi

# Get backup file size
BACKUP_SIZE=$(stat -c%s "$BACKUP_FILE_PATH")
BACKUP_SIZE_MB=$((BACKUP_SIZE / 1024 / 1024))
echo "Backup file size: ${BACKUP_SIZE_MB} MB"

echo "WARNING: This operation will delete all current data from '$DB_SERVICE_NAME' and overwrite it with the backup."
read -p "Are you sure you want to continue? (yes/no): " confirmation
if [ "$confirmation" != "yes" ]; then
    echo "Operation cancelled."
    exit 0
fi

echo "1/5: Stopping all services..."
docker compose down

echo "2/5: Removing old data volume '$VOLUME_NAME'..."
docker volume rm "$VOLUME_NAME" 2>/dev/null

echo "3/5: Creating new, empty data volume '$VOLUME_NAME'..."
docker volume create "$VOLUME_NAME"

echo "4/5: Restoring data from '$BACKUP_FILE'..."
CURRENT_DIR=$(pwd)

# Check Backup Directory
echo "Checking backup contents..."
docker run --rm -v "${CURRENT_DIR}/${BACKUP_DIR}:/backup" busybox sh -c "tar -tzf '/backup/$BACKUP_FILE' | head -10"

# Easy approach to restore
echo "Extracting and restoring data..."
docker run --rm -v "${VOLUME_NAME}:/data" -v "${CURRENT_DIR}/${BACKUP_DIR}:/backup" busybox sh -c "tar -xzf '/backup/$BACKUP_FILE' -C /tmp && ls -la /tmp/ && cp -r /tmp/backup/storasense_data_volume/* /data/ && ls -la /data/ && du -sh /data"

if [ $? -ne 0 ]; then
    echo "Error: Basic restore failed, trying alternative method..."

    docker run --rm -v "${VOLUME_NAME}:/data" -v "${CURRENT_DIR}/${BACKUP_DIR}:/backup" busybox sh -c "
        tar -xzf '/backup/$BACKUP_FILE' -C /tmp
        echo 'Extracted contents:'
        find /tmp -type d -name '*storasense*'
        find /tmp -name 'postgresql.conf'

        if [ -d '/tmp/backup/storasense_data_volume' ]; then
            cp -r /tmp/backup/storasense_data_volume/* /data/
            echo 'Copied from backup/storasense_data_volume'
        else
            PGDIR=\$(find /tmp -name 'postgresql.conf' | head -1 | xargs dirname)
            if [ -n \"\$PGDIR\" ]; then
                cp -r \"\$PGDIR\"/* /data/
                echo \"Copied from \$PGDIR\"
            fi
        fi

        ls -la /data/
    "
fi

# Check if PostgreSQL files are present
echo "Verifying PostgreSQL files..."
docker run --rm -v "${VOLUME_NAME}:/data" busybox sh -c "ls -la /data/ && if [ -f /data/postgresql.conf ]; then echo 'SUCCESS: postgresql.conf found'; else echo 'WARNING: postgresql.conf not found'; fi"

echo "5/5: Restarting all services..."
docker compose up -d

echo "Restore completed!"