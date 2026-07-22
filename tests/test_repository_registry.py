import pytest
from knowledge.repository_registry import RepositoryRegistry
from schemas.repository_metadata import RepositoryMetadata
from datetime import datetime
import os

def test_registry(tmp_path):
    registry_file = os.path.join(tmp_path, "registry.json")
    registry = RepositoryRegistry(registry_file)
    
    meta = RepositoryMetadata(
        repo_id="test_repo",
        name="Test",
        path="/tmp/test",
        language="python",
        framework="fastapi",
        database="sqlite",
        architecture_style="mvc",
        modules=["auth"],
        conventions={},
        indexed_at=datetime.utcnow()
    )
    registry.register_repository(meta)
    
    repos = registry.list_repositories()
    assert len(repos) == 1
    assert repos[0].repo_id == "test_repo"
