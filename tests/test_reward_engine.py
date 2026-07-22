import pytest
from evolution.reward_engine import RewardEngine
from schemas.engineering_experience import EngineeringExperience
from datetime import datetime

def test_reward_engine():
    engine = RewardEngine()
    exp = EngineeringExperience(
        run_id="run-1", organization_id="org-1", repository_id="repo-1", feature_request="test",
        planner_version="v1", repair_strategy="v1", retrieval_strategy="v1", prompt_versions={},
        benchmark_score=100.0, verification_passed=True, repair_success=True, repair_depth=0,
        tokens_used=1000, cost_usd=0.0, runtime_seconds=10.0, human_intervention=False,
        created_at=datetime.utcnow()
    )
    reward = engine.compute_reward(exp)
    # 40 (verification) + 25 (benchmark) + 20 (repair) = 85
    assert reward == 85.0
