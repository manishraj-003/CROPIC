# MVP Demo Script

## 5-Minute Flow
1. Login and OTP/token generation.
2. Mobile capture with ghost overlay and blur quality gate.
3. Metadata submission and claim creation.
4. Dual verification (ground stress vs NDVI) and fraud queue update.
5. Dashboard review of flagged claim with discrepancy and tamper score.

## Fallback Plan
- If map tiles fail: switch to table mode for claims.
- If model endpoint fails: use cached demo output JSON.
- If internet drops: show offline queue behavior from mobile app.

## Judge Q&A Anchors
- Accuracy: baseline target and model roadmap.
- Fraud prevention: NDVI discrepancy + ELA dual checks.
- Scale: containerized services with phased district onboarding.
