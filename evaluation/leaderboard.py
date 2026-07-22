import os
import json
from typing import List, Dict, Any

class Leaderboard:
    @staticmethod
    def build_leaderboard(results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        # Rank by score descending
        sorted_results = sorted(results, key=lambda x: x.get("total_score", 0), reverse=True)
        for idx, res in enumerate(sorted_results):
            res["Rank"] = idx + 1
        return sorted_results

    @staticmethod
    def export_leaderboard(leaderboard_data: List[Dict[str, Any]], run_dir: str):
        os.makedirs(run_dir, exist_ok=True)
        path = os.path.join(run_dir, "leaderboard.json")
        with open(path, "w") as f:
            json.dump(leaderboard_data, f, indent=2)
