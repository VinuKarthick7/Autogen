from pydantic import BaseModel

class PolicyDecision(BaseModel):
    policy_id: str
    target_id: str
    action: str
    reasoning: str
