# LeakFence

### CI/CD Security Gate for Secret Detection

LeakFence is a lightweight security tool that scans source code for accidentally hard-coded secrets and integrates the scan directly into a CI/CD pipeline.

The main goal is simple:

> **Prevent code containing exposed credentials from reaching production.**

---

## Project Overview

Developers can accidentally commit sensitive information such as:

- AWS access keys
- Passwords
- Private keys
- JWT tokens
- API credentials

LeakFence detects these patterns automatically.

If a secret is detected, the GitHub Actions validation stage fails and the deployment stage is not executed.

This turns secret detection into an automated **CI/CD security gate** rather than relying on manual inspection.

---

## How It Works

```text
Developer
    |
    | git push
    v
GitHub Repository
    |
    v
GitHub Actions
    |
    +--> Pytest
    |
    +--> LeakFence Secret Scan
    |
    +--> Ruff Code Quality Check
    |
    v
Validation Passed?
    |
    +---- NO ----> Pipeline Stops
    |
    +---- YES
            |
            v
       Docker Build
            |
            v
       GitHub Container Registry
            |
            v
       Render Deployment
            |
            v
       Production Application
