import os
import yaml
from schemas.rule_violation import RuleViolation
from schemas.patch_operation import PatchOperation
from typing import List

class RepairMemory:
    def __init__(self, knowledge_dir: str = "knowledge"):
        self.successful_repairs_path = os.path.join(knowledge_dir, "successful_repairs.yaml")
        self.failed_repairs_path = os.path.join(knowledge_dir, "failed_repairs.yaml")
        
        for path in [self.successful_repairs_path, self.failed_repairs_path]:
            if not os.path.exists(path):
                with open(path, 'w', encoding='utf-8') as f:
                    yaml.dump({"repairs": []}, f)

    def log_successful_repair(self, violations: List[RuleViolation], ops: List[PatchOperation]):
        # Store a simple log for now
        with open(self.successful_repairs_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f) or {"repairs": []}
            
        for v in violations:
            record = {
                "failure": {
                    "category": v.category,
                    "message": v.message
                },
                "fix": {
                    "action": "modify",
                    "files": [op.path for op in ops]
                },
                "frequency": 1
            }
            # Simplistic frequency merge
            merged = False
            for existing in data.get("repairs", []):
                if existing.get("failure", {}).get("message") == v.message:
                    existing["frequency"] = existing.get("frequency", 1) + 1
                    merged = True
                    break
            if not merged:
                data.setdefault("repairs", []).append(record)

        with open(self.successful_repairs_path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f)
            
    def log_failed_repair(self, violations: List[RuleViolation], reason: str):
        with open(self.failed_repairs_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f) or {"repairs": []}
            
        for v in violations:
            record = {
                "failure": {
                    "category": v.category,
                    "message": v.message
                },
                "reason": reason
            }
            data.setdefault("repairs", []).append(record)

        with open(self.failed_repairs_path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f)
