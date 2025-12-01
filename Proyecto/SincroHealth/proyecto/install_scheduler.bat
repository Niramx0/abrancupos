@echo off

:: Obtener ruta absoluta del proyecto (donde está este .bat)
set PROJECT_PATH=%~dp0

:: Archivos a programar
set NOTIFY_FILE=%PROJECT_PATH%notificaciones.bat
set BACKUP_FILE=%PROJECT_PATH%backup.bat

echo Verificando archivos...

if not exist "%NOTIFY_FILE%" (
    echo ERROR: No se encuentra notify.bat
    pause
    exit /b 1
)

if not exist "%BACKUP_FILE%" (
    echo ERROR: No se encuentra backup.bat
    pause
    exit /b 1
)

echo Archivos encontrados correctamente.
echo.

schtasks /create ^
  /tn "SincroHealth_Notificaciones" ^
  /tr "\"%NOTIFY_FILE%\"" ^
  /sc daily ^
  /st 08:00 ^
  /f

echo.
echo  Tarea de notificaciones creada (08:00 AM).


schtasks /create ^
  /tn "SincroHealth_Backup" ^
  /tr "\"%BACKUP_FILE%\"" ^
  /sc daily ^
  /st 23:59 ^
  /f

echo.
echo  Tarea de backup creada (23:59 PM).

echo.
echo Las tareas se ejecutarán automáticamente todos los días.
echo.
pause
