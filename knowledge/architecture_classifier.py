import os
from schemas.repository_metadata import RepositoryMetadata

class ArchitectureClassifier:
    def __init__(self):
        self.known_styles = [
            "modular-monolith",
            "layered-architecture",
            "clean-architecture",
            "ddd",
            "microservices",
            "hexagonal-architecture"
        ]

    def classify_repository(self, metadata: RepositoryMetadata) -> dict:
        # Mock classification logic based on modules/framework
        style = "layered-architecture"
        confidence = 0.6
        
        modules = metadata.modules
        if any("domain" in m for m in modules) and any("infrastructure" in m for m in modules):
            style = "clean-architecture"
            confidence = 0.85
        elif len(modules) > 5:
            style = "modular-monolith"
            confidence = 0.90
            
        return {
            "repository": metadata.repo_id,
            "architecture": style,
            "confidence": confidence
        }

    def score_architecture(self, repo_id: str):
        pass

    def extract_layers(self, repo_id: str):
        pass
