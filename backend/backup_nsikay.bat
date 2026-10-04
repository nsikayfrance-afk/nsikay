@echo off

echo === BACKUP NSIKAY ===

set BACKUP=backup_%date:~-4%%date:~3,2%%date:~0,2%.sql


pg_dump -U nsikay_admin nsikay > %BACKUP%


echo BACKUP TERMINE

