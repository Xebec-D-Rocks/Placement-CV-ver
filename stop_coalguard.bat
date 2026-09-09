@echo off
cd /d "%~dp0"

echo.
echo ============================================
echo   Stopping CoalGuard
echo ============================================
echo.

set "DOCKER_CMD="
where docker >nul 2>&1
if %errorlevel%==0 (
    set "DOCKER_CMD=docker"
    goto :found
)
if exist "C:\Program Files\Docker\Docker\resources\bin\docker.exe" (
    set "PATH=C:\Program Files\Docker\Docker\resources\bin;%PATH%"
    where docker >nul 2>&1
    if %errorlevel%==0 (
        set "DOCKER_CMD=docker"
        goto :found
    )
)
echo Docker not found. If you used run_local.bat, press Ctrl+C in the server window instead.
pause
exit /b 0

:found
echo Stopping containers (data is preserved in volumes)...
docker compose down
echo.
echo Done. Your data is still there.
echo Run start_coalguard.bat to start again.
if exist db.sqlite3 echo Note: db.sqlite3 also exists (from run_local.bat).
echo.
pause