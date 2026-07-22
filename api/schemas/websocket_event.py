from pydantic import BaseModel
from typing import Literal, Optional
from datetime import datetime

class WebsocketEvent(BaseModel):
    run_id: str
    timestamp: datetime
    stage: str
    agent: Optional[str] = None
    event_type: Literal[
        "workflow_started",
        "agent_started",
        "agent_completed",
        "verification_started",
        "verification_completed",
        "repair_started",
        "repair_completed",
        "approval_required",
        "workflow_completed",
        "workflow_failed"
    ]
    message: str
    metadata: dict
