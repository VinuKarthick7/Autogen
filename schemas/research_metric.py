from pydantic import BaseModel

class ResearchMetric(BaseModel):
    experiments_run: int
    hypotheses_validated: int
    architectures_explored: int
    strategies_retired: int
    self_improvements: int
    innovation_score: float
