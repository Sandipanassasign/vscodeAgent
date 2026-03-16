# Release Readiness Checklist — Monitoring (Banking Edition)

## 📈 Banking Business Observability

### 💸 Critical Transaction Metrics
- [ ] **Transaction Success Rate (TSR)**: Real-time alerting if success rate for fund transfers drops < 99.9%.
- [ ] **Average Latency**: Track time-to-complete for ATM and Point-of-Sale (POS) api calls (Threshold: < 500ms).
- [ ] **Settlement Backlog**: Monitor queues for ACH and SWIFT message settlements.
- [ ] **Authorization Failures**: Distinguish between user errors (insufficient funds) and system errors.

### 🕵️ Security & Fraud Monitoring
- [ ] **Velocity Checks**: Alert on abnormal spikes in transaction volume per user/IP.
- [ ] **MFA Success/Fail**: Monitor rates of second-factor authentication failures.
- [ ] **SIEM Integration**: Real-time export of access logs to the Security Operations Center (SOC).

---

## 🖥️ Operational Dashboards
- [ ] **API Health**: Traffic and error rates for all B2B and Internal Core Banking APIs.
- [ ] **Database Health**: Active connections, lock contention, and replication lag for the Ledger DB.
- [ ] **Partner Health**: Status page monitors for downstream payment providers and cloud infrastructure.

---

## 🚨 Alerts & On-Call
- **P1 (CRITICAL)**: Any spike in 5xx errors on the Transfer API → Immediate Page.
- **P1 (CRITICAL)**: HSM Connectivity Loss → Immediate Rollback.
- **P2 (WARN)**: Latency increase on non-critical path (e.g., Statement generation) > 2s.


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
