from pydantic import BaseModel
from datetime import datetime

class MetricsSnapshot(BaseModel):
    snapshot_id: str
    timestamp: datetime
    service: str
    cpu_usage_pct: float
    memory_usage_mb: float
    active_connections: int
