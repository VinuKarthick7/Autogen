from pydantic import BaseModel

class ProductRisk(BaseModel):
    risk_id: str
    description: str
    severity: str
    mitigation_strategy: str
