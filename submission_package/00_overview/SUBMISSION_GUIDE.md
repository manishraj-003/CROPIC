# CROPIC-AI Submission Guide

## Package Intent
This folder is prepared for direct hackathon submission and judge review.
It includes architecture, implementation evidence, verification reports, and demo execution assets.

## Contents
- `01_problem_docs/`: PRD, SDD, and tech stack references.
- `02_architecture/`: architecture snapshot and deployed component map.
- `03_checklists/`: implementation checklists and compliance/security trackers.
- `04_reports/`: generated load/latency/metrics/reliability/drift evidence.
- `05_demo_bundle/`: final demo flow, finale runbook, TRL roadmap, integration notes.
- `06_tech_assets/`: scripts to rerun checks and validate readiness.

## Judge Quick Review Path (Recommended)
1. `02_architecture/ARCHITECTURE_SNAPSHOT.md`
2. `03_checklists/CROPIC_AI_TODO.md`
3. `04_reports/load_test_report.json`
4. `04_reports/success_metrics_report.txt`
5. `05_demo_bundle/demo_script.md`

## Reproducibility
From repo root:
- `powershell -ExecutionPolicy Bypass -File scripts/run_all_checks.ps1`
- `python scripts/summarize_checks.py`

## Current Status
- Core TRL 4/5 prototype workflow is implemented.
- Automated technical gates pass in local verification.
- Remaining non-automatable items are field-dependent (interviews, real satellite pipeline ops, full-scale labeled data collection).
