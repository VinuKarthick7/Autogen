from pydantic import BaseModel

class VerificationStep(BaseModel):
    name: str
    command: str
    success: bool
    duration_ms: int
    stdout: str
    stderr: str
