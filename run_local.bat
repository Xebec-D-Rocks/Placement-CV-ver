@echo off
setlocal
cd /d "%~dp0"

echo.
echo ============================================
echo   CoalGuard - Local Mode (No Docker)
echo   SQLite + in-memory cache
echo ============================================
echo.

if not exist logs mkdir logs
if not exist data\raw mkdir data\raw
if not exist media mkdir media

:: --- Read WEB_PORT from .env or env (default 8000) ---
set "WEB_PORT="
if exist ".env" (
    for /f "usebackq tokens=1,2 delims==" %%A in (".env") do (
        if "%%A"=="WEB_PORT" set "WEB_PORT=%%B"
    )
)
if "%WEB_PORT%"=="" set "WEB_PORT=8000"

set "PY="
py -3 --version >nul 2>&1
if %errorlevel%==0 (
    set "PY=py -3"
    goto :got_python
)
python --version >nul 2>&1
if %errorlevel%==0 (
    set "PY=python"
    goto :got_python
)
echo [ERROR] Python 3.11+ not found.
echo   Install from https://www.python.org/downloads/
echo.
pause
exit /b 1

:got_python
echo [OK] Using %PY%

:: --- Isolated virtual environment (created per project, on first run) ---
if not exist .venv (
    echo [1/4] Creating virtual environment (.venv) ...
    %PY% -m venv .venv
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to create .venv
        pause
        exit /b 1
    )
)
set "VPY=.venv\Scripts\python.exe"

echo [2/5] Installing requirements into .venv...
"%VPY%" -m pip install --upgrade pip --quiet
"%VPY%" -m pip install -r requirements.txt --quiet
if %errorlevel% neq 0 (
    echo [ERROR] pip install failed.
    pause
    exit /b 1
)

set USE_SQLITE=1
set DJANGO_DEBUG=1

echo [3/5] Running migrations...
"%VPY%" manage.py migrate --noinput
if %errorlevel% neq 0 (
    echo [ERROR] migrate failed
    pause
    exit /b 1
)

echo [4/5] Seeding data (first run only, ~30s)...
"%VPY%" manage.py bootstrap_data
"%VPY%" manage.py seed_demo_users

echo [5/5] Collecting static files...
"%VPY%" manage.py collectstatic --noinput >nul 2>&1

echo.
echo ============================================
echo   CoalGuard is LIVE (Local Mode - no Docker)
echo ============================================
echo.
echo   Dashboard:     http://127.0.0.1:%WEB_PORT%/
echo   API Docs:      http://127.0.0.1:%WEB_PORT%/api/docs/
echo   Admin:         http://127.0.0.1:%WEB_PORT%/admin/
echo.
echo   Demo accounts: admin/Admin@123, inspector/Inspector@123, regulator/Regulator@123
echo.
echo   Efficient:     To change port:  set WEB_PORT=9000  before running this script
echo   (or edit WEB_PORT= in .env).
echo.
echo   Press Ctrl+C to stop. Data lives in db.sqlite3.
echo.

start "" "http://127.0.0.1:%WEB_PORT%"
"%VPY%" manage.py runserver 127.0.0.1:%WEB_PORT%
pause