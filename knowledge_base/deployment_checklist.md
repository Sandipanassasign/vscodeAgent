# Release Readiness Checklist — Deployment

## Pre-Deployment Checklist

### Infrastructure & Environment
- Target environment (staging/prod) provisioned and validated
- Infrastructure-as-code (Terraform/CloudFormation) reviewed and applied
- Environment variables and secrets configured in secret manager
- Database migrations tested in staging, rollback script available
- CDN and caching configurations updated

### CI/CD Pipeline
- All CI checks (lint, unit tests, integration tests) passing on main branch
- Deployment pipeline tested end-to-end in staging environment
- Artifact versioning confirmed (docker image, build tag)
- Zero-downtime deployment strategy validated (Blue/Green or Rolling)

### Deployment Steps
1. Notify stakeholders of deployment window
2. Enable maintenance mode (if applicable)
3. Take database backup
4. Deploy application artifact
5. Run smoke tests post-deploy
6. Monitor dashboards for 15 minutes
7. Disable maintenance mode
8. Notify stakeholders — deployment complete

### Rollback Plan
- Rollback procedure documented and reviewed
- Previous stable version artifact available
- Rollback triggers defined (error rate > 5%, latency > 3x baseline)
- Rollback tested in staging
- On-call engineer identified and available during deployment

### Post-Deployment
- Smoke tests passing in production
- Synthetic monitoring configured
- Feature flags enabled/disabled as planned
- Runbook updated with new deployment details

## Go/No-Go Criteria
- All deployment checklist items complete: GO
- Any P1 blocker or untested rollback: NO-GO
