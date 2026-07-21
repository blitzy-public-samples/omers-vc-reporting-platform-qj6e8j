# Blitzy Project Guide — OMERS VC Reporting Platform Security Remediation

> **Engagement type:** Security vulnerability remediation (Minimal Change Clause)
> **Stack:** Python / FastAPI microservices on Microsoft Azure
> **Branch:** `blitzy-c9b156c8-1da5-413c-bbf6-2dcac483d52c` @ HEAD `afaff43`
> **AAP‑scoped completion:** **87.5%** (105 h completed / 120 h total)

---

## 1. Executive Summary

### 1.1 Project Overview

This engagement hardened the **OMERS VC Reporting Platform** — a Python/FastAPI microservices system (five backend services plus one Azure Function) deployed on Microsoft Azure — against a multi‑layer set of discovered security vulnerabilities. Working under a binding **Minimal Change Clause**, Blitzy remediated vulnerable open‑source dependencies, an overly permissive CORS posture, weak/predictable fallback secrets, a hard‑coded database credential in Terraform, and container‑hardening gaps, then added a CI dependency‑scan gate, security‑event logging, regression tests, and mandated documentation. Every edit is traceable to a specific CVE or CWE while preserving all existing endpoints, workflows, and the Pydantic v1 API surface. The result eliminates the identified findings and prepares the platform for a secure production deployment.

### 1.2 Completion Status

The completion percentage is computed strictly on **AAP‑scoped work plus path‑to‑production activities** (PA1 methodology). All security‑remediation development is delivered and independently verified; the remaining effort is operational deployment provisioning that requires human action in the target environment.

```mermaid
%%{init: {'theme':'base', 'themeVariables': {'pie1':'#5B39F3','pie2':'#FFFFFF','pieStrokeColor':'#B23AF2','pieStrokeWidth':'2px','pieOuterStrokeWidth':'2px','pieTitleTextSize':'18px','pieSectionTextSize':'15px','pieLegendTextSize':'14px'}}}%%
pie showData title Completion — 87.5% Complete (105 h of 120 h)
    "Completed Work (AI)" : 105
    "Remaining Work" : 15
```

| Metric | Hours |
|--------|-------|
| **Total Hours** | **120** |
| Completed Hours (AI) | 105 |
| Completed Hours (Manual) | 0 |
| **Completed Hours (AI + Manual)** | **105** |
| **Remaining Hours** | **15** |
| **Percent Complete** | **87.5%** |

> Calculation: `105 / (105 + 15) × 100 = 87.5%`. Completed = 105 h of AAP‑scoped remediation delivered by Blitzy agents; Remaining = 15 h of path‑to‑production operational provisioning. No manual (human) hours have been logged against this branch to date.

### 1.3 Key Accomplishments

- ✅ **Dependency layer:** All nine advisory‑listed packages upgraded to patched pins across six `requirements.txt` manifests (`fastapi==0.125.0`, `pydantic==1.10.13` v1 line, `PyJWT==2.13.0`, `cryptography==49.0.0`, `gunicorn==23.0.0`, `azure-identity==1.16.1`, `requests==2.34.2/2.33.0`, patched `python-dotenv`, plus transitive `h11>=0.16.0` and `urllib3==2.7.0`). `pip-audit` reports zero unignored advisories.
- ✅ **CORS (CWE‑942):** Wildcard‑plus‑credentials removed from all affected services; explicit non‑wildcard allow‑lists with fail‑closed validators that reject `*`; the `CORS_ALLOW_ORIGINS` env‑name mismatch corrected; the missing `metrics_input_service` CORS setting added.
- ✅ **Weak secrets (CWE‑798/259):** `JWT_SECRET_KEY` and `SECRET_KEY` now required from the environment with a 32‑character minimum; `DATABASE_URL` required; insecure defaults removed; services fail‑closed on misconfiguration.
- ✅ **IaC credential (CWE‑798):** Plaintext PostgreSQL password removed from `main.tf` in favor of the sensitive `var.postgresql_admin_password`; residual‑secret scan is clean; `terraform validate` succeeds.
- ✅ **Container hardening (CWE‑250):** `authentication_service` and `reporting_metrics_service` moved off end‑of‑life `python:3.8-slim` to `python:3.10-slim` and run as a non‑root user (uid 1000).
- ✅ **CI gate:** `pip-audit` `SecurityScan` stage added to Azure Pipelines with `Build → Test → SecurityScan → Deploy` gate ordering.
- ✅ **Security‑event logging (FR‑8.5/FR‑10.6):** Structured, correlation‑ID‑tagged records for authentication failures, token‑validation failures, and CORS rejections, reusing existing logging.
- ✅ **Testing:** 8 new security regression suites — **83 tests, 100% passing** (independently re‑run this session).
- ✅ **Documentation:** `SECURITY.md`, `docs/security/decision-log.md`, `docs/security/security-observability-dashboard.md`, a self‑contained reveal.js executive deck, and updated root + five service READMEs.

