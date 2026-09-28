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
        <title>LeakFence</title>
        <style>
          body { font-family: system-ui, sans-serif; max-width: 760px; margin: 60px auto; padding: 0 20px; }
          .ok { padding: 14px 18px; border: 1px solid #222; border-radius: 10px; }
          code { background: #f3f3f3; padding: 2px 5px; border-radius: 4px; }
        </style>
      </head>
      <body>
        <h1>LeakFence</h1>
        <div class="ok">
          <strong>Deployment successful.</strong>
          <p>GitHub Actions tested, scanned, built and published this image before deployment.</p>
        </div>
        <p>Health endpoint: <code>/health</code></p>
      </body>
    </html>
    """


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "leakfence", "version": __version__}
