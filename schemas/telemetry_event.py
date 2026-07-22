from pydantic import BaseModel
from datetime import datetime

class TelemetryEvent(BaseModel):
    event_id: str
    service: str
    endpoint: str
    timestamp: datetime
    latency_ms: float
    cpu_usage: float
    memory_usage: float
    status_code: int
    metadata: dict
