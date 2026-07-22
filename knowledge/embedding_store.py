import os
import json

class EmbeddingStore:
    def __init__(self, store_dir="knowledge/embeddings"):
        self.store_dir = store_dir
        os.makedirs(self.store_dir, exist_ok=True)
        self.vectors = {}
        self._load()

    def _load(self):
        path = os.path.join(self.store_dir, "vectors.json")
        if os.path.exists(path):
            with open(path, "r") as f:
                self.vectors = json.load(f)

    def _save(self):
        path = os.path.join(self.store_dir, "vectors.json")
        with open(path, "w") as f:
            json.dump(self.vectors, f, indent=4)

    def embed_repository(self, repo_id: str, content: str):
        # Mock embedding
        self.vectors[f"repo_{repo_id}"] = [0.1, 0.2, 0.3]
        self._save()

    def embed_module(self, repo_id: str, module_name: str, content: str):
        self.vectors[f"mod_{repo_id}_{module_name}"] = [0.15, 0.25, 0.35]
        self._save()

    def embed_pattern(self, pattern_id: str, content: str):
        self.vectors[f"pat_{pattern_id}"] = [0.2, 0.3, 0.4]
        self._save()

    def find_similar(self, query_vector: list[float]) -> list[str]:
        # Mock similarity
        return list(self.vectors.keys())
