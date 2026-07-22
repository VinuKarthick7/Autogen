from pydantic import BaseModel
from typing import Optional

class TraceSpan(BaseModel):
    trace_id: str
    span_id: str
    parent_span_id: Optional[str] = None
    service: str
    operation: str
    duration_ms: float
    tags: dict
