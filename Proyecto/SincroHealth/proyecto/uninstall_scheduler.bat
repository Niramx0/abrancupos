@echo off
echo.

echo Intentando eliminar tarea: SincroHealth_Notificaciones...
schtasks /delete /tn "SincroHealth_Notificaciones" /f >nul 2>&1

if %errorlevel%==0 (
    echo Tarea 'SincroHealth_Notificaciones' eliminada exitosamente.
) else (
    echo La tarea 'SincroHealth_Notificaciones' no existe o ya fue eliminada.
)

echo.
echo Intentando eliminar tarea: SincroHealth_Backup...
schtasks /delete /tn "SincroHealth_Backup" /f >nul 2>&1

if %errorlevel%==0 (
    echo Tarea 'SincroHealth_Backup' eliminada exitosamente.
) else (
    echo La tarea 'SincroHealth_Backup' no existe o ya fue eliminada.
)

echo.
echo Todas las tareas programadas de SincroHealth han sido removidas.
echo.
pause
