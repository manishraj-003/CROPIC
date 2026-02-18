# CROPIC

This repository contains the CROPIC-AI TRL 4/5 prototype workstream.

## Structure
- `mobile/`: React Native app scaffold (capture + ghost overlay + blur gate)
- `backend/`: FastAPI APIs for metadata, claims, discrepancy, fraud/tamper queue
- `dashboard/`: Next.js command-center dashboard scaffold
- `ai-services/`: model utility modules and tests
- `db/`: PostgreSQL schema drafts and migration seeds
- `satellite/`: Sentinel-2 NDVI templates and pilot district notes
- `research/`: interview templates and persona outputs
- `infra/`: local infra (docker compose)
- `docs/execution/`: phase-wise execution trackers and finale runbook

## Backend Quick Run
1. `cd backend`
2. `python -m venv .venv`
3. `.venv\Scripts\Activate.ps1`
4. `pip install -r requirements.txt`
5. `uvicorn app.main:app --reload --port 8000`

## Local Infra
1. `cd infra`
2. `docker compose up -d`
3. For TLS ingress setup, follow `infra/nginx/README.md` and use `https://localhost:8443`.

## MVP Endpoints
- `GET /health`
- `POST /v1/images/metadata`
- `POST /v1/claims`
- `POST /v1/verification/dual`
- `POST /v1/fraud/ela`
- `GET /v1/audit/queue`

## Smoke Test
1. Start backend on `http://localhost:8000`.
2. Run `python scripts/smoke_backend_flow.py`.

## Load Test
1. Start backend on `http://localhost:8000`.
2. Run `python scripts/load_test_backend.py` for concurrent health, summary, and metadata upload checks.
3. Run `python scripts/latency_gate.py` to enforce `<2s` p95 thresholds from the generated report.
4. Or run full pipeline: `powershell -ExecutionPolicy Bypass -File scripts/run_all_checks.ps1`

## Reliability and Governance
- Uptime watcher: `python scripts/uptime_monitor.py`
- Drift detection: `python scripts/drift_monitor.py`
- Runbooks: `docs/execution/incident_runbook.md`, `docs/execution/model_governance.md`
- Compliance checklist: `docs/execution/compliance_prep_checklist.md`

## Success Metric Evaluation
1. Fill:
   - `docs/execution/classification_eval.csv`
   - `docs/execution/segmentation_eval.csv`
   - `docs/execution/fraud_eval.csv`
2. Run `python scripts/evaluate_success_metrics.py`.
3. Summarize all reports: `python scripts/summarize_checks.py`.
4. Run final TRL gate: `python scripts/trl_gate.py`.

## Full One-Command Checks
- `powershell -ExecutionPolicy Bypass -File scripts/run_all_checks.ps1`
