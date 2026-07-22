import os
import ast
import json
from typing import List
from schemas.dependency_edge import DependencyEdge

class DependencyGraph:
    def __init__(self, repo_path: str):
        self.repo_path = repo_path
        self.edges: List[DependencyEdge] = []

    def build_graph(self):
        self.edges = []
        for root, _, files in os.walk(self.repo_path):
            if '.git' in root or '__pycache__' in root or '.pytest_cache' in root:
                continue
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    self._parse_imports(file_path)

    def _parse_imports(self, file_path: str):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            tree = ast.parse(content)
        except Exception:
            return

        rel_path = os.path.relpath(file_path, self.repo_path)
        source = rel_path.replace(os.sep, '.')
        if source.endswith('.py'):
            source = source[:-3]

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    self.edges.append(DependencyEdge(source=source, target=alias.name, relation_type="imports"))
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    self.edges.append(DependencyEdge(source=source, target=node.module, relation_type="imports"))

    def get_edges(self) -> List[DependencyEdge]:
        return self.edges

    def export(self, path: str):
        with open(path, 'w', encoding='utf-8') as f:
            json.dump([e.__dict__ for e in self.edges], f, indent=2)
