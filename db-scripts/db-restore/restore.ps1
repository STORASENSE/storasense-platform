param(
    [Parameter(Mandatory=$true)]
    [string]$BackupFile
)

$VOLUME_NAME = "storasense-platform_storasense_data_volume"
$DB_SERVICE_NAME = "timescaledb"
$BACKUP_DIR = "./storasense_data_volume_backup"

$BACKUP_FILE_PATH = Join-Path $BACKUP_DIR $BackupFile
if (-not (Test-Path $BACKUP_FILE_PATH)) {
    Write-Host "Error: The backup file '$BACKUP_FILE_PATH' was not found." -ForegroundColor Red
    exit 1
}

$backupSize = (Get-Item $BACKUP_FILE_PATH).Length
Write-Host "Backup file size: $($backupSize / 1MB) MB" -ForegroundColor Cyan

Write-Host "WARNING: This operation will delete all current data from '$DB_SERVICE_NAME' and overwrite it with the backup." -ForegroundColor Yellow
$confirmation = Read-Host "Are you sure you want to continue? (yes/no)"
if ($confirmation -ne "yes") {
    Write-Host "Operation cancelled."
    exit 0
}

Write-Host "1/5: Stopping all services..."
docker compose down

Write-Host "2/5: Removing old data volume '$VOLUME_NAME'..."
docker volume rm $VOLUME_NAME 2>$null

Write-Host "3/5: Creating new, empty data volume '$VOLUME_NAME'..."
docker volume create $VOLUME_NAME

Write-Host "4/5: Restoring data from '$BackupFile'..."
$currentDir = Get-Location

# Check Backup Directory
Write-Host "Checking backup contents..." -ForegroundColor Cyan
docker run --rm -v "${currentDir}/${BACKUP_DIR}:/backup" busybox sh -c "tar -tzf '/backup/$BackupFile' | head -10"

# Easy approach to restore
Write-Host "Extracting and restoring data..." -ForegroundColor Cyan
docker run --rm -v "${VOLUME_NAME}:/data" -v "${currentDir}/${BACKUP_DIR}:/backup" busybox sh -c "tar -xzf '/backup/$BackupFile' -C /tmp && ls -la /tmp/ && cp -r /tmp/backup/storasense_data_volume/* /data/ && ls -la /data/ && du -sh /data"

if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Basic restore failed, trying alternative method..." -ForegroundColor Yellow


    docker run --rm -v "${VOLUME_NAME}:/data" -v "${currentDir}/${BACKUP_DIR}:/backup" busybox sh -c "
        tar -xzf '/backup/$BackupFile' -C /tmp
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
}

# Check if PostgreSQL files are present
Write-Host "Verifying PostgreSQL files..." -ForegroundColor Cyan
docker run --rm -v "${VOLUME_NAME}:/data" busybox sh -c "ls -la /data/ && if [ -f /data/postgresql.conf ]; then echo 'SUCCESS: postgresql.conf found'; else echo 'WARNING: postgresql.conf not found'; fi"

Write-Host "5/5: Restarting all services..."
docker compose up -d

Write-Host "Restore completed!" -ForegroundColor Green
