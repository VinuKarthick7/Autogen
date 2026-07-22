from pydantic import BaseModel
from typing import Literal

class Alert(BaseModel):
    alert_id: str
    message: str
    severity: Literal[
        "critical",
        "high",
        "medium",
        "low"
    ]
    escalated: bool
