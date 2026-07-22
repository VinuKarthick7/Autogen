from pydantic import BaseModel

class EffortEstimate(BaseModel):
    feature_name: str
    backend_points: int
    frontend_points: int
    infra_points: int
    qa_points: int
    total_points: int
    estimated_sprints: int
    confidence: float
