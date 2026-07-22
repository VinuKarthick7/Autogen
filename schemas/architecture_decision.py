from pydantic import BaseModel

class ArchitectureDecision(BaseModel):
    decision_id: str
    rfc_id: str
    decision: str
    rationale: str

