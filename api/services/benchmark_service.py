import os
import json
from api.workers.queue import JobQueue

class BenchmarkService:
    def __init__(self):
        self.queue = JobQueue()
        self.runs_dir = os.path.join("evaluation", "runs")
        
    async def run_suite(self, suite: str, difficulty: str = None):
        # Enqueue benchmark job
        await self.queue.enqueue("execute_benchmark", suite=suite, difficulty=difficulty)
        return {"status": "queued", "suite": suite}
        
    def get_results(self, suite_run_id: str):
        path = os.path.join(self.runs_dir, suite_run_id, "report.json")
        if os.path.exists(path):
            with open(path, "r") as f:
                return json.load(f)
        return None
        
    def get_leaderboard(self):
        # Scan evaluation/runs for the latest leaderboard
        runs = []
        if os.path.exists(self.runs_dir):
            for d in os.listdir(self.runs_dir):
                runs.append(d)
        runs.sort(reverse=True)
        for r in runs:
            lb_path = os.path.join(self.runs_dir, r, "leaderboard.json")
            if os.path.exists(lb_path):
                with open(lb_path, "r") as f:
                    return json.load(f)
        return []
