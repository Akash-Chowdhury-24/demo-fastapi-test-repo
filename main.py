from fastapi import FastAPI

from app.core.config import settings
from app.routers import api_router

app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
)

app.include_router(api_router)


@app.get("/")
def root() -> dict[str, str]:
    return {
        "message": f"Welcome to {settings.app_name} prod and dev",
        "docs": "/docs",
    }
