# Security Observability Dashboard (Template)

This document is a **template**. It describes the dashboard **panels** an operator would build for the **security-event signals** introduced by the security-vulnerability remediation on the OMERS Ventures Backend Platform. It intentionally contains **panel descriptions and illustrative log-field names only** — there are no live queries, dashboard definitions, connection strings, or credentials in this file.

The remediation did **not** introduce any new monitoring infrastructure. The security-event signals are emitted as **structured log records that carry a correlation identifier and a service name**, built entirely on the **reused standard-library `logging`** configuration already present in the services and on the existing **`/health`** endpoints on the **API gateway** and the **reporting-metrics service**. No tracing backend, metrics backend, or new monitoring agent was added.

An operator would construct the panels described below in whatever log-aggregation backend the platform is configured to use (for example, **Azure Monitor / Azure Log Analytics**, per the product specification). This remediation does **not** implement, configure, or verify any such collection integration; it only emits the security-event records onto the reused standard-library `logging` stream. Collecting those records and building the panels remains an **operator responsibility** and is a deferred follow-up (see below).

- **Scope:** three security-event panels plus a deferred-work note. Nothing beyond security-relevant signals is described here.
- **Signal shape:** every panel is driven by structured log records that include, at minimum, a `correlation_id` (for request-level drill-down) and a `service` name (for per-service breakdown).
- **Field names are illustrative:** identifiers such as `timestamp`, `service`, `correlation_id`, `outcome`, and `origin` are examples of the fields a panel would read, not a fixed schema contract.

## Panel: Authentication Failures

- **Metric / visualization:** rate or count of authentication failures over time, rendered as a time-series (line or bar) chart.
- **Suggested breakdown dimensions:** broken down by `service`, distinguishing failures observed at the authentication service from those observed at the API gateway; an aggregate total line may be overlaid.
- **Correlation & service context:** each underlying log record carries a `correlation_id` (available for per-request drill-down) and the emitting `service` name, so a spike in the panel can be pivoted to the individual failing requests.
- **Signal source:** the security-event log record emitted on an authentication failure by the authentication service and the API gateway.

## Panel: Token-Validation Failures

- **Metric / visualization:** count or rate over time of JWT decode/verify rejections, rendered as a time-series chart.
- **Suggested breakdown dimensions:** broken down by `service`, and optionally by rejection reason (for example, invalid signature, expired token, or malformed token) where the log record distinguishes them.
- **Correlation & service context:** each underlying log record carries a `correlation_id` and the emitting `service` name for drill-down and per-service attribution.
- **Signal source:** the `token_validation_failure` security-event record emitted when a token is rejected at a service's authentication boundary (the authentication service's protected route and the API gateway's token dependency and authentication middleware). The underlying `validate_token` decode enforces `algorithms=["HS256"]`; this panel makes those rejections observable.

## Panel: CORS Rejections

- **Metric / visualization:** count or rate over time of requests from unlisted or untrusted origins that were rejected, rendered as a time-series chart.
- **Suggested breakdown dimensions:** broken down by `service` and by `origin`, so operators can see which untrusted origins are attempting access and against which service.
- **Correlation & service context:** each underlying log record carries a `correlation_id`, the emitting `service` name, and the rejected `origin`.
- **Signal source:** the rejected cross-origin request log record. This panel validates the CORS hardening — no wildcard `Access-Control-Allow-Origin` is combined with credentials, and only configured origins are reflected.

## Panel → Signal Mapping

The table below maps each panel to the log event that feeds it and the key fields a panel would read. The field names are illustrative rather than a schema contract.

| Panel | Signal source (log event) | Key fields |
|-------|---------------------------|------------|
| Authentication failures | Auth-failure security-event log record | `timestamp`, `service`, `correlation_id`, `outcome` |
| Token-validation failures | JWT decode/verify rejection log record | `timestamp`, `service`, `correlation_id`, `outcome` |
| CORS rejections | Rejected cross-origin request log record | `timestamp`, `service`, `correlation_id`, `origin`, `outcome` |

## Deferred Follow-ups

The following observability capabilities exceed the scope of this security fix and were recorded as recommended next steps, not undertaken as part of this engagement.

- **Log-collection wiring and dashboard construction** — routing the emitted security-event records into a log-aggregation backend (for example, Azure Monitor / Log Analytics) and building the panels above is **not** implemented or configured by this remediation (operator follow-up).
- **Full distributed tracing** — not implemented (recommended follow-up).
- **Wiring the declared-but-unused `prometheus-client` metrics endpoint** — not implemented (recommended follow-up).
- **Application Insights integration** — not implemented (recommended follow-up).
