from pydantic import BaseModel

class SLAReport(BaseModel):
    report_id: str
    service: str
    availability_percentage: float
    p95_latency_ms: float
    sla_violated: bool
    violations: list[str]
