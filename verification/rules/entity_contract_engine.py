import os
import yaml
import re
from typing import List
from schemas.patch_set import PatchSet
from schemas.rule_violation import RuleViolation

class EntityContractEngine:
    def __init__(self, conventions_dir: str = "conventions"):
        self.conventions_dir = conventions_dir
        self.entities_config = self._load_yaml("entities.yaml")

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
            
            # Simple heuristic: check if file defines an entity matching our config
            for entity_name, config in self.entities_config.items():
                if entity_name in content:
                    required_fields = config.get("required_fields", [])
                    for field in required_fields:
                        if not re.search(r'\b' + re.escape(field) + r'\b', content):
                            violations.append(
                                RuleViolation(
                                    severity="HIGH",
                                    category="EntityContract",
                                    file=op.path,
                                    line=1,
                                    message=f"{entity_name} is missing required field: {field}",
                                    suggestion=f"Add {field} to {entity_name} to comply with entity contract."
                                )
                            )
        return violations