### 1.4 Critical Unresolved Issues

There are **no unresolved defects in the AAP‑scoped security remediation** — every in‑scope layer is delivered, tested, and verified. The items below are operational prerequisites that must be completed by humans before production deployment (they are not code defects).

| Issue | Impact | Owner | ETA |
|-------|--------|-------|-----|
| Production secrets not yet provisioned (`SECRET_KEY`, `JWT_SECRET_KEY` ≥32 chars, `DATABASE_URL`) | Services fail‑closed at import until set (intended hardening); blocks deploy | DevOps / Platform | 0.5 day |
| Terraform DB admin password not yet supplied at apply time (`var.postgresql_admin_password`) | `terraform apply` requires the secret; blocks infra provisioning | DevOps / Platform | 0.25 day |
| Real CORS origins not yet declared per environment | Browser‑facing calls fail until real origins configured | DevOps / Frontend | 0.25 day |

### 1.5 Access Issues

No access issues were encountered that blocked autonomous validation. Docker, Terraform, and the six service dependency sets were all exercisable in the validation environment, and the git tree is clean and up to date with `origin`.

| System / Resource | Type of Access | Issue Description | Resolution Status | Owner |
|-------------------|----------------|-------------------|-------------------|-------|
| Azure subscription / Key Vault | Deployment credentials | Production secret stores are not reachable from the build environment (expected); needed for HT‑1/HT‑2 | Pending human provisioning | DevOps / Platform |
| Live Azure DevOps project | Pipeline execution | The `SecurityScan` gate is defined in YAML but not yet exercised in a live run | Pending human enablement (HT‑4) | DevOps |

> No repository‑permission or source‑access issues exist. The two rows above are standard deployment‑time access prerequisites, not blockers to the completed remediation.

### 1.6 Recommended Next Steps

1. **[High]** Provision the required application secrets (`SECRET_KEY`, `JWT_SECRET_KEY` ≥32 chars, `DATABASE_URL`) in each environment's secret store / pipeline variable group. *(HT‑1)*
2. **[High]** Supply the Terraform PostgreSQL admin password as a sensitive variable / pipeline secret at apply time. *(HT‑2)*
3. **[High]** Declare real CORS allow‑list origins for each environment (`CORS_ALLOW_ORIGINS`, `CORS_ORIGINS`, service‑specific origins). *(HT‑3)*
4. **[Medium]** Enable and validate the CI `SecurityScan` gate in the live Azure Pipelines project. *(HT‑4)*
5. **[Medium]** Run an end‑to‑end integration & deployment smoke verification (services + PostgreSQL + browser CORS + `/health`). *(HT‑5)*

---

## 2. Project Hours Breakdown

### 2.1 Completed Work Detail

| Component | Hours | Description |
|-----------|-------|-------------|
| Vulnerability research & version‑compatibility analysis | 8 | OSV.dev / PyPI / changelog research; established the FastAPI ↔ Pydantic‑v1 (`<0.126.0`) and cryptography ↔ Python ceilings that shape the whole fix |
| Dependency remediation (6 manifests) | 10 | Bumped 9 patched pins + transitive hygiene (`h11`, `urllib3`, per‑runtime `python-dotenv`); confirmed no import breakage; Pydantic held on v1 line |
| CORS hardening — CWE‑942 (4 services) | 16 | Explicit allow‑lists + wildcard‑rejecting validators in `config.py`/`main.py`/`app/__init__.py`; `CORS_ALLOW_ORIGINS` env fix; added missing `metrics_input` setting |
| Weak‑secret remediation — CWE‑798/259 (2 services) | 6 | `JWT_SECRET_KEY`/`SECRET_KEY` required with `min_length=32`; `DATABASE_URL` required; fail‑closed + blank/whitespace validators |
| IaC credential remediation — CWE‑798 | 2 | `main.tf` now references `var.postgresql_admin_password`; plaintext literal removed |
| Container hardening — CWE‑250 (2 Dockerfiles) | 5 | Non‑root `USER` + base image advanced off EOL `python:3.8-slim` → `3.10-slim`; `.dockerignore` added |
| Security‑event logging — FR‑8.5/FR‑10.6 (2 services) | 7 | `log_security_event` + `get_correlation_id`; auth/token/CORS‑rejection events with correlation IDs, reusing stdlib logging |
| CI `SecurityScan` gate | 5 | `pip-audit==2.9.0` stage, per‑runtime groups, curated ignore‑lists, `Build→Test→SecurityScan→Deploy` ordering |
| Security regression test suites | 16 | 8 new files, 83 tests: CORS regression, secret‑required config, JWT `algorithms=["HS256"]` assertion |
| Rule‑mandated documentation | 18 | `SECURITY.md`, decision‑log table, observability dashboard template, six READMEs, self‑contained reveal.js executive deck (1,118 lines) |
| Autonomous validation & QA hardening | 12 | 21‑commit iterative review gates; 83‑test verification; terraform/container/secret checks; residual‑secret scans |
| **Total Completed** | **105** | |

