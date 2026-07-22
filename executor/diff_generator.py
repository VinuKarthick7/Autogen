import os
import json
from schemas.patch_set import PatchSet

class DiffGenerator:
    def __init__(self, artifacts_dir: str):
        self.artifacts_dir = artifacts_dir

    def generate(self, run_id: str, diff_content: str, patch_set: PatchSet):
        run_artifacts = os.path.join(self.artifacts_dir, f"run_{run_id}")
        os.makedirs(run_artifacts, exist_ok=True)
        
        diff_path = os.path.join(run_artifacts, "patch.diff")
        with open(diff_path, "w", encoding="utf-8") as f:
            f.write(diff_content)
            
        summary_path = os.path.join(run_artifacts, "summary.json")
        summary_data = {
            "run_id": run_id,
            "total_operations": len(patch_set.operations),
            "operations": [
                {"operation": op.operation, "path": op.path, "reason": op.reason} 
                for op in patch_set.operations
            ]
        }
        with open(summary_path, "w", encoding="utf-8") as f:
            json.dump(summary_data, f, indent=2)
            
        return diff_path
