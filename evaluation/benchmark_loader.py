import yaml
import os
from typing import List, Dict, Any
from schemas.benchmark_case import BenchmarkCase

class BenchmarkLoader:
    def __init__(self, catalog_path: str = "benchmarks/benchmark_catalog.yaml"):
        self.catalog_path = catalog_path
        self._catalog = self.load_catalog()

    def load_catalog(self) -> Dict[str, Any]:
        if not os.path.exists(self.catalog_path):
            return {}
        with open(self.catalog_path, "r") as f:
            return yaml.safe_load(f) or {}

    def load_suite(self, repo: str, difficulty: str = None) -> List[BenchmarkCase]:
        cases = []
        repos = self._catalog.get("repositories", {})
        if repo not in repos:
            return cases
            
        repo_data = repos[repo]
        
        if difficulty:
            if difficulty in repo_data:
                for item in repo_data[difficulty]:
                    cases.append(self._parse_case(repo, difficulty, item))
        else:
            for diff, items in repo_data.items():
                for item in items:
                    cases.append(self._parse_case(repo, diff, item))
        return cases

    def get_cases(self, repo: str = None, tags: List[str] = None) -> List[BenchmarkCase]:
        all_cases = []
        repos = self._catalog.get("repositories", {})
        
        for r, r_data in repos.items():
            if repo and r != repo:
                continue
            for diff, items in r_data.items():
                for item in items:
                    c = self._parse_case(r, diff, item)
                    if tags:
                        if any(t in c.tags for t in tags):
                            all_cases.append(c)
                    else:
                        all_cases.append(c)
        return all_cases

    def _parse_case(self, repo: str, diff: str, item: dict) -> BenchmarkCase:
        return BenchmarkCase(
            id=item.get("id", ""),
            repository_type=repo,
            difficulty=diff,
            category=item.get("category", "general"),
            feature_request=item.get("feature_request", ""),
            expected_modules=item.get("expected_modules", []),
            expected_files=item.get("expected_files", []),
            expected_dependencies=item.get("expected_dependencies", []),
            expected_repairs=item.get("expected_repairs", []),
            max_repair_depth=item.get("max_repair_depth", 0),
            tags=item.get("tags", [])
        )
