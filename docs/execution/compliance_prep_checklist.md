# Compliance Prep Checklist (DPDP/GDPR)

## Consent and Purpose
- [x] Define explicit purpose text for data collection (claims verification, fraud checks).
- [ ] Show consent prompt in mobile app before first upload.
- [ ] Add withdrawal/revocation flow.

## Data Minimization
- [x] Collect only required metadata fields for claim verification.
- [ ] Remove optional fields not used in decision workflows.

## Retention and Deletion
- [x] Define retention policy draft:
  - Raw images: 12 months
  - Derived metadata: 24 months
  - Audit logs: 36 months
- [ ] Implement scheduled deletion jobs.
- [ ] Add delete-by-user request endpoint workflow.

## Security Controls
- [x] JWT auth and RBAC implemented.
- [x] TLS reverse proxy config added (dev ingress).
- [x] Audit logs enabled for sensitive operations.
- [ ] Key rotation policy automated for production secrets.

## Governance
- [ ] Appoint data protection owner.
- [ ] Complete DPIA for pilot districts.
- [ ] Final legal review before production rollout.