### 2.2 Remaining Work Detail

| Category | Hours | Priority |
|----------|-------|----------|
| Provision production application secrets (`SECRET_KEY`, `JWT_SECRET_KEY` ≥32, `DATABASE_URL`) — path‑to‑production for the CWE‑798 fix | 3 | High |
| Provision Terraform PostgreSQL admin password as sensitive var / pipeline secret at apply time — path‑to‑production for the IaC fix | 2 | High |
| Configure real CORS allow‑list origins per environment — path‑to‑production for the CWE‑942 fix | 2 | High |
| Enable & validate CI `SecurityScan` gate in the live Azure Pipelines project | 2 | Medium |
| End‑to‑end integration & deployment smoke verification (services + DB + browser CORS + `/health`) | 6 | Medium |
| **Total Remaining** | **15** | |

> **Cross‑check:** Section 2.1 (105 h) + Section 2.2 (15 h) = **120 h** total, matching Section 1.2. Section 2.2 total (15 h) matches Section 1.2 Remaining Hours and the Section 7 "Remaining Work" value.

### 2.3 Out‑of‑Scope Follow‑ups (not counted in hours)

Per AAP §0.8.2 these are **explicitly outside the remediation scope** and are therefore excluded from the completion percentage and the remaining‑hours total. They are surfaced only so the team understands the full production‑hardening roadmap.

| Follow‑up | Indicative Effort | Notes |
|-----------|-------------------|-------|
| Introduce dependency lockfiles (pip‑tools) | ~3 h | Pins transitive dependencies; AAP‑recommended |
| Upgrade `pytest` 6.x → 9.0.3 + revalidate | ~6 h | Requires Python ≥3.10 on all services; AAP‑deferred |
| Fix pre‑existing `outputs.tf` undeclared‑resource references | ~4 h | Unblocks full‑module `terraform validate/apply`; baseline defect |
| Correct pre‑existing CI Test‑stage paths | ~2 h | `tests/unit` / `tests/integration` do not exist; baseline defect |
| Repair pre‑existing `data_transformation` / `reporting_financials` test defects | ~5 h | Human‑authored test issues; never touched by the security work |
| Broader observability build‑out (tracing, Prometheus, App Insights) | ~16 h | Beyond the security‑event logging in scope |
| Architectural auth rework + EOL PostgreSQL v11 upgrade | TBD | Demo‑credential placeholder replacement; DB engine uplift |

---

## 3. Test Results

All tests below originate from Blitzy's autonomous validation logs for this project and were **independently re‑executed during this assessment** in the validator's exact runtimes (Docker `python:3.9-slim` / `python:3.10-slim`, `PYTHONPATH=/workspace`). Every in‑scope security regression test passes.

| Test Category (Suite) | Framework | Total Tests | Passed | Failed | Coverage % | Notes |
|-----------------------|-----------|-------------|--------|--------|-----------|-------|
| api_gateway security (CORS + config) | pytest + FastAPI `TestClient` | 13 | 13 | 0 | N/A¹ | Wildcard rejection, credentialed‑origin reflection, secret min‑length |
| authentication_service security (CORS + config) | pytest + `TestClient` | 12 | 12 | 0 | N/A¹ | CORS allow‑list, secret required, security‑event logging paths |
| metrics_input_service security (CORS) | pytest + `TestClient` | 15 | 15 | 0 | N/A¹ | New `CORS_ORIGINS` setting + validator behavior |
| reporting_financials_service security (CORS + config) | pytest + `TestClient` | 28 | 28 | 0 | N/A¹ | `JWT_SECRET_KEY` fail‑closed, wildcard rejection |
| reporting_metrics_service security (config) | pytest + `TestClient` | 15 | 15 | 0 | N/A¹ | `SECRET_KEY` min‑length, `DATABASE_URL` required, JWT `HS256` restriction |
| **Total (in‑scope security regression)** | | **83** | **83** | **0** | — | **100% pass** |
| Dependency vulnerability scan | `pip-audit==2.9.0` (6 manifests) | 6 | 6 | 0 | — | "No known vulnerabilities found" per manifest with curated ignore‑lists (7 for Python 3.10, 8 for Python 3.9) |

¹ *Coverage percentage was not instrumented for these suites; they are targeted behavioral security‑regression assertions rather than coverage‑measured unit tests.*

**Out‑of‑scope / pre‑existing test status (transparency, not part of the remediation):** the `data_transformation` suite has 4 pre‑existing assertion failures, `reporting_financials/tests/test_financials.py` has 1 pre‑existing collection `ImportError`, and 11 async tests skip because `pytest-asyncio` has never been in any manifest. Git history confirms these files were never modified by the security work; they are documented in AAP §0.8.2 as out of scope and are excluded from the results above.

---

## 4. Runtime Validation & UI Verification

**Runtime health (all verified in this session):**

