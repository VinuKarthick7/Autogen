from pydantic import BaseModel

class RunSummary(BaseModel):
    run_id: str
    feature_request: str
    repository: str
    status: str
    duration_seconds: float
    files_modified: int
    repair_attempts: int
