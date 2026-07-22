from pydantic import BaseModel

class ReliabilityReport(BaseModel):
    report_id: str
    availability_score: float
    resilience_score: float
    failed_scenarios: list[str]
    recommendations: list[str]
