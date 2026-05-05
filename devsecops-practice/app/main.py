from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel, Field

app = FastAPI(title="DevSecOps Practice App", version="1.0.0")

API_KEY = "change-me-in-prod"


class SecretRequest(BaseModel):
    username: str = Field(min_length=3, max_length=30)
    environment: str = Field(pattern="^(dev|qa|prod)$")


@app.get("/health")
def health_check() -> dict:
    return {"status": "ok"}


@app.post("/api/secret")
def get_secret(payload: SecretRequest, x_api_key: str | None = Header(default=None)) -> dict:
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

    return {
        "message": f"Hello {payload.username}",
        "hint": f"Use a secret manager for {payload.environment} credentials.",
    }
