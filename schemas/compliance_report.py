from pydantic import BaseModel

class ComplianceReport(BaseModel):
    report_id: str
    standards_checked: list[str]
    passed_checks: list[str]
    failed_checks: list[str]
    risk_score: float