- ✅ **api_gateway** — starts via `uvicorn main:create_app --factory`; `/health` and `/openapi.json` return HTTP 200 with correct app identity.
- ✅ **authentication_service** — starts via `uvicorn main:create_app --factory`; app constructs; CORS middleware verified in‑process.
- ✅ **metrics_input_service** — starts via `uvicorn main:app`; `/openapi.json` returns HTTP 200 ("Metrics Input Service", v1.0.0). *(No `/health` route — expected; `/health` exists only on api_gateway and reporting_metrics per design.)*
- ✅ **reporting_financials_service** — starts via `uvicorn main:app`; app constructs cleanly.
- ✅ **reporting_metrics_service** — starts via `uvicorn main:app`; `/health` and `/openapi.json` return HTTP 200.
- ✅ **data_transformation (Azure Function)** — `transform_data()` executes and returns the correct 39‑key result with correct FX math.

**Security‑behavior verification:**

- ✅ CORS: an allowed origin is reflected **with** credentials; a disallowed origin is **not** reflected; `Access-Control-Allow-Origin: *` with `Access-Control-Allow-Credentials: true` is **never** emitted by any service.
- ✅ Secrets: services fail‑closed at import when `SECRET_KEY`/`JWT_SECRET_KEY`/`DATABASE_URL` are absent or too short (intended CWE‑798 hardening).
- ✅ Containers: hardened images run as non‑root uid 1000.
- ✅ IaC: `terraform validate` (`main.tf` + `variables.tf`) → "Success! The configuration is valid."; residual‑secret scan returns zero matches.

**UI verification:** ⚠ **Not applicable.** This platform is a set of backend microservices with no web front‑end in scope. API surfaces were verified via `/openapi.json`, `/health`, and in‑process `TestClient` exercises.

---

## 5. Compliance & Quality Review

Each AAP deliverable is cross‑mapped below to its security benchmark (OWASP Top 10 / CWE) and its verified status. All fixes were already applied and committed before validation; the autonomous validation session confirmed correctness and applied **zero** additional in‑scope changes.

| Benchmark / Deliverable | Mapping | Status | Evidence / Progress |
|--------------------------|---------|--------|---------------------|
| Vulnerable & outdated components | OWASP A06:2021 | ✅ Pass | 9 packages patched across 6 manifests; `pip-audit` zero unignored |
| CORS misconfiguration | OWASP A05:2021 / CWE‑942 | ✅ Pass | Explicit allow‑lists + wildcard‑rejecting validators; 32 CORS tests pass |
| Weak / predictable secrets | OWASP A02 & A07 / CWE‑798, CWE‑259 | ✅ Pass | Required env secrets, `min_length=32`, fail‑closed validators |
| Hard‑coded IaC credential | CWE‑798 | ✅ Pass | `var.postgresql_admin_password`; residual‑secret scan clean |
| Container least privilege | CWE‑250 | ✅ Pass | Non‑root uid 1000; supported base image |
| Security‑event logging | FR‑8.5 / FR‑10.6 | ✅ Pass | Correlation‑ID auth/token/CORS events in 2 services |
| CI dependency‑scan gate | CWE‑1104 (hygiene) | ✅ Pass | `pip-audit` `SecurityScan` stage; `Build→Test→SecurityScan→Deploy` |
| JWT algorithm restriction | Algorithm‑confusion class | ✅ Pass | `jwt.decode(..., algorithms=["HS256"])`; regression assertion added |
| Minimal Change Clause adherence | User directive | ✅ Pass | Only in‑scope files changed; clean packages & secure services untouched |
| Explainability (decision log) | Rule | ✅ Pass | `docs/security/decision-log.md` + AAP §0.10.2 table |
| Visual architecture (before/after) | Rule | ✅ Pass | Titled, legended Mermaid before/after diagram (AAP §0.4.3) |
| Observability (reuse) | Rule | ⚠ Partial | Security‑event logging + dashboard template shipped; full tracing/metrics deferred (AAP‑noted) |
| Onboarding & continued development | Rule | ✅ Pass | `SECURITY.md` + root and five service READMEs updated |
| Executive presentation | Rule | ✅ Pass | Self‑contained reveal.js deck (`blitzy-deck/executive-summary.html`) |

**Fixes applied during autonomous validation:** none required (remediation validated correct as‑is). **Outstanding compliance item:** observability remains intentionally partial per the Minimal Change Clause; full tracing/metrics/App Insights are recorded as recommended follow‑ups.

---

## 6. Risk Assessment

