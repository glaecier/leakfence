from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from leakfence import __version__

app = FastAPI(title="LeakFence", version=__version__)


@app.get("/", response_class=HTMLResponse)
def home() -> str:
    return """
    <!doctype html>
    <html lang="en">
    <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1">

      <title>LeakFence — CI/CD Security</title>

      <style>
        * {
          box-sizing: border-box;
        }

        :root {
          --bg: #07090d;
          --panel: #0d1118;
          --panel-hover: #111722;
          --border: #202938;
          --text: #f4f7fb;
          --muted: #8b96a8;
          --green: #35e58c;
          --green-dark: #123c2a;
          --red: #ff5c70;
          --blue: #6ea8ff;
        }

        body {
          margin: 0;
          min-height: 100vh;
          background:
            radial-gradient(
              circle at 50% -10%,
              #17243a 0%,
              var(--bg) 45%
            );
          color: var(--text);
          font-family:
            Inter, ui-sans-serif, system-ui, -apple-system,
            BlinkMacSystemFont, "Segoe UI", sans-serif;
        }

        .container {
          width: min(1050px, calc(100% - 40px));
          margin: 0 auto;
          padding: 32px 0 60px;
        }

        nav {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 80px;
        }

        .brand {
          display: flex;
          align-items: center;
          gap: 11px;
          font-size: 19px;
          font-weight: 750;
          letter-spacing: -0.3px;
        }

        .shield {
          width: 32px;
          height: 32px;
          display: grid;
          place-items: center;
          border: 1px solid #31513f;
          border-radius: 9px;
          background: var(--green-dark);
          color: var(--green);
          font-size: 16px;
        }

        .nav-label {
          color: var(--muted);
          font-size: 12px;
          font-weight: 700;
          letter-spacing: 1.2px;
        }

        .hero {
          max-width: 780px;
          margin-bottom: 46px;
        }

        .eyebrow {
          display: inline-flex;
          align-items: center;
          gap: 8px;
          margin-bottom: 20px;
          padding: 7px 11px;
          border: 1px solid #254735;
          border-radius: 999px;
          background: rgba(18, 60, 42, 0.55);
          color: var(--green);
          font-size: 11px;
          font-weight: 800;
          letter-spacing: 1px;
        }

        .dot {
          width: 7px;
          height: 7px;
          border-radius: 50%;
          background: var(--green);
          box-shadow: 0 0 12px rgba(53, 229, 140, 0.8);
        }

        h1 {
          margin: 0;
          font-size: clamp(42px, 7vw, 76px);
          line-height: 0.98;
          letter-spacing: -4px;
        }

        .gradient {
          background: linear-gradient(
            110deg,
            #ffffff 15%,
            #9deec2 55%,
            #61e9ff 100%
          );
          -webkit-background-clip: text;
          background-clip: text;
          color: transparent;
        }

        .subtitle {
          max-width: 680px;
          margin: 25px 0 0;
          color: var(--muted);
          font-size: 18px;
          line-height: 1.65;
        }

        .status {
          display: flex;
          align-items: center;
          gap: 14px;
          margin-bottom: 35px;
          padding: 20px 22px;
          border: 1px solid #28553f;
          border-radius: 14px;
          background: rgba(18, 60, 42, 0.28);
        }

        .status-icon {
          width: 42px;
          height: 42px;
          display: grid;
          place-items: center;
          flex: 0 0 auto;
          border-radius: 12px;
          background: var(--green-dark);
          color: var(--green);
          font-size: 20px;
          font-weight: 900;
        }

        .status-title {
          font-weight: 800;
          font-size: 15px;
        }

        .status-text {
          margin-top: 3px;
          color: var(--muted);
          font-size: 13px;
        }

        .section-title {
          margin: 0 0 17px;
          color: #c7cfdb;
          font-size: 12px;
          font-weight: 800;
          letter-spacing: 1.3px;
          text-transform: uppercase;
        }

        .pipeline {
          display: grid;
          grid-template-columns: repeat(4, 1fr);
          gap: 12px;
          margin-bottom: 60px;
        }

        .stage {
          padding: 22px;
          border: 1px solid var(--border);
          border-radius: 14px;
          background: rgba(13, 17, 24, 0.9);
          transition:
            transform 0.2s ease,
            border-color 0.2s ease,
            background 0.2s ease;
        }

        .stage:hover {
          transform: translateY(-3px);
          border-color: #344256;
          background: var(--panel-hover);
        }

        .stage-top {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 24px;
        }

        .stage-number {
          color: #657186;
          font-size: 11px;
          font-weight: 800;
        }

        .check {
          width: 24px;
          height: 24px;
          display: grid;
          place-items: center;
          border-radius: 50%;
          background: var(--green-dark);
          color: var(--green);
          font-size: 13px;
          font-weight: 900;
        }

        .stage h3 {
          margin: 0 0 6px;
          font-size: 15px;
        }

        .stage p {
          margin: 0;
          color: var(--muted);
          font-size: 12px;
          line-height: 1.5;
        }

        .explanation {
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: 16px;
          margin-bottom: 50px;
        }

        .card {
          padding: 27px;
          border: 1px solid var(--border);
          border-radius: 16px;
          background: rgba(13, 17, 24, 0.75);
        }

        .card h2 {
          margin: 0 0 12px;
          font-size: 17px;
        }

        .card p {
          margin: 0;
          color: var(--muted);
          font-size: 14px;
          line-height: 1.7;
        }

        .flow {
          margin-top: 18px;
          color: #cbd4e1;
          font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
          font-size: 12px;
          line-height: 2;
        }

        .danger {
          color: var(--red);
        }

        .footer {
          display: flex;
          justify-content: space-between;
          gap: 20px;
          padding-top: 25px;
          border-top: 1px solid var(--border);
          color: #657186;
          font-size: 12px;
        }

        .health {
          color: var(--green);
        }

        code {
          color: #b9c5d8;
          font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
        }

        @media (max-width: 760px) {
          .container {
            width: min(100% - 28px, 1050px);
            padding-top: 22px;
          }

          nav {
            margin-bottom: 55px;
          }

          h1 {
            letter-spacing: -2.5px;
          }

          .pipeline {
            grid-template-columns: 1fr 1fr;
          }

          .explanation {
            grid-template-columns: 1fr;
          }
        }

        @media (max-width: 480px) {
          .pipeline {
            grid-template-columns: 1fr;
          }

          .footer {
            flex-direction: column;
          }
        }
      </style>
    </head>

    <body>
      <main class="container">

        <nav>
          <div class="brand">
            <div class="shield">✓</div>
            LeakFence
          </div>
          <div class="nav-label">CI/CD SECURITY GATE</div>
        </nav>

        <section class="hero">
          <div class="eyebrow">
            <span class="dot"></span>
            DEPLOYMENT PROTECTED
          </div>

          <h1>
            <span class="gradient">Not secrets.</span>
          </h1>

          <p class="subtitle">
            inside the CI/CD pipeline and blocks deployment when a potential
            secret is detected.
          </p>
        </section>

        <section class="status">
          <div class="status-icon">✓</div>
          <div>
            <div class="status-title">Production deployment is protected</div>
            <div class="status-text">
              This version passed testing, secret scanning, quality checks,
              containerization and deployment.
            </div>
          </div>
        </section>

        <section>
          <div class="section-title">Deployment pipeline</div>

          <div class="pipeline">

            <div class="stage">
              <div class="stage-top">
                <span class="stage-number">01</span>
                <span class="check">✓</span>
              </div>
              <h3>Test</h3>
              <p>Automated Pytest suite validates application behaviour.</p>
            </div>

            <div class="stage">
              <div class="stage-top">
                <span class="stage-number">02</span>
                <span class="check">✓</span>
              </div>
              <h3>Scan</h3>
              <p>LeakFence searches source files for potential credentials.</p>
            </div>

            <div class="stage">
              <div class="stage-top">
                <span class="stage-number">03</span>
                <span class="check">✓</span>
              </div>
              <h3>Build</h3>
              <p>Validated code is packaged into a Docker container.</p>
            </div>

            <div class="stage">
              <div class="stage-top">
                <span class="stage-number">04</span>
                <span class="check">✓</span>
              </div>
              <h3>Deploy</h3>
              <p>The verified container is published and deployed to Render.</p>
            </div>

          </div>
        </section>

        <section class="explanation">

          <div class="card">
            <h2>How LeakFence works</h2>
            <p>
              Every push is validated by GitHub Actions. If the scanner finds
              a potential secret, the validation job fails and the deployment
              job cannot run.
            </p>

            <div class="flow">
              PUSH → TEST → SCAN → BUILD → GHCR → DEPLOY
            </div>
          </div>

          <div class="card">
            <h2>What happens when a secret is found?</h2>
            <p>
              The unsafe change is rejected by the CI security gate.
              Production remains on the previous successful deployment.
            </p>

            <div class="flow">
              SECRET FOUND → <span class="danger">BLOCK DEPLOYMENT</span>
            </div>
          </div>

        </section>

        <footer class="footer">
          <span>LeakFence v__VERSION__</span>
          <span class="health">● Service healthy · <code>/health</code></span>
        </footer>

      </main>
    </body>
    </html>
    """.replace("__VERSION__", __version__)


@app.get("/health")
def health() -> dict[str, str]:
    return {
        "status": "ok",
        "service": "leakfence",
        "version": __version__,
    }
