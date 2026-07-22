from pydantic import BaseModel

class Optimization(BaseModel):
    id: str
    target: str
    proposed_change: str
    expected_roi: float
