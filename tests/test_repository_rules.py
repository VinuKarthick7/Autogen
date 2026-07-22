import pytest
from schemas.patch_set import PatchSet
from schemas.patch_operation import PatchOperation
from verification.rules.repository_rules import RepositoryRulesEngine
import yaml
import os

def test_repository_rules_engine(tmp_path):
    rules_dir = tmp_path / "rules"
    rules_dir.mkdir()
    
    forbidden_yaml = """
forbidden_patterns:
  - pattern: 'store\\.box<'
    severity: CRITICAL
    reason: "Feature code must not touch ObjectBox"
  - pattern: 'password\\s*==\\s*[''\\"]1234[''\\"]'
    severity: CRITICAL
    reason: "Hardcoded default authentication token"
"""
    (rules_dir / "forbidden_patterns.yaml").write_text(forbidden_yaml)
    
    severity_yaml = """
CRITICAL:
  block_merge: true
HIGH:
  block_merge: true
MEDIUM:
  block_merge: false
"""
    (rules_dir / "severity.yaml").write_text(severity_yaml)
    
    engine = RepositoryRulesEngine(rules_dir=str(rules_dir))
    
    patch = PatchSet(operations=[
            PatchOperation(
                operation="modify",
                path="app/test.py",
                new_content="def test():\n    store.box<User>()\n    if password == '1234':\n        pass",
                reason="Test reason"
            )  ])
    
    violations = engine.scan_patch(patch)
    
    assert len(violations) == 2
    
    assert violations[0].severity == "CRITICAL"
    assert violations[0].line == 2
    assert violations[0].suggestion == "Feature code must not touch ObjectBox"
    
    assert violations[1].severity == "CRITICAL"
    assert violations[1].line == 3
    
    blocking = engine.get_blocking_violations(violations)
    assert len(blocking) == 2
