from pydantic import BaseModel

class BenchmarkResult(BaseModel):
    benchmark_id: str
    run_id: str
    passed: bool
    planner_accuracy: float
    dependency_accuracy: float
    repair_success_rate: float
    verification_success: bool
    repair_attempts: int
    human_intervention: bool
    generated_files: int
    modified_files: int
    duration_seconds: float
    tokens_used: int
    estimated_cost_usd: float
