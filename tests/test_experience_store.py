import pytest
import os
from evolution.experience_store import ExperienceStore
from schemas.engineering_experience import EngineeringExperience
from datetime import datetime

def test_experience_store(tmp_path):
    store = ExperienceStore(base_dir=str(tmp_path))
    exp = EngineeringExperience(
        run_id="run-1", organization_id="org-1", repository_id="repo-1", feature_request="test",
        planner_version="v1", repair_strategy="v1", retrieval_strategy="v1", prompt_versions={},
        benchmark_score=80.0, verification_passed=True, repair_success=True, repair_depth=1,
        tokens_used=1000, cost_usd=0.01, runtime_seconds=10.0, human_intervention=False,
        created_at=datetime.utcnow()
    )
    store.store_experience(exp)
    
    retrieved = store.get_experience("run-1")
    assert retrieved is not None
    assert retrieved.run_id == "run-1"
