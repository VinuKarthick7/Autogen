from pydantic import BaseModel
from typing import Literal

class Anomaly(BaseModel):
    anomaly_id: str
    category: Literal[
        "latency",
        "memory",
        "cpu",
        "errors",
        "cost",
        "availability"
    ]
    severity: Literal[
        "critical",
        "high",
        "medium",
        "low"
    ]
    confidence: float
    description: str
    recommendation: str
