from pydantic import BaseModel

class RollbackDecision(BaseModel):
    decision_id: str
    deployment_id: str
    reason: str
    approved: bool
