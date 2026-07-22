from pydantic import BaseModel

class OrganizationReport(BaseModel):
    report_id: str
    timestamp: str
    metrics: dict[str, float]
    hiring_recommendations: list[str]

