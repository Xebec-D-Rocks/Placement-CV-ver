# CoalGuard — AI-Based Smart Governance & Compliance Monitoring for Coal Mines

**PSID 26024 · Ministry of Coal / Coal India Limited · SIH 2026 · Category: Software · Theme: Smart Automation**

Centralized AI-enabled governance platform that digitally integrates mine-level activities, statutory compliance, inspections, contractor management, and field reporting into a single paperless ecosystem — with real-time dashboards, geo-tagged mobile sync, automated escalations, blockchain audit trails, and explainable risk analytics.

[![Stack](https://img.shields.io/badge/stack-Django%205.1%20%7C%20Postgres%2017%20%7C%20Redis%207%20%7C%20DRF%20%7C%20Celery-blue)](#stack)
[![License](https://img.shields.io/badge/license-MIT-green)](#license)
[![Local First](https://img.shields.io/badge/deploy-localhost%20%7C%20Docker%20Compose-orange)](#how-to-run)

---

## 1. Problem → Solution Mapping (PS requirements)

| PS Requirement | How CoalGuard Implements It | Where in Code |
|---|---|---|
| Digitally track statutory compliance (safety, environment, production, labour) | `ComplianceRequirement` + `ComplianceRecord` with due dates, evidence uploads, status workflow `PENDING → COMPLIANT / OVERDUE / ESCALATED`, regulatory reference, PDF report | `apps/compliance/models.py`, `apps/dashboard/report.py` |
| Real-time monitoring of inspections / violations / corrective actions | `Inspection` + `Observation` (severity LOW→CRITICAL) + `CorrectiveAction` with priority, owner, verification & escalation | `apps/inspections/models.py`, `apps/corrective_actions/models.py` |
| AI/analytics for high-risk areas, recurring failures, anomalies | Transparent weighted risk engine + z-score anomaly detection + recurring failure frequency analysis | `apps/analytics/risk.py`, `apps/analytics/anomaly.py`, `apps/analytics/api_views.py` |
| Geo-tagged, time-stamped field reporting with offline support | `latitude/longitude/accuracy` on inspections & observations, `client_id` for idempotent sync, `photo` evidence | `apps/inspections/models.py`, `apps/inspections/serializers.py` |
| Dashboards for mine officials / corporate / regulators | RBAC profiles + role-aware dashboard; GIS Leaflet map, KPI cards, Chart.js analytics; per-role API filtering | `apps/accounts/models.py`, `templates/base.html`, `apps/dashboard/templates/dashboard/index.html` |
| Automated alerts, reminders, escalations | `Notification` + `AlertRule` + Celery beat tasks `check_overdue_compliance` / `escalate_overdue_actions` (hourly) | `apps/notifications/models.py`, `apps/notifications/tasks.py` |
| Paperless governance | Document upload + `pytesseract` OCR pipeline, `reportlab` PDF reports, CSV exports, digital verification workflow | `apps/documents/ocr.py`, `apps/documents/models.py` |
| Scalable across mines & subsidiaries | Subsidiary-scoped filtering, per-state/subsidiary analytics, bulk import (Kaggle + CSV), containerized | `apps/mines/models.py`, `apps/data_import/management/commands/import_mines.py` |
| Blockchain audit trail | Hash-chained `AuditLog` (`previous_hash` + `entry_hash` SHA256), chain verification endpoint, append-only admin | `apps/audit/models.py`, `config/urls.py` |
| Multilingual & accessibility | `LANGUAGES` (en/hi/bn/te/mr/ta), `language` on `Profile`, locale-ready templates | `config/settings.py`, `apps/accounts/models.py` |

---

## 2. Architecture

```
                ┌─────────────────────────────────────────────────┐
                │              Browser / Mobile App               │
                │  Dashboard (Chart.js + Leaflet)  ·  Swagger UI │
                └──────────────┬──────────────────┬───────────────┘
                               │                  │
                    ┌──────────▼──────┐  ┌────────▼────────┐
                    │  Django 5.1     │  │  DRF + JWT API  │
                    │  Gunicorn (3wk) │  │  /api/*         │
                    └──────┬──────────┘  └────────┬────────┘
                           │                     │
              ┌────────────┼─────────────────────┼────────────┐
              │            │   config/celery.py  │            │
              │   ┌────────▼────────┐  ┌─────────▼─────────┐  │
              │   │ Celery Worker   │  │  Celery Beat     │  │
              │   │ overdue checks  │  │  hourly / daily  │  │
              │   └────────┬────────┘  └─────────┬─────────┘  │
              │            └──────────┬───────────┘            │
              │                       ▼                        │
              │          Redis 7  ·  Postgres 17              │
              │   ┌──────────────────────────────────┐       │
              │   │ mines · compliance · inspections │       │
              │   │ corrective_actions · audit       │       │
              │   │ notifications · contractors      │       │
              │   │ documents (OCR) · accounts (RBAC)│       │
              │   └──────────────────────────────────┘       │
              └───────────────────────────────────────────────┘
```

- **Local-only by default:** DB/Redis bind to `127.0.0.1` and the web app is published dual-stack (IPv4+IPv6, so `http://localhost:8000` works on modern Windows/macOS browsers) via Docker Compose; all host ports are overridable through `.env`. No cloud dependency except the one-time Kaggle download (cached; offline fallback to `data/raw/manual_mines.csv`).
- **Data source:** `shitalgaikwad123/indian-coal-mines-dataset-january-20211` (Kaggle) ingested via `kagglehub`; fuzzy column mapping by keyword (`apps/data_import/cleaning.py`) so it tolerates `Mine Name` vs `mine_name` vs `Name of Mine`. Every mapping decision is written to `docs/schema.md` at import time.
- **Static assets:** `whitenoise` (compressed manifest) — no separate nginx needed for demo; replace with S3/CDN in prod.

---

## 3. Stack

| Layer | Tech |
|---|---|
| Backend | Django 5.1, Django REST Framework, SimpleJWT, django-filter, drf-spectacular |
| DB / Cache / Queue | PostgreSQL 17, Redis 7, Celery 5.4 |
| Analytics | `apps/analytics/risk.py` (explainable weighted formula), `apps/analytics/anomaly.py` (z-score + frequency) |
| GIS | Stored `latitude/longitude` per mine/inspection/observation; Leaflet.js frontend; GeoJSON API |
| OCR / Reports | `pytesseract` + `Pillow`, `reportlab` PDF, `openpyxl` |
| Frontend | Django templates + Chart.js 4.4 + Leaflet 1.9, dark theme, responsive |
| Auth | `django.contrib.auth` + `Profile` RBAC (6 roles), JWT for mobile, session for web |
| Infra | Docker Compose (web + db + redis + celery_worker + celery_beat), `gunicorn`, healthcheck on `/health/` |

---

## 4. Complete Model Reference

### apps.mines — Mine Registry
| Field | Type | Notes |
|---|---|---|
| name | CharField(255) | Mine name |
| code | CharField(100) | Unique code, db_index |
| mine_type | CharField(20) | OPENCAST / UNDERGROUND / MIXED / UNKNOWN |
| location | CharField(255) | |
| latitude / longitude | FloatField | Geo-tagged |
| active | BooleanField | |
| state / district | CharField(100) | db_index |
| subsidiary | CharField(150) | db_index |
| coal_type | CharField(100) | |
| annual_production | FloatField | |
| source_row_id | CharField(100) | Kaggle row reference |
| is_synthetic | BooleanField | True = synthetic, False = real Kaggle row |
| risk_score / risk_level | FloatField / CharField | From risk engine |
| risk_safety / risk_compliance / risk_contractor / risk_incident | FloatField | Component scores |
| risk_computed_at | DateTimeField | |
| compliance_rate | property | % of COMPLIANT ComplianceRecords |

### apps.compliance — Statutory Compliance
| Model | Key Fields |
|---|---|
| ComplianceRequirement | name, category (SAFETY/ENVIRONMENT/LABOUR/PRODUCTION/OTHER), frequency_days, regulatory_reference, is_mandatory |
| ComplianceRecord | mine, requirement, status (COMPLIANT/PENDING/OVERDUE/ESCALATED/NOT_APPLICABLE), due_date, completed_date, assigned_to, escalation_level, evidence_file, created_by |

### apps.inspections — Inspections & Observations
| Model | Key Fields |
|---|---|
| Inspection | mine, inspector, inspector_name, inspection_type (ROUTINE/STATUTORY/SURPRISE/FOLLOW_UP), started_at, completed_at, status, latitude, longitude, location_accuracy_m, client_id (offline sync), synced_at |
| Observation | inspection, mine, severity (LOW/MEDIUM/HIGH/CRITICAL), category, description, status, raised_at, latitude, longitude, photo, closed_at, closed_by |

### apps.corrective_actions — Corrective Actions
| Model | Key Fields |
|---|---|
| CorrectiveAction | mine, observation, description, owner, assigned_to, priority (LOW/MEDIUM/HIGH/CRITICAL), due_date, completed_date, verified_by, verified_at, status, escalation_level |

### apps.audit — Blockchain Audit Trail
| Model | Key Fields |
|---|---|
| AuditLog | mine, actor, action, message, metadata (JSON), previous_hash, entry_hash (SHA256 chain), created_at |

### apps.accounts — RBAC
| Model | Key Fields |
|---|---|
| Profile (one-to-one with User) | role (ADMIN/REGULATOR/CORPORATE/MINE_OFFICIAL/INSPECTOR/CONTRACTOR), subsidiary, assigned_mine, phone, language |

### apps.notifications — Alerts & Escalations
| Model | Key Fields |
|---|---|
| Notification | recipient, mine, notification_type, priority, title, message, is_read, related_object_type/id, created_at, read_at |
| AlertRule | name, overdue_days_l1/l2/l3, is_active |

### apps.contractors — Contractor Management
| Model | Key Fields |
|---|---|
| Contractor | name, registration_no, contact_person, phone, email, mines (M2M), safety_score, compliance_rate, status |
| ContractorAssignment | contractor, mine, work_description, start_date, end_date, worker_count, is_active |

### apps.documents — OCR & Paperless
| Model | Key Fields |
|---|---|
| Document | mine, uploaded_by, doc_type, title, file, status (PENDING/PROCESSED/FAILED/VERIFIED), ocr_text, ocr_confidence, extracted_data (JSON), is_verified |

---

## 5. How to Run

> **Portability guarantee:** the project has **no hard-coded paths or machine names**.
> Everything is relative to the project folder, so you can move it, rename it, or clone
> it onto any PC and it just works. Ports and container names are configurable in
> `.env` (below) — nothing forces port `8000`.

### Prerequisites
- **Docker route (recommended):** [Docker Desktop](https://www.docker.com/products/docker-desktop/) running (or `docker` + `docker compose` CLI), 4 GB free RAM.
  - Default host ports `8000` (web), `5432` (Postgres), `6379` (Redis). **Each is configurable** via `.env` if already taken on your machine.
- **No-Docker route:** Python 3.11+ on the PATH. Everything else self-installs into a local `.venv`.
- Internet is only needed **once** (image pull + optional Kaggle dataset). If offline, seeding falls back to `data/raw/manual_mines.csv` (45 real mines).

### Configuration (.env) — optional, defaults work out of the box
Copy `.env.example` → `.env` if you want to change anything. The launchers create `.env` automatically from the example when missing.

| Variable | Default | Used by | Purpose |
|---|---|---|---|
| `COMPOSE_PROJECT_NAME` | `coalguard` | compose | Prefix of Docker container names — change if names collide with another project |
| `WEB_PORT` | `8000` | compose, bat/sh | Host port of the web app (e.g. `WEB_PORT=8080` if 8000 is busy) |
| `DB_PORT_HOST` | `5432` | compose | Host port of PostgreSQL (e.g. `5433` if busy) |
| `REDIS_PORT_HOST` | `6379` | compose | Host port of Redis (e.g. `6380` if busy) |
| `POSTGRES_DB` / `POSTGRES_USER` / `POSTGRES_PASSWORD` | `coalguard` / `coalguard` / `coalguard` | compose + Django | Postgres credentials (also defaulted in `config/settings.py`) |
| `POSTGRES_HOST` / `POSTGRES_PORT` | `db` / `5432` | Django | How the *web container* reaches Postgres inside the network |
| `REDIS_URL` | `redis://redis:6379/0` | Django/Celery | Broker + cache inside the network |
| `DJANGO_SECRET_KEY` | `dev-only-change-me` | Django | **Set a strong random value when `DJANGO_DEBUG=0`** |
| `DJANGO_DEBUG` | `1` | Django | `1` = allowed hosts `*`, friendly errors, CORS allow-all. `0` = production hardening (HSTS, secure cookies, SSL redirect) |
| `DJANGO_ALLOWED_HOSTS` | `localhost,127.0.0.1,[::1],0.0.0.0,web` | Django | Host header whitelist — only used when `DJANGO_DEBUG=0` |
| `CORS_ALLOWED_ORIGINS` | *(empty)* | Django | Comma-separated origins for cross-origin API clients |

### One-Click (Windows — recommended)
1. Double-click **`start_coalguard.bat`**.
   - Verifies Docker, launches Docker Desktop if needed (waits up to 120s), builds images, starts the stack with `--force-recreate` so stale containers never serve old code.
   - `web` waits for Postgres (`pg_isready`), then runs `migrate → bootstrap_data (import_mines → generate_activity → recompute_risk → seed_demo_users) → collectstatic → gunicorn`.
   - First boot seeds 200+ mines (real + synthetic) and governance activity — takes 1–2 minutes. Subsequent starts skip seeding (checks `Mine.objects.exists()`).
   - Reads `WEB_PORT` from `.env` and opens the dashboard automatically.
2. Browse (default port 8000; use your `WEB_PORT` if changed):
   - **Dashboard** `http://localhost:8000/`
   - **Mine Registry** `http://localhost:8000/mines/`
   - **API Docs** `http://localhost:8000/api/docs/`
   - **Admin** `http://localhost:8000/admin/`
   - **Health** `http://localhost:8000/health/` · **Audit chain** `http://localhost:8000/api/audit/verify/` · **PDF report** `http://localhost:8000/api/report/pdf/`
3. Double-click **`stop_coalguard.bat`** to stop (`docker compose down` without `-v` — data persists in volumes).

### No-Docker Fallback (Windows, Linux, macOS)
- **Windows:** double-click **`run_local.bat`**.
- **Linux/macOS:** `./run_local.sh`.

Both create a project-local **`.venv`** (isolated — no global Python pollution), install `requirements.txt` into it, then run on **SQLite + in-memory cache** with synchronous tasks (`USE_SQLITE=1` in `config/settings.py`):
- `migrate → bootstrap_data → seed_demo_users → collectstatic → runserver 127.0.0.1:<WEB_PORT>`.
- Data stored in `db.sqlite3` (kept across runs).
- Change port with `set WEB_PORT=9000` before running (Windows) / `WEB_PORT=9000 ./run_local.sh` (Unix), or set `WEB_PORT=` in `.env`.

### Manual (any OS, Docker)
```bash
cp .env.example .env
# optionally edit WEB_PORT / COMPOSE_PROJECT_NAME / passwords
docker compose up -d --build
docker compose exec web python manage.py createsuperuser
docker compose exec web python manage.py seed_demo_users
```

### Useful Commands
```bash
docker compose exec web python manage.py import_mines
docker compose exec web python manage.py generate_activity --reset
docker compose exec web python manage.py recompute_risk
docker compose exec web python manage.py seed_demo_users
docker compose exec web python manage.py shell
curl http://localhost:8000/health/
```

### Troubleshooting
| Symptom | Cause & fix |
|---|---|
| Browser shows *"can't connect"* to `localhost:8000` but works via `127.0.0.1:8000` | Windows resolves `localhost` → `::1` (IPv6) first; Docker once published IPv4-only. Current defaults bind dual-stack (`0.0.0.0` + `[::]`), so this is fixed — but re-run `start_coalguard.bat` (it uses `--force-recreate`) if your stack predates this fix. |
| HTTP `400 DisallowedHost` | Stale container/worker still running old `ALLOWED_HOSTS`. Re-create: `docker compose up -d --force-recreate`. In `DJANGO_DEBUG=1` all hosts are allowed automatically. |
| Dashboard shows `—` KPIs / blank charts after editing templates | gunicorn serves compiled templates + browser caches. Run `start_coalguard.bat` again (force-recreate) and hard-refresh (Ctrl+F5). A `NoCacheHTMLMiddleware` already sends no-cache headers on HTML. |
| Port `8000` already in use | Put `WEB_PORT=8080` in `.env` (and change `DB_PORT_HOST`/`REDIS_PORT_HOST` if 5432/6379 are busy). All launchers and the auto-opened browser URL follow `.env`. |
| `docker compose` errors about container name already in use | Change `COMPOSE_PROJECT_NAME` in `.env` — every container name is prefixed with it. |
| Docker Desktop not starting | The start script waits up to 120s; if it still fails, open Docker Desktop manually, wait until the whale is green, then re-run. |
| First boot very slow / no internet | `kagglehub` needs network once; if it fails it automatically falls back to the bundled `data/raw/manual_mines.csv`. Subsequent boots skip seeding. |
| OCR returns empty text | `tesseract` (eng+hin) must be installed on the host for the no-Docker route; inside Docker it is installed in the image. |
| JWT API calls get 401 on analytics | Analytics endpoints are intentionally `AllowAny` (no auth needed for dashboard charts); everything else requires a valid token/session. |

---

## 6. Roles & Demo Accounts

| Username | Password | Role | Access |
|---|---|---|---|
| admin | Admin@123 | System Admin | Full |
| regulator | Regulator@123 | Regulatory Authority | Read all, audit verify, reports |
| corporate | Corporate@123 | Corporate Management | Subsidiary-scoped |
| inspector | Inspector@123 | Field Inspector | Inspections, geo-tagged reporting |
| mine_official | Mine@12345 | Mine Official | Assigned mine(s) |
| contractor | Contractor@123 | Contractor | Contractor assignments |

Create/sync: `docker compose exec web python manage.py seed_demo_users`. Profiles auto-create via `post_save` signal on `User` (`apps/accounts/signals.py:7`).

---

## 7. API Reference

Base: `http://localhost:8000` · Auth: `Authorization: Bearer <access>` (JWT) or session cookie · Schema: `/api/schema/` · Swagger: `/api/docs/`

### Auth
| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/auth/token/` | Obtain JWT pair |
| POST | `/api/auth/token/refresh/` | Refresh access |
| GET | `/api/auth/me/` | Current user + profile |
| POST | `/api/auth/register/` | Create user (staff only) |

### Mines
| Method | Endpoint | Notes |
|---|---|---|
| GET/POST | `/api/mines/` | Filter: `state, district, subsidiary, coal_type, mine_type, risk_level, is_synthetic`; Search: `name, code`; Order: `name, risk_score, state` |
| GET/PATCH/DELETE | `/api/mines/{id}/` | |
| GET | `/api/mines/geojson/` | GeoJSON FeatureCollection |

### Compliance
| Method | Endpoint |
|---|---|
| GET/POST | `/api/compliance/requirements/` |
| GET/PATCH/DELETE | `/api/compliance/requirements/{id}/` |
| GET/POST | `/api/compliance/records/` |
| GET/PATCH/DELETE | `/api/compliance/records/{id}/` |

### Inspections & Observations
| Method | Endpoint | Notes |
|---|---|---|
| GET/POST | `/api/inspections/` | Provide `client_id` (UUID) for idempotent offline sync |
| GET/POST | `/api/observations/` | |

### Corrective Actions
| Method | Endpoint | Notes |
|---|---|---|
| GET/POST | `/api/corrective-actions/` | |
| POST | `/api/corrective-actions/{id}/verify/` | |
| POST | `/api/corrective-actions/{id}/close/` | |

### Contractors
| Method | Endpoint |
|---|---|
| GET/POST | `/api/contractors/` |
| GET/PATCH/DELETE | `/api/contractors/{id}/` |

### Documents (OCR)
| Method | Endpoint | Notes |
|---|---|---|
| GET/POST | `/api/documents/` | Upload `file`; sync OCR runs |
| GET | `/api/documents/{id}/` | Returns `ocr_text`, `ocr_confidence`, `extracted_data` |

### Notifications
| Method | Endpoint | Notes |
|---|---|---|
| GET | `/api/notifications/` | Recipient's notifications |
| POST | `/api/notifications/{id}/mark_read/` | |
| POST | `/api/notifications/mark_all_read/` | |
| GET | `/api/notifications/unread_count/` | |

### Analytics
| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/analytics/anomalies/` | Z-score flagged mines |
| GET | `/api/analytics/recurring-failures/` | Requirements by failure rate |
| GET | `/api/analytics/category-breakdown/` | Observations by category |
| GET | `/api/analytics/subsidiary-risk/` | Subsidiaries by avg risk |

### Dashboard (legacy JSON)
`api/dashboard/kpis`, `api/dashboard/risk-distribution`, `api/dashboard/mines-by-state`, `api/dashboard/compliance-breakdown`, `api/dashboard/inspection-trend`, `api/dashboard/mines-geojson`, `api/dashboard/high-risk-mines`

### Reports & Audit
| Endpoint | Description |
|---|---|
| GET /api/report/pdf/ | `reportlab` compliance PDF |
| GET /api/audit/verify/ | `{valid: bool, broken_at_id: int\|null}` |
| GET /health/ | `{status: ok, service: coalguard, version: 1.0.0}` |

**Example — offline inspection sync (mobile):**
```bash
TOKEN=$(curl -s -X POST http://localhost:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"inspector","password":"Inspector@123"}' | python -c "import sys,json;print(json.load(sys.stdin)['access'])")
curl -X POST http://localhost:8000/api/inspections/ \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"mine": 1, "started_at": "2026-08-29T10:00:00+05:30", "status": "COMPLETED",
       "inspection_type": "ROUTINE", "summary": "Routine safety walk",
       "latitude": 23.3441, "longitude": 85.3096, "location_accuracy_m": 12,
       "client_id": "550e8400-e29b-41d4-a716-446655440000"}'
```

---

## 8. Risk Engine

`apps/analytics/risk.py:12` — explainable, no trained model:

```
risk_score = safety_score     * 0.35
           + compliance_score * 0.30
           + contractor_score * 0.15
           + incident_score   * 0.20
```

| Level | Range |
|---|---|
| LOW | 80–100 |
| MEDIUM | 60–79.99 |
| HIGH | 40–59.99 |
| CRITICAL | 0–39.99 |

- **safety_score** — 100 − penalties per open observation: LOW −2, MEDIUM −5, HIGH −12, CRITICAL −25.
- **compliance_score** — `COMPLIANT / (COMPLIANT+OVERDUE+ESCALATED)` ×100; no determinable records → 50.
- **contractor_score** — placeholder `70 ± hash(subsidiary)` (−10…+10), flagged as weakest-grounded; replace with real contractor data in Phase 2.
- **incident_score** — 100 − OPEN×5 − IN_PROGRESS×3 − OVERDUE×15.

Recompute: `python manage.py recompute_risk` (also Celery beat nightly).

Anomaly module (`apps/analytics/anomaly.py:29`) flags mines with `open_obs > mean+2σ` or `overdue_cas ≥3`; recurring failures ranks requirements by `OVERDUE+ESCALATED` rate.

---

## 9. Security, Governance & Compliance

- **Hash-chained audit log** — every `AuditLog` entry stores `previous_hash` + `entry_hash = SHA256(...)`. `GET /api/audit/verify/` verifies the chain; admin is append-only (`has_delete_permission = False`).
- **RBAC** — 6 roles, per-mine/subsidiary scoping (`Profile.has_mine_access`), JWT for mobile, session for web, staff gates for user creation.
- **Escalations** — `AlertRule` configurable thresholds; Celery tasks flip `PENDING → OVERDUE` and bump `escalation_level` / `ESCALATED` states; notifications fan-out to staff.
- **Validation** — DRF serializers, `django-filter`, throttling (`anon 100/h, user 1000/h`), CORS (allow-all in DEBUG), security headers in prod (`HSTS, SECURE_SSL_REDIRECT` when `DEBUG=0`).
- **Paperless** — OCR via `tesseract` (eng+hin), PDF via `reportlab`, CSV export on mine registry, `evidence_file`/`photo` uploads under `media/`.

---

## 10. Folder Structure

```
coalguard/
├── config/
│   ├── settings.py        # DRF+JWT, Celery, CORS, i18n, Redis cache, logging
│   ├── celery.py           # beat schedule: overdue checks, risk recompute
│   ├── urls.py             # web + /api/* + /health + /api/docs + report + audit verify
│   ├── wsgi.py / asgi.py / celery.py
├── apps/
│   ├── accounts/           # Profile RBAC, /api/auth/me, /api/auth/register, seed_demo_users
│   ├── mines/              # Mine registry, MineViewSet, GeoJSON, CSV export
│   ├── compliance/         # Requirement / Record (ESCALATED workflow), report PDF
│   ├── inspections/        # Inspection + Observation (geo + offline client_id + photo)
│   ├── corrective_actions/ # CA (priority, verify/close actions)
│   ├── audit/              # Hash-chained AuditLog, chain verification
│   ├── analytics/          # risk.py + anomaly.py + tasks.py
│   ├── dashboard/          # KPI + Chart.js JSON + Leaflet map + high-risk table + report.py
│   ├── data_import/        # kagglehub import, cleaning.py (fuzzy mapping), synthetic generator
│   ├── notifications/      # Notification + AlertRule, Celery overdue/escalation tasks
│   ├── contractors/        # Contractor + Assignment
│   └── documents/          # Document + pytesseract OCR pipeline
├── templates/base.html
├── docs/schema.md          # auto-regenerated by import_mines
├── docs/model_report.md    # auto-regenerated by recompute_risk
├── requirements.txt
├── Dockerfile
├── .dockerignore            # keeps .env/DB/media/venv out of the image
├── docker-compose.yml       # ports & container names configurable via .env
├── .env.example             # full configuration reference (copy to .env)
├── start_coalguard.bat      # one-click: Docker check, build, force-recreate, seed, open browser
├── stop_coalguard.bat
├── run_local.bat            # Windows no-Docker fallback (self-contained .venv + SQLite)
├── run_local.sh             # Linux/macOS no-Docker fallback (same behaviour)
└── README.md
```

---

## 11. Roadmap (post-MVP — out of scope for this submission)

- **PostGIS + GeoDjango** interactive heatmap & radius search (currently plain `FloatField` lat/lon).
- **Celery beat persistence** (`django-celery-beat` DB scheduler) + async OCR queue.
- **ML retrain** — replace weighted formula with trained classifier when labeled incident data exists.
- **Offline-first mobile** — PWA with WatermelonDB + background sync to `client_id`-idempotent endpoints.
- **Multilingual conversational interface** — local LLM / RAG over compliance/inspection corpus.

---

## 12. Data Provenance

- Every `Mine` row carries `is_synthetic` — real Kaggle rows are never mutated; synthetic rows are separate, clearly tagged, drawn from the real data's own state/coal-type/subsidiary distributions.
- All compliance/inspection/corrective-action activity is synthetic (no real governance-activity dataset exists) generated with fixed seed `20260828` (`apps/data_import/management/commands/generate_activity.py:25`) — visible on dashboard via Real/Synthetic KPI.
- `docs/schema.md` and `docs/model_report.md` are generated artifacts, not hand-written — they always reflect the last actual run.

---

## 13. License & Credits

MIT. Built for **SIH 2026 — PSID 26024**. Dataset: `shitalgaikwad123/indian-coal-mines-dataset-january-20211` (Kaggle, via `kagglehub`). GIS tiles: OpenStreetMap. OCR: Tesseract.
