# LeakFence

**Automated secret detection and prevention in a CI/CD pipeline.**

LeakFence scans the repository for common hard-coded credentials. A finding returns exit code 1, which fails GitHub Actions and blocks the Docker build/deployment job.

## Pipeline

```text
Push / Pull Request
        |
      pytest
        |
  LeakFence scan
        |
       Ruff
     /       \
   fail       pass
    |           |
  stop      Docker build
                |
               GHCR
                |
          Render deploy
```

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
pytest -q
ruff check .
python -m leakfence .
```

## Structure

```text
app/                    Tiny FastAPI application
leakfence/              Secret scanner
  scanner.py
  __main__.py
tests/                  Unit tests
.github/workflows/      GitHub Actions workflow
Dockerfile              Container image
```

See `SETUP.md` for the exact submission sequence and `DEMO.md` for the required red/green proof.
