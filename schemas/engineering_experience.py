from pydantic import BaseModel
from datetime import datetime

class EngineeringExperience(BaseModel):
    run_id: str
    organization_id: str
    repository_id: str
    feature_request: str
    planner_version: str
    repair_strategy: str
    retrieval_strategy: str
    prompt_versions: dict
    benchmark_score: float
    verification_passed: bool
    repair_success: bool
    repair_depth: int
    tokens_used: int
    cost_usd: float
    runtime_seconds: float
    human_intervention: bool
    created_at: datetime
