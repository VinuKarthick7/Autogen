"""Small, failure-tolerant client for the local FastAPI dashboard API."""

import os
from typing import Any

import requests


def api_url() -> str:
    return st_session_api_url() or os.getenv("API_URL", "http://localhost:8000")


def st_session_api_url() -> str | None:
    try:
        import streamlit as st

        return st.session_state.get("api_url")
    except Exception:
        return None


def get(path: str, *, params: dict[str, Any] | None = None) -> tuple[Any | None, str | None]:
    try:
        response = requests.get(f"{api_url().rstrip('/')}{path}", params=params, timeout=5)
        response.raise_for_status()
        return response.json(), None
    except requests.RequestException as exc:
        return None, str(exc)
