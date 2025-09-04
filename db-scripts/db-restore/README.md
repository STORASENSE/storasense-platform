This folder contains script(s) to restore the database from a backup file - for Unix and Windows systems.
The backup file may be under the `storasense_data_volume_backup` folder in the project root.

For Unix systems:
```bash
docker run --rm -v storasense-platform_storasense_data_volume:/data -v <absolute--project-path>/storasense_data_volume_backup:/backup busybox sh -c "tar -xvf /backup/storasense-platform_storasense_data_volume.tar.gz -C /data"
```

For Windows systems with PowerShell:
```powershell
.\restore.ps1 <backup-file>
```

or directly with Docker:

```bash
docker run --rm -v storasense-platform_storasense_data_volume:/data -v <absolute--project-path>\storasense_data_volume_backup:/backup busybox sh -c "tar -xvf /backup/storasense-platform_storasense_data_volume.tar.gz -C /data"
```
