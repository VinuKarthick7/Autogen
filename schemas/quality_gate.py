from pydantic import BaseModel

class QualityGate(BaseModel):
    gate_id: str
    condition: str
    threshold: float
    passed: bool
