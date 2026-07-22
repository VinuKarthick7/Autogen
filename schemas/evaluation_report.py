from pydantic import BaseModel
from typing import List
from schemas.benchmark_result import BenchmarkResult

class EvaluationReport(BaseModel):
    total_runs: int
    passed_runs: int
    failed_runs: int
    average_score: float
    average_repair_depth: float
    average_tokens: float
    average_cost: float
    benchmark_results: List[BenchmarkResult]
