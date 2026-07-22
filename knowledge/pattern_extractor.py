import os
import json

class PatternExtractor:
    def __init__(self, patterns_dir="knowledge/patterns"):
        self.patterns_dir = patterns_dir
        os.makedirs(self.patterns_dir, exist_ok=True)
        
    def extract_patterns(self, repo_id: str, code_data: dict) -> list[dict]:
        patterns = []
        # Mock logic
        if "coupon" in json.dumps(code_data).lower():
            patterns.append({"pattern": "Coupon pattern", "repo": repo_id})
        if "auth" in json.dumps(code_data).lower():
            patterns.append({"pattern": "Auth pattern", "repo": repo_id})
        return patterns
        
    def cluster_patterns(self, patterns: list[dict]):
        pass
        
    def save_patterns(self, category: str, patterns: list[dict]):
        path = os.path.join(self.patterns_dir, f"{category}_patterns.json")
        with open(path, "w") as f:
            json.dump(patterns, f, indent=4)
