import os
import re
import yaml
from typing import List, Dict, Any
from schemas.rule_violation import RuleViolation
from schemas.patch_set import PatchSet

class RepositoryRulesEngine:
    def __init__(self, rules_dir: str = "rules"):
        self.rules_dir = rules_dir
        self.forbidden_patterns = self._load_yaml("forbidden_patterns.yaml").get("forbidden_patterns", [])
        self.severities = self._load_yaml("severity.yaml")

    def _load_yaml(self, filename: str) -> Dict[str, Any]:
        path = os.path.join(self.rules_dir, filename)
        if not os.path.exists(path):
            return {}
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}

    def scan_patch(self, patch_set: PatchSet) -> List[RuleViolation]:
        violations = []
        for op in patch_set.operations:
            if not op.new_content:
                continue
            
            lines = op.new_content.splitlines()
            for line_idx, line_content in enumerate(lines):
                # Check forbidden patterns
                for rule in self.forbidden_patterns:
                    pattern = rule.get("pattern")
                    if pattern and re.search(pattern, line_content):
                        violations.append(
                            RuleViolation(
                                severity=rule.get("severity", "MEDIUM"),
                                category="ForbiddenPattern",
                                file=op.path,
                                line=line_idx + 1,
                                message=f"Matched forbidden pattern: {pattern}",
                                suggestion=rule.get("reason", "")
                            )
                        )
        from verification.rules.entity_contract_engine import EntityContractEngine
        from verification.rules.offline_contract_engine import OfflineContractEngine
        from verification.rules.domain_rules import DomainRulesEngine
        from verification.rules.knowledge_memory import KnowledgeMemoryEngine
        
        entity_engine = EntityContractEngine(self.rules_dir.replace("rules", "conventions"))
        violations.extend(entity_engine.scan_patch(patch_set))
        
        offline_engine = OfflineContractEngine(self.rules_dir.replace("rules", "conventions"))
        violations.extend(offline_engine.scan_patch(patch_set))
        
        domain_engine = DomainRulesEngine()
        violations.extend(domain_engine.scan_patch(patch_set))
        
        knowledge_engine = KnowledgeMemoryEngine(self.rules_dir.replace("rules", "knowledge"))
        violations.extend(knowledge_engine.scan_patch(patch_set))
        
        return violations

    def get_blocking_violations(self, violations: List[RuleViolation]) -> List[RuleViolation]:
        blocking = []
        for v in violations:
            sev_config = self.severities.get(v.severity, {})
            if sev_config.get("block_merge") is True:
                blocking.append(v)
        return blocking
