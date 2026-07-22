import os
import yaml
import re
from typing import List
from schemas.patch_set import PatchSet
from schemas.rule_violation import RuleViolation

class OfflineContractEngine:
    def __init__(self, conventions_dir: str = "conventions"):
        self.conventions_dir = conventions_dir
        self.offline_rules = self._load_yaml("offline.yaml").get("offline_rules", [])

    def _load_yaml(self, filename: str) -> dict:
        path = os.path.join(self.conventions_dir, filename)
        if not os.path.exists(path):
            return {}
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}

    def scan_patch(self, patch_set: PatchSet) -> List[RuleViolation]:
        violations = []
        
        for op in patch_set.operations:
            if not op.new_content:
                continue
                
            content = op.new_content
            
            # Simple static check for some offline invariants
            # e.g., if there's a network call (http.get, fetch), we ensure it's not inside a transaction block
            # For this mock implementation, we just flag known bad static patterns related to offline
            
            if "sync_writes_require_transaction" in self.offline_rules:
                if "sync(" in content and "transaction(" not in content and "session.begin()" not in content:
                    violations.append(
                        RuleViolation(
                            severity="CRITICAL",
                            category="OfflineContract",
                            file=op.path,
                            line=1,
                            message="Sync write performed without a transaction block.",
                            suggestion="Wrap sync writes in a transaction."
                        )
                    )
                    
            if "no_network_calls_inside_transactions" in self.offline_rules:
                if "transaction(" in content and ("http.get" in content or "fetch(" in content or "requests.post" in content):
                    violations.append(
                        RuleViolation(
                            severity="CRITICAL",
                            category="OfflineContract",
                            file=op.path,
                            line=1,
                            message="Network call found inside a transaction block.",
                            suggestion="Move network calls outside the transaction block."
                        )
                    )
                    
        return violations
