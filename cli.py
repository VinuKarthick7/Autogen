"""Interactive command-line workflow runner."""

import argparse
import json
import os
import sys

from executor.git_manager import GitManager
from orchestrator.workflow import Workflow
from scanners.convention_schema import ConventionSchema


def main() -> None:
    parser = argparse.ArgumentParser(description="Convention-Aware Multi-Agent Code Generator")
    parser.add_argument("--repo", required=True, help="Path to the target repository")
    parser.add_argument("--feature", required=True, help="Feature description to implement")
    args = parser.parse_args()

    print(f"Starting workflow for feature: '{args.feature}' in repo: {args.repo}")
    conventions = ConventionSchema(
        project_info={"name": "test", "backend_framework": "FastAPI", "frontend_framework": "Flutter", "database": "PostgreSQL"},
        folder_structure={}, database={}, auth={}, api={}, existing_modules={"modules": []},
    )
    workflow = Workflow(repo_path=args.repo)
    result = workflow.run_workflow(args.feature, conventions)
    if not result:
        print("Workflow failed to generate files.")
        sys.exit(1)

    print(f"\n[OK] Branch created: {result.branch_name}")
    print(f"[OK] {result.files_changed} files generated")
    print(f"[OK] Diff generated: {result.diff_path}")
    report_path = os.path.join("artifacts", f"run_{result.run_id}", "verification", "report.json")
    if os.path.exists(report_path):
        with open(report_path, encoding="utf-8") as report_file:
            report = json.load(report_file)
        for step in report.get("steps", []):
            status = "[OK]" if step["success"] else "[FAILED]"
            print(f"{status} {step['name']} passed")

    print(f"[{'OK' if result.verification_passed else 'FAILED'}] Reviewer validation")
    if os.path.exists(result.diff_path):
        with open(result.diff_path, encoding="utf-8") as diff_file:
            print("--- Patch Diff ---")
            print(diff_file.read())
            print("------------------")

    approval = input("Do you approve these changes? (yes/no): ").strip().lower()
    target_repo = os.path.join("workspaces", f"run_{result.run_id}", "repo")
    git_manager = GitManager(target_repo)
    if approval in {"yes", "y"}:
        git_manager.commit("Approved and applied AI patch")
        print("Changes committed successfully.")
    else:
        git_manager.rollback()
        print("Changes rolled back.")


if __name__ == "__main__":
    main()
