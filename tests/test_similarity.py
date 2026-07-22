import pytest
from datetime import datetime
from knowledge.convention_similarity import ConventionSimilarity
from schemas.repository_metadata import RepositoryMetadata

def test_similarity():
    sim = ConventionSimilarity()
    
    repo1 = RepositoryMetadata(
        repo_id="r1", name="r1", path="", language="python", framework="fastapi", 
        database="postgres", architecture_style="clean", modules=["auth"], 
        conventions={}, indexed_at=datetime.utcnow()
    )
    
    repo2 = RepositoryMetadata(
        repo_id="r2", name="r2", path="", language="python", framework="fastapi", 
        database="postgres", architecture_style="clean", modules=["auth", "users"], 
        conventions={}, indexed_at=datetime.utcnow()
    )
    
    score = sim.compute_similarity(repo1, repo2)
    # framework 0.25 + database 0.20 + auth_mock 0.20 + api_mock 0.15 + module_intersect 0.15 = 0.95
    assert score == 0.95
