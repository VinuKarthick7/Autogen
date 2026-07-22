"""Failure-tolerant client for the local repository analysis API."""

from __future__ import annotations

import os
from typing import Any

import requests


def _base_url() -> str:
    return os.getenv("API_URL", "http://localhost:8000").rstrip("/")


def _request(method: str, path: str, **kwargs: Any) -> tuple[dict[str, Any] | None, str | None]:
    try:
        response = requests.request(method, f"{_base_url()}{path}", timeout=120, **kwargs)
        if not response.ok:
            try:
                detail = response.json().get("detail", response.text)
            except ValueError:
                detail = response.text
            return None, str(detail)
        return response.json(), None
    except requests.RequestException as exc:
        return None, f"Could not reach the API at {_base_url()}: {exc}"


def analyze_repository(path: str, *, force: bool = False) -> tuple[dict[str, Any] | None, str | None]:
    return _request("POST", "/api/repository/analyze", json={"path": path, "force": force})


def latest_analysis() -> tuple[dict[str, Any] | None, str | None]:
    return _request("GET", "/api/repository/latest")


def recent_analyses() -> tuple[list[dict[str, Any]] | None, str | None]:
    data, error = _request("GET", "/api/repository/recent")
    return data, error


def browse_folders(path: str) -> tuple[dict[str, Any] | None, str | None]:
    return _request("GET", "/api/repository/browse", params={"path": path})


def review_repository(path: str) -> tuple[dict[str, Any] | None, str | None]:
    return _request("POST", "/api/repository/review", json={"path": path})
