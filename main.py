"""ASGI entrypoint for ``uvicorn main:app --reload``."""

from api.main import app, create_app

__all__ = ["app", "create_app"]
