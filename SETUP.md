# LeakFence Setup

## 1. Local setup

Create and activate a Python virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the tests:

```bash
pytest -q
```

Run the code quality check:

```bash
ruff check .
```

Run LeakFence:

```bash
python -m leakfence .
```

A clean repository should report:

```text
✅ No potential hard-coded secrets detected.
```

## 2. GitHub repository

Create a **public** GitHub repository named `leakfence`.

Push the project:

```bash
git init
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/leakfence.git
git add .
git commit -m "feat: initialize LeakFence"
git push -u origin main
```

## 3. GitHub Actions

The workflow is located at:

```text
.github/workflows/ci-cd.yml
```

The validation pipeline performs:

1. Install dependencies
2. Run unit tests
3. Run LeakFence
4. Run Ruff
5. Build the Docker image
6. Publish the image to GitHub Container Registry
7. Deploy to Render

Deployment depends on the validation job passing.

## 4. GitHub Container Registry

The GitHub Actions workflow publishes the Docker image to:

```text
ghcr.io/YOUR_USERNAME/leakfence
```

Make the container package public so Render can pull it without additional registry credentials.

## 5. Render

Create a Render Web Service using the GHCR image:

```text
ghcr.io/YOUR_USERNAME/leakfence:latest
```

Use the Free instance.

The application listens on port `10000` and provides:

```text
/
```

and:

```text
/health
```

Use `/health` as the Render health-check path.

## 6. Render deploy hook

Create a Render Deploy Hook and add it to GitHub as an Actions repository secret:

```text
RENDER_DEPLOY_HOOK_URL
```

The deploy hook is used only after all CI validation steps succeed.

## 7. Failure demonstration

For the required failed pipeline demonstration, create a temporary file containing a fake credential, commit it, and push it.

Do not add real credentials to the repository.

After capturing the failed pipeline, remove the temporary file, commit the fix, and push again.

The final successful run should proceed through validation, Docker build, GHCR publication, and Render deployment.

