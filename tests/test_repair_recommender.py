import pytest
from knowledge.repair_recommender import RepairRecommender

def test_repair_recommender():
    recommender = RepairRecommender()
    
    recs = recommender.recommend_repairs("MissingImport")
    assert len(recs) == 1
    assert recs[0]["success_rate"] == 0.94
    
    ranked = recommender.rank_repairs([
        {"repair": "A", "success_rate": 0.5},
        {"repair": "B", "success_rate": 0.9}
    ])
    assert ranked[0]["repair"] == "B"
