# Incident Response Runbook

## Severity Levels
- SEV-1: API outage or critical claim flow unavailable.
- SEV-2: Major degradation (high latency, partial failures).
- SEV-3: Non-critical feature issue.

## First 15 Minutes
1. Confirm incident and scope from `/health`, `/v1/ops/latency`, and logs.
2. Assign incident owner and communication owner.
3. Announce initial status and mitigation ETA.

## Mitigation Playbook
- Restart affected service.
- Scale backend instances if CPU saturation detected.
- Disable non-critical endpoints if needed.
- Roll back to last known stable release when regression is confirmed.

## Recovery Validation
- Smoke run: `python scripts/smoke_backend_flow.py`
- Load run: `python scripts/load_test_backend.py`
- Gate: `python scripts/latency_gate.py`

## Postmortem
- Root cause summary.
- Timeline with exact timestamps.
- Corrective actions with owners and due dates.
