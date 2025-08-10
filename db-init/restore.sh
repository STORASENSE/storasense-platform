#!/bin/bash

# =================================================================
#  Configuration - Adjust these variables if needed
# =================================================================
# The name of the volume to be restored (from docker-compose.yml)
VOLUME_NAME="storasense_data_volume"
# The name of the database service using this volume
DB_SERVICE_NAME="timescaledb"
# The local folder where your backups are stored
BACKUP_DIR="./storasense_data_volume_backup"
# =================================================================


# Safety check: Verify that a backup filename was provided
if [ -z "$1" ]; then
    echo "Error: You must specify a filename for the backup."
    echo "Usage: ./restore.sh <backup-filename.tar.gz>"
    # Show the latest backup filename as a suggestion
    LATEST_BACKUP=$(ls -t ${BACKUP_DIR}/*.tar.gz 2>/dev/null | head -n 1)
    if [ ! -z "$LATEST_BACKUP" ]; then
        echo "Suggestion (latest backup): ./restore.sh $(basename $LATEST_BACKUP)"
    fi
    exit 1
fi

BACKUP_FILE=$1
BACKUP_FILE_PATH="${BACKUP_DIR}/${BACKUP_FILE}"

# Check if the specified backup file exists
if [ ! -f "$BACKUP_FILE_PATH" ]; then
    echo "Error: The backup file '${BACKUP_FILE_PATH}' was not found."
    exit 1
fi


echo "WARNING: This operation will delete all current data from '${DB_SERVICE_NAME}' and overwrite it with the backup."
read -p "Are you sure you want to continue? (yes/no) " -n 4 -r
echo
if [[ ! $REPLY =~ ^[Yy][Ee][Ss]$ ]]; then
    echo "Operation cancelled."
    exit 0
fi


# --- START OF RESTORE PROCESS ---

echo "1/5: Stopping all services..."
docker compose down

echo "2/5: Removing old data volume '${VOLUME_NAME}'..."
docker volume rm ${VOLUME_NAME}

echo "3/5: Creating new, empty data volume '${VOLUME_NAME}'..."
docker volume create ${VOLUME_NAME}

echo "4/5: Restoring data from '${BACKUP_FILE}'..."
# Start a temporary container to extract the data.
# --strip-components=2 removes the leading directories 'volume/storasense_data_volume' from the archive.
docker run --rm \
    -v "${VOLUME_NAME}:/data" \
    -v "$(pwd)/${BACKUP_DIR}:/backup" \
    busybox sh -c "tar -xzvf /backup/${BACKUP_FILE} -C /data --strip-components=2"

echo "5/5: Restarting all services with the restored data..."
docker compose up -d

echo ""
echo "Restore completed successfully!"
