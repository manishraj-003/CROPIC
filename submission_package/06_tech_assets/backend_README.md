# Backend Notes

## Scope
- Metadata ingest API
- Claim creation API
- Dual-verification discrepancy API
- Fraud tamper (ELA) API
- Audit queue API
- Role-based JWT-protected endpoints
- Persistent local storage via SQLite

## Run
```powershell
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## Test
```powershell
cd backend
.venv\Scripts\Activate.ps1
pytest
```

## Key Endpoints
- `GET /health`
- `POST /v1/auth/token`
- `POST /v1/images/metadata` (JWT)
- `POST /v1/claims` (JWT)
- `POST /v1/ai/classify` (JWT)
- `POST /v1/ai/segment` (JWT)
- `POST /v1/ai/stress` (JWT)
- `POST /v1/verification/dual` (JWT)
- `POST /v1/fraud/ela` (JWT)
- `GET /v1/audit/queue` (JWT)
- `GET /v1/dashboard/summary` (JWT)
- `GET /v1/dashboard/clusters` (JWT)
- `GET /v1/dashboard/regions` (JWT)
- `POST /v1/voice/report` (JWT)
- `GET /v1/voice/languages`
- `POST /v1/satellite/ndvi` (JWT)
- `GET /v1/ops/latency` (JWT, role `admin`/`insurer`)

Note: `/v1/satellite/ndvi` currently returns deterministic simulation values (`sentinel2-sim`) until live Sentinel-2/GEE integration is connected.

## Quick Auth
1. `POST /v1/auth/token` with `{"phone":"9999999999","role":"insurer"}`
2. Use `Authorization: Bearer <token>` for protected endpoints.
