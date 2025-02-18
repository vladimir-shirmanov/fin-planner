import uvicorn
from contextlib import asynccontextmanager

from .infrastructure.database.database import create_engine_and_session
from .domain.configs.config import get_settings
from .infrastructure.logging.logging import configure_logging
from .infrastructure.logging.logging_middleware import StructLogMiddleware
from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI
from .routers import health, categories, budget
from .utils.init_db import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    engine, session_maker = create_engine_and_session(settings)
    async with session_maker() as session:
        await init_db(session)
    yield
    await engine.dispose()

def create_app() -> FastAPI:
    settings = get_settings()
    configure_logging(settings.json_logs)

    app = FastAPI(
        title=settings.SERVICE_NAME,
        version="1.0.0",
        lifespan=lifespan,
    )

    app.add_middleware(StructLogMiddleware)
    app.add_middleware(CorrelationIdMiddleware)

    app.include_router(health.router)
    app.include_router(categories.router)
    app.include_router(budget.router)

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