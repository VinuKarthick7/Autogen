import pytest
from evolution.recommendation_engine import RecommendationEngine

def test_recommendation_engine():
    engine = RecommendationEngine()
    recs = engine.generate_recommendations()
    assert len(recs) == 3
    assert recs[0]["category"] == "Planner Optimization"
