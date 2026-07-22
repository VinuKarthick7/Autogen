from pydantic import BaseModel

class ScorecardResult(BaseModel):
    planner_score: float
    repair_score: float
    verification_score: float
    dependency_score: float
    safety_score: float
    total_score: float
    grade: str
