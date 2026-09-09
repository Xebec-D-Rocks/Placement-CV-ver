@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"

:: ============================================================
:: CoalGuard - Smart Governance Platform
:: PSID 26024 | Ministry of Coal | CIL | SIH 2026
:: Single-file launcher: Docker Compose with auto-recovery
:: ============================================================

:: Create logs dir
if not exist logs mkdir logs
> "logs\startup.log" echo [%date% %time%] CoalGuard startup initiated

echo.
echo ============================================
echo   CoalGuard - Smart Governance Platform
echo   PSID 26024 ^| Ministry of Coal ^| CIL
echo ============================================
echo.

:: --- Step 1: Find Docker ---
set "DOCKER_CMD="
where docker >nul 2>&1
if %errorlevel%==0 (
    set "DOCKER_CMD=docker"
    goto :found_docker
)

:: Try common install paths
if exist "C:\Program Files\Docker\Docker\resources\bin\docker.exe" (
    set "PATH=C:\Program Files\Docker\Docker\resources\bin;%PATH%"
    where docker >nul 2>&1
    if %errorlevel%==0 (
        set "DOCKER_CMD=docker"
        goto :found_docker
    )
)

if exist "C:\Program Files\Docker\Docker\Docker Desktop.exe" (
    set "PATH=C:\Program Files\Docker\Docker\resources\bin;%PATH%"
    where docker >nul 2>&1
    if %errorlevel%==0 (
        set "DOCKER_CMD=docker"
        goto :found_docker
    )
)

echo [ERROR] Docker not found on this machine.
echo.
echo   Install Docker Desktop from:
echo   https://www.docker.com/products/docker-desktop/
echo.
echo   OR use run_local.bat to run without Docker.
echo.
>> "logs\startup.log" echo [ERROR] docker not found
pause
exit /b 1

:found_docker
echo [OK] Docker CLI found.
>> "logs\startup.log" echo docker CLI found

:: --- Step 2: Check Docker Engine ---
"%DOCKER_CMD%" info >nul 2>&1
if %errorlevel%==0 goto :engine_running

echo [INFO] Docker Engine is not running. Launching Docker Desktop...
>> "logs\startup.log" echo launching Docker Desktop

if exist "C:\Program Files\Docker\Docker\Docker Desktop.exe" (
    start "" "C:\Program Files\Docker\Docker\Docker Desktop.exe"
) else (
    start "" docker-desktop
)

echo   Waiting for Docker Engine (up to 120 seconds)...
set /a DT_COUNT=0
:wait_engine
set /a DT_COUNT+=1
if !DT_COUNT! gtr 24 (
    echo [ERROR] Docker Engine did not start in 120 seconds.
    echo   Check the Docker Desktop icon in your system tray.
    echo   OR use run_local.bat to run without Docker.
    echo.
    pause
    exit /b 1
)
"%DOCKER_CMD%" info >nul 2>&1
if %errorlevel%==0 goto :engine_running
echo   Attempt !DT_COUNT!/24 ...
timeout /t 5 >nul
goto :wait_engine

:engine_running
echo [OK] Docker Engine is running.
>> "logs\startup.log" echo docker engine running

:: --- Step 3: Create .env if missing ---
if not exist ".env" (
    if exist ".env.example" (
        copy /Y .env.example .env >nul
        echo [SETUP] Created .env from .env.example
    )
) else (
    echo [SETUP] Using existing .env
)

:: --- Read WEB_PORT from .env (default 8000) ---
set "WEB_PORT="
if exist ".env" (
    for /f "usebackq tokens=1,2 delims==" %%A in (".env") do (
        if "%%A"=="WEB_PORT" set "WEB_PORT=%%B"
    )
)
if "%WEB_PORT%"=="" set "WEB_PORT=8000"

:: --- Step 4: Build images ---
echo.
echo [BUILD] Building Docker images (this may take a few minutes on first run)...
>> "logs\startup.log" echo building images
"%DOCKER_CMD%" compose build 2>> "logs\startup.log"
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Docker build failed. Showing last 20 lines of build log:
    echo.
    "%DOCKER_CMD%" compose build 2>&1 | more +1
    echo.
    echo   Full log: logs\startup.log
    echo   Try: docker compose build --no-cache
    echo.
    pause
    exit /b 1
)
echo [OK] Images built successfully.
>> "logs\startup.log" echo images built

:: --- Step 5: Start containers ---
echo [START] Starting containers...
>> "logs\startup.log" echo starting containers
"%DOCKER_CMD%" compose up -d --force-recreate 2>> "logs\startup.log"
if %errorlevel% neq 0 (
    echo [ERROR] Failed to start containers.
    echo   Try: docker compose down and run this script again.
    echo.
    pause
    exit /b 1
)
echo [OK] Containers started.
>> "logs\startup.log" echo containers started

:: --- Step 6: Wait for database ---
echo.
echo [WAIT] Waiting for database...
set /a DB_COUNT=0
:wait_db
set /a DB_COUNT+=1
if !DB_COUNT! gtr 30 (
    echo [ERROR] Database not ready after 90 seconds.
    echo.
    "%DOCKER_CMD%" compose logs db --tail=20 2>&1
    echo.
    pause
    exit /b 1
)
"%DOCKER_CMD%" compose exec -T db pg_isready -U coalguard >nul 2>&1
if %errorlevel%==0 goto :db_ready
timeout /t 3 >nul
goto :wait_db

:db_ready
echo [OK] Database is ready.
>> "logs\startup.log" echo database ready

:: --- Step 7: Wait for web app (gunicorn) ---
echo [WAIT] Waiting for web app (bootstrap + migrations)...
set /a WEB_COUNT=0
:wait_web
set /a WEB_COUNT+=1
if !WEB_COUNT! gtr 40 (
    echo.
    echo [ERROR] Web app not responding after 120 seconds.
    echo   Showing web container logs:
    echo.
    "%DOCKER_CMD%" compose logs web --tail=40 2>&1
    echo.
    pause
    exit /b 1
)
"%DOCKER_CMD%" compose exec -T web curl -sf http://0.0.0.0:8000/health/ >nul 2>&1
if %errorlevel%==0 goto :web_ready
echo   Attempt !WEB_COUNT!/40 ...
timeout /t 3 >nul
goto :wait_web

:web_ready
echo [OK] Web app is responding.
>> "logs\startup.log" echo web responding

:: --- Step 8: Done ---
echo.
echo ============================================
echo   CoalGuard is LIVE!
echo ============================================
echo.
echo   Dashboard:     http://localhost:%WEB_PORT%/
echo   Mine Registry:  http://localhost:%WEB_PORT%/mines/
echo   API Docs:       http://localhost:%WEB_PORT%/api/docs/
echo   Health:         http://localhost:%WEB_PORT%/health/
echo   Admin:          http://localhost:%WEB_PORT%/admin/
echo.
echo   Demo Accounts:
echo     admin / Admin@123          (System Admin)
echo     regulator / Regulator@123  (Regulatory Authority)
echo     corporate / Corporate@123  (Corporate Management)
echo     inspector / Inspector@123  (Field Inspector)
echo     mine_official / Mine@12345 (Mine Official)
echo     contractor / Contractor@123 (Contractor)
echo.
echo   Commands:
echo     View logs:    docker compose logs -f web
echo     Stop:         stop_coalguard.bat
echo     Local mode:   run_local.bat (no Docker needed)
echo     Full log:     logs\startup.log
echo.
>> "logs\startup.log" echo STARTUP SUCCESSFUL

start "" "http://localhost:%WEB_PORT%"
echo Press any key to keep this window open (containers keep running in background).
pause >nul