| Risk | Category | Severity | Probability | Mitigation | Status |
|------|----------|----------|-------------|------------|--------|
| Fail‑closed secret validation halts service start if secrets are absent or <32 chars | Technical | Medium | Medium | Documented in READMEs and task HT‑1; fails loudly rather than silently using a weak secret | Mitigated by design |
| Dependency major‑version jumps (pydantic 1.8→1.10, fastapi 0.68→0.125, cryptography 3.4→49) cause behavioral drift | Technical | Medium | Low | Pinned to specific patched versions; Pydantic held on v1; FastAPI capped <0.126; 83/83 regression pass | Mitigated |
| No lockfiles — transitive dependencies float | Technical | Low | Medium | Top‑level `==` pins + `pip-audit` CI gate | Open (AAP‑noted follow‑up) |
| Production secrets not yet provisioned | Security | High | Medium | Fail‑closed design + tasks HT‑1/HT‑2; deploy blocks until set | Mitigated (pending human action) |
| Operator could declare an overly broad CORS origin list | Security | Medium | Low | Wildcard‑rejecting validator forbids `*`; onboarding docs | Mitigated |
| End‑of‑life PostgreSQL v11 engine | Security | Medium | Low | — | Deferred (out of AAP scope §0.8.2) |
| Demo‑credential placeholder in `api_gateway` `authenticate_user` | Security | Medium | Low | — | Deferred (out of AAP scope — auth rework §0.8.2) |
| Deployment coupling — DB password must be provisioned as a secret at apply time | Operational | Medium | Medium | Deployment‑coordination note in `SECURITY.md`/README; task HT‑2 | Documented |
| Observability partial — only security‑event logging shipped | Operational | Low | Low | Dashboard template shipped; recommended next steps | Deferred (AAP‑noted) |
| Pre‑existing CI Test‑stage paths (`tests/unit`, `tests/integration`) do not exist | Operational | Low | Medium | In‑scope `SecurityScan` stage is correct and independent | Deferred (out of AAP scope §0.8.2) |
| `azure-identity` 1.16.1 vs `azure-keyvault-secrets` 4.3.0 / `azure-core` peers | Integration | Low | Low | `pip check` clean in all six venvs; verify at deploy | Mitigated |
| `outputs.tf` references undeclared resources — blocks full‑module `terraform validate/apply` | Integration | Medium | Medium | `main.tf` credential fix validates independently; pre‑existing baseline defect | Deferred (out of AAP scope — flag for human) |
| Browser CORS + credentials flow only verified in‑process (TestClient), not in a deployed environment | Integration | Low | Low | Covered by task HT‑5 e2e verification | Open (path‑to‑production) |

---

## 7. Visual Project Status

**Overall completion (hours):**

```mermaid
%%{init: {'theme':'base', 'themeVariables': {'pie1':'#5B39F3','pie2':'#FFFFFF','pieStrokeColor':'#B23AF2','pieStrokeWidth':'2px','pieOuterStrokeWidth':'2px','pieTitleTextSize':'16px','pieSectionTextSize':'14px','pieLegendTextSize':'13px'}}}%%
pie showData title Project Hours — Completed vs Remaining
    "Completed Work" : 105
    "Remaining Work" : 15
```

**Remaining work by priority (hours):**

```mermaid
%%{init: {'theme':'base', 'themeVariables': {'pie1':'#5B39F3','pie2':'#A8FDD9','pieStrokeColor':'#B23AF2','pieStrokeWidth':'2px','pieTitleTextSize':'16px','pieSectionTextSize':'14px','pieLegendTextSize':'13px'}}}%%
pie showData title Remaining 15 h by Priority
    "High" : 7
    "Medium" : 8
```

**Remaining hours by category (Section 2.2):**

| Category | Hours | Priority |
|----------|-------|----------|
| Provision production application secrets | 3 | High |
| Provision Terraform DB admin password | 2 | High |
| Configure real CORS origins per environment | 2 | High |
| Enable & validate CI SecurityScan gate | 2 | Medium |
| End‑to‑end integration & deployment verification | 6 | Medium |
| **Total** | **15** | |

> **Integrity:** the pie "Remaining Work" (15) equals Section 1.2 Remaining Hours (15) and the Section 2.2 Hours total (15). Colors: Completed = Dark Blue `#5B39F3`; Remaining = White `#FFFFFF`.

---

## 8. Summary & Recommendations

**Achievements.** The AAP‑scoped security remediation is **complete and independently verified**. All five vulnerability layers — dependencies, CORS, weak secrets, the IaC credential, and container hardening — are fixed with the smallest, most targeted set of changes, and the required CI gate, security‑event logging, regression tests, and documentation deliverables are in place. Blitzy modified 72 files (+4,226 / −1,057 lines) across 21 commits while honoring the Minimal Change Clause: clean dependencies and already‑secure services were deliberately left untouched. The 83 in‑scope security regression tests pass at 100%, `pip-audit` reports zero unignored advisories on every manifest, `terraform validate` succeeds, and the residual‑secret scan is clean.

**Remaining gaps & critical path.** The project is **87.5% complete** (105 h of 120 h). The remaining 15 h is entirely **path‑to‑production operational provisioning** that cannot be performed autonomously: injecting real secrets, supplying the Terraform DB password at apply time, declaring real CORS origins per environment, enabling the CI gate in the live pipeline, and running a deployment smoke test. The critical path is HT‑1 → HT‑2 → HT‑3 (all High, ~7 h) to unblock a first secure deploy, followed by HT‑4 and HT‑5 (Medium, ~8 h).

