import os
import json
from datetime import datetime
from schemas.repository_metadata import RepositoryMetadata

class RepositoryRegistry:
    def __init__(self, registry_file="knowledge/repositories/registry.json"):
        self.registry_file = registry_file
        os.makedirs(os.path.dirname(self.registry_file), exist_ok=True)
        self._load()

    def _load(self):
        if os.path.exists(self.registry_file):
            with open(self.registry_file, "r") as f:
                data = json.load(f)
                self.repositories = {k: RepositoryMetadata(**v) for k, v in data.items()}
        else:
            self.repositories = {}

    def _save(self):
        with open(self.registry_file, "w") as f:
            data = {k: v.model_dump() for k, v in self.repositories.items()}
            # datetime serialization requires custom handling
            json.dump(data, f, indent=4, default=str)

    def register_repository(self, metadata: RepositoryMetadata):
        self.repositories[metadata.repo_id] = metadata
        self._save()

    def remove_repository(self, repo_id: str):
        if repo_id in self.repositories:
            del self.repositories[repo_id]
            self._save()

    def list_repositories(self) -> list[RepositoryMetadata]:
        return list(self.repositories.values())

    def update_repository(self, repo_id: str, metadata: RepositoryMetadata):
        if repo_id in self.repositories:
            self.repositories[repo_id] = metadata
            self._save()
        else:
            raise ValueError(f"Repository {repo_id} not found")

    def get_repository(self, repo_id: str) -> RepositoryMetadata:
        if repo_id in self.repositories:
            return self.repositories[repo_id]
        raise ValueError(f"Repository {repo_id} not found")
