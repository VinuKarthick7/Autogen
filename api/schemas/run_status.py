from pydantic import BaseModel
from typing import Literal, Optional
from datetime import datetime

class RunStatus(BaseModel):
    run_id: str
    status: Literal[
        "queued",
        "running",
        "verifying",
        "repairing",
        "waiting_approval",
        "completed",
        "failed"
    ]
    current_agent: Optional[str] = None
    current_stage: str
    progress: int
    repair_depth: int
    verification_passed: bool
    score: Optional[float] = None
    created_at: datetime
