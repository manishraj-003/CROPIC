# Architecture Snapshot (Submission)

## System Flow
Mobile App -> FastAPI Backend -> AI Services -> Data Store -> Web Dashboard

Auxiliary flows:
- Satellite NDVI verification service (`/v1/satellite/ndvi`)
- Fraud checks (ELA + discrepancy audit queue)
- Voice reporting in 11 supported languages

## Implemented Modules
- Mobile (React Native): guided capture, blur gate, geotagging, offline queue, sync.
- Backend (FastAPI): auth, claim APIs, verification, fraud, dashboard summaries/clusters/regions, ops latency.
- AI service layer: baseline crop/stage classification, segmentation damage ratio, stress scoring.
- Dashboard (Next.js): KPI cards, fraud queue, geospatial cluster/region report feeds.

## Security & Compliance Controls
- JWT auth and role-based endpoint guards.
- Audit logging for sensitive actions.
- TLS 1.3 ingress config (nginx dev proxy).
- Compliance checklist and retention/control mapping documented.

## Verification Evidence
- Latency gate (<2s p95): pass.
- Reliability run: pass (10/10).
- Multilingual voice validation: pass (11/11).
- Success metrics: classification >= 0.85 and IoU >= 0.80 (based on current eval datasets).

## Deployment Notes
- Local verification scripts and runbooks are included in `06_tech_assets/`.
- Full one-command verification available via `run_all_checks.ps1`.
