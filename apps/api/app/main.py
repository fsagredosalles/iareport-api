import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from fastapi import FastAPI
from .api.v1 import upload


sentry_sdk.init(
    dsn="https://your-sentry-dsn@your-project.ingest.sentry.io/123",
    integrations=[FastApiIntegration()],
)

app = FastAPI()

app.include_router(upload.router, prefix="/api/v1")

