# DevSecOps Practice Application (End-to-End)

This mini project is intentionally designed for **DevSecOps hands-on practice**. It gives you a simple API, tests, containerization, and a security checklist so you can practice secure SDLC from coding to deployment.

## 1) What You Build

- A FastAPI service with:
  - `GET /health`
  - `POST /api/secret` (API-key protected)
- Unit tests with `pytest`
- Docker image with a non-root runtime user
- A pipeline blueprint for SAST, dependency scanning, IaC/container scanning, and runtime checks

---

## 2) Project Structure

```text
devsecops-practice/
├── app/
│   └── main.py
├── tests/
│   └── test_app.py
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## 3) Local Setup

### Prerequisites

- Python 3.11+
- pip
- Docker (optional, for container run)

### Install & Run

```bash
cd devsecops-practice
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open: `http://127.0.0.1:8000/docs`

---

## 4) Run Tests

```bash
cd devsecops-practice
pytest -q
```

---

## 5) Security Practices Included

1. **Input validation** with Pydantic fields and regex environment constraints.
2. **Simple API authentication** using `x-api-key` header.
3. **Least privilege in container** by running as non-root user.
4. **Basic test coverage** for happy-path and unauthorized access.

> Practice task: Replace hard-coded API key with environment variable or secret manager.

---

## 6) Suggested DevSecOps Pipeline (CI/CD)

Use the following stages in your CI pipeline:

1. **Lint & Unit Test**
   - `pytest -q`
2. **SAST**
   - Bandit for Python code
3. **Dependency Scan**
   - `pip-audit` or Snyk
4. **Container Scan**
   - Trivy on built image
5. **Policy Gate**
   - Fail build on critical vulnerabilities
6. **Deploy to Staging**
   - Smoke test `/health`
7. **Promote to Production**
   - Only after manual approval + clean reports

---

## 7) Example Security Commands

```bash
# SAST
bandit -r app

# Dependency vulnerability scan
pip-audit

# Build container image
docker build -t devsecops-practice:local .

# Container image vulnerability scan
trivy image devsecops-practice:local
```

---

## 8) Practice Backlog (What to Improve Next)

- Move API key to Vault / AWS Secrets Manager / Kubernetes Secret.
- Add JWT/OAuth2 instead of static API key.
- Add rate limiting and audit logs.
- Add SBOM generation (Syft) and signed artifacts (Cosign).
- Add DAST (OWASP ZAP) against staging.
- Add IaC with Terraform + Checkov scan.

---

## 9) Threat Modeling Prompts

Use these questions in your exercise:

- What happens if API keys leak in logs?
- How does the app behave under brute-force header attempts?
- What data should never appear in error messages?
- What controls detect malicious use post-deployment?

---

## 10) Definition of Done for DevSecOps Practice

A practice run is complete when:

- Tests pass.
- SAST + dependency + container scans execute.
- No critical vulnerabilities remain open.
- Secrets are not hard-coded.
- Deployment uses immutable artifact and approved gate.

