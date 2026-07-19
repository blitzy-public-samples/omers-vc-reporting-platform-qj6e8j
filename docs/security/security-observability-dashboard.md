# Security Observability Dashboard (Template)

This document is a **template**. It describes the dashboard **panels** an operator would build for the **security-event signals** introduced by the security-vulnerability remediation on the OMERS Ventures Backend Platform. It intentionally contains **panel descriptions and illustrative log-field names only** — there are no live queries, dashboard definitions, connection strings, or credentials in this file.

The remediation did **not** introduce any new monitoring infrastructure. The security-event signals are emitted as **structured log records that carry a correlation identifier and a service name**, built entirely on the **reused standard-library `logging`** configuration already present in the services and on the existing **`/health`** endpoints on the **API gateway** and the **reporting-metrics service**. No tracing backend, metrics backend, or new monitoring agent was added.

An operator would construct the panels described below in whatever log-aggregation backend the platform is configured to use (for example, **Azure Monitor / Azure Log Analytics**, per the product specification). This remediation does **not** implement, configure, or verify any such collection integration; it only emits the security-event records onto the reused standard-library `logging` stream. Collecting those records and building the panels remains an **operator responsibility** and is a deferred follow-up (see below).

- **Scope:** three security-event panels plus a deferred-work note. Nothing beyond security-relevant signals is described here.
- **Signal shape:** every panel is driven by the single structured (JSON) security-event record emitted by `log_security_event(...)` in `authentication_service/app/security.py`. Every record carries these keys: `security_event` (the event type), `service` (emitting service), `outcome`, and `correlation_id` (for request-level drill-down); per-event extra fields are added as noted per panel. The record does **not** itself embed a `timestamp` — the wall-clock time is supplied by the standard-library `logging` handler/formatter that writes the record, so a panel reads it from the log line's timestamp rather than from the JSON payload.
- **Event types emitted (the contract):** `authentication_failure` (outcome `denied`), `token_validation_failure` (outcome `denied`), and `cors_origin_not_allowed` (outcome `not_allowed`). No other security-event types are emitted.

## Panel: Authentication Failures

- **Metric / visualization:** rate or count of authentication failures over time, rendered as a time-series (line or bar) chart.
- **Suggested breakdown dimensions:** broken down by `service`, distinguishing failures observed at the authentication service from those observed at the API gateway; an aggregate total line may be overlaid.
- **Event fields:** `security_event = "authentication_failure"`, `outcome = "denied"`, `service`, `correlation_id`, and a `subject` field carrying a **pseudonymized** (hashed) form of the attempted username — never the raw credential.
- **Correlation & service context:** each record carries a `correlation_id` (for per-request drill-down) and the emitting `service` name, so a spike in the panel can be pivoted to the individual failing requests.
- **Signal source:** the `authentication_failure` record emitted on a failed login by the authentication service (`main.py`) and the API gateway (`main.py`).

## Panel: Token-Validation Failures

- **Metric / visualization:** count or rate over time of JWT decode/verify rejections, rendered as a time-series chart.
- **Event fields:** `security_event = "token_validation_failure"`, `outcome = "denied"`, `service`, `correlation_id`, and a `reason` field. The `reason` values actually emitted are `invalid_token`, `decode_error`, and `missing_subject`, plus — at the authentication service's protected route — the PyJWT exception class name (for example `ExpiredSignatureError`, `InvalidSignatureError`). The `reason` values are heterogeneous across call sites and are intended for coarse triage, not as a stable enumerated taxonomy.
- **Suggested breakdown dimensions:** broken down by `service`, and optionally by the `reason` field noted above.
- **Correlation & service context:** each record carries a `correlation_id` and the emitting `service` name for drill-down and per-service attribution.
- **Signal source:** the `token_validation_failure` record emitted when a token is rejected at a service's authentication boundary (the authentication service's protected route, `main.py`; and the API gateway's token dependency in `main.py`, plus the authentication middleware in the non-deployed alternate factory `app/__init__.py`). The underlying `validate_token` decode enforces `algorithms=["HS256"]`; this panel makes those rejections observable. Note: the deployed gateway entrypoint (`app = create_app()` in `main.py`) validates the bearer token exactly once via a single `OAuth2PasswordBearer` dependency (remediated in commit `655a630`; see `SECURITY.md` → Known Issues), so its counts are not inflated by re-decoding. The re-decode caveat — where a `token_validation_failure` can also fire for an otherwise-valid token, making gateway counts a superset — applies only to the non-deployed `app/__init__.py` authentication middleware, until that alternate factory is unified with the deployed path.

## Panel: Unlisted-Origin Cross-Origin Requests (observability signal)

- **Metric / visualization:** count or rate over time of requests that carry an `Origin` header not on the configured allow-list, rendered as a time-series chart.
- **Important semantics — this is an observability signal, not a server rejection:** the server does **not** reject or alter these requests. `CORSMiddleware` simply does not echo an `Access-Control-Allow-Origin` header for an unlisted origin, so the browser withholds the credentialed response on the client side. The middleware emits the signal and adds the correlation id to the response headers; it never changes the response status or body. Panels and alerts must therefore be worded as "unlisted-origin request observed," not "request blocked/rejected."
- **Event fields:** `security_event = "cors_origin_not_allowed"`, `outcome = "not_allowed"`, `service`, `correlation_id`, and the observed `origin` (sanitized before it enters the record — an attacker-controlled `Origin` header cannot inject additional log fields, CWE-117).
- **Suggested breakdown dimensions:** broken down by `service` and by `origin`, so operators can see which unlisted origins are attempting access and against which service.
- **Signal source:** the `cors_origin_not_allowed` record emitted by the shared middleware in `authentication_service/app/security.py` (`install_security_logging`). This panel gives visibility into the CORS hardening — no wildcard `Access-Control-Allow-Origin` is combined with credentials, and only configured origins are reflected.

## Panel → Signal Mapping

The table below maps each panel to the `security_event` value that feeds it and the record fields a panel reads. These are the fields actually emitted by `log_security_event(...)`; the `timestamp` column is supplied by the logging handler that writes the record (see the intro), not by the JSON payload.

| Panel | `security_event` (and `outcome`) | Record fields |
|-------|----------------------------------|---------------|
| Authentication failures | `authentication_failure` (`denied`) | `service`, `correlation_id`, `subject` (pseudonymized) + handler `timestamp` |
| Token-validation failures | `token_validation_failure` (`denied`) | `service`, `correlation_id`, `reason` + handler `timestamp` |
| Unlisted-origin cross-origin requests | `cors_origin_not_allowed` (`not_allowed`) | `service`, `correlation_id`, `origin` + handler `timestamp` |

## Deferred Follow-ups

The following observability capabilities exceed the scope of this security fix and were recorded as recommended next steps, not undertaken as part of this engagement.

- **Log-collection wiring and dashboard construction** — routing the emitted security-event records into a log-aggregation backend (for example, Azure Monitor / Log Analytics) and building the panels above is **not** implemented or configured by this remediation (operator follow-up).
- **Full distributed tracing** — not implemented (recommended follow-up).
- **Wiring the declared-but-unused `prometheus-client` metrics endpoint** — not implemented (recommended follow-up).
- **Application Insights integration** — not implemented (recommended follow-up).
