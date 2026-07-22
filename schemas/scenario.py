from pydantic import BaseModel

class Scenario(BaseModel):
    id: str
    type: str
    description: str
    resilience_score: float
