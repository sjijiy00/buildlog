from fastapi import FastAPI

from app.core.config import get_settings


get_settings()

app = FastAPI(title="BuildLog API")


@app.get("/api/health", tags=["system"])
def health() -> dict[str, str]:
    return {"status": "ok"}
