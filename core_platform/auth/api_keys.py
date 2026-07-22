import secrets
import hashlib

def generate_api_key(prefix="ak"):
    token = secrets.token_urlsafe(32)
    return f"{prefix}_{token}"

def hash_api_key(api_key: str) -> str:
    return hashlib.sha256(api_key.encode()).hexdigest()

def verify_api_key(plain_key: str, hashed_key: str) -> bool:
    return hash_api_key(plain_key) == hashed_key
