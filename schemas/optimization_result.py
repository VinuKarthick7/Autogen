from pydantic import BaseModel

class OptimizationResult(BaseModel):
    target_id: str
    original_performance: float
    new_performance: float
    improvement_percentage: float
