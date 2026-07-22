from contextlib import asynccontextmanager
import logging
import os
from time import time

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from api.routes import runs, benchmarks, artifacts, repairs, approvals, health
from api.services.websocket_service import WebsocketService
from api.middleware.exception_handler import global_exception_handler
from api.middleware.logging import log_request_middleware
from api.middleware.timing import TimingMiddleware

logger = logging.getLogger(__name__)


def _cors_origins() -> list[str]:
    """Read a comma-separated allowlist, keeping local development usable."""
    raw_origins = os.getenv("CORS_ORIGINS", "http://localhost:8501,http://127.0.0.1:8501")
    return [origin.strip() for origin in raw_origins.split(",") if origin.strip()]


@asynccontextmanager
async def lifespan(application: FastAPI):
    application.state.started_at = time()
    logger.info("Autonomous Engineering API started")
    try:
        yield
    finally:
        logger.info("Autonomous Engineering API stopped")


def create_app() -> FastAPI:
    app = FastAPI(
        title="Autonomous Engineering API",
        version="1.0.0",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=_cors_origins(),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_middleware(TimingMiddleware)
    app.middleware("http")(log_request_middleware)
    app.add_exception_handler(Exception, global_exception_handler)

    app.include_router(runs.router)
    app.include_router(approvals.router)
    app.include_router(artifacts.router)
    app.include_router(benchmarks.router)
    app.include_router(repairs.router)
    app.include_router(health.router)

    from api.routes.product import router as prod_router
    from api.routes.quality import router as qual_router

    app.include_router(prod_router)
    app.include_router(qual_router)

    websocket_service = WebsocketService()

    @app.get("/", tags=["system"])
    async def root() -> dict[str, str]:
        return {"service": "Autonomous Engineering API", "status": "ok"}

    @app.websocket("/ws/runs/{run_id}")
    async def websocket_endpoint(websocket: WebSocket, run_id: str) -> None:
        await websocket_service.connect(run_id, websocket)
        try:
            while True:
                await websocket.receive_text()
        except WebSocketDisconnect:
            websocket_service.disconnect(run_id, websocket)

    return app


app = create_app()
