from pydantic import BaseModel

class RootCauseReport(BaseModel):
    report_id: str
    incident_id: str
    root_cause: str
    confidence: float
    impacted_components: list[str]
    remediation_steps: list[str]
