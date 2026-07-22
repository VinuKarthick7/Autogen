from pydantic import BaseModel

class Hypothesis(BaseModel):
    id: str
    statement: str
    confidence: float
    status: str
    proposed_by: str