**Success metrics.** Zero unignored dependency advisories; zero wildcard‑plus‑credentials CORS responses; zero plaintext secrets in source; non‑root containers on supported base images; 100% security‑regression pass rate. All are met in the delivered code.

**Production‑readiness assessment.** The **codebase is production‑ready** for the security remediation scope. Deployment readiness is gated only on the operational provisioning tasks above and on the human‑owned, out‑of‑scope follow‑ups (lockfiles, `pytest` uplift, `outputs.tf` repair, broader observability, and the EOL PostgreSQL / demo‑credential architectural rework) which are documented but intentionally not addressed under the Minimal Change Clause. **Recommendation:** complete HT‑1 through HT‑3, deploy to a staging environment, execute HT‑5, then promote.

| Metric | Value |
|--------|-------|
| AAP‑scoped completion | 87.5% |
| In‑scope security tests passing | 83 / 83 (100%) |
| Dependency advisories (unignored) | 0 |
| Residual plaintext secrets | 0 |
| Critical path to first secure deploy | ~7 h (HT‑1 → HT‑3) |

---

## 9. Development Guide

> Verified in this session using the validator's runtimes. Backend services run on **Python 3.9** (`api_gateway`, `metrics_input_service`) and **Python 3.10** (`authentication_service`, `reporting_financials_service`, `reporting_metrics_service`); the `data_transformation` Function targets **Python 3.11**. The pinned `pydantic==1.10.13` (v1 line) does not build on Python 3.13 — use the runtimes below (Docker is the most reliable path).

### 9.1 System Prerequisites

- Docker 28.x (recommended) **or** Python 3.9 / 3.10 available locally
- Terraform ≥ 1.9 (for infrastructure validation)
- `git`; a POSIX shell
- PostgreSQL 15 (local container is sufficient for development)

### 9.2 Environment Setup

Set the required environment variables **before** starting any service — the hardened services fail‑closed if secrets are missing or too short.

```bash
# Application secrets (SECRET_KEY / JWT_SECRET_KEY must be >= 32 characters)
export SECRET_KEY="$(python -c 'import secrets; print(secrets.token_urlsafe(48))')"
export JWT_SECRET_KEY="$SECRET_KEY"
export API_KEY="dev-api-key"
export DATABASE_URL="postgresql://omers:omers@localhost:5432/omers"

# CORS — explicit, non-wildcard origins only (wildcard '*' is rejected)
export CORS_ALLOW_ORIGINS="http://localhost:3000"   # api_gateway
export CORS_ORIGINS="http://localhost:3000"         # auth / metrics_input / reporting_financials
export BACKEND_CORS_ORIGINS="http://localhost:3000" # reporting_metrics
```

Optional local PostgreSQL:

```bash
docker run -d --name omers-pg -e POSTGRES_USER=omers -e POSTGRES_PASSWORD=omers \
  -e POSTGRES_DB=omers -p 5432:5432 postgres:15-alpine
```

### 9.3 Dependency Installation

Install per service into an isolated environment (venv locally, or a Docker container). Example with Docker for a Python 3.10 service:

```bash
# From the repository root
docker run --rm -it -v "$PWD":/workspace -w /workspace python:3.10-slim \
  pip install -r src/backend/reporting_metrics_service/requirements.txt
```

Local venv equivalent (Python 3.10 service):

```bash
python3.10 -m venv .venv-rm && . .venv-rm/bin/activate
pip install -r src/backend/reporting_metrics_service/requirements.txt
```

### 9.4 Application Startup

Run each service from the **repository root** with `PYTHONPATH` set to the root. Assign a distinct host port per service.

```bash
export PYTHONPATH="$PWD"

# api_gateway  (factory entrypoint)
uvicorn main:create_app --factory --app-dir src/backend/api_gateway --host 127.0.0.1 --port 8000 &

# authentication_service  (factory entrypoint)
uvicorn main:create_app --factory --app-dir src/backend/authentication_service --host 127.0.0.1 --port 8001 &

# metrics_input_service
uvicorn main:app --app-dir src/backend/metrics_input_service --host 127.0.0.1 --port 8002 &

# reporting_financials_service
uvicorn main:app --app-dir src/backend/reporting_financials_service --host 127.0.0.1 --port 8003 &

# reporting_metrics_service
uvicorn main:app --app-dir src/backend/reporting_metrics_service --host 127.0.0.1 --port 8004 &
```

> In the container images the entrypoints are identical but bind `0.0.0.0:8000` (see each `Dockerfile` `CMD`).

### 9.5 Verification Steps

