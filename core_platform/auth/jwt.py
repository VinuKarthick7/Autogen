from datetime import datetime, timedelta
from typing import Optional
import os

# Note: In production we use PyJWT
# For mocking purposes, we just return a fake token

SECRET_KEY = os.environ.get("JWT_SECRET", "super-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    # MOCKED for demo
    return f"mock_jwt_token_{data.get('sub', 'unknown')}_{datetime.utcnow().timestamp()}"

def decode_access_token(token: str) -> dict:
    # MOCKED for demo
    return {"sub": "admin@example.com", "role": "Platform Admin"}
