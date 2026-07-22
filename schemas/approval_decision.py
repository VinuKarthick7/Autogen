from pydantic import BaseModel

class ApprovalDecision(BaseModel):
    approved: bool
    reviewer_notes: str
