#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"
echo "============================================"
echo " CoalGuard - Local run WITHOUT Docker"
echo " SQLite + in-memory cache"
echo "============================================"
mkdir -p logs data/raw media

# Read WEB_PORT from .env or env (default 8000)
WEB_PORT=""
if [ -f .env ]; then
    WEB_PORT="$(grep -E '^WEB_PORT=' .env | cut -d= -f2- | tr -d '\r')"
fi
[ -z "$WEB_PORT" ] && WEB_PORT="${WEB_PORT:-8000}"

PYTHON="${PYTHON:-python3}"
echo "[OK] Using $PYTHON"

# Isolated virtual environment (created per project, on first run)
if [ ! -d .venv ]; then
    echo "[1/4] Creating virtual environment (.venv) ..."
    "$PYTHON" -m venv .venv
fi
VPY=".venv/bin/python"

echo "[2/4] Installing requirements into .venv..."
"$VPY" -m pip install --upgrade pip --quiet
"$VPY" -m pip install -r requirements.txt --quiet

export USE_SQLITE=1 DJANGO_DEBUG=1

echo "[3/4] Running migrations..."
"$VPY" manage.py migrate --noinput
echo "[4/4] Seeding data (first run only, ~30s) and collecting static files..."
"$VPY" manage.py bootstrap_data || true
"$VPY" manage.py seed_demo_users || true
"$VPY" manage.py collectstatic --noinput >/dev/null 2>&1 || true

echo ""
echo "============================================"
echo "  CoalGuard is LIVE (Local Mode - no Docker)"
echo "============================================"
echo "  Dashboard: http://127.0.0.1:$WEB_PORT/"
echo "  API Docs:  http://127.0.0.1:$WEB_PORT/api/docs/"
echo "  Admin:     http://127.0.0.1:$WEB_PORT/admin/"
echo ""
echo "  Demo accounts: admin/Admin@123, inspector/Inspector@123, regulator/Regulator@123"
echo "  Change port:   WEB_PORT=9000 ./run_local.sh   (or set WEB_PORT= in .env)"
echo "  Stop with Ctrl+C. Data lives in db.sqlite3."
echo ""
"$VPY" manage.py runserver 127.0.0.1:"$WEB_PORT"