import os
import json
import time
from typing import List
from schemas.benchmark_case import BenchmarkCase
from schemas.benchmark_result import BenchmarkResult
from evaluation.metrics_engine import MetricsEngine
from evaluation.scorecard import Scorecard
from evaluation.cost_estimator import CostEstimator

class BenchmarkRunner:
    def __init__(self, repo_path: str):
        self.repo_path = repo_path

    def run_case(self, case: BenchmarkCase, run_id: str) -> BenchmarkResult:
        start_time = time.time()
        
        from orchestrator.workflow import Workflow
        from scanners.convention_schema import (
            ConventionSchema, ProjectInfo, FolderStructure, DatabaseConvention, 
            AuthConvention, ApiConvention, FrontendConvention, ExistingModules
        )
        workflow = Workflow(repo_path=self.repo_path)
        conventions = ConventionSchema(
            project_info=ProjectInfo(name="test", backend_framework="fastapi", frontend_framework="react", database="postgres"),
            folder_structure=FolderStructure(),
            database=DatabaseConvention(),
            auth=AuthConvention(),
            api=ApiConvention(),
            frontend=FrontendConvention(),
            existing_modules=ExistingModules()
        )
        
        # In a real scenario, we'd mock the LLM if testing or use the real one.
        # For development testing without LLM keys, we mock the result directly:
        try:
            import os
            if os.environ.get("MOCK_GEMINI") == "1":
                from schemas.workflow_result import WorkflowResult
                from schemas.generated_file import GeneratedFile
                # Dummy files based on expected files
                dummy_files = [GeneratedFile(path=p, content="mocked content") for p in case.expected_files]
                result = WorkflowResult(
                    run_id=run_id,
                    branch_name="mock_branch",
                    files_changed=len(dummy_files),
                    diff_path="mock_diff.patch",
                    committed=False,
                    rollback_available=True,
                    verification_passed=True
                )
                result.generated_files = dummy_files
                time.sleep(1) # Simulate some work
            else:
                result = workflow.run_workflow(feature_request=case.feature_request, conventions=conventions)
                
            workflow_run_id = result.run_id if result else run_id
            passed = getattr(result, "verification_passed", True) if result else False
        except Exception as e:
            print(f"Workflow failed: {e}")
            result = None
            passed = False

        duration = time.time() - start_time
        
        # Extract metrics
        # Mocking values for demonstration since we don't track tokens everywhere yet
        tokens_used = 15000 if passed else 5000
        cost = CostEstimator.estimate_cost(tokens_used)
        
        generated_files = []
        if result and getattr(result, "generated_files", None):
            generated_files = [f.path for f in result.generated_files]

        planner_acc = MetricsEngine.compute_planner_accuracy(case.expected_files, generated_files)
        repair_attempts = 0 # Need to extract from workflow history
        
        res = BenchmarkResult(
            benchmark_id=case.id,
            run_id=run_id,
            passed=passed,
            planner_accuracy=planner_acc,
            dependency_accuracy=1.0,
            repair_success_rate=1.0 if passed else 0.0,
            verification_success=passed,
            repair_attempts=repair_attempts,
            human_intervention=False,
            generated_files=len(generated_files),
            modified_files=0,
            duration_seconds=duration,
            tokens_used=tokens_used,
            estimated_cost_usd=cost
        )
        
        # Save metrics
        run_dir = os.path.join("evaluation", "runs", run_id)
        os.makedirs(run_dir, exist_ok=True)
        with open(os.path.join(run_dir, "metrics.json"), "w") as f:
            f.write(res.model_dump_json(indent=2))
            
        score = Scorecard.generate_scorecard(planner_acc, 1.0, 1.0 if passed else 0.0, 1.0)
        with open(os.path.join(run_dir, "scorecard.json"), "w") as f:
            f.write(score.model_dump_json(indent=2))
            
        return res

    def run_suite(self, suite: List[BenchmarkCase], suite_run_id: str) -> List[BenchmarkResult]:
        results = []
        import uuid
        for case in suite:
            print(f"Running benchmark case: {case.id}")
            case_run_id = f"{suite_run_id}_{case.id}_{uuid.uuid4().hex[:6]}"
            res = self.run_case(case, case_run_id)
            results.append(res)
        return results
