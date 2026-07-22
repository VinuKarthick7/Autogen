import yaml
import os

class RepairPolicy:
    def __init__(self, policy_file: str = "repair/repair_policies.yaml"):
        self.policies = self._load_policies(policy_file)
        
    def _load_policies(self, path: str) -> dict:
        if not os.path.exists(path):
            return {}
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f).get("repair_policies", {})

    def can_auto_repair(self, category: str) -> bool:
        policy = self.policies.get(category)
        if not policy:
            # Default to no auto-repair for unknown categories just to be safe
            return False
        return policy.get("auto_repair", False)

    def get_max_attempts(self, category: str) -> int:
        policy = self.policies.get(category)
        if not policy:
            return 0
        return policy.get("max_attempts", 0)
