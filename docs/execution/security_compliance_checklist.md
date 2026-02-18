# Security and Compliance Checklist (Phase Gate)

## Security Baseline
- [x] JWT token issuance and protected API dependencies scaffolded.
- [ ] OTP verification integrated with SMS provider.
- [x] TLS 1.3 configured at ingress/load balancer.
- [x] Audit logging scaffold enabled (`backend/audit.log`).
- [x] Role-based authorization checks implemented per endpoint.

## Compliance Prep
- [ ] Consent text and data purpose statements in mobile app.
- [ ] Data retention and deletion policy document approved.
- [x] DPA/DPDP controls mapped for personal and farm data.
- [ ] Encryption key rotation process documented.