```bash
# Health (api_gateway and reporting_metrics expose /health)
curl -s http://127.0.0.1:8000/health
curl -s http://127.0.0.1:8004/health

# OpenAPI identity (all services expose /openapi.json)
curl -s http://127.0.0.1:8002/openapi.json | python -c 'import sys,json;print(json.load(sys.stdin)["info"])'

# Security regression suite (run from repo root; expect 83 passing across the five services)
PYTHONPATH="$PWD" python -m pytest \
  src/backend/api_gateway/tests/test_security_cors.py \
  src/backend/api_gateway/tests/test_security_config.py \
  src/backend/authentication_service/tests/test_security_cors.py \
  src/backend/authentication_service/tests/test_security_config.py \
  src/backend/metrics_input_service/tests/test_security_cors.py \
  src/backend/reporting_financials_service/tests/test_security_cors.py \
  src/backend/reporting_financials_service/tests/test_security_config.py \
  src/backend/reporting_metrics_service/tests/test_security_config.py -q

# Dependency vulnerability scan (mirrors the CI SecurityScan gate)
pip install pip-audit==2.9.0
pip-audit -r src/backend/reporting_metrics_service/requirements.txt \
  --ignore-vuln PYSEC-2026-1845 --ignore-vuln PYSEC-2022-14 \
  --ignore-vuln PYSEC-2026-161 --ignore-vuln PYSEC-2026-248 --ignore-vuln PYSEC-2026-249 \
  --ignore-vuln PYSEC-2026-2280 --ignore-vuln PYSEC-2026-2281 --progress-spinner off
# Expected: "No known vulnerabilities found, 7 ignored"

# Infrastructure validation (validate main.tf + variables.tf in isolation)
tmp=$(mktemp -d); cp infrastructure/terraform/main.tf infrastructure/terraform/variables.tf "$tmp"/
( cd "$tmp" && terraform init -backend=false && terraform validate ); rm -rf "$tmp"
# Expected: "Success! The configuration is valid."

# Residual-secret scan (expect no matches)
grep -rn "H@Sh1CoR3!\|your-secret-key" src infrastructure
```

### 9.6 Example Usage

```bash
# Start reporting_metrics locally and confirm it serves
export PYTHONPATH="$PWD"
export SECRET_KEY="$(python -c 'import secrets; print(secrets.token_urlsafe(48))')"
export DATABASE_URL="postgresql://omers:omers@localhost:5432/omers"
uvicorn main:app --app-dir src/backend/reporting_metrics_service --host 127.0.0.1 --port 8004 &
sleep 2
curl -s http://127.0.0.1:8004/health     # -> {"status":"ok"} (200)
```

### 9.7 Troubleshooting

- **Service exits immediately with a validation error** → a required secret is missing or `SECRET_KEY`/`JWT_SECRET_KEY` is shorter than 32 characters. This is intended CWE‑798 hardening; set the env vars from §9.2.
- **`pip install` fails building pydantic on Python 3.13** → use Python 3.9/3.10 (Docker images above); the v1 line does not provide 3.13 wheels.
- **`/health` returns 404 on `metrics_input`, `authentication`, or `reporting_financials`** → expected; only `api_gateway` and `reporting_metrics` define `/health`. Use `/openapi.json` to confirm those services are up.
- **`curl: command not found` inside `python:*-slim`** → slim images have no curl; use `python -c "import urllib.request…"` or `apt-get install -y curl`.
- **Full‑module `terraform validate` fails** → a pre‑existing `outputs.tf` defect references undeclared resources (out of scope). Validate `main.tf` + `variables.tf` in isolation as shown in §9.5.
- **`pip-audit` reports advisories** → ensure the full per‑runtime ignore‑list is supplied (7 IDs for Python 3.10, 8 for Python 3.9); these cover AAP‑deferred (`pytest`, `loguru`) and compatibility‑envelope (`starlette`, `click`, `python-dotenv`) advisories that are blocked by the Pydantic‑v1 ceiling or the service's Python version.

---

## 10. Appendices

### A. Command Reference

| Purpose | Command |
|---------|---------|
| Install a service's deps | `pip install -r src/backend/<service>/requirements.txt` |
| Run security suite (repo root) | `PYTHONPATH="$PWD" python -m pytest src/backend/<service>/tests/test_security_*.py -q` |
| Start a factory service | `uvicorn main:create_app --factory --app-dir src/backend/<api_gateway or authentication_service> --port <p>` |
| Start a module‑app service | `uvicorn main:app --app-dir src/backend/<service> --port <p>` |
| Dependency scan | `pip-audit -r <manifest> <ignore-list> --progress-spinner off` |
| Terraform validate | `terraform init -backend=false && terraform validate` (main.tf + variables.tf) |
| Residual‑secret scan | `grep -rn "H@Sh1CoR3!\|your-secret-key" src infrastructure` |
| Container non‑root check | `docker run --rm --entrypoint python <image> -c "import os;print(os.getuid())"` → `1000` |

### B. Port Reference

| Service | In‑container port | Suggested local port | Entry point |
|---------|-------------------|----------------------|-------------|
| api_gateway | 8000 | 8000 | `main:create_app --factory` |
| authentication_service | 8000 | 8001 | `main:create_app --factory` |
| metrics_input_service | 8000 | 8002 | `main:app` |
| reporting_financials_service | 8000 | 8003 | `main:app` |
| reporting_metrics_service | 8000 | 8004 | `main:app` |

