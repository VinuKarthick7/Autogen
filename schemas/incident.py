from pydantic import BaseModel
from typing import Literal
from datetime import datetime

class Incident(BaseModel):
    incident_id: str
    title: str
    severity: Literal[
        "critical",
        "high",
        "medium",
        "low"
    ]
    affected_services: list[str]
    detected_at: datetime
    status: Literal[
        "open",
        "investigating",
        "resolved"
    ]
