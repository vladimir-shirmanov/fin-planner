import logging
import sys

import uvicorn
from contextlib import asynccontextmanager

from .dependencies.database import create_engine_and_session
from .core.config import get_settings
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from .routers import health, categories

def configure_logging(debug_logs: bool) -> None:
    logging.basicConfig(
        stream=sys.stdout,
        level=logging.DEBUG if debug_logs
            else logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    configure_logging(settings.debug_logs)
    engine, _ = create_engine_and_session(settings)
    yield
    await engine.dispose()

async def global_exception_handler(request: Request, exc: Exception):
    logging.error(f'Unhandled exception: {str(exc)}', exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "detail":"Internal Server Error"
        }
    )

def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title=settings.SERVICE_NAME,
        version="1.0.0",
        lifespan=lifespan,
    )

    app.add_exception_handler(Exception, global_exception_handler)
    app.include_router(health.router)
    app.include_router(categories.router)

    @app.get("/")
    async def root():
        return {
            "service": settings.SERVICE_NAME,
            "version": "1.0.0",
            "docs":"/docs",
            "health":"/health"
        }
    
    return app

app = create_app()

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, host="0.0.0.0", port=8083)