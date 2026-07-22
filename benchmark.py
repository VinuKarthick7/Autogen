import argparse
import os
import uuid
import datetime
from evaluation.benchmark_loader import BenchmarkLoader
from evaluation.benchmark_runner import BenchmarkRunner
from evaluation.evaluator import Evaluator
from evaluation.leaderboard import Leaderboard
from evaluation.report_generator import ReportGenerator

def main():
    parser = argparse.ArgumentParser(description="Run Benchmark Suite")
    parser.add_argument("--repo", type=str, required=True, help="Path to repository")
    parser.add_argument("--suite", type=str, required=True, help="Benchmark suite (e.g., pms)")
    parser.add_argument("--difficulty", type=str, help="Difficulty level")
    args = parser.parse_args()

    print(f"Loading benchmarks for {args.suite} (Difficulty: {args.difficulty or 'all'})...")
    loader = BenchmarkLoader()
    cases = loader.load_suite(args.suite, args.difficulty)
    
    if not cases:
        print("No cases found.")
        return

    print(f"Found {len(cases)} cases.")
    
    runner = BenchmarkRunner(repo_path=args.repo)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    suite_run_id = f"bench_{args.suite}_{timestamp}"
    
    print(f"Starting suite execution: {suite_run_id}")
    results = runner.run_suite(cases, suite_run_id)
    
    print("Evaluating results...")
    report = Evaluator.evaluate_suite(results)
    
    out_dir = os.path.join("evaluation", "runs", suite_run_id)
    os.makedirs(out_dir, exist_ok=True)
    
    # Save report
    with open(os.path.join(out_dir, "report.json"), "w") as f:
        f.write(report.model_dump_json(indent=2))
        
    print("Generating markdown/html reports...")
    ReportGenerator.generate_report(report, os.path.join("reports", suite_run_id))
    
    print("Updating leaderboard...")
    # Read existing or create new list for leaderboard
    all_runs_data = []
    for r in results:
        all_runs_data.append({
            "run_id": r.run_id,
            "benchmark_id": r.benchmark_id,
            "passed": r.passed,
            "total_score": r.planner_accuracy * 100, # Simplified
            "repairs": r.repair_attempts,
            "cost": r.estimated_cost_usd,
            "time": r.duration_seconds
        })
    lb = Leaderboard.build_leaderboard(all_runs_data)
    Leaderboard.export_leaderboard(lb, out_dir)
    
    print(f"✅ Benchmark suite completed. Artifacts in {out_dir}")

if __name__ == "__main__":
    main()
