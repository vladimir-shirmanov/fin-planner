import logging
import sys

import uvicorn
from contextlib import asynccontextmanager

from .dependencies.database import sessionmanager
from .core.config import settings
from fastapi import FastAPI

from .routers import health

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG if settings.debug_logs else logging.INFO)

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    if sessionmanager._engine is not None:
        await sessionmanager.close()

app = FastAPI(
    title=settings.SERVICE_NAME,
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(health.router)

@app.get("/")
async def root():
    return {
        "service": settings.SERVICE_NAME,
        "version": "1.0.0",
        "docs":"/docs",
        "health":"/health"
    }

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, host="0.0.0.0", port=8083)