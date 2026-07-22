from pydantic import BaseModel

class DeploymentDecision(BaseModel):
    decision_id: str
    status: str
    reason: str
    blocked_by: list[str]
