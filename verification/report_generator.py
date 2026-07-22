import os
import json
from schemas.verification_report import VerificationReport

class ReportGenerator:
    def __init__(self, artifacts_dir: str):
        self.artifacts_dir = artifacts_dir

    def save_report(self, run_id: str, report: VerificationReport) -> str:
        ver_dir = os.path.join(self.artifacts_dir, f"run_{run_id}", "verification")
        os.makedirs(ver_dir, exist_ok=True)
        
        report_path = os.path.join(ver_dir, "report.json")
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(report.model_dump_json(indent=2))
            
        for step in report.steps:
            log_path = os.path.join(ver_dir, f"{step.name.lower()}.log")
            with open(log_path, "w", encoding="utf-8") as f:
                f.write(f"--- STDOUT ---\n{step.stdout}\n\n--- STDERR ---\n{step.stderr}\n")
                
        return report_path
