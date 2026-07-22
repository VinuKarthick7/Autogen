import os
import json
from schemas.cross_repo_match import CrossRepoMatch

class CrossRepoGraph:
    def __init__(self, graph_file="knowledge/graphs/global_graph.json"):
        self.graph_file = graph_file
        os.makedirs(os.path.dirname(self.graph_file), exist_ok=True)
        self.nodes = {}
        self.edges = []
        self._load()

    def _load(self):
        if os.path.exists(self.graph_file):
            with open(self.graph_file, "r") as f:
                data = json.load(f)
                self.nodes = data.get("nodes", {})
                self.edges = data.get("edges", [])

    def _save(self):
        with open(self.graph_file, "w") as f:
            json.dump({"nodes": self.nodes, "edges": self.edges}, f, indent=4)

    def add_node(self, node_id: str, node_type: str, metadata: dict = None):
        self.nodes[node_id] = {"type": node_type, "metadata": metadata or {}}

    def add_edge(self, source: str, target: str, relationship: str, weight: float = 1.0):
        self.edges.append({
            "source": source,
            "target": target,
            "relationship": relationship,
            "weight": weight
        })

    def build_graph(self):
        self._save()

    def find_neighbors(self, node_id: str) -> list[dict]:
        neighbors = []
        for e in self.edges:
            if e["source"] == node_id:
                neighbors.append({"node": e["target"], "relationship": e["relationship"], "weight": e["weight"]})
            elif e["target"] == node_id:
                neighbors.append({"node": e["source"], "relationship": e["relationship"], "weight": e["weight"]})
        return neighbors

    def find_similar_repositories(self, repo_id: str) -> list[CrossRepoMatch]:
        matches = []
        neighbors = self.find_neighbors(repo_id)
        for n in neighbors:
            if n["relationship"] == "similarity":
                matches.append(CrossRepoMatch(
                    source_repo=repo_id,
                    target_repo=n["node"],
                    similarity_score=n["weight"],
                    matching_modules=[],
                    matching_patterns=[]
                ))
        return sorted(matches, key=lambda x: x.similarity_score, reverse=True)

    def export_graph(self) -> dict:
        return {"nodes": self.nodes, "edges": self.edges}
