# LeakFence Demo

## 1. Green baseline

Show a successful GitHub Actions run.

The pipeline should show:

* Tests passed
* LeakFence scan passed
* Code quality check passed
* Docker image built and published
* Deployment succeeded

## 2. Red proof

Create a temporary file containing a fake AWS access key, commit it, and push it to demonstrate the failed security gate.

The GitHub Actions pipeline should show:

```text
pytest                 ✅
LeakFence scan         ❌
Build/deploy           skipped
```

LeakFence should report the file, line number, and detected secret type.

Take a screenshot of the failed pipeline.

## 3. Fix

Remove the temporary secret:

```bash
rm demo_secret.py
git add -u
git commit -m "fix: remove demo secret"
git push
```

The pipeline should successfully complete:

```text
pytest                 ✅
LeakFence scan         ✅
Code quality           ✅
Docker build           ✅
GHCR publish           ✅
Render deployment      ✅
```

Take a screenshot of the successful pipeline and the deployed application.

## 4. Explanation

"LeakFence turns secret detection into a CI/CD security gate: when the scan fails, the deployment job cannot run because it depends on the validation job."