### C. Key File Locations

| Area | Path |
|------|------|
| Backend services | `src/backend/<service>/` |
| Azure Function | `src/functions/data_transformation/` |
| Dependency manifests | `src/backend/*/requirements.txt`, `src/functions/data_transformation/requirements.txt` |
| CORS config | `src/backend/*/config.py`, `src/backend/*/main.py`, `src/backend/*/app/__init__.py` |
| Secret config | `reporting_financials_service/config.py`, `reporting_metrics_service/config.py` |
| Terraform | `infrastructure/terraform/{main.tf,variables.tf,outputs.tf,backend.tf}` |
| CI pipeline | `infrastructure/azure-pipelines/azure-pipelines.yml` |
| Security tests | `src/backend/*/tests/test_security_{cors,config}.py` |
| Security docs | `SECURITY.md`, `docs/security/decision-log.md`, `docs/security/security-observability-dashboard.md` |
| Executive deck | `blitzy-deck/executive-summary.html` |

### D. Technology Versions (patched pins in force)

| Package | Version | Advisory addressed |
|---------|---------|--------------------|
| fastapi | 0.125.0 (`<0.126.0`) | CVE‑2024‑24762 (keeps Pydantic v1) |
| pydantic | 1.10.13 (v1 line) | CVE‑2024‑3772 |
| PyJWT | 2.13.0 | CVE‑2022‑29217 |
| cryptography | 49.0.0 | CVE‑2023‑50782 / CVE‑2023‑0286 / CVE‑2024‑0727 |
| gunicorn | 23.0.0 | CVE‑2024‑1135 / CVE‑2024‑6827 |
| azure-identity | 1.16.1 | CVE‑2024‑35255 |
| requests | 2.34.2 / 2.33.0 | CVE‑2024‑47081 / CVE‑2024‑35195 / CVE‑2023‑32681 |
| python-dotenv | 1.0.1 (py3.9) / 1.2.2 (py3.10+) | PYSEC‑2026‑2270 |
| h11 | ≥0.16.0 | CVE‑2025‑43859 |
| urllib3 | 2.7.0 | PYSEC‑2026‑141 / ‑142 |

### E. Environment Variable Reference

| Variable | Services | Notes |
|----------|----------|-------|
| `SECRET_KEY` | api_gateway, authentication_service, reporting_metrics_service | ≥32 chars; required (fail‑closed) |
| `JWT_SECRET_KEY` | reporting_financials_service | ≥32 chars; required (fail‑closed) |
| `DATABASE_URL` | all backend services | PostgreSQL DSN; required |
| `API_KEY` | api_gateway, metrics_input_service, reporting_financials_service | required |
| `CORS_ALLOW_ORIGINS` | api_gateway | explicit list; `*` rejected |
| `CORS_ORIGINS` | authentication_service, metrics_input_service, reporting_financials_service | explicit list; `*` rejected |
| `BACKEND_CORS_ORIGINS` | reporting_metrics_service | explicit list; `*` rejected |
| `TOKEN_EXPIRATION`, `DEBUG` | authentication_service | operational |
| `JWT_ALGORITHM`, `ACCESS_TOKEN_EXPIRE_MINUTES` | reporting_financials_service | operational |
| `LOG_LEVEL` | metrics_input_service, reporting_financials_service, reporting_metrics_service | operational |
| `ENVIRONMENT` | reporting_metrics_service | operational |
| `TF_VAR_postgresql_admin_password` | Terraform | sensitive; supply at apply time |

### F. Developer Tools Guide

- **pytest** — security regression suites; run from repo root with `PYTHONPATH="$PWD"`.
- **pip-audit 2.9.0** — dependency scanning; mirrors the CI `SecurityScan` gate (supply the per‑runtime ignore‑list).
- **Terraform 1.9.x** — `terraform validate` for IaC; validate `main.tf` + `variables.tf` in isolation.
- **Docker 28.x** — reproduces the validator runtimes (`python:3.9-slim`, `python:3.10-slim`, `python:3.11-slim`) and container non‑root checks.
- **uvicorn** — ASGI server for local service startup.

### G. Glossary

| Term | Definition |
|------|------------|
| AAP | Agent Action Plan — the controlling directive for this engagement |
| Minimal Change Clause | User constraint: make only the smallest changes needed to remediate findings |
| CWE‑942 | Overly permissive Cross‑Origin Resource Sharing |
| CWE‑798 / CWE‑259 | Use of hard‑coded / weak credentials |
| CWE‑250 | Execution with unnecessary (root) privileges |
| Fail‑closed | Service refuses to start rather than run with a missing/weak secret |
| Compatibility envelope | Advisories whose fixes are blocked by the Pydantic‑v1 ceiling or a service's Python version, ignored in CI with rationale |
| Path‑to‑production | Operational steps required to deploy delivered code (secrets, origins, verification) |