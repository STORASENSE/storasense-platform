This folder contains scripts to restore the database from a backup file - for Unix and Windows systems.

- Ensure you have the necessary permissions to execute these scripts and that the backup file is accessible - especially on Unix systems where you may need to set executable permissions:
```bash
chmod +x restore.sh
```

- For Unix systems:
```bash
./restore.sh <backup-file>
```

- For Windows systems with PowerShell:
```powershell
.\restore.ps1 <backup-file>
```
