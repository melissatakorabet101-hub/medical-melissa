@echo off

set "PROJECT_DIR=%~dp0"
set "BACKUP_DIR=%PROJECT_DIR%backups"

if not exist "%BACKUP_DIR%" mkdir "%BACKUP_DIR%"

copy "%PROJECT_DIR%db_clinique_a.sqlite3" "%BACKUP_DIR%\backup.sqlite3"

echo.
echo ==========================
echo Backup termine !
echo ==========================
echo.
pause