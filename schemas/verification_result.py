from pydantic import BaseModel

class VerificationResult(BaseModel):
    run_id: str
    passed: bool
    report_path: str
    total_time_ms: int
