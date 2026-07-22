from typing import List
from schemas.benchmark_result import BenchmarkResult
from schemas.evaluation_report import EvaluationReport

class Evaluator:
    @staticmethod
    def evaluate_suite(results: List[BenchmarkResult]) -> EvaluationReport:
        total = len(results)
        if total == 0:
            return EvaluationReport(
                total_runs=0, passed_runs=0, failed_runs=0,
                average_score=0.0, average_repair_depth=0.0,
                average_tokens=0.0, average_cost=0.0,
                benchmark_results=[]
            )

        passed = sum(1 for r in results if r.passed)
        avg_repair = sum(r.repair_attempts for r in results) / total
        avg_tokens = sum(r.tokens_used for r in results) / total
        avg_cost = sum(r.estimated_cost_usd for r in results) / total
        
        # We can also compute average score by pulling scorecard data, 
        # but for now we'll mock an average score based on pass rate
        avg_score = (passed / total) * 100

        return EvaluationReport(
            total_runs=total,
            passed_runs=passed,
            failed_runs=total - passed,
            average_score=avg_score,
            average_repair_depth=avg_repair,
            average_tokens=avg_tokens,
            average_cost=avg_cost,
            benchmark_results=results
        )
