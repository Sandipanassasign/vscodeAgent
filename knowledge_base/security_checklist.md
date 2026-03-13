# Release Readiness Checklist — Security

## Security Readiness for Production Release

### Code Security
- Static Application Security Testing (SAST) scan completed — no critical findings
- Software Composition Analysis (SCA) run — no critical CVEs in dependencies
- Secrets scanning run — no hardcoded API keys, passwords, or tokens in codebase
- Code review by security-aware team member completed

### Authentication & Authorization
- MFA enforced for all admin accounts
- Role-based access control (RBAC) implemented and tested
- JWT/session token expiry configured correctly
- OAuth2/OIDC flows tested with edge cases

### Data Security
- PII data identified and classified
- PII encrypted at rest (AES-256 or equivalent)
- Data in transit encrypted with TLS 1.2+
- Database access restricted to application service account only
- Backup encryption verified

### API Security
- Rate limiting configured on all public-facing endpoints
- Input validation and sanitization implemented
- SQL injection and XSS protection in place
- CORS policy reviewed and tightened for production

### Infrastructure Security
- Network security groups / firewall rules reviewed
- Unnecessary ports closed
- VPN or private network access enforced for admin interfaces
- Logging and audit trail enabled for security events

### Compliance
- GDPR/DPDP data processing agreements in place (if applicable)
- Data retention policy implemented
- Privacy policy updated to reflect new features
- Security sign-off from CISO/security team received

## Security Go/No-Go Criteria
- No critical or high severity unresolved vulnerabilities: GO
- Any critical unpatched CVE or compliance gap: NO-GO
