from pydantic import BaseModel

class QualitySummary(BaseModel):
    summary_id: str
    tests_generated: int
    vulnerabilities_detected: int
    security_score: float
    compliance_score: float
    average_latency_ms: float
    availability_score: float
    blocked_deployments: int
