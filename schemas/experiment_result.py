from pydantic import BaseModel

class ExperimentResult(BaseModel):
    id: str
    experiment_id: str
    winner: str
    confidence_level: float
    summary: str
