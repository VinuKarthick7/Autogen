"""Endpoints for static local repository intelligence."""

from typing import Any

from pathlib import Path

from fastapi import APIRouter, HTTPException, Query, Request
from pydantic import BaseModel, Field

from services.repository_scanner import repository_scanner
from services.ai_review_service import ai_review_service


router = APIRouter(prefix="/api/repository", tags=["repository"])


class RepositoryAnalysisRequest(BaseModel):
    path: str = Field(min_length=1, description="Absolute or user-relative local repository path")
    force: bool = Field(default=False, description="Bypass the in-memory cached analysis")


class RepositoryReviewRequest(BaseModel):
    path: str = Field(min_length=1, description="Absolute or user-relative local repository path")


@router.post("/analyze")
async def analyze_repository(payload: RepositoryAnalysisRequest, request: Request) -> dict[str, Any]:
    """Analyze a local repository and retain the result for dashboard consumers."""
    try:
        result = repository_scanner.analyze(payload.path, force=payload.force)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    request.app.state.repository_analysis = result
    recent = [item for item in getattr(request.app.state, "recent_repository_analyses", []) if item["path"] != result["path"]]
    recent.insert(0, {key: result[key] for key in ("repository_name", "path", "scanned_at", "scan_duration_ms")})
    request.app.state.recent_repository_analyses = recent[:5]
    return result


@router.post("/review")
async def review_repository(payload: RepositoryReviewRequest) -> dict[str, Any]:
    """Return a cached, bounded AutoGen review derived solely from scanner output."""
    try:
        return await ai_review_service.review_repository(payload.path)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.get("/latest")
async def latest_repository_analysis(request: Request) -> dict[str, Any]:
    """Return the most recently completed scan for this API process."""
    result = getattr(request.app.state, "repository_analysis", None)
    if result is None:
        raise HTTPException(status_code=404, detail="No repository has been analyzed yet")
    return result


@router.get("/recent")
async def recent_repository_analyses(request: Request) -> list[dict[str, Any]]:
    """Return recently scanned repositories for the Streamlit picker."""
    return getattr(request.app.state, "recent_repository_analyses", [])


@router.get("/browse")
async def browse_repository_folders(path: str = Query(min_length=1)) -> dict[str, Any]:
    """List direct server-side directories to help select a local repository."""
    folder = Path(path).expanduser().resolve()
    if not folder.is_dir():
        raise HTTPException(status_code=422, detail=f"Folder does not exist: {folder}")
    try:
        directories = [{"name": child.name, "path": str(child)} for child in sorted(folder.iterdir(), key=lambda item: item.name.lower()) if child.is_dir() and not child.name.startswith(".")]
    except OSError as exc:
        raise HTTPException(status_code=422, detail=f"Could not browse folder: {exc}") from exc
    return {"path": str(folder), "directories": directories[:200]}
