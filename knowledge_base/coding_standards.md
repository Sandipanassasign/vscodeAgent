# 💻 Coding Standards & Best Practices (Banking Edition)

Guidelines for our development teams to ensure high-integrity, audit-friendly financial systems.

## 💰 Financial Precision & Math
- **Money Types**: Never use `float` or `double` for currency. Always use `Decimal` (Python) or `BigDecimal` (Java) to avoid IEEE 754 rounding errors.
- **Rounding**: Default to "Round Half Even" (Banker's Rounding) for all transaction calculations unless specified otherwise by local law.
- **Precision**: Maintain at least 4-8 decimal places in intermediate calculations for multi-currency conversions.

## 🔄 Idempotency & Concurrency
- **Idempotency Keys**: All Payment/Transfer APIs must require an `X-Idempotency-Key` to prevent duplicate transactions on network retry.
- **Pessimistic Locking**: Use database-level row locking for account balance updates to prevent race conditions.

## 🕵️ Audit & Logging
- **Correlation IDs**: Every request must carry a unique `Correlation-ID` across all microservices for troubleshooting.
- **Audit Fields**: Every record must include `created_by`, `updated_by`, `created_at`, and `source_ip`.
- **Sensitive Data**: Log strings must be stripped of PII (PAN, CVV, Passwords) using a centralized masking utility.

## 🏗️ Automation Testing Standards
- **Contract Tests**: Mandatory for all inter-departmental APIs.
- **Chaos Engineering**: Weekly simulations of Database failovers and Latency spikes in staging.
- **Test Data**: Never use production data for testing; use anonymized or synthetic data generators.
