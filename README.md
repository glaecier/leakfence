# LeakFence

### Automated Secret Detection and Prevention in CI/CD Pipelines

LeakFence is a lightweight security tool that detects potentially exposed secrets and credentials in source code and prevents them from reaching deployment through a CI/CD security gate.

## Project Objective

The project demonstrates how GitHub Actions can automatically detect security issues during the software development lifecycle and block deployment when a potential secret is found.

## How It Works

```text
Developer pushes code
        ↓
GitHub Actions
        ↓
   Run tests
        ↓
 LeakFence scan
        ↓
  Ruff quality check
        ↓
   All checks pass?
      /       \
    No         Yes
    ↓           ↓
  Stop      Docker build
                ↓
              GHCR
                ↓
            Render deploy
```

## What LeakFence Detects

The scanner checks source files for patterns commonly associated with:

* AWS access keys
* GitHub tokens
* Google API keys
* JWT tokens
* Private keys
* Hard-coded passwords and credentials

The scanner reports the file, line number, and secret type without printing the detected credential itself.

## Example

If source code contains a hard-coded credential, LeakFence reports:

```text
❌ Potential secret detected

File : config.py
Line : 12
Type : AWS Access Key

CI pipeline blocked.
```

Replacing the credential with an environment variable allows the scan to pass.

## CI/CD Pipeline

The GitHub Actions pipeline performs:

1. Install dependencies
2. Run unit tests with Pytest
3. Scan the repository with LeakFence
4. Run Ruff code-quality checks
5. Build the Docker image
6. Publish the image to GitHub Container Registry
7. Deploy to Render

The deployment job depends on the validation job. Therefore, a failed test or secret scan prevents the deployment stage from executing.

## Demonstrated Failure

A fake AWS credential was intentionally introduced into the repository.

The pipeline detected it and stopped before deployment:

```text
Tests                 ✅
LeakFence scan        ❌
Build/deployment      skipped
```

After removing the fake credential, the pipeline successfully completed all stages and deployed the application to Render.

## Technologies

* Python
* FastAPI
* Pytest
* Ruff
* GitHub Actions
* Docker
* GitHub Container Registry
* Render
* Regular expression pattern matching

## Deployment

Live application:

https://leakfence-latest.onrender.com

Health endpoint:

https://leakfence-latest.onrender.com/health

## Repository Structure

```text
leakfence/
├── .github/
│   └── workflows/
│       └── ci-cd.yml
├── app/
│   └── main.py
├── leakfence/
│   ├── scanner.py
│   └── __main__.py
├── tests/
│   ├── test_app.py
│   └── test_scanner.py
├── Dockerfile
├── pyproject.toml
├── requirements.txt
├── DEMO.md
└── SETUP.md
```
