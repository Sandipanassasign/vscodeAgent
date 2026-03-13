# Release Readiness Checklist — Monitoring & Observability

## Monitoring Readiness

### Logging
- Structured logging implemented (JSON format preferred)
- Log levels appropriately set (ERROR, WARN, INFO, DEBUG)
- Application logs forwarded to centralized log management (Splunk/ELK)
- Log retention policy set (minimum 90 days)
- No sensitive data logged (PII, credentials)

### Metrics & Dashboards
- Application health dashboard created and reviewed
- Key business metrics tracked (conversion rate, error rate, latency)
- Infrastructure metrics monitored (CPU, memory, disk, network)
- Database performance metrics visible

### Alerting
- P1 alert: error rate > 5% — PagerDuty/OpsGenie notification
- P2 alert: latency > 3x baseline — team Slack notification
- P1 alert: service down — immediate on-call page
- Alert runbooks documented for all P1/P2 alerts
- Oncall rotation updated for release window

### Tracing
- Distributed tracing enabled (Jaeger/Zipkin/Datadog APM)
- Critical user journeys traced end-to-end
- Trace sampling rate set appropriately

### Synthetic Monitoring
- Synthetic monitors created for critical user flows
- Monitor running in production region
- Alert configured if synthetic monitor fails

## Post-Release Monitoring Protocol
- Dedicated engineer watching dashboards for first 30 minutes
- Hourly check-ins for first 4 hours post-release
- Daily review of metrics for first 7 days
- Rollback ready to trigger within 15 minutes if required
