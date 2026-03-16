# 🐞 Incident & Bug History (Banking Edition)

This file tracks major incidents and common bugs to help the Bug Analysis Agent identify recurring patterns in our financial systems.

## Incident Log
- **INC-2024-001**: Database connection pool exhaustion during peak salary processing.
  - **Resolution**: Scaled pool size and added monitoring for idle connections.
- **INC-2024-002**: Memory leak in Auth Service causing logout loops on Mobile.
  - **Resolution**: Patched JWT library and added nightly restarts as a stop-gap.
- **INC-2024-003**: SWIFT message delay due to invalid character encoding in BIC headers.
  - **Resolution**: Added strict regex validation for all outbound payment messages.

## Common Bug Patterns
- **Currency Precision Loss**: Caused by unintentional `float` conversions in legacy middleware.
- **Duplicate Transfers**: Occurs when retry logic lacks an Idempotency Key check.
- **API Timeout in VDI**: Often caused by proxy latency within the virtual environment.

## Debugging Checklist
- Check logs for "503 Service Unavailable" from Payment Gateways.
- Verify HSM connectivity status.
- Ensure proxy settings are correct for SWIFT/ACH endpoints.
