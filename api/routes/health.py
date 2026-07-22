from time import time

from fastapi import APIRouter, Request

router = APIRouter(tags=["health"])

@router.get("/health")
async def health(request: Request) -> dict[str, object]:
    return {
        "status": "healthy",
        "service": "Autonomous Engineering API",
        "uptime_seconds": round(time() - request.app.state.started_at, 3),
    }
