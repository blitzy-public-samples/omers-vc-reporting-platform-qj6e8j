# Security Policy

The **OMERS Ventures Backend Platform** is a Python/FastAPI microservices system that manages financial reporting metrics for OMERS Ventures' portfolio companies on Microsoft Azure (see the [project README](README.md) for a component overview). This document defines the platform's security policy and coordinated-disclosure process, and summarizes the security-remediation engagement carried out against the codebase, including advisories that remain under documented CI waivers and pre-existing defects that are out of scope and remain open (see [Known Issues and Deferred Items](#known-issues-and-deferred-items)). The full rationale for every remediation decision is maintained separately in the [security decision log](docs/security/decision-log.md).

## Supported Versions

This repository does not follow a formal versioning scheme. Security updates are applied to the latest `main` line only; older commits and forks are not maintained.

| Version | Supported |
|---------|-----------|
| `main` (latest) | :white_check_mark: |
| Older commits / forks | :x: |

## Reporting a Vulnerability

We take the security of the OMERS Ventures Backend Platform seriously and welcome coordinated, private disclosure of security issues.

- **Where to report:** Email the maintainers privately at **`security@omersventures.com`**. *This address is a placeholder and must be confirmed by the repository maintainers before it is relied upon.* Please do **not** open a public GitHub issue or pull request for an undisclosed vulnerability.
- **What to include:**
  - The affected service and/or file path (for example, `src/backend/api_gateway/config.py`).
  - Clear, step-by-step reproduction instructions.
  - The impact you have observed or believe is possible (confidentiality, integrity, and/or availability).
  - Any relevant logs, request/response captures, or proof-of-concept material, with secrets redacted.
- **Acknowledgement window:** We aim to acknowledge a report within **3 business days** and will keep you informed of remediation progress.
- **Coordinated disclosure:** Please do not publicly disclose the issue until a fix has been released and coordinated disclosure has been agreed with the maintainers.

## Disclosure Handling

Incoming reports are triaged by severity — **Critical / High / Medium / Low** — based on exploitability and impact. Each confirmed finding is remediated with the **least-invasive fix** that fully closes the issue while preserving existing functionality, consistent with the Minimal Change Clause that governed the remediation summarized below.

## Security Remediation Summary

An authoritative discovery pass — combining the OSV.dev advisory database with a manual audit of code, configuration, and infrastructure-as-code — surfaced **72 advisory findings across 16 vulnerable pinned packages**, plus **four non-dependency findings** (permissive CORS, weak fallback secrets, a hard-coded Terraform database credential, and container-hardening gaps). These findings were addressed with minimal, targeted changes that preserve existing functionality and workflows, with two documented exceptions: advisories whose only fix would breach the frozen compatibility envelope (notably `starlette`, held below 0.51 by the FastAPI `< 0.126` / Pydantic v1 ceiling) or whose fix is not installable on a service's runtime (`click` on the Python 3.9 services), together with the AAP-deferred `pytest` and `loguru` advisories, remain under documented CI waivers rather than being cleared; and several pre-existing, out-of-scope defects — which block some service test suites from collecting — are retained for separately scoped work. Both categories are enumerated under [Known Issues and Deferred Items](#known-issues-and-deferred-items) below.

### Dependency Upgrades

Vulnerable pins were raised to the minimal patched versions that clear each advisory. Clean dependencies were left unchanged.

| Package | Current | Patched To | CVE / Advisory | Severity |
|---------|---------|------------|----------------|----------|
| cryptography | 3.4.8 | 49.0.0 | CVE-2023-50782, CVE-2023-0286, CVE-2024-0727 (+ others) | Critical |
| gunicorn | 20.1.0 | 23.0.0 | CVE-2024-1135, CVE-2024-6827 | High |
| PyJWT | 2.3.0 | 2.13.0 | CVE-2022-29217 | High |
| requests | 2.26.0 / 2.27.1 / 2.31.0 | 2.34.2 (data-transformation function: 2.33.0) | CVE-2024-47081, CVE-2024-35195, CVE-2023-32681, PYSEC-2026-2275 | High |
| fastapi | 0.68.0 / 0.68.1 | 0.125.0 | CVE-2024-24762 | High |
| azure-identity | 1.7.0 | 1.16.1 | CVE-2024-35255 | High |
| pydantic | 1.8.2 | 1.10.13 | CVE-2024-3772 | Medium |
| httpx (test) | 0.18.2 | 0.27.0 | CVE-2021-41945 | Medium |
| python-dotenv | 0.19.0 / 0.19.2 | 1.2.2 | CVE-2026-28684 | Medium |

**Compatibility note:** Pydantic stays on the v1 line (preserves the `BaseSettings` API used throughout the codebase); FastAPI is capped `< 0.126.0` to retain Pydantic v1 support.

### Code & Configuration Fixes

- **CORS (CWE-942 / OWASP A05:2021):** Removed the `allow_origins=["*"]` + `allow_credentials=True` combination. Services now consume an explicit, operator-supplied origins allow-list; the API gateway environment-variable binding was corrected to `CORS_ALLOW_ORIGINS`; and the metrics-input service gained its previously missing `CORS_ORIGINS` setting.
- **Weak secrets (CWE-798 / CWE-259 / OWASP A02:2021 & A07:2021):** Removed the fallback defaults (`"your-secret-key"`, `"your-secret-key-here"`) and the credential-bearing default `DATABASE_URL`. Signing keys and database URLs are now required from the environment with a minimum-length guard (minimum 32 characters), mirroring the pattern already used by the authentication service and API gateway.
- **IaC credential (CWE-798):** Removed the plaintext PostgreSQL administrator password from `infrastructure/terraform/main.tf`; it now references the pre-declared sensitive variable `var.postgresql_admin_password`.
- **Container hardening (CWE-250):** The authentication and reporting-metrics Dockerfiles add a dedicated non-root `USER` and advance off the end-of-life `python:3.8-slim` base image to the supported `python:3.10-slim` (built images run as uid 1000).
- **CI/CD gate:** A `pip-audit` dependency-vulnerability scan stage was added to `infrastructure/azure-pipelines/azure-pipelines.yml` so future regressions are caught automatically.

### Security Verification

Dependency-vulnerability scan. In CI this runs per manifest on each service's actual runtime (Python 3.10 for `authentication_service`, `reporting_financials_service`, and `reporting_metrics_service`; Python 3.9 for `api_gateway` and `metrics_input_service`; Python 3.11 for the data-transformation function), with documented `--ignore-vuln` waivers for the advisories listed under [Known Issues and Deferred Items](#known-issues-and-deferred-items). The gate passes when **no un-waived advisory** remains — not that every advisory is cleared:

```bash
pip-audit -r src/backend/<service>/requirements.txt
```

Security and regression tests (per service; pytest does not enter watch mode). Some suites currently skip or fail to collect because of the pre-existing, out-of-scope defects listed under [Known Issues and Deferred Items](#known-issues-and-deferred-items); those suites reference the specific blocker so it stays visible rather than passing silently:

```bash
cd src/backend/<service> && python -m pytest -v --tb=short
```

Infrastructure validation:

```bash
cd infrastructure/terraform && terraform validate && terraform fmt -check
```

Container non-root verification (expect a non-zero uid):

```bash
docker build -t svc . && docker run --rm svc id -u
```

Residual-secret scan (expect no matches):

```bash
grep -rn "H@Sh1CoR3!\|your-secret-key" src infrastructure
```

## Known Issues and Deferred Items

This section discloses the advisories and defects that remain open after the engagement, so the remediation summary above is not read as a clean-slate claim.

**Advisories retained under documented CI `--ignore-vuln` waivers.** Each is recorded explicitly in the pipeline; its only fix would either breach the frozen compatibility envelope or is not installable on the affected service's runtime:

- **`starlette`** (PYSEC-2026-161, -248, -249, -2280, -2281) — the fix requires FastAPI `>= 0.126`, which drops Pydantic v1; `starlette` is therefore held below 0.51 by the compatibility ceiling.
- **`click`** (PYSEC-2026-2132) — on the Python 3.9 services (`api_gateway`, `metrics_input_service`) only; the fix requires Python `>= 3.10`.
- **`pytest`** (PYSEC-2026-1845) and **`loguru`** (PYSEC-2022-14) — AAP-deferred (see the follow-ups below).

**Pre-existing, out-of-scope defects that block some checks.** These are retained for separately scoped work; the affected test suites skip with a reference to the specific blocker rather than passing silently:

- A circular import in `src/backend/api_gateway/app/routers` prevents the API gateway application from importing, so its CORS regression suite skips.
- The reporting-financials application misuses `Config.DATABASE_URL`, preventing its package from importing; its security suites skip and the settings class is tested directly instead.
- Pre-existing defects in the reporting-metrics and metrics-input services (an unsupported SQLAlchemy `UUID` import / missing modules, and a stray syntax fragment) now surface at collection rather than being suppressed.
- The `terraform validate` verification step above currently fails on pre-existing duplicate variable/backend declarations in `infrastructure/terraform/`; the Terraform layer is to be repaired under separately scoped work.

**Deferred follow-ups** — outside the scope of this security-remediation engagement and recorded here as recommended next steps; they are **not** addressed by the changes summarized above:

- **`pytest` 6.x → 9.x** (test-only; local symlink attack vector) — deferred; the three-major-version jump risks breaking the existing test suite.
- **`loguru` advisory** — informational and Windows-specific — deferred.
- **End-of-life PostgreSQL v11 engine version** — follow-up.
- **Hard-coded placeholder demo credentials (`testuser` / `testpassword`)** — belong to an architectural authentication rework — follow-up.
- **Mis-wired CI Test-stage paths and the missing root Dockerfile referenced by the pipeline** — follow-up.
- **Broad observability build-out** (distributed tracing, Prometheus metrics wiring, Application Insights integration) — beyond the security-event logging added in this engagement — follow-up.
- **No dependency lockfiles exist** — the manifests pin only top-level packages, so transitive versions float; introducing lockfiles is a recommended follow-up.

## Rationale and Decision Log

The full rationale, the alternatives considered, and the residual risk for every non-trivial remediation decision are recorded in [`docs/security/decision-log.md`](docs/security/decision-log.md), which is the single source of truth for that rationale. Code comments were kept minimal and factual (naming the control and its CVE/CWE identifier); the explanatory detail lives solely in the decision log.

## Standards

Mappings applied: **OWASP Top 10** — A02:2021 (Cryptographic Failures), A05:2021 (Security Misconfiguration), A06:2021 (Vulnerable and Outdated Components), and A07:2021 (Identification and Authentication Failures); and **CWE** — CWE-942 (Overly Permissive CORS), CWE-798 (Use of Hard-coded Credentials), CWE-259 (Use of Hard-coded Password), and CWE-250 (Execution with Unnecessary Privileges).
