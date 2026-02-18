# Model Governance and Retraining Cadence

## Versioning
- Keep dataset manifests versioned in `data/metadata/`.
- Tag model artifacts with: model name, dataset version, training date, metrics.

## Drift Monitoring
- Generate baseline/current label distributions.
- Run `python scripts/drift_monitor.py`.
- If drift threshold is exceeded, trigger retraining ticket.

## Retraining Cadence
- Weekly for pilot stage.
- Bi-weekly after stabilization unless drift alert triggers earlier retraining.

## Rollback
- Keep previous production model artifact and inference config.
- If latency or accuracy degrades after release, revert to prior model version.
